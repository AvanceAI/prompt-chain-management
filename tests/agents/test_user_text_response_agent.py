import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from src.agents.user_text_response_agent import UserTextResponseAgent, AgentParams

# Fixture to create UserTextResponseAgent with a mock dependency resolver
@pytest.fixture
def user_text_response_agent():
    dependency_resolver = AsyncMock()
    agent_params = {
        "dependencies": ["dep1", "dep2"],
        "message": "Please enter input:"
    }
    return UserTextResponseAgent(agent_params=agent_params, dependency_resolver=dependency_resolver)

@pytest.mark.asyncio
async def test_execute(user_text_response_agent):
    # Arrange
    user_input = "user's input data"
    correlation_id = user_text_response_agent.correlation_id
    # Mock get_user_response to return the expected user input immediately
    user_text_response_agent.dependency_resolver.get_user_response.return_value = user_input

    # Act
    response = await user_text_response_agent.execute(None)  # variable_store is not used in execute

    # Assert
    user_text_response_agent.dependency_resolver.request_user_input.assert_called_once_with(correlation_id, user_text_response_agent.agent_params.message)
    user_text_response_agent.dependency_resolver.get_user_response.assert_called_once_with(correlation_id)
    assert response == user_input  # This should now be comparing two strings, not a Future to a string
