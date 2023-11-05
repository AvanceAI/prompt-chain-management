from typing import List
from pydantic import BaseModel, Field

class Prompt(BaseModel):
    prompt_id: str = Field(..., description="Unique identifier for the prompt.")
    prompt_text: str = Field(..., description="The text of the prompt to be sent.")
    response_type: str = Field(..., description="Expected response type.", enum=["text", "json"])
    dependencies: List[str] = Field(default_factory=list, description="List of dependencies that this prompt relies on.")
    parameters: dict = Field(default_factory=dict, description="Parameters that can be passed into the prompt.")
    user_interaction: dict = Field(default_factory=dict, description="Details about user interaction if required.")
    external_service: str = Field(None, description="Name of external service to integrate with the prompt.")

class PromptChain(BaseModel):
    chain_id: str = Field(..., description="Unique identifier for the prompt chain.")
    chain_title: str = Field(..., description="Title of the prompt chain.")
    chain_description: str = Field(None, description="Description of the prompt chain's purpose.")
    version: str = Field(None, description="Version of the prompt chain.")
    prompts: List[Prompt] = Field(..., description="List of prompts in the prompt chain.")
