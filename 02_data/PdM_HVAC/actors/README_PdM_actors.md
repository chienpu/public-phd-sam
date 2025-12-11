# PdM_HVAC/actors — 維運角色（Actors）

本資料夾包含 PdM 案例中所有可接受任務之角色（Actor）。  
對應到 TIAA 中的「A（Actor）」語意角色，用於建立語意行動鏈。

---

## 📄 Actors.csv

### 欄位定義

| 欄位 | 說明 |
|------|------|
| `actor_id` | Actor 節點主鍵（Technician_01） |
| `name` | 顯示名稱 |
| `role` | Technician / Supervisor / AI-Agent |
| `team` | 維運小組／部門 |

### 典型示例

| actor_id | role | team |
|----------|------|------|
| Technician_01 | Technician | HVAC_Team |
| Technician_02 | Technician | HVAC_Team |
| Supervisor_01 | Supervisor | FM_Office |
| AI_Agent_01 | AI-Agent | AI_Service |

---

所有 Actor 將在匯入 Neo4j 後參與工單分派，並作為語意責任鏈（Provenance Chain）的一部分。