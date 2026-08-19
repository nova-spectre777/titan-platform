import unittest
from titan.atlas.planner import AtlasPlanner
from titan.atlas.factory import FactoryBoard
from titan.atlas.models import WorkItem,WorkStatus
class AtlasTests(unittest.TestCase):
 def test_spec(self): self.assertIn("authentication",AtlasPlanner().derive_spec("Build an AI analytics service").features)
 def test_short_idea(self):
  with self.assertRaises(ValueError): AtlasPlanner().derive_spec("x")
 def test_graph(self): self.assertGreaterEqual(len(AtlasPlanner().work_graph(AtlasPlanner().derive_spec("Build a useful developer service"))),7)
 def test_plan(self): self.assertEqual(AtlasPlanner().plan("Build a self hosted tracker").kind,"atlas.factory")
 def test_ready(self):
  a=WorkItem("a","x"); b=WorkItem("b","x",[a.id]); board=FactoryBoard([a,b]); self.assertEqual(board.ready()[0].id,a.id); board.complete(a.id); self.assertEqual(board.ready()[0].id,b.id)
 def test_failure_blocks(self):
  a=WorkItem("a","x"); b=WorkItem("b","x",[a.id]); board=FactoryBoard([a,b]); board.complete(a.id,False); board.ready(); self.assertEqual(b.status,WorkStatus.BLOCKED)
 def test_cycle(self):
  a=WorkItem("a","x"); b=WorkItem("b","x",[a.id]); a.depends_on=[b.id]
  with self.assertRaises(ValueError): FactoryBoard([a,b])
