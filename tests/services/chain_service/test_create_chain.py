import pytest
from src.services.chain_service.chain_service import ChainService
from src.repository.prompt_db.json_repository import JsonRepository

@pytest.fixture
def mock_repository(tmp_path):
    repository_file = tmp_path / "test_step_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filepath=str(repository_file))

@pytest.fixture
def tmp_filepath(tmp_path):
    return tmp_path / "test_step_chain.json"

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
