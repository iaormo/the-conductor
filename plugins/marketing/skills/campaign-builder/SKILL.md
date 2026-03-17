---
name: campaign-builder
description: "Triggered when building, executing, or analyzing marketing campaigns across email, social media, and content channels. Use during outreach and engagement phases."
---

# Campaign Builder Skill

## When to use

- Prospect engagement campaigns during lead development
- Product launch and announcement campaigns
- Thought leadership content distribution
- Customer education and onboarding campaigns
- Event promotion and registration campaigns
- Multi-channel nurture sequences for sales pipeline

## Workflow

1. **Campaign definition**: Define objectives, target audience, channels, and success metrics
2. **Audience segmentation**: Identify and segment prospects by firmographics, behavior, engagement
3. **Content planning**: Develop messaging, creative assets, and scheduling across channels
4. **Campaign setup**: Configure automation, tracking, personalization, and triggers
5. **Execution**: Launch campaign across coordinated channels
6. **Monitoring**: Track performance, engagement, conversions, and attribution
7. **Logging**: Submit campaign metrics and insights to persistence layer

## Key patterns

### Email Campaign Strategy
```
- Objective: Lead nurturing, product education, event promotion, re-engagement
- Audience: Firmographic targeting (company size, industry, role)
- Segmentation: Behavioral triggers (website visit, content download, engagement level)
- Personalization: Company name, role-specific messaging, content recommendations
- Content: Value-focused subject lines, clear CTAs, mobile-optimized design
- Cadence: Optimal frequency (2-3x per week), time zone optimization
- A/B testing: Subject lines, CTAs, send times, content variations
- Metrics: Open rate (target >25%), Click rate (target >3%), Conversion rate
```

### Social Media Campaigns
```
- Platform strategy: LinkedIn (B2B, thought leadership), Twitter (news, engagement), YouTube (education)
- Content types: Educational posts (40%), industry insights (30%), promotional (20%), engagement (10%)
- Cadence: LinkedIn (3-5x week), Twitter (1-3x daily), YouTube (weekly long-form)
- Engagement: Response to comments within 24h, community participation, retweets
- Analytics: Impressions, engagement rate (target >3%), share of voice, reach
- Hashtag strategy: Branded + industry hashtags, trending topic monitoring
- Influencer partnerships: Thought leader mentions, co-marketing opportunities
```

### Content Strategy
```
- Topic clusters: Core topic families (e.g., security, compliance, cloud infrastructure)
- Content types: Blog posts, whitepapers, case studies, webinars, guides, videos
- SEO optimization: Keyword research (target keywords <50 competition score)
- Publishing cadence: 2-4 blog posts monthly, 1 whitepaper quarterly, 1-2 webinars monthly
- Promotion: Email distribution, social amplification, influencer sharing
- Performance: Page views, time on page (target >3min), lead capture rate (target >5%)
- Repurposing: Convert blogs to social snippets, whitepapers to webinar scripts
```

### Multi-Channel Orchestration
```
- Journey mapping: Prospect awareness → consideration → decision stages
- Touchpoint design: Email → content → webinar → sales conversation
- Timing: Optimal intervals between touchpoints (24-48h minimum)
- Personalization: Role-specific messaging, company-relevant content
- Attribution: Track which channels drive conversion, optimize budget allocation
- Frequency capping: Max 5 touchpoints/week, prevent message fatigue
- Coordination: Ensure consistent messaging and branding across channels
```

## Output format

For each campaign or insight, log:

```python
log_finding(
    agent_name="campaign-builder",
    team="marketing",
    severity="[INFO|LOW]",  # For marketing context
    category="[email-campaign|social-media|content-strategy|campaign-orchestration|seo-optimization]",
    title="[Campaign name or insight title]",
    detail="[Objective, audience, channels] — [Key metrics or performance data]",
    reference="[Campaign template, best practice source, or performance benchmark]",
    remediation="[Optimization or next action recommendation]",
)
```

### Example output

```
Campaign: Series B Fintech Outreach
Objective: Generate qualified opportunities from growth-stage fintech companies
Audience: 250 prospects (CFOs, VPs Finance, Compliance Officers) at Series B fintech companies
Channels: LinkedIn, Email (weekly), webinar (monthly)
Schedule: 8-week sequence
Content: Compliance automation ROI, regulatory trends, customer success stories
Metrics Target: 15% open rate, 3% click rate, 5% meeting booking rate
Estimated Opportunities: 12-15 qualified conversations

---

Content Strategy: Compliance Trends Quarterly
Topics: Regulatory changes, emerging standards, best practices, compliance automation
Format: Blog series (4 posts), 1 long-form whitepaper, 1 industry webinar
Audience: Compliance teams, RegTech decision-makers, enterprise security
SEO Targets: "compliance automation ROI" (52 searches/month), "emerging compliance standards"
Distribution: Email list (5K), LinkedIn (18K followers), partner syndication
Expected Performance: 8-12K impressions, 3-5% CTR, 400-600 leads
ROI: $2-3K per conversion, target 10-15 conversions
```

## Campaign management best practices

- **Lead scoring**: Assign points for email opens (+1), clicks (+3), webinar attendance (+10)
- **Engagement thresholds**: Pause after 3 consecutive non-opens; re-activate on engagement spike
- **Feedback loops**: Track bounces, unsubscribes, complaints; maintain list health >98%
- **Personalization depth**: Use company research, recent news, job change signals for messaging
- **Testing cadence**: Run A/B tests on 20% of segment; validate statistical significance (n>100)

## False positive handling

De-prioritize or adjust findings in:
- New campaigns (first 2 weeks of data insufficient for trend analysis)
- Holiday periods (adjust expected engagement rates)
- List quality issues (flag separately from campaign performance)
- External events (competitive announcements, industry news affecting engagement)

## Reference standards

- [HubSpot Email Marketing Benchmarks](https://www.hubspot.com/email-marketing-benchmarks)
- [Campaign Monitor Best Practices](https://www.campaignmonitor.com/guides/)
- [Content Marketing Institute Standards](https://contentmarketinginstitute.com/)
- [SEMrush SEO Best Practices](https://www.semrush.com/)
- [Hootsuite Social Media Best Practices](https://blog.hootsuite.com/)
