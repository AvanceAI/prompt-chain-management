from src.models.chain import Step
from src.services.chain_service.dependency_resolver import DependencyResolver
from src.services.chain_service.step_execution.search_executor import SearchExecutor
from src.services.chain_service.step_execution.llm_query_executor import LlmQueryExecutor
from src.core.logger import get_logger

logger = get_logger(__name__)

class StepExecutor:
    def __init__(self, run_id, save_dir="outputs", send_callback=None, dependency_resolver=None, variables={}):
        self.run_id = run_id
        self.save_dir = save_dir
        self.dependency_resolver = dependency_resolver or DependencyResolver(send_callback=send_callback)
        self.variables = variables # Store user input variables and output variables, which may be needed later in the Chain

    async def execute_step(self, step: Step):
        logger.info(f"Executing step {step.step_id}")
        # Resolve dependencies for the step
        dependencies = await self.dependency_resolver.resolve(step)
        
        self.variables.update(dependencies)
        if step.step_type == "search":
            # Execute the search with the resolved dependencies (now stored in self.variables)
            result = SearchExecutor(run_id=self.run_id, save_dir=self.save_dir).execute(step, self.variables)
        elif step.step_type == "llm-query":
            result =  LlmQueryExecutor(run_id=self.run_id, save_dir=self.save_dir).execute(step, self.variables)
        if step.response_type == "json":
            if isinstance(result, tuple):
                raise NotImplementedError("Tuple results not supported yet. Assuming outputs array is only length 1")
            self.variables[step.outputs[0].name] = result

        logger.info(f"Step {step.step_id} executed successfully")
        return result