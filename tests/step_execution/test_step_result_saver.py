import json
import pytest
from pathlib import Path
from src.step_execution.step_result_saver import StepResultSaver

@pytest.fixture
def step_result_saver(tmp_path):
    return StepResultSaver(save_dir=tmp_path)

def test_save_step_result(step_result_saver, tmp_path):
    step_id = "test_step"
    result = {"status": "success", "data": "some data"}
    step_result_saver.save_step_result(step_id, result)
    
    expected_file = tmp_path / f"{step_id}.json"
    assert expected_file.exists()
    
    with open(expected_file, 'r') as f:
        saved_result = json.load(f)
    
    assert saved_result == result

def test_load_step_result(step_result_saver, tmp_path):
    step_id = "test_step"
    result = {"status": "success", "data": "some data"}
    
    with open(tmp_path / f"{step_id}.json", 'w') as f:
        json.dump(result, f)
    
    loaded_result = step_result_saver.load_step_result(step_id)
    assert loaded_result == result

def test_load_all_step_results(step_result_saver, tmp_path):
    results = {
        "step1": {"status": "success", "data": "data1"},
        "step2": {"status": "success", "data": "data2"}
    }
    for step_id, result in results.items():
        with open(tmp_path / f"{step_id}.json", 'w') as f:
            json.dump(result, f)
    
    loaded_results = step_result_saver.load_all_step_results()
    assert len(loaded_results) == len(results)
    for step_id, result in results.items():
        assert loaded_results[step_id] == result
