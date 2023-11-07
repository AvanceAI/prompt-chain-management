import pytest
import asyncio
from unittest.mock import AsyncMock
from src.models.chain import Step, Dependency
from src.services.chain_service.dependency_resolver import DependencyResolver

# Fixture to create dependency resolver
@pytest.fixture
def dependency_resolver():
    send_callback = AsyncMock()
    return DependencyResolver(send_callback=send_callback)

# Fixture to create a step with dependencies
@pytest.fixture
def step_with_dependencies():
    data = {'name': 'input1',
            'type':'json', 
            'class':'user_entry', 
            'message': 'Please enter input 1'
            }
    return Step(
        step_id='test_step',
        description='test step',
        step_type='search',
        response_type='json',
        dependencies=[
            Dependency(**data),
        ]
    )


@pytest.mark.asyncio
async def test_resolve_with_user_entry(dependency_resolver, step_with_dependencies):
    # Arrange
    correlation_id = f"{step_with_dependencies.step_id}-input1"
    user_input = "user's input data"
    
    # Act
    resolve_task = asyncio.create_task(dependency_resolver.resolve(step_with_dependencies))

    # Wait a bit for request_user_input to execute
    await asyncio.sleep(0.01) 

    # Simulate user input
    dependency_resolver.resolve_user_input(correlation_id, user_input)

    # Now await the resolution process to complete
    dependencies = await resolve_task

    # Assert
    assert dependencies['input1'] == user_input
    dependency_resolver.send_callback.assert_called_once_with({
        "type": "user_entry",
        "correlation_id": correlation_id,
        "message": 'Please enter input 1'
    })

@pytest.mark.asyncio
async def test_request_user_input_creates_future(dependency_resolver):
    # Arrange
    correlation_id = 'test_correlation_id'
    message = 'Test message'

    # Act
    await dependency_resolver.request_user_input(correlation_id, message)

    # Assert
    assert correlation_id in dependency_resolver.pending_responses
    assert isinstance(dependency_resolver.pending_responses[correlation_id], asyncio.Future)

@pytest.mark.asyncio
async def test_get_user_response(dependency_resolver):
    # Arrange
    correlation_id = 'test_correlation_id'
    expected_value = 'user_response'
    dependency_resolver.pending_responses[correlation_id] = asyncio.Future()
    dependency_resolver.pending_responses[correlation_id].set_result(expected_value)

    # Act
    response = await dependency_resolver.get_user_response(correlation_id)

    # Assert
    assert response == expected_value

@pytest.mark.asyncio
async def test_resolve_user_input_sets_future_result(dependency_resolver):
    # Arrange
    correlation_id = 'test_correlation_id'
    value = 'test_value'
    dependency_resolver.pending_responses[correlation_id] = asyncio.Future()

    # Act
    dependency_resolver.resolve_user_input(correlation_id, value)
    result = await dependency_resolver.pending_responses[correlation_id]

    # Assert
    assert result == value
