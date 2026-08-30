from __future__ import annotations

from typing import Any


def markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['scenario']}",
        "",
        f"**Readiness:** `{report['readiness']}`",
        f"**Evidence:** `{report['evidence_level']}`",
        f"**Receipt:** `{report['receipt_sha256']}`",
        "",
        "## Cloud migration and modernization portfolio",
        "",
        "| Workload group | Applications | VMs | 7R strategy | Target | Status |",
        "|---|---:|---:|---|---|---|",
    ]
    for item in report["decisions"]:
        lines.append(f"| {item['group']} | {item['application_count']} | {item['vm_count']} | {item['strategy']} | {item['target']} | {item['status']} |")
    lines.extend(["", "## Dependency-aware migration waves", ""])
    for wave in report["migration_waves"]:
        lines.append(f"- Wave {wave['wave']}: {', '.join(wave['workloads'])}")
    lines.extend(["", "## Cloud migration business case", ""])
    for key, value in report["economics"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Claim boundary", ""])
    for boundary in report["claim_boundary"]:
        lines.append(f"- {boundary}")
    return "\n".join(lines) + "\n"
