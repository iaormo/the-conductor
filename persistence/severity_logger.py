#!/usr/bin/env python3
"""
severity_logger.py — the-conductor persistence layer
Logs all agent findings to SQLite with severity classification.

Usage (from agents via ruflo hooks):
    python3 persistence/severity_logger.py --event finding --data '{"agent": ...}'

Usage (from Claude Code agents directly):
    from persistence.severity_logger import log_finding, get_findings
"""

import sqlite3
import json
import argparse
import sys
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "audit.db"

VALID_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
VALID_CATEGORIES = {
    "injection", "authentication", "authorization", "cryptography",
    "misconfiguration", "secrets-exposure", "dependency", "api-security",
    "network", "iam", "compliance", "privacy", "policy", "forensics",
    "threat", "incident", "infrastructure", "code-quality", "other"
}

# ANSI colors for terminal output
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

SEVERITY_COLOR = {
    "CRITICAL": RED + BOLD,
    "HIGH": RED,
    "MEDIUM": YELLOW,
    "LOW": CYAN,
    "INFO": GREEN,
}


def init_db(db_path=None):
    """Initialize the SQLite database and create tables if not exist."""
    path = db_path or DB_PATH
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS findings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id    TEXT NOT NULL,
            agent_name  TEXT NOT NULL,
            team        TEXT NOT NULL,
            severity    TEXT NOT NULL,
            category    TEXT NOT NULL,
            title       TEXT NOT NULL,
            detail      TEXT,
            reference   TEXT,
            remediation TEXT,
            file_path   TEXT,
            line_number INTEGER,
            status      TEXT DEFAULT 'open',
            created_at  TEXT NOT NULL,
            updated_at  TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS audits (
            id          TEXT PRIMARY KEY,
            target      TEXT,
            started_at  TEXT NOT NULL,
            completed_at TEXT,
            status      TEXT DEFAULT 'running',
            summary     TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id    TEXT,
            event_type  TEXT NOT NULL,
            agent_name  TEXT,
            payload     TEXT,
            created_at  TEXT NOT NULL
        )
    """)

    conn.commit()
    return conn


def get_or_create_audit(conn, audit_id=None, target=None):
    """Get existing audit or create a new one."""
    if not audit_id:
        audit_id = datetime.utcnow().strftime("audit-%Y%m%d-%H%M%S")

    c = conn.cursor()
    c.execute("SELECT id FROM audits WHERE id = ?", (audit_id,))
    row = c.fetchone()

    if not row:
        now = datetime.utcnow().isoformat() + "Z"
        c.execute(
            "INSERT INTO audits (id, target, started_at, status) VALUES (?, ?, ?, ?)",
            (audit_id, target or "unknown", now, "running")
        )
        conn.commit()

    return audit_id


def log_finding(
    agent_name,
    team,
    severity,
    category,
    title,
    detail=None,
    reference=None,
    remediation=None,
    file_path=None,
    line_number=None,
    audit_id=None,
    db_path=None,
):
    """
    Log a security finding to the database.

    Args:
        agent_name:   Name of the agent reporting (e.g. 'sast-engineer')
        team:         Team identifier (e.g. 'software-security')
        severity:     CRITICAL | HIGH | MEDIUM | LOW | INFO
        category:     Finding category (e.g. 'injection', 'misconfiguration')
        title:        Short description of the finding
        detail:       Full detail / evidence
        reference:    CVE, CWE, OWASP reference (e.g. 'CWE-89', 'OWASP-A03:2021')
        remediation:  Recommended fix
        file_path:    Affected file path
        line_number:  Affected line number
        audit_id:     Audit session ID (auto-created if None)
        db_path:      Override default DB path

    Returns:
        int: finding ID
    """
    severity = severity.upper()
    if severity not in VALID_SEVERITIES:
        raise ValueError(f"Invalid severity '{severity}'. Must be one of {VALID_SEVERITIES}")

    category = category.lower()
    if category not in VALID_CATEGORIES:
        category = "other"

    conn = init_db(db_path)
    audit_id = get_or_create_audit(conn, audit_id)
    now = datetime.utcnow().isoformat() + "Z"

    c = conn.cursor()
    c.execute("""
        INSERT INTO findings
        (audit_id, agent_name, team, severity, category, title, detail,
         reference, remediation, file_path, line_number, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        audit_id, agent_name, team, severity, category, title, detail,
        reference, remediation, file_path, line_number, now, now
    ))
    conn.commit()
    finding_id = c.lastrowid
    conn.close()

    color = SEVERITY_COLOR.get(severity, "")
    print(f"  {color}[{severity}]{RESET} {title} — {agent_name}")

    return finding_id


def get_findings(severity=None, team=None, audit_id=None, db_path=None):
    """Query findings from the database."""
    conn = init_db(db_path)
    c = conn.cursor()

    query = "SELECT * FROM findings WHERE 1=1"
    params = []

    if severity:
        query += " AND severity = ?"
        params.append(severity.upper())
    if team:
        query += " AND team = ?"
        params.append(team)
    if audit_id:
        query += " AND audit_id = ?"
        params.append(audit_id)

    query += " ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 WHEN 'LOW' THEN 4 ELSE 5 END"

    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def log_event(event_type, agent_name=None, payload=None, audit_id=None, db_path=None):
    """Log a lifecycle event (task_complete, audit_complete, etc.)."""
    conn = init_db(db_path)
    audit_id = get_or_create_audit(conn, audit_id)
    now = datetime.utcnow().isoformat() + "Z"

    c = conn.cursor()
    c.execute("""
        INSERT INTO events (audit_id, event_type, agent_name, payload, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        audit_id, event_type, agent_name,
        json.dumps(payload) if payload else None,
        now
    ))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# CLI (called by ruflo hooks)
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="the-conductor severity logger")
    parser.add_argument("--event", required=True,
                        choices=["finding", "task_complete", "audit_complete"],
                        help="Event type")
    parser.add_argument("--data", help="JSON payload (for finding events)")
    parser.add_argument("--audit-id", help="Audit session ID")
    parser.add_argument("--db", help="Override DB path")

    args = parser.parse_args()

    if args.event == "finding" and args.data:
        try:
            data = json.loads(args.data)
            log_finding(
                agent_name=data.get("agent_name", "unknown"),
                team=data.get("team", "unknown"),
                severity=data.get("severity", "INFO"),
                category=data.get("category", "other"),
                title=data.get("title", "Untitled finding"),
                detail=data.get("detail"),
                reference=data.get("reference"),
                remediation=data.get("remediation"),
                file_path=data.get("file_path"),
                line_number=data.get("line_number"),
                audit_id=args.audit_id,
                db_path=args.db,
            )
        except json.JSONDecodeError as e:
            print(f"Error parsing --data JSON: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.event in ("task_complete", "audit_complete"):
        payload = json.loads(args.data) if args.data else {}
        log_event(args.event, payload=payload, audit_id=args.audit_id, db_path=args.db)
        print(f"  Event logged: {args.event}")
    else:
        print("No action taken. Use --event finding with --data JSON.")


if __name__ == "__main__":
    main()
