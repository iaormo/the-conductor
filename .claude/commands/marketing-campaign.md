---
name: marketing:campaign
description: >
  Orchestrate Division 6 (Marketing & Content) campaigns across content creation,
  email marketing, social media, and SEO. Creates blog posts, whitepapers, case
  studies, email sequences, social content calendars, and SEO audits. Supports
  multiple content types and platforms with integrated reporting.
---

# Marketing Campaign Orchestrator

Run comprehensive marketing campaigns across Division 6 (Marketing & Content).
Orchestrates 4 specialist agents to produce content, manage campaigns, and optimize for search.

## Usage

```
/marketing:campaign --type blog --topic "AI in healthcare" --audience "CTOs" --keywords "AI, machine learning, healthcare"
/marketing:campaign --type whitepaper --subject "Security trends 2026" --research-focus "Zero Trust" --format pdf
/marketing:campaign --type case-study --client "Acme Corp" --metrics "40% faster deployment" --approval-status draft
/marketing:campaign --type email-sequence --goal "welcome" --audience "new-prospects" --frequency daily
/marketing:campaign --type email-sequence --goal "nurture" --segment "trial-users" --duration "12 weeks"
/marketing:campaign --type email-sequence --goal "re-engagement" --inactive-days 30 --audience "dormant-leads"
/marketing:campaign --type social --platforms "linkedin,twitter,instagram" --content-from blog --topic "AI trends"
/marketing:campaign --type social --platform linkedin --format article --topic "Zero Trust Strategy" --author "CEO"
/marketing:campaign --type social --platform instagram --format carousel --topic "Team highlights"
/marketing:campaign --type social --calendar --quarter "Q2 2026" --focus "product-launch,thought-leadership"
/marketing:campaign --type seo-audit --url "https://example.com" --depth full --competitors 3
/marketing:campaign --type seo-audit --url "https://example.com" --focus on-page --keyword "target-keyword"
```

## Instructions

You are orchestrating Division 6 (Marketing & Content) with 4 specialist agents.
Run agents in parallel by default unless workflow requires sequencing.
All campaigns log findings to persistence/severity_logger.py for reporting integration.

---

### Step 1 — Parse Campaign Arguments

Extract from `$ARGUMENTS`:

```
CONTENT TYPE (Required):
  --type [blog|whitepaper|case-study|email-sequence|social|seo-audit]

BLOG-SPECIFIC:
  --topic: Topic/subject matter
  --audience: Target persona (role, industry, expertise level)
  --keywords: Comma-separated target keywords
  --length: Word count (default 1200)
  --format: [standard|listicle|q&a|tutorial|case-study] (default: standard)
  --cta: Call-to-action (newsletter, demo, product, etc.)

WHITEPAPER-SPECIFIC:
  --subject: Topic/title area
  --research-focus: Primary research angle
  --length: Word count (default 4000)
  --format: [pdf|markdown|html] (default: pdf)
  --include-visuals: Include charts/infographics (default: yes)

CASE-STUDY-SPECIFIC:
  --client: Client company name
  --metrics: Key metrics/outcome (e.g., "40% faster")
  --industry: Client industry
  --company-size: Employee count or revenue range
  --approval-status: [draft|ready-for-review|approved] (default: draft)

EMAIL-SEQUENCE-SPECIFIC:
  --goal: [welcome|nurture|re-engagement|promotional] (default: nurture)
  --audience: Audience segment (new-prospects, trial-users, customers, etc.)
  --frequency: Send frequency [daily|2x-week|weekly|bi-weekly] (default: weekly)
  --duration: Campaign duration (e.g., "12 weeks", "ongoing")
  --segment: Audience segmentation criteria
  --inactive-days: Days inactive (for re-engagement)
  --subject-line-test: A/B test count (2, 3, 4 variants)

SOCIAL-SPECIFIC:
  --platforms: Target platforms [linkedin|twitter|instagram] (comma-separated)
  --platform: Single platform (alternative to --platforms)
  --format: [article|thread|carousel|single-image|reel|post]
  --content-from: Source [blog|whitepaper|existing-content]
  --topic: Content topic
  --calendar: Generate calendar (yes/no)
  --quarter: Quarter for calendar [Q1|Q2|Q3|Q4] [year]
  --focus: Focus themes [thought-leadership|product|educational|promotional]
  --author: Author name (for bylined content)

SEO-AUDIT-SPECIFIC:
  --url: Website URL to audit (required)
  --depth: Audit depth [full|on-page|technical|keywords|competitors]
  --focus: Focus area [on-page|technical|content|all] (default: all)
  --keyword: Primary target keyword
  --competitors: Number of competitors to analyze (default: 3)

OPTIONAL (All types):
  --output: Output format [markdown|pdf|html|csv|json] (default: markdown)
  --brand-guidelines: Path to brand guide document
  --target-date: Target completion date
  --priority: [high|medium|low] (default: medium)
  --assign-to: Team member email (optional)
```

