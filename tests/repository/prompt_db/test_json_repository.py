import json
import pytest
from src.repository.prompt_db.json_repository import JsonRepository 

@pytest.fixture()
def chain_data():
    with open("tests/data/chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def repository_instance():
    db = JsonRepository(filename="tests/data/chain_fixture.json")
    return db

def test_save_chain(repository_instance, chain_data):
    repository_instance.save_chain(chain_data)
    assert len(repository_instance.list_chains()) == 1

def test_get_chain(repository_instance, chain_data):
    chain = repository_instance.get_chain(chain_data["chain_id"])
    assert chain[0]["chain_id"] == chain_data["chain_id"]

def test_update_chain(repository_instance, chain_data):
    updated_version = "1.0.1"
    chain_data["version"] = updated_version
    repository_instance.update_chain(chain_data["chain_id"], chain_data)
    chain = repository_instance.get_chain(chain_data["chain_id"])
    assert chain[0]["version"] == updated_version

def test_delete_chain(repository_instance, chain_data):
    repository_instance.delete_chain(chain_data["chain_id"])
    chain = repository_instance.get_chain(chain_data["chain_id"])
    assert not chain

def test_list_chains(repository_instance, chain_data):
    repository_instance.save_chain(chain_data)
    assert isinstance(repository_instance.list_chains(), list)
    repository_instance.delete_chain(chain_data["chain_id"])  # Clean up after test
