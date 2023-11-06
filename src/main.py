# src/main.py
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.websocket.connection_manager import ConnectionManager
from src.core.security import setup_cors

app = FastAPI()

manager = ConnectionManager()

@app.websocket("/communicate")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)  # Parse the text data into JSON
            # Check the type of the message
            if data_json.get('type') == 'startChain':
                filepath = data_json.get('filePath')
                # Call a method to handle the startChain command
                await manager.start_chain(filepath, websocket)
            elif data_json.get('type') == 'userInput':
                user_input = data_json.get('text')
                # Now we call the process_user_input method
                await manager.process_user_input(user_input)
            else:
                # Handle other message types or errors
                pass
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("A client just disconnected.")


##############################################
############## Test Endpoints ################
##############################################
@app.get("/hello-world")
async def hello_word():
    return {"message": "Hello, World!"}

@app.options("/hello-world")
async def hello_word():
    return {"message": "Hello, World!"}
##############################################
##############################################
##############################################

setup_cors(app)