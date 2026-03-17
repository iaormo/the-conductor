# client-onboard — Run client onboarding and project setup pipeline

Onboards a new client by generating SOW, setting up project milestones, creating
billing schedule, and configuring reporting dashboards.

## Usage

```
/client:onboard --client "Acme Corp" --service "security-audit" --value 50000 --timeline "12 weeks"
/client:onboard --client "TechCorp" --service "security-audit" --value 35000 --contact "john@techcorp.com" --sow-only
/client:onboard --client "FinanceInc" --service "compliance-gap-analysis" --value 25000 --stakeholders "ciso,cto,cfo"
```

## Instructions

You are orchestrating a client onboarding pipeline with 4 specialist agents.
Run agents in sequence as each depends on prior outputs. Some can run in parallel.

---

### Step 1 — Parse Client Arguments

Extract from `$ARGUMENTS`:
- `--client`: Client legal name (required)
- `--service`: Service type (security-audit, compliance-gap, remediation-support, custom)
- `--value`: Project value in USD (required)
- `--timeline`: Duration (e.g., "12 weeks", "3 months", "90 days")
- `--contact`: Primary client contact (name, email, phone)
- `--stakeholders`: Key stakeholders (comma-separated titles: ciso, cto, cfo, etc.)
- `--sow-only`: Generate SOW only (skip other steps)
- `--milestone-mode`: Milestone-based billing (default) or T&M time tracking

**Validate:**
- Client name non-empty
- Service type is valid
- Value is positive number
- Timeline is parseable
- Output: structured client object for downstream agents

---

### Step 2 — Spawn Project Manager Agent (PARALLEL: with Step 3)

**Task 1: Project Manager Agent**

```
Client: [client name]
Service: [service type]
Value: $[value]
Timeline: [timeline]
Stakeholders: [stakeholders list]

Responsibilities:
  1. Create project structure with phases and milestones
  2. Define milestone hierarchy based on service type:
     Phase 1: Kickoff & Planning
     Phase 2: Discovery/Audit (if applicable)
     Phase 3: Implementation/Remediation
     Phase 4: Closeout & Handoff
  3. Assign target dates based on timeline
  4. Identify critical path and dependencies
  5. Assign owners and escalation contacts
  6. Create risk assessment
  7. Generate project charter and kickoff agenda

Deliverables:
  - project_charter.md (timeline, milestones, owners, risks)
  - kickoff_agenda.md (meeting agenda for kickoff call)
  - milestone_schedule.csv (dates, owners, dependencies)

Constraints:
  - Use realistic timelines (don't compress beyond reason)
  - Include buffer time (10% of duration minimum)
  - Always identify critical path
  - Flag any timeline risks upfront
```

**Proceed to Step 3 in parallel; wait for both to complete before Step 4.**

---

### Step 3 — Spawn SOW Generator Agent (PARALLEL: with Step 2)

**Task 2: SOW Generator Agent**

```
Client: [client name]
Service: [service type]
Value: $[value]
Timeline: [timeline]
Project charter: [from Step 2 if available, otherwise assume defaults]

Responsibilities:
  1. Define scope of work based on service type:
     - In-scope items (detailed list)
     - Out-of-scope items (explicit exclusions)
     - Assumptions and constraints
  2. List deliverables with acceptance criteria:
     - Reports, recommendations, training, dashboards, etc.
  3. Create timeline section with milestone schedule
  4. Itemize pricing breakdown:
     - Service costs (by phase or category)
     - Reimbursable expenses
     - Payment schedule (deposit, milestone, final)
  5. Add terms & conditions:
     - Confidentiality, IP ownership, liability, change orders
  6. Prepare signature blocks
  7. Export as PDF and Word (.docx) for signing

Deliverables:
  - SOW_[ClientName]_[Date].pdf (signed-ready PDF)
  - SOW_[ClientName]_[Date].docx (editable Word version)
  - pricing_summary.csv (itemized costs)

Constraints:
  - Never promise specific vulnerability counts
  - Include standard liability disclaimer
  - Pricing must match --value total
  - Use realistic effort estimates
  - No legal advice (e.g., "You should consult your lawyer on...")
```

**Proceed to Step 4 after both Step 2 and 3 complete.**

---

### Step 4 — Spawn Invoice Agent (for payment setup)

**Task 3: Invoice Agent**

