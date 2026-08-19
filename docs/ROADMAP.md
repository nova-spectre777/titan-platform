# Roadmap

## v0.1 — Foundation
- domain models for all ten systems
- deterministic planners/schedulers
- top-level TITAN orchestrator
- CLI and optional FastAPI control surface
- offline unit tests
- contributor documentation

## v0.2 — Execution boundaries
- Git worktree workspace manager
- Docker sandbox adapter
- durable SQLite/PostgreSQL state store
- artifact manifests
- explicit approval workflow
- structured logs and traces

## v0.3 — Interoperability
- MCP tool discovery
- A2A-style agent adapter
- provider plugin SDK
- OpenAI/Anthropic/local-model adapters behind GENESIS/NEURALNET boundaries
- cloud provider discovery for ORBIT

## v0.4 — Distributed operation
- authenticated SYNAPSE workers
- lease heartbeats and cancellation
- encrypted node communication
- artifact transfer abstraction
- ORBIT health probes and failover executor

## v0.5 — Control plane
- React/TypeScript dashboard
- live task DAGs
- incident timeline
- infrastructure snapshot diff viewer
- compute/agent topology
- world scenario explorer

## v1.0 target
A stable, extensible platform where an operator can turn an intent into a reviewed software/AI architecture, schedule permitted execution across trusted infrastructure, observe incidents, and restore known-good state without surrendering control to opaque automation.
