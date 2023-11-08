import pytest
from src.step_execution.variable_store import VariableStore
from src.agents.search_agent import SearchAgent

@pytest.fixture
def agent_params():
    return {
        "dependencies": ["topic"],
        "total_results": 10
    }

@pytest.fixture
def variable_store():
    return VariableStore(variables={"topic": "Everything"})

def test_execute(agent_params, variable_store):
    agent = SearchAgent(agent_params)
    result = agent.execute(variable_store)
    assert isinstance(result, dict)
    assert len(result.keys()) == 10
