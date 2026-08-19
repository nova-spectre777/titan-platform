from __future__ import annotations
from dataclasses import dataclass,field
from enum import Enum
import time,uuid
class SessionState(str,Enum): CREATED='created'; ACTIVE='active'; PAUSED='paused'; CLOSED='closed'
@dataclass(slots=True)
class Session:
    intent_id:str; workspace:str|None=None; state:SessionState=SessionState.CREATED; id:str=field(default_factory=lambda:uuid.uuid4().hex[:12]); started_at:float=field(default_factory=time.time); notes:list[str]=field(default_factory=list)
class SessionManager:
    def __init__(self):self.sessions={}
    def create(self,intent_id:str,workspace:str|None=None):
        s=Session(intent_id,workspace);self.sessions[s.id]=s;return s
    def activate(self,id:str):self.sessions[id].state=SessionState.ACTIVE
    def pause(self,id:str,note:str=''):self.sessions[id].state=SessionState.PAUSED; self.sessions[id].notes.append(note) if note else None
    def close(self,id:str):self.sessions[id].state=SessionState.CLOSED