**Validation:**
- Campaign type is valid
- Required fields are present (--type always, plus type-specific fields)
- Output format is valid
- Date fields are valid ISO 8601 format

---

### Step 2 — Route to Appropriate Agent(s)

Based on `--type`, spawn agent task(s):

**IF type = "blog" OR "whitepaper" OR "case-study":**

Task: Content Writer Agent

```
Create [content-type] on topic: [topic]

Requirements:
  - Target audience: [audience]
  - Primary keywords: [keywords]
  - Output format: [format]
  - Word count target: [length]
  - Brand voice: [infer from guidelines or use professional]
  - Deliverables:
    * Final content
    * Metadata (title, keywords, CTA, etc.)
    * SEO score (80-100 range)
    * Brand voice match (90-100%)

Quality gates:
  - Grammar/spellcheck: 100% pass
  - Fact-checked: All claims verified
  - Brand-compliant: No prohibited terms
  - SEO-optimized: Keywords integrated naturally

Output: [Content file] + metadata.json
```

**WAIT for completion before proceeding to Step 3.**

---

**IF type = "email-sequence":**

Task: Email Campaign Agent

```
Design email campaign: [goal]

Requirements:
  - Goal: [welcome|nurture|re-engagement|promotional]
  - Audience segment: [audience]
  - Frequency: [frequency]
  - Duration: [duration]
  - Deliverables:
    * Email sequence (3-7 emails depending on goal)
    * Subject line variants (primary + alternatives)
    * Segment definitions
    * A/B test recommendations (if applicable)
    * Performance benchmarks and targets
    * Engagement triggers and branch logic

Quality gates:
  - Subject lines optimized for open rate
  - Copy is scannable and compelling
  - CTAs are clear and action-focused
  - Legal compliance (CAN-SPAM, GDPR)
  - Segment definitions are realistic

Output: Campaign plan + sequence files + performance targets
```

**WAIT for completion before proceeding to Step 3.**

---

**IF type = "social":**

Task: Social Media Agent

```
Create social media content: [platforms]

Requirements:
  - Platform(s): [platforms list]
  - Format: [format type]
  - Topic: [topic]
  - Source content: [if adapting from existing]
  - Deliverables:
    * Platform-specific posts (optimized for each platform)
    * Hashtag research & recommendations
    * Content calendar (if --calendar requested)
    * Engagement strategy
    * Performance expectations per platform
    * Link/UTM parameter tracking setup

Quality gates:
  - Posts optimized for platform specs (character length, visual requirements)
  - Hashtags researched and tested
  - CTAs aligned with platform norms
  - Tone consistent with brand voice
  - No cross-platform duplication

Output: Social content files + calendar + hashtag recommendations
```

**WAIT for completion before proceeding to Step 3.**

---

**IF type = "seo-audit":**

Task: SEO Analyst Agent

