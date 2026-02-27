"""
BlackRoad OS Deca-Layered Task Scaffold.

Implements the 10-step scaffolding process triggered by the @blackroad-agents
command. Each step defines a stage of task review, distribution, and deployment.
"""

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class ScaffoldStep(Enum):
    """The ten steps of the @blackroad-agents scaffold."""
    INITIAL_REVIEWER = 1
    TASK_TO_ORGANIZATION = 2
    TASK_TO_TEAM = 3
    TASK_TO_PROJECT = 4
    TASK_TO_AGENT = 5
    TASK_TO_REPOSITORY = 6
    TASK_TO_DEVICE = 7
    TASK_TO_DRIVE = 8
    TASK_TO_CLOUDFLARE = 9
    TASK_TO_WEBSITE_EDITOR = 10


SCAFFOLD_DESCRIPTIONS: Dict[ScaffoldStep, str] = {
    ScaffoldStep.INITIAL_REVIEWER: (
        "Layer 6 (Lucidia Core) agent reviews the request for clarity, "
        "security compliance, and resource availability."
    ),
    ScaffoldStep.TASK_TO_ORGANIZATION: (
        "Route the task to one of the 15 BlackRoad organizations based "
        "on functional domain."
    ),
    ScaffoldStep.TASK_TO_TEAM: (
        "Distribute the task to a specific team within the organization. "
        "Pause for manual approval on high-risk operations."
    ),
    ScaffoldStep.TASK_TO_PROJECT: (
        "Record the task in a GitHub Project board and synchronize "
        "metadata with Salesforce for enterprise audit trail."
    ),
    ScaffoldStep.TASK_TO_AGENT: (
        "Instantiate or assign a specialized autonomous agent using the "
        "Planner-Executor-Reflector design pattern."
    ),
    ScaffoldStep.TASK_TO_REPOSITORY: (
        "Identify the target repository, create a new branch, and "
        "follow GitHub Flow branching strategy."
    ),
    ScaffoldStep.TASK_TO_DEVICE: (
        "Route to device layer for physical execution (firmware updates, "
        "Raspberry Pi deployments, DigitalOcean Droplets)."
    ),
    ScaffoldStep.TASK_TO_DRIVE: (
        "Distribute artifacts to Google Drive using Service Account "
        "(GSA) pattern for persistent storage."
    ),
    ScaffoldStep.TASK_TO_CLOUDFLARE: (
        "Execute network configuration changes (Cloudflare Tunnels, "
        "DNS records) to make services reachable and secured."
    ),
    ScaffoldStep.TASK_TO_WEBSITE_EDITOR: (
        "Route to AI-driven website editor or headless CMS for "
        "autonomous content generation and landing page updates."
    ),
}


