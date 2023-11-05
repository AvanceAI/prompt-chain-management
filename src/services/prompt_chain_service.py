from models.prompt_chain import PromptChain
from db.json_db import JsonDB

class PromptChainService:
    def __init__(self, db: JsonDB):
        self.db = db

    def create_prompt_chain(self, prompt_chain_data: dict) -> PromptChain:
        prompt_chain = PromptChain(**prompt_chain_data)
        # Save to the database
        self.db.save_prompt_chain(prompt_chain.dict())
        return prompt_chain

    def execute_prompt_chain(self, chain_id: str) -> None:
        # Retrieve the prompt chain from the database
        prompt_chain_data = self.db.get_prompt_chain(chain_id)
        if not prompt_chain_data:
            raise ValueError("Prompt chain not found")

        prompt_chain = PromptChain(**prompt_chain_data)
        
        # Here you would add the logic to execute each prompt in the chain
        # This would involve iterating over the prompt_chain.prompts list
        # And handling each prompt's execution and response according to the business logic

        # For now, we'll just print out each prompt for illustration purposes
        for prompt in prompt_chain.prompts:
            print(f"Executing prompt {prompt.prompt_id}: {prompt.prompt_text}")
            # Here you would interact with the AI model or external API
            # And then save the response back to the database
