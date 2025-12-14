#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_ingestion_etl.py — PdM Execution (ETL)

讀取 02_data/PdM_HVAC 內的 CSV（raw/processed/edges/tasks/actors），
將資料以「可重現」方式匯入 Neo4j（節點與關係），並產出匯入日誌。

設計目標：
- 對齊論文 STRIDE：Semantic ingestion layer
- 支援 replication：同一份資料可在不同環境重建圖譜
- 不強依賴特定欄位名稱：用 config 提供欄位對映（mapping）

Usage:
    python 03_execution/data_ingestion_etl.py --config config/pdm_demo.yaml

輸出：
- logs/etl_import_log.csv（可選，依 config）
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple

import pandas as pd

from utils.config_loader import load_config
from utils.logger import RunLogger
from utils.neo4j_helper import Neo4jHelper, neo4j_available


# -----------------------------
# Helpers
# -----------------------------
def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)

def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]
    return df

# -----------------------------
# Main ETL
# -----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="YAML/JSON config path")
    args = ap.parse_args()

    cfg = load_config(args.config)
    scenario = cfg.get("scenario", "PdM_HVAC")
    mode = cfg.get("mode", "sam")

    # Paths
    root = Path(cfg.get("data_root", "../../02_data")).resolve()
    dataset = cfg.get("dataset", "PdM_HVAC")
    ds = (root / dataset).resolve()

    raw_dir = ds / "raw"
    processed_dir = ds / "processed"
    edges_dir = ds / "edges"
    tasks_dir = ds / "tasks"
    actors_dir = ds / "actors"

    # Logs
    out_dir = Path(cfg.get("output_dir", "./logs")).resolve()
    _ensure_dir(out_dir)
    logger = RunLogger(out_dir=out_dir, scenario=scenario, mode=mode, component="etl")

    logger.log_event("START", details={"dataset_path": str(ds)})

    # Read inputs (expected names, can be overridden in config)
    files = cfg.get("files", {})
    f_assets = raw_dir / files.get("assets", "BuildingComponent_Dataset.csv")
    f_sensor = raw_dir / files.get("sensor", "Sensor_Data_300.csv")
    f_perf = processed_dir / files.get("performance", "Performance_Data_300.csv")
    f_anom = processed_dir / files.get("anomaly", "Anomaly_Data_300.csv")
    f_edge_maps = edges_dir / files.get("edge_maps", "Edge_MAPS_SENSOR_DATA.csv")
    f_edge_gen = edges_dir / files.get("edge_generates", "Edge_GENERATES.csv")
    f_tasks = tasks_dir / files.get("tasks", "MaintenanceTasks_Generated.csv")
    f_actors = actors_dir / files.get("actors", "Actors.csv")

    # Hash inputs for provenance (optional)
    input_hashes = {}
    for p in [f_assets, f_sensor, f_perf, f_anom, f_edge_maps, f_edge_gen, f_tasks, f_actors]:
        if p.exists():
            input_hashes[p.name] = file_sha256(p)
    logger.log_event("INPUT_HASH", details=input_hashes)

    # Load data
    assets_df = _normalize_cols(_read_csv(f_assets))
    sensor_df = _normalize_cols(_read_csv(f_sensor))
    perf_df = _normalize_cols(_read_csv(f_perf))
    anom_df = _normalize_cols(_read_csv(f_anom))
    edge_maps_df = _normalize_cols(_read_csv(f_edge_maps))
    edge_gen_df = _normalize_cols(_read_csv(f_edge_gen))
    tasks_df = _normalize_cols(_read_csv(f_tasks))
    actors_df = _normalize_cols(_read_csv(f_actors))

    # If no Neo4j, we still write a dry-run report
    if not neo4j_available():
        logger.log_event("NEO4J_NOT_AVAILABLE", level="WARN", details={"hint": "pip install neo4j"})
        logger.write_csv()
        print("Neo4j driver not available. Dry-run only. Logs written to:", out_dir)
        return

    neo = Neo4jHelper.from_config(cfg.get("neo4j", {}))

    # Create minimal constraints/indexes (safe to run multiple times)
    with neo.session() as s:
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:BuildingComponent) REQUIRE c.component_id IS UNIQUE")
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (sd:SensorData) REQUIRE sd.sensor_data_id IS UNIQUE")
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (pd:PerformanceData) REQUIRE pd.performance_id IS UNIQUE")
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (a:Anomaly) REQUIRE a.anomaly_id IS UNIQUE")
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:MaintenanceTask) REQUIRE t.task_id IS UNIQUE")
        s.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE")

    # Mapping (allow user override)
    m = cfg.get("mapping", {})

    def col(df, key, fallback):
        return m.get(key, fallback) if key in m else fallback

    # ---- Nodes: BuildingComponent
    if not assets_df.empty:
        cid = col(assets_df, "component_id", "ComponentId")
        cname = col(assets_df, "component_name", "Name")
        ctype = col(assets_df, "component_type", "Type")
        rows = []
        for _, r in assets_df.iterrows():
            comp_id = str(r.get(cid, "")).strip()
            if not comp_id:
                continue
            rows.append({
                "component_id": comp_id,
                "name": str(r.get(cname, "")),
                "type": str(r.get(ctype, "")),
            })
        neo.merge_nodes("BuildingComponent", "component_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "BuildingComponent", "count": len(rows)})

    # ---- Nodes: SensorData (raw sensor stream)
    if not sensor_df.empty:
        sid = col(sensor_df, "sensor_data_id", "SensorDataId")
        ts = col(sensor_df, "sensor_timestamp", "Timestamp")
        val = col(sensor_df, "sensor_value", "Value")
        sensor_id = col(sensor_df, "sensor_id", "SensorId")
        rows = []
        for i, r in sensor_df.iterrows():
            sdata_id = str(r.get(sid, f"sd_{i}")).strip()
            rows.append({
                "sensor_data_id": sdata_id,
                "sensor_id": str(r.get(sensor_id, "")),
                "timestamp": str(r.get(ts, "")),
                "value": r.get(val, None),
            })
        neo.merge_nodes("SensorData", "sensor_data_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "SensorData", "count": len(rows)})

    # ---- Nodes: PerformanceData (processed)
    if not perf_df.empty:
        pid = col(perf_df, "performance_id", "PerformanceId")
        ts = col(perf_df, "performance_timestamp", "Timestamp")
        metric = col(perf_df, "performance_metric", "Metric")
        val = col(perf_df, "performance_value", "Value")
        sensor_id = col(perf_df, "sensor_id", "SensorId")
        component_id = col(perf_df, "component_id", "ComponentId")
        rows = []
        for i, r in perf_df.iterrows():
            perf_id = str(r.get(pid, f"pd_{i}")).strip()
            rows.append({
                "performance_id": perf_id,
                "sensor_id": str(r.get(sensor_id, "")),
                "component_id": str(r.get(component_id, "")),
                "timestamp": str(r.get(ts, "")),
                "metric": str(r.get(metric, "")),
                "value": r.get(val, None),
            })
        neo.merge_nodes("PerformanceData", "performance_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "PerformanceData", "count": len(rows)})

    # ---- Nodes: Anomaly (optional seed from processed anomaly file)
    if not anom_df.empty:
        aid = col(anom_df, "anomaly_id", "AnomalyId")
        ts = col(anom_df, "anomaly_timestamp", "Timestamp")
        atype = col(anom_df, "anomaly_type", "Type")
        severity = col(anom_df, "anomaly_severity", "Severity")
        component_id = col(anom_df, "component_id", "ComponentId")
        rows = []
        for i, r in anom_df.iterrows():
            an_id = str(r.get(aid, f"a_{i}")).strip()
            rows.append({
                "anomaly_id": an_id,
                "timestamp": str(r.get(ts, "")),
                "type": str(r.get(atype, "")),
                "severity": str(r.get(severity, "")),
                "component_id": str(r.get(component_id, "")),
            })
        neo.merge_nodes("Anomaly", "anomaly_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "Anomaly", "count": len(rows)})

    # ---- Nodes: MaintenanceTask
    if not tasks_df.empty:
        tid = col(tasks_df, "task_id", "TaskId")
        ttype = col(tasks_df, "task_type", "TaskType")
        priority = col(tasks_df, "task_priority", "Priority")
        component_id = col(tasks_df, "component_id", "ComponentId")
        rows = []
        for i, r in tasks_df.iterrows():
            task_id = str(r.get(tid, f"t_{i}")).strip()
            rows.append({
                "task_id": task_id,
                "type": str(r.get(ttype, "")),
                "priority": str(r.get(priority, "")),
                "component_id": str(r.get(component_id, "")),
            })
        neo.merge_nodes("MaintenanceTask", "task_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "MaintenanceTask", "count": len(rows)})

    # ---- Nodes: Person (Actor)
    if not actors_df.empty:
        pid = col(actors_df, "person_id", "ActorId")
        name = col(actors_df, "person_name", "Name")
        role = col(actors_df, "person_role", "Role")
        rows = []
        for i, r in actors_df.iterrows():
            person_id = str(r.get(pid, f"p_{i}")).strip()
            rows.append({
                "person_id": person_id,
                "name": str(r.get(name, "")),
                "role": str(r.get(role, "")),
            })
        neo.merge_nodes("Person", "person_id", rows)
        logger.log_event("IMPORT_NODE", details={"label": "Person", "count": len(rows)})

    # ---- Relationships (edges CSV)
    # Edge_MAPS_SENSOR_DATA: (BuildingComponent)-[:MAPS_SENSOR_DATA]->(SensorData) or similar
    if not edge_maps_df.empty:
        src = col(edge_maps_df, "src_component_id", "ComponentId")
        tgt = col(edge_maps_df, "tgt_sensor_data_id", "SensorDataId")
        rel = col(edge_maps_df, "rel_type", "REL")
        rel_type = "MAPS_SENSOR_DATA"
        rows = []
        for _, r in edge_maps_df.iterrows():
            c_id = str(r.get(src, "")).strip()
            sd_id = str(r.get(tgt, "")).strip()
            if not c_id or not sd_id:
                continue
            rows.append((c_id, sd_id, rel_type))
        neo.merge_rels("BuildingComponent", "component_id", "SensorData", "sensor_data_id",
                       rows, rel_type=rel_type)
        logger.log_event("IMPORT_REL", details={"type": rel_type, "count": len(rows)})

    # Edge_GENERATES: (PerformanceData)-[:GENERATES]->(Anomaly) or (SensorData)->(PerformanceData)
    if not edge_gen_df.empty:
        src = col(edge_gen_df, "src_id", "SRC")
        tgt = col(edge_gen_df, "tgt_id", "TGT")
        rel_type = col(edge_gen_df, "rel_type", "GENERATES")
        rows = []
        for _, r in edge_gen_df.iterrows():
            s_id = str(r.get(src, "")).strip()
            t_id = str(r.get(tgt, "")).strip()
            if not s_id or not t_id:
                continue
            rows.append((s_id, t_id, rel_type))
        # We don't know labels; attempt common pattern: PerformanceData -> Anomaly
        neo.merge_rels("PerformanceData", "performance_id", "Anomaly", "anomaly_id",
                       [(a,b,rel_type) for a,b,_ in rows], rel_type=rel_type)
        logger.log_event("IMPORT_REL", details={"type": rel_type, "count": len(rows)})

    logger.log_event("DONE")
    logger.write_csv()
    print("ETL complete. Logs:", out_dir / logger.default_csv_name())

if __name__ == "__main__":
    main()
