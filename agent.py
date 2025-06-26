from typing import List,Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth

@dataclass
class Agent(ABC):
    name: str
    description: str
    system_prompt: str
    messages:List[dict[str,str]] = field(default_factory=list) # ensures each instance has its own separate list
    datetime_created:str
    health: AgentHealth

    @abstractmethod
    def get_mcp(self):
        #return mcp for this agent so that other agents know what it does and how to interact with it
        raise NotImplementedError
    
    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError