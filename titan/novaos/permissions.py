from __future__ import annotations
from dataclasses import dataclass,field
@dataclass(slots=True)
class Principal:
    name:str; roles:set[str]=field(default_factory=set)
class PermissionMatrix:
    def __init__(self): self.role_permissions:dict[str,set[str]]={}
    def grant_role(self,role:str,*permissions:str): self.role_permissions.setdefault(role,set()).update(permissions)
    def allowed(self,principal:Principal,permission:str): return any(permission in self.role_permissions.get(r,set()) or '*' in self.role_permissions.get(r,set()) for r in principal.roles)
    def require(self,principal:Principal,permission:str):
        if not self.allowed(principal,permission): raise PermissionError(f"{principal.name} lacks {permission}")
