from __future__ import annotations
from .models import Incident, Diagnosis, Severity
from titan.core.models import Plan, Step, Risk

class Helios:
    def diagnose(self,i:Incident)->Diagnosis:
        causes=[]; ev=[]; s=i.symptom.lower(); signals=i.signals
        if "timeout" in s or float(signals.get("latency_ms",0) or 0)>2000: causes.append(("upstream saturation or network latency",.72)); ev.append("latency/timeout signal")
        if "memory" in s or float(signals.get("memory_pct",0) or 0)>92: causes.append(("memory pressure",.86)); ev.append("high memory")
        if "disk" in s or float(signals.get("disk_pct",0) or 0)>95: causes.append(("disk exhaustion",.9)); ev.append("disk capacity critical")
        if float(signals.get("error_rate",0) or 0)>.2: causes.append(("application or dependency failure",.68)); ev.append("elevated error rate")
        if not causes: causes=[("unknown; collect more telemetry",.2)]; ev=["insufficient discriminating signals"]
        causes.sort(key=lambda x:x[1],reverse=True)
        return Diagnosis(causes,ev,causes[0][1])

    def remediate(self,i:Incident,d:Diagnosis)->Plan:
        steps=[Step("Capture diagnostics","collect logs, metrics and recent deployment metadata")]
        top=d.likely_causes[0][0]
        destructive=False
        if "memory" in top: steps += [Step("Reduce pressure","scale/restart candidate requires approval",destructive=True)] ; destructive=True
        elif "disk" in top: steps += [Step("Free or expand storage","cleanup/resize requires approval",destructive=True)] ; destructive=True
        elif "latency" in top or "saturation" in top: steps += [Step("Shift traffic","fail over or scale healthy capacity",destructive=True)] ; destructive=True
        else: steps += [Step("Create diagnostic branch","reproduce failure in isolated environment")]
        risk=Risk.HIGH if i.severity in {Severity.HIGH,Severity.CRITICAL} or destructive else Risk.MEDIUM
        return Plan("helios.remediation",f"Recover {i.service}",steps,risk,metadata={"incident":i.id,"confidence":d.confidence})
