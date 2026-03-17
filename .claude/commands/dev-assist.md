# dev-assist — Development and engineering assistance command

Unified development orchestration: code generation, code review, CI/CD pipeline setup,
and documentation generation. Routes tasks to the appropriate Division 4 agent,
executes in parallel when possible, and synthesizes results into actionable reports.

## Usage

```bash
# Code generation modes
/dev:assist --task "build REST API for user management" --lang python --framework fastapi
/dev:assist --task "generate database schema for e-commerce app" --lang sql --db postgres
/dev:assist --task "create authentication middleware" --lang typescript

# Code review modes
/dev:assist --task "review PR #42" --mode review
/dev:assist --task "review commit abc123" --mode review
/dev:assist --task "audit src/auth.py for security issues" --mode review

# CI/CD pipeline modes
/dev:assist --task "set up CI/CD" --mode pipeline --platform github
/dev:assist --task "set up CI/CD" --mode pipeline --platform gitlab --deploy kubernetes
/dev:assist --task "optimize pipeline for faster builds" --mode pipeline

# Documentation modes
/dev:assist --task "generate API docs" --mode docs --format openapi
/dev:assist --task "generate README and setup guide" --mode docs --target .
/dev:assist --task "create architecture documentation" --mode docs
/dev:assist --task "generate docstrings from code" --mode docs --language python
```

## Instructions

You are coordinating Division 4: Development & Engineering across 4 specialist agents.
Parse the task, validate arguments, dispatch to appropriate agent(s), and synthesize results.

---

### Step 1 — Parse and Validate Input

Extract from `$ARGUMENTS`:

- `--task` — Description of what to accomplish (required)
- `--mode` — Mode type: `generate`, `review`, `pipeline`, `docs` (required)
- `--lang` — Programming language: `python`, `typescript`, `javascript`, `go`, `rust` (for generate mode)
- `--framework` — Framework: `fastapi`, `express`, `gin`, etc. (for generate mode, optional)
- `--db` — Database: `postgres`, `mysql`, `sqlite` (for schema generation, optional)
- `--platform` — CI/CD platform: `github`, `gitlab`, `jenkins` (for pipeline mode, optional)
- `--deploy` — Deployment target: `docker`, `kubernetes`, `lambda`, `ec2` (for pipeline mode, optional)
- `--format` — Documentation format: `openapi`, `markdown`, `html` (for docs mode, optional)
- `--target` — Target directory or file path (for review and docs modes, optional)
- `--output` — Output directory for generated files (optional, defaults to current directory)

**Validation rules:**

```
✓ --task is non-empty
✓ --mode is one of: generate, review, pipeline, docs
✓ For --mode generate: --lang is provided
✓ For --mode review: --target is provided
✓ For --mode pipeline: --platform is provided or defaults to github
✓ For --mode docs: --target is provided or defaults to current directory
✓ All paths exist and are readable (for review and docs modes)
```

If validation fails, report the error and exit without spawning agents.

**Example validation:**

```
Validating arguments:
  ✓ task: "build REST API for user management"
  ✓ mode: generate
  ✓ lang: python
  ✓ framework: fastapi
  ✓ output: current directory

Proceeding to code-generation-agent...
```

---

### Step 2 — Dispatch to Appropriate Agent(s)

**Route by mode:**

#### Mode: `generate` → code-generation-agent

```
Task("Code Generation
Requirement: [task description]
Language: [lang]
Framework: [framework]
Target directory: [output]
Style matching enabled: true

Deliver:
  1. Generated source files (main code, models, config)
  2. Test files with coverage
  3. Supporting config files (.env.example, etc.)
  4. README section with usage examples
  5. File listing with paths and descriptions
")
```

#### Mode: `review` → code-review-agent

```
Task("Code Review
Target: [--target or current directory]
Languages detected: [auto-detect from files]

Responsibilities:
  1. Scan for code quality issues (naming, structure, complexity)
  2. Check error handling and edge cases
  3. Detect security anti-patterns
  4. Find dead code and unused imports
  5. Verify test coverage for critical paths
  6. Check consistency with existing code style
  7. Generate review report with file:line references

Deliver:
  1. Detailed review report with issues by severity
  2. Review comments with specific line numbers
  3. Consistency assessment
  4. Test coverage analysis
  5. Top 3 recommended improvements
")
```

#### Mode: `pipeline` → cicd-pipeline-agent

