from dataclasses import dataclass, field
import time

@dataclass(slots=True)
class Provider:
    name:str; region:str; cpu:int; memory_gb:float; gpu:int=0; hourly_cost:float=0.0; latency_ms:float=50; healthy:bool=True; tags:set[str]=field(default_factory=set)

@dataclass(slots=True)
class Workload:
    name:str; cpu:int=1; memory_gb:float=1; gpu:int=0; max_hourly_cost:float|None=None; preferred_regions:list[str]=field(default_factory=list); required_tags:set[str]=field(default_factory=set)

@dataclass(slots=True)
class Placement:
    provider:str; score:float; reasons:list[str]; created_at:float=field(default_factory=time.time)
