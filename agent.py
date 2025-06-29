from typing import List,Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth

@dataclass
class Agent(ABC):
    name: str
    description: str
    system_prompt: str #describe task here
    tools_available: List[str] = field(default_factory=list)
    messages:List[dict[str,str]] = field(default_factory=list) # ensures each instance has its own separate list
    datetime_created:str
    health: AgentHealth
    total_cost: float
    total_prompt_tokens: int
    total_completion_tokens: int
    model: str

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def get_mcp(self):
        #return mcp for this agent so that other agents know what it does and how to interact with it
        """
        schema = {
            "name":self.name,
            "description":self.description,
            "parameters":{
                "type": "Agent",
                "properties":{

                },
                "required":["name",]
            }
        }
        """
        raise NotImplementedError
    
    def heartbeat(self) -> AgentHealth:
        return self.health
    
    def restart(self)->None:
        # clear message history
        raise NotImplementedError