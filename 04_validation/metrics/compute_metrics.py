#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
compute_metrics.py
-------------------
自動計算以下指標：
1. TTA (Time-to-Action)
2. Latency (Workflow latency)
3. Throughput (events per second)
4. Loss Rate
5. Compensation Hit Rate
6. Portability 指標（僅紀錄成功案例數）

輸入資料來源：
 - 02_data/PdM_HVAC/processed/Performance_Data_300.csv
 - 04_validation/workflow_logs/sample_workflow_log.csv
 - 04_validation/workflow_logs/compensation_log.csv

輸出結果：
 - 04_validation/RESULTS/tta_log.csv
 - 04_validation/RESULTS/latency_results.csv
 - 04_validation/RESULTS/compensation_rate.csv
 - 04_validation/RESULTS/summary_statistics.md
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


# ==========================================================
# 路徑設定
# ==========================================================

BASE = "../../"   # relative to metrics/
PD_PATH = BASE + "02_data/PdM_HVAC/processed/Performance_Data_300.csv"
WORKFLOW_LOG = BASE + "04_validation/workflow_logs/sample_workflow_log.csv"
COMP_LOG = BASE + "04_validation/workflow_logs/compensation_log.csv"

RESULT_DIR = BASE + "04_validation/RESULTS/"
os.makedirs(RESULT_DIR, exist_ok=True)


# ==========================================================
# 輔助函式
# ==========================================================

def to_dt(x):
    """轉換為 datetime，遇到錯誤回傳 NaT"""
    try:
        return pd.to_datetime(x)
    except:
        return pd.NaT


# ==========================================================
# 載入資料
# ==========================================================

print("讀取 Performance Data...")
pd_df = pd.read_csv(PD_PATH)

print("讀取 workflow event log...")
wf_df = pd.read_csv(WORKFLOW_LOG)

print("讀取 compensation log...")
comp_df = pd.read_csv(COMP_LOG)


# ==========================================================
# 1. TTA 計算
# ==========================================================
print("計算 TTA ...")

wf_df["trigger_time"] = wf_df["trigger_time"].apply(to_dt)
wf_df["action_start"] = wf_df["action_start"].apply(to_dt)

wf_df["TTA_sec"] = (wf_df["action_start"] - wf_df["trigger_time"]).dt.total_seconds()

tta_df = wf_df[["event_id", "trigger_time", "action_start", "TTA_sec"]]
tta_df.to_csv(RESULT_DIR + "tta_log.csv", index=False)


# ==========================================================
# 2. Latency 計算（工作流自身延遲）
# ==========================================================
print("計算 Latency ...")

wf_df["workflow_end"] = wf_df["workflow_end"].apply(to_dt)
wf_df["latency_sec"] = (wf_df["workflow_end"] - wf_df["action_start"]).dt.total_seconds()

latency_df = wf_df[["event_id", "action_start", "workflow_end", "latency_sec"]]
latency_df.to_csv(RESULT_DIR + "latency_results.csv", index=False)


# ==========================================================
# 3. Throughput 計算（每秒事件數）
# ==========================================================
print("計算 Throughput ...")

if len(wf_df) > 1:
    duration = (wf_df["trigger_time"].max() - wf_df["trigger_time"].min()).total_seconds()
    throughput = len(wf_df) / duration if duration > 0 else np.nan
else:
    throughput = np.nan

# ==========================================================
# 4. Loss Rate = (事件輸入 - 成功處理) / 輸入
# ==========================================================
print("計算 Loss Rate ...")

input_events = pd_df["event_id"].nunique()
processed_events = wf_df["event_id"].nunique()

loss_rate = (input_events - processed_events) / input_events if input_events > 0 else np.nan


# ==========================================================
# 5. 補償命中率（Compensation Hit Rate）
# ==========================================================
print("計算補償命中率 ...")

if len(comp_df) > 0:
    comp_df["is_correct"] = comp_df["expected"] == comp_df["actual"]
    compensation_rate = comp_df["is_correct"].mean()
else:
    compensation_rate = np.nan


# ==========================================================
# 6. 可移植性（Portability）— 以成功執行的場景數表示
# ==========================================================
portability_score = 1  # 基於你的設定：PdM + SID-CM 均可重用 → 設為 1


# ==========================================================
# 輸出 summary
# ==========================================================
print("輸出 summary_statistics.md ...")

summary = f"""
# 效能指標統計摘要（compute_metrics.py 自動產生）

## 1. 事件至行動延遲（TTA）
- 平均 TTA：{tta_df["TTA_sec"].mean():.4f} 秒
- 中位數：{tta_df["TTA_sec"].median():.4f} 秒
- 標準差：{tta_df["TTA_sec"].std():.4f} 秒

---

## 2. Latency（工作流延遲）
- 平均 latency：{latency_df["latency_sec"].mean():.4f} 秒
- 中位數：{latency_df["latency_sec"].median():.4f} 秒

---

## 3. Throughput（吞吐量）
- 事件吞吐量：{throughput:.4f} events/sec

---

## 4. Loss Rate（遺失率）
- 輸入事件數：{input_events}
- 成功處理事件數：{processed_events}
- 遺失率：{loss_rate:.4f}

---

## 5. 補償命中率（Compensation Hit Rate）
- 補償命中率：{compensation_rate:.4f}

---

## 6. 可移植性（Portability）
- 跨案例成功重部署數：{portability_score}

"""

with open(RESULT_DIR + "summary_statistics.md", "w", encoding="utf-8") as f:
    f.write(summary)

print("🎉 compute_metrics.py 完成！")
print("結果已輸出至 04_validation/RESULTS/")

