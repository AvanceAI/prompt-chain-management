from typing import List
from pydantic import BaseModel, Field
from src.models.prompt import Prompt

class PromptChain(BaseModel):
    chain_id: str = Field(..., description="Unique identifier for the prompt chain.")
    chain_title: str = Field(..., description="Title of the prompt chain.")
    chain_description: str = Field(None, description="Description of the prompt chain's purpose.")
    version: str = Field(None, description="Version of the prompt chain.")
    prompts: List[Prompt] = Field(..., description="List of prompts in the prompt chain.")
