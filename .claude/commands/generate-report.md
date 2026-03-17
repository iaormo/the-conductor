---
name: report:generate
description: >
  Synthesize current audit findings from the persistence layer into
  a comprehensive HTML report. Queries all divisions (security, business development,
  client delivery) and generates executive summary with risk scoring.
---

# Generate Report

## Overview

This command synthesizes all audit findings, leads, projects, and invoices from the persistence layer
into a professional HTML report with:
- Executive summary with risk score calculation
- Security findings grouped by team and severity
- Business development pipeline status
- Client delivery project status
- Invoice tracking and revenue analysis
- Actionable remediation roadmap

## Usage

```bash
/report:generate
/report:generate --output audit_report.html
/report:generate --audit audit-20260317-120000
/report:generate --divisions security,business,delivery
```

## Parameters

- `--output`: Output filename (default: `audit_report_YYYYMMDD_HHMMSS.html`)
- `--audit`: Specific audit ID to report on (default: latest)
- `--divisions`: Comma-separated divisions to include (default: all)
  - `security`: Security audit findings
  - `business`: Business development leads and pipeline
  - `delivery`: Client projects and invoicing

## Report Structure

### Executive Summary
- Risk score (0-100 based on critical/high findings)
- Key metrics by division
- Trend analysis vs. previous audits
- Executive dashboard

### Security Division
- Findings by team (Software Security, Infrastructure, Compliance, Incident Response)
- Findings by severity (Critical, High, Medium, Low, Info)
- Affected files and components
- Remediation roadmap with SLAs

### Business Development Division
- Lead pipeline status (new → qualified → contacted → closed)
- Lead scoring distribution
- Source analysis (best performing sources)
- Outreach cadence and engagement metrics

### Client Delivery Division
- Active projects and status
- Project value analysis
- Invoice status and revenue tracking
- Client satisfaction and deliverables

### Appendices
- Full findings table with references
- Lead database export
- Project timeline
- Invoice history

## Command Process

1. CISO Orchestrator queries persistence layer:
   - `SELECT * FROM findings WHERE audit_id = ?`
   - `SELECT * FROM leads WHERE created_at >= ?`
   - `SELECT * FROM projects WHERE status != 'closed'`
   - `SELECT * FROM invoices WHERE created_at >= ?`

2. Calculate metrics:
   - Risk score: (CRITICAL * 100) + (HIGH * 50) + (MEDIUM * 20) + (LOW * 5)
   - Lead conversion rates and pipeline velocity
   - Revenue realized and at-risk

3. Generate HTML report with:
   - Professional styling (Tailwind CSS)
   - Interactive tables
   - Charts and graphs (D3.js-compatible data)
   - Export-friendly PDF layout

4. Output report to specified file

## Example Output

```
audit_report_20260317_142530.html
├── Executive Summary
│   ├── Risk Score: 285 (HIGH)
│   ├── Security Findings: 3 CRITICAL, 5 HIGH, 12 MEDIUM
│   ├── Leads in Pipeline: 24 qualified
│   └── Revenue This Quarter: $125,000
├── Security Division
│   ├── Software Security: 8 findings
│   ├── Infrastructure: 5 findings
│   ├── Compliance: 3 findings
│   └── Incident Response: 4 findings
├── Business Development
│   ├── New Leads: 12
│   ├── Qualified: 24
│   └── Pipeline Value: $500,000
├── Client Delivery
│   ├── Active Projects: 8
│   ├── Upcoming Invoices: 3
│   └── YTD Revenue: $450,000
└── Appendices
    ├── Full Findings Table
    ├── Lead Database
    ├── Project Timeline
    └── Invoice History
```
