import unittest,time
from titan.orbit.models import Provider,Workload
from titan.orbit.scheduler import OrbitScheduler
from titan.synapse.models import Node,ComputeJob
from titan.synapse.scheduler import SynapseScheduler
from titan.omnifabric.models import BackendNeed,ResourceOption
from titan.omnifabric.planner import OmniFabricPlanner
class InfraTests(unittest.TestCase):
 def test_orbit_place(self):
  ps=[Provider("cheap","us",4,8,hourly_cost=.1,latency_ms=50),Provider("fast","us",8,16,hourly_cost=.2,latency_ms=5)]; self.assertIn(OrbitScheduler().place(Workload("x",preferred_regions=["us"]),ps).provider,{"cheap","fast"})
 def test_orbit_reject(self):
  with self.assertRaises(RuntimeError): OrbitScheduler().place(Workload("x",gpu=1),[Provider("cpu","x",8,8)])
 def test_orbit_budget(self):
  s=OrbitScheduler(); self.assertFalse(s.eligible(Workload("x",max_hourly_cost=.1),Provider("p","x",2,2,hourly_cost=1))[0])
 def test_synapse_schedule(self):
  s=SynapseScheduler(); n=Node("n",8,16,1,{"docker"},.9); s.add_node(n); l=s.schedule(ComputeJob("echo hi",required={"docker"},min_trust=.5)); self.assertEqual(l.node_id,n.id)
 def test_synapse_token(self):
  s=SynapseScheduler(); n=Node("n",8,16); s.add_node(n); l=s.schedule(ComputeJob("x"))
  with self.assertRaises(PermissionError): s.release(l.job_id,"bad")
 def test_synapse_busy(self):
  s=SynapseScheduler(); n=Node("n",8,16); s.add_node(n); s.schedule(ComputeJob("a"))
  with self.assertRaises(RuntimeError): s.schedule(ComputeJob("b"))
 def test_omnifabric(self):
  opts=[ResourceOption("database","local-postgres",{"self-hosted"},0,True),ResourceOption("auth","authx",set(),1)]; p=OmniFabricPlanner().plan(BackendNeed(auth=True,constraints={"self-hosted"}),opts); self.assertIn("database",p.resources); self.assertIn("no provider satisfies auth",p.warnings)
