from typing import List
from pydantic import BaseModel, Field

class QueryParams(BaseModel):
    model: str = Field(..., description="The model to use for the query.")
    temperature: float = Field(..., description="The temperature for the query.")
    max_tokens: int = Field(..., description="The maximum number of tokens to generate.")
    top_p: float = Field(..., description="The top p value for the query.")
    frequency_penalty: float = Field(..., description="The frequency penalty for the query.")
    presence_penalty: float = Field(..., description="The presence penalty for the query.")
    eval_literal: bool = Field(..., description="Whether to evaluate the literal or not.")
    
class Output(BaseModel):
    name: str = Field(..., description="The name of the output.")
    type: str = Field(..., description="The type of the output.")
    
class Step(BaseModel):
    step_id: str = Field(..., description="Unique identifier for the Step.")
    description: str = Field(..., description="The description of the Step.")
    agent: str = Field(..., description="The agent to use for the Step.")
    agent_params: dict = Field(..., description="The parameters for the agent.")
    output: Output = Field(..., description="The output of the Step.")
    
class Chain(BaseModel):
    chain_id: str = Field(..., description="Unique identifier for the chain.")
    chain_title: str = Field(..., description="Title of the chain.")
    chain_description: str = Field(None, description="Description of the chain's purpose.")
    version: str = Field(None, description="Version of the chain.")
    steps: List[Step] = Field(..., description="List of Steps in the chain.")
