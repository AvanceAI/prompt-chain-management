import pytest
import asyncio
from unittest.mock import AsyncMock
from src.models.chain import Step, Dependency, AgentParams
from src.agents.UserTextResponseAgent import UserTextResponseAgent

# Fixture to create UserTextResponseAgent
@pytest.fixture
def user_text_response_agent():
    send_callback = AsyncMock()
    return UserTextResponseAgent(send_callback=send_callback)


@pytest.fixture
def agent_params_fixture():
    return AgentParams(dependencies=['input1'], message='Please enter input 1')

@pytest.mark.asyncio
async def test_execute_with_user_entry(user_text_response_agent, agent_params_fixture):
    # Arrange
    correlation_id = 'input1'
    user_input = "user's input data"
    
    # Act
    execute_task = asyncio.create_task(user_text_response_agent.execute(agent_params_fixture))

    # Wait a bit for request_user_input to execute
    await asyncio.sleep(0.01)

    # Simulate user input
    user_text_response_agent.resolve_user_input(correlation_id, user_input)

    # Now await the execution process to complete
    responses = await execute_task

    # Assert
    assert responses[0] == user_input
    user_text_response_agent.send_callback.assert_called_once_with({
        "type": "user_entry",
        "correlation_id": correlation_id,
        "message": 'Please enter input 1'
    })

@pytest.mark.asyncio
async def test_get_user_response(user_text_response_agent):
    # Arrange
    correlation_id = 'input1'
    expected_value = 'user_response'
    user_text_response_agent.pending_responses[correlation_id] = asyncio.Future()
    user_text_response_agent.pending_responses[correlation_id].set_result(expected_value)

    # Act
    response = await user_text_response_agent.get_user_response(correlation_id)

    # Assert
    assert response == expected_value

@pytest.mark.asyncio
async def test_resolve_user_input_sets_future_result(user_text_response_agent):
    # Arrange
    correlation_id = 'input1'
    value = 'test_value'
    user_text_response_agent.pending_responses[correlation_id] = asyncio.Future()

    # Act
    user_text_response_agent.resolve_user_input(correlation_id, value)
    result = await user_text_response_agent.pending_responses[correlation_id]

    # Assert
    assert result == value