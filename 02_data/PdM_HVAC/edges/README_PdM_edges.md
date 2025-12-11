# PdM_HVAC/edges — 圖關係（Edge Lists）

本資料夾包含將 raw／processed 資料連結成 Neo4j 語意圖譜所需之關係定義。

---

## 📄 Edge_MAPS_SENSOR_DATA.csv  
描述 Sensor 與 BuildingComponent 間監測關係。

| 欄位 | 說明 |
|------|------|
| `Source` | Sensor ID（sensor_id） |
| `Target` | BuildingComponent.GlobalId |
| `Relationship` | 固定為 `MONITORS` |

匯入結果：

```cypher
(:Sensor)-[:MONITORS]->(:BuildingComponent)
```

📄 Edge_GENERATES.csv
描述感測器產生 PerformanceData 之關係。

| 欄位          | 說明                     |
| ----------- | ---------------------- |
| `event_id`  | PerformanceData ID     |
| `sensor_id` | 感測器 ID                 |
| `global_id` | 所屬設備（輔助查詢）             |
| 其他欄位        | 與 Performance_Data 同格式 |

匯入結果：

```cypher
(:Sensor)-[:GENERATES]->(:PerformanceData)
```

此資料夾定義了 PdM 語意圖譜的“關係層”（Relationships）。

---