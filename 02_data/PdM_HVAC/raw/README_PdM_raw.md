# PdM_HVAC / raw — 原始資料說明

本資料夾包含本研究在 PdM（預測性維護）案例中使用之原始資料來源，包括：

- 感測器資料（Sensor_Data_300.csv）
- 建築元件 / BIM 匯出資料（BuildingComponent_Dataset.csv）

這些資料構成語意圖譜中 `Sensor` 與 `BuildingComponent` 的基礎節點。

---

## 1. Sensor_Data_300.csv

**用途：**  
模擬 HVAC 系統之異常前後的感測值，作為後續 PerformanceData 的輸入。

**欄位：**

| 欄位名稱 | 說明 |
|---------|------|
| event_id | 單筆觀測 ID |
| sensor_id | 感測器 ID（例如 S001, S002） |
| MetricName | 測量項目（Energy, Temp, Vibration …） |
| Value | 數值 |
| Timestamp | ISO 8601 時間戳記 |

**語意圖譜對應：**

```cypher
(:Sensor {sensor_id})-[:GENERATES]->(:PerformanceData {event_id})
```

---

## 2. BuildingComponent_Dataset.csv

**用途：**  
提供 BIM / IFC 中的設備清單，對應為圖譜中的 `BuildingComponent`。

**欄位：**

| 欄位名稱 | 說明 |
|---------|------|
| GlobalId | IFC GlobalId（唯一識別） |
| LastUpdatedDate | BIM 更新時間 |
| TypeOfBC | 設備類型（AHU, Pump, Coil …） |
| Name | 設備名稱 |
| Location | 位置描述 |
| Floor | 樓層 |
| Sponsor | 維運責任單位 |

**語意圖譜對應：**

```cypher
(:BuildingComponent {GlobalId})
```

---

## 📌 小結

raw/ 資料作為 STRIDE 第 1 層（資料整合層）之輸入，  
後續 processed/ 會將其轉換成 Performance 與 Anomaly 用於推理與驗證。
