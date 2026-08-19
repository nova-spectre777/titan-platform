from __future__ import annotations
import argparse,json
from dataclasses import asdict,is_dataclass
from .orchestrator import Titan

def dump(x):
    if is_dataclass(x): x=asdict(x)
    return json.dumps(x,indent=2,default=lambda o:getattr(o,"value",str(o)))

def main(argv=None):
    p=argparse.ArgumentParser(prog="titan",description="TITAN autonomous systems platform")
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("demo")
    plan=sub.add_parser("plan"); plan.add_argument("idea")
    ai=sub.add_parser("ai-plan"); ai.add_argument("task"); ai.add_argument("--retrieval",action="store_true"); ai.add_argument("--tools",action="store_true")
    sub.add_parser("health")
    args=p.parse_args(argv); t=Titan()
    if args.cmd=="demo": print(dump(t.demo()))
    elif args.cmd=="plan":
        x=t.plan_product(args.idea); print(dump({"plan":asdict(x),"policy":asdict(t.review(x))}))
    elif args.cmd=="ai-plan": print(dump(t.plan_ai(args.task,needs_retrieval=args.retrieval,needs_tools=args.tools)))
    elif args.cmd=="health": print(dump(t.system_health()))

if __name__=="__main__": main()
