from __future__ import annotations
from dataclasses import dataclass, field
import re

@dataclass(slots=True)
class Requirement:
    statement: str
    priority: str = "should"
    source: str = "user"
    tags: set[str] = field(default_factory=set)

@dataclass(slots=True)
class RequirementSet:
    functional: list[Requirement] = field(default_factory=list)
    nonfunctional: list[Requirement] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)

class RequirementExtractor:
    NONFUNCTIONAL = ("secure", "fast", "available", "reliable", "scalable", "private", "offline", "accessible", "latency", "performance")

    def extract(self, text: str) -> RequirementSet:
        sentences = [x.strip(" -\t") for x in re.split(r"[.!?\n]+", text) if x.strip()]
        out = RequirementSet()
        for sentence in sentences:
            lower = sentence.lower()
            priority = "must" if any(x in lower for x in ("must", "required", "need to")) else "should"
            requirement = Requirement(sentence, priority)
            if any(key in lower for key in self.NONFUNCTIONAL):
                out.nonfunctional.append(requirement)
            else:
                out.functional.append(requirement)
        if not sentences:
            out.assumptions.append("No explicit requirements provided")
        return out
