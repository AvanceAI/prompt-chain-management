# tests/conftest.py
import pytest
from src.core.config import Settings 

@pytest.fixture(scope="session")
def settings():
    return Settings()
