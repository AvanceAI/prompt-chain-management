from src.services.google_search.searcher import Searcher
from src.models.chain import Step
from src.core.logger import get_logger

logger = get_logger(__name__)

class SearchExecutor:
    def __init__(self, run_id, save_dir="outputs"):
        self.searcher = Searcher(run_id=run_id, save_dir=save_dir)

    def execute(self, step: Step, variables: dict):
        logger.info("Executing search step")
        search_results = self.searcher.run(query=variables["topic"], step_id=step.step_id)
        logger.info("Search step executed successfully")
        return search_results
