import pytest
from src.services.chain_service.step_execution.step_executor import StepExecutor
from src.models.chain import Step
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


@pytest.mark.asyncio
@pytest.mark.skip(reason="Not fully implemented yet")
async def test_execute_llm_query_step():
    def mock_user_interface(dep_key): 
        data = {
          "topic": "DS-260 Form",
          "search_results": {
            0: {"mock": True},
            1: {"mock": True},
            2: {"mock": True}
          }
                }
        return data[dep_key]
    
    mock_resolver = DependencyResolver(user_interface=mock_user_interface)
    step_executor = StepExecutor(run_id="test_run", save_dir="outputs", dependency_resolver=mock_resolver)

    step_dict = {
        "step_id": "find-themes",
        "description": "Analyzes the search results and finds the most common themes, which are then presented to the user to refine the article topic.",
        "step_type": "llm-query",
        "query_params": {
            "model": "gpt-4",
            "temperature": 0,
            "max_tokens": 1000,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0
          },
        "prompt_text": "I have a list of search results related to the topic \"{topic}\". Please analyze the following data and group the results into 3-4 thematic categories based on their content and purpose. You may ignore uncommon themes and focus on the most prominent categories presented in these results. Here is the data:\n\n\n{search_results}\n\n\nBased on the titles and descriptions, please provide a brief overview of each identified category and list which entries (by their number) belong to each category.\n\nFormat your response like this.\n\nResponse:\n{\n\"0\": {\n       \"theme\": \"First theme identified\",\n       \"results\": [0, 4, 5, 7, 9] \n       },\n\"1\": {\n       \"theme\": \"First theme identified\",\n       \"results\": [1,8,11,13] \n       },\n\"2\": {\n       \"theme\": \"First theme identified\",\n       \"results\": [2,3, 6] \n       }\n}\n\n\nResponse:\n",
        "response_type": "json",
        "dependencies": [
          {
            "name": "topic",
            "type": "str",
            "class": "input"
          },
          {
            "name": "search_results",
            "type": "json",
            "class": "input"
          }
        ],
        "outputs": [
          {
            "name": "themes",
            "type": "json",
            "class": "output"
          }
        ],
        "actions": [
          {
            "name": "select-preferred-theme",
            "type": "select",
            "data": "themes"
          }
        ]
      }
    
    step = Step(**step_dict)
    themes = await step_executor.execute_step(step)
    print(themes)
    assert isinstance(themes, dict)