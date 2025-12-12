# PdM_HVAC / actors — 維運角色名冊

此資料夾包含：

- Actors.csv（手動或自動產生）

Actor 在 TIAA 與 STRIDE 中扮演 **行動執行者** 的角色。

---

## CSV 欄位

| actor_id | name | role | team |
|----------|------|------|------|
| Tech01 | Technician_01 | Technician | HVAC_Team |
| Tech02 | Technician_02 | Technician | HVAC_Team |
| Sup01 | Supervisor_01 | Supervisor | FM_Office |
| AIA01 | AI_Agent_01 | AI-Agent | AI_Service |

---

## 語意圖譜對應

```cypher
(:MaintenanceTask)-[:ASSIGNED_TO]->(:Actor)
```

---

## 📌 小結

actors/ 資料夾提供 STRIDE 中 Action 的執行者資訊，  
對應 TIAA 的「Actor」語意區塊。
