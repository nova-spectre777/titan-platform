from __future__ import annotations
from .models import BackendNeed,ResourceOption,BackendPlan

class OmniFabricPlanner:
    def plan(self,n:BackendNeed,options:list[ResourceOption])->BackendPlan:
        requested={k for k in ("database","auth","storage","queue","realtime","search","ai") if getattr(n,k)}
        selected={}; warnings=[]
        for kind in requested:
            candidates=[o for o in options if o.kind==kind and n.constraints.issubset(o.capabilities|({"self-hosted"} if o.self_hosted else set()))]
            if not candidates:
                warnings.append(f"no provider satisfies {kind}"); continue
            candidates.sort(key=lambda o:(o.cost_tier,not o.self_hosted,-len(o.capabilities)))
            selected[kind]=candidates[0]
        return BackendPlan(selected,warnings)
