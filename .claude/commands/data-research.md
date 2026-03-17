---
name: data:research
description: >
  Execute data research, extraction, and intelligence tasks. Routes requests to
  market research, competitive intelligence, and data extraction agents. Supports
  market analysis, competitor tracking, web scraping, and dashboard creation.
  Multi-mode research engine for Division 5 (Data & Analytics).
---

# Data Research Command

## Overview

The `/data:research` command orchestrates Division 5 (Data & Analytics) agents to
conduct market research, competitive intelligence, data extraction, and business
intelligence dashboard generation.

## Usage patterns

### Pattern 1: Market research

```bash
/data:research --topic "medtech SaaS market 2026" --depth deep
/data:research --topic "AI security tools market growth" --depth quick
/data:research --topic "Zero Trust Architecture adoption" --segments enterprise,midmarket
```

**Route to:** market-research-agent

**Agent tasks:**
1. Define research scope and questions
2. Conduct web searches for market data
3. Gather analyst reports and industry data
4. Compile market size, growth rates, segments
5. Generate comprehensive research report

**Output:**
- Markdown research report with sources
- JSON structured data (market size, segments, trends)
- HTML formatted report
- Competitive landscape summary

---

### Pattern 2: Competitive analysis

```bash
/data:research --competitors "CrowdStrike, Palo Alto Networks, Microsoft Defender" --mode competitive
/data:research --competitor CrowdStrike --analysis features,pricing,positioning
/data:research --topic "Cloud security" --competitors "all" --depth detailed
```

**Route to:** competitive-intel-agent

**Agent tasks:**
1. Identify competitor product portfolio
2. Analyze pricing and feature positioning
3. Track win/loss patterns
4. Monitor organizational activity (hiring, partnerships)
5. Identify market gaps and opportunities
6. Generate competitive intelligence report

**Output:**
- Competitive positioning matrix
- Feature comparison table
- Win/loss analysis with patterns
- Market gap and opportunity analysis
- Threat and opportunity assessment

---

### Pattern 3: Web data extraction

```bash
/data:research --url "https://example.com/data" --mode extract
/data:research --url "https://example.com/directory" --mode scrape --pagination true
/data:research --urls "list.txt" --format csv --output extracted_data.csv
```

**Route to:** data-extraction-agent

**Agent tasks:**
1. Assess data source (website, API, PDF)
2. Extract structured data using CSS selectors, XPath, or API calls
3. Handle pagination and rate limiting
4. Normalize and validate extracted data
5. Deduplicate records
6. Output clean CSV/JSON datasets

**Output:**
- CSV file with extracted data
- JSON file with structured records
- Extraction log with record counts, errors
- Data quality report

---

### Pattern 4: Dashboard creation

```bash
/data:research --query "SELECT severity, COUNT(*) FROM findings GROUP BY severity" --mode dashboard
/data:research --source audit.db --kpis "critical_findings,high_findings,remediation_progress" --mode dashboard
/data:research --csv leads.csv --dashboard kpis --output sales_pipeline_dashboard.html
```

**Route to:** bi-dashboard-agent

**Agent tasks:**
1. Connect to data source (SQLite, Postgres, CSV)
2. Execute queries and aggregate data
3. Define KPIs and metrics
4. Select appropriate chart types
5. Generate interactive HTML dashboard
6. Create dashboard with D3.js/Chart.js visualizations

**Output:**
- Interactive HTML dashboard
- Embedded KPI cards with alerts
- Interactive charts and graphs
- Dashboard metadata (created_at, data_source, refresh info)

---

### Pattern 5: Integrated research workflow

```bash
/data:research --topic "enterprise security market" --depth comprehensive --mode integrated
  # Runs: market sizing → competitive landscape → customer analysis → trend analysis

/data:research --domain "cloud security" --analyze "market_size,competitors,gaps,trends"
  # Runs: market research + competitive intelligence + opportunity identification

/data:research --project "product_planning_2026" --analysis full
  # Runs: market sizing → competitive landscape → win/loss analysis →
  #       opportunity identification → recommendations
```

**Route to:** market-research-agent + competitive-intel-agent

**Agent workflow:**
1. Market-research-agent: Market sizing, segments, trends
2. Competitive-intel-agent: Competitor positioning, opportunities
3. Synthesis: Combined findings, gap analysis, recommendations

