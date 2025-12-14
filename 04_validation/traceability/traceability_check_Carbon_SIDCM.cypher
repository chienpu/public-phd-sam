
// =====================================================
// Carbon_SIDCM Traceability Check (Building × Month)
// Purpose:
//   Validate semantic provenance chain:
//   Building -> EnergyFlow -> EmissionRecord
// Scenario:
//   Carbon_SIDCM
// =====================================================

// -------------------------------
// Section 0: Schema Overview
// -------------------------------
CALL db.labels();
CALL db.relationshipTypes();

// -------------------------------
// Section 1: Building → EnergyFlow → EmissionRecord Chain
// -------------------------------
MATCH (b:Building)-[r1:CONSUMES_ENERGY]->(e:EnergyFlow)-[r2:GENERATES_EMISSION]->(c:EmissionRecord)
WHERE b.scenario = 'Carbon_SIDCM'
RETURN
  b.name            AS building,
  e.name            AS energy_flow,
  c.name            AS emission_record,
  r1.relationship_type AS consumes_rel,
  r2.relationship_type AS generates_rel
LIMIT 50;

// -------------------------------
// Section 2: Missing Provenance Detection
// -------------------------------
// EnergyFlow without Building
MATCH (e:EnergyFlow)
WHERE NOT ( (:Building)-[:CONSUMES_ENERGY]->(e) )
  AND e.scenario = 'Carbon_SIDCM'
RETURN e.node_id AS orphan_energy_flow;

// EmissionRecord without EnergyFlow
MATCH (c:EmissionRecord)
WHERE NOT ( (:EnergyFlow)-[:GENERATES_EMISSION]->(c) )
  AND c.scenario = 'Carbon_SIDCM'
RETURN c.node_id AS orphan_emission_record;

// -------------------------------
// Section 3: Monthly Coverage Check
// -------------------------------
// Count EnergyFlow records per month
MATCH (e:EnergyFlow)
WHERE e.scenario = 'Carbon_SIDCM'
WITH split(e.name, '_')[-1] AS month, count(e) AS records
RETURN month, records
ORDER BY month;

// -------------------------------
// Section 4: Trace Path Visualization
// -------------------------------
MATCH p = (b:Building)-[:CONSUMES_ENERGY]->(e:EnergyFlow)-[:GENERATES_EMISSION]->(c:EmissionRecord)
WHERE b.scenario = 'Carbon_SIDCM'
RETURN p
LIMIT 25;
