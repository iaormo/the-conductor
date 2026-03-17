# lead-gen-prospect — Run lead prospecting pipeline

Finds and enriches ideal customer profiles (ICPs) matching your go-to-market criteria,
creates outreach sequences, and syncs to CRM for pipeline tracking.

## Usage

```
/lead-gen:prospect --icp "VP Engineering at Series B+ SaaS, 100-500 emp, US, AWS" --limit 50
/lead-gen:prospect --icp "CISO at healthcare, 1000+ emp, US East" --output csv,json
/lead-gen:prospect --icp "Security Manager at fintech" --enrich --sequence --crm-sync
/lead-gen:prospect --segment "enterprise" --location "US" --industry "SaaS" --limit 100
```

## Instructions

You are orchestrating a lead generation pipeline with 4 specialist agents.
Run all agents in parallel unless otherwise specified.

---

### Step 1 — Parse ICP Arguments

Extract from `$ARGUMENTS`:
- `--icp`: Customer profile description (titles, industry, company size, location, pain points)
- `--limit`: Max prospects to return (default: 50)
- `--output`: Format(s): csv, json, pdf (default: csv)
- `--enrich`: Include full enrichment (default: no)
- `--sequence`: Generate outreach sequences (default: no)
- `--crm-sync`: Add to Apollo CRM (default: no)
- `--segment`: Pre-defined segment (enterprise, mid-market, startup, etc.)
- `--location`: Geographic filter (US, EU, Asia, specific regions)
- `--industry`: Industry filter (SaaS, fintech, healthcare, etc.)
- `--headcount-range`: Company size (1-10, 11-50, 51-200, 201-500, 501-1000, 1000+)

**Validate:**
- ICP description is non-empty
- Limit is 1-1000 (cap at 1000 to avoid abuse)
- Output formats are valid (csv, json, pdf)

---

### Step 2 — Spawn Prospecting Agent

**Task 1: Prospecting Agent**

```
Your ICP is: [parsed ICP description]

Responsibilities:
  1. Build search queries from ICP description
  2. Search Apollo for matching people and companies
  3. Filter by role, seniority, company signals, location
  4. Rank prospects by fit score (0-100)
  5. Deduplicate by email + company
  6. Output: CSV with Name, Title, Company, Email, Phone, LinkedIn, FitScore

Constraints:
  - Only report data returned by Apollo API
  - No invented email addresses or phone numbers
  - Fit score must be justified by actual filters
  - Limit results to [limit] top prospects

Deliver: prospects.csv with [count] prospects, ranked by fit score
```

**Wait for completion before proceeding to Step 3.**

---

### Step 3 — Optional: Spawn Enrichment Agent (if --enrich)

**Task 2: Lead Enrichment Agent**

```
Input: prospects.csv from Step 2

Responsibilities:
  1. Load CSV with partial lead data
  2. Match each lead to Apollo database
  3. Enrich with full contact info (email, phone, LinkedIn, company data)
  4. Validate email deliverability
  5. Flag enrichment signals (job change, company hiring, funding)
  6. Deduplicate records
  7. Assign data quality grade (A/B/C/D/F)

Constraints:
  - Never invent data — only report Apollo results
  - Require email match confidence > 80%
  - Flag unverified emails explicitly

Deliver: enriched_leads.csv with full data + quality grades
```

**Wait for completion before proceeding to Step 4.**

---

### Step 4 — Optional: Spawn Outreach Agent (if --sequence)

**Task 3: Outreach Sequencing Agent**

```
Input: enriched_leads.csv from Step 3 (or prospects.csv from Step 2 if no enrichment)

Responsibilities:
  1. Analyze each prospect's profile (title, company, industry)
  2. Identify pain points relevant to their role
  3. Design personalized 5-touch outreach sequence
    - Touch 1 (Day 0): Email introduction
    - Touch 2 (Day 1): LinkedIn connection request
    - Touch 3 (Day 3): Email with social proof
    - Touch 4 (Day 7): Email with ROI focus
    - Touch 5 (Day 14): Email with limited-time offer
  4. Write copy for each touch (personalized, non-templated)
  5. Create A/B test variants (2 subject lines)
  6. Prepare campaign file for Apollo import

Constraints:
  - Personalization must reference actual prospect data (company, title, pain point)
  - No invented metrics or case studies
  - Copy must include unsubscribe option (compliance)

Deliver:
  - Email templates (HTML + plain text)
  - LinkedIn message templates
  - Campaign specification file (names, schedule, A/B variants)
  - Readiness report for Apollo campaign creation
```

