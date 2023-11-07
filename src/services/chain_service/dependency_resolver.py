import asyncio
from src.models.chain import Step
from src.core.logger import get_logger

logger = get_logger(__name__)

class DependencyResolver:
    def __init__(self, send_callback=None):
        self.send_callback = send_callback
        self.pending_responses = {}  # Store futures awaiting user input

    async def resolve(self, step: Step):
        dependencies = {}
        for dependency in step.dependencies:
            dep_key = dependency.name
            if dependency.class_ == 'user_entry':
                correlation_id = f"{step.step_id}-{dep_key}"
                logger.info(f"Resolving user entry dependency: {dep_key}")
                await self.request_user_input(correlation_id, dependency.message)
                user_input = await self.get_user_response(correlation_id)
                dependencies[dep_key] = user_input
                logger.info(f"Resolved user entry dependency: {dep_key}")
            elif dependency.class_ == 'output':
                pass # handle output class dependencies if required
        return dependencies

    async def request_user_input(self, correlation_id, message):
        # Send the request for user input with a unique correlation ID
        logger.info(f"Sending request for user input with correlation_id: {correlation_id}")
        await self.send_callback({"type": "user_entry", "correlation_id": correlation_id, "message": message})
        # Create a future to be fulfilled when the response arrives
        logger.info(f"Creating future for correlation_id: {correlation_id}")
        self.pending_responses[correlation_id] = asyncio.get_event_loop().create_future()
        logger.info(f"Future created for correlation_id: {correlation_id}")

    async def get_user_response(self, correlation_id):
        # Wait for the response to arrive for the given correlation ID
        response = await self.pending_responses[correlation_id]
        logger.info(f"Received user response for correlation_id: {correlation_id}")
        return response

    def resolve_user_input(self, correlation_id, value):
        if correlation_id in self.pending_responses:
            self.pending_responses[correlation_id].set_result(value)
            logger.info(f"Resolved user input for correlation_id: {correlation_id}")