```
Conduct SEO audit: [url]

Requirements:
  - Target URL: [url]
  - Audit scope: [depth]
  - Focus areas: [focus]
  - Primary keyword: [keyword] (if specified)
  - Competitors: [number] (default 3)
  - Deliverables:
    * On-page SEO audit (titles, meta, headings, keywords, alt text)
    * Technical SEO assessment (speed, mobile, security, schema, structure)
    * Keyword research & gap analysis
    * Competitive analysis (top 3 competitors)
    * Site health metrics (Core Web Vitals, load time)
    * Prioritized action plan (quick wins, short-term, long-term)
    * Performance tracking recommendations

Quality gates:
  - All findings are data-driven (no speculation)
  - Recommendations are specific and actionable
  - Severity levels are accurate
  - Competitive data is verified from actual rankings
  - Report is comprehensive and prioritized

Output: Audit report (PDF/markdown) + action plan + keyword recommendations
```

**WAIT for completion before proceeding to Step 3.**

---

### Step 3 — Review Quality and Compliance

After agent(s) complete:

```
QUALITY CHECKLIST:

For content deliverables:
  ☐ Meets brand voice guidelines (if provided)
  ☐ No typos, grammar errors, clarity issues
  ☐ Factually accurate (claims verified)
  ☐ Keywords naturally integrated (not stuffed)
  ☐ CTA is clear and compelling
  ☐ Format matches requested type
  ☐ Metadata is complete and accurate

For email campaigns:
  ☐ Subject lines optimized for opens
  ☐ Copy is scannable and compelling
  ☐ CTAs are unambiguous
  ☐ Legal disclaimers present (if needed)
  ☐ Unsubscribe link included
  ☐ Segment definitions are realistic
  ☐ Trigger logic is sound

For social content:
  ☐ Platform-specific formatting correct
  ☐ Hashtags researched and relevant
  ☐ Character limits respected
  ☐ Visual requirements met
  ☐ Tone consistent with brand
  ☐ Engagement strategy clear
  ☐ Links tracked with UTM parameters

For SEO audit:
  ☐ All findings have evidence/data
  ☐ Recommendations are actionable
  ☐ Severity prioritization is accurate
  ☐ Competitive analysis is verified
  ☐ Action plan is realistic and phased
  ☐ Metrics are specific and measurable
```

---

### Step 4 — Log Findings to Persistence

For all campaign types, log structured findings:

```python
log_finding(
    agent_name="[agent-name]",
    team="marketing",
    severity="[INFO|LOW|MEDIUM|HIGH|CRITICAL]",
    category="[content|email|social|seo]",
    title="[Campaign deliverable summary]",
    detail="[Key outcomes, metrics, or findings]",
    reference="[Campaign ID or URL]",
    remediation="[Approval/review/publication next steps]",
)
```

Examples:

```python
# Content creation
log_finding(
    agent_name="content-writer-agent",
    team="marketing",
    severity="INFO",
    category="content",
    title="Blog post created: 'AI in Healthcare'",
    detail="1200-word article optimized for keywords: AI, healthcare, ML. SEO score: 88/100. Brand voice match: 95%.",
    reference="blog-ai-healthcare-2026",
    remediation="Ready for editorial review and publication. Recommend publishing Tuesday morning.",
)

# Email campaign
log_finding(
    agent_name="email-campaign-agent",
    team="marketing",
    severity="INFO",
    category="email",
    title="Welcome sequence designed: 5-email nurture campaign",
    detail="Sequence targets new prospects. Subject lines optimized for 35-45% open rate. Segment: high-engagement leads (est. 500 recipients).",
    reference="email-welcome-new-2026",
    remediation="Ready for stakeholder review. Send time optimization: test Tuesday 10am vs Thursday 2pm.",
)

# Social campaign
log_finding(
    agent_name="social-media-agent",
    team="marketing",
    severity="INFO",
    category="social",
    title="Q2 social calendar created: 90 posts across 3 platforms",
    detail="Content distribution: 40% educational, 25% social proof, 20% promotional, 15% engagement. LinkedIn articles: 2. Twitter threads: 12.",
    reference="social-calendar-q2-2026",
    remediation="Ready for approval. Recommend scheduling via Buffer/Hootsuite. Monitor engagement weekly.",
)

# SEO audit
log_finding(
    agent_name="seo-analyst-agent",
    team="marketing",
    severity="MEDIUM",
    category="seo",
    title="SEO audit completed: example.com on-page optimization gaps",
    detail="On-page score: 72/100. Quick wins: missing keywords in 8 title tags, 12 pages without meta descriptions. Keyword gap: 47 competitor keywords not targeted.",
    reference="seo-audit-example.com-2026",
    remediation="Fix critical on-page issues within 1 week. Expand 3 top pages with better content. Create 2 new high-opportunity keyword pages.",
)
```

