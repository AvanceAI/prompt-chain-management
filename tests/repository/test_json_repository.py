import json
import pytest
from src.repository.json_repository import JsonRepository 

@pytest.fixture()
def prompt_chain_data():
    with open("tests/repository/prompt_chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def db_instance(tmp_path):
    # Create a temporary database file
    db_file = tmp_path / "test_prompt_chains.json"
    db = JsonRepository(filename=db_file)
    return db

def test_save_prompt_chain(db_instance, prompt_chain_data):
    db_instance.save_prompt_chain(prompt_chain_data)
    assert len(db_instance.list_prompt_chains()) == 1

def test_get_prompt_chain(db_instance, prompt_chain_data):
    chain = db_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert chain[0]["chain_id"] == prompt_chain_data["chain_id"]

def test_update_prompt_chain(db_instance, prompt_chain_data):
    updated_version = "1.0.1"
    prompt_chain_data["version"] = updated_version
    db_instance.update_prompt_chain(prompt_chain_data["chain_id"], prompt_chain_data)
    chain = db_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert chain[0]["version"] == updated_version

def test_delete_prompt_chain(db_instance, prompt_chain_data):
    db_instance.delete_prompt_chain(prompt_chain_data["chain_id"])
    chain = db_instance.get_prompt_chain(prompt_chain_data["chain_id"])
    assert not chain

def test_list_prompt_chains(db_instance, prompt_chain_data):
    db_instance.save_prompt_chain(prompt_chain_data)
    assert isinstance(db_instance.list_prompt_chains(), list)
    db_instance.delete_prompt_chain(prompt_chain_data["chain_id"])  # Clean up after test
