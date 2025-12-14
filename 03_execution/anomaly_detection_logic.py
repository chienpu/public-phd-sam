#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
anomaly_detection_logic.py — PdM Execution (Traversal / Rule Logic)

在 Neo4j 圖譜上執行「複合條件異常偵測」，產生 Anomaly 節點並連結到
SensorData / PerformanceData / BuildingComponent，對應 TIAA 的 Trigger + Issue。

設計：
- 以「規則」替代 ML（符合你目前論文的 demo/原型階段）
- 允許使用 config 內的 threshold 規則
- 輸出偵測 log（t_trigger, t_detected, t_task_created 可於後續流程補齊）

Usage:
    python 03_execution/anomaly_detection_logic.py --config config/pdm_demo.yaml --demo ahu12
"""
from __future__ import annotations

import argparse
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List

from utils.config_loader import load_config
from utils.logger import RunLogger
from utils.neo4j_helper import Neo4jHelper, neo4j_available


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--demo", default="ahu12", help="demo target (e.g., ahu12)")
    args = ap.parse_args()

    cfg = load_config(args.config)
    scenario = cfg.get("scenario", "PdM_HVAC")
    mode = cfg.get("mode", "sam")

    out_dir = cfg.get("output_dir", "./logs")
    logger = RunLogger(out_dir=out_dir, scenario=scenario, mode=mode, component="anomaly_detection")

    logger.log_event("START", details={"demo": args.demo})

    if not neo4j_available():
        logger.log_event("NEO4J_NOT_AVAILABLE", level="WARN")
        logger.write_csv()
        print("Neo4j driver not available. Dry-run only.")
        return

    neo = Neo4jHelper.from_config(cfg.get("neo4j", {}))

    # Threshold rule (configurable)
    rules = cfg.get("anomaly_rules", {
        "default_metric": "temperature",
        "upper": 30.0,
        "lower": None
    })

    metric = rules.get("default_metric", "temperature")
    upper = rules.get("upper", None)
    lower = rules.get("lower", None)

    # Query candidate PerformanceData
    # We assume PerformanceData has properties: performance_id, metric, value, timestamp, component_id
    q = """
    MATCH (pd:PerformanceData)
    WHERE ($metric IS NULL OR pd.metric = $metric)
      AND pd.value IS NOT NULL
    RETURN pd.performance_id AS performance_id,
           pd.timestamp AS timestamp,
           pd.metric AS metric,
           toFloat(pd.value) AS value,
           pd.component_id AS component_id
    LIMIT $limit
    """
    limit = int(cfg.get("anomaly_query_limit", 5000))

    t_trigger = utc_now_iso()  # treat this run as trigger emit time (for controlled replay)
    logger.log_event("TRIGGER_EMIT", details={"t_trigger": t_trigger})

    rows = neo.query(q, {"metric": metric, "limit": limit})
    t_detected = utc_now_iso()
    logger.log_event("DETECTION_START", details={"candidates": len(rows), "t_detected": t_detected})

    anomalies = []
    for r in rows:
        v = r.get("value", None)
        if v is None:
            continue
        is_anom = False
        if upper is not None and v > float(upper):
            is_anom = True
        if lower is not None and v < float(lower):
            is_anom = True
        if not is_anom:
            continue

        anomaly_id = f"anom_{uuid.uuid4().hex[:12]}"
        anomalies.append({
            "anomaly_id": anomaly_id,
            "type": "RuleBasedThreshold",
            "severity": "HIGH" if upper is not None and v > float(upper) else "MEDIUM",
            "metric": r.get("metric"),
            "value": v,
            "timestamp": r.get("timestamp"),
            "t_trigger": t_trigger,
            "t_detected": t_detected,
            "performance_id": r.get("performance_id"),
            "component_id": r.get("component_id"),
        })

    # Write anomalies into Neo4j
    if anomalies:
        neo.merge_nodes("Anomaly", "anomaly_id", [
            {k:v for k,v in a.items() if k not in ("performance_id","component_id")}
            for a in anomalies
        ])

        # Connect: PerformanceData -[:GENERATES]-> Anomaly, Component -[:HAS_ANOMALY]-> Anomaly
        rel_pd = [(a["performance_id"], a["anomaly_id"]) for a in anomalies if a.get("performance_id")]
        rel_c  = [(a["component_id"], a["anomaly_id"]) for a in anomalies if a.get("component_id")]
        neo.merge_rels("PerformanceData", "performance_id", "Anomaly", "anomaly_id", rel_pd, rel_type="GENERATES")
        neo.merge_rels("BuildingComponent", "component_id", "Anomaly", "anomaly_id", rel_c, rel_type="HAS_ANOMALY")

    logger.log_event("DETECTION_DONE", details={"anomaly_count": len(anomalies), "upper": upper, "lower": lower})
    logger.log_event("DONE")
    logger.write_csv()
    print("Anomaly detection complete. Logs:", logger.default_csv_name())

if __name__ == "__main__":
    main()
