# full-service — Run all 7 divisions in comprehensive business operations

Coordinates full orchestration across Security, Business Development, Client Delivery,
Development & Engineering, Data & Analytics, Marketing & Content, and Automation & Integration.
Perfect for comprehensive quarterly reviews, major business milestones, or system audits.

## Usage

```
/full-service
/full-service --divisions security,business,delivery,dev,data,marketing,automation
/full-service --skip-divisions compliance,incident-response
/full-service --output html,json,pdf
```

## Instructions

You are orchestrating a comprehensive cross-division business operations review with 40 specialist agents.
Route requests through the Master Orchestrator and spawn divisions in the correct order.

---

### Step 1 — Parse Arguments

Extract from `$ARGUMENTS`:
- `--divisions`: Comma-separated list of divisions to run (default: all 7)
- `--skip-divisions`: Comma-separated list of divisions to exclude
- `--output`: Format(s): html, json, pdf, csv (default: html)
- `--scope`: Optional custom scope (default: "comprehensive business operations review")

**Validate:**
- Divisions requested are valid (security, business, delivery, dev, data, marketing, automation)
- Output formats are valid
- No conflicting --divisions and --skip-divisions flags

---

### Step 2 — Engage Master Orchestrator

Invoke the Master Orchestrator agent with:

```
Role: Master Orchestrator
Objective: [parsed scope or custom scope]
Divisions to engage: [security, business, delivery, dev, data, marketing, automation] (minus skipped)
Output format: [html, json, pdf, csv]

Responsibilities:
  1. Determine which of the 7 divisions should run based on the objective
  2. Sequence Division 1 (Security) teams sequentially
  3. Spawn Divisions 2-7 in parallel after Security completes
  4. Monitor all division progress via persistence layer
  5. Synthesize all findings into unified executive report
  6. Generate final output in requested format(s)

Constraints:
  - Security division runs teams sequentially: Team 2 → Team 3 → Team 4 → Team 5
  - Business divisions (2-7) run in parallel
  - Never invent findings — only report logged data
  - Always query persistence layer before synthesizing
  - Batch spawn all parallel agents in single message

Deliver: Unified executive report with all divisions' findings, leads, projects, insights
```

---

### Step 3 — Division 1: Security (Sequential Teams)

Master Orchestrator spawns Division 1 with teams in sequence:

**Team 2 — Software Security**
```
Spawn: SAST Engineer, Dependency Auditor, Code Review Agent, API Security Analyst

Tasks:
  - SAST: Static application security testing on codebase
  - Dependency: Check package managers for vulnerable dependencies
  - Code Review: Security-focused review of critical code paths
  - API: Test API endpoints for auth/authorization/injection issues

Deliver: Security findings (CRITICAL/HIGH/MEDIUM/LOW) with file:line references
```

**Team 3 — Infrastructure Security**
```
Spawn: Cloud Security Engineer, Network Security Analyst, Secrets/IAM Auditor

Tasks:
  - Cloud: Audit cloud accounts (AWS/Azure/GCP) for misconfigurations
  - Network: Check network segmentation, firewall rules, VPN configs
  - Secrets/IAM: Scan for exposed secrets, audit IAM permissions

Deliver: Infrastructure findings with remediation paths
```

**Team 4 — Compliance**
```
Spawn: Compliance Auditor, Privacy Officer, Policy Manager

Tasks:
  - Compliance: Gap analysis against SOC2, ISO27001, HIPAA, PCI-DSS
  - Privacy: GDPR/CCPA compliance, data retention, consent tracking
  - Policy: Review security policies, incident response procedures

Deliver: Compliance gaps, policy recommendations, remediation timeline
```

**Team 5 — Incident Response**
```
Spawn: IR Lead, Forensics Analyst, Threat Hunter

Tasks:
  - IR Triage: Check for active incidents, escalation procedures
  - Forensics: Log analysis, timeline reconstruction, evidence preservation
  - Threat Hunt: Search for indicators of compromise, persistence mechanisms

Deliver: Incident status, threat landscape, hunting results
```

**Wait for Security completion before proceeding to Step 4.**

---

### Step 4 — Divisions 2-7: Business Operations (Parallel)

After Security completes, spawn all remaining divisions in parallel:

**Division 2 — Business Development**
```
Spawn: Prospecting Agent, Lead Enrichment Agent, Outreach Agent, CRM Sync Agent

Tasks:
  1. Prospecting: Search for ICPs matching target customer profiles
  2. Enrichment: Validate and enrich lead data
  3. Outreach: Create personalized sequences
  4. CRM Sync: Add leads to Apollo or internal CRM

Deliver: Prospect list, enriched leads, outreach templates, CRM sync report
```

**Division 3 — Client Delivery**
```
Spawn: Project Manager Agent, SOW Generator Agent, Invoice Agent, Reporting Agent

Tasks:
  1. Project Manager: Track active projects, milestones, deliverables, blockers
  2. SOW Generator: Review existing contracts, suggest updates, create new SOWs
  3. Invoice: Generate invoices for billable work, track payments
  4. Reporting: Create client-facing status reports, health metrics

Deliver: Project health dashboard, invoices, client reports
```

