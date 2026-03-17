# lead-gen-quick — Fast ICP prospect scoring without enrichment

Lightweight prospecting pipeline that identifies and ranks ideal customer profiles (ICPs)
without full enrichment or outreach. Best for quick market exploration, validation, or
rapid lead identification.

## Usage

```
/lead-gen:quick --icp "CTO at fintech startups" --limit 20
/lead-gen:quick --segment "enterprise" --location "US" --industry "SaaS" --limit 50
/lead-gen:quick --icp "VP Sales at mid-market tech" --output csv,json
/lead-gen:quick --headcount-range "101-500" --limit 100
```

## Instructions

You are running a lightweight prospecting pipeline with 1 specialist agent.
This is a fast alternative to the full lead-gen:prospect pipeline — prospecting only, no enrichment.

---

### Step 1 — Parse ICP Arguments

Extract from `$ARGUMENTS`:
- `--icp`: Customer profile description (titles, industry, company size, location, pain points)
- `--limit`: Max prospects to return (default: 50, max: 500)
- `--output`: Format(s): csv, json (default: csv)
- `--segment`: Pre-defined segment (enterprise, mid-market, startup, sme)
- `--location`: Geographic filter (US, EU, Asia, specific regions)
- `--industry`: Industry filter (SaaS, fintech, healthcare, manufacturing, etc.)
- `--headcount-range`: Company size (1-10, 11-50, 51-200, 201-500, 501-1000, 1000+)
- `--exclude-companies`: Comma-separated list of companies to exclude from results

**Validate:**
- ICP description OR segment is provided (at least one required)
- Limit is 1-500 (cap at 500 to avoid abuse)
- Output formats are valid (csv, json)
- Industry and location filters are recognized

---

### Step 2 — Spawn Prospecting Agent Only

**Task: Prospecting Agent**

```
Your ICP is: [parsed ICP description]

Segment: [parsed segment if provided]
Location: [parsed location if provided]
Industry: [parsed industry if provided]
Headcount range: [parsed range if provided]
Exclude: [companies to exclude]

Responsibilities:
  1. Build search queries from ICP description and filters
  2. Search Apollo database for matching people and companies
  3. Filter by role, seniority, company signals, location, industry
  4. Rank prospects by fit score (0-100)
     - Fit score basis:
       * Title match: 0-30 points
       * Seniority match: 0-20 points
       * Company size match: 0-15 points
       * Industry match: 0-15 points
       * Location match: 0-10 points
       * Company hiring signals: 0-10 points
  5. Deduplicate by email + company
  6. Output: CSV with Name, Title, Company, Email, Phone, LinkedIn, FitScore, Rationale

Constraints:
  - Only report data returned by Apollo API
  - No invented email addresses or phone numbers
  - Fit score must be justified in Rationale column
  - Limit results to [limit] top prospects by fit score
  - Sort by fit score descending

Deliver: prospects.csv with [count] prospects, ranked by fit score, [estimated time]
```

---

### Step 3 — Format Results

After prospecting completes, format and deliver results:

```
LEAD GENERATION QUICK SCAN RESULTS
═════════════════════════════════════════════════════════════════

ICP: [parsed ICP description]
Execution date: [date]
Scan duration: [X seconds]

SUMMARY
──────────────────────────────────────────────────────────────
Prospects found: [N]
Top fit score: [X/100]
Average fit score: [Y/100]
Lowest fit score: [Z/100]

TOP 10 PROSPECTS (by fit score)
──────────────────────────────────────────────────────────────
Rank | Name | Title | Company | Email | Fit Score | Rationale
  1  | [name] | [title] | [company] | [email] | [score] | [reason]
  2  | ...
  [continues for top 10]

DISTRIBUTION
──────────────────────────────────────────────────────────────
Prospects by seniority:
  - C-Suite: [N]
  - VP/Director: [N]
  - Manager: [N]
  - Individual Contributor: [N]
  - Other: [N]

Prospects by industry:
  - [Industry 1]: [N]
  - [Industry 2]: [N]
  [...]

Prospects by location:
  - [Region 1]: [N]
  - [Region 2]: [N]
  [...]

SCORE RANGES
──────────────────────────────────────────────────────────────
90-100 (Excellent fit):   [N] prospects
80-89  (Very good fit):   [N] prospects
70-79  (Good fit):        [N] prospects
60-69  (Fair fit):        [N] prospects
Below 60 (Lower priority): [N] prospects

DATA QUALITY
──────────────────────────────────────────────────────────────
Email verified: [X%]
Phone available: [Y%]
LinkedIn profile: [Z%]

EXPORTED FILES
──────────────────────────────────────────────────────────────
• prospects.csv — [N] prospects with full contact data and fit scores
[• prospects.json — Same data in JSON format (if --output includes json)]

NEXT STEPS
──────────────────────────────────────────────────────────────

Option 1: Use for manual outreach
  - Review prospects.csv
  - Filter by fit score and seniority
  - Prepare personalized messaging
  - Reach out directly

Option 2: Upgrade to full pipeline
  - Run /lead-gen:prospect --icp "[same]" --enrich --sequence --crm-sync
  - Get full enrichment, outreach templates, CRM sync
  - Takes 2-3x longer but higher conversion

Option 3: Filter and refine
  - Adjust ICP filters (industry, location, company size)
  - Re-run quick scan for refined results
  - Narrow targeting for higher quality leads

═════════════════════════════════════════════════════════════════
```

---

### Step 4 — Save Outputs

Save prospecting results:
- `prospects.csv` — Primary output with all prospect data
- `prospects.json` — JSON format (if requested)
- `scan_metadata.json` — Execution metadata (count, scores, timestamps)

---

### Anti-Hallucination Rules

For lead-gen:quick command:

1. **Only prospect** — Do not run enrichment, outreach, or CRM sync
2. **Never invent prospect data** — Only include what Apollo returns
3. **Never promise lead quality** — Prospects are candidates, not validated sales leads
4. **Fit score must be justified** — Always include reasoning in Rationale column
5. **Never skip deduplication** — Always deduplicate by email + company before ranking
6. **Only use Apollo data** — No external data sources or guesses
7. **Respect limit parameter** — Never exceed --limit, cap at 500 maximum
8. **Always sort by fit score** — Deliver prospects ranked by score, highest first

---

### Performance Notes

Expected execution times:
- 20 prospects: 10-15 seconds
- 50 prospects: 20-30 seconds
- 100 prospects: 30-45 seconds
- 200 prospects: 45-60 seconds
- 500 prospects: 60-90 seconds

Times depend on Apollo API responsiveness and filter complexity.
