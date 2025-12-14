#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils/config_loader.py

支援 YAML / JSON 設定檔載入，並提供最小的預設值合併（shallow merge）。

- YAML: requires PyYAML (yaml)
- JSON: built-in json

本工具用於提升 portability：同一套腳本可透過 config 切換 PdM / Carbon。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

def load_config(path: str) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config not found: {p}")

    if p.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except Exception as e:
            raise RuntimeError("PyYAML not installed. Run: pip install pyyaml") from e
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return dict(data)
    elif p.suffix.lower() == ".json":
        return json.loads(p.read_text(encoding="utf-8"))
    else:
        raise ValueError("Config must be .yaml/.yml or .json")
