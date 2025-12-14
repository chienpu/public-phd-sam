#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
compute_metrics.py

Unified evaluation metrics for SAM–STRIDE testbed
supporting both PdM and Carbon_SIDCM scenarios.

Scenarios:
- PdM_HVAC        : event-driven (TTA, Latency, Funnel, Portability)
- Carbon_SIDCM    : data-integration-driven (Portability only)

Author: SAM–STRIDE Replication Package
"""

import argparse
import os
import sys
import pandas as pd


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def _log(msg: str):
    print(f"[compute_metrics] {msg}", file=sys.stderr)


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# Portability (PdM + Carbon 共用)
# ---------------------------------------------------------------------------

def compute_portability(
    portability_df: pd.DataFrame,
    output_path: str,
):
    """
    Compute portability effort for each scenario.

    Expected columns:
        - scenario : PdM_HVAC / Carbon_SIDCM
        - mode     : baseline / sam
        - effort   : numeric effort score (e.g., setup steps)
        - unit     : steps / hours / rules

    Output (portability.csv):
        - scenario
        - mode
        - effort
        - unit
    """
    required = ["scenario", "mode", "effort", "unit"]
    missing = [c for c in required if c not in portability_df.columns]
    if missing:
        _log(f"WARNING: missing columns for portability: {missing}")
        return pd.DataFrame()

    portability_df = portability_df.copy()
    portability_df.to_csv(output_path, index=False)
    _log(f"[Portability] Written to {output_path}")

    return portability_df


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--portability",
        default="../../data/portability/portability_input.csv",
        help="CSV defining setup effort for PdM and Carbon scenarios",
    )
    parser.add_argument(
        "--output-dir",
        default="../../artifacts/tables",
        help="Directory to write metric tables",
    )
    args = parser.parse_args()

    _ensure_dir(args.output_dir)

    # ------------------------------------------------------------
    # Portability (shared)
    # ------------------------------------------------------------
    if os.path.exists(args.portability):
        portability_df = pd.read_csv(args.portability)
        compute_portability(
            portability_df,
            os.path.join(args.output_dir, "portability.csv"),
        )
    else:
        _log("Portability input not found. Skipping.")


if __name__ == "__main__":
    main()
