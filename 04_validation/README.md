
# 04_validation— STRIDE/SAM 評估指標、效能測試與重現工具 

本資料夾包含本研究 語意行動管理（SAM）與 STRIDE 框架 的完整實驗流程、效能測試、可追溯性驗證與所有指標（metrics）計算方法。
其目的在於：
1. 重現論文第 5 章（STRIDE 系統實作）之效能評估結果
2. 重現論文第 6 章（PdM 與 SID-CM 案例）之量化指標
3. 提供審稿委員與研究者可直接執行的驗證環境
4. 形成可審計、透明、可複製（Reproducible）的研究驗證流程

論文對應章節（需引用本目錄）：
 - Ch. 5 系統實作與效能驗證（5.3–5.5）
 - Ch. 6 案例驗證（所有指標）
 - Appendix C（Validation Scripts & Metrics）

## 📁 資料夾結構

```text
04_validation/
├─ formulas/                     ← 所有指標公式圖片（自動產生）
│   ├─ TTA_formula.png
│   ├─ Latency_formula.png
│   ├─ Throughput_formula.png
│   ├─ Loss_formula.png
│   ├─ Portability_formula.png
│   └─ Compensation_formula.png
│
├─ metrics/
│   ├─ formulas.md               ← 各項指標的定義、LaTeX、文獻依據
│   ├─ compute_metrics.py        ← 自動計算 TTA / Latency / Loss 等指標
│   └─ mapping_to_chapter6.md    ← 指標與論文第六章的對位
│
├─ traceability/
│   ├─ traceability_check.cypher ← PROV-Chain 可追溯性查詢
│   ├─ traceability_explain.cypher
│   └─ examples/                 ← 可視化圖譜輸出
│
├─ performance/
│   ├─ query_performance.cypher  ← scalability / traversal 測試
│   ├─ stress_test_cypher.md     ← 節點量增加測試
│   └─ throughput_measurement.md ← IoT 事件壓測流程
│
├─ workflow_logs/
│   ├─ workflow_events_schema.md ← TTA / 補償流程 Log 格式
│   ├─ sample_workflow_log.csv
│   └─ compensation_log.csv
│
├─ RESULTS/
│  ├─ TTA/
│  │  ├─ tta_distribution_pdm_baseline_vs_sam.csv
│  │  ├─ tta_summary_stats.csv
│  │  └─ README.md
│  │
│  ├─ Latency_Decomposition_L1_L4/
│  │  ├─ latency_l1_l4_raw.csv
│  │  ├─ latency_l1_l4_summary.csv
│  │  └─ README.md
│  │
│  ├─ Provenance_Replay/
│  │  ├─ provenance_replay_latency.csv
│  │  └─ README.md
│  │
│  ├─ Portability_Setup_Effort/
│  │  ├─ portability_setup_effort.csv
│  │  └─ README.md
│  │
│  ├─ Traceability_Coverage/
│  │  ├─ traceability_coverage.csv
│  │  └─ README.md
│  │
│  ├─ Compensation_Funnel/
│  │  ├─ compensation_funnel.csv
│  │  └─ README.md
│  │
│  ├─ Effective_Throughput/
│  │  ├── throughput_definition.md
│  │  ├── throughput_pdm_summary.csv
│  │  ├── throughput_chart.xlsx
│  │  ├── README.md
│  │
│  └─ Loss_Rate/
│     ├─ loss_rate.csv
│     └─ README.md
│
└─ README.md   ←（本檔案）

```

## 🔍 1. 驗證目的（Validation Objectives）

本研究針對 SAM/STRIDE 框架提出六大量化指標，分屬兩類：

### A. 語意–行動驗證（Semantic–Action Validation）

| 指標                               | 目的                      | 說明                        |
| -------------------------------- | ----------------------- | ------------------------- |
| **TTA（事件至行動延遲）**                 | 驗證語意推理 → 任務派送的即時性       | HVAC PdM 基準指標             |
| **Traceability（可追溯性）**           | 驗證語意行動能否回溯至事件、規則、角色     | PROV-Chain                |
| **Portability（可移植性）**            | 驗證框架能否跨 PdM 與 SID-CM 復用 | ontology 與 traversal 規則通用 |
| **Compensation Hit Rate（補償命中率）** | 驗證系統在異常／失敗時能否觸發補償流程     | BPMN compensation 模式      |

