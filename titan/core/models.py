from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
import time, uuid

class Risk(str, Enum):
    LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"

class Decision(str, Enum):
    ALLOW="allow"; DENY="deny"; REVIEW="review"

@dataclass(slots=True)
class Step:
    name: str
    action: str
    destructive: bool=False
    metadata: dict[str, Any]=field(default_factory=dict)

@dataclass(slots=True)
class Plan:
    kind: str
    summary: str
    steps: list[Step]=field(default_factory=list)
    risk: Risk=Risk.LOW
    id: str=field(default_factory=lambda: uuid.uuid4().hex[:12])
    created_at: float=field(default_factory=time.time)
    metadata: dict[str, Any]=field(default_factory=dict)

    @property
    def destructive(self) -> bool:
        return any(s.destructive for s in self.steps)

@dataclass(slots=True, frozen=True)
class Capability:
    name: str
    version: str="1"
    attributes: tuple[tuple[str,str], ...]=()

@dataclass(slots=True)
class Health:
    healthy: bool
    score: float
    reasons: list[str]=field(default_factory=list)

    def __post_init__(self):
        self.score=max(0.0,min(1.0,float(self.score)))
