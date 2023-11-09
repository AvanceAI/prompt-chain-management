from typing import List, Union
from pydantic import BaseModel, Field
from src.tools.google_search.searcher import Searcher
from src.core.logger import get_logger
from src.utils.dependency_resolver import resolve_dependencies

logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    total_results: Union[int, None] = Field(None, description="The total number of results to return.")

class SearchAgent:
    def __init__(self, agent_params, input_resolver=None):
        self.agent_params = AgentParams(**agent_params)
        self.searcher = Searcher(total_results=self.agent_params.total_results)

    async def execute(self, variable_store):
        logger.info("Executing search step")
        
        if len(self.agent_params.dependencies) > 1:
            raise ValueError("SearchAgent can only have one dependency.")
        
        dependencies = resolve_dependencies(self.agent_params, variable_store)
        
        results = self.searcher.run(query=dependencies["topic"])
        logger.info("Search step executed successfully")
        return results
