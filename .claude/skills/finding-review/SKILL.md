---
name: finding-review
description: >
  Use to review security findings produced by audit agents before they reach
  the CISO Orchestrator. Conductor-specific implementation of Superpowers
  two-stage subagent review (spec compliance → code quality). Activates when
  a team has completed its scan and findings need quality gate before synthesis.
  Also activates when the CISO Orchestrator is reviewing team output.
---

# Finding Review

This is the-conductor's implementation of the Superpowers two-stage review
(`subagent-driven-development`) adapted for security findings instead of code.

Every batch of findings goes through two review stages before reaching the
CISO Orchestrator. This is not optional. Low-quality findings waste human
remediation time and erode trust in the audit system.

---

## Stage 1 — Scope Compliance Review

**Question: Did the agent stay within scope and follow the rules?**

For each finding, check:

```
[ ] File path is real (not hallucinated — verify it exists in the target)
[ ] Finding is within the defined audit scope (not a tangential observation)
[ ] No CVE numbers invented — unknown CVEs use "potential [type] vulnerability"
[ ] No remediation steps invented — all reference OWASP/CWE/NIST/vendor docs
[ ] Severity justification is present (not just "this looks HIGH")
[ ] Finding is logged to persistence layer (not just written as prose)
```

**Stage 1 verdicts:**
- `PASS` → proceed to Stage 2
- `FAIL` → return to agent with specific failures listed. Re-scan required.
- `PARTIAL` → acceptable if fewer than 20% of findings have minor issues.
  Document which findings need correction and proceed with the rest.

---

## Stage 2 — Finding Quality Review

**Question: Would a senior security engineer agree with these findings?**

For each CRITICAL and HIGH finding specifically:

```
[ ] Exploitability is correctly assessed (not theoretical if marked CRITICAL)
[ ] Attack vector is described (network/local/physical — not assumed)
[ ] Impact is described (data exposure/system compromise/denial of service)
[ ] Remediation is specific enough to act on (not "improve security")
[ ] Reference actually maps to this vulnerability type (CWE-89 = SQLi, not XSS)
[ ] Finding is not a duplicate of another finding from a different agent
```

For MEDIUM and LOW findings:

```
[ ] Not being used to pad the finding count (INFO is more honest for observations)
[ ] Actionable remediation exists
[ ] Not a false positive (checked 2+ signals before logging)
```

**Stage 2 verdicts:**
- `PASS` → findings cleared for CISO synthesis
- `NEEDS_REVISION` → specific findings flagged. Agent revises those only.
- `DOWNGRADE` → severity was overstated. Downgrade with justification noted.
- `REMOVE` → finding is a false positive or duplicate. Remove from DB.

---

## Dispatching Review Subagents

The CISO Orchestrator dispatches review subagents with precisely crafted context.
**Never pass your session history to the reviewer.** Pass only:

```
Task("Stage 1 Scope Review — Team: [name]
Context:
- Target: [path]
- Scope: [what was in scope]
- Compliance context: [frameworks]

Findings to review: [list of finding IDs from audit.db]
Checklist: [paste Stage 1 checklist above]

Report verdict per finding: PASS / FAIL / PARTIAL
For FAIL: state exactly which checklist item failed and why.")
```

Then Stage 2:

```
Task("Stage 2 Quality Review — Team: [name]
Stage 1 result: PASS
CRITICAL/HIGH findings to review deeply: [IDs]
All findings to review: [IDs]

Checklist: [paste Stage 2 checklist above]

Report verdict per finding: PASS / NEEDS_REVISION / DOWNGRADE / REMOVE
For each non-PASS: specific reason and recommended action.")
```

---

## Handling Reviewer Disagreement

If a reviewer disagrees with an agent's finding and the agent pushes back:

1. CISO Orchestrator arbitrates — not the agent, not the reviewer
2. If both have valid technical arguments, keep the finding at the lower severity
3. If the reviewer identifies a false positive but agent is unsure → mark as `INFO` with note
4. Escalate to human (Ian) if CRITICAL finding is disputed by Stage 2 reviewer

**Principle:** In security, it is better to miss a finding than to report a false one.
False positives destroy the audit's credibility and waste remediation resources.

---

## Review Turnaround

- Stage 1 review: run immediately after each team completes
- Stage 2 review: run after Stage 1 passes, before CISO synthesis
- Maximum 2 revision cycles per team before escalating to human
- If a team fails Stage 1 twice on the same findings → human review required
