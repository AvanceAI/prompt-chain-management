import pytest
from src.services.chain_service.step_execution.step_executor import StepExecutor
from src.models.chain import Chain, Step
from src.repository.prompt_db.json_repository import JsonRepository
from src.services.chain_service.dependency_resolver import DependencyResolver

def mock_repository(tmp_path):
    repository_file = tmp_path / "test_step_chain.json"
    repository_file.write_text('{}')  # Initialize the file with an empty JSON object
    return JsonRepository(filename=str(repository_file))

@pytest.mark.asyncio
async def test_execute_search_step():
    def mock_user_interface(dep_key): 
        data = {"topic": "DS-260 Form"}
        return data[dep_key]
    
    mock_resolver = DependencyResolver(user_interface=mock_user_interface)
    step_executor = StepExecutor(run_id="test_run", save_dir="outputs", dependency_resolver=mock_resolver)

    step_dict = {
        "step_id": "search-for-topic",
        "description": "Uses Google Search API to perform a search on a topic and return the top results in JSON form.",
        "step_type": "search",
        "response_type": "json",
        "dependencies": [
          {
            "name": "topic",
            "type": "str",
            "class": "user_entry"
          }
      ],
        "outputs": [
          {
            "name": "search_results",
            "type": "json",
            "class": "output"
          }
        ],
        "actions": None
      }
    
    step = Step(**step_dict)
    search_results = await step_executor.execute_step(step)
    assert len(list(search_results.keys())) == 20
