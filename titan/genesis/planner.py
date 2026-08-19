from __future__ import annotations
from .models import AIRequirement, AIBlueprint

class GenesisPlanner:
    def design(self,r:AIRequirement)->AIBlueprint:
        if not r.task.strip(): raise ValueError("task required")
        local=r.privacy in {"private","strict"}
        if "image" in r.modalities: model="multimodal-capable model adapter"
        elif r.budget=="low": model="small instruct model with provider adapter"
        else: model="quality-first general model with fallback"
        if local: model="local/self-hosted "+model
        retrieval="hybrid lexical + vector retrieval with citations" if r.needs_retrieval else None
        evaluation=["task success set","regression cases","latency budget","cost tracking"]
        if r.needs_retrieval: evaluation += ["retrieval recall","citation correctness"]
        guardrails=["input validation","structured outputs where possible","permissioned tools","human review for destructive actions"]
        if r.needs_tools: guardrails += ["tool allowlist","argument schema validation"]
        serving="local API gateway" if local else "provider-neutral model gateway"
        return AIBlueprint(model,retrieval,evaluation,guardrails,serving,[f"latency={r.latency}",f"budget={r.budget}"])
