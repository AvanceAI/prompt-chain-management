import pytest
from src.services.prompt_chain_service.runner import PromptChainService
from src.repository.prompt_db.json_repository import JsonRepository

# Fixture to mock the database file interaction
@pytest.fixture
def mock_repository(tmp_path):
    repository_file = tmp_path / "test_prompt_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filename=str(repository_file))

# Test the creation of a prompt chain
def test_create_prompt_chain(mock_repository):
    service = PromptChainService(repository=mock_repository)
    prompt_chain_data = {
        "chain_id": "test_chain",
        "chain_title": "Test Chain",
        "prompts": [
            {
                "prompt_id": "test_prompt_1",
                "prompt_text": "This is a test prompt.",
                "response_type": "text"
            }
        ]
    }
    prompt_chain = service.create_prompt_chain(prompt_chain_data)
    assert prompt_chain.chain_id == prompt_chain_data["chain_id"]
    assert len(prompt_chain.prompts) == len(prompt_chain_data["prompts"])

# Test the retrieval and execution of a prompt chain
def test_execute_prompt_chain(mock_repository):
    service = PromptChainService(repository=mock_repository)
    prompt_chain_data = {
        "chain_id": "test_chain_execute",
        "chain_title": "Test Chain for Execution",
        "prompts": [
            {
                "prompt_id": "test_prompt_exec_1",
                "prompt_text": "Execute this test prompt.",
                "response_type": "text"
            }
        ]
    }
    service.create_prompt_chain(prompt_chain_data)

    # You should ideally mock the execution response as well
    service.execute_prompt_chain("test_chain_execute")
    # Add assertions here to check if the prompt was executed correctly
    # For example, check the state of the database if the responses are stored

# Test the error handling when the prompt chain does not exist
def test_execute_nonexistent_prompt_chain(mock_repository):
    service = PromptChainService(repository=mock_repository)
    with pytest.raises(ValueError) as excinfo:
        service.execute_prompt_chain("nonexistent_chain")
    assert "Prompt chain not found" in str(excinfo.value)

