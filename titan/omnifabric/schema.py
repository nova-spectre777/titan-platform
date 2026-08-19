from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(slots=True)
class Field:
    name:str; type:str; required:bool=True; unique:bool=False; default:object=None
@dataclass(slots=True)
class Entity:
    name:str; fields:list[Field]=field(default_factory=list)
class Schema:
    def __init__(self,entities:list[Entity]|None=None): self.entities={e.name:e for e in entities or []}
    def add(self,e:Entity):
        if e.name in self.entities: raise ValueError("duplicate entity")
        names=[f.name for f in e.fields]
        if len(names)!=len(set(names)): raise ValueError("duplicate field")
        self.entities[e.name]=e
    def validate_record(self,entity:str,record:dict):
        e=self.entities[entity]; errors=[]
        for f in e.fields:
            if f.required and f.name not in record and f.default is None:errors.append(f"missing {f.name}")
        known={f.name for f in e.fields}; errors += [f"unknown {k}" for k in record if k not in known]
        return errors
