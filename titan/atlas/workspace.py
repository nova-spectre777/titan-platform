from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
import shutil
@dataclass(slots=True)
class WorkspaceRecord:
    task_id:str; path:str; branch:str|None=None; created:bool=False; metadata:dict=field(default_factory=dict)
class WorkspaceManager:
    """Filesystem-only v0.1 boundary. Git worktree execution is a roadmap adapter."""
    def __init__(self,root:str|Path): self.root=Path(root).resolve(); self.root.mkdir(parents=True,exist_ok=True); self.records={}
    def create(self,task_id:str)->WorkspaceRecord:
        safe="".join(c for c in task_id if c.isalnum() or c in "-_")
        if not safe or safe!=task_id: raise ValueError("unsafe task id")
        path=(self.root/safe).resolve()
        if self.root not in path.parents: raise ValueError("workspace escape")
        path.mkdir(exist_ok=False); rec=WorkspaceRecord(task_id,str(path),created=True); self.records[task_id]=rec; return rec
    def cleanup(self,task_id:str):
        rec=self.records.pop(task_id); path=Path(rec.path).resolve()
        if self.root not in path.parents: raise ValueError("workspace escape")
        shutil.rmtree(path,ignore_errors=False)
