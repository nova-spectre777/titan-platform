from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import json, os

@dataclass(slots=True)
class TitanConfig:
    state_dir: str=".titan"
    environment: str="local"
    allow_network: bool=False
    allow_destructive: bool=False
    log_level: str="INFO"
    labels: dict[str,str]=field(default_factory=dict)

    @classmethod
    def from_env(cls,prefix:str="TITAN_"):
        return cls(
            state_dir=os.getenv(prefix+"STATE_DIR",".titan"),
            environment=os.getenv(prefix+"ENVIRONMENT","local"),
            allow_network=os.getenv(prefix+"ALLOW_NETWORK","0").lower() in {"1","true","yes"},
            allow_destructive=os.getenv(prefix+"ALLOW_DESTRUCTIVE","0").lower() in {"1","true","yes"},
            log_level=os.getenv(prefix+"LOG_LEVEL","INFO").upper(),
        )

    @classmethod
    def load(cls,path:str|Path):
        data=json.loads(Path(path).read_text(encoding="utf-8")); return cls(**data)

    def save(self,path:str|Path):
        Path(path).write_text(json.dumps({"state_dir":self.state_dir,"environment":self.environment,"allow_network":self.allow_network,"allow_destructive":self.allow_destructive,"log_level":self.log_level,"labels":self.labels},indent=2),encoding="utf-8")
