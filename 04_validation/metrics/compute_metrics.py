#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_metrics.py

Compute PdM evaluation metrics for the SAM–STRIDE testbed (thesis scenario).

Input (default paths, relative to this script):
    ../../data/synthetic/pdm/thesis_iot.csv
    ../../data/synthetic/pdm/thesis_assets.csv
    ../../data/synthetic/pdm/thesis_workorders.csv

Output (CSV tables, relative to this script):
    ../../artifacts/tables/tta.csv
    ../../artifacts/tables/latency.csv
    ../../artifacts/tables/funnels.csv
    ../../artifacts/tables/portability.csv

Metrics:
    - TTA (Time-To-Action)
    - Latency breakdown (L1–L4)
    - Compensation funnel (exception → compensated → recovered)
    - Portability effort (config/setup effort per scenario)

Usage:
    python compute_metrics.py
    python compute_metrics.py --input-dir ../../data/synthetic/pdm \
                              --output-dir ../../artifacts/tables

Author: SAM–STRIDE Replication Package
"""

import argparse
import os
import sys
from typing import Tuple, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _log(msg: str):
    """Lightweight logger."""
    print(f"[compute_metrics] {msg}", file=sys.stderr)


def _ensure_dir(path: str):
    """Create directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def _parse_timestamp(df: pd.DataFrame, cols) -> pd.DataFrame:
    """
    Safely parse timestamp columns if they exist.
    `cols` can be a single column name or a list of names.
    """
    if isinstance(cols, str):
        cols = [cols]
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
        else:
            _log(f"WARNING: timestamp column '{c}' not found.")
    return df


# ---------------------------------------------------------------------------
# 1. TTA (Time-To-Action)
# ---------------------------------------------------------------------------

def compute_tta(
    wo_df: pd.DataFrame,
    output_path: str,
    trigger_col: str = "t_trigger",
    action_start_col: str = "t_action_start",
    mode_col: str = "mode",
    id_col: str = "workorder_id",
) -> pd.DataFrame:
    """
    Compute Time-To-Action per work order and export summary stats.

    Expected columns in thesis_workorders.csv:
        - t_trigger          : time when trigger was emitted
        - t_action_start     : time when action execution started
        - mode               : "baseline" or "sam"
        - workorder_id       : unique ID per work order

    Output table (tta.csv) columns:
        - mode
        - count
        - tta_mean_seconds
        - tta_median_seconds
        - tta_p90_seconds
        - tta_p95_seconds
    """
    # Check required columns
    required = [trigger_col, action_start_col]
    for c in required:
        if c not in wo_df.columns:
            _log(f"WARNING: Cannot compute TTA, missing column '{c}'.")
            return pd.DataFrame()

    # Parse timestamps
    wo_df = _parse_timestamp(wo_df, [trigger_col, action_start_col])

    # Compute TTA in seconds
    wo_df["TTA_seconds"] = (
        (wo_df[action_start_col] - wo_df[trigger_col])
        .dt.total_seconds()
        .astype("float")
    )

    # Drop rows with invalid/NaT
    before = len(wo_df)
    wo_df = wo_df.dropna(subset=["TTA_seconds"])
    _log(f"TTA: dropped {before - len(wo_df)} rows with invalid timestamps.")

    if mode_col not in wo_df.columns:
        _log(f"WARNING: mode column '{mode_col}' not found. "
             f"Using single group 'all'.")
        wo_df[mode_col] = "all"

    # Aggregate by mode
    def _p(series, q):
        return series.quantile(q) if not series.empty else None

    grouped = wo_df.groupby(mode_col)["TTA_seconds"]
    tta_summary = grouped.agg(
        count="count",
        tta_mean_seconds="mean",
        tta_median_seconds="median"
    ).reset_index()

    # add P90 and P95
    p90_list = []
    p95_list = []
    for mode, grp in wo_df.groupby(mode_col):
        p90_list.append((mode, _p(grp["TTA_seconds"], 0.90)))
        p95_list.append((mode, _p(grp["TTA_seconds"], 0.95)))

    p90_df = pd.DataFrame(p90_list, columns=[mode_col, "tta_p90_seconds"])
    p95_df = pd.DataFrame(p95_list, columns=[mode_col, "tta_p95_seconds"])

    tta_summary = (
        tta_summary.merge(p90_df, on=mode_col, how="left")
        .merge(p95_df, on=mode_col, how="left")
    )

    tta_summary.to_csv(output_path, index=False)
    _log(f"[TTA] Written summary to {output_path}")

    return tta_summary


# ---------------------------------------------------------------------------
# 2. Latency breakdown (L1–L4)
# ---------------------------------------------------------------------------

