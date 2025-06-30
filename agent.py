from typing import List,Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from definitions import AgentHealth, Model

@dataclass
class Agent(ABC):
    name: str
    type: str 
    description: str
    system_prompt: str #describe task here
    datetime_created:str
    health: AgentHealth
    total_cost: float
    total_prompt_tokens: int
    total_completion_tokens: int
    model: Model
    num_tool_calls: int
    terminate: bool = False
    messages:List[dict[str,str]] = field(default_factory=list) # ensures each instance has its own separate list
    tools_available: List[str] = field(default_factory=list)

    @abstractmethod
    def run(self) -> Any:
        raise NotImplementedError
    
    def terminate(self) -> dict[str,Any]:
        self.terminate = True
        raise NotImplementedError

    def heartbeat(self) -> AgentHealth:
        return self.health
    
    def update_health(self) -> None:
        self.health.health_score = self.total_prompt_tokens / self.model.context_window

