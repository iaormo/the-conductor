---
name: agent-development
description: >
  Use when building a new security agent, plugin, skill, or Python component
  for the-conductor. Enforces the full Superpowers development workflow:
  brainstorm → plan → TDD implementation → review → finish branch.
  Activates when someone wants to add a new agent file, new plugin directory,
  new Python module in persistence/ or tools/, or new SKILL.md.
  DO NOT activate during audit mode — this is development mode only.
---

# Agent Development

You are building new tooling for the-conductor.
This skill enforces the full Superpowers development discipline for this context.

**Development mode is NOT audit mode.** If you are running a security audit,
this skill should not have activated. Check CLAUDE.md mode detection.

---

## The Mandatory Workflow

You MUST follow this sequence. Skipping steps is not allowed.

```
1. BRAINSTORM (Superpowers brainstorming skill)
   ↓
2. WRITE PLAN (Superpowers writing-plans skill)
   ↓
3. AUDIT NEW SKILLS (tools/skill_auditor.py before adding any SKILL.md)
   ↓
4. IMPLEMENT with TDD (Superpowers test-driven-development for Python)
   ↓
5. REVIEW (finding-review skill adapted for agent/skill review)
   ↓
6. FINISH BRANCH (Superpowers finishing-a-development-branch)
```

Do not start Step 3 before Step 2 is complete and approved.
Do not start Step 4 before Step 3 passes audit.
Do not skip to Step 4 because "it's just a markdown file." Markdown agents have
bugs too — they produce hallucinated findings, wrong severity, missed scope.

---

## Brainstorming Checklist for New Agents

When `brainstorming` activates for a new agent, answer these before designing:

```
1. What is this agent's SINGLE responsibility?
   (If you can't state it in one sentence, it's doing too much)

2. Which team does it belong to? (Command / Software / Infra / Compliance / IR)

3. What does it scan/check/analyze? (specific artifacts, not "security in general")

4. What are its output finding categories? (list the category values for severity_logger)

5. What external tools does it use? (grep, bash, view — no npx unless audited)

6. What would make this agent produce a false positive? (define safeguards)

7. What would make this agent miss a real finding? (define coverage tests)

8. How does it avoid hallucinating findings? (evidence requirements)
```

All 8 must be answered before writing the agent file.

---

## TDD for Python Components

For any new Python file in `persistence/` or `tools/`:

```
RED → Write the test first. Run it. Watch it fail.
GREEN → Write minimal code to make the test pass.
REFACTOR → Clean up. Re-run tests. All pass.
COMMIT → Only after all tests pass.
```

Delete any code written before the test. Start over with the test.
"I already know what it needs to do" is not an excuse to skip RED.
Every rationalization for skipping TDD is wrong. Write the test first.

Test file location: `tests/test_[component_name].py`

---

## Skill Audit Before Merging

Before any new SKILL.md enters the repo:

```bash
python3 tools/skill_auditor.py --file path/to/new/SKILL.md
```

- BLOCK result → do not merge. Fix the SKILL.md first.
- WARN result → get explicit approval before merging. Document decision.
- PASS result → proceed.

This applies to skills you write yourself. Even your own skills can contain
accidental npx references, external URLs, or dangerous patterns.

---

## The Agent Review (Stage 2 adapted for agent files)

After implementing a new agent file, dispatch a review subagent:

```
Task("Review new agent: [agent-name].md
Context: Agent is for the-conductor CISO system, Team [N].
Checklist:
[ ] Single clear responsibility (not trying to do too many things)
[ ] Description frontmatter accurately describes when it triggers
[ ] All bash commands use safe, known tools (grep, view, bash — not arbitrary npx)
[ ] No hardcoded paths (uses relative paths or env vars)
[ ] Evidence requirements are explicit (agent must read files before findings)
[ ] Severity guide is included and calibrated correctly
[ ] Output format matches severity_logger.py interface exactly
[ ] No hallucinated tool names, packages, or commands

Verdict: PASS / NEEDS_REVISION / BLOCK
For non-PASS: specific line or section that needs fixing.")
```

---

## Finishing a Development Branch

When a new agent or component is complete:
→ Invoke Superpowers `finishing-a-development-branch`

Before that, confirm:
- [ ] All tests pass (`python3 -m pytest tests/` if Python added)
- [ ] New agent has been reviewed (agent review above)
- [ ] New SKILL.md has passed `skill_auditor.py`
- [ ] `docs/role-map.md` is updated if a new agent was added
- [ ] `README.md` plugin list is updated if a new plugin was added
- [ ] `setup.sh` installs the new component if needed
