from src.models.chain import Chain 
from src.repository.prompt_db.json_repository import JsonRepository

class ChainService:
    def __init__(self, repository: JsonRepository):
        self.repository = repository 

    def create_chain(self, chain_data: dict) -> Chain:
        chain = Chain(**chain_data)
        # Save to the database
        self.repository.save_chain(chain.dict())
        return chain 

    def execute_chain(self, chain_id: str) -> None:
        chain_data = self.repository.get_chain(chain_id)
        
        if not chain_data or len(chain_data) == 0:
            raise ValueError("Prompt chain not found")
        chain = Chain(**chain_data[0])
        
        for step in chain.steps:
            print(f"Executing prompt {step.step_id}")
            # Here you would interact with the AI model or external API
