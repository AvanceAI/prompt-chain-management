from src.models.prompt_chain import PromptChain
from src.repository.prompt_db.json_repository import JsonRepository

class PromptChainService:
    def __init__(self, repository: JsonRepository):
        self.repository = repository 

    def create_prompt_chain(self, prompt_chain_data: dict) -> PromptChain:
        prompt_chain = PromptChain(**prompt_chain_data)
        # Save to the database
        self.repository.save_prompt_chain(prompt_chain.dict())
        return prompt_chain

    def execute_prompt_chain(self, chain_id: str) -> None:
        prompt_chain_data = self.repository.get_prompt_chain(chain_id)
        
        if not prompt_chain_data or len(prompt_chain_data) == 0:
            raise ValueError("Prompt chain not found")
        prompt_chain = PromptChain(**prompt_chain_data[0])
        
        for prompt in prompt_chain.prompts:
            print(f"Executing prompt {prompt.prompt_id}: {prompt.prompt_text}")
            # Here you would interact with the AI model or external API
