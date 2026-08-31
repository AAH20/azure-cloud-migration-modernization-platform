from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


PHASES = ("assessed", "planned", "built", "validated", "canary", "cutover", "optimized")
REQUIRED_GATES = {
    "planned": {"application-owner-confirmed", "dependency-graph-validated"},
    "built": {"landing-zone-ready", "identity-dns-tested"},
    "validated": {"network-path-tested", "transaction-replay-pass", "recovery-objectives-pass"},
    "canary": {"rollback-tested", "security-review-pass"},
    "cutover": {"change-approval", "business-owner-approval"},
    "optimized": {"decommission-evidence", "finops-baseline-verified"},
}


@dataclass
class MigrationWorkflow:
    run_id: str
    workload: str
    phase: str = "assessed"
    evidence: dict[str, dict[str, Any]] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)

    def add_evidence(self, gate: str, artifact_sha256: str, actor: str) -> None:
        if len(artifact_sha256) != 64 or any(char not in "0123456789abcdef" for char in artifact_sha256):
            raise ValueError("artifact_sha256 must be a lowercase SHA-256 digest")
        self.evidence[gate] = {"artifact_sha256": artifact_sha256, "actor": actor}

    def advance(self, target: str, actor: str) -> dict[str, Any]:
        if target not in PHASES:
            raise ValueError("unknown target phase")
        current_index = PHASES.index(self.phase)
        if PHASES.index(target) != current_index + 1:
            raise ValueError("workflow transitions must advance exactly one phase")
        missing = sorted(REQUIRED_GATES[target] - self.evidence.keys())
        if missing:
            raise ValueError(f"missing evidence gates: {', '.join(missing)}")
        event = {
            "from": self.phase,
            "to": target,
            "actor": actor,
            "at": datetime.now(timezone.utc).isoformat(),
            "evidence": {gate: self.evidence[gate] for gate in sorted(REQUIRED_GATES[target])},
        }
        canonical = json.dumps(event, sort_keys=True, separators=(",", ":"))
        event["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
        self.phase = target
        self.history.append(event)
        return event

    def as_dict(self) -> dict[str, Any]:
        return {"run_id": self.run_id, "workload": self.workload, "phase": self.phase, "evidence": self.evidence, "history": self.history}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "MigrationWorkflow":
        return cls(**value)
