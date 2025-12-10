
# 02_data

本資料夾包含所有實驗所需之 **輸入數據（input data）**，用以重現：

- PdM HVAC 案例（預測性維護）
- SID-CM 案例（碳管理工作流）
- 動態本體（ontology evolution）與事件序列案例

## 結構概述

```text
02_data/
├─ PdM_HVAC/
│  ├─ HVAC_Sensor_Input.csv
│  ├─ Building_Component_IFC_Map.csv
│  ├─ PdM_Metadata.yaml
│  └─ README.md
├─ SID_CM/
│  ├─ Carbon_Input.csv
│  ├─ Material_Database.csv
│  └─ README.md
├─ Dynamic_Ontology/
│  ├─ Ontology_Change_Log.csv
│  ├─ TBox_ABox_Snapshots/
│  └─ README.md
└─ raw/
```

### PdM_HVAC

- `HVAC_Sensor_Input.csv`  
  - 包含時間序列感測資料（溫度、能源使用量等）  
  - 主要欄位示例：  
    - `sensor_id`  
    - `timestamp`（ISO 格式）  
    - `measure_type`（如 `Temp`, `Energy`）  
    - `value`（float）  

- `Building_Component_IFC_Map.csv`  
  - 將感測器對應至 BIM / IFC 元件  
  - 主要欄位示例：  
    - `component_id`  
    - `ifc_guid`  
    - `sensor_id`  
    - `zone_id`  

### SID_CM

- `Carbon_Input.csv`  
  - 涵蓋建築構件、工項、材料批次等資訊，支援生命周期碳排估算。  

- `Material_Database.csv`  
  - 對應 ICE / EPD 等資料來源的排碳係數。  

### Dynamic_Ontology

- `Ontology_Change_Log.csv`  
  - 記錄 ontological change 事件（新增類別、屬性調整、關係變更等）。  

- `TBox_ABox_Snapshots/`  
  - 儲存不同時間點的 schema（TBox）與資料（ABox）快照，用於分析語義演化對推理與自動化流程的影響。  

---

## 使用注意事項

- 若您的實驗牽涉到真實專案資料，請以本資料夾中的 **模擬/匿名化版本** 為基礎。  
- 部分檔案僅供結構示意，需依照您的實際場域另行填入或接軌。  
