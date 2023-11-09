import importlib
from src.core.logger import get_logger

logger = get_logger(__name__)

class AgentLoader:
    def __init__(self, dependency_resolver, run_id, save_dir="outputs"):
        self.dependency_resolver = dependency_resolver
        self.run_id = run_id
        self.save_dir = save_dir

    def _get_agent_class_name(self, agent_name):
        return ''.join(part.capitalize() for part in agent_name.split('_'))

    def load_agent(self, agent_name, agent_params):
        module_name = f"src.agents.{agent_name}_agent"
        try:
            agent_class_name = self._get_agent_class_name(agent_name)
            agent_module = importlib.import_module(module_name)
        except ModuleNotFoundError as err:
            logger.error(f"Module '{module_name}' not found. Ensure that the agent is properly implemented and the module exists.")
            raise ImportError(f"Module '{module_name}' could not be found.") from err
        
        try:
            agent_class = getattr(agent_module, f"{agent_class_name}Agent")
        except AttributeError as err:
            logger.error(f"Class '{agent_class_name}Agent' not found in '{module_name}'. Ensure that the agent class is correctly named and implemented.")
            raise ImportError(f"Class '{agent_class_name}Agent' not found in '{module_name}'.") from err
        
        return agent_class(agent_params=agent_params, dependency_resolver=self.dependency_resolver)