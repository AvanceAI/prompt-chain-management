from tinydb import TinyDB, Query
from src.core.logger import get_logger
from src.utils.utils import read_json

logger = get_logger(__name__)

class JsonRepository:
    def __init__(self, filepath: str):
        self.db = {}
        self.db[filepath] = read_json(filepath)
        
    def get_chain(self, filepath: str) -> dict:
        if filepath not in self.db:
            raise KeyError(f"Chain not found (filepath): {filepath}")
        return self.db[filepath]

    def save_chain(self, filepath, chain_data: dict) -> None:
        # Insert a new document
        self.db[filepath] = chain_data

    def list_chains(self) -> list:
        # Return all documents in the table
        return list(self.db.keys()) 
