from dataclasses import dataclass, field
import time, uuid

@dataclass(slots=True)
class Node:
    name:str; cpu:int; memory_gb:float; gpu:int=0; capabilities:set[str]=field(default_factory=set); trust:float=.5; healthy:bool=True; id:str=field(default_factory=lambda:uuid.uuid4().hex[:10]); last_seen:float=field(default_factory=time.time)

@dataclass(slots=True)
class ComputeJob:
    command:str; cpu:int=1; memory_gb:float=1; gpu:int=0; required:set[str]=field(default_factory=set); min_trust:float=.0; id:str=field(default_factory=lambda:uuid.uuid4().hex[:10])

@dataclass(slots=True)
class Lease:
    job_id:str; node_id:str; expires_at:float; token:str=field(default_factory=lambda:uuid.uuid4().hex)