**Output:**
- Integrated research report (30-50 pages)
- Executive summary with key findings
- Market sizing and segment analysis
- Competitive landscape
- Customer segment analysis
- Trend analysis
- Market gap identification
- Strategic recommendations

---

## Parameters

### Common parameters (all modes)

- `--topic STRING` — Research topic or area
- `--depth LEVEL` — Research depth: `quick` | `standard` | `deep` (default: standard)
- `--output STRING` — Output filename (default: auto-generated)
- `--format FORMAT` — Output format: `markdown` | `html` | `json` | `csv` (default: markdown)

### Market research parameters

- `--topic STRING` — Market topic (required)
- `--segments STRING` — Comma-separated segments to focus on (optional)
- `--timeframe STRING` — Time period: `2024`, `2024-2026`, `5year` (default: current year)
- `--include_forecast BOOL` — Include market forecasts (default: true)
- `--competitor_analysis BOOL` — Include competitive landscape (default: true)

### Competitive analysis parameters

- `--competitors STRING` — Comma-separated competitor names or "all"
- `--analysis STRING` — Analysis type: `products,pricing,positioning,hiring,partnerships`
  (default: all)
- `--win_loss BOOL` — Include win/loss analysis (default: true)
- `--threat_assessment BOOL` — Include threat/opportunity assessment (default: true)

### Data extraction parameters

- `--url STRING` — URL to scrape
- `--urls STRING` — File containing URLs (one per line)
- `--mode STRING` — Extraction mode: `extract` | `scrape` (default: extract)
- `--pagination BOOL` — Handle pagination (default: true)
- `--rate_limit INT` — Rate limit in requests per second (default: 1)
- `--format STRING` — Output format: `csv` | `json` (default: csv)

### Dashboard parameters

- `--source STRING` — Data source: `audit.db` | `crm.db` | CSV filename (required)
- `--query STRING` — SQL query to execute
- `--kpis STRING` — Comma-separated KPI names
- `--charts STRING` — Chart types: `bar,line,pie,funnel,scatter` (default: auto)
- `--template STRING` — Dashboard template: `security` | `sales` | `financial` (default: blank)

---

## Command process

### Step 1: Parse request

```
Input: /data:research --topic "SaaS security market 2026" --depth deep

Parsed:
  - command: data:research
  - mode: market_research (inferred from --topic)
  - topic: SaaS security market 2026
  - depth: deep
  - format: markdown (default)
  - output: market_research_20260317_saas_security.md (auto-generated)
```

### Step 2: Route to appropriate agent(s)

```
Mode: market_research
  → Agent: market-research-agent
  → Task: Conduct deep market research on SaaS security market 2026
  → Input: topic, depth, segments, timeframe
  → Output: Comprehensive research report with market sizing, segments, trends
```

### Step 3: Agent execution

Each agent follows its standard workflow:
- Data gathering (web search, API queries, document extraction)
- Analysis and synthesis
- Validation and source checking
- Report generation
- Persistence logging (if audit-related)

### Step 4: Output generation

Format output according to requested format:
- **Markdown**: Report with structured sections, tables, citations
- **HTML**: Rendered report with styling, interactive elements
- **JSON**: Structured data for programmatic consumption
- **CSV**: Tabular data for spreadsheets

### Step 5: Logging and archival

Log to persistence layer (if applicable):

```python
# For audit-related research
log_finding(
    agent_name="market-research-agent",
    team="data-analytics",
    severity="INFO",
    category="research",
    title="Market Research: SaaS Security 2026",
    detail="Completed deep market analysis: TAM $50B, growth 13.5% CAGR",
    reference="market_research_20260317_saas_security.md"
)

# For competitive intelligence
log_finding(
    agent_name="competitive-intel-agent",
    team="data-analytics",
    severity="INFO",
    category="competitive-intelligence",
    title="Competitive Landscape Analysis",
    detail="Analyzed 8 competitors, identified 3 market gaps",
    reference="comp_intel_20260317_cloud_security.md"
)
```

---

## Example workflows

### Workflow 1: Pre-launch market validation

```bash
# Phase 1: Market sizing
/data:research --topic "compliance automation platform market" --depth deep

# Phase 2: Competitive analysis
/data:research --competitors "all" --analysis features,pricing,positioning

# Phase 3: Customer analysis
/data:research --topic "compliance automation" --analyze customer_segments

# Phase 4: Dashboard creation
/data:research --source research.json --kpis "tam,market_growth,competitor_count" --mode dashboard

# Output: Market validation report with sizing, competitive position, and go-to-market recommendations
```

