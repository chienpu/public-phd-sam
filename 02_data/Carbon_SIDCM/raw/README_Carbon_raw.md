# Carbon_SIDCM 原始資料說明（README_Carbon_raw.md）

本資料夾包含 **碳管理情境（Carbon_SIDCM）** 中尚未進行語意整合的原始資料（raw data），模擬實務中碳相關資訊分散於不同資料來源（LCA、BoQ、能耗系統）的現況。

這些資料將於後續流程中透過 **SID-CM（Semantic Integration and Digitization for Carbon Management）** 方法轉換為具備語意結構與可追溯性的圖資料。

---

## 1. 資料夾用途

- 作為 **Baseline（非語意整合）** 的資料輸入形式  
- 作為語意整合（raw → processed）的起點  
- 支援論文第六章中對「資料碎片化問題」的說明  

---

## 2. 檔案列表與說明

### 2.1 Carbon_Material_Factors_demo.csv
**用途**：提供建築材料之碳排放係數（Emission Factors）

**典型來源**：
- EPD（Environmental Product Declaration）
- LCA 資料庫（如 ecoinvent）

**主要欄位說明**：
| 欄位名稱 | 說明 |
|--------|------|
| material_id | 材料唯一識別碼 |
| material_name | 材料名稱 |
| emission_factor | 單位碳排放量 |
| unit | 碳排放單位（如 kgCO2e/kg） |

---

### 2.2 Carbon_Component_BoQ_demo.csv
**用途**：描述構件與材料之工程量（Bill of Quantities）

**主要欄位說明**：
| 欄位名稱 | 說明 |
|--------|------|
| component_id | 建築構件 ID |
| material_id | 對應材料 ID |
| quantity | 使用數量 |
| unit | 數量單位 |

---

### 2.3 Carbon_Energy_Use_demo.csv
**用途**：記錄建築或系統的能耗資料

**主要欄位說明**：
| 欄位名稱 | 說明 |
|--------|------|
| system_id | 系統或設備 ID |
| energy_type | 能源類型（電力、天然氣等） |
| energy_consumption | 能耗數值 |
| time_period | 統計期間 |

---

## 3. 資料特性與限制

- 資料來源彼此獨立，**缺乏明確語意關聯**
- 無法直接回答跨資料問題（如：某構件的生命週期碳排）
- 需仰賴人工或客製化腳本進行整合

這些限制正是 SID-CM 方法欲解決的核心問題。

---

## 4. 與後續處理流程之關係

本資料夾內容將作為輸入，經由：

1. 語意角色定義（Entity / Activity / Actor）
2. 關係對齊（Material–Component–Energy）
3. 可追溯性標註（PROV-O）

轉換為 `processed/` 中的語意圖資料。

---

## 5. 論文對應說明

- 論文章節：Chapter 6（Carbon Management Case Study）
- 對應議題：
  - 資料碎片化（Data Fragmentation）
  - 語意落差（Semantic Gap）
  - 傳統碳管理流程之限制

---

## 6. 備註

本資料集為示範用途（demo），欄位結構與語意設計可直接擴展至真實建築專案。
