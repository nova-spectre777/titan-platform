from __future__ import annotations
from collections import defaultdict
from .models import Observation
class ObservationFusion:
    def fuse_numeric(self,observations:list[Observation]):
        numeric=[o for o in observations if isinstance(o.value,(int,float)) and not isinstance(o.value,bool)]
        if not numeric: raise ValueError("no numeric observations")
        total=sum(max(0,o.confidence) for o in numeric)
        if total==0: raise ValueError("zero total confidence")
        value=sum(float(o.value)*o.confidence for o in numeric)/total
        confidence=min(1.0,total/max(1,len(numeric)))
        return value,confidence
    def conflicts(self,observations:list[Observation],tolerance:float=.2):
        by=defaultdict(list)
        for o in observations: by[o.key].append(o)
        out={}
        for k,xs in by.items():
            vals={str(x.value) for x in xs if x.confidence>=tolerance}
            if len(vals)>1: out[k]=xs
        return out
