
# Reproducibility Checklist

本清單有助於確認是否具備重現實驗所需的所有條件。

- [ ] Neo4j 版本已記錄（4.x 或 5.x）
- [ ] Python 版本已記錄（3.8+）
- [ ] 所有套件由 `requirements.txt` 安裝
- [ ] 已執行 `01_ontology_schema/cypher/create_schema.cypher`
- [ ] `02_data/` 內資料完整且未被修改
- [ ] `03_execution/` 腳本可成功連線 Neo4j
- [ ] Workflow URL（Power Automate / n8n）已設定於設定檔
- [ ] 所有實驗輸出均儲存在 `04_validation/RESULTS/`
- [ ] Notebook `04_validation/notebooks/analysis.ipynb` 可順利執行完畢
- [ ] 實驗環境（OS、CPU、Memory）基本資訊已另行記錄（建議）
