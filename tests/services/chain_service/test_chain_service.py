import pytest
from src.services.chain_service.chain_service import ChainService
from src.repository.prompt_db.json_repository import JsonRepository

@pytest.fixture
def mock_repository(tmp_path):
    repository_file = tmp_path / "test_step_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filename=str(repository_file))

# Test the creation of a prompt chain
def test_create_chain(mock_repository):
    service = ChainService(run_id="test_run", repository=mock_repository)
    chain_data = {
        "chain_id": "test_chain",
        "chain_title": "Test Chain",
        "chain_description": "This is a test chain",
        "steps": [
            {
                "step_id": "test_step_1",
                "description": "this is a test step",
                "step_type": "search",
                "prompt_text": "This is a test prompt.",
                "response_type": "text"
            }
        ]
    }
    chain = service.create_chain(chain_data)
    assert chain.chain_id == chain_data["chain_id"]
    assert len(chain.steps) == len(chain_data["steps"])

@pytest.mark.asyncio
async def test_execute_chain(mock_repository):
    service = ChainService(run_id="test_run", repository=mock_repository)
    chain_data = {
        "chain_id": "test_chain_execute",
        "chain_title": "Test Chain for Execution",
        "chain_description": "This is a test chain for execution.",
        "steps": [
            {
                "step_id": "test_step_exec_1",
                "description": "this is a test step",
                "step_type": "llm-query",
                "prompt_text": "Execute this test prompt.",
                "response_type": "text"
            }
        ]
    }
    service.create_chain(chain_data)

    with pytest.raises(NotImplementedError) as excinfo:
        # "llm-query" step type is not yet implemented
        await service.execute_chain("test_chain_execute")

# Test the error handling when the prompt chain does not exist
def test_execute_nonexistent_chain(mock_repository):
    service = ChainService(run_id="test_run", repository=mock_repository)
    with pytest.raises(ValueError) as excinfo:
        service.execute_chain("nonexistent_chain")
    assert "Chain not found" in str(excinfo.value)
