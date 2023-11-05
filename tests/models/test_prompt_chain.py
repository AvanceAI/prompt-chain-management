import json
import pytest
from src.models.prompt_chain import Prompt, PromptChain

@pytest.fixture()
def prompt_chain_data(): 
    with open("tests/data/prompt_chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def prompt_data(prompt_chain_data):
    return prompt_chain_data['prompts'][0]

def test_create_prompt(prompt_data):
    prompt = Prompt(**prompt_data)
    assert prompt.prompt_id == "content_outline"
    assert prompt.prompt_text == "Generate an outline for a webpage about {{ topic }}."
    assert prompt.response_type == "json"

def test_create_prompt_chain(prompt_chain_data):
    prompt_chain = PromptChain(**prompt_chain_data)
    assert prompt_chain.chain_id == "webpage_creation_chain_001"
    assert prompt_chain.chain_title == "Webpage Content Creation"
    assert len(prompt_chain.prompts) == 4

def test_prompt_chain_validation_error(prompt_chain_data):
    invalid_data = prompt_chain_data
    invalid_data['prompts'][0]['response_type'] = {} # invalid type
    with pytest.raises(ValueError):
        PromptChain(**invalid_data)

def test_prompt_dependency_list(prompt_data):
    prompt_with_deps = prompt_data
    prompt_with_deps['dependencies'] = ['test_prompt_000']
    prompt = Prompt(**prompt_with_deps)
    assert prompt.dependencies == ['test_prompt_000']

def test_missing_required_fields():
    incomplete_data = {
        "chain_id": "chain_002",
        "chain_title": "Incomplete Chain"
        # 'prompts' field is missing
    }
    with pytest.raises(ValueError):
        PromptChain(**incomplete_data)

def test_default_values(prompt_data):
    prompt = Prompt(**prompt_data)
    assert prompt.dependencies == []
    assert prompt.user_interaction == {}
    assert prompt.external_service is None