```
Task("CI/CD Pipeline Setup
Target: [target directory or current]
Platform: [github|gitlab|jenkins]
Deploy target: [optional: docker|kubernetes|lambda|ec2]

Responsibilities:
  1. Analyze project structure (languages, frameworks, tests)
  2. Generate CI/CD configuration files
  3. Configure test runners and linters
  4. Set up build and deployment steps
  5. Configure branch protection rules
  6. Set up monitoring and notifications
  7. Optimize pipeline for speed

Deliver:
  1. CI/CD configuration file(s)
  2. Test runner configuration
  3. Linter/formatter configuration
  4. Dockerfile (if deploying containers)
  5. Kubernetes manifests (if deploying K8s)
  6. Setup and optimization guide
")
```

#### Mode: `docs` → documentation-agent

```
Task("Documentation Generation
Target: [target directory]
Format: [openapi|markdown|html]
Languages: [auto-detect from files]

Responsibilities:
  1. Scan project for existing documentation
  2. Identify documentation gaps
  3. Extract API endpoints and schemas
  4. Generate or update README
  5. Generate API documentation
  6. Generate architecture docs
  7. Generate setup/deployment guides
  8. Generate docstrings for functions
  9. Create or update CHANGELOG

Deliver:
  1. Updated or new README.md
  2. API documentation (OpenAPI or Markdown)
  3. Architecture documentation
  4. Setup guides (DEVELOPMENT.md, DEPLOYMENT.md)
  5. Updated docstrings in code
  6. Changelog updates
  7. Documentation completeness report
")
```

---

### Step 3 — Execute Agents (Parallel When Possible)

**For single-mode tasks** (most common):

One agent runs independently. Wait for completion before proceeding.

**For multi-mode tasks** (if user requests multiple):

If user passes multiple modes in one command, dispatch all agents in parallel:

```
Task("Code Review — src/auth.py")
Task("Generate tests for auth module")
Task("Generate API docs for /auth endpoints")

Wait for all tasks to complete, then synthesize results in Step 4.
```

---

### Step 4 — Log Findings to Persistence Layer

After each agent completes, log results to persistence:

```python
# For code generation findings
log_finding(
    agent_name="code-generation-agent",
    team="development",
    severity="INFO",
    category="code-quality",
    title="Generated FastAPI user management API",
    detail="Created 8 new files: models.py, routes.py, database.py, schemas.py, tests/test_users.py, requirements.txt, .env.example, docker-compose.yml. Code follows project conventions. Test coverage 92%.",
    file_path="src/users/",
)

# For code review findings
log_finding(
    agent_name="code-review-agent",
    team="development",
    severity="HIGH",
    category="code-quality",
    title="Missing error handling in user creation endpoint",
    detail="POST /users endpoint does not catch database constraint violations. Email uniqueness conflicts will cause 500 error instead of 409 Conflict.",
    remediation="Add try/except block to catch IntegrityError and return 409 Conflict response.",
    file_path="src/routes/users.py",
    line_number=45,
)

# For CI/CD findings
log_finding(
    agent_name="cicd-pipeline-agent",
    team="development",
    severity="MEDIUM",
    category="infrastructure",
    title="Pipeline execution time can be optimized",
    detail="GitHub Actions workflow runs tests sequentially. Test matrix for Python 3.9-3.11 adds 15 minutes. Using parallel jobs and caching dependencies could reduce by 60%.",
    remediation="Enable dependency caching with actions/setup-python@v4 pip-cache. Use matrix strategy for parallel test execution.",
    file_path=".github/workflows/ci.yml",
    line_number=28,
)

# For documentation findings
log_finding(
    agent_name="documentation-agent",
    team="development",
    severity="MEDIUM",
    category="code-quality",
    title="API documentation missing endpoint specifications",
    detail="README.md has no API documentation section. /users, /posts, /comments endpoints are undocumented. No OpenAPI spec exists.",
    remediation="Generate OpenAPI specification and API.md documentation covering all 12 endpoints with request/response examples.",
    file_path="README.md",
)
```

---

### Step 5 — Synthesize Results and Generate Summary

Generate comprehensive summary report:

