# automate — Orchestrate workflow automation, scheduling, and alerting

Designs and deploys automated workflows, integrations, schedules, and multi-channel
alerts. Connects business events to actions via the-conductor's automation layer.

## Usage

```
/automate:workflow --trigger "new-lead" --action "enrich,score,add-to-crm,notify-slack"
/automate:workflow --trigger "critical-finding" --action "alert-email,escalate,create-ticket"
/automate:workflow --trigger "invoice-overdue" --action "send-reminder,update-status,notify-pm"
/automate:workflow --trigger "cron:daily-9am" --action "run-security-scan,generate-report,email-ciso"

/automate:schedule --job "daily-security-report" --cron "0 6 * * *" --timezone "America/New_York"
/automate:schedule --job "weekly-audit" --cron "0 2 * * 0" --workflow "weekly-audit.yaml"
/automate:schedule --job "monthly-billing" --cron "0 1 1 * *" --workflow "billing-run.yaml"

/automate:alert --trigger "finding.critical" --channels "email,slack,sms" --recipients "ciso@company.com"
/automate:alert --trigger "lead.high-score" --channels "slack" --escalate-after "30m"
/automate:alert --trigger "invoice.overdue" --channels "email,slack" --escalate-to "finance,pm"

/automate:integration --service "jira" --action "create-issue" --auth "api-key"
/automate:integration --service "stripe" --action "get-invoice-status" --webhook-url "https://..."

/automate:test --workflow "new-lead-to-crm.yaml" --mode "dry-run"
/automate:deploy --workflow "new-lead-to-crm.yaml" --env "production"
```

## Instructions

You are orchestrating Division 7 automation infrastructure. Run agents in sequence,
ensuring each step builds on prior outputs. Validate integrations, test workflows,
and ensure proper persistence logging.

---

## Step 1 — Parse Automation Request

Extract from `$ARGUMENTS`:

