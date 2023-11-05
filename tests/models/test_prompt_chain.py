import json
import pytest
from src.models.chain import Step, Chain, Dependency, Output, Action

@pytest.fixture()
def chain_data(): 
    with open("tests/data/chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def step_data(chain_data):
    return chain_data['steps'][0]

def test_create_step(step_data):
    step = Step(**step_data)
    assert step.step_id == "search-for-topic"
    assert step.description == "Uses Google Search API to perform a search on a topic and return the top results in JSON form."
    assert step.response_type == "json"
    # Ensure that the dependencies are parsed correctly
    assert isinstance(step.dependencies[0], Dependency)
    assert step.dependencies[0].name == "topic"

def test_create_chain(chain_data):
    chain = Chain(**chain_data)
    assert chain.chain_id == "based-off-top-google-results-no-citations"
    assert chain.chain_title == "Write Article Based Off Top Google Results (No Citations)"
    assert len(chain.steps) == 2  # Based on the JSON provided

def test_chain_validation_error(chain_data):
    invalid_data = chain_data
    invalid_data['steps'][0]['response_type'] = {}  # invalid type
    with pytest.raises(ValueError):
        Chain(**invalid_data)

def test_step_dependency_list(step_data):
    step_with_deps = step_data
    step_with_deps['dependencies'] = [{"name": "test_dependency", "type": "str", "class": "user_entry"}]
    step = Step(**step_with_deps)
    assert isinstance(step.dependencies[0], Dependency)
    assert step.dependencies[0].name == "test_dependency"

def test_missing_required_fields():
    incomplete_data = {
        "chain_id": "incomplete_chain_001",
        "chain_title": "Incomplete Chain"
        # 'steps' field is missing
    }
    with pytest.raises(ValueError):
        Chain(**incomplete_data)

def test_default_values(step_data):
    step = Step(**step_data)
    assert step.dependencies != []
    assert step.outputs != []
    # Testing if the outputs are correctly parsed
    assert isinstance(step.outputs[0], Output)
    assert step.outputs[0].name == "search_results"
    # Assuming the step_data has no actions, otherwise adjust accordingly
    assert step.actions is None

def test_step_actions_list(step_data):
    # Assume step_data includes an 'actions' field
    # If step_data does not include actions, this test should be adjusted accordingly.
    step_with_actions = step_data
    step_with_actions['actions'] = [
        {"name": "select-preferred-theme", "type": "select", "data": "themes"}
    ]
    step = Step(**step_with_actions)
    assert step.actions is not None
    assert isinstance(step.actions[0], Action)
    assert step.actions[0].name == "select-preferred-theme"
    assert step.actions[0].type == "select"
    assert step.actions[0].data == "themes"

