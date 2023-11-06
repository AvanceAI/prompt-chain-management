# src/websocket/connection_manager.py
import json
import asyncio
import functools
from fastapi import WebSocket
from src.services.chain_service.chain_service import ChainService
from src.repository.prompt_db.json_repository import JsonRepository
from src.core.logger import get_logger

logger = get_logger(__name__)

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(json.dumps({"message": message}))
    
    async def start_chain(self, filepath: str, websocket: WebSocket):
        """Start chain execution event."""
        repository = JsonRepository(filepath=filepath)
        send_message_func = functools.partial(self.send_personal_message, websocket=websocket)
        chain_service = ChainService(run_id="run_1", repository=repository, send_callback=send_message_func)
        # Invoke the ChainService to start the execution
        asyncio.create_task(chain_service.execute_chain(filepath))
        # Send a JSON-encoded message
        await websocket.send_text(json.dumps({"status": "Chain execution started"}))

    async def process_user_input(self, user_input: str):
        """Process the user input."""
        print(f"User Input: {user_input}")
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message: str):
        """Broadcast a message to all connected websockets."""
        for connection in self.active_connections:
            await connection.send_text(message)
        