```
Client: [client name]
Service value: $[value]
Payment terms: [Net 30 (default), milestone-based, custom]
Milestone schedule: [from Step 2]

Responsibilities:
  1. Create payment schedule based on project phases:
     - Deposit (typically 30-50% upon SOW signature)
     - Milestone payments (upon deliverable completion)
     - Final payment (upon project completion)
  2. Generate invoice template for each milestone
  3. Calculate tax (based on client location)
  4. Create payment tracking spreadsheet
  5. Draft payment reminder templates
  6. Set up collection/follow-up schedule
  7. Generate financial summary for project accounting

Deliverables:
  - payment_schedule.csv (milestone dates, amounts, invoice #s)
  - invoice_template_[ClientName].xlsx
  - payment_reminder_templates.md
  - financial_summary.csv (revenue recognition, DSO, ARR impact)

Constraints:
  - Payment schedule must total to project value
  - Include realistic payment terms (Net 30 standard)
  - Factor in tax requirements based on client state
  - Never commit to late-payment penalties without agreement
  - Build in buffer for payment delays (assume 5-10 day average)
```

**Wait for completion before Step 5.**

---

### Step 5 — Spawn Client Reporting Agent (for dashboard setup)

**Task 4: Client Reporting Agent**

```
Client: [client name]
Service: [service type]
Timeline: [timeline]
Project structure: [from Step 2]
Service scope: [from Step 3]

Responsibilities:
  1. Design reporting cadence:
     - Weekly status report template (for engineering team)
     - Monthly executive summary (for board/C-suite)
     - Final report template (at project completion)
  2. Create dashboards based on service:
     - Security audit: findings by severity, remediation progress
     - Compliance: gap analysis, control mapping, audit readiness
     - Progress: milestone completion, timeline vs. plan, budget utilization
  3. Identify key metrics to track:
     - Completion %, timeline variance, budget variance, quality metrics
  4. Draft sample reports for client review
  5. Create reporting calendar (weekly/monthly sync dates)
  6. Set up dashboard templates (PDF, HTML, Excel)

Deliverables:
  - executive_summary_template.md
  - status_report_template.md
  - dashboard_template.html
  - reporting_calendar.csv (scheduled report dates)
  - metrics_definition.md (what we'll measure and report)

Constraints:
  - Reporting must be non-technical for executive audience
  - Status reports must be actionable (not just data dumps)
  - Dashboards must be visual and clear
  - Avoid jargon; use business language
```

**Wait for completion before Step 6.**

---

### Step 6 — Consolidate Onboarding Package

Gather all outputs and create final onboarding package:

