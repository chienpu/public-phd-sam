# PdM_HVAC — HVAC 預測性維護（Predictive Maintenance）案例資料集

本資料夾收錄本研究於第六章中所使用的 **HVAC（空調系統）預測性維護案例資料**。  
所有資料均為經過匿名化或合成之 demo 數據，目的是支援：

- STRIDE / SAM 框架之資料整合、語意推理與任務派發驗證
- 第六章案例中之 TTA、Traceability、Scalability 等指標量測
- 04_validation 工具中之自動化指標計算流程（compute_metrics.py）

此案例展示從 **IoT 感測 → 異常偵測 → 語意推理 → 行動指派** 的完整閉環。

---

## 📁 資料夾結構

PdM_HVAC/
├─ raw/ ← 原始資料（Sensor + BuildingComponent）
├─ processed/ ← 清洗後之 Performance + Anomaly
├─ edges/ ← Graph 關係映射 CSV
├─ tasks/ ← 自動生成的維修工單
├─ actors/ ← 維運角色名冊
└─ README_PdM_overview.md ← 本檔案

---

## 🔍 模型對應（SAM / STRIDE）

| Data Folder | 對應語意模型 | 說明 |
|------------|-------------|------|
| raw/ | Sensor, BuildingComponent | IoT 與 BIM 匯出資料 |
| processed/ | PerformanceData, Anomaly | 經 ETL 處理與異常判定後的資料 |
| edges/ | MONITORS, GENERATES, ABOUT | 建立語意圖譜的必要關係 |
| tasks/ | MaintenanceTask | TIAA 中 Action 之實例化 |
| actors/ | Actor | TIAA 中 Actor |

---

## 🧩 語意圖譜（Property Graph Schema）

- `Sensor --MONITORS--> BuildingComponent`
- `Sensor --GENERATES--> PerformanceData`
- `PerformanceData --ABOUT--> BuildingComponent`
- `PerformanceData --GENERATES--> Anomaly`
- `Anomaly --TRIGGERS--> MaintenanceTask`
- `MaintenanceTask --ASSIGNED_TO--> Actor`

此語意結構對應本研究 STRIDE 框架的核心推理流程。

---

## 📘 參考章節

- **論文第 5 章**：STRIDE 技術堆疊與推理機制  
- **論文第 6 章**：HVAC 預測性維護案例  
- **附錄 A / B**：資料實例與完整圖譜架構
