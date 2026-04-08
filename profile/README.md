# BlackRoad-Security

> *Sovereign identity. Zero trust.*

15 repositories. Zero-trust authentication, encryption infrastructure, SIEM, secret scanning, and sovereign credential management.

## What Lives Here
- **CarKeys** — Sovereign credential vault → [carkeys.blackroad.io](https://carkeys.blackroad.io)
- **RoadChain** — Immutable identity ledger → [roadchain.blackroad.io](https://roadchain.blackroad.io)
- **Auth layer** — JWT, OAuth, fine-grained PATs
- **Secret scanner** — Prevents credentials in repos
- **Audit logs** — Every agent action logged and signed
- **Zero-trust policies** — No implicit trust, verify everything

## Security Rules
1. Never commit secrets — rotate every 90 days
2. Fine-grained PATs, not classic tokens
3. Enable 2FA on all accounts
4. Dependabot alerts on all repos

---
*Part of [BlackRoad OS, Inc.](https://os.blackroad.io) — Remember the Road. Pave Tomorrow.* 🖤🛣️
