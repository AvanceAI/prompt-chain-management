# src/websocket/server.py
import json
import asyncio
import websockets
from src.services.chain_service.chain_service import ChainService
from src.repository.prompt_db.json_repository import JsonRepository

async def websocket_handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data['command'] == 'startChain':
            filepath = data['filePath']
            repository = JsonRepository(filepath=filepath)
            chain_service = ChainService(run_id="run_1", repository=repository)
            # Invoke the ChainService to start the execution
            asyncio.create_task(chain_service.execute_chain(filepath))
        await websocket.send("Chain execution started")
        
async def start_websocket_server():
    server = websockets.serve(
        websocket_handler, 
        "127.0.0.1", # Use IPv4 address here
        8080
    )
    print("SUCCESS:     Websocket server started!")
    await server

if __name__ == "__main__":
    asyncio.run(start_websocket_server())
