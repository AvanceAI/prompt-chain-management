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
    store = VariableStore(step_result_saver_mock)
    # Explicitly load the saved state in the fixture
    store.load_saved_state()
    return store

def test_update_variables(variable_store):
    step_id = "step2"
    new_variables = {"var4": "value4"}
    variable_store.update_variables(step_id, new_variables)
    # Ensure the internal state is as expected
    assert "var4" in variable_store._variables
    assert variable_store._variables["var4"] == "value4"

def test_get_variable(variable_store):
    # Ensure that initial variables were loaded
    assert "var1" in variable_store._variables
    assert variable_store.get_variable("var1") == "value1"

def test_load_saved_state(variable_store, step_result_saver_mock):
    # Since the state is loaded in the fixture, assert it's already loaded
    assert "var3" in variable_store._variables
    assert variable_store.get_variable("var3") == "value3"
    step_result_saver_mock.load_all_step_results.assert_called_once()

def test_set_variable(variable_store):
    variable_store.set_variable("var5", "value5")
    # Check that the variable was set correctly
    assert "var5" in variable_store._variables
    assert variable_store.get_variable("var5") == "value5"
