# PdM_HVAC / processed — 數據處理後資料

本資料夾包含：

- Performance_Data_300.csv（感測資料彙整後的性能資料）
- Anomaly_Data_300.csv（異常標註）

這些資料是執行語意推理與維修工單產生的核心輸入。

---

## 1. Performance_Data_300.csv

來源：

- Sensor_Data_300.csv
- Edge_MAPS_SENSOR_DATA.csv（對應 Sensor → BC）

**欄位：**

| 欄位名稱 | 說明 |
|---------|------|
| event_id | 對應原始事件 |
| sensor_id | 感測器 |
| global_id | 監控設備 GlobalId |
| MetricName | 測量项目 |
| Value | 值 |
| update_start / update_end | 時間窗彙整結果 |
| date / time_only | 查詢方便用 |

語意圖譜：

```cypher
(:Sensor)-[:GENERATES]->(:PerformanceData)-[:ABOUT]->(:BuildingComponent)
```

---

## 2. Anomaly_Data_300.csv

包含以 AI 模型或規則偵測出的異常事件。

**欄位：**

| 欄位 | 說明 |
|------|------|
| p_id | 異常 ID |
| event_id | 對應 PerformanceData |
| sensor_id | 來源感測器 |
| global_id | 所屬設備 |
| MetricName | 異常類型參數 |
| Value | 異常觸發時數值 |
| Timestamp | 發生時間 |
| Anomaly | 異常類別（HighEnergy, OverTemp …） |
| ai_model | 模型名稱（如 IForest） |

語意圖譜：

```cypher
(:PerformanceData)-[:GENERATES]->(:Anomaly)
```

## 📌 小結

processed/ 檔案屬於 STRIDE 第 2 層（知識與資料管理層）。  
其內容將直接參與語意推理、工單生成與效能量測。
