# PdM_HVAC/raw — 原始資料（Raw Sensor & Equipment Data）

本資料夾包含 HVAC PdM 案例之 **原始輸入資料**，為後續 ETL、語意推理與 STRIDE 框架執行的基礎。

---

## 📄 Sensor_Data_300.csv — 感測器高頻資料

此檔案模擬 HVAC 系統中的溫度、能耗等量測，用於生成 PerformanceData 並對應異常偵測。

### 欄位定義

| 欄位 | 說明 |
|------|------|
| `event_id` | 感測事件 ID（對應 PerformanceData.event_id） |
| `sensor_id` | 感測器 ID（對應 `:Sensor`） |
| `MetricName` | 量測類型（Energy、Temperature…） |
| `Value` | 觀測值 |
| `Timestamp` | ISO 8601 時戳 |

### 對應圖模式

```cypher
(:Sensor {sensor_id})-[:GENERATES]->(:PerformanceData {event_id})

---

