import os
import pytest
from src.services.google_search.searcher import Searcher

@pytest.fixture()
def searcher():
    return Searcher(save_dir="tests/services/google_search", run_id="test_run")

def test_run(searcher):
    step_id = "test-step-1"
    query = "DS-160 Form"
    results = searcher.run(query=query, step_id=step_id)
    assert len(list(results.keys())) == 20
    assert os.path.exists(f"tests/services/google_search/test_run/{step_id}.json")
    # os.remove(f"tests/services/google_search/test_run/{step_id}.json")
