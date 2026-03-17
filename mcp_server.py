#!/usr/bin/env python3
"""
the-conductor MCP Server
Exposes the full 7-division orchestration system as MCP tools over SSE.
Deploy to Railway → connect from Claude Desktop / Claude Code.
"""

import os
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "persistence" / "audit.db"

mcp = FastMCP("the-conductor")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_db():
    """Get a DB connection, initializing tables if needed."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    # Ensure tables exist
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS findings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_id TEXT NOT NULL, agent_name TEXT NOT NULL, team TEXT NOT NULL,
            severity TEXT NOT NULL, category TEXT NOT NULL, title TEXT NOT NULL,
            detail TEXT, reference TEXT, remediation TEXT, file_path TEXT,
            line_number INTEGER, status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS audits (
            id TEXT PRIMARY KEY, target TEXT, started_at TEXT NOT NULL,
            completed_at TEXT, status TEXT DEFAULT 'running', summary TEXT
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, audit_id TEXT,
            event_type TEXT NOT NULL, agent_name TEXT, payload TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL,
            first_name TEXT, last_name TEXT, email TEXT, phone TEXT,
            linkedin TEXT, title TEXT, company TEXT, industry TEXT,
            company_size TEXT, status TEXT DEFAULT 'new', score INTEGER DEFAULT 0,
            notes TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT, client_name TEXT NOT NULL,
            service TEXT NOT NULL, status TEXT DEFAULT 'proposal', value REAL DEFAULT 0,
            start_date TEXT, end_date TEXT, milestones TEXT, notes TEXT,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT, project_id INTEGER,
            client_name TEXT NOT NULL, amount REAL NOT NULL,
            status TEXT DEFAULT 'draft', due_date TEXT, paid_date TEXT,
            line_items TEXT, notes TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
    """)
    conn.commit()
    return conn


def load_agent_md(name: str) -> str:
    """Load an agent's markdown definition."""
    path = BASE_DIR / ".claude" / "agents" / f"{name}.md"
    if path.exists():
        return path.read_text()
    return f"Agent '{name}' not found."


def load_command_md(name: str) -> str:
    """Load a command's markdown definition."""
    path = BASE_DIR / ".claude" / "commands" / f"{name}.md"
    if path.exists():
        return path.read_text()
    return f"Command '{name}' not found."


AGENTS = {
    "security": [
        "ciso-orchestrator", "sast-engineer", "dependency-auditor",
        "secure-code-reviewer", "api-security-analyst", "cloud-security-architect",
        "network-security-engineer", "secrets-iam-auditor", "compliance-analyst",
        "privacy-officer", "policy-enforcer", "ir-lead", "forensics-analyst",
        "threat-hunter", "risk-officer", "security-program-manager",
    ],
    "business-development": [
        "prospecting-agent", "lead-enrichment-agent",
        "outreach-sequencing-agent", "crm-sync-agent",
    ],
    "client-delivery": [
        "project-manager-agent", "sow-generator-agent",
        "invoice-agent", "client-reporting-agent",
    ],
    "development": [
        "code-generation-agent", "code-review-agent",
        "cicd-pipeline-agent", "documentation-agent",
    ],
    "data-analytics": [
        "data-extraction-agent", "bi-dashboard-agent",
        "market-research-agent", "competitive-intel-agent",
    ],
    "marketing": [
        "content-writer-agent", "email-campaign-agent",
        "social-media-agent", "seo-analyst-agent",
    ],
    "automation": [
        "workflow-automation-agent", "api-integration-agent",
        "scheduling-agent", "notification-alert-agent",
    ],
}

DIVISIONS = {
    "1-security": "16 agents: SAST, dependencies, code review, API, cloud, network, IAM, compliance, privacy, policy, IR, forensics, threat hunting, risk, program mgmt",
    "2-business-development": "4 agents: prospecting, lead enrichment, outreach sequencing, CRM sync",
    "3-client-delivery": "4 agents: project management, SOW generation, invoicing, client reporting",
    "4-development": "4 agents: code generation, code review, CI/CD pipelines, documentation",
    "5-data-analytics": "4 agents: data extraction, BI dashboards, market research, competitive intel",
    "6-marketing": "4 agents: content writing, email campaigns, social media, SEO",
    "7-automation": "4 agents: workflow automation, API integration, scheduling, alerts",
}