**Wait for completion before proceeding to Step 5.**

---

### Step 5 — Optional: Spawn CRM Sync Agent (if --crm-sync)

**Task 4: CRM Sync Agent**

```
Input: enriched_leads.csv from Step 3 (or prospects.csv if no enrichment)

Responsibilities:
  1. Create accounts in Apollo for new companies (if not exists)
  2. Create contact records for each prospect
    - Name, title, email, phone, company, LinkedIn, location
  3. Assign labels: [segment], [industry], [location], [pain_point]
  4. Assign initial pipeline stage: lead_prospecting
  5. Deduplicate: check for existing contacts by email/name+company
  6. Log all new contacts to Apollo database
  7. Generate CRM sync summary report

Constraints:
  - Use run_dedupe=True for all creations
  - Reference existing accounts (create if missing)
  - Never invent contact IDs
  - Validate email format before creation

Deliver:
  - CRM sync report (X contacts created, Y updated, Z duplicates)
  - Pipeline snapshot (prospecting stage count)
  - Data quality metrics (email verified %, phone %, LinkedIn %)
```

**Wait for completion before proceeding to Step 6.**

---

### Step 6 — Consolidate Results

Gather outputs from all spawned agents and produce final summary:

```
LEAD GENERATION PIPELINE SUMMARY
═════════════════════════════════════════════════════════════════════

ICP: [parsed ICP]
Execution date: [date]
Pipeline stage: [prospecting → enrichment → outreach → CRM sync]

RESULTS
─────────────────────────────────────────────────────────────────

Step 1 — Prospecting:
  Prospects found: [N]
  Top fit scores: [list top 5 fit scores]
  Output: prospects.csv

[If --enrich]:
Step 2 — Enrichment:
  Prospects enriched: [N]
  Data quality A: [X] | B: [Y] | C: [Z]
  Email verified: [%]
  Output: enriched_leads.csv

[If --sequence]:
Step 3 — Outreach:
  Email templates: [N] (5 per prospect)
  LinkedIn templates: [N]
  A/B variants: 2 (subject line testing)
  Cadence: [Day 0, 1, 3, 7, 14]
  Output: campaign_spec.json

[If --crm-sync]:
Step 4 — CRM Sync:
  Contacts created: [N]
  Contacts updated: [M]
  Duplicates flagged: [K]
  Pipeline stage: lead_prospecting
  Output: crm_sync_report.csv

NEXT STEPS
─────────────────────────────────────────────────────────────────

[If --sequence and --crm-sync]:
  1. Review outreach templates (review by sales leadership)
  2. Create campaign in Apollo UI (manual step)
  3. Add enriched contacts to campaign (use CRM Sync output)
  4. Launch first email touch (Day 0)
  5. Monitor open/click rates daily

[If --crm-sync only]:
  1. Sales team follows up with enriched prospects
  2. Track in Apollo pipeline
  3. Move to discovery stage as they engage

DATA EXPORTED
─────────────────────────────────────────────────────────────────
  • prospects.csv (from Step 1)
  [• enriched_leads.csv (from Step 2, if --enrich)]
  [• campaign_spec.json (from Step 3, if --sequence)]
  [• crm_sync_report.csv (from Step 4, if --crm-sync)]

═════════════════════════════════════════════════════════════════
```

---

### Anti-Hallucination Rules

For this command:

1. **Never run steps out of order** — always: Prospecting → Enrichment → Outreach → CRM Sync
2. **Never invent prospect data** — only include what Apollo returns
3. **Never promise results** — prospecting finds candidates, not guaranteed deals
4. **Never skip deduplication** — always check for duplicates
5. **Never include false metrics** — report only verified fit scores and counts
