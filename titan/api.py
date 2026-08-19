"""Optional FastAPI control surface. Install with `pip install -e .[api]`."""
from __future__ import annotations
from dataclasses import asdict
from .orchestrator import Titan

def create_app():
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
    except ImportError as exc:
        raise RuntimeError("FastAPI extra not installed; use pip install -e '.[api]'") from exc
    app=FastAPI(title="TITAN Control Plane",version="0.1.0")
    titan=Titan()
    class Idea(BaseModel): idea:str
    class AITask(BaseModel): task:str; needs_retrieval:bool=False; needs_tools:bool=False
    @app.get("/health")
    def health(): return {"status":"ok","systems":titan.system_health()}
    @app.post("/atlas/plan")
    def atlas(body:Idea):
        try:
            p=titan.plan_product(body.idea); return {"plan":asdict(p),"policy":asdict(titan.review(p))}
        except ValueError as e: raise HTTPException(400,str(e))
    @app.post("/genesis/plan")
    def genesis(body:AITask): return asdict(titan.plan_ai(body.task,needs_retrieval=body.needs_retrieval,needs_tools=body.needs_tools))
    @app.get("/events")
    def events(): return [asdict(e) for e in titan.events.history()]
    return app

try: app=create_app()
except RuntimeError: app=None
