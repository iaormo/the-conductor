---
name: security-audit-discipline
description: >
  Use before running any security audit command or spawning any audit subagent.
  Enforces the-conductor's audit discipline: scope-first, evidence-required,
  no-hallucination, structured output. Activates automatically when any audit,
  scan, compliance, or incident response task begins. Superpowers equivalent
  of brainstorming + verification-before-completion for the security domain.
---

# Security Audit Discipline

You are operating as part of the-conductor CISO security audit system.
This skill enforces the discipline that separates real security work from security theater.

## The Iron Law

**No finding without evidence. No evidence without reading the file.**

Before logging ANY finding, you must have:
1. Read the specific file that contains the issue
2. Identified the exact line or configuration
3. Confirmed the issue is not a false positive (check context)
4. Referenced an authoritative source (OWASP, CWE, NIST, CVE)

Violating the letter of these rules = violating the spirit. There are no exceptions.
"I'm pretty sure" is not evidence. "It looks like" is not evidence. Read the file.

---

## Pre-Audit Scope Check

Before spawning any agent or running any scan:

```
1. WHAT is the target? (specific path, module, or entire repo)
2. WHAT frameworks/languages are present? (check package.json, requirements.txt, go.mod)
3. WHAT is in scope? (explicitly list what IS and IS NOT being audited this run)
4. WHAT compliance context applies? (payment data → PCI, health data → HIPAA, EU users → GDPR)
5. WHAT is the audit mode? (full-audit / quick-scan / compliance-only / ir-triage)
```

Do NOT spawn agents until all 5 are answered. This prevents agents wasting tokens
auditing irrelevant paths or missing the actual attack surface.

---

## Agent Spawning Discipline (Superpowers SDD adapted)

When spawning audit subagents, apply the two-stage review from
Superpowers `subagent-driven-development` — adapted for security:

**Stage 1 — Scope Compliance Review**
After each team completes, dispatch a scope-compliance subagent:
- Did the agent stay within the defined scope?
- Did every finding reference a real file path?
- Were any findings logged without reading the source?
- Did the agent invent any CVE numbers or remediation steps?

**Stage 2 — Finding Quality Review**
After scope review passes, dispatch a quality subagent:
- Is the severity classification correct? (not over- or under-stated)
- Is the remediation actionable and specific?
- Does the reference (CWE/OWASP) actually match the finding?
- Would a senior security engineer agree with this finding?

Both stages must pass before findings flow to the CISO Orchestrator for synthesis.

---

## The Rationalizations Table

Agents will try to skip discipline. Recognize and reject these:

| Rationalization | Reality | Response |
|----------------|---------|----------|
| "I can tell from the code pattern" | You haven't read the file | Read the file first |
| "This is a common vulnerability" | May not apply to this codebase | Confirm with evidence |
| "The severity is probably HIGH" | Severity requires context | Assess with full context |
| "I'll verify after logging" | Logging unverified = noise | Verify before logging |
| "The fix is obvious" | Obvious fixes are often wrong | Reference authoritative source |
| "I already know this CVE" | CVE may not match | Check CWE mapping first |
| "Let me add a few more findings" | Quantity ≠ quality | One verified > ten guessed |

---

## Completion Gate

Before declaring any audit phase complete, answer these:

- [ ] Every finding has a real file path (not a guess)
- [ ] Every finding has a severity with documented justification
- [ ] Every finding has a remediation linked to an authoritative source
- [ ] No CVE numbers were invented — "potential vulnerability" used where CVE unknown
- [ ] All findings are logged via `persistence/severity_logger.py` (not just prose)
- [ ] The scope-compliance review has been run
- [ ] The finding-quality review has been run

If any box is unchecked → the phase is NOT complete. Do not proceed.

---

## When Systematic Debugging Applies

If any audit tool, agent, or Python component produces unexpected output:
→ **DO NOT** guess at the fix
→ **DO** invoke Superpowers `systematic-debugging` skill immediately
→ Follow the 4-phase root cause process before touching any code

"It seems like it might be..." is not a diagnosis.
