// ===================================================================
// STRIDE / SAM — Semantic Reasoning Examples
// Author: Chien-Pu Huang
// Description: Semantic reasoning rules used by STRIDE for PdM,
//              anomaly detection, multi-hop traceability, and risk scoring.
// ===================================================================


// --------------------------------------------------------------
// 1. 複合異常推理：能源與溫度同時超標
//    Composite anomaly (Energy + Temperature)
// --------------------------------------------------------------
MATCH (c:BuildingComponent)<-[:MONITORS]-(temp:Sensor {type:"Temperature"})
     -[:GENERATES]->(td:PerformanceData),
      (c)<-[:MONITORS]-(energy:Sensor {type:"Energy"})
     -[:GENERATES]->(ed:PerformanceData)
WHERE td.timestamp = ed.timestamp
  AND td.value > c.avg_temp
  AND ed.value > c.avg_energy
WITH c, td, ed,
     apoc.create.uuid() AS anomalyId
CREATE (a:Anomaly {
    AnomalyId: anomalyId,
    timestamp: td.timestamp,
    type: "Composite_Temp_Energy_Overload",
    severity: (td.value - c.avg_temp) + (ed.value - c.avg_energy)
})
MERGE (temp)-[:GENERATES]->(a)
MERGE (energy)-[:GENERATES]->(a)
MERGE (a)-[:AFFECTS]->(c)
RETURN a, c;


// --------------------------------------------------------------
// 2. 重複異常偵測：同設備 7 天內至少三次異常
//    Repetitive anomaly detection
// --------------------------------------------------------------
MATCH (c:BuildingComponent)<-[:AFFECTS]-(a:Anomaly)
WHERE a.timestamp > datetime() - duration("P7D")
WITH c, count(a) AS anomalyCount
WHERE anomalyCount >= 3
RETURN c.ComponentId AS Component,
       anomalyCount AS Frequency7Days
ORDER BY Frequency7Days DESC;


// --------------------------------------------------------------
// 3. 多跳追溯：工單 → 異常 → 量測 → Sensor
//    Multi-hop traceability (used in STRIDE evaluation)
// --------------------------------------------------------------
MATCH (t:MaintenanceTask {TaskId:$tid})<-[:TRIGGERS]-(a:Anomaly)
MATCH (a)<-[:GENERATES]-(pd:PerformanceData)<-[:GENERATES]-(s:Sensor)
RETURN t, a, pd, s
ORDER BY pd.timestamp DESC;


// --------------------------------------------------------------
// 4. PdM 風險分級：異常強度 × 發生頻率
//    Risk scoring (baseline version)
// --------------------------------------------------------------
MATCH (a:Anomaly)-[:AFFECTS]->(c:BuildingComponent)
WHERE a.timestamp > datetime() - duration("P3D")
WITH c,
     count(a) AS freq,
     avg(a.severity) AS avgSeverity
RETURN c.ComponentId AS Component,
       freq,
       avgSeverity,
       (freq * avgSeverity) AS RiskScore
ORDER BY RiskScore DESC;


// --------------------------------------------------------------
// 5. 溫度異常推斷：基準線偏差 + 上升速度
//    Temperature anomaly reasoning with rate-of-change
// --------------------------------------------------------------
MATCH (c:BuildingComponent)<-[:MONITORS]-(s:Sensor {type:"Temperature"})
     -[:GENERATES]->(d:PerformanceData)
WITH c, s, d
ORDER BY d.timestamp DESC
WITH c, collect(d)[0..3] AS recent
WHERE recent[0].value > c.avg_temp
  AND (recent[0].value - recent[2].value) > 3  // 3-degree rise
CREATE (a:Anomaly {
    AnomalyId: apoc.create.uuid(),
    timestamp: recent[0].timestamp,
    type: "Rapid_Temperature_Rise",
    severity: recent[0].value - c.avg_temp
})
MERGE (s)-[:GENERATES]->(a)
MERGE (a)-[:AFFECTS]->(c)
RETURN a, c;


// --------------------------------------------------------------
// 6. 能源效率下降：移動平均偏移 (SID-CM Optional Rule)
//    Energy efficiency degradation (baseline ML-free rule)
// --------------------------------------------------------------
MATCH (c:BuildingComponent)<-[:MONITORS]-(s:Sensor {type:"Energy"})
     -[:GENERATES]->(d:PerformanceData)
WITH c, s, d
ORDER BY d.timestamp DESC
WITH c, collect(d)[0..6] AS last7
WITH c,
     avg([x IN last7 | x.value]) AS movingAvg,
     last7[0].value AS currentVal
WHERE currentVal > movingAvg * 1.2
CREATE (a:Anomaly {
    AnomalyId: apoc.create.uuid(),
    timestamp: last7[0].timestamp,
    type: "Energy_Efficiency_Degradation",
    severity: currentVal - movingAvg
})
MERGE (s)-[:GENERATES]->(a)
MERGE (a)-[:AFFECTS]->(c)
RETURN a, c;


// --------------------------------------------------------------
// 7. 事件到行動的語意鏈：TIAA → workflow trigger
//    TIAA semantic chain (Trigger → Issue → Action → Actor)
// --------------------------------------------------------------
MATCH (a:Anomaly)-[:TRIGGERS]->(t:MaintenanceTask)
OPTIONAL MATCH (t)-[:ASSIGNED_TO]->(actor:Actor)
RETURN a AS Trigger,
       t AS Action,
       actor AS Actor
ORDER BY a.timestamp DESC
LIMIT 20;


// --------------------------------------------------------------
// End of File
// ===================================================================
