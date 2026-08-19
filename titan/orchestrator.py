from __future__ import annotations
from dataclasses import asdict
from titan.core.events import EventBus
from titan.core.policy import PolicyEngine
from titan.core.registry import ComponentRegistry
from titan.core.models import Plan, Decision
from titan.atlas.planner import AtlasPlanner
from titan.genesis.planner import GenesisPlanner
from titan.genesis.models import AIRequirement
from titan.helios.engine import Helios
from titan.orbit.scheduler import OrbitScheduler
from titan.neuralnet.registry import AgentDirectory
from titan.neuralnet.broker import AgentBroker
from titan.synapse.scheduler import SynapseScheduler
from titan.omnifabric.planner import OmniFabricPlanner
from titan.chronos.store import ChronosStore
from titan.worldengine.engine import WorldEngine
from titan.novaos.runtime import NovaRuntime

class Titan:
    def __init__(self):
        self.events=EventBus(); self.policy=PolicyEngine(); self.registry=ComponentRegistry()
        systems={
            "atlas":AtlasPlanner(),"orbit":OrbitScheduler(),"neuralnet":AgentDirectory(),"worldengine":WorldEngine(),
            "synapse":SynapseScheduler(),"genesis":GenesisPlanner(),"helios":Helios(),"omnifabric":OmniFabricPlanner(),
            "chronos":ChronosStore(),"novaos":NovaRuntime(),
        }
        systems["agent_broker"]=AgentBroker(systems["neuralnet"])
        for name,obj in systems.items(): self.registry.register(name,obj,"system")
        self.events.publish("titan.started",{"systems":self.registry.tagged("system")})

    def plan_product(self,idea:str)->Plan:
        plan=self.registry.get("atlas").plan(idea)
        self.events.publish("plan.created",{"id":plan.id,"kind":plan.kind},"atlas")
        return plan

    def plan_ai(self,task:str,**kwargs):
        blueprint=self.registry.get("genesis").design(AIRequirement(task=task,**kwargs))
        self.events.publish("blueprint.created",{"task":task},"genesis")
        return blueprint

    def review(self,plan:Plan):
        result=self.policy.evaluate(plan)
        self.events.publish("policy.decision",{"plan":plan.id,"decision":result.decision.value,"reason":result.reason},"policy")
        return result

    def system_health(self)->dict:
        return {name:"ready" for name in self.registry.names() if name!="agent_broker"}

    def demo(self)->dict:
        product=self.plan_product("Build a self-hosted project tracker with AI search and analytics")
        ai=self.plan_ai("Answer questions over project documents",needs_retrieval=True,needs_tools=True)
        review=self.review(product)
        return {"systems":self.system_health(),"product_plan":{"id":product.id,"steps":len(product.steps),"risk":product.risk.value},"ai_blueprint":asdict(ai),"policy":{"decision":review.decision.value,"reason":review.reason},"events":len(self.events.history())}
