import os
from src.models.chain import Step
from src.repository.openai.query import Query
from src.repository.openai.completion_query import CompletionQuery
from src.core.logger import get_logger
from src.utils.results_saver import save_results

logger = get_logger(__name__)

class LlmQueryExecutor:
    def __init__(self, run_id, save_dir="outputs"):
        self.run_id = run_id
        self.save_dir = os.path.join(save_dir, run_id)
    
    def _run_completions_api_query(self, step, system_message, eval_literal):
        query = CompletionQuery(
            model=step.query_params.model, 
            temperature=step.query_params.temperature, 
            max_tokens=step.query_params.max_tokens, 
            top_p=step.query_params.top_p, 
            frequency_penalty=step.query_params.frequency_penalty
            )
        return query.run(prompt=system_message, eval_literal=eval_literal)
    
    def _run_chat_api_query(self, step, system_message, eval_literal):
        query = Query(
            model=step.query_params.model, 
            temperature=step.query_params.temperature, 
            max_tokens=step.query_params.max_tokens, 
            top_p=step.query_params.top_p, 
            frequency_penalty=step.query_params.frequency_penalty,
            system_message=system_message
            )
        return query.run(eval_literal=eval_literal)
    
    
    def execute(self, step: Step, dependencies: dict):
        logger.info("Executing LLM query step")
        system_message = step.prompt_text.format(**dependencies)

        if step.response_type == "json":
            eval_literal = True
        else:
            eval_literal = False

        if step.query_params.model == "gpt-3.5-turbo-instruct":
            results = self._run_completions_api_query(step, system_message, eval_literal)
        else:
            results = self._run_chat_api_query(step, system_message, eval_literal)
        save_results(self.save_dir, results, step=step)
        logger.info("LLM query step executed successfully")
        return results
    