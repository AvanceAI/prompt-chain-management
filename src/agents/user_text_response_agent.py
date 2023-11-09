from uuid import uuid4
from typing import List, Union
from pydantic import BaseModel, Field
from src.core.logger import get_logger

logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    message: str = Field(None, description="The message to send to the user.")

class UserTextResponseAgent:
    def __init__(self, agent_params, input_resolver=None):
        self.agent_params = AgentParams(**agent_params)
        self.input_resolver = input_resolver
        self.correlation_id = uuid4().hex  # Create a correlation ID

    async def execute(self, variable_store):
        logger.info("Executing User Text Response step")
        # Use the InputResolver to send the user input request message
        await self.input_resolver.request_user_input(self.correlation_id, self.agent_params.message)
        response = await self.input_resolver.get_user_response(self.correlation_id)
        return response
