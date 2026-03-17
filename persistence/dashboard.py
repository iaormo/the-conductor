#!/usr/bin/env python3
"""
dashboard.py — the-conductor audit dashboard
Renders current audit findings to terminal or HTML report.

Usage:
    python3 persistence/dashboard.py                    # Terminal view
    python3 persistence/dashboard.py --html             # Export HTML report
    python3 persistence/dashboard.py --audit latest     # Latest audit only
    python3 persistence/dashboard.py --severity CRITICAL HIGH
"""

import sqlite3
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "audit.db"

BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GREEN = "\033[92m"
DIM = "\033[2m"
RESET = "\033[0m"

SEVERITY_COLOR = {
    "CRITICAL": RED + BOLD,
    "HIGH": RED,
    "MEDIUM": YELLOW,
    "LOW": CYAN,
    "INFO": GREEN,
}

SEVERITY_ORDER = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4, "INFO": 5}


def connect(db_path=None):
    path = db_path or DB_PATH
    if not Path(str(path)).exists():
        print(f"No database found at {path}")
        print("Run an audit first, or: python3 persistence/init_db.py")
        sys.exit(1)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def get_latest_audit_id(conn):
    c = conn.cursor()
    c.execute("SELECT id FROM audits ORDER BY started_at DESC LIMIT 1")
    row = c.fetchone()
    return row["id"] if row else None


def get_findings(conn, audit_id=None, severities=None):
    c = conn.cursor()
    query = "SELECT * FROM findings WHERE 1=1"
    params = []
    if audit_id:
        query += " AND audit_id = ?"
        params.append(audit_id)
    if severities:
        placeholders = ",".join("?" * len(severities))
        query += f" AND severity IN ({placeholders})"
        params.extend(severities)
    query += " ORDER BY CASE severity WHEN 'CRITICAL' THEN 1 WHEN 'HIGH' THEN 2 WHEN 'MEDIUM' THEN 3 WHEN 'LOW' THEN 4 ELSE 5 END, created_at"
    c.execute(query, params)
    return [dict(r) for r in c.fetchall()]


def get_audit_info(conn, audit_id):
    c = conn.cursor()
    c.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
    row = c.fetchone()
    return dict(row) if row else {}


def render_terminal(findings, audit_info):
    width = 72

    print("\n" + "=" * width)
    print(f"{BOLD}  the-conductor — Security Audit Dashboard{RESET}")
    print(f"  Audit ID : {audit_info.get('id', 'unknown')}")
    print(f"  Target   : {audit_info.get('target', 'unknown')}")
    print(f"  Started  : {audit_info.get('started_at', 'unknown')}")
    print(f"  Status   : {audit_info.get('status', 'unknown')}")
    print("=" * width)

    # Summary counts
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    print(f"\n  {BOLD}Summary{RESET}")
    for sev, count in sorted(counts.items(), key=lambda x: SEVERITY_ORDER.get(x[0], 99)):
        if count > 0:
            color = SEVERITY_COLOR.get(sev, "")
            bar = "█" * min(count, 40)
            print(f"  {color}{sev:10s}{RESET}  {bar} {count}")

    print(f"\n  {BOLD}Total findings: {len(findings)}{RESET}")
    print("\n" + "-" * width)

    # Findings by team
    teams = {}
    for f in findings:
        teams.setdefault(f["team"], []).append(f)

    for team, team_findings in sorted(teams.items()):
        print(f"\n  {BOLD}{team.upper()}{RESET}  ({len(team_findings)} findings)")
        for f in team_findings:
            color = SEVERITY_COLOR.get(f["severity"], "")
            print(f"  {color}[{f['severity']:8s}]{RESET}  {f['title']}")
            if f.get("file_path"):
                line = f":{f['line_number']}" if f.get("line_number") else ""
                print(f"  {DIM}           {f['file_path']}{line}{RESET}")
            if f.get("reference"):
                print(f"  {DIM}           ref: {f['reference']}{RESET}")
            if f.get("remediation"):
                print(f"  {DIM}           fix: {f['remediation'][:60]}...{RESET}" if len(f["remediation"]) > 60 else f"  {DIM}           fix: {f['remediation']}{RESET}")
            print()

    print("=" * width + "\n")


