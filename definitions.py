from dataclasses import dataclass
from typing import List,Any,Tuple

@dataclass
class Tool:
    signature:str # similar signatures ==> similar tool calls ==> similar action taken
                  # semantic hashes can be stored in memory. Similar hashes can be found. Maybe just use KKN/semantic search for this? Have to consider latency, maybe for long term memory its alright.
                  # mabye use semantic hashing?
    name:str
    input:dict[str,Any]
    datetime:str

@dataclass
class Thinking:
    signature:str # have to think more about why Anthropic decided to use a signature instead of a raw ID.
                  # maybe to store in long term memory semanticly? 
    content:str
    datetime:str
    
@dataclass
class Text:
    id:str
    content:str
    datetime:str

@dataclass
class AgentHealth:
    #context_length: int
    health_score: float # [0,1], basically just how much of their context window they've used. 0 --> None, 1 --> full

@dataclass
class System:
    total_active_agents: int
    total_agents_created: int
    total_token_usage: int 
    total_cost: float
    total_tool_calls: int
    task_start_time: Any
    task_end_time: Any

@dataclass
class Model:
    name:str
    context_window:str
    description: str # e.g. Large model execellent for reasoning and long horizon planning
    input_cost: float
    output_cost: float


#@dataclass
#class Message:
