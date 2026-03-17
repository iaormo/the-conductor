---
name: data-research
description: "Triggered when extracting data, conducting market research, competitive intelligence, or business intelligence analysis. Use during prospecting and lead enrichment phases."
---

# Data Research Skill

## When to use

- Lead generation and prospect qualification during business development
- Market sizing and industry analysis for new business opportunities
- Competitive intelligence gathering and positioning analysis
- Customer data enrichment and segmentation
- Business intelligence metric aggregation and trend analysis
- Sales pipeline analysis and forecast modeling

## Workflow

1. **Source identification**: Determine available data sources (public APIs, proprietary databases, research platforms)
2. **Query design**: Formulate extraction queries with appropriate filters and parameters
3. **Data collection**: Execute extraction with error handling and validation
4. **Cleansing**: Remove duplicates, normalize formats, validate completeness
5. **Enrichment**: Augment with additional data from complementary sources
6. **Analysis**: Apply aggregation, trending, and comparative analysis
7. **Logging**: Submit insights to persistence layer with structured format

## Key patterns

### Lead Extraction & Enrichment
```
- Company data: Domain, industry, employee count, revenue, funding history
- Contact data: Name, title, email, phone, LinkedIn profile
- Engagement signals: Website activity, content downloads, webinar attendance
- Company signals: Recent funding rounds, executive changes, technology adoption
- Firmographic targeting: Company size, location, technology stack
```

### Market Research Analysis
```
- Market sizing: TAM (Total Addressable Market), SAM (Serviceable Available Market)
- Industry trends: Growth rates, adoption curves, emerging technologies
- Technology landscape: Tool proliferation, integration patterns, competitive features
- Regulatory environment: Compliance requirements, industry standards
- Customer pain points: Survey data, support ticket analysis, user feedback
```

### Competitive Intelligence
```
- Competitor feature sets and product positioning
- Pricing strategy and go-to-market approach
- Customer base and industry coverage
- Funding and investment history
- Executive team and organizational structure
- Marketing messaging and positioning claims
- Integration ecosystem and technology partnerships
```

### Business Intelligence
```
- Sales pipeline metrics: Stage distribution, conversion rates, ACV trends
- Customer metrics: CAC (Customer Acquisition Cost), LTV (Lifetime Value), churn
- Operational metrics: Deal velocity, sales cycle length, win rates by segment
- Product metrics: Feature usage, user engagement, retention cohorts
- Financial metrics: Revenue by segment, margin analysis, forecasting
```

## Output format

For each finding or insight, log:

```python
log_finding(
    agent_name="data-research",
    team="business-development",
    severity="[INFO|LOW|MEDIUM|HIGH|CRITICAL]",  # For research context
    category="[lead-generation|prospecting|market-research|competitive-intelligence|business-intelligence]",
    title="[Brief insight title]",
    detail="[Source] — [Key metric, finding, or trend with supporting numbers]",
    reference="[Data source, methodology, confidence level]",
    remediation="[Action or recommendation based on insight]",
)
```

### Example output

```
Insight: High-growth fintech segment with underserved compliance tooling market
Source: Crunchbase, G2, industry reports
Finding: 247 fintech companies raised >$10M in last 12 months; 78% report compliance as top operational challenge
Market Size: TAM $8.3B, SAM $1.2B, SOM $45M (Year 1)
Competitors: 12 direct competitors, 3 with >$100M funding
Confidence: HIGH
Recommendation: Target Series B/C fintech companies (50-500 employees) with expansion into APAC markets

---

Prospect Enrichment: Acme Corp, Inc.
Source: Apollo, Crunchbase, company website
Findings:
- 287 employees, $18M revenue (est.), founded 2019
- Recent Series B ($8M) indicates growth trajectory
- 4 job openings: 2 for Engineering, 2 for Sales
- Technology stack: AWS, React, PostgreSQL (from stackshare)
- Recent exec hire: CTO from Stripe (strong technical credibility)
Recommendation: High-priority target (growth stage, technical team, expansion hiring)
```

## Data quality standards

For each extraction, validate:
- **Completeness**: Fields populated (flag missing data >10%)
- **Uniqueness**: Deduplicate records by company domain and contact email
- **Recency**: Flag data older than 6 months without refresh
- **Accuracy**: Cross-reference against multiple sources for critical metrics
- **Consistency**: Format normalization (phone, email, date fields)

## False positive handling

Adjust confidence or de-prioritize findings in:
- Outdated sources (data >12 months old without confirmation)
- Conflicting data across sources (flag as "requires verification")
- Speculative or projected metrics (explicitly label as forecast)
- Small sample sizes (<5 data points for trend conclusions)

## Reference standards

- [Crunchbase Research Methodology](https://www.crunchbase.com/)
- [G2 Review Aggregation](https://www.g2.com/)
- [Gartner Magic Quadrant Methodology](https://www.gartner.com/en/research/magic-quadrant)
- [SiriusDecisions Sales Benchmarks](https://www.forrester.com/)
- [LinkedIn Sales Navigator Best Practices](https://business.linkedin.com/en-us/sales-solutions/sales-navigator)
