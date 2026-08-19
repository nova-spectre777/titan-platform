from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class Component:
    name: str
    instance: Any
    tags: set[str]=field(default_factory=set)

class ComponentRegistry:
    def __init__(self): self._items: dict[str,Component]={}
    def register(self,name:str,instance:Any,*tags:str)->None:
        if not name or name in self._items: raise ValueError(f"component already registered or invalid: {name}")
        self._items[name]=Component(name,instance,set(tags))
    def get(self,name:str)->Any:
        if name not in self._items: raise KeyError(name)
        return self._items[name].instance
    def names(self)->list[str]: return sorted(self._items)
    def tagged(self,tag:str)->list[str]: return sorted(c.name for c in self._items.values() if tag in c.tags)
