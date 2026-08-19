from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(slots=True)
class ModelProfile:
    name:str; modalities:set[str]; context:int; local:bool=False; tool_use:bool=False; structured:bool=False; cost_rank:int=5; quality_rank:int=5
class ModelCatalog:
    def __init__(self,models:list[ModelProfile]|None=None): self.models=models or []
    def add(self,m:ModelProfile): self.models.append(m)
    def select(self,modalities:set[str],local:bool=False,tools:bool=False,max_cost_rank:int=10):
        xs=[m for m in self.models if modalities.issubset(m.modalities) and (not local or m.local) and (not tools or m.tool_use) and m.cost_rank<=max_cost_rank]
        if not xs: raise RuntimeError("no model profile satisfies requirements")
        return sorted(xs,key=lambda m:(-m.quality_rank,m.cost_rank,-m.context))[0]
