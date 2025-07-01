from agent import Agent
from typing import List,Any

class WorkerAgent(Agent):
    def __init__(self):
        #super().__init__( # args ) # must call super init with required parameters as defined in agent abstract interface
        raise NotImplementedError
    

    """
    Sample prompt from orchestrator agent:
    "Research school mergers in the 1990s that involved combining a girls' and a boys' school to form a coeducational school, given a Latin name, in a town with a history reaching back to the second half of the 19th century. Specifically, identify the name of the original girls' school that was part of this merger."
    
    """