---

### Step 5 — Generate Campaign Summary Report

Synthesize all deliverables:

```
CAMPAIGN SUMMARY REPORT — [Campaign Name]
=========================================

Campaign Details:
  Type: [blog|email|social|seo]
  Objective: [Primary goal]
  Duration: [Timeframe]
  Team: Division 6 (Marketing & Content)
  Status: [Draft|Ready for Review|Approved|Active]

KEY DELIVERABLES:
  [List each deliverable with brief description]

TIMELINE:
  Created: [Date]
  Scheduled for review: [Date]
  Target launch: [Date]

METRICS & EXPECTATIONS:

For Blog/Whitepaper:
  - SEO score: [X]/100
  - Brand voice match: [X]%
  - Estimated organic traffic (6 months): [estimate]
  - Target keyword ranking: [position in 12 weeks]

For Email Sequences:
  - Audience size: [segment count]
  - Expected open rate: [benchmark]%
  - Expected CTR: [benchmark]%
  - Expected conversion: [benchmark]%

For Social Campaigns:
  - Posts: [count] across [platforms]
  - Estimated reach: [estimate]
  - Expected engagement rate: [benchmark]%
  - Follower growth estimate: [estimate/month]

For SEO Audits:
  - Issues found: [critical], [high], [medium], [low]
  - Quick wins: [count] (1-2 weeks to implement)
  - Estimated organic traffic potential: [estimate]
  - Implementation timeline: [3-month plan]

NEXT STEPS:
  1. [First action]
  2. [Second action]
  3. [Third action]

APPROVALS REQUIRED:
  - [ ] Content/Campaign owner sign-off
  - [ ] Brand compliance review (if applicable)
  - [ ] Legal review (if applicable, email campaigns)
```

---

### Step 6 — Output Deliverables

Provide all campaign assets:

```
FOLDER STRUCTURE (Generated):

/marketing-campaigns/[campaign-id]/
  ├── campaign-summary.md          (report above)
  ├── content/
  │   ├── [blog-post].md
  │   ├── [whitepaper].pdf
  │   └── [case-study].md
  ├── email/
  │   ├── sequence-plan.md
  │   ├── email-1-welcome.html
  │   ├── email-2-follow-up.html
  │   └── segment-definitions.json
  ├── social/
  │   ├── content-calendar.csv
  │   ├── linkedin-posts.md
  │   ├── twitter-threads.md
  │   ├── instagram-captions.md
  │   └── hashtag-strategy.md
  ├── seo/
  │   ├── audit-report.pdf
  │   ├── keyword-recommendations.csv
  │   ├── action-plan.md
  │   └── competitor-analysis.md
  └── metadata.json                (campaign tracking)
```

---

## Anti-hallucination rules

- Never invent metrics or performance data without basis
- Never promise specific ranking positions or timeframes
- Never invent competitor metrics or search volumes
- Never create fake client case studies without approval
- Never invent email engagement benchmarks (cite industry sources)
- Never fabricate social media analytics (use industry benchmarks)
- Never claim SEO improvements without data-backed methodology

## Success criteria

Campaign execution is successful when:

✓ All deliverables are complete and meet quality standards
✓ Content is brand-compliant and factually accurate
✓ Email sequences are legally compliant (CAN-SPAM, GDPR)
✓ Social content is platform-optimized and engaging
✓ SEO recommendations are data-driven and actionable
✓ All findings logged to persistence layer
✓ Stakeholders have clear review/approval path
✓ Implementation timeline is realistic and documented
