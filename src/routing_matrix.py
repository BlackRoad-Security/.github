"""
BlackRoad OS Routing Matrix.

Manages organization routing, domain registry, and task distribution
across the BlackRoad enterprise ecosystem (15 organizations, 18+ domains).
"""

import json
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, List, Optional


class OrganizationDomain(Enum):
    """Functional domains for the 15 BlackRoad organizations."""
    CORPORATE = "corporate"
    AI = "ai"
    ARCHIVE = "archive"
    CLOUD = "cloud"
    EDUCATION = "education"
    FOUNDATION = "foundation"
    GOV = "gov"
    HARDWARE = "hardware"
    INTERACTIVE = "interactive"
    LABS = "labs"
    MEDIA = "media"
    OS = "os"
    SECURITY = "security"
    STUDIO = "studio"
    VENTURES = "ventures"


@dataclass
class Organization:
    """A BlackRoad GitHub organization."""
    name: str
    domain: OrganizationDomain
    responsibility: str
    repositories: List[str] = field(default_factory=list)


@dataclass
class DomainEntry:
    """A registered domain in the BlackRoad infrastructure."""
    domain: str
    use_case: str
    organization: str


@dataclass
class RouteDecision:
    """Result of routing a task through the matrix."""
    organization: str
    domain: OrganizationDomain
    confidence: float
    reasoning: str


# Organization registry — the 15 BlackRoad organizations
ORGANIZATIONS: Dict[str, Organization] = {
    "Blackbox-Enterprises": Organization(
        name="Blackbox-Enterprises",
        domain=OrganizationDomain.CORPORATE,
        responsibility="Corporate and Enterprise Integrations",
        repositories=["blackbox-api", "enterprise-bridge"],
    ),
    "BlackRoad-AI": Organization(
        name="BlackRoad-AI",
        domain=OrganizationDomain.AI,
        responsibility="Core LLM and Reasoning Engine Development",
        repositories=["lucidia-core", "blackroad-reasoning"],
    ),
    "BlackRoad-Archive": Organization(
        name="BlackRoad-Archive",
        domain=OrganizationDomain.ARCHIVE,
        responsibility="Long-term Data Persistence and Documentation",
        repositories=["blackroad-os-docs", "history-ledger"],
    ),
    "BlackRoad-Cloud": Organization(
        name="BlackRoad-Cloud",
        domain=OrganizationDomain.CLOUD,
        responsibility="Infrastructure as Code and Orchestration",
        repositories=["cloud-orchestrator", "railway-deploy"],
    ),
    "BlackRoad-Education": Organization(
        name="BlackRoad-Education",
        domain=OrganizationDomain.EDUCATION,
        responsibility="Onboarding and Documentation Frameworks",
        repositories=["br-help", "onboarding-portal"],
    ),
    "BlackRoad-Foundation": Organization(
        name="BlackRoad-Foundation",
        domain=OrganizationDomain.FOUNDATION,
        responsibility="Governance and Protocol Standards",
        repositories=["protocol-specs", "governance-rules"],
    ),
    "BlackRoad-Gov": Organization(
        name="BlackRoad-Gov",
        domain=OrganizationDomain.GOV,
        responsibility="Regulatory Compliance and Policy Enforcement",
        repositories=["compliance-audit", "regulatory-tools"],
    ),
    "BlackRoad-Hardware": Organization(
        name="BlackRoad-Hardware",
        domain=OrganizationDomain.HARDWARE,
        responsibility="SBC and IoT Device Management",
        repositories=["blackroad-agent-os", "pi-firmware"],
    ),
    "BlackRoad-Interactive": Organization(
        name="BlackRoad-Interactive",
        domain=OrganizationDomain.INTERACTIVE,
        responsibility="User Interface and Frontend Systems",
        repositories=["blackroad-os-web", "interactive-ui"],
    ),
    "BlackRoad-Labs": Organization(
        name="BlackRoad-Labs",
        domain=OrganizationDomain.LABS,
        responsibility="Experimental R&D and Prototyping",
        repositories=["experimental-agents", "quantum-lab"],
    ),
    "BlackRoad-Media": Organization(
        name="BlackRoad-Media",
        domain=OrganizationDomain.MEDIA,
        responsibility="Content Delivery and Public Relations",
        repositories=["media-engine", "pr-automation"],
    ),
    "BlackRoad-OS": Organization(
        name="BlackRoad-OS",
        domain=OrganizationDomain.OS,
        responsibility="Core System Kernel and CLI Development",
        repositories=["blackroad-cli", "kernel-source"],
    ),
    "BlackRoad-Security": Organization(
        name="BlackRoad-Security",
        domain=OrganizationDomain.SECURITY,
        responsibility="Auditing, Cryptography, and Security",
        repositories=["security-audit", "hash-witnessing"],
    ),
    "BlackRoad-Studio": Organization(
        name="BlackRoad-Studio",
        domain=OrganizationDomain.STUDIO,
        responsibility="Production Assets and Creative Tooling",
        repositories=["lucidia-studio", "creative-assets"],
    ),
    "BlackRoad-Ventures": Organization(
        name="BlackRoad-Ventures",
        domain=OrganizationDomain.VENTURES,
        responsibility="Strategic Growth and Ecosystem Funding",
        repositories=["tokenomics-api", "venture-cap"],
    ),
}

