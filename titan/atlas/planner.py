from __future__ import annotations
from .models import ProductSpec, WorkItem
from titan.core.models import Plan, Step, Risk

class AtlasPlanner:
    def derive_spec(self, idea: str) -> ProductSpec:
        idea=" ".join(idea.split())
        if len(idea)<8: raise ValueError("idea is too short to derive a useful product spec")
        lower=idea.lower()
        features=["authentication","observability","testing"]
        if "ai" in lower: features += ["model adapter","evaluation harness"]
        if any(x in lower for x in ("self-host","self hosted","local")): features += ["self-hosted deployment"]
        if any(x in lower for x in ("analytics","dashboard")): features += ["analytics dashboard"]
        return ProductSpec(name=self._name(idea),goal=idea,users=["operator","developer"],constraints=["local-first core","review destructive actions"],features=list(dict.fromkeys(features)))

    def work_graph(self, spec: ProductSpec) -> list[WorkItem]:
        architecture=WorkItem("Define architecture","architecture",acceptance=["components documented","interfaces identified"])
        backend=WorkItem("Implement backend core","backend",[architecture.id],acceptance=["core API works","validation covered"])
        data=WorkItem("Implement data model","data",[architecture.id],acceptance=["schema documented","migrations planned"])
        frontend=WorkItem("Implement operator UI","frontend",[backend.id],acceptance=["primary flows usable"])
        tests=WorkItem("Build verification suite","qa",[backend.id,data.id],acceptance=["failure paths covered","offline tests pass"])
        security=WorkItem("Review trust boundaries","security",[architecture.id,backend.id],acceptance=["threat model updated"])
        release=WorkItem("Prepare release","devops",[frontend.id,tests.id,security.id],acceptance=["build reproducible","release notes ready"])
        return [architecture,backend,data,frontend,tests,security,release]

    def plan(self, idea: str) -> Plan:
        spec=self.derive_spec(idea); graph=self.work_graph(spec)
        return Plan("atlas.factory",f"Build {spec.name}",[Step(w.title,f"{w.discipline}:{w.id}",metadata={"depends_on":w.depends_on,"acceptance":w.acceptance}) for w in graph],Risk.MEDIUM,metadata={"spec":spec.__dict__ if hasattr(spec,'__dict__') else {"name":spec.name,"goal":spec.goal,"features":spec.features}})

    def _name(self,idea:str)->str:
        words=[w.strip(".,:;!?()[]{}") for w in idea.split() if len(w)>2]
        return " ".join(words[:4]).title() or "Untitled Product"
