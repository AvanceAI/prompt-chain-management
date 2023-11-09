import pytest
from unittest.mock import MagicMock
from src.step_execution.variable_store import VariableStore

@pytest.fixture
def step_result_saver_mock():
    saver = MagicMock()
    # Mock the result of load_all_step_results
    saver.load_all_step_results.return_value = {
        "var1": "value1", "var2": "value2", "var3": "value3"
    }
    return saver

@pytest.fixture
def variable_store(step_result_saver_mock):
    store = VariableStore(save_dir='/', variables=None)  # Assuming save_dir is just '/'
    store.result_saver = step_result_saver_mock
    # Explicitly load the saved state in the fixture
    store.load_saved_state()
    return store

def test_set_save_variable(variable_store, step_result_saver_mock):
    variable_name = "var4"
    result = "value4"
    variable_store.set_save_variable(variable_name, result)
    # Check that the variable was set correctly
    assert variable_store.get_variable(variable_name) == result
    # Check that the result saver was called correctly
    step_result_saver_mock.save_step_result.assert_called_once_with(variable_name=variable_name, result=result)

def test_get_variable(variable_store):
    # Ensure that initial variables were loaded
    assert variable_store.get_variable("var1") == "value1"

def test_load_saved_state(variable_store, step_result_saver_mock):
    # Since the state is loaded in the fixture, assert it's already loaded
    assert variable_store.get_variable("var3") == "value3"
    step_result_saver_mock.load_all_step_results.assert_called_once()

def test_set_variable(variable_store):
    variable_store.set_variable("var5", "value5")
    # Check that the variable was set correctly
    assert variable_store.get_variable("var5") == "value5"
