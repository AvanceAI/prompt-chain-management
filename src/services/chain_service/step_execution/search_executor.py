import os
from src.services.google_search.searcher import Searcher
from src.models.chain import Step
from src.core.logger import get_logger
from src.utils.results_saver import save_results

logger = get_logger(__name__)

class SearchExecutor:
    def __init__(self, run_id, save_dir="outputs"):
        self.searcher = Searcher()
        self.save_dir = os.path.join(save_dir, run_id)

    def execute(self, step: Step, variables: dict):
        logger.info("Executing search step")
        results = self.searcher.run(query=variables["topic"])
        save_results(self.save_dir, results, step=step)
        logger.info("Search step executed successfully")
        return results
