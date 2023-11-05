from tinydb import TinyDB, Query

class JsonRepository:
    def __init__(self, filename: str):
        self.db = TinyDB(filename)
        self.prompt_chain_table = self.db.table('prompt_chain')  # Create a table for prompt chains

    def save_prompt_chain(self, prompt_chain_data: dict) -> None:
        # Insert a new document into the table
        self.prompt_chain_table.insert(prompt_chain_data)

    def get_prompt_chain(self, chain_id: str) -> dict:
        # Search for a document by chain_id
        PromptChain = Query()
        return self.prompt_chain_table.search(PromptChain.chain_id == chain_id)

    def update_prompt_chain(self, chain_id: str, updated_data: dict) -> None:
        # Update document matched by chain_id
        PromptChain = Query()
        self.prompt_chain_table.update(updated_data, PromptChain.chain_id == chain_id)

    def delete_prompt_chain(self, chain_id: str) -> None:
        # Remove document by chain_id
        PromptChain = Query()
        self.prompt_chain_table.remove(PromptChain.chain_id == chain_id)

    def list_prompt_chains(self) -> list:
        # Return all documents in the table
        return self.prompt_chain_table.all()

# Example usage
# db = JsonDB('prompt_chains.json')
# db.save_prompt_chain(prompt_chain_data)
# chain = db.get_prompt_chain('chain_id')
# db.update_prompt_chain('chain_id', updated_data)
# db.delete_prompt_chain('chain_id')
# all_chains = db.list_prompt_chains()
