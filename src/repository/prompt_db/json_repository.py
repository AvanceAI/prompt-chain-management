from tinydb import TinyDB, Query
from src.core.logger import get_logger
from src.utils.utils import read_json

logger = get_logger(__name__)

class JsonRepository:
    def __init__(self, filepath: str):
        self.db = {}
        self.db[filepath] = read_json(filepath)
        
    def get_chain(self, chain_id: str) -> dict:
        return self.db[chain_id]

    def update_chain(self, chain_id: str, updated_data: dict) -> None:
        # Update document matched by chain_id
        self.db[chain_id] = updated_data

    def list_chains(self) -> list:
        # Return all documents in the table
        return list(self.db.keys()) 
