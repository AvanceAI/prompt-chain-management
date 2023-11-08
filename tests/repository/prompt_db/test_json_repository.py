import json
import pytest
from src.repository.prompt_db.json_repository import JsonRepository 

@pytest.fixture()
def chain_data():
    with open("tests/data/chain_fixture.json", "r") as f:
        data = json.load(f)
    return data

@pytest.fixture()
def filepath():
    return "tests/data/chain_fixture.json"

@pytest.fixture()
def repository_instance():
    db = JsonRepository(filepath="tests/data/chain_fixture.json")
    return db

def test_save_chain(repository_instance, filepath, chain_data):
    repository_instance.save_chain(filepath, chain_data)
    print(repository_instance.list_chains())
    assert len(repository_instance.list_chains()) == 1

def test_get_chain(repository_instance, filepath, chain_data):
    chain = repository_instance.get_chain(filepath)
    assert chain["chain_id"] == chain_data["chain_id"]

def test_list_chains(repository_instance, filepath ,chain_data):
    repository_instance.save_chain(filepath, chain_data)
    assert isinstance(repository_instance.list_chains(), list)
