from dataclasses import dataclass, field

@dataclass(slots=True)
class AIRequirement:
    task:str; latency:str="interactive"; privacy:str="standard"; modalities:set[str]=field(default_factory=lambda:{"text"}); needs_retrieval:bool=False; needs_tools:bool=False; budget:str="low"

@dataclass(slots=True)
class AIBlueprint:
    model_strategy:str; retrieval:str|None; evaluation:list[str]; guardrails:list[str]; serving:str; notes:list[str]=field(default_factory=list)
