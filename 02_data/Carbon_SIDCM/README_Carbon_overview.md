# Carbon_SIDCM 資料集總覽（README_Carbon_overview.md）

本資料夾提供 **SID-CM（Semantic Integration and Digitization for Carbon Management）** 情境之示範資料集，用於驗證本論文所提出之 **語意行動管理（Semantic Action Management, SAM）框架** 在「非即時、跨生命週期碳管理情境」中的可攜性（Portability）、可追溯性（Traceability）與語意整合能力。

本情境對應論文第六章之 **碳管理驗證案例（Carbon Management Case Study）**，並與 PdM-HVAC 情境共享相同的語意架構與驗證方法，以證明 SAM / SID-CM 框架之 **跨領域通用性（Domain Independence）**。

---

## 1. 情境說明與論文對位

- **應用情境**：建築環境生命週期碳管理  
- **研究目的**：
  1. 驗證異質碳資料（材料、能耗、構件）之語意整合能力  
  2. 驗證 SAM 架構是否能在非即時情境下支援可追溯決策  
  3. 比較 Baseline 與 SID-CM 在部署與資料準備上的可攜性差異  

- **論文章節對應**：
  - Chapter 6：Validation and Case Studies  
  - §6.x Carbon Management Case Study  
  - §6.x Cross-domain Portability and Traceability Analysis  

---

## 2. 資料夾結構總覽

```
Carbon_SIDCM/
├─ raw/
│   ├─ Carbon_Material_Factors_demo.csv
│   ├─ Carbon_Component_BoQ_demo.csv
│   ├─ Carbon_Energy_Use_demo.csv
│   └─ README_Carbon_raw.md
│
├─ processed/
│   ├─ SIDCM_Graph_Nodes_demo.csv
│   ├─ SIDCM_Graph_Relationships_demo.csv
│   └─ README_Carbon_processed.md
│
└─ README_Carbon_overview.md
```

---

## 3. raw 資料層說明（原始碳資料）

`raw/` 資料夾包含未經語意整合之前的原始碳相關資料，模擬實務中常見之資料分散狀態。

### 3.1 Carbon_Material_Factors_demo.csv
- 功能：材料碳排係數資料  
- 典型來源：EPD、LCA Database  
- 主要欄位：
  - material_id  
  - material_name  
  - emission_factor  
  - unit  

### 3.2 Carbon_Component_BoQ_demo.csv
- 功能：構件工程量（Bill of Quantities）  
- 主要欄位：
  - component_id  
  - material_id  
  - quantity  
  - unit  

### 3.3 Carbon_Energy_Use_demo.csv
- 功能：建築或系統能耗紀錄  
- 主要欄位：
  - system_id  
  - energy_type  
  - energy_consumption  
  - time_period  

---

## 4. processed 資料層說明（SID-CM 語意整合結果）

`processed/` 資料夾為透過 SID-CM 方法，將 raw 資料轉換為可直接匯入圖資料庫（Neo4j）的語意圖結構。

### 4.1 SIDCM_Graph_Nodes_demo.csv
代表已語意化的節點（Nodes），常見類型包括：

- BuildingComponent  
- Material  
- EnergyFlow  
- EmissionRecord  
- Actor / Organization  

此層對應論文中 **語意節點建模（Semantic Node Modeling）** 的成果。

---

### 4.2 SIDCM_Graph_Relationships_demo.csv
定義節點間之語意關係（Relationships），例如：

- COMPONENT_USES_MATERIAL  
- MATERIAL_HAS_EMISSION_FACTOR  
- COMPONENT_CONSUMES_ENERGY  
- ACTOR_RESPONSIBLE_FOR  

此層對應論文中 **跨資料來源關係對齊（Semantic Relationship Alignment）**。

---

## 5. 與 PdM-HVAC 情境之關聯

雖然 Carbon_SIDCM 與 PdM-HVAC 在資料型態與時間特性上不同，但兩者：

- 共用 **SAM 核心語意架構**
- 共用 **PROV-O 為基礎之可追溯模型**
- 共用 **04_validation 中的驗證流程與指標設計邏輯**

差異整理如下：

| 面向 | PdM-HVAC | Carbon-SIDCM |
|----|---------|--------------|
| 時間特性 | 即時 / 事件驅動 | 非即時 / 批次 |
| 核心指標 | TTA、Latency | Portability、Traceability |
| 資料頻率 | 高頻 IoT | 低頻彙總資料 |
| 驗證重點 | 自動化反應能力 | 語意整合與部署效率 |

---

## 6. 與 04_validation 的關係

Carbon_SIDCM 資料將用於：

- **Portability 指標**：比較 Baseline 與 SID-CM 在資料準備與模型設定上的成本  
- **Traceability 驗證**：測試跨材料、構件、能耗資料之 PROV-O 可追溯鏈  
- **Cross-domain 驗證**：證明 SAM 架構可在不同 domain 重用  

相關驗證腳本位於：

```
04_validation/
├─ metrics/
├─ traceability/
└─ performance/
```

---

## 7. 重現說明（Reproducibility Notes）

- 本資料集為示範性資料（demo），結構與語意角色與實務資料一致  
- 所有欄位命名與關係設計皆可直接擴展至真實專案  
- 搭配 04_validation 目錄，即可完整重建論文第六章之碳管理驗證流程  

---

## 8. 小結

Carbon_SIDCM 情境展示了 SAM / SID-CM 框架在 **非即時、跨生命週期決策支援** 中的應用潛力，並補足傳統碳管理工具在語意整合、可追溯性與可重用性上的不足。

本資料夾與 PdM-HVAC 情境共同構成論文第六章的雙案例驗證基礎。
