import json
from pathlib import Path

class StepResultSaver:
    def __init__(self, save_dir):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_step_result(self, variable_name, result):
        with open(self.save_dir / f"{variable_name}.json", 'w') as f:
            json.dump(result, f)

    def load_step_result(self, variable_name):
        with open(self.save_dir / f"{variable_name}.json", 'r') as f:
            return json.load(f)

    def load_all_step_results(self):
        all_results = {}
        # Iterate over all .json files in the save directory
        for step_file in self.save_dir.glob("*.json"):
            variable_name = step_file.stem  # Extract the variable_name from the file name
            with open(step_file, 'r') as f:
                all_results[variable_name] = json.load(f)
        return all_results
