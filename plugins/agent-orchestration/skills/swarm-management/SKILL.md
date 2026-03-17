---
name: swarm-management
description: "Triggered when spawning multi-agent workflows, monitoring team progress, handling agent failures, or synthesizing parallel results. Core skill for audit initialization and inter-team coordination."
---

# Swarm Management Skill

## When to use

- Initializing full audit with `/security-audit:full-audit`
- Spawning individual teams in parallel workflows
- Monitoring real-time progress across agents
- Handling agent failures or timeouts
- Synthesizing findings from parallel teams
- Load balancing work across available agents
- Resolving team conflicts or duplicate scanning

## Workflow

1. **Scope**: CISO Orchestrator defines audit boundaries and team assignments
2. **Spawn**: Launch all agents for a team in ONE batch message
3. **Monitor**: Poll agent progress and manage task queue
4. **Recover**: Retry failed tasks or escalate to human review
5. **Synthesize**: Merge parallel results into unified finding list
6. **Report**: Aggregate findings by severity and category

## Key orchestration patterns

### Team Spawning (CORRECT way)

```bash
# ✅ CORRECT: Batch all agents in one message
Teams 2 spawn:
  Task("sast-scanner: scan src/ --lang js,python")
  Task("dependency-auditor: check package.json and requirements.txt")
  Task("secure-code-reviewer: review auth module and api handlers")
  Task("api-analyst: audit /api/v1 endpoints --method rest")

# Run in parallel, DO NOT sequence
```

### Progress Monitoring

```bash
# Poll agent status
for agent in sast-scanner dependency-auditor code-reviewer api-analyst; do
  status=$(query_agent_status "$agent")
  if [[ "$status" == "running" ]]; then
    echo "$agent: in progress..."
  elif [[ "$status" == "failed" ]]; then
    echo "$agent: FAILED — initiating retry"
  elif [[ "$status" == "complete" ]]; then
    findings=$(get_agent_findings "$agent")
    log_findings "$findings"
  fi
done
```

### Failure Handling

```bash
# Retry policy: exponential backoff
RETRY_COUNT=0
MAX_RETRIES=3
BACKOFF=5

for attempt in {1..$MAX_RETRIES}; do
  if run_agent "$agent"; then
    break
  else
    sleep $((BACKOFF ** attempt))
    RETRY_COUNT=$((RETRY_COUNT + 1))
  fi
done

# If still failing, escalate
if [[ $RETRY_COUNT -eq $MAX_RETRIES ]]; then
  log_finding(
    severity="INFO",
    title="Agent timeout: $agent",
    detail="Agent did not complete after 3 retries. Manual review required.",
    remediation="Review agent logs at persistence/logs/$agent.log"
  )
fi
```

### Result Synthesis

```bash
# Merge findings from parallel agents
python3 << 'EOF'
import sqlite3

conn = sqlite3.connect('persistence/audit.db')
cursor = conn.cursor()

# Get all findings from current audit session
findings = cursor.execute('''
  SELECT severity, category, title, agent_name
  FROM findings
  WHERE session_id = ?
  ORDER BY severity DESC, category ASC
''', (session_id,)).fetchall()

# Group by severity for report
report = {}
for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
  report[severity] = [f for f in findings if f[0] == severity]

# Count findings
summary = {
  'critical': len(report['CRITICAL']),
  'high': len(report['HIGH']),
  'medium': len(report['MEDIUM']),
  'low': len(report['LOW']),
  'info': len(report['INFO']),
}

print(f"Audit Summary: {summary['critical']} CRITICAL, {summary['high']} HIGH, ...")
EOF
```

### Team Sequencing

```bash
# Teams run sequentially to avoid resource contention
# But agents WITHIN a team run in parallel

Team 2 (Software Security): 4 agents parallel
├── sast-scanner
├── dependency-auditor
├── code-reviewer
└── api-analyst
   [Wait for Team 2 to complete]

Team 3 (Infrastructure): 3 agents parallel
├── cloud-auditor
├── network-auditor
└── secrets-iam-reviewer
   [Wait for Team 3 to complete]

Team 4 (Compliance): 3 agents parallel
├── compliance-auditor
├── privacy-auditor
└── policy-reviewer
   [Wait for Team 4 to complete]

Team 5 (Incident Response): 3 agents parallel
├── ir-lead
├── forensics-analyst
└── threat-hunter
   [Wait for Team 5 to complete]

CISO Orchestrator: Synthesis & Report
```

### Anti-Drift (Scope Enforcement)

```bash
# Each agent validates its findings against defined scope
for finding in findings:
  if finding['path'] not in scope['target_paths']:
    log_drift(finding, "Outside defined audit scope")
    SKIP

  if finding['category'] not in scope['severity_classes']:
    log_drift(finding, "Category not in audit scope")
    SKIP

  else:
    ACCEPT_FINDING
```

## Output format

Agent spawn message:

```
[ORCHESTRATION] Spawning Team 2 (Software Security)
├── sast-scanner: Pattern-matching SAST on src/
├── dependency-auditor: Analyzing package.json, requirements.txt
├── code-reviewer: Manual review of auth and API modules
└── api-analyst: Testing /api/v1 endpoints
[Execution time estimate: 8-12 minutes]
[Running in parallel - wait for all to complete]
```

Progress tracking:

```
[PROGRESS] Team 2 Status
├── sast-scanner: ████████░░ 80% (found 3 HIGH, 7 MEDIUM)
├── dependency-auditor: ██████░░░░ 60% (found 1 CRITICAL)
├── code-reviewer: ███░░░░░░░ 30% (in review)
└── api-analyst: ░░░░░░░░░░ 0% (queued)
[Overall: 42% complete, 4 findings so far]
```

Synthesis output:

```
[SYNTHESIS] Team 2 Results
CRITICAL: 1 finding
├── SQL injection in login.py:47 (sast-scanner)

HIGH: 4 findings
├── Outdated lodash package (dependency-auditor)
├── Missing CSRF token on form (code-reviewer)
├── Weak password reset endpoint (api-analyst)
└── Unvalidated redirect in /auth/callback (sast-scanner)

MEDIUM: 9 findings
[...]

[Passing to Team 3]
```

## Configuration reference

```yaml
# swarm_config.yaml
topology: hierarchical
maxAgents: 16
strategy: specialized
antiDrift: true
coordinator: ciso-orchestrator

teams:
  team2:
    name: "Software Security"
    agents: [sast-scanner, dependency-auditor, code-reviewer, api-analyst]
    parallel: true
  team3:
    name: "Infrastructure"
    agents: [cloud-auditor, network-auditor, secrets-iam-reviewer]
    parallel: true
  team4:
    name: "Compliance"
    agents: [compliance-auditor, privacy-auditor, policy-reviewer]
    parallel: true
  team5:
    name: "Incident Response"
    agents: [ir-lead, forensics-analyst, threat-hunter]
    parallel: true

retryPolicy:
  maxRetries: 3
  backoffMs: 5000
  exponential: true

timeouts:
  agentMax: 1800  # 30 minutes per agent
  teamMax: 3600   # 60 minutes per team
  fullAudit: 7200 # 120 minutes total
```

## Reference standards

- [Ruflo Swarm Documentation](https://obra.sh/superpowers)
- [the-conductor CLAUDE.md](../../CLAUDE.md)
- [NIST SP 800-18 Guide for System Security Plans](https://csrc.nist.gov/publications/detail/sp/800-18/rev-1/final)