# ---------------------------------------------------------------------------
# MCP Tools — Orchestrator
# ---------------------------------------------------------------------------

@mcp.tool()
def orchestrate(command: str, target: str = ".", options: str = "") -> str:
    """
    Run a conductor command. This is the main entry point.

    Commands:
      full-audit          — Full 16-agent CISO security audit (all 4 teams)
      quick-scan          — Teams 2+3 only (software + infrastructure)
      compliance-gap      — Team 4 only (compliance audit)
      ir-triage           — Team 5 only (incident response)
      lead-gen            — Division 2 (prospecting pipeline)
      client-onboard      — Division 3 (client onboarding)
      dev-assist          — Division 4 (development assistance)
      data-research       — Division 5 (data & analytics)
      marketing-campaign  — Division 6 (marketing & content)
      automate-workflow   — Division 7 (automation)
      full-service        — All 7 divisions

    Args:
        command: The workflow command to run
        target: Target path, URL, or scope description
        options: Additional options (e.g. '--severity CRITICAL HIGH', '--skip-ir')
    """
    now = datetime.utcnow().isoformat() + "Z"
    audit_id = f"audit-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO audits (id, target, started_at, status) VALUES (?, ?, ?, ?)",
        (audit_id, target, now, "running"),
    )
    conn.commit()

    # Map command to divisions
    cmd_map = {
        "full-audit": ["security"],
        "quick-scan": ["security"],
        "compliance-gap": ["security"],
        "ir-triage": ["security"],
        "lead-gen": ["business-development"],
        "client-onboard": ["client-delivery"],
        "dev-assist": ["development"],
        "data-research": ["data-analytics"],
        "marketing-campaign": ["marketing"],
        "automate-workflow": ["automation"],
        "full-service": list(AGENTS.keys()),
    }

    divisions = cmd_map.get(command, ["security"])
    agents_involved = []
    for div in divisions:
        agents_involved.extend(AGENTS.get(div, []))

    # Load the command definition if it exists
    cmd_def = ""
    cmd_file = BASE_DIR / ".claude" / "commands" / f"{command}.md"
    if cmd_file.exists():
        cmd_def = cmd_file.read_text()

    # Load agent definitions for involved agents
    agent_briefs = []
    for agent_name in agents_involved:
        path = BASE_DIR / ".claude" / "agents" / f"{agent_name}.md"
        if path.exists():
            content = path.read_text()
            # Just get first 5 lines for brief
            lines = content.strip().split("\n")[:8]
            agent_briefs.append(f"### {agent_name}\n" + "\n".join(lines))

    # Log event
    c.execute(
        "INSERT INTO events (audit_id, event_type, agent_name, payload, created_at) VALUES (?, ?, ?, ?, ?)",
        (audit_id, "orchestrate_start", "mcp-server",
         json.dumps({"command": command, "target": target, "options": options, "agents": agents_involved}), now),
    )
    conn.commit()
    conn.close()

    result = f"""# the-conductor — Orchestration Initiated

**Audit ID**: {audit_id}
**Command**: {command}
**Target**: {target}
**Options**: {options or 'none'}
**Divisions activated**: {', '.join(divisions)}
**Agents involved** ({len(agents_involved)}): {', '.join(agents_involved)}

---

## Command Definition
{cmd_def if cmd_def else f'No specific command file for "{command}". Using default orchestration.'}

---

## Agent Briefs

{chr(10).join(agent_briefs)}

---

## Execution Instructions

You are the Master Orchestrator. Execute this command by:

1. **Scope** the target: read its structure, identify languages/frameworks
2. **Spawn teams in parallel** (batch all in ONE message):
{chr(10).join(f'   - {a}' for a in agents_involved)}
3. **Review findings** using two-stage review (scope compliance → quality)
4. **Synthesize** executive report
5. **Log all findings** via the `log_finding` tool

Use `get_findings` and `get_dashboard` to check progress.
"""
    return result


