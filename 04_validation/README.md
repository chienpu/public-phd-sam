
# 04_validation— STRIDE/SAM 評估與結果重現工具

本資料夾提供 語意行動管理（SAM）/ STRIDE 框架的所有驗證方法、指標量測腳本、查詢範例、與實驗結果格式。
目的在於重現論文第 6 章的四大評估面向：
1. Semantic–Action Validation（語意–行動驗證）
2. Event-Driven Architecture (EDA) Performance（事件驅動效能）
3. Traceability & Governance（可追溯性與治理）
4. Scalability（可擴展性與多跳查詢效率）
   
所有工具均以 **可重現（Reproducible）** 為優先設計，並與 02_data/、03_execution/ 的資料格式、推理腳本與工作流事件日誌完全對應。

## 📁 資料夾結構

```text
04_validation/
├─ metrics/
│   ├─ formulas.md                 ← 所有指標的定義與 LaTeX 公式（與論文對應）
│   ├─ compute_metrics.py          ← 自動計算全指標（TTA, latency…）
│   └─ mapping_to_chapter6.md      ← 指標如何對應論文第六章
│
├─ traceability/
│   ├─ traceability_check.cypher   ← 可追溯性驗證查詢
│   ├─ traceability_explain.cypher ← 展開責任鏈（PROV-Chain）
│   └─ examples/                   ← 產生供論文繪圖的圖譜截圖資料
│
├─ performance/
│   ├─ query_performance.cypher    ← 多跳查詢與 scalability 測試
│   ├─ stress_test_cypher.md       ← 壓力測試說明（提升節點/邊數）
│   └─ throughput_measurement.md   ← 吞吐量與事件流量壓測流程
│
├─ workflow_logs/
│   ├─ workflow_events_schema.md   ← 工作流日誌欄位定義（TTA/補償流程所需）
│   ├─ sample_workflow_log.csv     ← 範例（可直接跑指標）
│   └─ compensation_log.csv        ← 補償命中率實驗用
│
├─ RESULTS/
│   ├─ tta_log.csv                 ← 由 compute_metrics.py 產生
│   ├─ latency_results.csv         ← query 性能測試結果
│   ├─ traceability_report.md      ← 自動摘要（可直接貼到論文）
│   ├─ compensation_rate.csv       ← 補償命中率結果
│   └─ summary_statistics.md       ← 全面統計摘要
│
└─ README.md                       ← 本文件
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
