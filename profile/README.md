<div align="center">

# BlackRoad Security

**Zero-trust security tooling — scanning, detection, identity, and secrets.**

[![Repos](https://img.shields.io/badge/repos-30-black?style=flat-square)](https://github.com/orgs/BlackRoad-Security/repositories)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](https://blackroad.ai)

</div>

---

## 🛡️ What We Build

BlackRoad Security manages the security posture of the entire BlackRoad ecosystem — from container scanning to threat detection to identity management.

---

## 📦 Repositories

### Scanning & SAST
| Repo | Upstream | Purpose |
|------|----------|---------|
| [`blackroad-trivy`](https://github.com/BlackRoad-Security/blackroad-trivy) | aquasecurity/trivy | Container + IaC vulnerability scanner |
| [`blackroad-grype`](https://github.com/BlackRoad-Security/blackroad-grype) | anchore/grype | Dependency vulnerability scanner |
| [`blackroad-semgrep`](https://github.com/BlackRoad-Security/blackroad-semgrep) | returntocorp/semgrep | Static analysis / SAST |
| [`blackroad-terrascan`](https://github.com/BlackRoad-Security/blackroad-terrascan) | accurics/terrascan | IaC security scanner |
| [`blackroad-kube-bench`](https://github.com/BlackRoad-Security/blackroad-kube-bench) | aquasecurity/kube-bench | CIS K8s benchmark |
| [`blackroad-scorecard`](https://github.com/BlackRoad-Security/blackroad-scorecard) | ossf/scorecard | Supply chain security |
| [`blackroad-nuclei`](https://github.com/BlackRoad-Security/blackroad-nuclei) | projectdiscovery/nuclei | Vulnerability scanner |
| [`blackroad-trufflehog`](https://github.com/BlackRoad-Security/blackroad-trufflehog) | trufflesecurity/trufflehog | Secrets scanner |
| [`penetration-testing`](https://github.com/BlackRoad-Security/penetration-testing) | — | Pentest tooling + playbooks |

### Threat Detection & Response
| Repo | Upstream | Purpose |
|------|----------|---------|
| [`blackroad-falco`](https://github.com/BlackRoad-Security/blackroad-falco) | falcosecurity/falco | Runtime threat detection |
| [`blackroad-wazuh`](https://github.com/BlackRoad-Security/blackroad-wazuh) | wazuh/wazuh | SIEM + XDR |
| [`blackroad-crowdsec`](https://github.com/BlackRoad-Security/blackroad-crowdsec) | crowdsecurity/crowdsec | Collaborative IPS |
| [`blackroad-thehive`](https://github.com/BlackRoad-Security/blackroad-thehive) | TheHive-Project/TheHive | Security incident response |
| [`blackroad-velociraptor`](https://github.com/BlackRoad-Security/blackroad-velociraptor) | Velocidex/velociraptor | Digital forensics |
| [`blackroad-osquery`](https://github.com/BlackRoad-Security/blackroad-osquery) | osquery/osquery | OS instrumentation |
| [`blackroad-misp`](https://github.com/BlackRoad-Security/blackroad-misp) | MISP/MISP | Threat intelligence |
| [`blackroad-threatmapper`](https://github.com/BlackRoad-Security/blackroad-threatmapper) | deepfence/ThreatMapper | Cloud-native threat mapping |
| [`blackroad-snort`](https://github.com/BlackRoad-Security/blackroad-snort) | snort3/snort3 | Network IDS |

### WAF & Network
| Repo | Upstream | Purpose |
|------|----------|---------|
| [`blackroad-modsecurity`](https://github.com/BlackRoad-Security/blackroad-modsecurity) | owasp-modsecurity | Web application firewall |
| [`blackroad-zap`](https://github.com/BlackRoad-Security/blackroad-zap) | zaproxy/zaproxy | Web security testing |
| [`blackroad-nmap`](https://github.com/BlackRoad-Security/blackroad-nmap) | nmap/nmap | Network discovery |
| [`blackroad-fail2ban`](https://github.com/BlackRoad-Security/blackroad-fail2ban) | fail2ban/fail2ban | Intrusion prevention |
| [`blackroad-cilium`](https://github.com/BlackRoad-Security/blackroad-cilium) | cilium/cilium | eBPF network security |
| [`blackroad-django-defectdojo`](https://github.com/BlackRoad-Security/blackroad-django-defectdojo) | DefectDojo/django-DefectDojo | Vuln management |

### Identity & Secrets
| Repo | Upstream | Purpose |
|------|----------|---------|
| [`blackroad-keycloak`](https://github.com/BlackRoad-Security/blackroad-keycloak) | keycloak/keycloak | Identity + SSO |
| [`blackroad-authentik`](https://github.com/BlackRoad-Security/blackroad-authentik) | goauthentik/authentik | Open-source IdP |
| [`blackroad-openbao`](https://github.com/BlackRoad-Security/blackroad-openbao) | openbao/openbao | Open-source Vault fork |
| [`blackroad-sops-new`](https://github.com/BlackRoad-Security/blackroad-sops-new) | getsops/sops | Encrypted file secrets |

### Audits
| Repo | Purpose |
|------|---------|
| [`security-audits`](https://github.com/BlackRoad-Security/security-audits) | Audit reports and findings |

---

> Part of [BlackRoad OS](https://github.com/BlackRoad-OS-Inc) — 17 orgs, 1,825+ repos.
> © BlackRoad OS, Inc. All rights reserved.
