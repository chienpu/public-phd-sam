#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
shacl_validation.py — Lightweight semantic consistency checks (PdM)

本專案不強依賴外部 SHACL 引擎，以「可重現且輕量」為目標，提供一組
等價的資料一致性檢查（可視為 SHACL-like rules），輸出 violations 報告。

檢查範例：
- BuildingComponent 必須有 component_id
- SensorData 必須有 sensor_data_id
- PerformanceData 必須有 performance_id + value
- 重要關係存在性（如 Component 有連到 SensorData / Anomaly）

Usage:
    python 03_execution/shacl_validation.py --config config/pdm_demo.yaml
"""
from __future__ import annotations

import argparse
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
    args = ap.parse_args()

    cfg = load_config(args.config)
    scenario = cfg.get("scenario", "PdM_HVAC")
    mode = cfg.get("mode", "sam")
    out_dir = cfg.get("output_dir", "./logs")
    logger = RunLogger(out_dir=out_dir, scenario=scenario, mode=mode, component="shacl_validation")

    logger.log_event("START", details={"t": utc_now_iso()})

    if not neo4j_available():
        logger.log_event("NEO4J_NOT_AVAILABLE", level="WARN")
        logger.write_csv()
        print("Neo4j driver not available. Dry-run only.")
        return

    neo = Neo4jHelper.from_config(cfg.get("neo4j", {}))

    checks = [
        ("BuildingComponent has component_id", "MATCH (c:BuildingComponent) WHERE c.component_id IS NULL RETURN count(c) AS n"),
        ("SensorData has sensor_data_id", "MATCH (s:SensorData) WHERE s.sensor_data_id IS NULL RETURN count(s) AS n"),
        ("PerformanceData has performance_id", "MATCH (p:PerformanceData) WHERE p.performance_id IS NULL RETURN count(p) AS n"),
        ("PerformanceData has value", "MATCH (p:PerformanceData) WHERE p.value IS NULL RETURN count(p) AS n"),
        ("Component maps sensor data", "MATCH (c:BuildingComponent) WHERE NOT (c)-[:MAPS_SENSOR_DATA]->(:SensorData) RETURN count(c) AS n"),
    ]

    violations = []
    for name, q in checks:
        r = neo.query(q, {})
        n = int(r[0]["n"]) if r else 0
        if n > 0:
            violations.append({"check": name, "violations": n})

    if violations:
        logger.log_event("VALIDATION_FAIL", level="WARN", details={"violations": violations})
    else:
        logger.log_event("VALIDATION_PASS", details={})

    logger.log_event("DONE")
    logger.write_csv()
    print("Validation complete. Violations:", len(violations))

if __name__ == "__main__":
    main()
