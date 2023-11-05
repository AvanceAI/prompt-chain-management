from src.models.chain import Step

class DependencyResolver:
    def __init__(self, user_interface=None):
        self.user_interface = user_interface or self.default_user_interface
        self.mock_responses = {}

    def default_user_interface(self, prompt_key):
        # This would be your default method for production which communicates with the actual UI
        raise NotImplementedError("User interface is not implemented.")

    async def resolve(self, step: Step):
        dependencies = {}
        for dependency in step.dependencies:
            dep_key = dependency.name
            if dependency.class_ == 'user_entry':
                dependencies[dep_key] = self.user_interface(dep_key)
        return dependencies
