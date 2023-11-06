# src/websocket/connection_manager.py
import json
import asyncio
import functools
from fastapi import WebSocket, WebSocketDisconnect
from src.services.chain_service.chain_service import ChainService
from src.repository.prompt_db.json_repository import JsonRepository
from src.core.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
        self.response_queues = {}  # Maps WebSocket to a Queue

    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.response_queues[websocket] = asyncio.Queue()  # Initialize a new queue for the websocket

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message and wait for the user's reply."""
        await websocket.send_text(json.dumps({"message": message}))
        user_input = await self.wait_for_user_input(websocket)
        return user_input

    async def wait_for_user_input(self, websocket: WebSocket):
        """Wait for user input from the frontend."""
        if websocket in self.response_queues:
            user_input = await self.response_queues[websocket].get()
            logger.info(f"User input received: {user_input}")
            return user_input
        return None
    
    async def start_chain(self, filepath: str, websocket: WebSocket):
        """Start chain execution event."""
        repository = JsonRepository(filepath=filepath)
        send_message_func = functools.partial(self.send_personal_message, websocket=websocket)
        chain_service = ChainService(run_id="run_1", repository=repository, send_callback=send_message_func)
        # Invoke the ChainService to start the execution
        asyncio.create_task(chain_service.execute_chain(filepath))
        # Send a JSON-encoded message
        await websocket.send_text(json.dumps({"status": "Chain execution started"}))

    async def listen_websocket(self, websocket: WebSocket):
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                await self.process_user_input(message, websocket)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    async def process_user_input(self, user_input: str, websocket: WebSocket):
        """Process the user input."""
        # Assuming you want to place the user input into the response queue for the websocket
        if websocket in self.response_queues:
            await self.response_queues[websocket].put(user_input)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message: str):
        """Broadcast a message to all connected websockets."""
        for connection in self.active_connections:
            await connection.send_text(message)
            
    async def listen_websocket(self, websocket: WebSocket):
        """Listens for messages from a specific WebSocket."""
        try:
            while True:
                data = await websocket.receive_text()
                data_json = json.loads(data)
                logger.info(f"Received message: {data_json}")
                if data_json.get('type') == 'startChain':
                    # Assuming that the 'startChain' message contains the filepath
                    filepath = data_json.get('filePath')
                    await self.start_chain(filepath, websocket)
                elif data_json.get('type') == 'userInput':
                    # Assuming that the 'userInput' is the text sent by the user.
                    user_input = data_json.get('userInput')
                    await self.process_user_input(user_input, websocket)
                else:
                    pass
                # Add more conditions for other message types as needed
        except WebSocketDisconnect:
            self.disconnect(websocket)
