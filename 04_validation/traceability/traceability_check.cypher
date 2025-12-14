// traceability_check.cypher
// ------------------------------------------------------------
// Purpose:
//   Validate traceability (PROV-style evidence chain + TIAA/SAM chain)
//   across domains (PdM_HVAC and Carbon_SIDCM) in a Neo4j graph.
//
// How to use:
//   1) Open Neo4j Browser
//   2) (Optional) Run Section 0 to inspect labels/relationship-types
//   3) Run Section 1 (generic PROV checks)
//   4) Run Section 2 (TIAA/SAM chain checks)
//   5) If your schema uses different labels/relationships, use Section 0 outputs
//      to adjust the patterns in Sections 1–2.
//
// Notes:
//   - This script is intentionally "schema-discovery-friendly".
//   - It includes discovery queries + two alternative chain patterns.
//
// ------------------------------------------------------------

// ============================================================
// 0) Schema discovery (run first if you are unsure about labels/rels)
// ============================================================

// 0.1 List node labels (top 30 by count)
CALL db.labels() YIELD label
CALL {
  WITH label
  MATCH (n) WHERE label IN labels(n)
  RETURN label AS lbl, count(n) AS cnt
}
RETURN lbl AS label, cnt
ORDER BY cnt DESC
LIMIT 30;

// 0.2 List relationship types (top 30 by count)
CALL db.relationshipTypes() YIELD relationshipType
CALL {
  WITH relationshipType
  MATCH ()-[r]->() WHERE type(r) = relationshipType
  RETURN relationshipType AS rel, count(r) AS cnt
}
RETURN rel AS relationship_type, cnt
ORDER BY cnt DESC
LIMIT 30;

// 0.3 If you tag domain/scenario in properties, check available values
//     (edit property key if you use scenario/domain/caseStudy/etc.)
MATCH (n)
WHERE exists(n.scenario)
RETURN n.scenario AS scenario, count(*) AS nodes
ORDER BY nodes DESC
LIMIT 20;


// ============================================================
// 1) PROV-style traceability checks (generic)
// ============================================================

// Assumed (common) PROV-ish labels:
//   Entity, Activity, Agent
// Assumed (common) PROV-ish relationships (aliases in different datasets):
//   :USED / :used
//   :WAS_GENERATED_BY / :wasGeneratedBy
//   :WAS_ASSOCIATED_WITH / :wasAssociatedWith
//
// If your graph uses different names, use Section 0.2 output to update.

// 1.1 Coverage: counts of Entity/Activity/Agent
MATCH (e:Entity) RETURN 'Entity' AS type, count(e) AS cnt
UNION ALL
MATCH (a:Activity) RETURN 'Activity' AS type, count(a) AS cnt
UNION ALL
MATCH (ag:Agent) RETURN 'Agent' AS type, count(ag) AS cnt;

// 1.2 Evidence chain existence: Agent -> Activity -> Entity
//     Pattern: (ag)-[:WAS_ASSOCIATED_WITH]->(act)-[:USED]->(ent)
MATCH (ag:Agent)-[r1]->(act:Activity)-[r2]->(ent:Entity)
WHERE toUpper(type(r1)) IN ['WAS_ASSOCIATED_WITH','WASASSOCIATEDWITH','ASSOCIATED_WITH','ASSOCIATEDWITH']
  AND toUpper(type(r2)) IN ['USED','USES']
RETURN
  count(*) AS chain_count,
  count(DISTINCT ag) AS agents,
  count(DISTINCT act) AS activities,
  count(DISTINCT ent) AS entities;

// 1.3 Evidence generation: Activity -> Entity (generated)
MATCH (act:Activity)-[r]->(ent:Entity)
WHERE toUpper(type(r)) IN ['WAS_GENERATED_BY','WASGENERATEDBY','GENERATES','CREATED','PRODUCES']
RETURN
  count(*) AS generated_links,
  count(DISTINCT act) AS activities,
  count(DISTINCT ent) AS entities;

// 1.4 Sample 10 provenance subgraphs for visual inspection (Browser graph view)
MATCH p=(ag:Agent)-[r1]->(act:Activity)-[r2]->(ent:Entity)
WHERE toUpper(type(r1)) IN ['WAS_ASSOCIATED_WITH','WASASSOCIATEDWITH','ASSOCIATED_WITH','ASSOCIATEDWITH']
  AND toUpper(type(r2)) IN ['USED','USES']
RETURN p
LIMIT 10;


// ============================================================
// 2) TIAA / SAM traceability checks (Trigger–Issue–Action–Actor)
// ============================================================

