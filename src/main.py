# src/main.py
from fastapi import FastAPI
import asyncio
from src.core.security import setup_cors
from src.websocket.server import start_websocket_server

app = FastAPI()

# Register FastAPI event handlers for startup and shutdown
@app.on_event("startup")
async def on_startup():
    # Start the WebSocket server in the background
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