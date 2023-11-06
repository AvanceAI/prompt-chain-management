from src.services.chain_service.step_execution.step_executor import StepExecutor
from src.repository.prompt_db.json_repository import JsonRepository
from src.models.chain import Chain

class ChainService:
    def __init__(self, run_id, send_callback=None, repository=JsonRepository, save_dir="outputs"):
        self.run_id = run_id
        self.repository = repository
        self.save_dir = save_dir
        self.step_executor = StepExecutor(run_id=run_id, save_dir=save_dir, send_callback=send_callback)

    def create_chain(self, chain_data: dict) -> Chain:
        chain = Chain(**chain_data)
        # Save to the database
        self.repository.save_chain(chain.dict())
        return chain 

    def execute_chain(self, chain_id: str) -> None:
        chain_data = self.repository.get_chain(chain_id)
        
        if not chain_data or chain_data == {}:
            raise ValueError("Chain not found")
        chain = Chain(**chain_data)
        
        for step in chain.steps:
            print(f"Executing step {step.step_id}")
            # Here we use the StepExecutor to execute the step
            return self.step_executor.execute_step(step)
