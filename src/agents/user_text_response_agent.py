from uuid import uuid4
from typing import List, Union
from pydantic import BaseModel, Field
from src.core.logger import get_logger

logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    message: str = Field(None, description="The message to send to the user.")

class UserTextResponseAgent:
    def __init__(self, agent_params, dependency_resolver=None):
        self.agent_params = AgentParams(**agent_params)
        self.dependency_resolver = dependency_resolver
        self.correlation_id = uuid4().hex  # Create a correlation ID

    async def execute(self):
        logger.info("Executing User Text Response step")
        # Use the DependencyResolver to send the user input request message
        await self.dependency_resolver.request_user_input(self.correlation_id, self.agent_params.message)
        response = await self.dependency_resolver.get_user_response(self.correlation_id)
        return response
