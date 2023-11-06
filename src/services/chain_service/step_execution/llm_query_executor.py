import json
from src.models.chain import Step
from src.repository.openai.query import Query

class LlmQueryExecutor:
    def __init__(self, run_id, save_dir="outputs"):
        self.run_id = run_id
        self.save_dir = save_dir
    
    def execute(self, step: Step, dependencies: dict):
        system_message = step.prompt_text.format(**dependencies)

        query = Query(
            model=step.query_params.model, 
            temperature=step.query_params.temperature, 
            max_tokens=step.query_params.max_tokens, 
            top_p=step.query_params.top_p, 
            frequency_penalty=step.query_params.frequency_penalty,
            system_message=system_message
            )

        if step.response_type == "json":
            eval_literal = True
        else:
            eval_literal = False
        return query.run(eval_literal=eval_literal)