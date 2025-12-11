# PdM_HVAC — HVAC 預測性維護（Predictive Maintenance）案例資料集

本資料夾收錄 HVAC（空調系統）預測性維護案例之語意化資料集，用於驗證：

- 語意行動管理（SAM）方法論  
- STRIDE 自動化框架  
- PdM 推理（異常偵測、多源資料整合）  
- 工單生成（TIAA → MaintenanceTask）  
- 時間效能（TTA）、追溯性（Traceability）與擴展性（Scalability）

資料依其語意角色分為五類：

| 類別 | 說明 |
|------|------|
| `raw/` | 原始感測與設備資料 |
| `processed/` | 經 ETL 對齊、標註後的語意化 Performance / Anomaly |
| `edges/` | Neo4j 圖關係（edge lists） |
| `tasks/` | 依異常自動生成的維運工單 |
| `actors/` | 維運角色（Technician / Supervisor / AI-Agent） |

此資料集於以下章節使用：

- **第 5 章 STRIDE 系統實作（特別是 5.1–5.3）**  
- **第 6 章 HVAC 預測性維護案例驗證**  
- **附錄 Appendix B（資料欄位與實驗設定）**

下列子資料夾包含詳細說明：

- `raw/README_PdM_raw.md`
- `processed/README_PdM_processed.md`
- `edges/README_PdM_edges.md`
- `tasks/README_PdM_tasks.md`
- `actors/README_PdM_actors.md`
