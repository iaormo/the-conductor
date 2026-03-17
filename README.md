# the-conductor

> Multi-agent CISO security audit system — three-layer stack, discipline-enforced, production-ready.

---

## Three-Layer Stack

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1 — obra/superpowers  ⭐ 40.9k                       │
│  Process discipline: brainstorm → plan → TDD → review        │
│  Auto-activates: verification, systematic-debugging,         │
│  two-stage subagent review, receiving-code-review            │
├─────────────────────────────────────────────────────────────┤
│  Layer 2 — the-conductor  (this repo)                        │
│  Security domain: 16-role architecture, 5 teams,            │
│  audited skills, Python persistence, audit commands          │
├─────────────────────────────────────────────────────────────┤
│  Layer 3 — ruvnet/ruflo  ⭐ 21.3k                            │
│  Swarm runtime: hierarchical topology, parallel execution,   │
│  HNSW memory, self-learning routing, 175+ MCP tools          │
└─────────────────────────────────────────────────────────────┘
```

### Why three layers?

**Superpowers** enforces the discipline no one wants to write themselves — agents
don't jump to code, findings get two-stage reviewed, Python gets TDD, nothing
is declared "done" without verification. It auto-activates based on context.

**The-conductor** is the security domain knowledge — what to look for, how to
classify it, how to log it, how to synthesize it. The 16 agents, 5 teams,
severity framework, and Python persistence layer.

**Ruflo** is the swarm runtime — it handles parallel agent execution, shared
memory across sessions, WASM-accelerated routing, and the MCP server interface
that wires everything into Claude Code.

---

## Architecture

```
the-conductor/
├── CLAUDE.md                    # Master rules + Superpowers integration config
├── .claude/
│   ├── agents/                  # 16-role agent definitions
│   ├── commands/                # Audit slash commands (full-audit, quick-scan)
│   └── skills/                  # Conductor-specific Superpowers skill adaptations
│       ├── security-audit-discipline/  # Scope check + evidence enforcement
│       ├── audit-verification/         # Completion gate for findings
│       ├── finding-review/             # Two-stage review (scope → quality)
│       └── agent-development/          # Dev mode: full Superpowers workflow
├── plugins/                     # Domain plugin packs (audited, cherry-picked)
│   ├── security-scanning/
│   ├── backend-api-security/
│   ├── agent-orchestration/
│   ├── infra-cloud/
│   ├── compliance/
│   └── incident-response/
├── ruflo/
│   └── swarm.config.js          # 16-role topology, hooks to persistence layer
├── persistence/
│   ├── severity_logger.py       # Structured finding logger → SQLite
│   ├── dashboard.py             # Terminal + HTML report
│   └── audit.db                 # SQLite (gitignored — never commit)
└── tools/
    └── skill_auditor.py         # Scan SKILL.md files before importing
```

---

## The 16-Role Architecture

### Team 1 — Command
| Role | Agent File | Status |
|------|-----------|--------|
| CISO Orchestrator | `ciso-orchestrator.md` | ✅ Built |
| Security Program Manager | `security-program-manager.md` | ✅ Built |
| Risk Officer | `risk-officer.md` | ✅ Built |

### Team 2 — Software Security
| Role | Agent File | Status |
|------|-----------|--------|
| SAST Engineer | `sast-engineer.md` | ✅ Built |
| Dependency Auditor | `dependency-auditor.md` | ✅ Built |
| Secure Code Reviewer | `secure-code-reviewer.md` | ✅ Built |
| API Security Analyst | `api-security-analyst.md` | ✅ Built |

### Team 3 — Infrastructure
| Role | Agent File | Status |
|------|-----------|--------|
| Cloud Security Architect | `cloud-security-architect.md` | ✅ Added |
| Network Security Engineer | `network-security-engineer.md` | ✅ Added |
| Secrets & IAM Auditor | `secrets-iam-auditor.md` | ✅ Added |

### Team 4 — Compliance
| Role | Agent File | Status |
|------|-----------|--------|
| Compliance Analyst | `compliance-analyst.md` | ✅ Added |
| Privacy Officer | `privacy-officer.md` | ✅ Added |
| Policy Enforcer | `policy-enforcer.md` | ✅ Added |

### Team 5 — Incident Response
| Role | Agent File | Status |
|------|-----------|--------|
| IR Lead | `ir-lead.md` | ✅ Added |
| Forensics Analyst | `forensics-analyst.md` | ✅ Added |
| Threat Hunter | `threat-hunter.md` | ✅ Added |

---

## Quick Start

### 1. Clone and setup
```bash
git clone https://github.com/YOUR_USERNAME/the-conductor.git
cd the-conductor
bash setup.sh
```

`setup.sh` installs Superpowers, ruflo, initializes the DB, and audits bundled skills.

### 2. Install Superpowers manually (if setup.sh can't auto-install)
In Claude Code:
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### 3. Run an audit
```bash
# In Claude Code, in your target project directory:
/security-audit:full-audit --target .
/security-audit:quick-scan --target ./src
/compliance:gap-analysis
```

### 4. View results
```bash
python3 persistence/dashboard.py
python3 persistence/dashboard.py --html
```

---

## How Superpowers Integrates

### Audit mode (running scans)
These Superpowers skills auto-activate:
- `verification-before-completion` — agents can't declare findings "done" without evidence
- `systematic-debugging` — if any agent or tool produces wrong output
- `receiving-code-review` — when CISO Orchestrator reviews team output

These are suppressed (the-conductor's workflow replaces them):
- `brainstorming` — audit scope is already defined by the command
- `using-git-worktrees` — ruflo handles isolation

### Development mode (building new agents/skills)
Full Superpowers workflow enforced via `agent-development` skill:
- `brainstorming` before any new agent file
- `writing-plans` before implementation
- `test-driven-development` for all Python
- Two-stage review before merging

### The two-stage finding review (SDD adapted)
Every team's findings go through:
1. **Scope compliance review** — did agents stay in scope, cite real files, avoid invented CVEs?
2. **Quality review** — is severity correct, remediation specific, reference accurate?

Both stages must pass before findings reach the CISO Orchestrator.

---

## Skill Audit Policy

Every `SKILL.md` in this repo has been pre-scanned with `tools/skill_auditor.py`.

**Never import skills without auditing first.** This repo exists partly because
`wshobson/agents` shipped 47 LLM-generated skills in one commit (Oct 2025) with
no review, including hallucinated `npx react-codeshift` package names exploitable
via slopsquatting (Aikido Security, Jan 2026).

```bash
python3 tools/skill_auditor.py --file path/to/SKILL.md
# PASS → safe | WARN → human review | BLOCK → do not use
```

---

## Sources & Attribution

| Source | Stars | What we took |
|--------|-------|-------------|
| `obra/superpowers` | ⭐ 40.9k | Process discipline layer — installed as plugin |
| `wshobson/agents` | ⭐ 31.4k | Plugin architecture, security agent patterns (audited) |
| `sickn33/antigravity-awesome-skills` | ⭐ 22k | OWASP, STRIDE, DFIR skills (audited) |
| `ruvnet/ruflo` | ⭐ 21.3k | Swarm runtime and orchestration config |
| Anthropic official skills | — | Base SKILL.md format |

---

## License

MIT
