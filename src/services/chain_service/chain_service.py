from src.models.chain import Chain, Step
from src.repository.prompt_db.json_repository import JsonRepository
from src.services.chain_service.step_execution.search_executor import SearchExecutor
from src.services.chain_service.dependency_resolver import DependencyResolver

class ChainService:
    def __init__(self, run_id, repository: JsonRepository, save_dir="outputs", dependency_resolver=None):
        self.run_id = run_id
        self.repository = repository 
        self.save_dir = save_dir
        self.dependency_resolver = dependency_resolver or DependencyResolver()

    def create_chain(self, chain_data: dict) -> Chain:
        chain = Chain(**chain_data)
        # Save to the database
        self.repository.save_chain(chain.dict())
        return chain 

    def execute_chain(self, chain_id: str) -> None:
        chain_data = self.repository.get_chain(chain_id)
        
        if not chain_data or len(chain_data) == 0:
            raise ValueError("Chain not found")
        chain = Chain(**chain_data[0])
        
        for step in chain.steps:
            print(f"Executing step {step.step_id}")
            self.execute_step(step)

    async def execute_step(self, step: Step):
        # Resolve dependencies for the step
        dependencies = await self.dependency_resolver.resolve(step)

        if step.step_type == "search":
            # Execute the search with the resolved dependencies
            return SearchExecutor(run_id=self.run_id, save_dir=self.save_dir).execute(step, dependencies)
        elif step.step_type == "llm-query":
            # Execution logic for LLM query would go here
            pass