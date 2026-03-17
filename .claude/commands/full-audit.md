# full-audit — Run complete 16-agent CISO security audit

Runs all 5 teams, applies two-stage Superpowers-style finding review
(scope compliance → quality), then synthesizes an executive report.

## Usage

```
/security-audit:full-audit --target ./src
/security-audit:full-audit --target . --severity CRITICAL HIGH
/security-audit:full-audit --target . --skip-ir
```

## Instructions

You are the CISO Orchestrator running a full security audit on `$ARGUMENTS`.

**FIRST: Invoke the `security-audit-discipline` skill.**
Announce: "Using security-audit-discipline skill — running scope check."

---

### Step 1 — Scope Definition

Parse `$ARGUMENTS` for `--target`, `--severity`, `--skip-ir`.

Read the target directory structure. Answer:
1. Target path confirmed
2. Languages/frameworks detected (check package.json, requirements.txt, go.mod, Dockerfile)
3. What IS and IS NOT in scope this run
4. Compliance context (payment data / health data / EU users?)
5. Mode: full-audit

---

### Step 2 — Spawn All Teams (ONE batched message, never sequential)

```
Task("Team 2 — Software Security | Target: [path] | Scope: [scope]
Agents to run IN PARALLEL: sast-engineer, dependency-auditor,
secure-code-reviewer, api-security-analyst.
Evidence rule: every finding requires a specific file path and line number.
Log via: python3 persistence/severity_logger.py
Output: team verification summary when complete.")

Task("Team 3 — Infrastructure | Target: [path] | Scope: [scope]
Agents IN PARALLEL: cloud-security-architect, network-security-engineer,
secrets-iam-auditor.
Evidence rule: every finding requires a specific file path and line number.
Log via: python3 persistence/severity_logger.py
Output: team verification summary when complete.")

Task("Team 4 — Compliance | Target: [path] | Context: [compliance]
Agents IN PARALLEL: compliance-analyst, privacy-officer, policy-enforcer.
Log via: python3 persistence/severity_logger.py
Output: gap summary table + team verification summary when complete.")

Task("Team 5 — Incident Response | Target: [path]
[Skip if --skip-ir was passed]
Agents IN PARALLEL: ir-lead, forensics-analyst, threat-hunter.
Log via: python3 persistence/severity_logger.py
Output: team verification summary when complete.")
```

---

### Step 3 — Two-Stage Finding Review

Invoke `finding-review` skill. Announce: "Running two-stage finding review."

**Stage 1 — Scope Compliance (all teams in parallel):**
```
Task("Stage 1 Scope Review — Team 2: verify file paths real, no invented CVEs, all logged")
Task("Stage 1 Scope Review — Team 3: verify file paths real, no invented CVEs, all logged")
Task("Stage 1 Scope Review — Team 4: verify gap table matches DB findings")
Task("Stage 1 Scope Review — Team 5: verify all artifacts read before findings logged")
```
FAIL on Stage 1 → return to team. Max 2 revision cycles then escalate to human.

**Stage 2 — Quality Review (CRITICAL + HIGH findings only):**
```
Task("Stage 2 Quality Review — all CRITICAL and HIGH findings:
Deep check exploitability, attack vector, remediation specificity.
Verdict per finding: PASS / NEEDS_REVISION / DOWNGRADE / REMOVE")
```
Apply verdicts to `persistence/audit.db` before synthesis.

---

### Step 4 — Invoke Audit Verification

Invoke `audit-verification` skill. Run Level 3 completion gate:
```bash
python3 persistence/dashboard.py --audit latest
```
Confirm all Level 3 checkboxes before proceeding.

---

### Step 5 — Executive Report

```
═══════════════════════════════════════════════════════
  the-conductor — EXECUTIVE AUDIT REPORT
  Target   : [system]
  Date     : [date UTC]
  Audit ID : [id]
  Overall Risk : CRITICAL | HIGH | MEDIUM | LOW
═══════════════════════════════════════════════════════

CRITICAL FINDINGS — IMMEDIATE ACTION REQUIRED
[title | team | file:line | reference | remediation]

HIGH FINDINGS — 24-HOUR SLA
[title | team | file:line | remediation]

MEDIUM FINDINGS — 7-DAY SLA
[count by category — detail in dashboard]

COMPLIANCE GAPS
[framework | control | status | gap description]

METRICS
Total findings        : [N]
False positives removed: [N]
Review cycles         : [N]
Risk score            : [X/100]
  (CRITICAL×25 + HIGH×10 + MEDIUM×3 + LOW×1, cap 100)

TOP 3 RECOMMENDED ACTIONS
1. [specific and actionable]
2. [specific and actionable]
3. [specific and actionable]

ESCALATE TO HUMAN (Ian): [all CRITICAL — never suppress]
═══════════════════════════════════════════════════════
```

---

### Step 6 — Export HTML

```bash
python3 persistence/dashboard.py --html --output audit_report_$(date +%Y%m%d).html
```

Report the HTML path to the user.