class StepStatus(Enum):
    """Status of a scaffold step."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    AWAITING_APPROVAL = "awaiting_approval"


@dataclass
class StepResult:
    """Result of executing a scaffold step."""
    step: ScaffoldStep
    status: StepStatus
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class TaskRecord:
    """A task moving through the scaffold."""
    task_id: str
    intent: str
    created_at: str
    organization: Optional[str] = None
    team: Optional[str] = None
    agent: Optional[str] = None
    repository: Optional[str] = None
    branch: Optional[str] = None
    steps: List[StepResult] = field(default_factory=list)
    witness_hash: Optional[str] = None

    def current_step(self) -> Optional[ScaffoldStep]:
        """Return the next pending step, or None if all complete."""
        completed = {s.step for s in self.steps if s.status == StepStatus.COMPLETED}
        for step in ScaffoldStep:
            if step not in completed:
                return step
        return None


class ScaffoldEngine:
    """Executes the deca-layered task scaffold.

    Each task progresses through 10 sequential steps.  The engine
    records every state transition and produces a SHA-256 witness
    hash for the roadchain ledger.
    """

    def __init__(self) -> None:
        self._tasks: Dict[str, TaskRecord] = {}

    def create_task(self, intent: str) -> TaskRecord:
        """Create a new task and initialize the scaffold.

        Args:
            intent: Natural language description of what needs to be done.

        Returns:
            A TaskRecord with a unique task_id.
        """
        task = TaskRecord(
            task_id=str(uuid.uuid4()),
            intent=intent,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._tasks[task.task_id] = task
        return task

    def advance(
        self,
        task_id: str,
        output: Optional[Dict[str, Any]] = None,
    ) -> StepResult:
        """Advance a task to the next scaffold step.

        Args:
            task_id: The unique task identifier.
            output: Optional output data from the step execution.

        Returns:
            The StepResult for the step that was executed.

        Raises:
            KeyError: If the task_id is not found.
            RuntimeError: If all steps are already complete.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Task not found: {task_id}")

        step = task.current_step()
        if step is None:
            raise RuntimeError(f"All scaffold steps already complete for {task_id}")

        now = datetime.now(timezone.utc).isoformat()
        result = StepResult(
            step=step,
            status=StepStatus.COMPLETED,
            started_at=now,
            completed_at=now,
            output=output or {},
        )
        task.steps.append(result)

        # Update task metadata based on the step
        if step == ScaffoldStep.TASK_TO_ORGANIZATION and output:
            task.organization = output.get("organization")
        elif step == ScaffoldStep.TASK_TO_TEAM and output:
            task.team = output.get("team")
        elif step == ScaffoldStep.TASK_TO_AGENT and output:
            task.agent = output.get("agent")
        elif step == ScaffoldStep.TASK_TO_REPOSITORY and output:
            task.repository = output.get("repository")
            task.branch = output.get("branch")

        # Compute witness hash after each step
        task.witness_hash = self._compute_witness_hash(task)
        return result

    def fail_step(
        self,
        task_id: str,
        error: str,
    ) -> StepResult:
        """Mark the current step as failed.

        Args:
            task_id: The unique task identifier.
            error: Description of the failure.

        Returns:
            The StepResult with failed status.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Task not found: {task_id}")

        step = task.current_step()
        if step is None:
            raise RuntimeError(f"All scaffold steps already complete for {task_id}")

        now = datetime.now(timezone.utc).isoformat()
        result = StepResult(
            step=step,
            status=StepStatus.FAILED,
            started_at=now,
            completed_at=now,
            error=error,
        )
        task.steps.append(result)
        task.witness_hash = self._compute_witness_hash(task)
        return result

    def get_task(self, task_id: str) -> Optional[TaskRecord]:
        """Retrieve a task by ID."""
        return self._tasks.get(task_id)

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Return a serializable summary of the task's current state."""
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Task not found: {task_id}")

        current = task.current_step()
        return {
            "task_id": task.task_id,
            "intent": task.intent,
            "organization": task.organization,
            "current_step": current.name if current else "COMPLETE",
            "steps_completed": sum(
                1 for s in task.steps if s.status == StepStatus.COMPLETED
            ),
            "total_steps": len(ScaffoldStep),
            "witness_hash": task.witness_hash,
        }

    @staticmethod
    def _compute_witness_hash(task: TaskRecord) -> str:
        """Compute a SHA-256 witness hash for the roadchain ledger.

        Every state transition is hashed and appended to the
        non-terminating witnessing ledger.
        """
        payload = json.dumps(
            {
                "task_id": task.task_id,
                "intent": task.intent,
                "steps": [
                    {
                        "step": s.step.name,
                        "status": s.status.value,
                        "completed_at": s.completed_at,
                    }
                    for s in task.steps
                ],
            },
            sort_keys=True,
        )
        return hashlib.sha256(payload.encode()).hexdigest()

    @staticmethod
    def describe_step(step: ScaffoldStep) -> str:
        """Return a human-readable description of a scaffold step."""
        return SCAFFOLD_DESCRIPTIONS.get(step, "Unknown step.")


if __name__ == "__main__":
    engine = ScaffoldEngine()

    # Create a task
    task = engine.create_task("Deploy security audit to BlackRoad-Security")
    print(f"Task created: {task.task_id}")

    # Walk through scaffold steps
    for i in range(len(ScaffoldStep)):
        step = task.current_step()
        if step is None:
            break
        print(f"\nStep {step.value}: {step.name}")
        print(f"  Description: {engine.describe_step(step)}")
        result = engine.advance(task.task_id, {"status": "ok"})
        print(f"  Status: {result.status.value}")

    # Final status
    status = engine.get_task_status(task.task_id)
    print(f"\n{json.dumps(status, indent=2)}")
