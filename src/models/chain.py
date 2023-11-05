from typing import List, Union
from pydantic import BaseModel, Field

class Dependency(BaseModel):
    name: str = Field(..., description="The name of the dependency.")
    type: str = Field(..., description="The type of the dependency.")
    class_: str = Field(..., alias='class', description="The class of the dependency.")

class Output(BaseModel):
    name: str = Field(..., description="The name of the output.")
    type: str = Field(..., description="The type of the output.")
    class_: str = Field(..., alias='class', description="The class of the output.")

class Action(BaseModel):
    name: str = Field(..., description="The name of the action.")
    type: str = Field(..., description="The type of the action.")
    data: Union[str, None] = Field(None, description="The data related to the action.")

class Step(BaseModel):
    step_id: str = Field(..., description="Unique identifier for the Step.")
    description: str = Field(..., description="The description of the Step.")
    step_type: Union[str, None] = Field(None, description="Type of the Step.")
    prompt_text: Union[str, None] = Field(None, description="The prompt text if applicable.")
    response_type: str = Field(..., description="Expected response type.", enum=["text", "json"])
    dependencies: List[Dependency] = Field(default_factory=list, description="List of dependencies that this Step relies on.")
    outputs: List[Output] = Field(default_factory=list, description="List of outputs that this Step returns.")
    actions: Union[List[Action], None] = Field(None, description="List of actions associated with the Step.")

class Chain(BaseModel):
    chain_id: str = Field(..., description="Unique identifier for the chain.")
    chain_title: str = Field(..., description="Title of the chain.")
    chain_description: str = Field(None, description="Description of the chain's purpose.")
    version: str = Field(None, description="Version of the chain.")
    steps: List[Step] = Field(..., description="List of Steps in the chain.")
