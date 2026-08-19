import os,tempfile,unittest
from pathlib import Path
from titan.core.config import TitanConfig
from titan.core.store import JsonStateStore
from titan.core.telemetry import MetricRegistry
from titan.atlas.requirements import RequirementExtractor
from titan.atlas.workspace import WorkspaceManager
from titan.orbit.topology import NetworkTopology,Link
from titan.orbit.health import HealthTracker,Probe
from titan.neuralnet.messages import MessageBus,Envelope
from titan.neuralnet.reputation import ReputationLedger,Outcome
from titan.worldengine.fusion import ObservationFusion
from titan.worldengine.models import Observation,WorldState
from titan.worldengine.rules import RuleEngine,Rule
from titan.synapse.queue import JobQueue
from titan.synapse.models import ComputeJob
from titan.synapse.artifacts import ArtifactStore
from titan.genesis.catalog import ModelCatalog,ModelProfile
from titan.genesis.evaluation import Evaluator,Case
from titan.helios.canary import CanaryGuard,CanaryObservation
from titan.omnifabric.schema import Schema,Entity,Field
from titan.omnifabric.migration import SchemaDiffer
from titan.chronos.timeline import Timeline,TimelineEvent
from titan.chronos.manifest import FileManifest
from titan.novaos.permissions import PermissionMatrix,Principal
from titan.novaos.sessions import SessionManager,SessionState
from titan.novaos.memory import MemoryStore,Memory

class ExtensionTests(unittest.TestCase):
 def test_config_env(self):
  os.environ['TITAN_ALLOW_NETWORK']='true'; self.assertTrue(TitanConfig.from_env().allow_network); del os.environ['TITAN_ALLOW_NETWORK']
 def test_store(self):
  with tempfile.TemporaryDirectory() as d:
   s=JsonStateStore(Path(d)/'x.json');s.put('a','b',{'x':1});self.assertEqual(s.get('a','b')['x'],1);self.assertIsNotNone(s.delete('a','b'))
 def test_metrics(self):
  m=MetricRegistry();[m.record('latency',x,service='api') for x in [1,2,3]];self.assertEqual(m.summary('latency',service='api')['count'],3)
 def test_requirements(self): self.assertTrue(RequirementExtractor().extract('The API must be secure. Users can export reports.').nonfunctional)
 def test_workspace_boundary(self):
  with tempfile.TemporaryDirectory() as d:
   m=WorkspaceManager(d);r=m.create('task_1');self.assertTrue(Path(r.path).exists());m.cleanup('task_1');self.assertFalse(Path(r.path).exists())
 def test_workspace_rejects_escape(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ValueError):WorkspaceManager(d).create('../bad')
 def test_topology(self):
  t=NetworkTopology();t.add(Link('a','b',5,100));t.add(Link('b','c',3,100));self.assertEqual(t.shortest_latency('a','c'),8)
 def test_health(self):
  h=HealthTracker();[h.record(Probe('x',True,10)) for _ in range(5)];self.assertTrue(h.healthy('x'))
 def test_messages_dedupe(self):
  b=MessageBus();e=Envelope('a','b','task',{});self.assertTrue(b.send(e));self.assertFalse(b.send(e));self.assertEqual(len(b.receive('b')),1)
 def test_reputation(self):
  r=ReputationLedger();r.record('a',Outcome(True));self.assertGreater(r.score('a'),.5)
 def test_fusion(self):
  v,c=ObservationFusion().fuse_numeric([Observation('x',10,'a',1),Observation('x',20,'b',.5)]);self.assertGreater(v,10);self.assertLess(v,20)
 def test_rules(self):
  e=RuleEngine([Rule('hot',lambda s:s.values.get('temp',0)>30,{'alert':True})]);s=e.apply(WorldState({'temp':40},{'temp':1}));self.assertTrue(s.values['alert'])
 def test_queue_priority(self):
  q=JobQueue();a=ComputeJob('a');b=ComputeJob('b');q.push(a,1);q.push(b,10);self.assertEqual(q.pop().id,b.id)
 def test_artifacts(self):
  with tempfile.TemporaryDirectory() as d:
   src=Path(d)/'a';src.write_text('x');s=ArtifactStore(Path(d)/'store');a=s.put(src);dst=Path(d)/'out';s.get(a.digest,dst);self.assertEqual(dst.read_text(),'x')
 def test_model_catalog(self):
  c=ModelCatalog([ModelProfile('cheap',{'text'},4096,True,True,cost_rank=1,quality_rank=5)]);self.assertEqual(c.select({'text'},local=True,tools=True).name,'cheap')
 def test_evaluator(self): self.assertEqual(Evaluator().run([Case(1,2)],lambda x:x+1).score,1)
 def test_canary(self):
  b=CanaryObservation(.01,100,.99);c=CanaryObservation(.5,100,.5);self.assertFalse(CanaryGuard().evaluate(b,c).promote)
 def test_schema(self):
  s=Schema();s.add(Entity('user',[Field('id','int')]));self.assertEqual(s.validate_record('user',{}),['missing id'])
 def test_schema_diff(self):
  a=Schema([Entity('u',[Field('id','int')])]);b=Schema([Entity('u',[Field('id','int'),Field('name','text')])]);self.assertEqual(SchemaDiffer().diff(a,b)[0].action,'add_field')
 def test_timeline(self):
  t=Timeline();t.add(TimelineEvent('deploy','me','api'));self.assertEqual(len(t.subject('api')),1)
 def test_manifest(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'a').write_text('x');self.assertIn('a',FileManifest().build(d))
 def test_permissions(self):
  p=PermissionMatrix();p.grant_role('dev','workspace.write');self.assertTrue(p.allowed(Principal('x',{'dev'}),'workspace.write'))
 def test_sessions(self):
  m=SessionManager();s=m.create('i');m.activate(s.id);self.assertEqual(s.state,SessionState.ACTIVE);m.close(s.id);self.assertEqual(s.state,SessionState.CLOSED)
 def test_memory(self):
  m=MemoryStore();m.remember(Memory('arch','use adapters',tags={'design'}));self.assertEqual(m.search('adapter')[0].key,'arch')
