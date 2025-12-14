# 05_workflows — External Workflow Integration (PdM)

本資料夾示範 **SAM–STRIDE 在 PdM（HVAC）案例中，如何與外部工作流平台整合**，
用以驗證論文第六章中的 **Action / Actor、自動派工、TTA 與補償流程**。

本研究並不依賴特定平台，而是以 **Power Automate** 與 **n8n** 作為代表性工具，
說明語意驅動任務如何被轉譯為可執行的工作流。

---

## 資料夾結構

```text
05_workflows/
├─ power_automate.json     # Power Automate flow（示意 / mock）
├─ n8n_pdm.json            # n8n workflow（示意 / mock）
├─ screenshots/
│  ├─ power_automate_flow.png
│  └─ n8n_flow.png
└─ README.md
```

---

## 設計原則（對應論文）

- **平台不可知（Platform-agnostic）**  
  SAM 僅負責輸出語意化任務 payload，不綁定特定 workflow engine。

- **可追溯（Traceable）**  
  每次 workflow 觸發皆帶有 `run_id`、`workorder_id`、`actor` 等欄位，
  並回寫至 Neo4j 以支援 PROV-style traceability。

- **可補償（Compensable）**  
  workflow 失敗或 timeout 時，可回傳狀態以觸發補償邏輯（第六章 Compensation 指標）。

---

## Power Automate（示意）

`power_automate.json` 示範一個簡化流程：

1. 接收 HTTP Request（來自 `workflow_trigger_api.py`）
2. 解析 Maintenance Task payload
3. 指派維修人員（mock）
4. 回傳執行結果與時間戳

實際部署時，可將該 JSON 匯入 Power Automate，或以此作為流程設計參考。

---

## n8n（示意）

`n8n_pdm.json` 示範一個等價的 n8n workflow：

1. Webhook Trigger
2. Function node（payload mapping）
3. IF node（模擬成功 / 失敗）
4. Respond to Webhook

n8n 版本特別適合本地測試與 reviewer 重現。

---

## 與第六章指標的關聯

| 指標 | Workflow 貢獻 |
|---|---|
| TTA | Workflow 接收與回應時間 |
| Compensation | 失敗回傳 → 補償邏輯 |
| Traceability | Task ↔ Actor ↔ Workflow log |
| Portability | 同一 payload 適用於不同平台 |

---

## 注意事項

- 本資料夾提供之 JSON 為 **研究示意與可重現輔助用途**，
  並非企業正式部署範本。
- 若 reviewer 未安裝 Power Automate / n8n，
  仍可使用 `03_execution/workflow_trigger_api.py` 的 mock 模式完成實驗。

- `power_automate_flow.png`：展示完整 flow 節點配置  
- `n8n_flow.png`：展示 PdM 案例之 n8n workflow 配置  

> 註：實際連接之 CMMS / 工單系統端點與認證資訊不包含在本 repo 中，請依照你所在之組織環境進行設定。  