```
CLIENT ONBOARDING PACKAGE
═════════════════════════════════════════════════════════════════════

Client: [client name]
Service: [service type]
Project value: $[value]
Timeline: [timeline]
Start date: [date]
End date: [date]
Onboarded by: [your name]
Date: [today]

═════════════════════════════════════════════════════════════════════

DELIVERABLES CREATED
─────────────────────────────────────────────────────────────────────

1. PROJECT STRUCTURE
   ✓ project_charter.md — Overall project structure, phases, milestones
   ✓ kickoff_agenda.md — Prepared agenda for kickoff call
   ✓ milestone_schedule.csv — Timeline with dates and owners
   ✓ risk_register.md — Identified risks and mitigation plans

2. STATEMENT OF WORK
   ✓ SOW_[ClientName].pdf — Signed-ready PDF
   ✓ SOW_[ClientName].docx — Editable version for changes
   ✓ pricing_summary.csv — Itemized costs by phase/service
   ✓ signature_page.pdf — Signature block for both parties

3. BILLING & PAYMENT
   ✓ payment_schedule.csv — Milestone-based payment dates and amounts
   ✓ invoice_template.xlsx — Ready-to-use invoice template
   ✓ payment_reminder_templates.md — Email templates for reminders
   ✓ financial_summary.csv — Revenue recognition and accounting data

4. CLIENT REPORTING
   ✓ status_report_template.md — Weekly status report template
   ✓ executive_summary_template.md — Monthly executive summary
   ✓ dashboard_template.html — Visual status dashboard
   ✓ reporting_calendar.csv — Scheduled report dates

═════════════════════════════════════════════════════════════════════

NEXT STEPS (PRE-KICKOFF)
─────────────────────────────────────────────────────────────────────

WEEK 1 — Contract & Communication
  ☐ Send SOW to client (email + wet signature copy)
  ☐ Schedule kickoff meeting (target: within 5 business days)
  ☐ Confirm project stakeholders and contacts
  ☐ Prepare kickoff materials (charter, agenda, team intro)
  ☐ Brief internal team on project scope and timeline

WEEK 2 — Kickoff Meeting
  ☐ Execute kickoff meeting (use prepared agenda)
  ☐ Confirm scope, timeline, and success criteria
  ☐ Introduce team members and assign owners
  ☐ Establish communication cadence (weekly syncs, monthly reviews)
  ☐ Distribute project charter and kickoff notes

WEEK 3 — Project Start
  ☐ Receive signed SOW from client
  ☐ Invoice for deposit (30-50% of total)
  ☐ Begin Phase 1 (Planning & access setup)
  ☐ Confirm all access credentials received
  ☐ Send first status report (outline what's starting)

═════════════════════════════════════════════════════════════════════

KEY CONTACTS
─────────────────────────────────────────────────────────────────────

Primary Client Contact:    [name | email | phone]
Executive Sponsor:         [name | email | phone]
Technical Lead:            [name | email | phone]

Our Project Manager:       [name | email | phone]
Our Service Lead:          [name | email | phone]
Our Account Manager:       [name | email | phone]

═════════════════════════════════════════════════════════════════════

PROJECT AT A GLANCE
─────────────────────────────────────────────────────────────────────

Total investment:          $[value]
Payment schedule:          [deposit] deposit, [milestone payments], [final] final
Timeline:                  [start] to [end] ([weeks] weeks)

Key milestones:
  • Kickoff:               [date]
  • Phase 1 complete:      [date]
  • Phase 2 complete:      [date]
  • Phase 3 complete:      [date]
  • Final delivery:        [date]

Critical success factors:
  1. [e.g., "Timely access to source code and infrastructure"]
  2. [e.g., "Weekly sync calls with engineering leadership"]
  3. [e.g., "Prompt feedback on draft findings/recommendations"]

Risk watch list:
  1. [e.g., "Team availability during holidays"]
  2. [e.g., "Dependency on external contractor for infrastructure testing"]

═════════════════════════════════════════════════════════════════════

PACKAGE CONTENTS (All files)
─────────────────────────────────────────────────────────────────────

/onboarding/[ClientName]/
├── project/
│   ├── project_charter.md
│   ├── kickoff_agenda.md
│   ├── milestone_schedule.csv
│   └── risk_register.md
├── sow/
│   ├── SOW_[ClientName].pdf
│   ├── SOW_[ClientName].docx
│   ├── pricing_summary.csv
│   └── signature_page.pdf
├── billing/
│   ├── payment_schedule.csv
│   ├── invoice_template.xlsx
│   ├── payment_reminders.md
│   └── financial_summary.csv
└── reporting/
    ├── status_report_template.md
    ├── executive_summary_template.md
    ├── dashboard_template.html
    └── reporting_calendar.csv

═════════════════════════════════════════════════════════════════════
```

---

### Step 7 — Send to Client

**Send to client contact (if email provided):**

```
Email subject: [ClientName] — Project Onboarding Package & SOW

Dear [client contact],

We're excited to begin our engagement with [ClientName] on [service].
Please find attached your onboarding package, including the Statement of Work,
project timeline, and next steps.

ATTACHED:
  • SOW_[ClientName].pdf — Please review and sign
  • Project Charter — Overview of our plan
  • Kickoff Agenda — What we'll cover in our kick-off meeting
  • Payment Schedule — Billing timeline and amounts

NEXT STEPS:
  1. Review the SOW and signature page
  2. Sign and return (wet signature or DocuSign)
  3. Confirm kickoff meeting date/time (proposed: [date/time])
  4. Introduce your team members and key contacts

If you have any questions, please reach out to:
  [Account Manager Name]: [email | phone]

Looking forward to working together!

Best regards,
[Your name and title]
[Company]
[Contact info]
```

---

### Anti-Hallucination Rules

For this command:

1. **Never create SOW without --value** — cost must be explicit
2. **Never skip the kickoff** — it's mandatory for project success
3. **Never promise specific finding counts** — audits are point-in-time
4. **Never compress timelines unrealistically** — add buffer time
5. **Never commit to legal/tax advice** — qualify as "not legal/tax advice"
6. **Never override client timeline** — use their timeline, not ours
7. **Never create deliverables before SOW signature** — SOW must come first
