#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
utils/neo4j_helper.py

Neo4j 操作封裝：
- 建立 driver/session
- query()
- merge_nodes()
- merge_rels()

設計原則：
- 對 replication 友善：以 MERGE 為主，避免重複匯入
- 允許在未安裝 neo4j driver 時 graceful fallback
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

def neo4j_available() -> bool:
    try:
        import neo4j  # noqa
        return True
    except Exception:
        return False

@dataclass
class Neo4jHelper:
    uri: str
    user: str
    password: str
    database: Optional[str] = None

    @classmethod
    def from_config(cls, cfg: Dict[str, Any]) -> "Neo4jHelper":
        return cls(
            uri=cfg.get("uri", "bolt://localhost:7687"),
            user=cfg.get("user", "neo4j"),
            password=cfg.get("password", "neo4j"),
            database=cfg.get("database", None),
        )

    def _driver(self):
        from neo4j import GraphDatabase
        return GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def session(self):
        driver = self._driver()
        if self.database:
            return driver.session(database=self.database)
        return driver.session()

    def query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        params = params or {}
        with self.session() as s:
            res = s.run(cypher, params)
            return [dict(r) for r in res]

    def merge_nodes(self, label: str, key: str, rows: List[Dict[str, Any]], batch_size: int = 1000):
        if not rows:
            return
        q = f"""
        UNWIND $rows AS row
        MERGE (n:{label} {{{key}: row.{key}}})
        SET n += row
        """
        for i in range(0, len(rows), batch_size):
            chunk = rows[i:i+batch_size]
            self.query(q, {"rows": chunk})

    def merge_rels(
        self,
        src_label: str,
        src_key: str,
        tgt_label: str,
        tgt_key: str,
        pairs: Sequence[Tuple[str, str]],
        rel_type: str,
        batch_size: int = 2000
    ):
        if not pairs:
            return
        q = f"""
        UNWIND $pairs AS p
        MATCH (s:{src_label} {{{src_key}: p[0]}})
        MATCH (t:{tgt_label} {{{tgt_key}: p[1]}})
        MERGE (s)-[r:{rel_type}]->(t)
        """
        for i in range(0, len(pairs), batch_size):
            chunk = pairs[i:i+batch_size]
            self.query(q, {"pairs": chunk})
