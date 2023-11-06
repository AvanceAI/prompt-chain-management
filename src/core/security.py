# src/core/security.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

def setup_cors(app: FastAPI) -> None:
    allowed_origins = settings.CORS_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
