from __future__ import annotations
from .models import Provider, Workload, Placement

class OrbitScheduler:
    def eligible(self,w:Workload,p:Provider)->tuple[bool,list[str]]:
        reasons=[]
        if not p.healthy: reasons.append("unhealthy")
        if p.cpu<w.cpu: reasons.append("insufficient cpu")
        if p.memory_gb<w.memory_gb: reasons.append("insufficient memory")
        if p.gpu<w.gpu: reasons.append("insufficient gpu")
        if w.max_hourly_cost is not None and p.hourly_cost>w.max_hourly_cost: reasons.append("over budget")
        if not w.required_tags.issubset(p.tags): reasons.append("missing required tags")
        return not reasons,reasons

    def score(self,w:Workload,p:Provider)->Placement:
        ok,reasons=self.eligible(w,p)
        if not ok: return Placement(p.name,float("-inf"),reasons)
        cost=max(0.0,10.0-p.hourly_cost*10)
        latency=max(0.0,10.0-p.latency_ms/20)
        region=4.0 if w.preferred_regions and p.region in w.preferred_regions else 0.0
        headroom=min(5.0,(p.cpu-w.cpu)*.25+(p.memory_gb-w.memory_gb)*.1+(p.gpu-w.gpu))
        return Placement(p.name,cost+latency+region+headroom,[f"cost={p.hourly_cost:.3f}",f"latency={p.latency_ms:.0f}ms",f"region={p.region}"])

    def place(self,w:Workload,providers:list[Provider])->Placement:
        ranked=sorted((self.score(w,p) for p in providers),key=lambda x:x.score,reverse=True)
        if not ranked or ranked[0].score==float("-inf"): raise RuntimeError("no eligible provider")
        return ranked[0]

    def failover(self,w:Workload,providers:list[Provider],current:str)->Placement:
        return self.place(w,[p for p in providers if p.name!=current])
