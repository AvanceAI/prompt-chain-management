import json
from pathlib import Path

class StepResultSaver:
    def __init__(self, save_dir):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_step_result(self, step_id, result):
        with open(self.save_dir / f"{step_id}.json", 'w') as f:
            json.dump(result, f)

    def load_step_result(self, step_id):
        with open(self.save_dir / f"{step_id}.json", 'r') as f:
            return json.load(f)

    def load_all_step_results(self):
        all_results = {}
        # Iterate over all .json files in the save directory
        for step_file in self.save_dir.glob("*.json"):
            step_id = step_file.stem  # Extract the step_id from the file name
            with open(step_file, 'r') as f:
                all_results[step_id] = json.load(f)
        return all_results
