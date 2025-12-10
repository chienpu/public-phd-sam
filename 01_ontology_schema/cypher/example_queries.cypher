// ===================================================================
// STRIDE / SAM — Example Cypher Queries
// Author: Chien-Pu Huang
// Description: Basic queries demonstrating how to explore the ontology
//              and retrieve semantic information in STRIDE.
// ===================================================================


// --------------------------------------------------------------
// 1. 查詢某 Component 所有監測它的 Sensors
// --------------------------------------------------------------
MATCH (c:BuildingComponent {ComponentId: $cid })<-[:MONITORS]-(s:Sensor)
RETURN s
ORDER BY s.SensorId;


// --------------------------------------------------------------
// 2. 查詢某個 Sensor 生成的最新 PerformanceData
// --------------------------------------------------------------
MATCH (s:Sensor {SensorId: $sid})-[:GENERATES]->(d:PerformanceData)
RETURN d
ORDER BY d.timestamp DESC
LIMIT 1;


// --------------------------------------------------------------
// 3. 查詢某 Component 最新的 PerformanceData（跨所有 sensors）
// --------------------------------------------------------------
MATCH (c:BuildingComponent {ComponentId: $cid})<-[:MONITORS]-(s:Sensor)
MATCH (s)-[:GENERATES]->(d:PerformanceData)
RETURN d
ORDER BY d.timestamp DESC
LIMIT 1;


// --------------------------------------------------------------
// 4. 查詢某 Component 最近的 Anomaly
// --------------------------------------------------------------
MATCH (c:BuildingComponent {ComponentId: $cid})
      <-[:AFFECTS]-(:Anomaly)-[:GENERATES*0..1]-(:PerformanceData)
RETURN DISTINCT c, collect(a)[0]
ORDER BY a.timestamp DESC
LIMIT 1;


// --------------------------------------------------------------
// 5. 查詢某 Anomaly 觸發的維修工單
// --------------------------------------------------------------
MATCH (a:Anomaly {AnomalyId: $aid})-[:TRIGGERS]->(t:MaintenanceTask)
RETURN t;


// --------------------------------------------------------------
// 6. 查詢某工單（MaintenanceTask）的負責人
// --------------------------------------------------------------
MATCH (t:MaintenanceTask {TaskId: $tid})-[:ASSIGNED_TO]->(actor:Actor)
RETURN actor;


// --------------------------------------------------------------
// 7. 查詢某 Actor 所負責的所有工單
// --------------------------------------------------------------
MATCH (actor:Actor {ActorId: $aid})<-[:ASSIGNED_TO]-(t:MaintenanceTask)
RETURN t, actor
ORDER BY t.created_at DESC;


// --------------------------------------------------------------
// 8. 查詢從 Sensor → PerformanceData → Anomaly → Task 的完整鏈（Traceability Demo）
// --------------------------------------------------------------
MATCH (s:Sensor {SensorId: $sid})-[:GENERATES]->(d:PerformanceData)
OPTIONAL MATCH (d)-[:GENERATES]->(a:Anomaly)
OPTIONAL MATCH (a)-[:TRIGGERS]->(t:MaintenanceTask)
RETURN s, d, a, t
ORDER BY d.timestamp DESC
LIMIT 20;


// --------------------------------------------------------------
// 9. 查詢某 Component 最近 7 天內是否出現異常
// --------------------------------------------------------------
MATCH (c:BuildingComponent {ComponentId: $cid})<-[:AFFECTS]-(a:Anomaly)
WHERE a.timestamp > datetime() - duration("P7D")
RETURN a
ORDER BY a.timestamp DESC;


// --------------------------------------------------------------
// 10. 查詢所有 Components 及其異常次數（簡單統計）
// --------------------------------------------------------------
MATCH (c:BuildingComponent)<-[:AFFECTS]-(a:Anomaly)
WITH c, count(a) AS anomalyCount
RETURN c.ComponentId AS Component, anomalyCount
ORDER BY anomalyCount DESC;
