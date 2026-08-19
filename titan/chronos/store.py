from __future__ import annotations
from .models import Snapshot,SnapshotDiff
from titan.core.models import Plan,Step,Risk

class ChronosStore:
    def __init__(self): self._snapshots:dict[str,Snapshot]={}
    def save(self,s:Snapshot): self._snapshots[s.digest]=s
    def get(self,digest:str)->Snapshot: return self._snapshots[digest]
    def diff(self,a:Snapshot,b:Snapshot)->SnapshotDiff:
        ak=set(a.manifest); bk=set(b.manifest)
        return SnapshotDiff({k:b.manifest[k] for k in bk-ak},{k:a.manifest[k] for k in ak-bk},{k:(a.manifest[k],b.manifest[k]) for k in ak&bk if a.manifest[k]!=b.manifest[k]})
    def restore_plan(self,target:Snapshot,current:Snapshot)->Plan:
        d=self.diff(current,target); steps=[]
        for k,v in d.added.items(): steps.append(Step(f"Create {k}",f"restore value {v!r}",destructive=True))
        for k,(old,new) in d.changed.items(): steps.append(Step(f"Change {k}",f"{old!r} -> {new!r}",destructive=True))
        for k in d.removed: steps.append(Step(f"Remove {k}","delete resource/state",destructive=True))
        return Plan("chronos.restore",f"Restore snapshot {target.name}",steps,Risk.CRITICAL,metadata={"target":target.digest})
