import pytest
from src.services.chain_service.runner import ChainService
from src.repository.prompt_db.json_repository import JsonRepository

# Fixture to mock the database file interaction
@pytest.fixture
def mock_repository(tmp_path):
    repository_file = tmp_path / "test_step_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filename=str(repository_file))

# Test the creation of a prompt chain
def test_create_chain(mock_repository):
    service = ChainService(repository=mock_repository)
    chain_data = {
        "chain_id": "test_chain",
        "chain_title": "Test Chain",
        "chain_description": "This is a test chain",
        "steps": [
            {
                "step_id": "test_step_1",
                "description": "this is a test step",
                "prompt_text": "This is a test prompt.",
                "response_type": "text"
            }
        ]
    }
    chain = service.create_chain(chain_data)
    assert chain.chain_id == chain_data["chain_id"]
    assert len(chain.steps) == len(chain_data["steps"])

# Test the retrieval and execution of a prompt chain
def test_execute_chain(mock_repository):
    service = ChainService(repository=mock_repository)
    chain_data = {
        "chain_id": "test_chain_execute",
        "chain_title": "Test Chain for Execution",
        "chain_description": "This is a test chain for execution.",
        "steps": [
            {
                "step_id": "test_step_exec_1",
                "description": "this is a test step",
                "prompt_text": "Execute this test prompt.",
                "response_type": "text"
            }
        ]
    }
    service.create_chain(chain_data)

    # You should ideally mock the execution response as well
    service.execute_chain("test_chain_execute")
    # Add assertions here to check if the prompt was executed correctly
    # For example, check the state of the database if the responses are stored

# Test the error handling when the prompt chain does not exist
def test_execute_nonexistent_chain(mock_repository):
    service = ChainService(repository=mock_repository)
    with pytest.raises(ValueError) as excinfo:
        service.execute_chain("nonexistent_chain")
    assert "Prompt chain not found" in str(excinfo.value)

