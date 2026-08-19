from __future__ import annotations
from .models import Node, ComputeJob, Lease
import time

class SynapseScheduler:
    def __init__(self,lease_seconds:int=60): self.lease_seconds=lease_seconds; self.nodes:dict[str,Node]={}; self.leases:dict[str,Lease]={}
    def add_node(self,n:Node): self.nodes[n.id]=n
    def heartbeat(self,node_id:str): self.nodes[node_id].last_seen=time.time(); self.nodes[node_id].healthy=True
    def candidates(self,j:ComputeJob)->list[Node]:
        now=time.time(); out=[]
        busy={l.node_id for l in self.leases.values() if l.expires_at>now}
        for n in self.nodes.values():
            if n.id in busy or not n.healthy or now-n.last_seen>120: continue
            if n.cpu<j.cpu or n.memory_gb<j.memory_gb or n.gpu<j.gpu or n.trust<j.min_trust or not j.required.issubset(n.capabilities): continue
            out.append(n)
        return sorted(out,key=lambda n:(n.trust,n.gpu,n.cpu,n.memory_gb),reverse=True)
    def schedule(self,j:ComputeJob)->Lease:
        c=self.candidates(j)
        if not c: raise RuntimeError("no eligible compute node")
        lease=Lease(j.id,c[0].id,time.time()+self.lease_seconds); self.leases[j.id]=lease; return lease
    def renew(self,job_id:str,token:str)->Lease:
        l=self.leases[job_id]
        if l.token!=token: raise PermissionError("invalid lease token")
        l.expires_at=time.time()+self.lease_seconds; return l
    def release(self,job_id:str,token:str)->None:
        l=self.leases[job_id]
        if l.token!=token: raise PermissionError("invalid lease token")
        del self.leases[job_id]
