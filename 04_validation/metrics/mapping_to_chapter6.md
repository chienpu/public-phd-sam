# 第六章評估指標與本資料庫（04_validation）對位說明

本文件建立論文第六章（Chapter 6）所有評估指標與本 GitHub 重建套件（replication package）之間的**一對一映射關係**，確保研究結果具備可重現性（reproducibility），並協助審稿者、研究者或學生依據本套件獨立重建實驗。

---

## 1. 指標與檔案對位總表

| 指標名稱 | 輸出檔案（Repo） | 原始資料來源 | 計算程式 | 論文章節 | 相關圖表 |
|----------|-------------------|--------------|-----------|-----------|----------|
| **TTA — 行動啟動時間（Time-To-Action）** | `tta.csv` | `thesis_workorders.csv` | `compute_metrics.py` | §6.5 結果與分析 | 圖 6.1（TTA 分佈） |
| **四階延遲分解（L1–L4）** | `latency.csv` | `thesis_workorders.csv` | `compute_metrics.py` | §6.5 | 圖 6.2（延遲分解） |
| **補償漏斗（Compensation Funnel）** | `funnels.csv` | `compensation_log.csv` 或 workorders 的 status 欄 | `compute_metrics.py` | §6.5 | 圖 6.5 |
| **可攜性（Portability）設定成本** | `portability.csv` | `portability_input.csv` | `compute_metrics.py` | §6.5 | 圖 6.4 |
| **可追溯性（Traceability）涵蓋與 replay 延遲** | `traceability_report.md` | Neo4j PROV 圖譜資料 | `traceability_check.cypher` | §6.5、§6.6 | 圖 6.3 |
| **事件吞吐量（Throughput）與遺失率（Loss）** | `summary_statistics.md` | workflow logs | `workflow_logs/*.csv` | §6.5 | 圖 6.6（Consumer Lag / Throughput） |

---

## 2. 指標對論文章節之詳細映射

### **2.1 TTA（行動啟動時間）**
- **定義：**  
  <img src="../formulas/TTA_formula.png" width="220"/>

- **原始資料來源：**  
  `02_data/synthetic/pdm/thesis_workorders.csv`

- **計算程式：**  
  `04_validation/metrics/compute_metrics.py`

- **輸出結果：**  
  `artifacts/tables/tta.csv`

- **論文對應：**  
  - 第六章 §6.5  
  - 圖 6.1：TTA 成效比較（Baseline vs SAM）  
  - 相關統計量（平均、P90、P95）來自 tta.csv  

---

### **2.2 四階延遲（Latency L1–L4）**

| 階段 | 公式 | 說明 |
|------|------|------|
| **L1：偵測延遲** | detected_time - trigger_time | IoT 事件 → 系統偵測 |
| **L2：語意推理延遲** | task_created_time - detected_time | Traversal / TIAA 推理時間 |
| **L3：派發延遲** | action_start_time - task_created_time | Workflow / API 任務派發 |
| **L4：執行延遲** | action_end_time - action_start_time | 實際行動執行 |


- **輸入資料：**  
  `thesis_workorders.csv`

- **輸出資料：**  
  `latency.csv`

- **論文位置：**  
  - 第六章 §6.5  
  - 圖 6.2：四階延遲堆疊圖（Baseline vs SAM）

---

### **2.3 補償漏斗（Exception → Compensation → Recovery）**

- **三階段：**
  1. Exception  
  2. Compensated  
  3. Recovered  

- **輸入資料來源：**  
  - `04_validation/workflow_logs/compensation_log.csv`  
  - 或 `thesis_workorders.csv` 的 `status` 欄位  

- **輸出：**  
  `funnels.csv`

- **論文位置：**  
  - 第六章 §6.5  
  - 圖 6.5：補償漏斗比較  

---

### **2.4 可攜性（Portability）— 跨系統部署成本**

- **資料來源：**  
  `04_validation/metrics/portability_input.csv`

- **輸出：**  
  `portability.csv`

- **論文位置：**  
  - 第六章 §6.5  
  - 圖 6.4：部署步驟數比較（或設定工作量比較）  

---

### **2.5 可追溯性（Traceability）**

- **資料來源：** Neo4j 圖資料庫  
- **執行腳本：**  
  - `traceability_check.cypher`  
  - `traceability_explain.cypher`  
- **輸出：**  
  `traceability_report.md`  
- **論文位置：**  
  - 第六章 §6.5、§6.6  
  - 圖 6.3：Provenance Replay Latency  

---

### **2.6 Throughput 與 Loss（事件處理效率）**

- **資料來源：**  
  - `workflow_logs/sample_workflow_log.csv`  
  - `workflow_logs/compensation_log.csv`

- **輸出：**  
  `summary_statistics.md`

- **論文對應：**  
  - 第六章 §6.5  
  - 圖 6.6：Throughput、Consumer Lag、Loss 分析  

---

## 3. 重建實驗流程（Reproduction Steps）

| 重建項目 | 執行方式 | 產出結果 |
|----------|----------|-----------|
| 計算所有指標 | `python compute_metrics.py` | tta.csv、latency.csv、funnels.csv、portability.csv |
| 驗證 TIAA → PROV-O 可追溯鏈 | 在 Neo4j 執行 `.cypher` | traceability_report.md |
| 重建 Workflow-based throughput | 放置 workflow logs | summary_statistics.md |
| scalability 測試 | 執行 performance 目錄內腳本 | scalability report |

---

## 4. 審稿者補充說明
- 所有結果均可從 raw CSV 自動計算得出  
- 本資料夾提供完整、透明、可重建之驗證流程  
- 第六章所有圖表均可由本資料夾內容重建  

---