# Domain registry — primary domains managed via Cloudflare
DOMAIN_REGISTRY: List[DomainEntry] = [
    DomainEntry("blackboxprogramming.io", "Developer Education and APIs", "Blackbox-Enterprises"),
    DomainEntry("blackroad.io", "Core Project Landing Page", "BlackRoad-OS"),
    DomainEntry("blackroad.company", "Corporate and HR Operations", "BlackRoad-Ventures"),
    DomainEntry("blackroad.me", "Personal Agent Identity Nodes", "BlackRoad-AI"),
    DomainEntry("blackroad.network", "Distributed Network Interface", "BlackRoad-Cloud"),
    DomainEntry("blackroad.systems", "Infrastructure and System Ops", "BlackRoad-Cloud"),
    DomainEntry("blackroadai.com", "AI Research and API Hosting", "BlackRoad-AI"),
    DomainEntry("blackroadinc.us", "US-based Governance and Legal", "BlackRoad-Gov"),
    DomainEntry("blackroadqi.com", "Quantum Intelligence Research", "BlackRoad-Labs"),
    DomainEntry("blackroadquantum.com", "Primary Quantum Lab Interface", "BlackRoad-Labs"),
    DomainEntry("lucidia.earth", "Memory Layer and Personal AI", "BlackRoad-AI"),
    DomainEntry("lucidia.studio", "Creative and Asset Management", "BlackRoad-Studio"),
    DomainEntry("roadchain.io", "Blockchain and Witnessing Ledger", "BlackRoad-Security"),
    DomainEntry("roadcoin.io", "Tokenomics and Financial Interface", "BlackRoad-Ventures"),
]

# Keyword-to-domain mapping for intent-based routing
_ROUTING_KEYWORDS: Dict[str, OrganizationDomain] = {
    # Security
    "security": OrganizationDomain.SECURITY,
    "audit": OrganizationDomain.SECURITY,
    "vulnerability": OrganizationDomain.SECURITY,
    "cryptography": OrganizationDomain.SECURITY,
    "hash": OrganizationDomain.SECURITY,
    "roadchain": OrganizationDomain.SECURITY,
    # AI
    "llm": OrganizationDomain.AI,
    "inference": OrganizationDomain.AI,
    "lucidia": OrganizationDomain.AI,
    "reasoning": OrganizationDomain.AI,
    "model": OrganizationDomain.AI,
    # Cloud
    "deploy": OrganizationDomain.CLOUD,
    "infrastructure": OrganizationDomain.CLOUD,
    "railway": OrganizationDomain.CLOUD,
    "droplet": OrganizationDomain.CLOUD,
    "orchestration": OrganizationDomain.CLOUD,
    # Hardware
    "raspberry": OrganizationDomain.HARDWARE,
    "raspberry pi": OrganizationDomain.HARDWARE,
    "firmware": OrganizationDomain.HARDWARE,
    "iot": OrganizationDomain.HARDWARE,
    "sbc": OrganizationDomain.HARDWARE,
    # OS
    "cli": OrganizationDomain.OS,
    "kernel": OrganizationDomain.OS,
    "operator": OrganizationDomain.OS,
    # Labs
    "experiment": OrganizationDomain.LABS,
    "quantum": OrganizationDomain.LABS,
    "research": OrganizationDomain.LABS,
    # Interactive
    "frontend": OrganizationDomain.INTERACTIVE,
    "ui": OrganizationDomain.INTERACTIVE,
    "website": OrganizationDomain.INTERACTIVE,
    # Media
    "content": OrganizationDomain.MEDIA,
    "media": OrganizationDomain.MEDIA,
    "blog": OrganizationDomain.MEDIA,
    # Education
    "onboarding": OrganizationDomain.EDUCATION,
    "tutorial": OrganizationDomain.EDUCATION,
    "documentation": OrganizationDomain.EDUCATION,
    # Gov
    "compliance": OrganizationDomain.GOV,
    "regulatory": OrganizationDomain.GOV,
    "policy": OrganizationDomain.GOV,
    # Foundation
    "governance": OrganizationDomain.FOUNDATION,
    "protocol": OrganizationDomain.FOUNDATION,
    # Archive
    "archive": OrganizationDomain.ARCHIVE,
    "backup": OrganizationDomain.ARCHIVE,
    "history": OrganizationDomain.ARCHIVE,
    # Studio
    "creative": OrganizationDomain.STUDIO,
    "design": OrganizationDomain.STUDIO,
    "asset": OrganizationDomain.STUDIO,
    # Ventures
    "tokenomics": OrganizationDomain.VENTURES,
    "funding": OrganizationDomain.VENTURES,
    "venture": OrganizationDomain.VENTURES,
    # Corporate
    "enterprise": OrganizationDomain.CORPORATE,
    "corporate": OrganizationDomain.CORPORATE,
}


