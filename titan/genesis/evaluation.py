from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any,Callable
@dataclass(slots=True)
class Case:
    input:Any; expected:Any; tags:set[str]=field(default_factory=set)
@dataclass(slots=True)
class EvalReport:
    passed:int; failed:int; failures:list[dict]
    @property
    def score(self): return self.passed/max(1,self.passed+self.failed)
class Evaluator:
    def run(self,cases:list[Case],fn:Callable[[Any],Any],judge:Callable[[Any,Any],bool]|None=None):
        judge=judge or (lambda a,b:a==b); p=f=0; failures=[]
        for i,c in enumerate(cases):
            try: actual=fn(c.input); ok=judge(actual,c.expected)
            except Exception as e: actual=f"{type(e).__name__}: {e}"; ok=False
            if ok:p+=1
            else:f+=1; failures.append({"index":i,"input":c.input,"expected":c.expected,"actual":actual})
        return EvalReport(p,f,failures)
