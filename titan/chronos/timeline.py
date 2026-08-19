from __future__ import annotations
from dataclasses import dataclass,field
import time
@dataclass(slots=True,frozen=True)
class TimelineEvent:
    kind:str; actor:str; subject:str; metadata:dict=field(default_factory=dict); timestamp:float=field(default_factory=time.time)
class Timeline:
    def __init__(self):self.events=[]
    def add(self,event:TimelineEvent): self.events.append(event); self.events.sort(key=lambda x:x.timestamp)
    def between(self,start:float,end:float):return [e for e in self.events if start<=e.timestamp<=end]
    def subject(self,name:str):return [e for e in self.events if e.subject==name]
