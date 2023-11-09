from src.step_execution.step_result_saver import StepResultSaver

class VariableStore:
    def __init__(self, save_dir, variables=None):
        self.result_saver = StepResultSaver(save_dir=save_dir)
        self._variables = variables or {}

    def set_save_variable(self, variable_name, result):
        """
        variable_name is Output.name
        """
        self.set_variable(key=variable_name, value=result)
        self.result_saver.save_step_result(variable_name=variable_name, result=result)

    def get_variable(self, key):
        return self._variables.get(key)

    def set_variable(self, key, value):
        self._variables[key] = value

    def load_saved_state(self):
        # Intended to be used on startup to load any previously saved states
        saved_state = self.result_saver.load_all_step_results()
        if saved_state:
            self._variables.update(saved_state)
