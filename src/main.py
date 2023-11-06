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
        await manager.listen_websocket(websocket)  # assuming you implement this method as suggested
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