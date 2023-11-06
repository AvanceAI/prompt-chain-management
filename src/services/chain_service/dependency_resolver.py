from src.models.chain import Step
from src.websocket.web_socket_user_interface import WebSocketUserInterface

class DependencyResolver:
    def __init__(self, user_interface=None):
        self.user_interface = user_interface or self.default_user_interface
        self.mock_responses = {}

    def default_user_interface(self):
        WebSocketUserInterface('ws://localhost:8080') 

    async def resolve(self, step: Step):
        dependencies = {}
        for dependency in step.dependencies:
            dep_key = dependency.name
            if dependency.class_ == 'user_entry':
                dependencies[dep_key] = self.user_interface(message=dependency.message)
            elif dependency.class_ == 'output':
                pass # Already contained in variables dict in StepExecutor
        return dependencies
