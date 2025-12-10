
# 03_execution

本資料夾包含 **ETL、推理、工作流觸發等核心執行腳本**，對應於論文中 STRIDE 框架的 Semantic / Traversal / Workflow 部分。  

## 結構

```text
03_execution/
├─ data_ingestion_etl.py
├─ anomaly_detection_logic.py
├─ workflow_trigger_api.py
├─ shacl_validation.py
├─ utils/
│  ├─ config_loader.py
│  ├─ logger.py
│  └─ neo4j_helper.py
└─ README.md
```

## 主要腳本說明

### `data_ingestion_etl.py`

- 功能：  
  - 讀取 `02_data/` 內之輸入檔案（例如 `PdM_HVAC` 資料集）  
  - 進行欄位檢查（如 GlobalId 一致性）  
  - 將資料以語義化方式寫入 Neo4j（建立節點與關係）  

- 範例執行：  

```bash
python 03_execution/data_ingestion_etl.py --config config/pdm_demo.yaml
```

### `anomaly_detection_logic.py`

- 功能：  
  - 根據語義圖譜中的感測數值與設備特性，執行複合條件異常偵測  
  - 建立 `Anomaly` 節點，並與 `Sensor`、`BuildingComponent` 相連結  
  - 實作 TIAA 模式中的 Trigger + Issue 兩個面向  

- 範例執行：  

```bash
python 03_execution/anomaly_detection_logic.py --demo ahu12
```

### `workflow_trigger_api.py`

- 功能：  
  - 針對偵測到的 `Anomaly` 節點，發送 payload 至外部工作流平台（Power Automate / n8n）  
  - 記錄發送與回應時間，用以計算 TTA（Event → Action Latency）  
  - 實作 TIAA 模式中的 Action + Actor 兩個面向  

- 範例執行：  

```bash
python 03_execution/workflow_trigger_api.py --demo ahu12
```

### `shacl_validation.py`

- 功能：  
  - 對目前圖譜中的 ABox 進行 SHACL/規則驗證  
  - 檢查語義完整性與資料一致性（支持動態本體場景）  

---

## utils/

- `config_loader.py`：載入 YAML/JSON 格式之設定檔（資料路徑、Neo4j 連線資訊等）。  
- `logger.py`：統一日誌格式，用於實驗可重現之 log trace。  
- `neo4j_helper.py`：封裝 Neo4j driver 的基本操作（query、transaction、bulk write 等）。  
