import unittest
from titan.novaos.runtime import NovaRuntime
from titan.novaos.models import Workspace,IntentStatus
from titan.orchestrator import Titan
class RuntimeTests(unittest.TestCase):
 def test_intent(self):
  n=NovaRuntime(); i=n.create_intent("Build a tool"); p=n.session_plan(i); self.assertEqual(i.status,IntentStatus.PLANNED); self.assertEqual(p.kind,"nova.session")
 def test_workspace(self):
  n=NovaRuntime(); n.add_workspace(Workspace("x","/tmp/x")); self.assertEqual(n.session_plan(n.create_intent("Build app"),"x").metadata["workspace"],"x")
 def test_missing_workspace(self):
  n=NovaRuntime()
  with self.assertRaises(KeyError): n.session_plan(n.create_intent("Build app"),"missing")
 def test_titan_systems(self):
  t=Titan(); health=t.system_health(); self.assertGreaterEqual(len(health),10); self.assertEqual(health["atlas"],"ready")
 def test_titan_product(self): self.assertEqual(Titan().plan_product("Build a serious developer platform").kind,"atlas.factory")
 def test_titan_demo(self):
  d=Titan().demo(); self.assertEqual(d["policy"]["decision"],"allow"); self.assertGreaterEqual(d["product_plan"]["steps"],7)
 def test_events_created(self):
  t=Titan(); t.plan_product("Build a serious service"); self.assertTrue(t.events.history("plan.created"))
