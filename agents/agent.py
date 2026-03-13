from pydantic import BaseModel
from typing import List

class Agent(BaseModel):
    name: str
    description: str
    capabilities: List[str]
    owner: str
