# PdM_HVAC/tasks — 自動生成的維運工單（Maintenance Tasks）

本資料夾包含依 Anomaly 類型自動建立的維運工單，用於：

- 驗證 SAM 中 Action／Actor 模型
- 觸發 STRIDE 工作流（n8n/Power Automate）
- 測量 TTA（Time-to-Action）
- 建立完整責任鏈（Provenance）

---

## 📄 MaintenanceTasks_Generated.csv

### 欄位定義

| 欄位 | 說明 |
|------|------|
| `task_id` | 工單 ID（T0001） |
| `anomaly_id` | 來源異常 p_id |
| `component_id` | GlobalId |
| `sensor_id` | 感測器 |
| `task_type` | 維修動作（Inspect / ReplaceFilter…） |
| `priority` | High / Medium / Low |
| `assigned_to` | 指派技師或 AI Agent |
| `timestamp_created` | 工單生成時間 |

### 圖模式對應

```cypher
(:Anomaly)-[:TRIGGERS]->(:MaintenanceTask)-[:ASSIGNED_TO]->(:Actor)
```

---