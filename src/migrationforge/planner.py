from __future__ import annotations

import hashlib
import json
from collections import defaultdict, deque
from typing import Any


def assess(estate: dict[str, Any]) -> dict[str, Any]:
    _validate(estate)
    decisions = [_decision(group) for group in estate["workload_groups"]]
    waves = _waves(estate["dependencies"])
    economics = _economics(estate["economics"])
    risky = [item for item in decisions if item["status"] == "blocked"]
    totals: dict[str, int] = defaultdict(int)
    for decision in decisions:
        totals[decision["strategy"]] += decision["application_count"]
    report: dict[str, Any] = {
        "schema_version": "migrationforge/v1",
        "scenario": estate["scenario"],
        "evidence_level": "synthetic-estate",
        "estate_summary": estate["estate_summary"],
        "strategy_portfolio": dict(sorted(totals.items())),
        "decisions": decisions,
        "migration_waves": waves,
        "economics": economics,
        "readiness": "blocked" if risky else "eligible-for-pilot-wave",
        "production_control": {
            "auto_execute": False,
            "required_gates": ["owner confirmation", "dependency validation", "transaction replay", "rollback test", "change approval"],
        },
        "claim_boundary": [
            "No live VMware, Azure, AWS, GCP or Kubernetes inventory was accessed",
            "No workload was migrated and no production cutover was performed",
            "Costs and outage values are configurable synthetic inputs",
            "Recommendations require customer evidence and accountable-owner approval",
        ],
        "search_evidence": estate["search_evidence"],
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["receipt_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return report


def _decision(group: dict[str, Any]) -> dict[str, Any]:
    status = "eligible"
    reasons = []
    if group["retire_candidate"]:
        strategy = "retire"
        reasons.append("no active business transactions")
    elif group["saas_replacement"]:
        strategy = "repurchase"
        reasons.append("approved SaaS replacement exists")
    elif group["latency_to_factory_ms"] > group["max_latency_ms"]:
        strategy = "retain"
        reasons.append("measured dependency latency exceeds workload SLO")
        status = "blocked"
    elif group["container_ready"] and group["modernization_value"] == "high":
        strategy = "replatform"
        reasons.append("container-ready with high modernization value")
    elif group["code_change_required"] and group["business_value"] == "high":
        strategy = "refactor"
        reasons.append("high-value workload requires architectural change")
    else:
        strategy = "rehost"
        reasons.append("deadline favors low-change relocation")
    if group["unsupported_os"]:
        reasons.append("unsupported operating system requires remediation before migration")
        status = "blocked"
    return {
        "group": group["name"],
        "application_count": group["application_count"],
        "vm_count": group["vm_count"],
        "strategy": strategy,
        "status": status,
        "reasons": reasons,
        "target": _target(strategy),
    }


def _target(strategy: str) -> str:
    return {
        "retire": "decommission with evidence retention",
        "repurchase": "SaaS integration landing zone",
        "retain": "on-premises with hybrid connectivity",
        "replatform": "Azure Kubernetes Service",
        "refactor": "Azure application landing zone",
        "rehost": "Azure virtual machines",
    }[strategy]


def _waves(edges: list[dict[str, str]]) -> list[dict[str, Any]]:
    graph: dict[str, list[str]] = defaultdict(list)
    degree: dict[str, int] = defaultdict(int)
    nodes: set[str] = set()
    for edge in edges:
        dependency, workload = edge["dependency"], edge["workload"]
        graph[dependency].append(workload)
        degree[workload] += 1
        nodes.update((dependency, workload))
    queue = deque(sorted(node for node in nodes if degree[node] == 0))
    levels: dict[str, int] = {node: 0 for node in queue}
    visited = []
    while queue:
        node = queue.popleft()
        visited.append(node)
        for child in sorted(graph[node]):
            levels[child] = max(levels.get(child, 0), levels[node] + 1)
            degree[child] -= 1
            if degree[child] == 0:
                queue.append(child)
    if len(visited) != len(nodes):
        raise ValueError("dependency graph contains a cycle")
    grouped: dict[int, list[str]] = defaultdict(list)
    for node in visited:
        grouped[levels[node]].append(node)
    return [
        {"wave": index, "workloads": sorted(grouped[index]), "required_validation": ["synthetic transactions", "network paths", "identity", "rollback"]}
        for index in sorted(grouped)
    ]


def _economics(values: dict[str, float]) -> dict[str, float]:
    monthly_difference = values["current_monthly_cost_usd"] - values["target_monthly_cost_usd"]
    payback = values["migration_investment_usd"] / monthly_difference if monthly_difference > 0 else 0
    outage_reduction = (values["baseline_cutover_hours"] - values["validated_cutover_hours"]) * values["outage_cost_per_hour_usd"]
    dual_run_cost = values["current_monthly_cost_usd"] / 30 * values["dual_run_days"]
    return {
        "current_monthly_cost_usd": round(values["current_monthly_cost_usd"], 2),
        "target_monthly_cost_usd": round(values["target_monthly_cost_usd"], 2),
        "modeled_monthly_difference_usd": round(monthly_difference, 2),
        "migration_investment_usd": round(values["migration_investment_usd"], 2),
        "dual_run_cost_usd": round(dual_run_cost, 2),
        "simple_payback_months": round(payback, 2),
        "modeled_outage_exposure_reduction_usd": round(outage_reduction, 2),
    }


def _validate(estate: dict[str, Any]) -> None:
    required = {"scenario", "estate_summary", "workload_groups", "dependencies", "economics", "search_evidence"}
    missing = sorted(required - estate.keys())
    if missing:
        raise ValueError(f"missing keys: {', '.join(missing)}")
    apps = sum(group["application_count"] for group in estate["workload_groups"])
    vms = sum(group["vm_count"] for group in estate["workload_groups"])
    if apps != estate["estate_summary"]["applications"] or vms != estate["estate_summary"]["virtual_machines"]:
        raise ValueError("workload-group totals do not match estate summary")
