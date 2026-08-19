# Threat Model

Key risks include generated-code escape, prompt/tool injection, malicious worker nodes, credential leakage, unsafe remediation, provider impersonation, poisoned observations, and destructive restore/deploy actions.

The core therefore separates **planning** from **execution**, models trust explicitly, keeps destructive operations behind review gates, and treats remote agents/workers/providers as untrusted until an adapter establishes stronger guarantees.
