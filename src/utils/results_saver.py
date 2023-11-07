import os
from src.models.chain import Step
from src.utils.utils import save_json, save_text
from src.core.logger import get_logger

logger = get_logger(__name__)

def save_results(save_dir, results, step: Step):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    if step.response_type == "json":
        save_path = os.path.join(save_dir, f"{step.step_id}.json")
        logger.info(f"Saving search results to {save_path}")
        save_json(filepath=save_path, data={"data": results})
    elif step.response_type == "text":
        save_path = os.path.join(save_dir, f"{step.step_id}.txt")
        logger.info(f"Saving search results to {save_path}")
        save_text(filepath=save_path, data=results)