import json
import pytest
from src.repository.prompt_db.json_repository import JsonRepository 

@pytest.fixture()
def prompt_chain_data():
    with open("tests/data/prompt_chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def repository_instance():
    db = JsonRepository(filename="tests/data/prompt_chain_fixture.json")
    return db

def test_save_prompt_chain(repository_instance, prompt_chain_data):
    repository_instance.save_prompt_chain(prompt_chain_data)
    assert len(repository_instance.list_prompt_chains()) == 1

def test_get_prompt_chain(repository_instance, prompt_chain_data):
    chain = repository_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert chain[0]["chain_id"] == prompt_chain_data["chain_id"]

def test_update_prompt_chain(repository_instance, prompt_chain_data):
    updated_version = "1.0.1"
    prompt_chain_data["version"] = updated_version
    repository_instance.update_prompt_chain(prompt_chain_data["chain_id"], prompt_chain_data)
    chain = repository_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert chain[0]["version"] == updated_version

def test_delete_prompt_chain(repository_instance, prompt_chain_data):
    repository_instance.delete_prompt_chain(prompt_chain_data["chain_id"])
    chain = repository_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert not chain

def test_list_prompt_chains(repository_instance, prompt_chain_data):
    repository_instance.save_prompt_chain(prompt_chain_data)
    assert isinstance(repository_instance.list_prompt_chains(), list)
    repository_instance.delete_prompt_chain(prompt_chain_data["chain_id"])  # Clean up after test
