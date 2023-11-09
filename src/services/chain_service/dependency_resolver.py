import asyncio
from src.core.logger import get_logger

logger = get_logger(__name__)

class DependencyResolver:
    def __init__(self, send_callback=None):
        self.send_callback = send_callback
        self.pending_responses = {}  # Store futures awaiting user input

    async def request_user_input(self, correlation_id, message, variable=None):
        logger.info(f"Sending request for user input with correlation_id: {correlation_id}")
        await self.send_callback({"type": "user_entry", "correlation_id": correlation_id, "message": message, "variable": variable})
        self.pending_responses[correlation_id] = asyncio.get_event_loop().create_future()

    async def get_user_response(self, correlation_id):
        # Wait for the response to arrive for the given correlation ID
        response = await self.pending_responses[correlation_id]
        logger.info(f"Received user response for correlation_id: {correlation_id}")
        return response

    def resolve_user_input(self, correlation_id, value):
        if correlation_id in self.pending_responses:
            self.pending_responses[correlation_id].set_result(value)
            logger.info(f"Resolved user input for correlation_id: {correlation_id}")
