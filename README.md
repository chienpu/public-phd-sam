# public-phd-sam : 語義行動管理（SAM）框架實證數據庫
Semantic Action Management (SAM) Reproducibility Package
MIT Licensed

本資料庫為博士論文《語義行動管理（SAM）框架之運維自動化研究》與期刊論文
STRIDE: Semantic Reasoning and Integration for Data-driven Engineering
所使用之完整可重現（reproducible）數據與程式套件（Replication Package）。

本專案涵蓋：
-語義模型（Ontology / TTL / Cypher / SHACL）
-資料集（PdM / Carbon / Dynamic Ontology）
-推理與自動化腳本（Neo4j + Python）
-工作流藍圖（Power Automate / n8n）
-性能、可追溯性、TTA（Event→Action Latency）量化驗證工具
-重現本論文所有統計結果之 notebook 與輸出檔案
本項目以 MIT License 授權，可自由使用、延伸、引用。

---

## 💡 專案概述 (Project Overview)

本儲存庫包含 **SAM (Semantic Action Management) 框架**的完整實驗數據、核心代碼與工作流藍圖，旨在支援博士論文和 Q1 級期刊文章《**語義行動管理框架於工程資訊系統之實證研究**》的所有量化結果重現性（Reproducibility）和透明度（Transparency）。

SAM 框架，亦稱 **STRIDE (SemanTic Reasoning and Integration for Data-driven Engineering)**，透過**本體論驅動**的方法，將異構數據（如 BIM/IFC、IoT 感測器數據和 FM 紀錄）整合至 **Neo4j 知識圖譜**，實現工程管理中的**實時推理**與**工作流程自動化**。

### 核心貢獻與驗證 (Core Contributions and Validation)

| 領域 | 關鍵指標 | 實證成果 (PdM 案例) | 論文支持文件 |
| :--- | :--- | :--- | :--- |
| **效率** | 任務執行時間縮減 | **81%** 總時間節省 | Table 1 |
| **實時性** | 事件至行動延遲 (TTA) | **亞秒級響應** (~0.42 秒) | Table A1.2 |
| **可追溯性** | 任務因果鏈完整度 | **100%** 任務可追溯至原始事件 | Table A2.1 |
| **可擴展性** | 查詢延遲 (30K 節點) | 僅需 **0.74 秒** | Section 4.2.5 |
| **可移植性** | 跨場景部署重用性 | 成功應用於 PdM 和 SID-CM (碳管理) 兩個不同領域 | Table A3 |

---

## ⚙️ 系統與環境要求 (System and Environment Requirements)

為確保實驗結果能夠準確重現，請準備以下環境：

### 核心依賴 (Core Dependencies)

| 組件 | 版本要求 | 用途 |
| :--- | :--- | :--- |
| **Neo4j Graph Database** | 4.x 或 5.x 穩定版本 | 知識圖譜存儲、語義建模與 Cypher 實時查詢 |
| **Python** | 3.8 或更高版本 | 數據 ETL、異常偵測邏輯與 API 觸發 |
| **Power Automate** | Desktop / Cloud 版本 | PdM 案例的工作流執行與 TTA 測量 |

### Python 依賴安裝

請使用以下命令安裝所有 Python 庫：

```bash
pip install -r requirements.txt
```

## 🛠️ 重現步驟：快速入門 (Quick Start Guide for Replication)
以下是重現核心 PdM/HVAC 案例（包括 TTA、Traceability 和 Latency 測量）的流程：

### Step 1: 設置 Neo4j 知識圖譜
1. 啟動您的 Neo4j 資料庫實例。
2. 執行 01_Ontology_Schema/Cypher_Schema_Creation.cypher，建立所有節點標籤、關係類型、約束和索引。此腳本定義了框架的語義規範。

