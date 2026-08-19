from __future__ import annotations
from dataclasses import dataclass,field
import time
@dataclass(slots=True)
class Memory:
    key:str; value:str; scope:str='workspace'; tags:set[str]=field(default_factory=set); created_at:float=field(default_factory=time.time)
class MemoryStore:
    def __init__(self):self.items:dict[str,Memory]={}
    def remember(self,m:Memory):self.items[f"{m.scope}:{m.key}"]=m
    def recall(self,key:str,scope:str='workspace'):return self.items.get(f"{scope}:{key}")
    def search(self,text:str,scope:str|None=None):
        q=text.lower(); return [m for m in self.items.values() if (scope is None or m.scope==scope) and (q in m.key.lower() or q in m.value.lower() or any(q in t.lower() for t in m.tags))]
