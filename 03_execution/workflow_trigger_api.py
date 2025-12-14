#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflow_trigger_api.py — PdM Execution (Workflow Trigger + Log Timestamps)

針對 Neo4j 中偵測到的 Anomaly 觸發外部工作流（Power Automate / n8n / webhook）。
本版本包含「workflow mock」功能：當未提供 endpoint 或 mock 啟用時，會以本地模擬回應，
同時產生可用於 TTA / latency 計算的時間戳（t_task_created / t_action_start / t_action_end）。

Usage:
    python 03_execution/workflow_trigger_api.py --config config/pdm_demo.yaml --demo ahu12

Outputs:
- logs/workflow_events.csv (by RunLogger)
- optional: 04_validation/workflow_logs/sample_workflow_log.csv (if configured)
"""
from __future__ import annotations

import argparse
import json
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

try:
    import requests
except Exception:
    requests = None  # allow running without requests

from utils.config_loader import load_config
from utils.logger import RunLogger
from utils.neo4j_helper import Neo4jHelper, neo4j_available


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def mock_workflow(payload: Dict[str, Any], sleep_ms: int = 120) -> Dict[str, Any]:
    time.sleep(max(sleep_ms, 0) / 1000.0)
    return {"status": "OK", "message": "mocked", "echo": {"anomaly_id": payload.get("anomaly_id")}}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--demo", default="ahu12")
    args = ap.parse_args()

    cfg = load_config(args.config)
    scenario = cfg.get("scenario", "PdM_HVAC")
    mode = cfg.get("mode", "sam")

    out_dir = cfg.get("output_dir", "./logs")
    logger = RunLogger(out_dir=out_dir, scenario=scenario, mode=mode, component="workflow_trigger")

    if not neo4j_available():
        logger.log_event("NEO4J_NOT_AVAILABLE", level="WARN")
        logger.write_csv()
        print("Neo4j driver not available. Dry-run only.")
        return

    neo = Neo4jHelper.from_config(cfg.get("neo4j", {}))

    # Workflow config
    wf = cfg.get("workflow", {})
    endpoint = wf.get("endpoint", "")  # webhook URL
    use_mock = bool(wf.get("mock", True)) or not endpoint
    timeout_s = float(wf.get("timeout_s", 5.0))
    mock_sleep_ms = int(wf.get("mock_sleep_ms", 120))

    # Query anomalies that are not yet dispatched (simple heuristic)
    q = """
    MATCH (a:Anomaly)
    WHERE coalesce(a.dispatched,false) = false
    RETURN a.anomaly_id AS anomaly_id,
           a.type AS type,
           a.severity AS severity,
           a.metric AS metric,
           a.value AS value,
           a.timestamp AS ts
    LIMIT $limit
    """
    limit = int(cfg.get("workflow_query_limit", 200))
    anomalies = neo.query(q, {"limit": limit})

    logger.log_event("START", details={"demo": args.demo, "candidates": len(anomalies), "mock": use_mock})

    # Create tasks + trigger workflow per anomaly
    for a in anomalies:
        anomaly_id = a.get("anomaly_id")
        if not anomaly_id:
            continue

        # (1) Task created
        task_id = f"wo_{uuid.uuid4().hex[:10]}"
        t_task_created = utc_now_iso()

        # Persist a WorkOrder node to support downstream metrics if desired
        neo.query("""
            MERGE (wo:WorkOrder {workorder_id:$woid})
            SET wo.mode=$mode,
                wo.status='CREATED',
                wo.t_trigger=coalesce(wo.t_trigger,$t_trigger),
                wo.t_task_created=$t_task_created
            WITH wo
            MATCH (a:Anomaly {anomaly_id:$aid})
            MERGE (wo)-[:CREATED_FROM]->(a)
        """, {
            "woid": task_id,
            "aid": anomaly_id,
            "mode": mode,
            "t_trigger": t_task_created,  # if you don't have a separate trigger stream timestamp
            "t_task_created": t_task_created,
        })

        payload = {
            "workorder_id": task_id,
            "anomaly_id": anomaly_id,
            "type": a.get("type"),
            "severity": a.get("severity"),
            "metric": a.get("metric"),
            "value": a.get("value"),
            "timestamp": a.get("ts"),
            "scenario": scenario,
            "mode": mode,
        }

        # (2) Action start (dispatch)
        t_action_start = utc_now_iso()
        resp_ok = False
        resp_body: Dict[str, Any] = {}
        try:
            if use_mock:
                resp_body = mock_workflow(payload, sleep_ms=mock_sleep_ms)
                resp_ok = True
            else:
                if requests is None:
                    raise RuntimeError("requests not installed; set workflow.mock=true or pip install requests")
                r = requests.post(endpoint, json=payload, timeout=timeout_s)
                resp_ok = (200 <= r.status_code < 300)
                try:
                    resp_body = r.json()
                except Exception:
                    resp_body = {"text": r.text[:500], "status_code": r.status_code}
        except Exception as e:
            resp_ok = False
            resp_body = {"error": str(e)}

        # (3) Action end
        t_action_end = utc_now_iso()

        # Update WorkOrder + mark anomaly dispatched
        neo.query("""
            MATCH (wo:WorkOrder {workorder_id:$woid})
            SET wo.status=$status,
                wo.t_action_start=$t_action_start,
                wo.t_action_end=$t_action_end,
                wo.response_ok=$resp_ok
            WITH wo
            MATCH (a:Anomaly {anomaly_id:$aid})
            SET a.dispatched=true, a.dispatched_at=$t_action_start
            MERGE (wo)-[:DISPATCHED_FOR]->(a)
        """, {
            "woid": task_id,
            "aid": anomaly_id,
            "status": "DISPATCHED" if resp_ok else "EXCEPTION",
            "t_action_start": t_action_start,
            "t_action_end": t_action_end,
            "resp_ok": bool(resp_ok),
        })

        # Log (for compute_metrics.py or audit)
        logger.log_event(
            "WORKFLOW_DISPATCH",
            details={
                "workorder_id": task_id,
                "anomaly_id": anomaly_id,
                "t_task_created": t_task_created,
                "t_action_start": t_action_start,
                "t_action_end": t_action_end,
                "response_ok": resp_ok,
                "response": resp_body,
                "mock": use_mock,
            }
        )

    logger.log_event("DONE")
    logger.write_csv()
    print("Workflow triggering complete. Logs:", logger.default_csv_name())

if __name__ == "__main__":
    main()
