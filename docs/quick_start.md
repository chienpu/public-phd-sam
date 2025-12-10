
# Quick Start Guide

本文件提供一個從空白環境開始，到成功重現 PdM 案例核心指標（TTA、traceability、latency）的最小流程。

## 1. 安裝環境

1. 安裝 Neo4j 4.x 或 5.x
2. 安裝 Python 3.8+
3. clone 專案：

```bash
git clone https://github.com/chienpu/public-phd-sam.git
cd public-phd-sam
pip install -r requirements.txt
```

## 2. 建立 Neo4j Schema

```bash
cypher-shell -u neo4j -p <password> -f 01_ontology_schema/cypher/create_schema.cypher
```

## 3. 匯入 PdM 資料

```bash
python 03_execution/data_ingestion_etl.py --config config/pdm_demo.yaml
```

## 4. 執行異常偵測與工單觸發

```bash
python 03_execution/anomaly_detection_logic.py --demo ahu12
python 03_execution/workflow_trigger_api.py --demo ahu12
```

## 5. 重現 TTA 與效能指標

```bash
cd 04_validation
jupyter notebook notebooks/analysis.ipynb
```

依照 notebook 指引執行各個 cell，即可產出與論文相對應之統計表與圖形。  
