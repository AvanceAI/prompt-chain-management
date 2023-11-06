from src.models.chain import Step

class DependencyResolver:
    def __init__(self, send_callback=None):
        self.send_callback = send_callback 
        self.mock_responses = {}

    async def resolve(self, step: Step):
        dependencies = {}
        for dependency in step.dependencies:
            dep_key = dependency.name
            if dependency.class_ == 'user_entry':
                dependencies[dep_key] = await self.send_callback(message=dependency.message)
            elif dependency.class_ == 'output':
                pass # Already contained in variables dict in StepExecutor
        return dependencies
