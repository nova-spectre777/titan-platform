<div align="center">

# TITAN

### Autonomous Systems Platform

**A modular control plane for building, deploying, operating, healing, versioning, and coordinating software systems.**

</div>

TITAN is an experimental open-source platform that connects ten ambitious infrastructure projects behind one coherent runtime. It is intentionally designed as a collection of real subsystems with explicit models and boundaries instead of a folder full of branded wrappers.

> **Status:** v0.1 foundation. The goal is to provide runnable architecture, deterministic planners, schedulers, state models, safety boundaries, tests, and extension points. It does **not** claim to be a finished production replacement for cloud platforms, operating systems, or mature agent frameworks.

## Systems

| System | Mission |
|---|---|
| **ATLAS** | Autonomous software factory: idea → spec → architecture → work graph → verification |
| **ORBIT** | Cloud operating layer: workload placement, cost scoring, health and failover planning |
| **NEURALNET** | Agent discovery network: identities, capabilities, trust, contracts and routing |
| **WORLDENGINE** | Digital-twin primitives: observations, world state, scenarios and simulation |
| **SYNAPSE** | Distributed compute fabric: nodes, leases, capability matching and scheduling |
| **GENESIS** | AI-system architect: workload requirements → model/data/retrieval/evaluation blueprint |
| **HELIOS** | Self-healing runtime: incidents → diagnosis → remediation plan → guarded recovery |
| **OMNIFABRIC** | Universal backend planner: database/auth/storage/queue/search/AI resource abstraction |
| **CHRONOS** | Infrastructure history: immutable snapshots, diffs, manifests and restore planning |
| **NOVA OS** | AI-native workspace runtime: intents, workspaces, permissions and task sessions |
| **TITAN CORE** | Cross-system orchestration, event bus, policy gates and lifecycle coordination |

## Architecture

```text
                             HUMAN INTENT
                                  │
                                  ▼
                              NOVA OS
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
                 ATLAS                      GENESIS
              software plan                AI blueprint
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                              TITAN CORE
             ┌────────────────────┼────────────────────┐
             ▼                    ▼                    ▼
           ORBIT               SYNAPSE             NEURALNET
        cloud/runtime       compute fabric        agent network
             │                    │                    │
             └──────────────┬─────┴─────┬──────────────┘
                            ▼           ▼
                      OMNIFABRIC    WORLDENGINE
                            │           │
                            └─────┬─────┘
                                  ▼
                                HELIOS
                           detect / recover
                                  │
                                  ▼
                               CHRONOS
                         snapshot / diff / restore
```

## Quick start

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -e .
titan demo
titan plan "Build a self-hosted project tracker with AI search"
titan health
```

Run the tests:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Design principles

1. **Local-first.** The core does not require a paid API or cloud account.
2. **Deterministic before magical.** Planners and schedulers expose their scoring and decisions.
3. **Adapters over lock-in.** Provider-specific behavior belongs behind interfaces.
4. **Human approval for destructive actions.** Healing, deployment, and restoration are plans unless explicitly approved.
5. **State is inspectable.** Tasks, incidents, leases, snapshots, contracts, and events are explicit data models.
6. **One subsystem can be useful alone.** TITAN should not require the entire platform to use ATLAS, CHRONOS, SYNAPSE, etc.
7. **Tests without external services.** The default suite is offline and deterministic.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md). The next milestones focus on Git worktree sandboxes, Docker execution, persistence, MCP/A2A adapters, real provider plugins, graph visualization, and a proper web control plane.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Architecture proposals and focused PRs are preferred over huge unreviewable rewrites.
