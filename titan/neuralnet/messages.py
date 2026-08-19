from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
import time,uuid
@dataclass(slots=True,frozen=True)
class Envelope:
    sender:str; recipient:str; kind:str; payload:dict[str,Any]; correlation_id:str|None=None; id:str=field(default_factory=lambda:uuid.uuid4().hex); timestamp:float=field(default_factory=time.time)
class MessageBus:
    def __init__(self): self.queues:dict[str,list[Envelope]]={}; self.seen:set[str]=set()
    def send(self,e:Envelope):
        if e.id in self.seen:return False
        self.seen.add(e.id); self.queues.setdefault(e.recipient,[]).append(e); return True
    def receive(self,recipient:str,limit:int=100):
        q=self.queues.setdefault(recipient,[]); out=q[:limit]; del q[:limit]; return out
