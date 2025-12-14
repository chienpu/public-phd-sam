# Carbon_SIDCM Traceability Validation

本目錄用於驗證 **Carbon_SIDCM（校園建築 × 營運用電 × 營運碳）** 情境下，
語意整合後之資料是否具備 **可追溯性（Traceability）** 與 **語意完整性（Semantic Completeness）**。
本驗證流程對應論文第六章之 Carbon 案例分析，並與 PdM 案例採用一致的方法論。

---

## 1. 驗證目標（Validation Objectives）

Carbon_SIDCM 案例的可追溯性驗證重點如下：

1. **語意鏈完整性**  
   驗證是否存在完整的語意因果鏈：  
   `Building → EnergyFlow → EmissionRecord`

2. **時間粒度一致性**  
   確保所有 EnergyFlow 與 EmissionRecord 皆以  
   **建築 × 月份（YYYY-MM）** 為基本分析單位。

3. **資料品質與斷鏈偵測**  
   檢查是否存在缺乏上游或下游關聯的孤立節點（orphan nodes）。

4. **可視化與可解釋性**  
   提供可視化路徑，以支援論文中對語意推理與碳資料來源的說明。

---

## 2. 使用檔案說明

### 2.1 Cypher 查詢腳本

- **`traceability_check_Carbon_SIDCM.cypher`**  
  Carbon_SIDCM 專用的可追溯性查詢腳本，涵蓋：
  - Schema 檢查（labels / relationships）
  - 語意鏈驗證（Building → Energy → Carbon）
  - 斷鏈節點偵測
  - 月份覆蓋率檢查
  - 路徑視覺化輸出

---

## 3. 驗證流程（Validation Procedure）

1. 將以下 CSV 載入 Neo4j：

```
02_data/Carbon_SIDCM/raw/
├─ Carbon_Component_BoQ_demo.csv
└─ Carbon_Energy_Use_demo.csv

02_data/Carbon_SIDCM/processed/
├─ SIDCM_Graph_Nodes_demo.csv
└─ SIDCM_Graph_Relationships_demo.csv
```

2. 開啟 Neo4j Browser 或 Neo4j Bloom。

3. 執行 `traceability_check_Carbon_SIDCM.cypher`。

4. 依序檢視各 Section 的輸出結果。

---

## 4. 驗證結果解讀（Result Interpretation）

### 4.1 語意鏈存在

若查詢結果顯示：

```
(Building)-[:CONSUMES_ENERGY]->(EnergyFlow)-[:GENERATES_EMISSION]->(EmissionRecord)
```

表示 Carbon_SIDCM 案例中，營運碳資料具備完整且可解釋的語意來源。

### 4.2 斷鏈節點

- 若無回傳 orphan nodes，表示資料語意結構完整。
- 若存在 orphan nodes，可用於說明資料缺漏或實務限制，
  作為未來研究與系統改善之依據。

### 4.3 月份覆蓋率

月份統計結果可用於驗證：
- 時間序列是否連續
- 是否存在缺失月份或異常資料

---

## 5. 與論文第六章之對應

本驗證內容對應論文第六章：

- **Carbon_SIDCM 案例分析**
- **語意整合後之可追溯性驗證**
- **與 PdM 案例之跨領域一致性比較**

Carbon 案例與 PdM 案例皆採用相同的語意行動管理（SAM）與
SID-CM 推理邏輯，證明本研究方法在不同應用情境下的可重用性與一致性。

---

## 6. 小結

本目錄所提供之驗證流程顯示，
即使在不同於設備維護的碳管理情境中，
語意驅動的資料整合與可追溯性驗證仍可維持一致的結構與推理邏輯。
此結果支持本研究所提出之方法具備跨領域擴展潛力。

