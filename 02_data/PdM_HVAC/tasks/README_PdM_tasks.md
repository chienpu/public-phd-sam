# PdM_HVAC/tasks — 自動生成的維運工單（Maintenance Tasks）

本資料夾包含依 Anomaly 類型自動建立的維運工單，用於：

- 驗證 SAM 中 Action／Actor 模型
- 觸發 STRIDE 工作流（n8n/Power Automate）
- 測量 TTA（Time-to-Action）
- 建立完整責任鏈（Provenance）

---

本資料夾包含：

- MaintenanceTasks_Generated.csv（依異常自動生成）
-（若需要）CompensationTasks.csv（補償流程）

工單由異常事件（Anomaly）觸發，符合本研究的 TIAA 模型：  
Trigger → Issue → Action → Actor

---

## 生成規則（本研究設定）

你選擇的規則為：

### **B. 同一設備（GlobalId）＋同一小時的異常 → 合併為一張工單**

此規則較符合實務維運流程。  
例：

| global_id | Timestamp | Anomaly | → 工單 |
|-----------|-----------|---------|--------|
| AHU01 | 15:01 | HighTemp | T001 |
| AHU01 | 15:45 | HighEnergy | T001（同一小時合併） |

---

## 工單欄位

| 欄位 | 說明 |
|------|------|
| task_id | T0001 形式 |
| anomaly_id | 來源 Anomaly |
| priority | High / Medium / Low |
| assigned_actor_id | 指派人員 |
| status | Open / InProgress / Closed |
| created_at | 工單時間 |
| due_at | 建議完成時間 |

語意圖譜：


```cypher
(:Anomaly)-[:TRIGGERS]->(:MaintenanceTask)-[:ASSIGNED_TO]->(:Actor)
```

---

## 📌 小結

tasks/ 對應 STRIDE 第 3 層「行動編排層」，  
是第六章實驗 TTA 與 Traceability 的核心資料。
