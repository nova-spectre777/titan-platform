from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
import time, uuid

@dataclass(slots=True, frozen=True)
class Event:
    topic: str
    payload: dict[str, Any]
    source: str="titan"
    id: str=field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: float=field(default_factory=time.time)

class EventBus:
    def __init__(self):
        self._events: list[Event]=[]
        self._subscribers: dict[str,list[Callable[[Event],None]]]={}

    def publish(self, topic: str, payload: dict[str,Any], source: str="titan") -> Event:
        event=Event(topic=topic,payload=dict(payload),source=source)
        self._events.append(event)
        for fn in tuple(self._subscribers.get(topic,())):
            fn(event)
        for fn in tuple(self._subscribers.get("*",())):
            fn(event)
        return event

    def subscribe(self, topic: str, callback: Callable[[Event],None]) -> None:
        self._subscribers.setdefault(topic,[]).append(callback)

    def history(self, topic: str|None=None) -> list[Event]:
        return [e for e in self._events if topic is None or e.topic==topic]