```
═══════════════════════════════════════════════════════════════════
  the-conductor — DEVELOPMENT ASSISTANCE REPORT
  Task      : [task]
  Mode      : [mode]
  Date      : [date UTC]
  Status    : [COMPLETED | COMPLETED_WITH_WARNINGS | FAILED]
═══════════════════════════════════════════════════════════════════

EXECUTION SUMMARY
─────────────────────────────────────────────────────────────────
Agent dispatched: [agent-name]
Execution time: [duration]
Status: [COMPLETED | FAILED]

[For mode: generate]
CODE GENERATION RESULTS
─────────────────────────────────────────────────────────────────
Files generated: [N]
  • src/models.py (127 lines)
  • src/routes.py (89 lines)
  • src/database.py (45 lines)
  • tests/test_api.py (156 lines)
  • requirements.txt (12 packages)
  • docker-compose.yml
  • .env.example

Code quality metrics:
  ✓ Follows project conventions
  ✓ All functions documented
  ✓ Error handling implemented
  ✓ Tests written for critical paths

Next steps:
  1. Review generated files
  2. Integrate into project
  3. Run pytest to verify tests pass
  4. Commit to feature branch

Generated files location: [path]

[For mode: review]
CODE REVIEW RESULTS
─────────────────────────────────────────────────────────────────
Files reviewed: [N]
Total issues found: [N]

CRITICAL ISSUES — Must fix before merge
  [issue | file:line | remediation]

HIGH SEVERITY ISSUES — Should fix
  [issue | file:line | remediation]

MEDIUM SEVERITY ISSUES — Nice to improve
  [issue | file:line | remediation]

Code quality score: [A|B|C|D]
Test coverage: [%]
Style consistency: [Matches | Minor gaps | Significant gaps]

Verdict: [APPROVE | REQUEST CHANGES | BLOCK]

[For mode: pipeline]
CI/CD PIPELINE SETUP RESULTS
─────────────────────────────────────────────────────────────────
Platform: [github|gitlab|jenkins]
Deployment target: [docker|kubernetes|none]

Configuration files created:
  • .github/workflows/ci.yml
  • Dockerfile
  • k8s/deployment.yaml (if K8s)

Pipeline stages:
  1. Lint (2 min)
  2. Test (8 min)
  3. Build (5 min)
  4. Deploy (3 min)
  Total: ~18 minutes

Branch protection configured:
  ✓ Require status checks: test, build
  ✓ Require code review: 1 approver
  ✓ Require passing tests

Next steps:
  1. Commit pipeline configuration
  2. Push to repository
  3. GitHub will run first pipeline
  4. Monitor for errors

[For mode: docs]
DOCUMENTATION GENERATION RESULTS
─────────────────────────────────────────────────────────────────
Documentation files:
  • README.md (updated)
  • docs/API.md (generated)
  • docs/ARCHITECTURE.md (generated)
  • docs/DEVELOPMENT.md (generated)
  • docs/DEPLOYMENT.md (generated)

Coverage:
  ✓ API endpoints: 12/12 documented
  ✓ Architecture: Documented
  ✓ Setup guide: Complete
  ✓ Docstrings: 95% coverage (42/44 functions)

Missing (for manual addition):
  • Example use cases (2 endpoints)
  • Troubleshooting section
  • Performance tuning guide

Next steps:
  1. Review generated documentation
  2. Add missing sections manually
  3. Commit documentation
  4. Host on GitHub Pages (optional)

METRICS & QUALITY
─────────────────────────────────────────────────────────────────
Findings logged: [N]
Critical issues: [N]
High issues: [N]
Medium issues: [N]
Action items: [N]

ESCALATE TO HUMAN (Ian): [if any CRITICAL issues]

═══════════════════════════════════════════════════════════════════
```

---

### Step 6 — Export Artifacts

Save all generated files and reports:

```bash
# Code generation: files already written to --output directory
ls -la [output_directory]/

# Code review: export report
cat > [output_directory]/code_review_report.txt << 'EOF'
[full review report]
EOF

# CI/CD: files already written to project root and .github/
cat > [output_directory]/pipeline_setup_guide.txt << 'EOF'
[setup and optimization guide]
EOF

# Docs: files already written to docs/ and root
cat > [output_directory]/docs_completeness_report.txt << 'EOF'
[documentation audit and gaps]
EOF
```

Report paths to user.

---

### Anti-Hallucination Rules

For this command:

1. **Never invent requirements** — Only generate code for specified requirements
2. **Never skip validation** — Fail early if arguments are invalid
3. **Never run multiple modes in wrong order** — Always: review → generate → pipeline → docs
4. **Never skip persistence logging** — Always log findings to persistence layer
5. **Never invent file paths** — Only reference files that actually exist
6. **Never promise unimplemented features** — Be clear about what was/wasn't completed
7. **Never suppress critical issues** — Always escalate CRITICAL findings to user
8. **Always reference specific code locations** — file:line for every issue
