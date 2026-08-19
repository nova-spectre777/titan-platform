from dataclasses import dataclass, field

@dataclass(slots=True)
class BackendNeed:
    database:bool=True; auth:bool=False; storage:bool=False; queue:bool=False; realtime:bool=False; search:bool=False; ai:bool=False; constraints:set[str]=field(default_factory=set)
@dataclass(slots=True)
class ResourceOption:
    kind:str; provider:str; capabilities:set[str]; cost_tier:int=0; self_hosted:bool=False
@dataclass(slots=True)
class BackendPlan:
    resources:dict[str,ResourceOption]; warnings:list[str]
