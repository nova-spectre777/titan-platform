from __future__ import annotations
from .models import WorkItem, WorkStatus

class FactoryBoard:
    def __init__(self, items:list[WorkItem]):
        self.items={x.id:x for x in items}
        self._validate()

    def _validate(self):
        for item in self.items.values():
            unknown=set(item.depends_on)-self.items.keys()
            if unknown: raise ValueError(f"unknown dependencies for {item.id}: {sorted(unknown)}")
        visiting=set(); visited=set()
        def walk(i):
            if i in visiting: raise ValueError("dependency cycle")
            if i in visited: return
            visiting.add(i)
            for d in self.items[i].depends_on: walk(d)
            visiting.remove(i); visited.add(i)
        for i in self.items: walk(i)

    def ready(self)->list[WorkItem]:
        out=[]
        for x in self.items.values():
            if x.status in {WorkStatus.DONE,WorkStatus.RUNNING,WorkStatus.FAILED,WorkStatus.BLOCKED}: continue
            deps=[self.items[d] for d in x.depends_on]
            if any(d.status in {WorkStatus.FAILED,WorkStatus.BLOCKED} for d in deps): x.status=WorkStatus.BLOCKED
            elif all(d.status==WorkStatus.DONE for d in deps): x.status=WorkStatus.READY; out.append(x)
        return out

    def complete(self,item_id:str,ok:bool=True):
        x=self.items[item_id]; x.status=WorkStatus.DONE if ok else WorkStatus.FAILED
        self.ready()
