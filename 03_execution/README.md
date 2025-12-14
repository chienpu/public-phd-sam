# 03_execution — 執行層（ETL × 語意推理 × 工作流觸發）

本資料夾提供 **SAM–STRIDE 測試床的核心執行腳本**，涵蓋資料匯入（ETL）、圖上推理（Traversal/Rule Logic）、以及工作流觸發（Workflow API）。  
其目的在於讓讀者能以可重現方式重建論文中「Semantic → Traversal → Workflow → Provenance」的執行管線，並連結第六章之量化結果與驗證（`04_validation/`）。

> **案例適用性提醒（重要）**  
> - **PdM_HVAC**：屬於高頻事件／即時任務情境，會使用 **ETL + 異常偵測 + 工作流觸發 + 記錄**。  
> - **Carbon_SIDCM**：屬於低頻（建築×月份）批次整合情境，主要使用 **ETL + 語意一致性檢查 + 可追溯性查詢**，**不啟用**即時 TTA/工作流觸發腳本。  

---

## 資料夾結構

```text
03_execution/
├─ data_ingestion_etl.py          # 02_data → Neo4j（節點/關係）
├─ anomaly_detection_logic.py     # PdM：複合條件異常偵測（Trigger/Issue）
├─ workflow_trigger_api.py        # PdM：觸發外部工作流（Action/Actor）
├─ shacl_validation.py            # 語意一致性檢查（可選）
├─ utils/
│  ├─ config_loader.py            # YAML/JSON 設定載入
│  ├─ logger.py                   # 統一 log 與 trace 欄位
│  └─ neo4j_helper.py             # Neo4j driver 操作封裝
└─ README.md
```

---

## 方法論對齊（對應 SAM / TIAA / STRIDE）

本資料夾各腳本與論文方法之對應關係如下（建議用於第六章引用）：

| Script | STRIDE 層級 | TIAA 角色 | 主要輸入 | 主要輸出 |
|---|---|---|---|---|
| `data_ingestion_etl.py` | Semantic | （前置） | `02_data/*/raw`、`processed` | Neo4j nodes/edges、匯入 log |
| `anomaly_detection_logic.py` | Traversal | Trigger + Issue | Neo4j（Sensor/Performance/Anomaly 規則） | `Anomaly`、`Issue` 節點/關係、偵測 log |
| `workflow_trigger_api.py` | Workflow | Action + Actor | Neo4j（待處理任務/異常） | 外部 workflow payload、回應 log、TTA timestamp |
| `shacl_validation.py` | Semantic Guardrail | （一致性） | Neo4j 匯入後的 ABox | 驗證報告（pass/fail、violations） |

---

## 快速開始（建議 reviewer / 委員使用）

### 0) 前置條件
- Python 3.10+
- Neo4j 5.x（建議與論文一致版本）
- 已完成 `02_data/` 的資料準備與檔名結構（PdM_HVAC、Carbon_SIDCM）

### 1) 設定檔（Config）
本資料夾支援使用 YAML/JSON 設定檔控制：
- Neo4j 連線（uri/user/password/db）
- 資料路徑（PdM 或 Carbon）
- 匯入模式（overwrite / append）
- demo 參數（例如 AHU12）

> 若你尚未建立設定檔，可先建立：
- `config/pdm_demo.yaml`
- `config/carbon_demo.yaml`

### 2) 匯入資料到 Neo4j（PdM / Carbon 共用）
```bash
python 03_execution/data_ingestion_etl.py --config config/pdm_demo.yaml
# or
python 03_execution/data_ingestion_etl.py --config config/carbon_demo.yaml
```

### 3) PdM：執行異常偵測與工作流觸發（僅 PdM）
```bash
python 03_execution/anomaly_detection_logic.py --config config/pdm_demo.yaml --demo ahu12
python 03_execution/workflow_trigger_api.py --config config/pdm_demo.yaml --demo ahu12
```

### 4)（可選）語意一致性檢查
```bash
python 03_execution/shacl_validation.py --config config/pdm_demo.yaml
```

---

## 與第六章與 `04_validation/` 的對應

- **TTA / Latency / Funnel（PdM）**：依賴 `workflow_trigger_api.py` 所產生的時間戳與 log，後續由 `04_validation/metrics/compute_metrics.py` 彙整成 `tta.csv / latency.csv / funnels.csv`。  
- **Traceability（PdM + Carbon）**：匯入後以 `04_validation/traceability/*.cypher` 驗證語意鏈：  
  - PdM：SensorEvent → Anomaly/Issue → MaintenanceTask（示意）  
  - Carbon：Building → EnergyFlow → EmissionRecord  
- **Portability（PdM + Carbon）**：設定檔與匯入／規則調整步驟由 `04_validation/metrics` 匯總（`portability.csv`）。

---

## 日誌與輸出（建議格式）

為支援可重現性，建議所有腳本在執行時輸出：
- `run_id`（一次執行的唯一識別）
- `scenario`（PdM_HVAC / Carbon_SIDCM）
- `mode`（baseline / sam）
- `t_trigger / t_detected / t_task_created / t_action_start / t_action_end`（若適用）
- `neo4j_db`、`input_hash`（可選，用於證明輸入版本）

---

## 常見問題（FAQ）

**Q1：Carbon_SIDCM 為何不計算 TTA / Latency L1–L4？**  
A：Carbon_SIDCM 為低頻批次整合情境，主要評估可追溯性與可移植性；即時事件驅動指標（TTA、L1–L4）僅適用於 PdM。此差異已於第六章指標摘要與 6.6 跨案例綜合中說明。

**Q2：我沒有 Power Automate / n8n，也能重現嗎？**  
A：可以。你可在 `workflow_trigger_api.py` 使用 mock endpoint 或本地測試伺服器，以產生一致的 payload 與時間戳，仍可輸出可計算之 log。

---

## 建議引用方式（論文內）
本資料夾對應論文 STRIDE 框架之執行層（Execution Layer），包含 ETL、Traversal 推理與 Workflow 觸發；其輸出 log 與 Neo4j 圖譜查詢支援第六章之 TTA、Traceability、Portability 與 Compensation 等指標量測與驗證。


- `config_loader.py`：載入 YAML/JSON 格式之設定檔（資料路徑、Neo4j 連線資訊等）。  
- `logger.py`：統一日誌格式，用於實驗可重現之 log trace。  
- `neo4j_helper.py`：封裝 Neo4j driver 的基本操作（query、transaction、bulk write 等）。  

