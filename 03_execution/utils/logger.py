#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils/logger.py

統一輸出「可重現」的執行 log（CSV）。
- 每個事件一列
- 包含 run_id / scenario / mode / component / event_name / timestamp / details(json)

此 log 可用於：
- 第六章指標（TTA / latency）之 timestamp 證據
- GitHub replication 的 trace
"""
from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class RunLogger:
    out_dir: str
    scenario: str
    mode: str
    component: str
    run_id: str = field(default_factory=lambda: f"run_{uuid.uuid4().hex[:10]}")
    rows: List[Dict[str, Any]] = field(default_factory=list)

    def log_event(self, name: str, level: str = "INFO", details: Optional[Dict[str, Any]] = None):
        self.rows.append({
            "run_id": self.run_id,
            "scenario": self.scenario,
            "mode": self.mode,
            "component": self.component,
            "event": name,
            "level": level,
            "timestamp": utc_now_iso(),
            "details": json.dumps(details or {}, ensure_ascii=False),
        })

    def default_csv_name(self) -> str:
        return f"{self.component}_{self.run_id}.csv"

    def write_csv(self, filename: Optional[str] = None):
        out = Path(self.out_dir)
        out.mkdir(parents=True, exist_ok=True)
        fn = filename or self.default_csv_name()
        pd.DataFrame(self.rows).to_csv(out / fn, index=False, encoding="utf-8-sig")
        return str(out / fn)