class RoutingMatrix:
    """Routes tasks to the appropriate BlackRoad organization based on intent."""

    def __init__(self) -> None:
        self.organizations = ORGANIZATIONS
        self.domains = DOMAIN_REGISTRY

    def route(self, intent: str) -> RouteDecision:
        """Route a task intent to the best-matching organization.

        Args:
            intent: Natural language description of the task.

        Returns:
            A RouteDecision with the target organization and confidence.
        """
        intent_lower = intent.lower()
        scores: Dict[OrganizationDomain, int] = {}

        for keyword, domain in _ROUTING_KEYWORDS.items():
            if keyword in intent_lower:
                scores[domain] = scores.get(domain, 0) + 1

        if not scores:
            return RouteDecision(
                organization="BlackRoad-OS",
                domain=OrganizationDomain.OS,
                confidence=0.1,
                reasoning="No keyword match; defaulting to core OS organization.",
            )

        best_domain = max(scores, key=scores.get)
        total_keywords = sum(scores.values())
        confidence = min(scores[best_domain] / max(total_keywords, 1), 1.0)

        # Find the organization for the winning domain
        target_org = next(
            (org for org in self.organizations.values() if org.domain == best_domain),
            None,
        )
        org_name = target_org.name if target_org else "BlackRoad-OS"

        matched = [k for k, v in _ROUTING_KEYWORDS.items()
                   if k in intent_lower and v == best_domain]

        return RouteDecision(
            organization=org_name,
            domain=best_domain,
            confidence=round(confidence, 2),
            reasoning=f"Matched keywords: {', '.join(matched)}",
        )

    def get_organization(self, name: str) -> Optional[Organization]:
        """Look up an organization by name."""
        return self.organizations.get(name)

    def get_domains_for_org(self, org_name: str) -> List[DomainEntry]:
        """Return all domains associated with an organization."""
        return [d for d in self.domains if d.organization == org_name]

    def list_organizations(self) -> List[Dict[str, Any]]:
        """Return all organizations as serializable dicts."""
        return [asdict(org) for org in self.organizations.values()]

    def list_domains(self) -> List[Dict[str, str]]:
        """Return all domains as serializable dicts."""
        return [asdict(d) for d in self.domains]


# Rate-limit mitigation configuration
RATE_LIMIT_STRATEGIES: Dict[str, Dict[str, str]] = {
    "github_copilot": {
        "observed_limit": "RPM / Token Exhaustion",
        "mitigation": "Redirect to local Raspberry Pi LiteLLM proxy",
        "proxy_url": "http://raspberrypi.local:4000",
        "env_var": "GH_COPILOT_OVERRIDE_PROXY_URL",
    },
    "huggingface": {
        "observed_limit": "IP-based Rate Limit",
        "mitigation": "Rotate HF_TOKEN or use authenticated SSH keys",
    },
    "google_drive": {
        "observed_limit": "Individual User Quota",
        "mitigation": "Use Shared Drives with GSA Content Manager role",
    },
    "digitalocean": {
        "observed_limit": "Concurrent Build Limits",
        "mitigation": "Queue tasks via Layer 7 Orchestration",
    },
    "salesforce": {
        "observed_limit": "Daily API Request Cap",
        "mitigation": "Batch updates via Data Cloud Streaming Transforms",
    },
}


if __name__ == "__main__":
    matrix = RoutingMatrix()

    # Example: route a security task
    decision = matrix.route("Run a security audit on the hash-witnessing repository")
    print(json.dumps(asdict(decision), indent=2, default=str))

    # Example: route an AI task
    decision = matrix.route("Deploy a new LLM inference model to lucidia")
    print(json.dumps(asdict(decision), indent=2, default=str))

    # List organizations
    print(f"\nTotal organizations: {len(matrix.list_organizations())}")
    print(f"Total domains: {len(matrix.list_domains())}")
