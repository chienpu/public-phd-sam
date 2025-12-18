# (6) Effective Throughput Evaluation

This module evaluates the **effective throughput** of the system, measuring how many tasks can be
**successfully completed per unit time** under different architectural designs.
Unlike raw processing rate, the proposed throughput metric explicitly accounts for
task correctness, compensation success, and system stability.

---

## 1. Motivation

While latency-related metrics (e.g., TTA and layer-wise latency decomposition) capture
**responsiveness**, they do not reflect the system’s ability to sustain task processing
under continuous workload.

Throughput is therefore introduced as a **capacity-level performance indicator**, answering:

> *How many tasks can the system reliably complete within a given time window?*

To avoid inflated performance claims, throughput is computed **only based on successfully
recovered tasks**, not merely triggered or dispatched tasks.

---

## 2. Definition of Effective Throughput

Effective Throughput is defined as:

\[
\mathrm{Throughput}_{\mathrm{eff}} =
\frac{N_{\mathrm{completed}}}{\Delta t}
\]

where:

- \( N_{\mathrm{completed}} \): Number of tasks that reach the
  *Successfully Recovered* state
- \( \Delta t \): Observation time window (in minutes)

This definition ensures that throughput reflects **end-to-end task success**, rather than
intermediate execution events.

---

## 3. Data Sources and Dependencies

The throughput metric is derived by integrating results from multiple evaluation modules:

| Source Module | Role in Throughput Computation |
|---------------|--------------------------------|
| `Compensation_Funnel` | Provides number of successfully recovered tasks |
| `Latency_Decomposition_L1_L4` | Defines observation time window |
| `Loss_Rate` | Verifies that tasks are not dropped silently |
| `Traceability_Coverage` | Ensures tasks are structurally traceable |
| `Provenance_Replay` | Confirms auditability of task completion |

Throughput results are **only considered valid** when loss rate is negligible and
traceability coverage exceeds the defined threshold.

---

## 4. Computation Procedure

1. **Select observation window**  
   A fixed time window \(\Delta t\) (e.g., 60 minutes) is used for both architectures.

2. **Extract completed task count**  
   From `compensation_funnel.csv`, obtain the number of
   *Successfully Recovered Tasks* for each framework.

3. **Compute effective throughput**  
   \[
   \mathrm{Throughput}_{\mathrm{eff}} =
   \frac{N_{\mathrm{successfully\ recovered}}}{\Delta t}
   \]

4. **Cross-check with stability metrics**  
   Ensure:
   - Loss rate is within acceptable bounds
   - No artificial throughput gain due to task skipping or silent failure

---

## 5. Output Files

### 5.1 Final CSV (Paper-Ready)

```csv
framework,time_window_min,completed_tasks,throughput_tasks_per_min
Baseline,60,18,0.30
SAM,60,102,1.70
```
Each row represents one architectural configuration

Values are normalized to tasks per minute for cross-case comparability

5.2 Visualization
Recommended visualization:
 - Bar chart comparing effective throughput across frameworks
 - Optional annotation linking throughput gains to compensation hit rate

6. Interpretation Guidance
 - Higher throughput under SAM reflects structural automation, not aggressive batching
 - Throughput improvement is interpreted jointly with:
    - Compensation Hit Rate
    - Latency reduction
    - Provenance completeness
This avoids misleading conclusions based on raw processing speed alone.

7. Reproducibility Notes
 - All throughput values can be recomputed directly from raw CSV files
 - No manual aggregation or hidden normalization steps are used
 - Time window definition is explicitly documented and fixed across experiments

8. Summary
Effective Throughput serves as a system-level synthesis metric, consolidating
correctness, responsiveness, and stability into a single capacity-oriented indicator.
It complements latency-based metrics and provides a holistic view of operational scalability.


---
