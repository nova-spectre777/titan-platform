from dataclasses import dataclass,field
from enum import Enum
import uuid,time

class IntentStatus(str,Enum): NEW="new"; PLANNED="planned"; ACTIVE="active"; DONE="done"; FAILED="failed"
@dataclass(slots=True)
class Intent:
    text:str; owner:str="local-user"; status:IntentStatus=IntentStatus.NEW; id:str=field(default_factory=lambda:uuid.uuid4().hex[:10]); created_at:float=field(default_factory=time.time)
@dataclass(slots=True)
class Workspace:
    name:str; root:str; permissions:set[str]=field(default_factory=lambda:{"read","write"}); metadata:dict=field(default_factory=dict)
