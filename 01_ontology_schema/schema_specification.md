# Schema Specification for SAM / STRIDE Ontology
Version: 1.0  
Author: Chien-Pu Huang  
Repository: public-phd-sam  
Last Updated: 2025  

---

# 1. Overview

本規格書說明本研究於 STRIDE（Semantic Reasoning and Integration for Data-driven Engineering）與 SAM（Semantic Action Management）框架中使用之 **語意圖（semantic property graph）結構**。

此 schema 為博士論文及期刊論文（Automation in Construction / Advanced Engineering Informatics）中所有：

- 語意推理（semantic reasoning）  
- 事件建模（event representation）  
- 維運行動（action automation）  
- 因果追溯（provenance tracking）  
- 多跳查詢（graph traversal）  
- 重現性實驗（traceability / latency / TTA）  

之基礎。

Ontology 以 **Neo4j Property Graph** 為主，並提供 **對照 TTL（IFC, SOSA, PROV-O）** 作為跨標準語意銜接使用。

---

# 2. Design Principles

STRIDE ontology 依循五項設計原則：

1. **Graph-native**：  
   所有 reasoning 與 workflow 都以多跳遍歷（graph traversal）作為主要機制，而非 rule engine。

2. **Domain-Agnostic but Domain-Adaptive**：  
   可支援 PdM（HVAC）與碳管理（SID-CM）兩種場景。

3. **Low-Entropy Modeling**：  
   僅建模維運所需的最小必要語意（Minimal Viable Ontology）。

4. **Traceability-first**：  
   所有事件 → 行動 → 工作流 → 回饋，都能被完整追蹤。

5. **Semantic Interoperability**：  
   與 IFC / SOSA / PROV-O 等標準保有語意對應（TTL）。

---

# 3. Node Type Specification

以下列出所有 Node Labels，其屬性與功能角色。

---

## 3.1 BuildingComponent

| 屬性 | 類型 | 說明 |
|------|------|------|
| `ComponentId` | STRING (UUID or IFC GlobalId) | 元件唯一識別碼 |
| `type` | STRING | 如 AHU, VAV, Pump, DuctSection |
| `avg_energy` | FLOAT | 基準能源耗用（PdM 用） |
| `avg_temp` | FLOAT | 基準溫度（PdM 用） |
| `location` | STRING | 建物區域或空間名稱 |

**角色：** PdM 與 SID-CM 的核心維運實體，可被 sensor 監測並可發生 anomaly。

---

## 3.2 Sensor

| 屬性 | 類型 | 說明 |
|------|------|------|
| `SensorId` | STRING | 感測器唯一識別碼 |
| `type` | STRING | `Temperature`, `Energy`, `CO2`, etc. |
| `unit` | STRING | `°C`, `kWh`, etc. |

**角色：** 監測 BuildingComponent，用來生成 PerformanceData。

---

## 3.3 PerformanceData

| 屬性 | 類型 | 說明 |
|------|------|------|
| `timestamp` | DATETIME | 量測時間 |
| `value` | FLOAT | 量測值 |
| `quality` | STRING | Good / Missing / Imputed（可選） |

**角色：** 代表觀測值，可能觸發 anomaly。

---

## 3.4 Anomaly

| 屬性 | 類型 | 說明 |
|------|------|------|
| `AnomalyId` | STRING | 自動生成 UUID |
| `timestamp` | DATETIME | 異常發生時間 |
| `type` | STRING | 單點異常、複合異常 |
| `severity` | FLOAT | 嚴重度（可選） |

**角色：** 代表維運事件，可觸發 To-Do 或自動化流程。

---

## 3.5 MaintenanceTask

| 屬性 | 類型 | 說明 |
|------|------|------|
| `TaskId` | STRING | Unique ID |
| `status` | STRING | Pending / Assigned / Closed |
| `created_at` | DATETIME | 建立時間 |
| `description` | STRING | 工單內容摘要 |

**角色：** 維修工單，由 anomaly 觸發，可指派給 Actor。

---

## 3.6 Actor

| 屬性 | 類型 | 說明 |
|------|------|------|
| `ActorId` | STRING | Unique |
| `role` | STRING | Engineer / System / Vendor |
| `name` | STRING | 名稱（人或系統） |

**角色：** 執行維修或流程的代理人。

---

## 3.7 WorkflowRun

| 屬性 | 類型 | 說明 |
|------|------|------|
| `RunId` | STRING | Workflow 觸發事件 UUID |
| `timestamp` | DATETIME | Workflow 執行時間 |
| `engine` | STRING | Power Automate / n8n |

**角色：** 表示 STRIDE workflow 的一次具體執行。

---

# 4. Relationship Type Specification

## 4.1 MONITORS
**Sensor → BuildingComponent**

意義：感測器監測此元件。

```cyper
(s:Sensor)-[:MONITORS]->(c:BuildingComponent)
```
