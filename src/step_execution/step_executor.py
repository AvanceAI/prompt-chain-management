import os
import importlib
from src.models.chain import Step
import json
from src.services.chain_service.dependency_resolver import DependencyResolver
from src.core.logger import get_logger
from src.step_execution.step_result_saver import StepResultSaver
from src.step_execution.variable_store import VariableStore

logger = get_logger(__name__)

class StepExecutor:
    def __init__(self, run_id, save_dir="outputs", send_callback=None, dependency_resolver=None):
        self.run_id = run_id
        self.save_dir = os.path.join(save_dir, run_id)
        self.dependency_resolver = dependency_resolver or DependencyResolver(send_callback=send_callback)
        self.result_saver = StepResultSaver(save_dir=self.save_dir)
        self.variable_store = VariableStore(self.result_saver)

    def load_all_step_results(self):
        all_results = {}
        for step_file in self.save_dir.glob("*.json"):
            step_id = step_file.stem  # Assumes the file name is the step_id
            with open(step_file, 'r') as f:
                all_results[step_id] = json.load(f)
        return all_results

    def load_agent(self, agent_name):
        try:
            agent_module = importlib.import_module(f"src.agents.{agent_name}_agent")
            agent_class = getattr(agent_module, f"{agent_name.capitalize()}Agent")
            return agent_class(run_id=self.run_id, save_dir=self.save_dir)
        except (ModuleNotFoundError, AttributeError) as e:
            logger.error(f"Error loading agent {agent_name}: {e}")
            raise ImportError(f"Agent {agent_name} could not be loaded.")

    async def execute_step(self, step: Step):
        logger.info(f"Executing step {step.step_id}")
        
        agent_name = step.agent.replace("-", "_")  # Replace hyphens with underscores if agent names contain them
        agent = self.load_agent(agent_name)
        result = agent.execute(step, self.variables)
        
        self.variable_store.update_variables(step.output.name, result) 
        self.result_saver.save_step_result(step.step_id, result)
        logger.info(f"Step {step.step_id} executed successfully")
        return result
