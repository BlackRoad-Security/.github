<div align="center">
  <h1>🛡️ BlackRoad Security</h1>
  <p><strong>Zero trust. Everything verified. Nothing assumed.</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Secrets-AES--256--CBC-FF1D6C?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/Scanning-Trivy%20%7C%20Grype-9C27B0?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/Memory-PS--SHA∞-2979FF?style=for-the-badge"/>
  </p>
</div>

## What Lives Here

Security tooling, secret management, and compliance infrastructure for the BlackRoad platform.

## Security Posture

| Layer | Implementation |
|-------|---------------|
| Secrets | Vault (`~/.blackroad/vault/`) — AES-256-CBC |
| Agent trust | Tokenless — gateway is the only trust boundary |
| Memory | PS-SHA∞ hash-chain journals — tamper-evident |
| Scanning | Trivy + Grype + TruffleHog (all PRs) |
| Runtime | Falco + Wazuh + CrowdSec |
| SSH | Keys must be chmod 600; no password auth |
| Gateway | Binds to 127.0.0.1 by default |

## Key Principle

Agents **never** hold API keys. All provider secrets live exclusively in the tokenless gateway. `verify-tokenless-agents.sh` scans for forbidden strings on every push.

---
*© BlackRoad OS, Inc. All rights reserved.*