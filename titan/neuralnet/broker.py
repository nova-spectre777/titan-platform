from __future__ import annotations
from dataclasses import dataclass, field
from .models import TaskContract, AgentIdentity
from .registry import AgentDirectory

@dataclass(slots=True)
class Assignment:
    contract_id:str; agents:list[str]; explanation:list[str]=field(default_factory=list)

class AgentBroker:
    def __init__(self,directory:AgentDirectory): self.directory=directory
    def route(self,contract:TaskContract)->Assignment:
        agents=self.directory.discover(contract)
        if not agents: raise RuntimeError("no trusted agent satisfies contract")
        return Assignment(contract.id,[a.id for a in agents],[f"{a.name}: trust={a.trust:.2f}" for a in agents])
