from typing import List, Union
from pydantic import BaseModel, Field
from src.models.chain import QueryParams
from src.repository.openai.query import Query
from src.repository.openai.completion_query import CompletionQuery
from src.core.logger import get_logger
from src.utils.dependency_resolver import resolve_dependencies
from src.tools.web_scrape import get_text_requests
import multiprocessing
from multiprocessing import Manager


logger = get_logger(__name__)

class AgentParams(BaseModel):
    dependencies: Union[List[str], None] = Field(None, description="List of dependencies/variables that the agent needs to execute its task/step.")
    query_params: QueryParams = Field(..., description="The model settings aka 'query parameters'.")
    prompt_text: Union[str, None] = Field(None, description="The prompt text if applicable.")

class MultiprocessingOutlineAgent:
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


    def _process_url(self, href, shared_dict):
        """
        Process each URL by scraping and querying. Catch exceptions and store them in shared_dict.
        """
        try:
            # Scrape the text from the URL
            scraped_text = get_text_requests(url_to_scrape=href)

            # Determine which query to run based on the agent's parameters
            system_message = self.agent_params.prompt_text.format(scraped_text=scraped_text)
            if self.agent_params.query_params.model == "gpt-3.5-turbo-instruct":
                result = self._run_completions_api_query(system_message)
            else:
                result = self._run_chat_api_query(system_message)
            
            # Return the result
            return result
        except Exception as e:
            # Log and store the error information in the shared dictionary
            logger.error(f"Error processing {href}: {e}")
            shared_dict[href] = str(e)
            return None 
    
    async def execute(self, variable_store):
        logger.info("Executing LLM query self.agent_params")
 
        dependencies = resolve_dependencies(self.agent_params, variable_store)
        
        indices = dependencies["themes"][dependencies["selected_theme_key"]]["results"]
        search_results = [dependencies["search_results"][index] for index in indices]
        hrefs = [result["href"] for result in search_results]
        
        manager = Manager()
        shared_dict = manager.dict()  # This shared dictionary will store error information

        # Create a pool of worker processes
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            # Map _process_url to each href, this will start the process pool
            results = pool.starmap(self._process_url, [(href, shared_dict) for href in hrefs])

        # Check for errors in shared_dict
        if shared_dict:
            for href, error in shared_dict.items():
                logger.error(f"Error with URL {href}: {error}")

        logger.info("LLM query self.agent_params executed successfully")
        # It's up to you how to handle the results, whether you need to combine them or return as is
        return results
