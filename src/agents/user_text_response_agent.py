import asyncio
from uuid import uuid4
from typing import List, Union
from pydantic import BaseModel, Field
from src.core.logger import get_logger

logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    message: str = Field(None, description="The message to send to the user.")

class UserTextResponseAgent:
    def __init__(self, agent_params):
        self.agent_params = AgentParams(**agent_params)

    async def execute(self, send_callback):
        logger.info("Executing User Text Response  step")
        correlation_id = uuid4()
        await self.request_user_input(correlation_id=correlation_id, send_callback=send_callback)
        results = await self.get_user_response(correlation_id)
        logger.info("User Text Response  step executed successfully")
        return results
    
    async def request_user_input(self, correlation_id, send_callback):
        # Send the request for user input with a unique correlation ID
        logger.info(f"Sending request for user input with correlation_id: {correlation_id}")
        await send_callback({"type": "user_entry", "correlation_id": correlation_id, "message": self.agent_params.message})
        # Create a future to be fulfilled when the response arrives
        logger.info(f"Creating future for correlation_id: {correlation_id}")
        self.pending_responses[correlation_id] = asyncio.get_event_loop().create_future()
        logger.info(f"Future created for correlation_id: {correlation_id}")

    async def get_user_response(self, correlation_id):
        # Wait for the response to arrive for the given correlation ID
        response = await self.pending_responses[correlation_id]
        logger.info(f"Received user response for correlation_id: {correlation_id}")
        return response
