from __future__ import annotations
from pathlib import Path
import hashlib
class FileManifest:
    def build(self,root:str|Path,ignore:tuple[str,...]=('.git','.titan','__pycache__')):
        root=Path(root).resolve(); out={}
        for p in sorted(root.rglob('*')):
            if not p.is_file():continue
            rel=p.relative_to(root).as_posix()
            if any(part in ignore for part in p.relative_to(root).parts):continue
            data=p.read_bytes(); out[rel]={"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)}
        return out
    def changed(self,a:dict,b:dict):
        keys=a.keys()|b.keys(); return {k:(a.get(k),b.get(k)) for k in keys if a.get(k)!=b.get(k)}