def render_html(findings, audit_info, output_path="audit_report.html"):
    counts = {s: 0 for s in SEVERITY_ORDER}
    for f in findings:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1

    sev_colors = {
        "CRITICAL": "#E24B4A",
        "HIGH": "#EF8B2C",
        "MEDIUM": "#EF9F27",
        "LOW": "#378ADD",
        "INFO": "#1D9E75",
    }

    rows = ""
    for f in findings:
        color = sev_colors.get(f["severity"], "#888")
        ref = f.get("reference") or ""
        fix = f.get("remediation") or ""
        path = f"{f.get('file_path', '')}{':%d' % f['line_number'] if f.get('line_number') else ''}"
        rows += f"""
        <tr>
          <td><span class="badge" style="background:{color}">{f['severity']}</span></td>
          <td>{f['agent_name']}</td>
          <td>{f['team']}</td>
          <td>{f['title']}</td>
          <td class="mono">{path}</td>
          <td>{ref}</td>
          <td>{fix[:80]}{'...' if len(fix) > 80 else ''}</td>
        </tr>"""

    summary_badges = ""
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]:
        c = counts.get(sev, 0)
        if c > 0:
            color = sev_colors[sev]
            summary_badges += f'<span class="badge" style="background:{color}">{sev}: {c}</span> '

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>the-conductor — Audit Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         margin: 0; padding: 2rem; background: #f5f5f0; color: #2c2c2a; }}
  h1 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: .25rem; }}
  .meta {{ font-size: .85rem; color: #888; margin-bottom: 1.5rem; }}
  .summary {{ margin-bottom: 1.5rem; }}
  .badge {{ display: inline-block; padding: .2rem .6rem; border-radius: 4px;
            font-size: .75rem; font-weight: 600; color: #fff; margin-right: .4rem; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff;
           border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
  th {{ background: #2c2c2a; color: #fff; padding: .6rem .8rem; text-align: left;
        font-size: .8rem; text-transform: uppercase; letter-spacing: .05em; }}
  td {{ padding: .55rem .8rem; border-bottom: 1px solid #eee; font-size: .85rem;
        vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #fafaf8; }}
  .mono {{ font-family: monospace; font-size: .8rem; }}
  footer {{ margin-top: 2rem; font-size: .8rem; color: #aaa; text-align: center; }}
</style>
</head>
<body>
<h1>the-conductor — Security Audit Report</h1>
<div class="meta">
  Audit ID: <strong>{audit_info.get('id', 'unknown')}</strong> &nbsp;|&nbsp;
  Target: <strong>{audit_info.get('target', 'unknown')}</strong> &nbsp;|&nbsp;
  Generated: <strong>{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</strong>
</div>
<div class="summary">{summary_badges}</div>
<table>
<thead>
  <tr><th>Severity</th><th>Agent</th><th>Team</th><th>Finding</th>
      <th>Location</th><th>Reference</th><th>Remediation</th></tr>
</thead>
<tbody>{rows}</tbody>
</table>
<footer>Generated by the-conductor &mdash; Multi-agent CISO security audit system</footer>
</body>
</html>"""

    Path(output_path).write_text(html)
    print(f"  HTML report saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="the-conductor audit dashboard")
    parser.add_argument("--html", action="store_true", help="Export HTML report")
    parser.add_argument("--output", default="audit_report.html", help="HTML output path")
    parser.add_argument("--audit", default="latest", help="Audit ID (default: latest)")
    parser.add_argument("--severity", nargs="+",
                        choices=["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"],
                        help="Filter by severity")
    parser.add_argument("--db", help="Override DB path")
    args = parser.parse_args()

    conn = connect(args.db)

    audit_id = get_latest_audit_id(conn) if args.audit == "latest" else args.audit
    if not audit_id:
        print("No audits found in database.")
        sys.exit(0)

    audit_info = get_audit_info(conn, audit_id)
    findings = get_findings(conn, audit_id=audit_id, severities=args.severity)
    conn.close()

    if args.html:
        render_html(findings, audit_info, args.output)
    else:
        render_terminal(findings, audit_info)


if __name__ == "__main__":
    main()
