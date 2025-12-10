
# 04_validation

本資料夾包含所有與 **效能、TTA、traceability、scalability** 相關的實驗與分析工具。  

## 結構

```text
04_validation/
├─ query_performance.cypher
├─ TTA_measurement_tool.py
├─ traceability_check.cypher
├─ notebooks/
│  └─ analysis.ipynb
├─ RESULTS/
│  ├─ latency_results.csv
│  ├─ tta_log.csv
│  ├─ traceability_graph.png
│  └─ summary_statistics.md
└─ README.md
```

## 主要內容

### `query_performance.cypher`

- 用於測試多跳圖遍歷的查詢效能，包括：  
  - 從 `Anomaly` 追溯至 `BuildingComponent`、`Space`、`Floor`、`Building` 等多層級結構  
  - 在不同圖規模（節點數、關係數）下，量測平均響應時間  

### `TTA_measurement_tool.py`

- 功能：  
  - 分析由 `workflow_trigger_api.py` 所產生的 log（包含請求與回應時間戳）  
  - 計算 event → action 的 latency（TTA）  
  - 匯出 `tta_log.csv` 與基本統計指標（平均值、分佈等）  

### `traceability_check.cypher`

- 功能：  
  - 驗證每一個 `MaintenanceTask` 是否能夠沿著圖譜追溯至對應 `Anomaly`、`Sensor`、`BuildingComponent`、`WorkflowRun` 等  
  - 產出可視化用資料（例如 `traceability_graph.*`）  

### `notebooks/analysis.ipynb`

- 以 Jupyter Notebook 彙整：  
  - TTA 統計圖表（分佈、箱型圖等）  
  - latency vs. graph size 的關係  
  - traceability completeness（百分比）  

---

## 如何重現論文中的指標

1. 執行 `03_execution/` 下的 ETL、推理與工作流觸發腳本  
2. 確認 `RESULTS/` 資料夾產生：  
   - `tta_log.csv`  
   - `latency_results.csv`  
3. 執行 `notebooks/analysis.ipynb` 以產生統計數據與圖像  
4. 將分析結果與論文中的表格與圖（Chapter 5）對照，即可完成重現  