### B. 事件驅動效能（EDA Performance）

| 指標                  | 目的                                |
| ------------------- | --------------------------------- |
| **Latency（延遲）**     | 單一事件在 STRIDE → workflow 的處理時間     |
| **Throughput（吞吐量）** | 單位時間可處理之事件數                       |
| **Loss Rate（遺失率）**  | 事件於 IoT → Neo4j → Workflow 中的丟失比率 |

## 🧮 2. 指標定義（含圖片）
### 2.1 事件至行動延遲（TTA, Time-to-Action）
事件觸發到行動開始的時間差：

<img src="../04_validation/formulas/TTA_formula.png" width="220"/>
來源：CEP / EDA 反應時間衡量方法（Chandy 2016；Teymourian 2009）

### 2.2 延遲（Latency）
處理單一事件（IoT → 推理 → 工單派送）的端到端延遲：

<img src="../04_validation/formulas/Latency_formula.png" width="220"/>

### 2.3 吞吐量（Throughput）
單位時間內系統可處理的事件數（events/sec）：

<img src="../04_validation/formulas/Throughput_formula.png" width="220"/>

### 2.4 遺失率（Event Loss Rate）
事件流中遺失事件比例：

<img src="../04_validation/formulas/Loss_formula.png" width="220"/>

### 2.5 可移植性（Portability Score）
衡量 STRIDE 在不同場域（PdM、SID-CM）之間重部署的容易度：

<img src="../04_validation/formulas/Portability_formula.png" width="220"/>

### 2.6 補償命中率（Compensation Hit Rate）
異常或流程失敗時，系統是否成功啟動補償流程：

<img src="../04_validation/formulas/Compensation_formula.png" width="220"/>

## 🧪 3. 如何重現論文中的所有指標
### 步驟一：執行 ETL 與推理（03_execution）

使用以下腳本會：
 - 載入 PdM 與 SID-CM 圖資料
 - 執行 anomaly → task → provenance
 - 將工作流事件與 API 觸發記錄於 workflow_logs/

```bash
python 03_execution/run_all.py
```

### 步驟二：執行 compute_metrics.py（自動計算所有指標）

此工具會：
 - 計算 TTA（由 IoT event 與 workflow start 時間）
 - 產生 latency 統計
 - 計算 compensation hit rate
 - 對 traceability 進行 completeness 檢查
 - 依據公式產出所有結果 CSV

```bash
python 04_validation/metrics/compute_metrics.py
```

輸出於：
 - `RESULTS/tta_log.csv`
 - `RESULTS/latency_results.csv`
 - `RESULTS/compensation_rate.csv`
 - `RESULTS/summary_statistics.md`

### 步驟三：跑 Cypher 查詢以產生 traceability 結果
```bash
:load 04_validation/traceability/traceability_check.cypher
```

輸出於：
 - `RESULTS/traceability_report.md`
 - `traceability/examples/*.png`（可直接插入論文第六章）

### 步驟四：效能與 Scalability 測試
使用以下查詢：
```bash
:load 04_validation/performance/query_performance.cypher
```

可得到：
 - 多跳查詢時間（對應論文 Fig 5-12）
 - 圖規模 vs 查詢成本（對應 Scalability 討論段落）

## 📊 4. 試算結果與論文對位

見 metrics/mapping_to_chapter6.md，其中逐一對應：
 - Table 6-1：Semantic–Action Validation 指標
 - Table 6-2：EDA Performance 指標
 - Fig 6-3：TTA 分佈
 - Fig 6-4：補償命中率
 - Fig 6-5：Traceability Path results
 - Fig 6-8：Throughput under IoT load

## 📝 5. 引用方式（供論文使用）

若需在論文或報告中引用本模組，建議使用以下格式：

本研究之所有指標、公式、效能測試腳本與結果皆收錄於
**04_validation 模組**（屬於 STRIDE–SAM Reproducibility Repository）。

GitHub Repository：
https://github.com/chienpu/public-phd-sam

該模組包含：指標定義（含公式圖片）、Cypher 查詢、TTA 衡量工具、補償流程驗證、
多跳查詢性能測試與 Scalability 分析，可完整重現論文第 5–6 章之實驗流程。
