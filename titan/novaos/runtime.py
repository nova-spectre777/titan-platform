from __future__ import annotations
from .models import Intent,IntentStatus,Workspace
from titan.core.models import Plan,Step,Risk

class NovaRuntime:
    def __init__(self): self.intents:dict[str,Intent]={}; self.workspaces:dict[str,Workspace]={}
    def create_intent(self,text:str,owner:str="local-user")->Intent:
        if len(text.strip())<4: raise ValueError("intent too short")
        i=Intent(text.strip(),owner); self.intents[i.id]=i; return i
    def add_workspace(self,w:Workspace):
        if not w.root: raise ValueError("workspace root required")
        self.workspaces[w.name]=w
    def session_plan(self,intent:Intent,workspace:str|None=None)->Plan:
        if workspace and workspace not in self.workspaces: raise KeyError(workspace)
        intent.status=IntentStatus.PLANNED
        return Plan("nova.session",f"Execute intent: {intent.text}",[Step("Understand intent","derive requirements and constraints"),Step("Select systems","choose TITAN subsystems"),Step("Request execution","run only approved actions")],Risk.MEDIUM,metadata={"intent":intent.id,"workspace":workspace})
