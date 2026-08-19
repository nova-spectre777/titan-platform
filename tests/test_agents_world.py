import unittest
from titan.neuralnet.models import AgentIdentity,TaskContract
from titan.neuralnet.registry import AgentDirectory
from titan.neuralnet.broker import AgentBroker
from titan.worldengine.models import Observation,Scenario
from titan.worldengine.engine import WorldEngine
class AgentWorldTests(unittest.TestCase):
 def test_discovery(self):
  d=AgentDirectory(); a=AgentIdentity("coder",{"python","git"},.9); d.register(a); self.assertEqual(d.discover(TaskContract("fix",{"python"}))[0].id,a.id)
 def test_trust_filter(self):
  d=AgentDirectory(); d.register(AgentIdentity("x",{"python"},.2)); self.assertEqual(d.discover(TaskContract("x",{"python"},minimum_trust=.8)),[])
 def test_broker_no_agent(self):
  with self.assertRaises(RuntimeError): AgentBroker(AgentDirectory()).route(TaskContract("x",{"missing"}))
 def test_world_ingest(self):
  e=WorldEngine(); e.ingest(Observation("temp",25,"sensor",.9)); self.assertEqual(e.state.values["temp"],25)
 def test_world_confidence_wins(self):
  e=WorldEngine(); e.ingest(Observation("x",1,"a",.9)); e.ingest(Observation("x",2,"b",.2)); self.assertEqual(e.state.values["x"],1)
 def test_world_scenario(self):
  e=WorldEngine(); e.ingest(Observation("port_open",True,"feed")); s=e.fork(Scenario("closure",{"port_open":False})); self.assertEqual(e.compare(e.state,s)["port_open"],(True,False))
 def test_bad_confidence(self):
  e=WorldEngine()
  with self.assertRaises(ValueError): e.ingest(Observation("x",1,"x",2))
