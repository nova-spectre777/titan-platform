# Contributing to TITAN

TITAN is intentionally modular. Pick one subsystem, understand its model and tests, and keep changes focused.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -p 'test_*.py'
```

## Good contribution areas

- Git worktree and container sandboxes for ATLAS/NOVA OS
- provider adapters for ORBIT/OMNIFABRIC/SYNAPSE
- MCP/A2A adapters for NEURALNET
- persistent event/snapshot stores
- Repo/infra visualization for the dashboard
- scenario models and geospatial adapters for WORLDENGINE
- incident parsers and safe remediation executors for HELIOS
- additional deterministic tests and fuzz/property tests

## Rules

- Do not introduce hidden network calls into the core.
- Never auto-execute destructive remediation or restore operations.
- New providers must have a clear adapter boundary.
- Add tests for failure paths, not only happy paths.
- Large architecture changes should start as an issue/RFC.
