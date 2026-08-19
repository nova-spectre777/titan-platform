from __future__ import annotations
from .models import AgentIdentity, TaskContract
import time

class AgentDirectory:
    def __init__(self): self._agents:dict[str,AgentIdentity]={}
    def register(self,a:AgentIdentity): self._agents[a.id]=a
    def heartbeat(self,agent_id:str): self._agents[agent_id].last_seen=time.time()
    def discover(self,c:TaskContract,stale_after:float=300)->list[AgentIdentity]:
        now=time.time()
        candidates=[a for a in self._agents.values() if c.required.issubset(a.capabilities) and a.trust>=c.minimum_trust and now-a.last_seen<=stale_after]
        return sorted(candidates,key=lambda a:(a.trust,len(a.capabilities)),reverse=True)[:c.max_agents]
    def adjust_trust(self,agent_id:str,delta:float):
        a=self._agents[agent_id]; a.trust=max(0,min(1,a.trust+delta))
