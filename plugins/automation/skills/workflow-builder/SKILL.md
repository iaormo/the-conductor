---
name: workflow-builder
description: "Triggered when setting up workflow automation, scheduling jobs, integrating external systems, or managing alerts. Use for cross-division automation and system coordination."
---

# Workflow Builder Skill

## When to use

- Scheduling recurring security audits and compliance scans
- Coordinating multi-step agent workflows with dependencies
- Integrating external data sources and systems
- Managing alert routing and escalation
- Automating report generation and distribution
- Synchronizing data across Division 1, 2, and 3 systems

## Workflow

1. **Workflow design**: Define steps, inputs, outputs, and error handling
2. **Dependency mapping**: Identify job dependencies and execution order
3. **Integration setup**: Configure API credentials, payload transformation, retry logic
4. **Scheduling**: Define triggers (cron, event-based, manual) and recurrence
5. **Alert configuration**: Set up notification rules and escalation policies
6. **Deployment**: Register workflow with scheduler and monitoring
7. **Logging**: Submit execution metrics to persistence layer

## Key patterns

### Workflow Orchestration
```
- Sequential execution: Job A completes → Job B starts
- Parallel execution: Jobs A and B run simultaneously, Job C waits for both
- Conditional logic: If result matches condition, branch to path X or path Y
- Error handling: On failure, retry up to N times with exponential backoff
- Timeout: Kill job if execution exceeds threshold (e.g., >1h)
- Dependency tracking: Block downstream jobs if upstream fails
- State management: Preserve workflow state for resume/replay capability
```

### API Integration Patterns
```
- Authentication: API key, OAuth 2.0, mTLS, custom headers
- Rate limiting: Respect API quotas, implement backoff strategy
- Payload transformation: Map source fields to target schema
- Error handling: Distinguish retryable (5xx) vs. non-retryable (4xx) errors
- Pagination: Handle multi-page results with cursor or offset
- Webhooks: Subscribe to system events for real-time triggers
- Data validation: Schema validation before submission
- Idempotency: Prevent duplicate operations with idempotency keys
```

### Job Scheduling Patterns
```
- Cron syntax: "0 2 * * *" (2am daily), "0 9 * * 1-5" (9am weekdays)
- One-time jobs: Execute once at specific datetime, then disable
- Recurring jobs: Execute on schedule indefinitely or until end date
- Job queues: FIFO or priority queue for job ordering
- Concurrency limits: Max parallel executions of same job type
- Execution windows: Run job only within allowed time windows
- Blackout periods: Skip execution during maintenance windows
```

### Alert Management
```
- Alert routing: Route to appropriate team/channel based on severity/category
- Escalation: Escalate unacknowledged alerts after N minutes
- Deduplication: Suppress duplicate alerts from same source
- Enrichment: Add context (owner, impacted service, remediation link)
- Notification channels: Email, Slack, PagerDuty, custom webhooks
- Frequency capping: Limit max notifications per time period
- Silence rules: Suppress known alerts during maintenance
```

### Error Handling & Retry
```
- Retry strategy: Exponential backoff (1s, 2s, 4s, 8s)
- Max retries: 3-5 attempts before failure
- Dead letter queue: Store failed jobs for manual review
- Circuit breaker: Stop retrying if error rate >10% over 5min
- Timeout handling: Distinguish timeout from actual failure
- Partial failure: Resume from last checkpoint (supports replay)
```

## Output format

For each workflow or automation insight, log:

```python
log_finding(
    agent_name="workflow-builder",
    team="automation",
    severity="[INFO|LOW|MEDIUM|HIGH|CRITICAL]",
    category="[workflow-automation|api-integration|job-scheduling|alert-management|error-handling]",
    title="[Workflow name or automation insight]",
    detail="[Trigger, steps, dependencies] — [Status, performance, or issue]",
    reference="[Standard practice, API documentation, or process reference]",
    remediation="[Setup instruction, improvement, or troubleshooting guidance]",
)
```

### Example output

```
Automation: Daily Security Audit Scheduler
Schedule: 2:00 AM UTC daily
Workflow:
  1. Trigger: cron "0 2 * * *"
  2. Step 1: Software Security team (Teams 2) scans in parallel
  3. Step 2: Infrastructure team (Team 3) scans in parallel
  4. Step 3: Await completion (max timeout 2 hours)
  5. Step 4: Compliance team (Team 4) generates summary report
  6. Step 5: Publish to persistence/audit.db
  7. Step 6: Notify CISO if findings >5 HIGH or >1 CRITICAL

Error Handling: Retry failed steps up to 3 times with exponential backoff
Alert: On complete failure, escalate to on-call DevOps after 15min
Performance: Target completion <90min, SLA 2 hours

---

Integration: Crunchbase Data Sync
Source: Crunchbase API (prospect company enrichment)
Trigger: Daily at 8:00 AM UTC
Steps:
  1. Authenticate with Crunchbase API key
  2. Query companies matching filters (industries=fintech, funding>$10M)
  3. Transform results: Map Crunchbase fields to internal schema
  4. Validate payload: Schema validation, data type checks
  5. Upsert to persistence/prospects table
  6. On error: Retry 3x with 5-min backoff; alert if final failure

Rate Limiting: Crunchbase API 100 requests/min; batch requests to respect quota
Deduplication: Merge by company domain; preserve historical funding data
Last Run: 2026-03-17T08:00:00Z, 387 companies synced, 12 updates, 0 errors

---

Alert: Audit Workflow Failure Detection
Rule: If workflow status=FAILED for >15min, escalate to CISO
Channels:
  1. Email to ciso@company.com
  2. Slack #security-alerts channel
  3. PagerDuty incident (severity=HIGH)
Enrichment: Include workflow name, failure step, error message, remediation link
Frequency: Max 1 alert per workflow per 30min (deduplication)
Silence: Disabled during scheduled maintenance windows (documented in STATUS page)
```

## Workflow design best practices

- **Timeout management**: Set reasonable timeouts (avoid infinite hangs); use SLA thresholds
- **Retry limits**: 3 retries covers transient failures; more indicates systemic issue
- **Monitoring**: Track execution time, success rate, queue depth, resource utilization
- **Documentation**: Document workflow logic, dependencies, and expected behavior
- **Version control**: Track workflow definition changes in Git; enable rollback
- **Testing**: Validate workflows in staging before production deployment
- **Graceful degradation**: Handle partial failures; continue when possible

## False positive handling

De-prioritize or adjust alerts in:
- Known system maintenance windows (explicit blackout periods)
- External system outages (acknowledge but continue workflow)
- High-volume legitimate alerts (increase deduplication window or suppress)
- Test/development workflows (isolate from production alert channels)

## Reference standards

- [CRON Expression Reference](https://crontab.guru/)
- [OpenAPI/Swagger Integration Standards](https://www.openapis.org/)
- [JSON Schema Validation](https://json-schema.org/)
- [REST API Best Practices](https://restfulapi.net/)
- [PagerDuty Alert Management](https://www.pagerduty.com/platform/alert-management/)
- [Temporal Workflow Engine](https://temporal.io/) (for complex orchestration)
