from __future__ import annotations
from dataclasses import dataclass,field
import heapq,time,itertools
from .models import ComputeJob
@dataclass(order=True)
class QueuedJob:
    sort_key:tuple; job:ComputeJob=field(compare=False); priority:int=field(default=0,compare=False); enqueued_at:float=field(default_factory=time.time,compare=False)
class JobQueue:
    def __init__(self): self._q=[]; self._seq=itertools.count(); self._ids=set()
    def push(self,job:ComputeJob,priority:int=0):
        if job.id in self._ids: raise ValueError("job already queued")
        self._ids.add(job.id); heapq.heappush(self._q,QueuedJob((-priority,next(self._seq)),job,priority))
    def pop(self):
        if not self._q:return None
        x=heapq.heappop(self._q); self._ids.remove(x.job.id); return x.job
    def __len__(self):return len(self._q)
