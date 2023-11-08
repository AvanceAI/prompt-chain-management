class VariableStore:
    def __init__(self, result_saver):
        self._variables = {}
        self.result_saver = result_saver

    def update_variables(self, step_id, new_variables):
        self._variables.update(new_variables)
        # Optionally save the state after each update
        self.result_saver.save_step_result(step_id, self._variables)

    def get_variable(self, key):
        return self._variables.get(key)

    def set_variable(self, key, value):
        self._variables[key] = value

    def load_saved_state(self):
        # Intended to be used on startup to load any previously saved states
        saved_state = self.result_saver.load_all_step_results()
        if saved_state:
            self._variables.update(saved_state)
