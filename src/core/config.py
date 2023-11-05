# src/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Supabase settings
    SUPABASE_URL: str = None
    SUPABASE_KEY: str = None
    CORS_ORIGINS: str = "http://localhost:3000"

    # Define other global settings here
    APP_NAME: str = "My-Visa-USA Form Backend"
    DEBUG: bool = False

    class Config:
        # Tells Pydantic to read the variables from environment
        env_file = ".env"

settings = Settings()
