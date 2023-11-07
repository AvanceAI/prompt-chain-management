from src.services.chain_service.step_execution.step_executor import StepExecutor
from src.repository.prompt_db.json_repository import JsonRepository
from src.models.chain import Chain
from src.core.logger import get_logger

logger = get_logger(__name__)

class ChainService:
    def __init__(self, run_id, send_callback=None, repository=JsonRepository, save_dir="outputs"):
        self.run_id = run_id
        self.repository = repository
        self.save_dir = save_dir
        self.step_executor = StepExecutor(run_id=run_id, save_dir=save_dir, send_callback=send_callback)

    def create_chain(self, chain_data: dict) -> Chain:
        chain = Chain(**chain_data)
        return chain 

    async def execute_chain(self, chain_id: str) -> None:
        chain_data = self.repository.get_chain(chain_id)
        if not chain_data or chain_data == {}:
            raise ValueError("Chain not found")
        chain = Chain(**chain_data)
        
        for i, step in enumerate(chain.steps):
            logger.info(f"Executing step {i+1} of {len(chain.steps)}")
            await self.step_executor.execute_step(step)
            logger.info(f"Step {i+1} of {len(chain.steps)} executed successfully")
