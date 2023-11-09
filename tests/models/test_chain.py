import json
import pytest
from src.models.chain import Step, Chain, Output, QueryParams

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
    assert step.step_id == "prompt-user-for-topic"
    assert step.description == "Prompt user for topic they would like to write about."
    assert step.output.name == "topic"
    assert step.output.type == "text"

def test_create_chain(chain_data):
    chain = Chain(**chain_data)
    assert chain.chain_id == "based-off-top-google-results-no-citations"
    assert chain.chain_title == "Write Article Based Off Top Google Results (No Citations)"
    assert len(chain.steps) == 10 

def test_chain_validation_error(chain_data):
    invalid_data = chain_data
    invalid_data['steps'][0]['step_id'] = {}
    with pytest.raises(ValueError):
        Chain(**invalid_data)

def test_missing_required_fields():
    incomplete_data = {
        "chain_id": "incomplete_chain_001",
        "chain_title": "Incomplete Chain"
        # 'steps' field is missing
    }
    with pytest.raises(ValueError):
        Chain(**incomplete_data)
