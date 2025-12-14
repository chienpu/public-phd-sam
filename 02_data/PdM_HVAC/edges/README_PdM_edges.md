# PdM_HVAC / edges — 圖譜關係映射資料

本資料夾包含兩種 CSV，用於建立 Neo4j Property Graph 中的關係（Edges）：

- Edge_MAPS_SENSOR_DATA.csv → Sensor MONITORS BuildingComponent
- Edge_GENERATES.csv → Sensor GENERATES PerformanceData

---

## 1. Edge_MAPS_SENSOR_DATA.csv

描述感測器監測哪一個建物元件。

| 欄位 | 說明 |
|------|------|
| Source | sensor_id |
| Target | GlobalId（建物設備） |
| Relationship | 固定為 MONITORS |

匯入後建立：

```cypher
(:Sensor)-[:MONITORS]->(:BuildingComponent)
```

---

## 2. Edge_GENERATES.csv

描述感測器產生 PerformanceData 的關係。

| 欄位 | 說明 |
|------|------|
| event_id | PerformanceData |
| sensor_id | Sensor |
| global_id | 冗餘欄位 |
| MetricName | 測量項目 |
| Value | 測量值 |
| 時間欄位 | 與 PerformanceData 對應 |

匯入後：

```cypher
(:Sensor)-[:GENERATES]->(:PerformanceData)
```

---

## 📌 小結

edges/ 是建立語意圖譜的關鍵步驟，  
對應 STRIDE 第 2 層「知識與資料管理層」。
此資料夾定義了 PdM 語意圖譜的“關係層”（Relationships）。

---
