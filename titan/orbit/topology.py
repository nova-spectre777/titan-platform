from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(slots=True)
class Link:
    a:str; b:str; latency_ms:float; bandwidth_mbps:float; healthy:bool=True
class NetworkTopology:
    def __init__(self): self.links:list[Link]=[]
    def add(self,link:Link):
        if link.a==link.b: raise ValueError("self-link not useful")
        self.links.append(link)
    def neighbors(self,node:str):
        out=[]
        for l in self.links:
            if not l.healthy: continue
            if l.a==node: out.append((l.b,l))
            elif l.b==node: out.append((l.a,l))
        return out
    def shortest_latency(self,start:str,end:str)->float:
        if start==end: return 0
        dist={start:0.0}; pending={start}
        while pending:
            cur=min(pending,key=lambda x:dist[x]); pending.remove(cur)
            if cur==end:return dist[cur]
            for nxt,link in self.neighbors(cur):
                nd=dist[cur]+link.latency_ms
                if nd<dist.get(nxt,float('inf')): dist[nxt]=nd; pending.add(nxt)
        return float('inf')
