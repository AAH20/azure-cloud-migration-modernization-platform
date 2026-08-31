import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient

from migrationforge.controlplane import create_app
from migrationforge.workflow import MigrationWorkflow

ROOT = Path(__file__).parents[1]
DIGEST = hashlib.sha256(b"verified-evidence").hexdigest()


def test_transition_requires_evidence():
    workflow = MigrationWorkflow("run-1", "orders")
    try:
        workflow.advance("planned", "architect@example.com")
        raise AssertionError("transition should have failed")
    except ValueError as exc:
        assert "application-owner-confirmed" in str(exc)


def test_transition_receipt_is_bound_to_evidence():
    workflow = MigrationWorkflow("run-1", "orders")
    workflow.add_evidence("application-owner-confirmed", DIGEST, "owner@example.com")
    workflow.add_evidence("dependency-graph-validated", DIGEST, "architect@example.com")
    event = workflow.advance("planned", "architect@example.com")
    assert workflow.phase == "planned"
    assert len(event["receipt_sha256"]) == 64


def test_control_plane_is_idempotent(tmp_path):
    estate = json.loads((ROOT / "examples/vmware-to-azure/250-vm-estate.json").read_text())
    with TestClient(create_app(estate, str(tmp_path / "runs.db"))) as client:
        payload = {"workload": "order-processing", "idempotency_key": "order-processing-001"}
        first = client.post("/v1/runs", json=payload)
        second = client.post("/v1/runs", json=payload)
        assert first.status_code == 201
        assert first.json()["run_id"] == second.json()["run_id"]


def test_control_plane_blocks_ungated_transition(tmp_path):
    estate = json.loads((ROOT / "examples/vmware-to-azure/250-vm-estate.json").read_text())
    with TestClient(create_app(estate, str(tmp_path / "runs.db"))) as client:
        run = client.post("/v1/runs", json={"workload": "orders", "idempotency_key": "orders-run-001"}).json()
        response = client.post(f"/v1/runs/{run['run_id']}/transition", json={"target": "planned", "actor": "agent"})
        assert response.status_code == 409
