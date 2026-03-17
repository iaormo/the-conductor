# Setup Guide — the-conductor

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Python 3.10+
- Node.js 18+
- Git

## Step 1 — Clone

```bash
git clone https://github.com/YOUR_USERNAME/the-conductor.git
cd the-conductor
```

## Step 2 — Python persistence layer

```bash
cd persistence
python3 init_db.py
cd ..
```

## Step 3 — Install ruflo swarm runtime

```bash
npm install -g ruflo@latest
claude mcp add ruflo -- npx -y ruflo@latest mcp start
claude mcp list   # Verify ruflo appears
```

## Step 4 — Install agents into Claude Code

```bash
# Option A: Project-level agents (recommended — scoped to this repo)
# Agents in .claude/agents/ are picked up automatically by Claude Code

# Option B: User-level agents (available across all projects)
mkdir -p ~/.claude/agents
cp .claude/agents/*.md ~/.claude/agents/
```

## Step 5 — Audit any new skills before use

```bash
python3 tools/skill_auditor.py --path plugins/ --recursive
# Check: audit_report.json
# Only use PASS skills without review
```

## Step 6 — Run your first audit

```bash
# In Claude Code terminal:
claude

# Then run:
/security-audit:full-audit --target ./your-project
```

## Adding new skills from external repos

```bash
# 1. Download the skill file
curl -O https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/skills/owasp-security/SKILL.md

# 2. Audit it BEFORE importing
python3 tools/skill_auditor.py --file SKILL.md

# 3. If PASS, move to appropriate plugin
mv SKILL.md plugins/compliance/skills/owasp-security/

# 4. If WARN, review manually, add # WARN: comment, then import
# If BLOCK, do not import
```

## CI/CD integration

The `.github/skill-audit.yml` workflow automatically scans all SKILL.md
files on every PR that touches `plugins/` or `.claude/skills/`.

PRs with BLOCK findings will fail the check.
WARN findings will post a comment but not block the PR (adjust `--fail-on-warn` to change this).
