---
name: dev-assist
description: "Triggered when analyzing code quality, CI/CD pipelines, code reviews, and development workflows. Use during engineering assessment phase of comprehensive audits."
---

# Development Assistance Skill

## When to use

- Code quality and architecture assessment during development audits
- CI/CD pipeline configuration and automation validation
- Code review process and quality gate analysis
- Technical documentation completeness and accuracy review
- Development team tooling and process efficiency evaluation

## Workflow

1. **Scope**: Determine development domain (code, CI/CD, docs, or process)
2. **Analysis**: Examine relevant artifacts (source code, workflow files, documentation, build logs)
3. **Pattern matching**: Identify architectural patterns, anti-patterns, and best practice violations
4. **Assessment**: Cross-reference findings against industry standards and framework guidelines
5. **Priority assignment**: Classify improvements using the-conductor severity scale
6. **Logging**: Submit findings to persistence layer with structured format

## Key patterns

### Code Quality (General)
```
- Single Responsibility Principle violations
- Cyclomatic complexity > 10 (flag as HIGH)
- Long method/function length (>50 lines)
- Duplicate code blocks across modules
- Missing type hints or inadequate documentation
```

### Code Review Process
```
- PR review SLA violations (flag findings >7 days old)
- Insufficient review criteria or checklists
- Lack of automated code quality gates
- Missing pre-commit hooks or linting
- Inadequate test coverage requirements
```

### CI/CD Pipeline Analysis
```
- Missing automated testing stages
- Long build/deploy times (>30 min without justification)
- Incomplete environment parity (dev vs. prod)
- Inadequate secret management in pipeline
- Missing rollback or deployment safety checks
- Insufficient logging and monitoring in automation
```

### Documentation Assessment
```
- API documentation missing or out-of-date
- README lacking setup and deployment instructions
- Architectural decision records (ADRs) absent
- Missing runbook documentation for operational tasks
- Inline code comments insufficient for complex logic
- Version history or changelog not maintained
```

## Output format

For each finding, log:

```python
log_finding(
    agent_name="dev-assist",
    team="development",
    severity="[CRITICAL|HIGH|MEDIUM|LOW|INFO]",
    category="[code-quality|code-review|ci-cd|documentation|process]",
    title="[Brief improvement title]",
    detail="[File path or workflow name] — [specific observation with context]",
    reference="[Industry standard: SOLID principles, 12-factor app, NIST guidelines]",
    remediation="[Specific improvement guidance with example or reference]",
)
```

### Example output

```
Finding: Missing pre-commit hooks for linting
File: .github/workflows/ci.yml
Observation: CI pipeline runs linting checks but developer machines lack local validation
Standard: Best Practice — Shift-left testing
Severity: MEDIUM
Remediation: Add husky and lint-staged to pre-commit workflow to catch issues before push
Reference: https://github.com/typicode/husky

---

Finding: Inadequate PR review SLA enforcement
Process: Code review workflow
Observation: 18 open PRs, 12 waiting >3 days for review
Standard: Code Review Best Practice
Severity: MEDIUM
Remediation: Define SLA targets (24h first review, 48h merge decision), enforce via automation
Reference: NIST SP 800-218 Section 3.3 (Code Review)
```

## False positive handling

Ignore or de-prioritize findings in:
- Legacy code marked for refactoring/deprecation
- Third-party dependencies or generated code
- Experimental branches or isolated feature development
- Code with explicit documentation explaining deviations

## Reference standards

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Code by Robert C. Martin](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [12 Factor App](https://12factor.net/)
- [NIST SP 800-218: Secure Software Development Framework](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [GitHub Workflow Best Practices](https://docs.github.com/en/actions/guides)
