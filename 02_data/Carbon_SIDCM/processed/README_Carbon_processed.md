# Carbon_SIDCM 語意整合後資料說明（README_Carbon_processed.md）

本資料夾包含經 **SID-CM（Semantic Integration and Digitization for Carbon Management）** 方法處理後的語意化資料，已轉換為可直接匯入圖資料庫（如 Neo4j）的結構。

此層資料為論文中「語意整合成果」與「可追溯決策支援」之核心依據。

---

## 1. processed 資料層角色

- 將原始碳資料轉換為 **語意節點（Nodes）與語意關係（Relationships）**
- 提供跨資料來源的一致語意模型
- 支援後續的 traceability 與 portability 驗證

---

## 2. 檔案列表與說明

### 2.1 SIDCM_Graph_Nodes_demo.csv
**用途**：定義所有語意節點（Graph Nodes）

**常見節點類型**：
- BuildingComponent
- Material
- EnergyFlow
- EmissionRecord
- Actor / Organization

**代表性欄位**：
| 欄位名稱 | 說明 |
|--------|------|
| node_id | 節點唯一識別碼 |
| node_type | 節點語意類型 |
| name | 節點名稱 |
| attributes | 補充屬性（JSON 或 key-value） |

---

### 2.2 SIDCM_Graph_Relationships_demo.csv
**用途**：定義節點間的語意關係（Graph Relationships）

**常見關係類型**：
- COMPONENT_USES_MATERIAL
- MATERIAL_HAS_EMISSION_FACTOR
- COMPONENT_CONSUMES_ENERGY
- EMISSION_CALCULATED_FROM
- ACTOR_RESPONSIBLE_FOR

**代表性欄位**：
| 欄位名稱 | 說明 |
|--------|------|
| source_id | 起始節點 ID |
| target_id | 目標節點 ID |
| relationship_type | 關係語意 |
| attributes | 關係屬性（如計算方式、版本） |

---

## 3. 語意整合重點

- 明確區分 **資料實體（Entity）** 與 **計算活動（Activity）**
- 支援 PROV-O 的 used / wasGeneratedBy / wasAssociatedWith 關係
- 可跨材料、構件與能耗資料進行推理與查詢

---

## 4. 與 Baseline 流程之差異

| 面向 | Baseline（raw） | SID-CM（processed） |
|----|----------------|---------------------|
| 資料結構 | 表格式、分散 | 圖結構、語意化 |
| 整合方式 | 人工 / 腳本 | 語意模型驅動 |
| 可追溯性 | 幾乎無 | 完整 PROV-O |
| 可重用性 | 低 | 高 |

---

## 5. 與 04_validation 的連結

本資料夾將被用於：

- **Traceability 驗證**（`04_validation/traceability`）
- **Portability 指標計算**（設定與建模成本）
- 跨 PdM 與 Carbon 之 domain reuse 證明

---

## 6. 論文對應說明

- 論文章節：
  - Chapter 6：Carbon Management Case Study
  - Chapter 7：Discussion（語意整合與可擴展性）

---

## 7. 備註

本 processed 資料為示範性成果，實務應用時可依專案需求擴充節點與關係型態。

