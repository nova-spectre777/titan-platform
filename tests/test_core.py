import unittest
from titan.core.models import Plan,Step,Risk,Decision,Health
from titan.core.events import EventBus
from titan.core.policy import PolicyEngine
from titan.core.registry import ComponentRegistry

class CoreTests(unittest.TestCase):
 def test_event_bus(self):
  bus=EventBus(); seen=[]; bus.subscribe("x",lambda e:seen.append(e)); e=bus.publish("x",{"a":1}); self.assertEqual(seen,[e]); self.assertEqual(bus.history("x"),[e])
 def test_policy_allows_safe(self):
  r=PolicyEngine().evaluate(Plan("x","safe",[Step("a","b")],Risk.LOW)); self.assertEqual(r.decision,Decision.ALLOW)
 def test_policy_reviews_destructive(self):
  r=PolicyEngine().evaluate(Plan("x","danger",[Step("a","b",True)],Risk.MEDIUM)); self.assertEqual(r.decision,Decision.REVIEW)
 def test_policy_reviews_high_risk(self): self.assertEqual(PolicyEngine().evaluate(Plan("x","x",risk=Risk.HIGH)).decision,Decision.REVIEW)
 def test_registry(self):
  r=ComponentRegistry(); r.register("x",123,"a"); self.assertEqual(r.get("x"),123); self.assertEqual(r.tagged("a"),["x"])
 def test_registry_duplicate(self):
  r=ComponentRegistry(); r.register("x",1)
  with self.assertRaises(ValueError): r.register("x",2)
 def test_health_clamps(self): self.assertEqual(Health(True,2).score,1)
