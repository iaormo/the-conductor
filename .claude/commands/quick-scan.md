---
name: security-audit:quick-scan
description: >
  Fast security scan — Teams 2 (Software Security) and 3 (Infrastructure) only.
  Runs in parallel. Best for CI/CD integration and PR-level checks.
---

# Quick Security Scan

Runs software security and infrastructure teams in parallel for fast feedback.
Skips compliance and incident response teams.

## Usage

```
/security-audit:quick-scan --target ./src
/security-audit:quick-scan --severity HIGH
```