**For workflows:**
- `--trigger`: Event type (new-lead, critical-finding, invoice-overdue, cron:daily-9am, webhook:name)
- `--action`: Comma-separated action list (enrich, score, add-to-crm, notify-slack, create-ticket, etc.)
- `--workflow-name`: Custom name for workflow (optional, auto-generated if not provided)
- `--timeout`: Workflow timeout in seconds (default: 300)
- `--test`: Dry-run mode (validate only, don't deploy)

**For schedules:**
- `--job`: Job name (daily-security-report, weekly-audit, monthly-billing)
- `--cron`: Cron expression (5-field format, e.g., "0 6 * * *")
- `--timezone`: Timezone for schedule (default: UTC)
- `--workflow`: Path to workflow to execute
- `--command`: Shell command to execute (alternative to workflow)

**For alerts:**
- `--trigger`: Event to alert on (finding.critical, lead.high-score, invoice.overdue)
- `--channels`: Alert channels (email, slack, sms, webhook, pagerduty)
- `--recipients`: Notification recipients (email addresses, Slack channels, phone numbers)
- `--escalate-after`: Escalation delay (e.g., "30m", "1h", "24h")
- `--escalate-to`: Escalation contacts/teams

**For integrations:**
- `--service`: External service (jira, stripe, salesforce, slack, twilio, etc.)
- `--action`: Integration action (create-issue, get-status, send-message, etc.)
- `--auth`: Authentication type (api-key, oauth, basic)
- `--webhook-url`: Webhook endpoint (if bidirectional)

**Validate:**
- Trigger type is recognized
- Actions exist and are sequentially logical
- Cron syntax is valid (if scheduling)
- Timezone is valid IANA format
- Recipients are non-empty and correctly formatted
- Services and actions are supported

**Output:** Structured request object with parsed parameters

---

## Step 2 — Spawn Workflow Automation Agent (PARALLEL: Steps 2, 3, 4 if multiple domains)

**If `--trigger` and `--action` provided:**

```
REQUEST:
Trigger: [trigger type]
Actions: [action list]
Workflow Name: [auto-generated if not provided]
Timeout: [timeout seconds]

RESPONSIBILITIES:
  1. Design n8n-style workflow definition
  2. Map trigger to initial node
  3. Create action nodes in sequence
  4. Add conditional branches where needed (e.g., route by lead score)
  5. Implement error handlers for critical paths
  6. Define retry policies (exponential backoff)
  7. Add timeout values (30s per API call, 5m total workflow)
  8. Log completion status to persistence
  9. Save workflow to persistence/workflows/[workflow-name].yaml
  10. Return workflow definition and deployment status

DELIVERABLES:
  - workflow_definition.yaml (complete n8n format)
  - deployment_status.json (success/failure, any errors)
  - workflow_url (if deployed to workflow engine)

CONSTRAINTS:
  - Use only agents defined in the-conductor
  - Don't invent service names or API endpoints
  - Include proper error handling (max 3 retries with backoff)
  - Ensure workflow completes within timeout
  - Log all actions to persistence layer
```

**Proceed to Step 3 in parallel if scheduling also requested; wait for completion before Step 5.**

---

## Step 3 — Spawn Scheduling Agent (IF `--cron` provided)

**For job scheduling:**

```
REQUEST:
Job ID: [job name]
Cron Expression: [validated cron]
Timezone: [validated timezone]
Workflow/Command: [to execute]

RESPONSIBILITIES:
  1. Validate cron expression (5-field format)
  2. Validate timezone (IANA database)
  3. Calculate next 5 execution times (show user)
  4. Add to persistence/schedules/recurring_tasks.yaml
  5. Configure monitoring (track duration, alert if missed, alert if slow)
  6. Set up maintenance window exclusions (if applicable)
  7. Create execution log database schema
  8. Return schedule definition and next run times

DELIVERABLES:
  - schedule_config.yaml (added to recurring_tasks.yaml)
  - next_runs.json (next 5 scheduled execution times)
  - monitoring_config.json (health check settings)

CONSTRAINTS:
  - Don't schedule during known maintenance windows
  - Ensure timezone offset accounts for daylight saving
  - Allow 10% buffer time for job completion
  - Log all scheduled runs to database
```

**Proceed to Step 4 in parallel if alerting also requested; wait for completion before Step 5.**

---

## Step 4 — Spawn Notification & Alert Agent (IF `--trigger` and `--channels` provided)

**For alert configuration:**

```
REQUEST:
Alert Trigger: [event to alert on]
Notification Channels: [email, slack, sms, webhook, pagerduty]
Recipients: [addresses/channels/numbers]
Escalation: [delay and escalation contacts]

RESPONSIBILITIES:
  1. Validate all channels are available (credentials, configurations exist)
  2. Validate recipients (email format, Slack channel exists, phone format)
  3. Design escalation policy (severity-based routing)
  4. Create alert templates for each channel
  5. Add deduplication logic (suppress duplicate alerts within 1 hour)
  6. Implement escalation timers
  7. Set up monitoring for alert delivery
  8. Add to persistence/alerts/escalation_policies.yaml
  9. Log alert configuration to persistence

DELIVERABLES:
  - escalation_policy.yaml (complete alert routing)
  - alert_templates.json (channel-specific message templates)
  - alert_config.json (dedup, escalation, recipients)

CONSTRAINTS:
  - Use existing credentials (env vars, API keys)
  - Don't send test alerts without explicit approval
  - Implement rate limiting (max alerts per hour per severity)
  - Ensure escalation doesn't create alert loops
  - Log all alerts to persistence layer
```

**Proceed to Step 5 after all parallel agents complete.**

---

## Step 5 — Spawn API Integration Agent (IF `--service` and `--action` provided)

**For external service integration:**

```
REQUEST:
Service: [jira, stripe, slack, salesforce, etc.]
Action: [create-issue, get-status, send-message, etc.]
Authentication: [api-key, oauth, basic, webhook]
Webhook URL: [if bidirectional]

RESPONSIBILITIES:
  1. Verify service credentials/API keys exist (in env vars)
  2. Generate API client code for the service
  3. Implement the requested action
  4. Add authentication (OAuth, API key, JWT, etc.)
  5. Handle pagination and rate limiting
  6. Implement data transformation if needed
  7. Add error handling and retry logic
  8. Test connectivity and authentication
  9. Create webhook receiver if applicable
  10. Save integration code to persistence/integrations/[service]_integration.py
  11. Log integration to persistence

DELIVERABLES:
  - api_client.py (service-specific client code)
  - integration_test_results.json (connectivity, auth, basic operation)
  - webhook_config.json (if applicable)

CONSTRAINTS:
  - Don't hardcode credentials
  - Use only documented API endpoints
  - Implement proper error handling
  - Support rate limiting
  - Log all API calls (success/failure)
```

---

## Step 6 — Test Configuration (IF `--test` provided)

**Validate automation end-to-end:**

```
TESTING STEPS:
  1. Validate workflow YAML syntax
  2. Check all referenced agents are available
  3. Verify all API integrations are reachable
  4. Test alert channels (send test message to Slack, test email, etc.)
  5. Verify database connections work
  6. Check all credentials are correctly configured
  7. Simulate workflow trigger and execution (dry-run mode)
  8. Verify persistence logging works
  9. Check escalation timers and notification routing

TEST REPORT:
  ✓ Workflow syntax valid
  ✓ All agents available
  ✓ API integrations reachable
  ✓ Alert channels functional
  ✓ Database connectivity OK
  ✓ Credentials configured
  ✗ [Any failures listed with remediation]

Output: test_results.json (detailed validation report)
```

---

## Step 7 — Deploy Automation (AFTER testing passes or on explicit `--deploy`)

**Make automation live:**

```
DEPLOYMENT STEPS:
  1. Move workflow YAML to production/workflows/
  2. Update cron daemon with new schedule (if applicable)
  3. Register alert policy in active escalation_policies.yaml
  4. Deploy API integration code
  5. Verify workflow is callable via webhook/event
  6. Set up monitoring and alerting on automation itself
  7. Log deployment event to persistence
  8. Return deployment summary

DEPLOYMENT VERIFICATION:
  - Workflow appears in automation dashboard
  - Schedule appears in cron list
  - Alert policy is active
  - Webhook endpoints are responding
  - Integration credentials are loaded
  - Monitoring is capturing execution metrics

OUTPUT:
  deployment_summary.json (what was deployed, status, next steps)
```

---

## Step 8 — Generate Summary Report

After all agents complete (or fail), generate comprehensive report:

```
AUTOMATION DEPLOYMENT REPORT
===============================

WORKFLOW
  Name: [workflow name]
  Trigger: [trigger type]
  Actions: [list of actions]
  Status: [deployed/failed/pending-approval]
  Execution Plan: [trigger] → [action 1] → [action 2] → ... → [completion]

SCHEDULE (if applicable)
  Job: [job name]
  Cron: [expression]
  Timezone: [timezone]
  Next Runs: [next 5 execution times]
  Status: [active/disabled/failed]

ALERTS (if applicable)
  Trigger: [event]
  Channels: [email, slack, etc.]
  Recipients: [list]
  Escalation: [policy]
  Status: [configured/testing/active]

INTEGRATIONS (if applicable)
  Service: [service name]
  Action: [action]
  Auth: [method]
  Status: [connected/failed/untested]

TESTING RESULTS
  Workflow tests: [PASS/FAIL]
  Integration tests: [PASS/FAIL]
  Alert tests: [PASS/FAIL]
  Overall: [READY FOR DEPLOYMENT / REQUIRES FIXES]

NEXT STEPS
  1. [Specific action required]
  2. [Specific action required]
  3. [Monitoring and maintenance schedule]

MONITORING & SUPPORT
  - Workflow execution logs: [dashboard URL]
  - Alert history: [dashboard URL]
  - Incident runbook: [wiki URL]
  - On-call contact: [contact info]

Deployed by: [your name]
Deployment date: [timestamp]
```

---

## Examples

### Example 1: New Lead Workflow

```
INPUT:
/automate:workflow \
  --trigger "new-lead" \
  --action "enrich,score,add-to-crm,notify-slack" \
  --workflow-name "new-lead-to-crm"

EXECUTION:
- Workflow Agent creates trigger → enrich → score → route (3 paths) → notify → complete
- Sets up conditional branching based on score
- Implements 3-retry backoff for enrichment
- 5-minute workflow timeout
- Logs all steps to persistence

OUTPUT:
- new-lead-to-crm.yaml deployed
- Ready to receive webhook events
- Slack notifications configured for sales team
```

### Example 2: Daily Security Report Schedule

```
INPUT:
/automate:schedule \
  --job "daily-security-report" \
  --cron "0 6 * * *" \
  --timezone "America/New_York" \
  --workflow "persistence/workflows/daily-report.yaml"

EXECUTION:
- Scheduling Agent validates cron and timezone
- Adds to recurring_tasks.yaml
- Calculates next 5 runs (accounting for EST/EDT)
- Sets up monitoring to alert if job doesn't run
- Creates execution log table

OUTPUT:
- Schedule active at 6 AM EST daily
- Next runs: [dates and times]
- Monitoring alerts if job misses window
```

### Example 3: Critical Finding Alert

```
INPUT:
/automate:alert \
  --trigger "finding.critical" \
  --channels "email,slack,sms" \
  --recipients "ciso@company.com,#security-incidents,+1-555-0123" \
  --escalate-after "5m"

EXECUTION:
- Alert Agent creates escalation policy
- Configures email (CISO), Slack (#security-incidents), SMS (CISO direct)
- Sets escalation timer (if unacknowledged after 5m, page on-call)
- Implements deduplication (max 1 per finding per hour)
- Creates alert templates for each channel

OUTPUT:
- Escalation policy added to active policies
- Test alert sent to validate channels
- Monitoring tracks alert delivery
```

---

## Anti-hallucination rules

- Never deploy automation without testing first (always use `--test` before `--deploy`)
- Never invent workflow actions — use only defined agents
- Never hardcode credentials — always use environment variables
- Never skip validation of cron expressions or timezones
- Never send unvetted test alerts to production channels
- Never create workflows with circular dependencies
- Never promise alert delivery without verifying channel configuration
- Never deploy to production without explicit `--deploy` flag
