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
        self.chain_service = ChainService(run_id="run_1", repository=repository, send_callback=send_message_func)
        # Invoke the ChainService to start the execution
        asyncio.create_task(self.chain_service.execute_chain(filepath))
        # Send a JSON-encoded message
        await websocket.send_text(json.dumps({"status": "Chain execution started"}))

    async def listen_websocket(self, websocket: WebSocket):
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                await self.process_user_input(message)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    async def process_user_input(self, user_input):
        """Process the user input."""
        if isinstance(user_input, str):
            user_input = json.loads(user_input)
        if 'correlation_id' in user_input:
            logger.info(f"Attempting to correlate user input for id: {user_input['correlation_id']}")
            # Extract the correlation_id and resolve the future in the InputResolver
            correlation_id = user_input['correlation_id']
            # Assume InputResolver is accessible through an instance variable
            self.chain_service.step_executor.input_resolver.resolve_user_input(correlation_id, user_input['user_entry'])
        else:
            logger.error("Received user input without correlation_id")
    
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
                message_type = data_json.get('type')
                
                if message_type == 'startChain':
                    # Start chain logic remains the same
                    filepath = data_json.get('filePath')
                    await self.start_chain(filepath, websocket)
                    
                elif message_type == 'user_entry':
                    # Process user input with the correlation ID
                    await self.process_user_input(data_json)
                else:
                    logger.warn(f"Unrecognized message type received: {message_type}")
                    # Handle other message types or errors
                    
        except WebSocketDisconnect:
            self.disconnect(websocket)


    async def receive_message(self, message):
        data = json.loads(message)  # Assuming messages are in JSON format
        if data.get("type") == "user_entry_response":
            correlation_id = data["correlation_id"]
            user_input = data["user_entry"]
            # Notify the InputResolver about the user input
            self.input_resolver.resolve_user_input(correlation_id, user_input)
