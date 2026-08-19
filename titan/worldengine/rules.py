from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
from .models import WorldState
@dataclass(slots=True)
class Rule:
    name:str; predicate:Callable[[WorldState],bool]; consequence:dict[str,object]
class RuleEngine:
    def __init__(self,rules:list[Rule]|None=None): self.rules=rules or []
    def add(self,r:Rule): self.rules.append(r)
    def evaluate(self,state:WorldState): return [r for r in self.rules if r.predicate(state)]
    def apply(self,state:WorldState,iterations:int=1)->WorldState:
        values=dict(state.values); confidence=dict(state.confidence)
        result=WorldState(values,confidence)
        for _ in range(max(1,iterations)):
            changed=False
            for r in self.evaluate(result):
                for k,v in r.consequence.items():
                    if result.values.get(k)!=v: result.values[k]=v; result.confidence[k]=min(result.confidence.get(k,1),.7); changed=True
            if not changed: break
        return result
