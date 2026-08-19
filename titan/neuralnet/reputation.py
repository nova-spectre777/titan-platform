from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(slots=True)
class Outcome:
    success:bool; weight:float=1; note:str=""
class ReputationLedger:
    def __init__(self,prior:float=.5): self.prior=prior; self.outcomes:dict[str,list[Outcome]]={}
    def record(self,agent_id:str,outcome:Outcome): self.outcomes.setdefault(agent_id,[]).append(outcome)
    def score(self,agent_id:str)->float:
        xs=self.outcomes.get(agent_id,[])
        if not xs:return self.prior
        pos=sum(x.weight for x in xs if x.success); total=sum(x.weight for x in xs)
        return round((self.prior*2+pos)/(2+total),4)
