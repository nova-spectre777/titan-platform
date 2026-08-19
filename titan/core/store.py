from __future__ import annotations
from dataclasses import asdict,is_dataclass
from pathlib import Path
from typing import Any
import json, threading

class JsonStateStore:
    """Tiny durable store for local development; production adapters can replace it."""
    def __init__(self,path:str|Path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True); self._lock=threading.RLock()
        if not self.path.exists(): self.path.write_text("{}",encoding="utf-8")
    def _read(self):
        with self._lock:
            try: return json.loads(self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e: raise RuntimeError(f"corrupt state store: {self.path}") from e
    def _write(self,data):
        tmp=self.path.with_suffix(self.path.suffix+".tmp"); tmp.write_text(json.dumps(data,indent=2,sort_keys=True,default=str),encoding="utf-8"); tmp.replace(self.path)
    def put(self,namespace:str,key:str,value:Any):
        data=self._read(); data.setdefault(namespace,{})[key]=asdict(value) if is_dataclass(value) else value; self._write(data)
    def get(self,namespace:str,key:str,default=None): return self._read().get(namespace,{}).get(key,default)
    def delete(self,namespace:str,key:str):
        data=self._read(); removed=data.get(namespace,{}).pop(key,None); self._write(data); return removed
    def list(self,namespace:str): return dict(self._read().get(namespace,{}))
