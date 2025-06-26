from typing import List,Any

class Agent:
    def __init__(self):
        self.messages:List[dict[str,str]] = []
        raise NotImplementedError