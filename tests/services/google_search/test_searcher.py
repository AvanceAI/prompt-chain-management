import os
import pytest
from src.step_execution.tools.google_search.searcher import Searcher

@pytest.fixture()
def searcher():
    return Searcher()

def test_run(searcher):
    query = "DS-160 Form"
    results = searcher.run(query=query)
    assert len(list(results.keys())) == 20
