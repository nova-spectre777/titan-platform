from __future__ import annotations
from dataclasses import dataclass,field
from .models import WorkItem,WorkStatus
@dataclass(slots=True)
class VerificationResult:
    passed:bool; checks:dict[str,bool]; notes:list[str]=field(default_factory=list)
class WorkVerifier:
    def verify(self,item:WorkItem,evidence:dict[str,object])->VerificationResult:
        checks={}
        for criterion in item.acceptance:
            key=self._key(criterion); checks[criterion]=bool(evidence.get(key) or evidence.get(criterion))
        if not checks: checks["work produced output"]=bool(evidence)
        passed=all(checks.values())
        return VerificationResult(passed,checks,[] if passed else ["one or more acceptance criteria lack evidence"])
    def finalize(self,item:WorkItem,result:VerificationResult):
        item.status=WorkStatus.DONE if result.passed else WorkStatus.FAILED
    @staticmethod
    def _key(s): return "_".join("".join(ch.lower() if ch.isalnum() else " " for ch in s).split())
