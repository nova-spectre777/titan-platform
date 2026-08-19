from dataclasses import dataclass, field
from typing import Any
import hashlib,json,time

@dataclass(slots=True,frozen=True)
class Snapshot:
    name:str; manifest:dict[str,Any]; created_at:float=field(default_factory=time.time); digest:str=""
    def __post_init__(self):
        canonical=json.dumps(self.manifest,sort_keys=True,separators=(",",":"),default=str).encode()
        object.__setattr__(self,"digest",hashlib.sha256(canonical).hexdigest())
@dataclass(slots=True)
class SnapshotDiff:
    added:dict[str,Any]; removed:dict[str,Any]; changed:dict[str,tuple[Any,Any]]
