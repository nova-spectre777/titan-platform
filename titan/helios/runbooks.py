from __future__ import annotations
from dataclasses import dataclass,field
from titan.core.models import Step,Risk,Plan
@dataclass(slots=True)
class Runbook:
    name:str; match_terms:set[str]; steps:list[Step]; risk:Risk=Risk.MEDIUM; tags:set[str]=field(default_factory=set)
class RunbookRegistry:
    def __init__(self):self.items=[]
    def add(self,r:Runbook):self.items.append(r)
    def match(self,text:str):
        words=set(text.lower().replace('/',' ').replace('-',' ').split())
        return sorted(((len(words&r.match_terms),r) for r in self.items if words&r.match_terms),key=lambda x:x[0],reverse=True)
    def plan(self,text:str):
        matches=self.match(text)
        if not matches:return None
        r=matches[0][1]; return Plan("helios.runbook",r.name,list(r.steps),r.risk,metadata={"tags":sorted(r.tags)})
