// ===================================================================
// STRIDE / SAM — Core Graph Schema Creation Script
// Author: Chien-Pu Huang
// Description: Creates essential node labels and relationship types
// ===================================================================

// -------------------------------
// Node Labels Initialization
// -------------------------------
CREATE (:_SchemaInit);

// Building / Spatial entities
CREATE (:BuildingComponent);
CREATE (:Space);
CREATE (:Zone);

// Sensor & Observation entities
CREATE (:Sensor);
CREATE (:PerformanceData);

// PdM / Workflow entities
CREATE (:Anomaly);
CREATE (:MaintenanceTask);
CREATE (:WorkflowRun);

// Actor / Provenance entities
CREATE (:Actor);
CREATE (:Organization);
CREATE (:Activity);
CREATE (:Entity);
CREATE (:Agent);

// -------------------------------
// Relationship Types (implicit declaration)
// -------------------------------
// MONITORS        (Sensor → BuildingComponent)
// LOCATED_IN      (BuildingComponent → Space / Zone)
// GENERATES       (Sensor → PerformanceData)
// GENERATES       (PerformanceData → Anomaly)
// TRIGGERS        (Anomaly → MaintenanceTask)
// RESOLVES        (MaintenanceTask → BuildingComponent)
// ASSIGNED_TO     (MaintenanceTask → Actor)
// EXECUTED_BY     (WorkflowRun → Actor)
// HAS_PROVENANCE  (Any → Provenance Node)

// This script prepares the labels and core relationship vocabulary.
// Data ingestion + constraints are defined in separate scripts.

RETURN "Schema labels initialized.";
