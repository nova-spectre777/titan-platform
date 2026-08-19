from __future__ import annotations
from dataclasses import dataclass
from .models import Decision, Plan, Risk

@dataclass(slots=True)
class PolicyResult:
    decision: Decision
    reason: str

class PolicyEngine:
    """Small explicit safety gate used by the top-level runtime."""
    def __init__(self, allow_destructive: bool=False, max_auto_risk: Risk=Risk.MEDIUM):
        self.allow_destructive=allow_destructive
        self.max_auto_risk=max_auto_risk
        self._order={Risk.LOW:0,Risk.MEDIUM:1,Risk.HIGH:2,Risk.CRITICAL:3}

    def evaluate(self, plan: Plan) -> PolicyResult:
        if plan.destructive and not self.allow_destructive:
            return PolicyResult(Decision.REVIEW,"destructive action requires explicit approval")
        if self._order[plan.risk] > self._order[self.max_auto_risk]:
            return PolicyResult(Decision.REVIEW,f"risk {plan.risk.value} exceeds automatic threshold")
        return PolicyResult(Decision.ALLOW,"plan is within configured policy")
