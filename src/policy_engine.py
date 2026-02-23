"""
Security policy engine for BlackRoad Security.
Manages and enforces security policies across the organization.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Callable
from enum import Enum
from dataclasses import dataclass, asdict


class PolicyAction(Enum):
    """Policy enforcement actions."""
    ALLOW = "allow"
    DENY = "deny"
    AUDIT = "audit"
    REQUIRE_MFA = "require_mfa"
    REQUIRE_APPROVAL = "require_approval"


@dataclass
class PolicyRule:
    """Security policy rule."""
    rule_id: str
    name: str
    description: str
    condition: str
    action: PolicyAction
    priority: int
    enabled: bool = True


@dataclass
class PolicyViolation:
    """Policy violation record."""
    violation_id: str
    rule_id: str
    timestamp: datetime
    subject: str
    resource: str
    details: Dict[str, Any]
    severity: str


class PolicyEngine:
    """Production-grade security policy enforcement engine."""

    def __init__(self, db_path: str = "policies.db"):
        """Initialize policy engine.
        
        Args:
            db_path: Path to SQLite database for policies
        """
        self.db_path = db_path
        self._init_db()
        self._evaluators = {}

    def _init_db(self):
        """Initialize policy database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS policies (
                    rule_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    condition TEXT NOT NULL,
                    action TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    enabled INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_priority (priority),
                    INDEX idx_enabled (enabled)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS policy_violations (
                    violation_id TEXT PRIMARY KEY,
                    rule_id TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    subject TEXT NOT NULL,
                    resource TEXT NOT NULL,
                    details TEXT,
                    severity TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (rule_id) REFERENCES policies(rule_id),
                    INDEX idx_timestamp (timestamp),
                    INDEX idx_subject (subject),
                    INDEX idx_severity (severity)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS policy_exemptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    expires_at DATETIME,
                    reason TEXT,
                    FOREIGN KEY (rule_id) REFERENCES policies(rule_id)
                )
            """)
            conn.commit()

    def add_rule(
        self,
        rule_id: str,
        name: str,
        description: str,
        condition: str,
        action: PolicyAction,
        priority: int
    ) -> bool:
        """Add a security policy rule.
        
        Args:
            rule_id: Unique rule identifier
            name: Human-readable rule name
            description: Rule description
            condition: Condition string for evaluation
            action: Action to take if violated
            priority: Rule priority (higher = evaluated first)
            
        Returns:
            True if rule added successfully
        """
        with sqlite3.connect(self.db_path) as conn:
            try:
                conn.execute("""
                    INSERT INTO policies
                    (rule_id, name, description, condition, action, priority)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (rule_id, name, description, condition, action.value, priority))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def evaluate_access(
        self,
        subject: str,
        resource: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Evaluate access request against policies.
        
        Args:
            subject: User or service requesting access
            resource: Resource being accessed
            context: Additional context (IP, time, etc.)
            
        Returns:
            Decision dict with action and violations
        """
        context = context or {}
        violations = []
        decisions = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM policies 
                WHERE enabled = 1 
                ORDER BY priority DESC
            """)
            rules = cursor.fetchall()
        
        for rule_row in rules:
            rule_id, name, desc, condition, action, priority, *_ = rule_row
            
            # Check exemption
            if self._is_exempt(subject, rule_id):
                continue
            
            # Evaluate condition
            if self._evaluate_condition(condition, subject, resource, context):
                action_enum = PolicyAction(action)
                decisions.append({
                    "rule_id": rule_id,
                    "action": action_enum.value,
                    "priority": priority
                })
                
                if action_enum == PolicyAction.DENY:
                    violation = self._record_violation(
                        rule_id, subject, resource, context
                    )
                    violations.append(violation)
                    break  # Stop on first deny
        
        # Determine final decision
        final_action = PolicyAction.ALLOW
        if violations:
            final_action = PolicyAction.DENY
        elif decisions:
            first_decision = decisions[0]
            final_action = PolicyAction(first_decision["action"])
        
        return {
            "decision": final_action.value,
            "subject": subject,
            "resource": resource,
            "decisions": decisions,
            "violations": violations,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _evaluate_condition(
        self,
        condition: str,
        subject: str,
        resource: str,
        context: Dict[str, Any]
    ) -> bool:
        """Evaluate policy condition string."""
        eval_globals = {
            "subject": subject,
            "resource": resource,
            **context
        }
        try:
            return bool(eval(condition, {"__builtins__": {}}, eval_globals))
        except Exception:
            return False

    def _is_exempt(self, subject: str, rule_id: str) -> bool:
        """Check if subject is exempt from rule."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 1 FROM policy_exemptions
                WHERE rule_id = ? AND subject = ? 
                AND (expires_at IS NULL OR expires_at > datetime('now'))
            """, (rule_id, subject))
            return cursor.fetchone() is not None

    def _record_violation(
        self,
        rule_id: str,
        subject: str,
        resource: str,
        context: Dict[str, Any]
    ) -> str:
        """Record policy violation."""
        import uuid
        violation_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO policy_violations
                (violation_id, rule_id, timestamp, subject, resource, details, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                violation_id,
                rule_id,
                datetime.utcnow().isoformat(),
                subject,
                resource,
                json.dumps(context),
                "HIGH"
            ))
            conn.commit()
        
        return violation_id

    def get_violations(
        self,
        subject: Optional[str] = None,
        hours: int = 24
    ) -> List[Dict[str, Any]]:
        """Query policy violations."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            query = """
                SELECT * FROM policy_violations 
                WHERE timestamp > datetime('now', ?)
            """
            params = [f'-{hours} hours']
            
            if subject:
                query += " AND subject = ?"
                params.append(subject)
            
            query += " ORDER BY timestamp DESC"
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]


if __name__ == "__main__":
    engine = PolicyEngine()
    
    # Add sample rule
    engine.add_rule(
        rule_id="admin_access",
        name="Admin Access",
        description="Enforce admin access controls",
        condition="resource.startswith('/admin') and 'admin' not in subject",
        action=PolicyAction.DENY,
        priority=100
    )
    
    # Evaluate access
    decision = engine.evaluate_access(
        subject="user:john",
        resource="/admin/settings",
        context={"ip": "192.168.1.1"}
    )
    print(json.dumps(decision, indent=2))