# ---------------------------------------------------------------------------
# MCP Tools — System Info
# ---------------------------------------------------------------------------

@mcp.tool()
def list_divisions() -> str:
    """List all 7 divisions and their agent counts."""
    lines = ["# the-conductor — Divisions\n"]
    for div, desc in DIVISIONS.items():
        lines.append(f"**{div}**: {desc}")
    lines.append(f"\n**Total agents**: 40")
    return "\n".join(lines)


@mcp.tool()
def list_agents(division: str = "") -> str:
    """
    List available agents. Optionally filter by division.

    Args:
        division: Filter by division name (e.g. 'security', 'marketing'). Empty = all.
    """
    lines = ["# the-conductor — Agents\n"]
    for div, agents in AGENTS.items():
        if division and division.lower() not in div.lower():
            continue
        lines.append(f"## {div} ({len(agents)} agents)")
        for a in agents:
            lines.append(f"  - {a}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def get_agent(name: str) -> str:
    """
    Get the full definition of a specific agent.

    Args:
        name: Agent name (e.g. 'ciso-orchestrator', 'threat-hunter')
    """
    return load_agent_md(name)


@mcp.tool()
def get_command(name: str) -> str:
    """
    Get the full definition of a workflow command.

    Args:
        name: Command name (e.g. 'full-audit', 'quick-scan', 'generate-report')
    """
    return load_command_md(name)


# ---------------------------------------------------------------------------
# MCP Tools — Findings (Security)
# ---------------------------------------------------------------------------

@mcp.tool()
def log_finding(
    agent_name: str,
    team: str,
    severity: str,
    category: str,
    title: str,
    detail: str = "",
    reference: str = "",
    remediation: str = "",
    file_path: str = "",
    line_number: int = 0,
    audit_id: str = "",
) -> str:
    """
    Log a security finding to the persistence layer.

    Args:
        agent_name: Agent reporting (e.g. 'sast-engineer')
        team: Team identifier (e.g. 'software-security', 'infrastructure')
        severity: CRITICAL | HIGH | MEDIUM | LOW | INFO
        category: Finding category (e.g. 'injection', 'misconfiguration', 'secrets-exposure')
        title: Short finding description
        detail: Full evidence and context
        reference: CVE/CWE/OWASP reference
        remediation: Recommended fix
        file_path: Affected file path
        line_number: Affected line number
        audit_id: Audit session ID (auto-created if empty)
    """
    severity = severity.upper()
    valid = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"}
    if severity not in valid:
        return f"Error: severity must be one of {valid}"

    conn = get_db()
    now = datetime.utcnow().isoformat() + "Z"

    if not audit_id:
        c = conn.cursor()
        c.execute("SELECT id FROM audits ORDER BY started_at DESC LIMIT 1")
        row = c.fetchone()
        audit_id = row["id"] if row else f"audit-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"

    c = conn.cursor()
    # Ensure audit exists
    c.execute("SELECT id FROM audits WHERE id = ?", (audit_id,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO audits (id, target, started_at, status) VALUES (?, ?, ?, ?)",
            (audit_id, "unknown", now, "running"),
        )

    c.execute("""
        INSERT INTO findings
        (audit_id, agent_name, team, severity, category, title, detail,
         reference, remediation, file_path, line_number, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        audit_id, agent_name, team, severity, category, title, detail,
        reference, remediation, file_path, line_number if line_number else None, now, now,
    ))
    conn.commit()
    finding_id = c.lastrowid
    conn.close()

    return f"Finding #{finding_id} logged: [{severity}] {title} — {agent_name} (audit: {audit_id})"


@mcp.tool()
def get_findings(
    severity: str = "",
    team: str = "",
    audit_id: str = "latest",
) -> str:
    """
    Query findings from the database.

    Args:
        severity: Filter by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO). Empty = all.
        team: Filter by team. Empty = all.
        audit_id: Audit ID to query. 'latest' = most recent audit.
    """
    conn = get_db()
    c = conn.cursor()

    if audit_id == "latest":
        c.execute("SELECT id FROM audits ORDER BY started_at DESC LIMIT 1")
        row = c.fetchone()
        if not row:
            conn.close()
            return "No audits found."
        audit_id = row["id"]

    query = "SELECT * FROM findings WHERE audit_id = ?"
    params = [audit_id]
    if severity:
        query += " AND severity = ?"
        params.append(severity.upper())
    if team:
        query += " AND team = ?"
        params.append(team)
    query += " ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 WHEN 'LOW' THEN 4 ELSE 5 END"

    c.execute(query, params)
    findings = [dict(r) for r in c.fetchall()]
    conn.close()

    if not findings:
        return f"No findings for audit {audit_id}" + (f" with severity={severity}" if severity else "") + (f" team={team}" if team else "")

    lines = [f"# Findings — Audit: {audit_id}\n"]
    for f in findings:
        loc = f"{f['file_path']}:{f['line_number']}" if f.get("file_path") else "N/A"
        lines.append(f"**[{f['severity']}]** {f['title']}")
        lines.append(f"  Agent: {f['agent_name']} | Team: {f['team']} | Category: {f['category']}")
        lines.append(f"  Location: {loc}")
        if f.get("reference"):
            lines.append(f"  Reference: {f['reference']}")
        if f.get("remediation"):
            lines.append(f"  Fix: {f['remediation']}")
        lines.append("")

    lines.append(f"**Total: {len(findings)} findings**")
    return "\n".join(lines)


@mcp.tool()
def get_dashboard(audit_id: str = "latest") -> str:
    """
    Get a summary dashboard for an audit.

    Args:
        audit_id: Audit ID. 'latest' = most recent.
    """
    conn = get_db()
    c = conn.cursor()

    if audit_id == "latest":
        c.execute("SELECT id FROM audits ORDER BY started_at DESC LIMIT 1")
        row = c.fetchone()
        if not row:
            conn.close()
            return "No audits found."
        audit_id = row["id"]

    # Audit info
    c.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
    audit = dict(c.fetchone()) if c.fetchone() else {}
    # Re-query (fetchone consumed it)
    c.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
    audit_row = c.fetchone()
    audit = dict(audit_row) if audit_row else {}

    # Counts
    c.execute("""
        SELECT severity, COUNT(*) as cnt FROM findings
        WHERE audit_id = ? GROUP BY severity
        ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 WHEN 'LOW' THEN 4 ELSE 5 END
    """, (audit_id,))
    sev_counts = {row["severity"]: row["cnt"] for row in c.fetchall()}

    # Team counts
    c.execute("""
        SELECT team, COUNT(*) as cnt FROM findings
        WHERE audit_id = ? GROUP BY team ORDER BY cnt DESC
    """, (audit_id,))
    team_counts = {row["team"]: row["cnt"] for row in c.fetchall()}

    total = sum(sev_counts.values())

    # Risk score: CRITICAL×25 + HIGH×10 + MEDIUM×3 + LOW×1, cap 100
    risk = min(100,
        sev_counts.get("CRITICAL", 0) * 25 +
        sev_counts.get("HIGH", 0) * 10 +
        sev_counts.get("MEDIUM", 0) * 3 +
        sev_counts.get("LOW", 0) * 1
    )

    conn.close()

    lines = [
        f"# the-conductor — Dashboard",
        f"",
        f"**Audit ID**: {audit.get('id', audit_id)}",
        f"**Target**: {audit.get('target', 'unknown')}",
        f"**Started**: {audit.get('started_at', 'unknown')}",
        f"**Status**: {audit.get('status', 'unknown')}",
        f"**Risk Score**: {risk}/100",
        f"",
        f"## Severity Breakdown",
    ]
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        cnt = sev_counts.get(sev, 0)
        if cnt:
            bar = "█" * min(cnt, 30)
            lines.append(f"  {sev:10s} {bar} {cnt}")

    lines.append(f"\n**Total findings: {total}**")
    lines.append(f"\n## By Team")
    for team, cnt in team_counts.items():
        lines.append(f"  {team}: {cnt}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MCP Tools — Leads (Business Development)
# ---------------------------------------------------------------------------

@mcp.tool()
def log_lead(
    source: str,
    first_name: str = "",
    last_name: str = "",
    email: str = "",
    company: str = "",
    title: str = "",
    industry: str = "",
    score: int = 0,
    notes: str = "",
) -> str:
    """
    Log a prospecting lead.

    Args:
        source: Lead source (linkedin, website, referral, apollo)
        first_name: Contact first name
        last_name: Contact last name
        email: Contact email
        company: Company name
        title: Job title
        industry: Industry
        score: Lead score 0-100
        notes: Additional notes
    """
    conn = get_db()
    now = datetime.utcnow().isoformat() + "Z"
    c = conn.cursor()
    c.execute("""
        INSERT INTO leads (source, first_name, last_name, email, title, company, industry, score, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (source, first_name, last_name, email, title, company, industry, score, notes, now, now))
    conn.commit()
    lid = c.lastrowid
    conn.close()
    return f"Lead #{lid} logged: {first_name} {last_name} ({company}) — score {score}"


@mcp.tool()
def get_leads(status: str = "", min_score: int = 0) -> str:
    """
    Query leads from the database.

    Args:
        status: Filter by status (new, qualified, contacted). Empty = all.
        min_score: Minimum lead score filter.
    """
    conn = get_db()
    c = conn.cursor()
    query = "SELECT * FROM leads WHERE score >= ?"
    params = [min_score]
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY score DESC"
    c.execute(query, params)
    leads = [dict(r) for r in c.fetchall()]
    conn.close()

    if not leads:
        return "No leads found."

    lines = [f"# Leads ({len(leads)} total)\n"]
    for l in leads:
        lines.append(f"**{l['first_name']} {l['last_name']}** — {l['company']}")
        lines.append(f"  Title: {l.get('title', 'N/A')} | Score: {l['score']} | Status: {l['status']}")
        if l.get("email"):
            lines.append(f"  Email: {l['email']}")
        lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# MCP Tools — Projects & Invoices (Client Delivery)
# ---------------------------------------------------------------------------

@mcp.tool()
def log_project(
    client_name: str,
    service: str,
    status: str = "proposal",
    value: float = 0,
    notes: str = "",
) -> str:
    """
    Log a client project.

    Args:
        client_name: Client company name
        service: Service type (audit, assessment, consulting)
        status: Project status (proposal, active, completed)
        value: Project value in USD
        notes: Additional notes
    """
    conn = get_db()
    now = datetime.utcnow().isoformat() + "Z"
    c = conn.cursor()
    c.execute("""
        INSERT INTO projects (client_name, service, status, value, notes, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (client_name, service, status, value, notes, now, now))
    conn.commit()
    pid = c.lastrowid
    conn.close()
    return f"Project #{pid}: {client_name} — {service} (${value})"


@mcp.tool()
def get_system_prompt() -> str:
    """Get the full CLAUDE.md system prompt (orchestration rules, severity classification, execution order)."""
    path = BASE_DIR / "CLAUDE.md"
    if path.exists():
        return path.read_text()
    return "CLAUDE.md not found."


# ---------------------------------------------------------------------------
# MCP Resources
# ---------------------------------------------------------------------------

@mcp.resource("conductor://claude-md")
def resource_claude_md() -> str:
    """The full CLAUDE.md orchestration rules."""
    return (BASE_DIR / "CLAUDE.md").read_text()


@mcp.resource("conductor://agents")
def resource_agents() -> str:
    """List of all 40 agents by division."""
    return list_agents()


@mcp.resource("conductor://divisions")
def resource_divisions() -> str:
    """All 7 divisions and descriptions."""
    return list_divisions()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"the-conductor MCP server starting on {host}:{port}")
    app = mcp.sse_app()
    uvicorn.run(app, host=host, port=port)
