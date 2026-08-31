from __future__ import annotations

import argparse
import json
import os
import sqlite3
import uuid
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from .planner import assess
from .workflow import MigrationWorkflow


class CreateRun(BaseModel):
    workload: str = Field(min_length=1, max_length=200)
    idempotency_key: str = Field(min_length=8, max_length=200)


class EvidenceInput(BaseModel):
    gate: str
    artifact_sha256: str
    actor: str


class TransitionInput(BaseModel):
    target: str
    actor: str


def create_app(estate: dict[str, Any], database_path: str | None = None) -> FastAPI:
    path = database_path or os.getenv("MIGRATIONFORGE_DB", "migrationforge.db")
    if os.getenv("MIGRATIONFORGE_ENV", "development") == "production" and path == "migrationforge.db":
        raise RuntimeError("production requires an explicit durable database path")
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.execute("CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE NOT NULL, state TEXT NOT NULL)")
    connection.commit()
    report = assess(estate)
    app = FastAPI(title="MigrationForge Modernization Control Plane", version="1.0.0")

    def authorize(authorization: str | None) -> None:
        expected = os.getenv("MIGRATIONFORGE_API_TOKEN")
        if os.getenv("MIGRATIONFORGE_ENV", "development") == "production" and not expected:
            raise HTTPException(503, "control-plane authentication is not configured")
        if expected and authorization != f"Bearer {expected}":
            raise HTTPException(401, "invalid bearer token")

    def load(run_id: str) -> MigrationWorkflow:
        row = connection.execute("SELECT state FROM runs WHERE id = ?", (run_id,)).fetchone()
        if row is None:
            raise HTTPException(404, "migration run not found")
        return MigrationWorkflow.from_dict(json.loads(row[0]))

    def save(workflow: MigrationWorkflow) -> None:
        connection.execute("UPDATE runs SET state = ? WHERE id = ?", (json.dumps(workflow.as_dict(), sort_keys=True), workflow.run_id))
        connection.commit()

    @app.get("/health/live")
    def live() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/health/ready")
    def ready() -> dict[str, Any]:
        connection.execute("SELECT 1").fetchone()
        return {"status": "ready", "assessment_receipt": report["receipt_sha256"]}

    @app.post("/v1/runs", status_code=201)
    def create(payload: CreateRun, authorization: str | None = Header(default=None)) -> dict[str, Any]:
        authorize(authorization)
        row = connection.execute("SELECT state FROM runs WHERE idempotency_key = ?", (payload.idempotency_key,)).fetchone()
        if row:
            return MigrationWorkflow.from_dict(json.loads(row[0])).as_dict()
        workflow = MigrationWorkflow(str(uuid.uuid4()), payload.workload)
        connection.execute("INSERT INTO runs VALUES (?, ?, ?)", (workflow.run_id, payload.idempotency_key, json.dumps(workflow.as_dict(), sort_keys=True)))
        connection.commit()
        return workflow.as_dict()

    @app.get("/v1/runs/{run_id}")
    def get(run_id: str, authorization: str | None = Header(default=None)) -> dict[str, Any]:
        authorize(authorization)
        return load(run_id).as_dict()

    @app.post("/v1/runs/{run_id}/evidence")
    def evidence(run_id: str, payload: EvidenceInput, authorization: str | None = Header(default=None)) -> dict[str, Any]:
        authorize(authorization)
        workflow = load(run_id)
        workflow.add_evidence(payload.gate, payload.artifact_sha256, payload.actor)
        save(workflow)
        return workflow.as_dict()

    @app.post("/v1/runs/{run_id}/transition")
    def transition(run_id: str, payload: TransitionInput, authorization: str | None = Header(default=None)) -> dict[str, Any]:
        authorize(authorization)
        workflow = load(run_id)
        try:
            event = workflow.advance(payload.target, payload.actor)
        except ValueError as exc:
            raise HTTPException(409, str(exc)) from exc
        save(workflow)
        return event

    return app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("estate", type=Path)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    uvicorn.run(create_app(json.loads(args.estate.read_text())), host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
