# src/main.py

from fastapi import FastAPI
from src.core.security import setup_cors

app = FastAPI()

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