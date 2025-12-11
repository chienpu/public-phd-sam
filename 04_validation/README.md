
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

## 1. 評估目的與對應論文章節

| 評估項目                             | 論文章節      | 本資料夾提供                            |
| -------------------------------- | --------- | --------------------------------- |
| **事件至行動延遲（TTA）**                 | Ch. 6.2.1 | compute_metrics.py、workflow_logs/ |
| **可追溯性（Traceability）**           | Ch. 6.2.2 | traceability_check.cypher         |
| **可移植性（Portability）**            | Ch. 6.2.3 | 由 PdM/SID-CM 兩案例資料驗證              |
| **補償命中率（Compensation Hit Rate）** | Ch. 6.2.4 | compensation_log.csv              |
| **Latency / Throughput**         | Ch. 6.3   | query_performance.cypher          |
| **多跳查詢效率（Scalability）**          | Ch. 6.4   | scalability 測試說明                  |

## 2. 指標定義（摘要）

完整的 LaTeX 公式請見 metrics/formulas.md。

$$
\mathrm{TTA} = t\_{\text{action\_start}} - t\_{\text{trigger\_emit}}
$$