### Workflow 2: Quarterly business review data

```bash
# Phase 1: Sales pipeline dashboard
/data:research --source crm.db --template sales --kpis "pipeline_value,conversion_rate,win_rate"

# Phase 2: Competitive win/loss analysis
/data:research --competitors "CrowdStrike,Palo Alto" --analysis win_loss --mode competitive

# Phase 3: Market trend tracking
/data:research --topic "cloud security" --segments "enterprise,midmarket" --mode market_research

# Output: Business review dashboard with sales metrics, competitive metrics, market trends
```

### Workflow 3: Customer data enrichment

```bash
# Phase 1: Extract prospect list
/data:research --url "https://example.com/companies" --mode scrape --pagination true

# Phase 2: Extract company data
/data:research --urls "company_urls.txt" --mode extract

# Phase 3: Normalize and output
# Output: clean_prospects.csv with company name, website, industry, headcount, location

# Phase 4: Create prospect dashboard
/data:research --source clean_prospects.csv --template sales --kpis "prospect_count,by_industry,by_location"
```

---

## Error handling

### Source not found

```
/data:research --url "https://example.com/data" --mode extract

ERROR: Could not reach source
  Reason: 404 Not Found
  Status: Source unavailable
  Action: Check URL and retry
  Fallback: Provide alternative source or manual data
```

### Rate limiting

```
/data:research --urls "urls.txt" --rate_limit 2

WARN: Rate limited by source
  Status: Retrying with exponential backoff
  Current rate: 1 request/2 seconds
  Estimated time: 50 minutes for 1,500 URLs
  Action: Continue with reduced rate or use API key
```

### Incomplete data

```
/data:research --topic "emerging market 2026" --depth deep

WARN: Limited data available
  Reason: Topic is emerging, limited analyst coverage
  Confidence: MEDIUM (based on 5 sources)
  Recommendation: Focus on existing sources, acknowledge data gaps
  Output: Report with confidence levels and caveats
```

---

## Output examples

### Market research output

```
# Enterprise SaaS Security Market 2026

## Executive Summary
- Total market size: $50B-$75B
- Growth rate (CAGR 2024-2030): 13.5%
- Key segments: Endpoint (30%), Identity (25%), Cloud (20%)
- Competitive landscape: 8 major players, emerging disruptors
- Top opportunity: SMB premium solution ($5B TAM)

## Market Sizing
## Competitive Landscape
## Customer Analysis
## Trend Analysis
## Recommendations

---

### Competitive intelligence output

```json
{
  "competitors_analyzed": 8,
  "market_gaps_identified": 3,
  "win_loss_summary": {
    "deals_analyzed": 45,
    "wins": 12,
    "losses": 8,
    "top_win_reason": "Price",
    "top_loss_reason": "Brand perception"
  },
  "recommendations": [
    "Launch SMB-focused product tier",
    "Focus sales on compliance vertical",
    "Differentiate on ease-of-use"
  ]
}
```

### Dashboard output

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sales Pipeline Dashboard</title>
</head>
<body>
    <div class="dashboard">
        <div class="kpi-grid">
            <div class="kpi-card">
                <h3>Pipeline Value</h3>
                <div class="value">$2.5M</div>
                <div class="target">Target: $2M</div>
            </div>
            ...
        </div>
        <div class="chart-grid">
            <canvas id="pipeline-funnel"></canvas>
            <canvas id="deals-by-stage"></canvas>
        </div>
    </div>
</body>
</html>
```

---

## Best practices

1. **Research depth vs speed** — Use `--depth quick` for initial scoping, escalate to `--depth deep` for important decisions
2. **Source verification** — Always verify sources, especially for market sizing data
3. **Regular updates** — Re-run competitive intelligence quarterly to track changes
4. **Cross-reference data** — Compare multiple sources to validate findings
5. **Acknowledge uncertainty** — Flag data gaps and confidence levels in reports
6. **Archive findings** — Save research reports for historical comparison

---

## Related commands

- `/report:generate` — Synthesize all data and research into comprehensive report
- `/compliance:gap-analysis` — Compliance and regulatory trend analysis (Division 1)
- `/lead-gen:prospect` — Lead generation and market research (Division 2)
