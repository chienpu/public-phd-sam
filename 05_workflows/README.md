
# 05_workflows

本資料夾提供 **工作流平台（Power Automate / n8n）** 之流程藍圖與示意截圖，用於支援：

- 維護工單自動建立  
- 事件回寫（provenance logging）  
- TTA 測量（event → action）  

## 結構

```text
05_workflows/
├─ power_automate.json
├─ n8n_pdM.json
├─ screenshots/
│  ├─ power_automate_flow.png
│  └─ n8n_flow.png
└─ README.md
```

## Power Automate


- `power_automate.json`：  
  - 匯入方式：於 Power Automate 入口網站中選擇「匯入方案 / flow」，上傳 JSON。  
  - 流程內容大致包括：  
    - 接收 HTTP request（含 anomaly payload）  
    - 建立或更新維護工單（可連接 SharePoint / Dataverse / 外部 CMMS）  
    - 回傳結果與時間戳至呼叫端  

## n8n

- `n8n_pdM.json`：  
  - 可於 n8n UI 中匯入作為 workflow blueprint。  
  - 典型節點：  
    - Webhook（接收 anomaly payload）  
    - Function / HTTP Request（與 CMMS / 工單系統串接）  
    - 回呼 API（將結果與時間戳回寫至 `workflow_trigger_api.py`）  

## 截圖（screenshots/）

- `power_automate_flow.png`：展示完整 flow 節點配置  
- `n8n_flow.png`：展示 PdM 案例之 n8n workflow 配置  

> 註：實際連接之 CMMS / 工單系統端點與認證資訊不包含在本 repo 中，請依照你所在之組織環境進行設定。  
