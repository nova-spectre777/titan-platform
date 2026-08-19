from dataclasses import dataclass, field
import time, uuid

@dataclass(slots=True)
class AgentIdentity:
    name:str; capabilities:set[str]; trust:float=.5; endpoint:str|None=None; labels:set[str]=field(default_factory=set); id:str=field(default_factory=lambda:uuid.uuid4().hex[:12]); last_seen:float=field(default_factory=time.time)
    def __post_init__(self): self.trust=max(0.0,min(1.0,float(self.trust)))

@dataclass(slots=True)
class TaskContract:
    task:str; required:set[str]; max_agents:int=1; minimum_trust:float=.0; id:str=field(default_factory=lambda:uuid.uuid4().hex[:10])
