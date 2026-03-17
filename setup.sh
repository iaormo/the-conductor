#!/usr/bin/env bash
set -e

echo ""
echo "═══════════════════════════════════════════"
echo "  the-conductor — Setup"
echo "═══════════════════════════════════════════"
echo ""

# ── 1. Copy agents ──────────────────────────────────────────────────────────
echo "▸ [1/6] Installing agents..."
mkdir -p ~/.claude/agents
cp -r .claude/agents/* ~/.claude/agents/ 2>/dev/null && \
  echo "  ✓ Agents installed to ~/.claude/agents/" || \
  echo "  ⚠ No agent files found yet in .claude/agents/"

# ── 2. Copy commands ────────────────────────────────────────────────────────
echo "▸ [2/6] Installing commands..."
mkdir -p ~/.claude/commands
cp -r .claude/commands/* ~/.claude/commands/ 2>/dev/null && \
  echo "  ✓ Commands installed" || \
  echo "  ⚠ No command files found"

# ── 3. Install Superpowers ──────────────────────────────────────────────────
echo "▸ [3/6] Installing Superpowers (process discipline layer)..."
if command -v claude &>/dev/null; then
  (claude plugin marketplace add obra/superpowers-marketplace 2>/dev/null && \
   claude plugin install superpowers@superpowers-marketplace 2>/dev/null && \
   echo "  ✓ Superpowers installed (obra/superpowers ⭐40.9k)") || \
  echo "  ⚠ Could not auto-install Superpowers. Add manually in Claude Code:
       /plugin marketplace add obra/superpowers-marketplace
       /plugin install superpowers@superpowers-marketplace"
else
  echo "  ⚠ Claude Code CLI not found. Install Superpowers manually in Claude Code:
       /plugin marketplace add obra/superpowers-marketplace
       /plugin install superpowers@superpowers-marketplace"
fi

# ── 4. Check ruflo ──────────────────────────────────────────────────────────
echo "▸ [4/6] Checking ruflo swarm runtime..."
if command -v ruflo &>/dev/null; then
  echo "  ✓ ruflo already installed"
else
  echo "  Installing ruflo globally..."
  npm install -g ruflo@latest && echo "  ✓ ruflo installed" || \
    echo "  ⚠ ruflo install failed — install manually: npm install -g ruflo@latest"
fi

if command -v claude &>/dev/null; then
  claude mcp add ruflo -- npx -y ruflo@latest mcp start 2>/dev/null && \
    echo "  ✓ ruflo MCP server registered" || \
    echo "  ⚠ MCP already registered or failed — add manually:
       claude mcp add ruflo -- npx -y ruflo@latest mcp start"
fi

# ── 5. Initialize persistence DB ────────────────────────────────────────────
echo "▸ [5/6] Initializing audit database..."
if command -v python3 &>/dev/null; then
  cd persistence && python3 init_db.py && cd .. && \
    echo "  ✓ Database initialized: persistence/audit.db"
else
  echo "  ⚠ python3 not found. Run: cd persistence && python3 init_db.py"
fi

# ── 6. Audit bundled skills ──────────────────────────────────────────────────
echo "▸ [6/6] Auditing bundled skills..."
if command -v python3 &>/dev/null; then
  python3 tools/skill_auditor.py --path plugins/ --recursive \
    --output skill_audit_report.json --quiet 2>/dev/null || true
  BLOCKS=$(python3 -c "import json; r=json.load(open('skill_audit_report.json')); print(r['summary']['block'])" 2>/dev/null || echo "0")
  WARNS=$(python3 -c "import json; r=json.load(open('skill_audit_report.json')); print(r['summary']['warn'])" 2>/dev/null || echo "0")
  if [ "$BLOCKS" -gt "0" ]; then
    echo "  ✗ $BLOCKS BLOCKED skill(s) — check skill_audit_report.json before using"
  elif [ "$WARNS" -gt "0" ]; then
    echo "  ⚠ $WARNS skill(s) need review — check skill_audit_report.json"
  else
    echo "  ✓ All bundled skills passed audit"
  fi
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  Setup complete."
echo ""
echo "  Layer stack:"
echo "    obra/superpowers  — process discipline (brainstorm→plan→TDD→review)"
echo "    the-conductor     — security domain (16 agents, audit commands)"
echo "    ruvnet/ruflo      — swarm runtime (parallel execution, memory)"
echo ""
echo "  Quick start:"
echo "    Open Claude Code in your project directory"
echo "    /security-audit:full-audit --target ."
echo ""
echo "  Dashboard:"
echo "    python3 persistence/dashboard.py"
echo "    python3 persistence/dashboard.py --html"
echo "═══════════════════════════════════════════"
echo ""
