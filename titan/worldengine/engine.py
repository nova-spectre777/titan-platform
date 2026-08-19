from __future__ import annotations
from .models import Observation, WorldState, Scenario

class WorldEngine:
    def __init__(self): self.state=WorldState(); self.history:list[Observation]=[]
    def ingest(self,obs:Observation):
        if not 0<=obs.confidence<=1: raise ValueError("confidence must be 0..1")
        old=self.state.confidence.get(obs.key,-1)
        if obs.confidence>=old:
            self.state.values[obs.key]=obs.value; self.state.confidence[obs.key]=obs.confidence; self.state.updated_at=obs.timestamp
        self.history.append(obs)
    def fork(self,scenario:Scenario)->WorldState:
        values=dict(self.state.values); values.update(scenario.changes)
        confidence=dict(self.state.confidence)
        for k in scenario.changes: confidence[k]=min(confidence.get(k,1.0),.75)
        return WorldState(values,confidence)
    def compare(self,a:WorldState,b:WorldState)->dict[str,tuple[object,object]]:
        keys=a.values.keys()|b.values.keys(); return {k:(a.values.get(k),b.values.get(k)) for k in keys if a.values.get(k)!=b.values.get(k)}
