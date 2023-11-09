import os
import json
from src.models.chain import Step
from src.core.logger import get_logger
from src.services.chain_service.dependency_resolver import DependencyResolver
from src.step_execution.step_result_saver import StepResultSaver
from src.step_execution.variable_store import VariableStore
from src.step_execution.agent_loader import AgentLoader

logger = get_logger(__name__)

class StepExecutor:
    def __init__(self, run_id, save_dir="outputs", send_callback=None, dependency_resolver=None):
        self.run_id = run_id
        self.save_dir = os.path.join(save_dir, run_id)
        self.dependency_resolver = dependency_resolver or DependencyResolver(send_callback=send_callback)
        self.result_saver = StepResultSaver(save_dir=self.save_dir)
        self.variable_store = VariableStore(self.result_saver)
        self.agent_loader = AgentLoader(self.dependency_resolver, self.run_id, self.save_dir)

    def load_all_step_results(self):
        all_results = {}
        for step_file in self.save_dir.glob("*.json"):
            step_id = step_file.stem  # Assumes the file name is the step_id
            with open(step_file, 'r') as f:
                all_results[step_id] = json.load(f)
        return all_results

    async def execute_step(self, step: Step):
        logger.info(f"Executing step {step.step_id}")
        
        agent_name = step.agent.replace("-", "_")  # Replace hyphens with underscores if agent names contain them
        agent = self.agent_loader.load_agent(agent_name=agent_name, agent_params=step.agent_params)
        result = await agent.execute()
        
        return result