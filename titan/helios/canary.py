from __future__ import annotations
from dataclasses import dataclass
@dataclass(slots=True)
class CanaryObservation:
    error_rate:float; latency_ms:float; success_rate:float
@dataclass(slots=True)
class CanaryDecision:
    promote:bool; reasons:list[str]
class CanaryGuard:
    def evaluate(self,baseline:CanaryObservation,candidate:CanaryObservation,max_error_delta:float=.02,max_latency_ratio:float=1.25):
        reasons=[]
        if candidate.error_rate>baseline.error_rate+max_error_delta: reasons.append("error rate regressed")
        if baseline.latency_ms>0 and candidate.latency_ms>baseline.latency_ms*max_latency_ratio: reasons.append("latency regressed")
        if candidate.success_rate<baseline.success_rate-.02: reasons.append("success rate regressed")
        return CanaryDecision(not reasons,reasons or ["candidate within configured guardrails"])
