from dataclasses import dataclass,field
from typing import List,Any,Tuple, Union
from utils import uid_hash, get_datetime
from datetime import datetime

@dataclass
class Tool:
    name:str
    input:dict[str,Any]
    signature:str = field(default_factory=uid_hash) # similar signatures ==> similar tool calls ==> similar action taken
                  # semantic hashes can be stored in memory. Similar hashes can be found. Maybe just use KKN/semantic search for this? Have to consider latency, maybe for long term memory its alright.
                  # mabye use semantic hashing?
    datetime:str = field(default_factory=get_datetime)

@dataclass
class Thinking:
    content:str
    signature:str = field(default_factory=uid_hash) # have to think more about why Anthropic decided to use a signature instead of a raw ID.
                  # maybe to store in long term memory semanticly? 
    datetime:str = field(default_factory=get_datetime)
    
@dataclass
class Text:
    content:str
    id:str = field(default_factory=uid_hash)
    datetime:str = field(default_factory=get_datetime)

@dataclass
class AgentHealth:
    #context_length: int
    health_score: float # [0,1], basically just how much of their context window they've used. 0 --> None, 1 --> full

@dataclass
class System:
    total_active_agents: int
    total_agents_created: int
    total_prompt_tokens: int 
    total_completion_tokens: int
    total_cost: float
    total_tool_calls: int
    task_start_time: Any
    task_end_time: Any

@dataclass
class Model:
    name: str
    client: Any
    context_window: int
    description: Union[str,None] # e.g. Large model execellent for reasoning and long horizon planning
    input_cost: float
    output_cost: float


@dataclass
class MemoryNode:
    agent_uid: str # the agent who this memory belongs to.
    content:Union[Thinking,Tool]
    memory_uid: str = field(default_factory=uid_hash) # uid for memory obj

#@dataclass
#class Message:
