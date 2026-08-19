from dataclasses import dataclass, field
from typing import Any
import time

@dataclass(slots=True,frozen=True)
class Observation:
    key:str; value:float|str|bool; source:str; confidence:float=1.0; timestamp:float=field(default_factory=time.time)

@dataclass(slots=True)
class WorldState:
    values:dict[str,Any]=field(default_factory=dict); confidence:dict[str,float]=field(default_factory=dict); updated_at:float=field(default_factory=time.time)

@dataclass(slots=True)
class Scenario:
    name:str; changes:dict[str,float|str|bool]
