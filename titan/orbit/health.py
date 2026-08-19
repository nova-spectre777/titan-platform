from __future__ import annotations
from dataclasses import dataclass, field
import time

@dataclass(slots=True)
class Probe:
    target: str
    ok: bool
    latency_ms: float
    timestamp: float = field(default_factory=time.time)
    detail: str = ""

class HealthTracker:
    def __init__(self, window: int = 20):
        if window < 1:
            raise ValueError("window must be positive")
        self.window = window
        self.probes: dict[str, list[Probe]] = {}

    def record(self, probe: Probe) -> None:
        points = self.probes.setdefault(probe.target, [])
        points.append(probe)
        if len(points) > self.window:
            del points[:-self.window]

    def score(self, target: str) -> float:
        points = self.probes.get(target, [])
        if not points:
            return 0.0
        availability = sum(1 for p in points if p.ok) / len(points)
        average_latency = sum(p.latency_ms for p in points) / len(points)
        latency_factor = max(0.1, 1 - min(average_latency, 5000) / 5000)
        return round(availability * 0.8 + latency_factor * 0.2, 4)

    def healthy(self, target: str, threshold: float = 0.7) -> bool:
        return self.score(target) >= threshold
