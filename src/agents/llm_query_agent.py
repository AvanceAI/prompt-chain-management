from typing import List, Union
from pydantic import BaseModel, Field
from src.models.chain import QueryParams
from src.repository.openai.query import Query
from src.repository.openai.completion_query import CompletionQuery
from src.core.logger import get_logger
from src.utils.dependency_resolver import resolve_dependencies

logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    query_params: QueryParams = Field(..., description="The model settings aka 'query parameters'.")
    prompt_text: Union[str, None] = Field(None, description="The prompt text if applicable.")

class LlmQueryAgent:
    def __init__(self, agent_params, dependency_resolver=None):
        self.agent_params = AgentParams(**agent_params)
    
    def _run_completions_api_query(self, system_message):
        query = CompletionQuery(
            model=self.agent_params.query_params.model, 
            temperature=self.agent_params.query_params.temperature, 
            max_tokens=self.agent_params.query_params.max_tokens, 
            top_p=self.agent_params.query_params.top_p, 
            frequency_penalty=self.agent_params.query_params.frequency_penalty
            )
        return query.run(prompt=system_message, eval_literal=self.agent_params.query_params.eval_literal)
    
    def _run_chat_api_query(self, system_message):
        query = Query(
            model=self.agent_params.query_params.model, 
            temperature=self.agent_params.query_params.temperature, 
            max_tokens=self.agent_params.query_params.max_tokens, 
            top_p=self.agent_params.query_params.top_p, 
            frequency_penalty=self.agent_params.query_params.frequency_penalty,
            system_message=system_message
            )
        return query.run(eval_literal=self.agent_params.query_params.eval_literal)
    
    
    def execute(self, variable_store):
        logger.info("Executing LLM query self.agent_params")
 
        dependencies = resolve_dependencies(self.agent_params, variable_store)
        
        system_message = self.agent_params.prompt_text.format(**dependencies)
        if self.agent_params.query_params.model == "gpt-3.5-turbo-instruct":
            results = self._run_completions_api_query(system_message)
        else:
            results = self._run_chat_api_query(system_message)
        logger.info("LLM query self.agent_params executed successfully")
        return results
    