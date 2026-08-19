from __future__ import annotations
from dataclasses import dataclass,field
import time, statistics

@dataclass(slots=True)
class MetricPoint:
    name:str; value:float; labels:dict[str,str]=field(default_factory=dict); timestamp:float=field(default_factory=time.time)

class MetricRegistry:
    def __init__(self,max_points:int=10000): self.max_points=max_points; self.points:list[MetricPoint]=[]
    def record(self,name:str,value:float,**labels):
        self.points.append(MetricPoint(name,float(value),labels))
        if len(self.points)>self.max_points: del self.points[:len(self.points)-self.max_points]
    def query(self,name:str,**labels):
        return [p for p in self.points if p.name==name and all(p.labels.get(k)==v for k,v in labels.items())]
    def summary(self,name:str,**labels):
        vals=[p.value for p in self.query(name,**labels)]
        if not vals: return {"count":0}
        ordered=sorted(vals); p95=ordered[min(len(ordered)-1,int(.95*(len(ordered)-1)))]
        return {"count":len(vals),"min":min(vals),"max":max(vals),"mean":statistics.fmean(vals),"p95":p95}