def compute_latency_breakdown(
    wo_df: pd.DataFrame,
    output_path: str,
    trigger_col: str = "t_trigger",
    detect_col: str = "t_detected",
    task_created_col: str = "t_task_created",
    action_start_col: str = "t_action_start",
    action_end_col: str = "t_action_end",
    mode_col: str = "mode",
) -> pd.DataFrame:
    """
    Compute latency decomposition into L1–L4.

    Interpretation (you can adapt to your exact thesis definition):
        - L1: Detection latency  = t_detected    - t_trigger
        - L2: Reasoning latency  = t_task_created - t_detected
        - L3: Dispatch latency   = t_action_start - t_task_created
        - L4: Execution latency  = t_action_end   - t_action_start

    Output table (latency.csv) columns:
        - mode
        - metric         (L1 / L2 / L3 / L4)
        - mean_seconds
        - median_seconds
        - p90_seconds
    """
    cols = [trigger_col, detect_col, task_created_col, action_start_col, action_end_col]
    missing = [c for c in cols if c not in wo_df.columns]
    if missing:
        _log("WARNING: Cannot compute latency breakdown. "
             f"Missing columns: {missing}")
        return pd.DataFrame()

    wo_df = _parse_timestamp(wo_df, cols)

    # Compute each latency in seconds
    wo_df["L1_seconds"] = (
        wo_df[detect_col] - wo_df[trigger_col]
    ).dt.total_seconds()
    wo_df["L2_seconds"] = (
        wo_df[task_created_col] - wo_df[detect_col]
    ).dt.total_seconds()
    wo_df["L3_seconds"] = (
        wo_df[action_start_col] - wo_df[task_created_col]
    ).dt.total_seconds()
    wo_df["L4_seconds"] = (
        wo_df[action_end_col] - wo_df[action_start_col]
    ).dt.total_seconds()

    # Drop rows with NaN in any latency
    latency_cols = ["L1_seconds", "L2_seconds", "L3_seconds", "L4_seconds"]
    before = len(wo_df)
    wo_df = wo_df.dropna(subset=latency_cols)
    _log(f"Latency: dropped {before - len(wo_df)} rows with invalid timestamps.")

    if mode_col not in wo_df.columns:
        _log(f"WARNING: mode column '{mode_col}' not found. "
             f"Using single group 'all'.")
        wo_df[mode_col] = "all"

    # Melt into long format: one row per latency type
    long_df = wo_df.melt(
        id_vars=[mode_col],
        value_vars=latency_cols,
        var_name="metric",
        value_name="seconds",
    )

    # Map metric names to L1–L4
    metric_map = {
        "L1_seconds": "L1_detection",
        "L2_seconds": "L2_reasoning",
        "L3_seconds": "L3_dispatch",
        "L4_seconds": "L4_execution",
    }
    long_df["metric"] = long_df["metric"].map(metric_map)

    def _p(series, q):
        return series.quantile(q) if not series.empty else None

    grouped = long_df.groupby([mode_col, "metric"])["seconds"]
    latency_summary = grouped.agg(
        mean_seconds="mean",
        median_seconds="median"
    ).reset_index()

    # add P90
    extra = []
    for (mode, metric), grp in long_df.groupby([mode_col, "metric"]):
        extra.append((mode, metric, _p(grp["seconds"], 0.90)))
    extra_df = pd.DataFrame(extra, columns=[mode_col, "metric", "p90_seconds"])

    latency_summary = latency_summary.merge(
        extra_df, on=[mode_col, "metric"], how="left"
    )

    latency_summary.to_csv(output_path, index=False)
    _log(f"[Latency] Written summary to {output_path}")

    return latency_summary


# ---------------------------------------------------------------------------
# 3. Compensation funnel (例外 → 補償 → 恢復)
# ---------------------------------------------------------------------------

def compute_compensation_funnel(
    wo_df: pd.DataFrame,
    output_path: str,
    status_col: str = "status",
    mode_col: str = "mode",
    exception_status: str = "EXCEPTION",
    compensated_status: str = "COMPENSATED",
    recovered_status: str = "RECOVERED",
) -> pd.DataFrame:
    """
    Compute compensation funnel statistics.

    Expected columns:
        - status : lifecycle status of the workorder
                   (e.g., EXCEPTION / COMPENSATED / RECOVERED / CLOSED)
        - mode   : baseline / sam

    Output table (funnels.csv) columns:
        - mode
        - stage           ("exception", "compensated", "recovered")
        - count
        - rate_from_prev  (relative rate from previous stage)
    """
    if status_col not in wo_df.columns:
        _log(f"WARNING: Cannot compute funnels, missing status column '{status_col}'.")
        return pd.DataFrame()

    if mode_col not in wo_df.columns:
        _log(f"WARNING: mode column '{mode_col}' not found. Using 'all'.")
        wo_df[mode_col] = "all"

    stages = [
        ("exception", exception_status),
        ("compensated", compensated_status),
        ("recovered", recovered_status),
    ]

    rows = []
    for mode, grp in wo_df.groupby(mode_col):
        counts = {}
        for stage_name, status_value in stages:
            counts[stage_name] = (grp[status_col] == status_value).sum()

        # compute funnel rates
        # exception is base
        base = counts["exception"]
        comp = counts["compensated"]
        recv = counts["recovered"]

        rows.append(
            {
                "mode": mode,
                "stage": "exception",
                "count": base,
                "rate_from_prev": 1.0 if base > 0 else None,
            }
        )
        rows.append(
            {
                "mode": mode,
                "stage": "compensated",
                "count": comp,
                "rate_from_prev": comp / base if base > 0 else None,
            }
        )
        rows.append(
            {
                "mode": mode,
                "stage": "recovered",
                "count": recv,
                "rate_from_prev": recv / comp if comp > 0 else None,
            }
        )

    funnel_df = pd.DataFrame(rows)
    funnel_df.to_csv(output_path, index=_
