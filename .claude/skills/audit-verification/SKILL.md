---
name: audit-verification
description: >
  Use before any agent declares a finding verified, a remediation confirmed,
  or an audit phase complete. Conductor-specific adaptation of Superpowers
  verification-before-completion. Activates when agents claim something is
  "fixed", "resolved", "confirmed", "done", or "complete" in a security context.
  Also activates before CISO Orchestrator synthesizes final report.
---

# Audit Verification

Security findings are not "done" when you say they are.
They are done when evidence confirms they are.

This skill is the-conductor's adaptation of Superpowers `verification-before-completion`.
The same iron law applies: you do not get to declare completion without proof.

---

## The Three Verification Levels

### Level 1 — Finding Verification (before logging)
Before logging a finding to `persistence/severity_logger.py`:

```
✅ I have read the exact file and line that contains this issue
✅ I have confirmed this is not a false positive (checked context, comments, tests)
✅ I have confirmed the severity matches the actual exploitability
✅ I have a specific remediation from an authoritative source
✅ If I cite a CVE, I have confirmed it maps to this exact vulnerability class
```

All 5 must be true. If any is false → do not log. Investigate further.

### Level 2 — Remediation Verification (after fix claimed)
If an agent or human claims a finding has been remediated:

```
1. READ the specific change that was made
2. CONFIRM the change actually addresses the root cause (not just the symptom)
3. CHECK for regressions — did the fix introduce new issues?
4. TEST the fix if a test exists or can be written
5. UPDATE the finding status in persistence/audit.db to 'remediated'
   (do not just take the human's word for it)
```

### Level 3 — Phase Completion Verification (before CISO synthesis)
Before the CISO Orchestrator synthesizes findings into the executive report:

```bash
# Run this check — do NOT skip it
python3 persistence/dashboard.py --audit latest

# Confirm:
# - All teams have reported (no team has 0 findings AND 0 INFO items — that's suspicious)
# - No findings are in 'pending' state (all have been scope + quality reviewed)
# - CRITICAL count is correct (double-check each CRITICAL manually before report)
# - The audit_id matches the current session (not a stale previous audit)
```

---

## False Completion Signals

These feel like completion but are not:

| Signal | Why it's not done |
|--------|------------------|
| "I scanned the directory" | Scanning ≠ reading. Did you actually read flagged files? |
| "No issues found" | Verify you actually checked — absence of findings needs justification |
| "The team finished" | Did both review stages pass? Check the DB. |
| "It looks clean" | Evidence, not impressions |
| "I found 3 HIGH findings" | Are they all verified? Or are some guesses? |
| "Remediation applied" | Confirmed by reading the change, not by the dev saying so |

---

## The Verification Report

Before reporting to the CISO Orchestrator, each team lead produces:

```
TEAM VERIFICATION SUMMARY
==========================
Team: [name]
Agents run: [list]
Findings logged: [N]
  - CRITICAL: [N] — all evidence-verified: YES/NO
  - HIGH: [N] — all evidence-verified: YES/NO
  - MEDIUM: [N] — all evidence-verified: YES/NO
  - LOW/INFO: [N]
Scope-compliance review: PASS/FAIL
Finding-quality review: PASS/FAIL
False positives discarded: [N] (reason: [])
Ready for synthesis: YES/NO
```

If any field is NO → resolve before passing to CISO Orchestrator.

---

## Special Case: "No Findings" Verification

If a team reports zero findings in a non-trivial codebase, this is a red flag.
Before accepting a zero-finding report:

1. Ask the agent: "What specifically did you scan and what did you look for?"
2. Verify at least 3 specific checks were performed (not just "I looked around")
3. Log an INFO finding: "No issues found in [scope] — agent confirmed [specific checks]"
4. If you still can't explain WHY there are no findings, escalate to CISO Orchestrator
