import pytest
from src.step_execution.agent_loader import AgentLoader
from src.services.chain_service.dependency_resolver import DependencyResolver

# Dummy run_id for testing purpose
test_run_id = 'test_run_id'
# Dummy save_dir for testing purpose
test_save_dir = 'test_outputs'
# Dummy dependency resolver, replace DependencyResolver with a mock or a fixture if needed
dependency_resolver = DependencyResolver()


@pytest.fixture(params=[
    "search",
    "llm_query",
    "multiprocessing_outline",
    "user_text_response",
])
def agent_name(request):
    return request.param

@pytest.fixture
def mock_params():
    return {
            "query_params": {
                "model": "gpt-4-1106-preview",
                "temperature": 0,
                "max_tokens": 2000,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "eval_literal": True
                }
            }

class TestAgentLoader:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.agent_loader = AgentLoader(dependency_resolver, test_run_id, test_save_dir)

    def test_load_agent(self, agent_name, mock_params):
        # Attempt to load the agent using the loader.
        agent = self.agent_loader.load_agent(agent_name=agent_name, agent_params=mock_params)