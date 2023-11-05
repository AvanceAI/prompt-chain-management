from tinydb import TinyDB, Query

class JsonRepository:
    def __init__(self, filename: str):
        self.db = TinyDB(filename)

    def save_chain(self, chain_data: dict) -> None:
        # Insert a new document into the table
        self.db.insert(chain_data)

    def get_chain(self, chain_id: str) -> dict:
        # Search for a document by chain_id
        PromptChain = Query()
        return self.db.search(PromptChain.chain_id == chain_id)

    def update_chain(self, chain_id: str, updated_data: dict) -> None:
        # Update document matched by chain_id
        PromptChain = Query()
        self.db.update(updated_data, PromptChain.chain_id == chain_id)

    def delete_chain(self, chain_id: str) -> None:
        # Remove document by chain_id
        PromptChain = Query()
        self.db.remove(PromptChain.chain_id == chain_id)

    def list_chains(self) -> list:
        # Return all documents in the table
        return self.db.all()
