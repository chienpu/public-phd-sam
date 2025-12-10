// ===================================================================
// STRIDE / SAM — Constraints and Index Creation Script
// Author: Chien-Pu Huang
// Description: Creates unique constraints and indexes required for
//              reasoning, ingestion, performance testing & provenance.
// ===================================================================

// -------------------------------
// Unique Identity Constraints
// -------------------------------

// BuildingComponent
CREATE CONSTRAINT building_component_id IF NOT EXISTS
FOR (c:BuildingComponent)
REQUIRE c.ComponentId IS UNIQUE;

// Sensor
CREATE CONSTRAINT sensor_id IF NOT EXISTS
FOR (s:Sensor)
REQUIRE s.SensorId IS UNIQUE;

// MaintenanceTask
CREATE CONSTRAINT task_id IF NOT EXISTS
FOR (t:MaintenanceTask)
REQUIRE t.TaskId IS UNIQUE;

// Actor
CREATE CONSTRAINT actor_id IF NOT EXISTS
FOR (a:Actor)
REQUIRE a.ActorId IS UNIQUE;

// Anomaly (optional but recommended)
CREATE CONSTRAINT anomaly_id IF NOT EXISTS
FOR (a:Anomaly)
REQUIRE a.AnomalyId IS UNIQUE;

// WorkflowRun
CREATE CONSTRAINT workflow_run_id IF NOT EXISTS
FOR (w:WorkflowRun)
REQUIRE w.RunId IS UNIQUE;


// -------------------------------
// Indexes for Performance
// -------------------------------

// Timestamp index for PerformanceData
// Needed for retrieval of the latest readings and anomaly detection
CREATE INDEX perf_timestamp IF NOT EXISTS
FOR (d:PerformanceData)
ON (d.timestamp);

// Timestamp index for Anomaly
CREATE INDEX anomaly_timestamp IF NOT EXISTS
FOR (a:Anomaly)
ON (a.timestamp);

// Timestamp index for WorkflowRun (TTA measurement)
CREATE INDEX workflow_timestamp IF NOT EXISTS
FOR (w:WorkflowRun)
ON (w.timestamp);


// -------------------------------
// Optional Indexes (recommended)
// -------------------------------

// Index for Sensor type-based reasoning
CREATE INDEX sensor_type IF NOT EXISTS
FOR (s:Sensor)
ON (s.type);

// Index for BuildingComponent type
CREATE INDEX component_type IF NOT EXISTS
FOR (c:BuildingComponent)
ON (c.type);


// -------------------------------
// Notes
// -------------------------------
// - These constraints ensure graph integrity for PdM + SID-CM experiments.
// - Timestamp indexes significantly accelerate multi-hop traversal.
// - Additional indexes can be added based on dataset size (>30K nodes).
// - This file can be executed independently after create_schema.cypher.
//

RETURN "All constraints and indexes created.";
