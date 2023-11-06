# src/main.py
from src.utils.utils import read_json
from fastapi import FastAPI, WebSocket
import asyncio
from src.core.security import setup_cors
from src.websocket.server import start_websocket_server

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print('INFO:    Starting websocket server')
    asyncio.create_task(start_websocket_server())

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