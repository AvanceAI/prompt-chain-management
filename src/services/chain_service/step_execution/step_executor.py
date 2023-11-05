from src.models.chain import Step
from src.services.chain_service.dependency_resolver import DependencyResolver
from src.services.chain_service.step_execution.search_executor import SearchExecutor

class StepExecutor:
    def __init__(self, run_id, save_dir="outputs", dependency_resolver=None):
        self.run_id = run_id
        self.save_dir = save_dir
        self.dependency_resolver = dependency_resolver or DependencyResolver()

    async def execute_step(self, step: Step):
        # Resolve dependencies for the step
        dependencies = await self.dependency_resolver.resolve(step)

        if step.step_type == "search":
            # Execute the search with the resolved dependencies
            return SearchExecutor(run_id=self.run_id, save_dir=self.save_dir).execute(step, dependencies)
        elif step.step_type == "llm-query":
            raise NotImplementedError