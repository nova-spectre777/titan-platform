import unittest
from titan.genesis.planner import GenesisPlanner
from titan.genesis.models import AIRequirement
from titan.helios.engine import Helios
from titan.helios.models import Incident,Severity
from titan.chronos.models import Snapshot
from titan.chronos.store import ChronosStore
from titan.core.models import Decision
from titan.core.policy import PolicyEngine
class SystemsTests(unittest.TestCase):
 def test_genesis_retrieval(self): self.assertIsNotNone(GenesisPlanner().design(AIRequirement("qa",needs_retrieval=True)).retrieval)
 def test_genesis_private(self): self.assertIn("local",GenesisPlanner().design(AIRequirement("qa",privacy="strict")).model_strategy)
 def test_genesis_invalid(self):
  with self.assertRaises(ValueError): GenesisPlanner().design(AIRequirement(""))
 def test_helios_memory(self): self.assertEqual(Helios().diagnose(Incident("api","memory high",{"memory_pct":98})).likely_causes[0][0],"memory pressure")
 def test_helios_plan_needs_review(self):
  h=Helios(); i=Incident("api","memory high",{"memory_pct":98},Severity.HIGH); p=h.remediate(i,h.diagnose(i)); self.assertEqual(PolicyEngine().evaluate(p).decision,Decision.REVIEW)
 def test_snapshot_digest_stable(self): self.assertEqual(Snapshot("a",{"x":1,"y":2}).digest,Snapshot("b",{"y":2,"x":1}).digest)
 def test_snapshot_diff(self):
  s=ChronosStore(); d=s.diff(Snapshot("a",{"x":1}),Snapshot("b",{"x":2,"y":3})); self.assertEqual(d.changed["x"],(1,2)); self.assertEqual(d.added["y"],3)
 def test_restore_destructive(self): self.assertTrue(ChronosStore().restore_plan(Snapshot("a",{"x":1}),Snapshot("b",{"x":2})).destructive)