// This section provides TWO common patterns.
// Choose the one that matches your schema; or adjust after running Section 0.
//
// Pattern A (relationship-centric, common in SAM/STRIDE papers):
//   (Trigger)-[:RAISES|:TRIGGERS]->(Issue)-[:RECOMMENDS|:LEADS_TO]->(Action)-[:ASSIGNED_TO]->(Actor)
//
// Pattern B (event->task->action, common in automation pipelines):
//   (Event)-[:TRIGGERS]->(Task)-[:EXECUTES]->(Action)-[:PERFORMED_BY]->(Actor)

// ---------------------------
// 2.A Pattern A
// ---------------------------
MATCH p=(t:Trigger)-[r1]->(i:Issue)-[r2]->(a:Action)-[r3]->(ac:Actor)
WHERE toUpper(type(r1)) IN ['TRIGGERS','RAISES','EMITS','INITIATES']
  AND toUpper(type(r2)) IN ['LEADS_TO','RECOMMENDS','RESULTS_IN','TRIGGERS']
  AND toUpper(type(r3)) IN ['ASSIGNED_TO','RESPONSIBLE_FOR','PERFORMED_BY','EXECUTED_BY']
RETURN
  count(*) AS tiaa_chains,
  count(DISTINCT t) AS triggers,
  count(DISTINCT i) AS issues,
  count(DISTINCT a) AS actions,
  count(DISTINCT ac) AS actors;

// Sample 10 chains for inspection
MATCH p=(t:Trigger)-[r1]->(i:Issue)-[r2]->(a:Action)-[r3]->(ac:Actor)
WHERE toUpper(type(r1)) IN ['TRIGGERS','RAISES','EMITS','INITIATES']
  AND toUpper(type(r2)) IN ['LEADS_TO','RECOMMENDS','RESULTS_IN','TRIGGERS']
  AND toUpper(type(r3)) IN ['ASSIGNED_TO','RESPONSIBLE_FOR','PERFORMED_BY','EXECUTED_BY']
RETURN p
LIMIT 10;

// ---------------------------
// 2.B Pattern B
// ---------------------------
MATCH p=(e:Event)-[r1]->(t:Task)-[r2]->(a:Action)-[r3]->(ac:Actor)
WHERE toUpper(type(r1)) IN ['TRIGGERS','GENERATES','CREATES','EMITS']
  AND toUpper(type(r2)) IN ['EXECUTES','LEADS_TO','TRIGGERS','PRODUCES']
  AND toUpper(type(r3)) IN ['PERFORMED_BY','ASSIGNED_TO','EXECUTED_BY','RESPONSIBLE_FOR']
RETURN
  count(*) AS event_task_action_actor_chains,
  count(DISTINCT e) AS events,
  count(DISTINCT t) AS tasks,
  count(DISTINCT a) AS actions,
  count(DISTINCT ac) AS actors;

// Sample 10 chains for inspection
MATCH p=(e:Event)-[r1]->(t:Task)-[r2]->(a:Action)-[r3]->(ac:Actor)
WHERE toUpper(type(r1)) IN ['TRIGGERS','GENERATES','CREATES','EMITS']
  AND toUpper(type(r2)) IN ['EXECUTES','LEADS_TO','TRIGGERS','PRODUCES']
  AND toUpper(type(r3)) IN ['PERFORMED_BY','ASSIGNED_TO','EXECUTED_BY','RESPONSIBLE_FOR']
RETURN p
LIMIT 10;


// ============================================================
// 3) Cross-domain sanity checks (PdM vs Carbon) — optional
// ============================================================

// If you use a 'scenario' property (recommended), compare chain counts by scenario.
// Edit the property key if needed.
MATCH (n)
WHERE exists(n.scenario)
WITH collect(DISTINCT n.scenario) AS scenarios
RETURN scenarios AS available_scenarios;

// Compare TIAA chain counts by scenario (Pattern B example)
MATCH (e:Event)-[r1]->(t:Task)-[r2]->(a:Action)-[r3]->(ac:Actor)
WHERE exists(e.scenario)
  AND toUpper(type(r1)) IN ['TRIGGERS','GENERATES','CREATES','EMITS']
  AND toUpper(type(r2)) IN ['EXECUTES','LEADS_TO','TRIGGERS','PRODUCES']
  AND toUpper(type(r3)) IN ['PERFORMED_BY','ASSIGNED_TO','EXECUTED_BY','RESPONSIBLE_FOR']
RETURN e.scenario AS scenario, count(*) AS chain_count
ORDER BY chain_count DESC;
