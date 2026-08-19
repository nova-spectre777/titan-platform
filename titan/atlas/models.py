from dataclasses import dataclass, field
from enum import Enum
import uuid

class WorkStatus(str,Enum):
    PENDING="pending"; READY="ready"; RUNNING="running"; DONE="done"; FAILED="failed"; BLOCKED="blocked"

@dataclass(slots=True)
class ProductSpec:
    name: str
    goal: str
    users: list[str]=field(default_factory=list)
    constraints: list[str]=field(default_factory=list)
    features: list[str]=field(default_factory=list)

@dataclass(slots=True)
class WorkItem:
    title: str
    discipline: str
    depends_on: list[str]=field(default_factory=list)
    id: str=field(default_factory=lambda: uuid.uuid4().hex[:8])
    status: WorkStatus=WorkStatus.PENDING
    acceptance: list[str]=field(default_factory=list)