**Division 4 — Development & Engineering**
```
Spawn: Code Generator, Code Reviewer, CI/CD Engineer, Documentation Agent

Tasks:
  1. Code Gen: Generate code from requirements or bug fixes
  2. Code Review: Review PRs, provide feedback, check quality metrics
  3. CI/CD: Audit pipelines, test coverage, deployment automation
  4. Docs: Update technical documentation, API specs, runbooks

Deliver: Code quality metrics, pipeline health, documentation status
```

**Division 5 — Data & Analytics**
```
Spawn: Data Extraction Agent, BI Dashboard Agent, Market Research Agent, Competitive Intel Agent

Tasks:
  1. Data Extraction: Pull data from sources, clean datasets
  2. BI Dashboard: Create dashboards for key business metrics
  3. Market Research: Research market trends, customer insights
  4. Competitive Intel: Analyze competitors, benchmark positioning

Deliver: Data extracts, dashboards, market analysis, competitive landscape
```

**Division 6 — Marketing & Content**
```
Spawn: Content Writer, Email Campaign Agent, Social Media Agent, SEO Agent

Tasks:
  1. Content: Draft blog posts, whitepapers, case studies
  2. Email: Build email sequences, optimize campaigns
  3. Social: Create social media content calendar, schedule posts
  4. SEO: Audit site SEO, identify ranking opportunities

Deliver: Content calendar, email templates, social strategy, SEO recommendations
```

**Division 7 — Automation & Integration**
```
Spawn: Workflow Automation Agent, API Integration Agent, Scheduling Agent, Alerting Agent

Tasks:
  1. Workflows: Build no-code automation workflows
  2. API Integration: Integrate third-party APIs, webhooks
  3. Scheduling: Set up cron jobs, scheduled tasks
  4. Alerting: Create monitoring rules, alert thresholds

Deliver: Automation inventory, API integrations, scheduled tasks, alert rules
```

**Wait for all divisions to complete before Step 5.**

---

### Step 5 — Synthesis & Reporting

Master Orchestrator synthesizes all division outputs:

1. **Query persistence layer:**
   ```bash
   python3 persistence/dashboard.py --table findings --filter "severity:CRITICAL,HIGH"
   python3 persistence/dashboard.py --table leads
   python3 persistence/dashboard.py --table projects
   python3 persistence/dashboard.py --table invoices
   ```

2. **Identify cross-division issues:**
   - Security findings that impact dev/ops
   - Business opportunities aligned with data insights
   - Automation opportunities from repeated tasks
   - Client risks from compliance gaps

3. **Produce unified report:**
   ```
   FULL-SERVICE OPERATIONS REPORT
   ════════════════════════════════════════════════════════════════
   
   Execution date: [date]
   Scope: Comprehensive business operations review
   
   ─────────────────────────────────────────────────────────────
   DIVISION SUMMARIES
   
   [See master-orchestrator.md synthesis format for all 7 divisions]
   
   ─────────────────────────────────────────────────────────────
   CRITICAL FINDINGS (All Divisions)
   - [Title] — [Division/Team] — Immediate action required
   
   ─────────────────────────────────────────────────────────────
   OPPORTUNITIES & ALIGNMENT
   - [Cross-division opportunity 1]
   - [Cross-division opportunity 2]
   - [Recommended next steps]
   
   ════════════════════════════════════════════════════════════════
   ```

4. **Generate output in requested format:**
   - HTML: Interactive dashboard with division summaries
   - JSON: Structured data export for systems integration
   - PDF: Executive summary printable format
   - CSV: Data export for spreadsheet analysis

---

### Step 6 — Deliver Consolidated Results

Gather all outputs and present:

```
FULL-SERVICE OPERATIONS SUMMARY
═════════════════════════════════════════════════════════════════

Execution date: [date]
Total agents deployed: 40
Divisions engaged: 7
Time to completion: [duration]

RISK ASSESSMENT (Division 1)
───────────────────────────
Overall security posture: [CRITICAL | HIGH | MEDIUM | LOW]
CRITICAL findings: [N]
HIGH findings: [N]
Remediation timeline: [immediate | 24-72 hours | 1-4 weeks]

BUSINESS METRICS (Divisions 2-3)
────────────────────────────────
Prospects identified: [N]
Active projects: [M]
Revenue impact: [K] (from invoicing + forecasts)
Client health: [score]

OPERATIONAL HEALTH (Divisions 4-7)
─────────────────────────────────
Code quality: [score/100]
Deployment readiness: [% ready]
Data & insights: [dashboard status]
Automation coverage: [% of tasks]

RECOMMENDED ACTIONS (Priority Order)
───────────────────────────────────
1. [CRITICAL security action] — [Division] — Immediate
2. [HIGH priority business action] — [Division] — 24-48 hours
3. [MEDIUM cross-division action] — [Divisions A + B] — 1 week
4. [LOW improvement] — [Division] — Next cycle

═════════════════════════════════════════════════════════════════
```

---

### Anti-Hallucination Rules

For full-service orchestration:

1. **Never run divisions out of order** — Always: Security (seq) → Business (parallel)
2. **Never invent findings** — Only report what agents have logged
3. **Never skip divisions** — Explicitly note why if a division is excluded
4. **Never claim false metrics** — Report only verified counts and scores
5. **Always query persistence** — Get authoritative DB state before synthesizing
6. **Always batch spawns** — Never spawn agents sequentially unless required by dependency
7. **Always verify findings** — Apply verification-before-completion skill to final report
