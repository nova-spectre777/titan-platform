# TITAN Architecture

TITAN uses explicit domain objects and small engines. Cross-subsystem communication occurs through typed events and plans rather than direct hidden side effects.

## Shared concepts

- **Plan**: an inspectable proposed action with steps, risk and metadata.
- **Event**: immutable notification recorded by the in-memory event bus.
- **Policy decision**: allow/deny/review outcome for an action.
- **Capability**: normalized feature used for agent/compute/provider matching.
- **Snapshot**: immutable state manifest managed by CHRONOS.

The top-level orchestrator coordinates systems but does not absorb their business logic. Each subsystem can be imported and tested independently.
