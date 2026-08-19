from dataclasses import dataclass, field
from enum import Enum
import time, uuid

class Severity(str,Enum): LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"
@dataclass(slots=True)
class Incident:
    service:str; symptom:str; signals:dict[str,float|str|bool]=field(default_factory=dict); severity:Severity=Severity.MEDIUM; id:str=field(default_factory=lambda:uuid.uuid4().hex[:10]); opened_at:float=field(default_factory=time.time)
@dataclass(slots=True)
class Diagnosis:
    likely_causes:list[tuple[str,float]]; evidence:list[str]; confidence:float
