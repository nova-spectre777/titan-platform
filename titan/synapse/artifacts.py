from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
import hashlib,shutil
@dataclass(slots=True,frozen=True)
class Artifact:
    name:str; digest:str; size:int; path:str
class ArtifactStore:
    def __init__(self,root:str|Path): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def put(self,path:str|Path,name:str|None=None):
        src=Path(path); data=src.read_bytes(); digest=hashlib.sha256(data).hexdigest(); dst=self.root/digest; dst.write_bytes(data); return Artifact(name or src.name,digest,len(data),str(dst))
    def get(self,digest:str,destination:str|Path):
        src=self.root/digest
        if not src.exists(): raise KeyError(digest)
        shutil.copy2(src,destination); return Path(destination)
