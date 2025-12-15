# Evaluation Results (RESULTS)

This directory contains all evaluation datasets used to validate the proposed
Semantic Action Management (SAM) framework and its STRIDE-based implementation.
The datasets correspond directly to the quantitative metrics reported in
Chapter 6 of the dissertation and are organized by metric type to ensure
clarity, traceability, and reproducibility.

All datasets in this directory represent **evaluation artifacts** derived
from system execution, controlled simulations, or structured measurements.
They are not raw input data. Raw or semi-processed input data can be found
under `02_data/`.

---

## Directory Structure and Correspondence to Chapter 6

### 1. Trigger-to-Action Latency (TTA)
**Path:** `RESULTS/TTA/`

This folder contains datasets measuring the end-to-end latency from event
detection to action initiation in predictive maintenance (PdM) scenarios.

- Event-level latency distributions for baseline (polling-based) and
  SAM (event-driven) pipelines
- Aggregated statistics used for comparative analysis

**Corresponding sections:**  
Chapter 6 – Event-to-Action Responsiveness Evaluation

---

### 2. Latency Decomposition (L1–L4)
**Path:** `RESULTS/Latency_Decomposition_L1_L4/`

These datasets decompose total decision latency into four semantic stages:
detection, reasoning, dispatch, and execution (L1–L4), enabling fine-grained
analysis of where performance gains are achieved.

**Corresponding sections:**  
Chapter 6 – Latency Decomposition and Pipeline Analysis

---

### 3. Provenance Replay Latency
**Path:** `RESULTS/Provenance_Replay/`

This dataset evaluates the time required to replay and reconstruct past
decisions using provenance information, reflecting auditability and
explainability of the decision pipeline.

**Corresponding sections:**  
Chapter 6 – Provenance-Based Explainability and Replay

---

### 4. Portability and Setup Effort
**Path:** `RESULTS/Portability_Setup_Effort/`

This dataset compares the setup complexity and deployment effort required
to instantiate decision pipelines across systems, reflecting portability
and configuration overhead.

**Corresponding sections:**  
Chapter 6 – System Portability and Deployment Effort

---

### 5. Traceability Coverage
**Path:** `RESULTS/Traceability_Coverage/`

This dataset reports the proportion of system actions that can be fully
traced back to triggering events, semantic reasoning steps, and executed
actions, reflecting governance completeness.

**Corresponding sections:**  
Chapter 6 – Traceability and Governance Coverage

---

### 6. Compensation Funnel
**Path:** `RESULTS/Compensation_Funnel/`

This dataset captures the multi-stage progression from detected anomalies
to compensable tasks and successful recovery actions, reflecting operational
resilience and closure efficiency.

**Corresponding sections:**  
Chapter 6 – Compensation and Operational Recovery

---

### 7. Loss Rate
**Path:** `RESULTS/Loss_Rate/`

This dataset quantifies the proportion of detected events that fail to
materialize into executable actions, capturing decision robustness and
pipeline reliability beyond latency-based metrics.

**Corresponding sections:**  
Chapter 6 – Loss Rate and Decision Robustness

---

## Methodological Note

All evaluation datasets were generated following the same execution logic,
event frequency, and orchestration structure as implemented in the STRIDE
testbed. Where controlled or synthetic data were used, generation strictly
followed the operational behavior of the deployed system to ensure
methodological consistency and reproducibility.

For details on system execution and workflow orchestration, please refer to:
- `03_execution/`
- `05_workflows/`

---

## Usage

These datasets are intended to be directly consumable by visualization and
analysis tools such as Power BI, Excel, or Jupyter notebooks located under
`04_validation/notebooks/`. Each dataset can be independently inspected,
visualized, or re-analyzed to reproduce the figures and tables reported
in the dissertation.
