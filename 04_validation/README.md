
# 04_validation— STRIDE/SAM 評估與結果重現工具

本資料夾提供 語意行動管理（SAM）/ STRIDE 框架的所有驗證方法、指標量測腳本、查詢範例、與實驗結果格式。
目的在於重現論文第 6 章的四大評估面向：
1. Semantic–Action Validation（語意–行動驗證）
2. Event-Driven Architecture (EDA) Performance（事件驅動效能）
3. Traceability & Governance（可追溯性與治理）
4. Scalability（可擴展性與多跳查詢效率）
所有工具均以 **可重現（Reproducible）** 為優先設計，並與 02_data/、03_execution/ 的資料格式、推理腳本與工作流事件日誌完全對應。

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
