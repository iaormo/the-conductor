# Security Scanning Plugin

**Purpose:** Static application security testing (SAST) and vulnerability pattern detection.

## Overview

The Security Scanning plugin provides automated source code analysis to identify common security vulnerabilities including injection flaws, XSS, command injection, hardcoded secrets, and weak cryptography. It uses grep-based pattern matching combined with semantic analysis to detect CWE-class vulnerabilities.

## Capabilities

- **SAST scanning**: Automated static code analysis across supported languages (Python, JavaScript/TypeScript, Java, Go, PHP)
- **Vulnerability pattern matching**: Detects common injection, XSS, command injection, and credential leak patterns
- **CWE mapping**: All findings reference specific CWE identifiers
- **OWASP alignment**: Findings categorized against OWASP Top 10

## How to Use

### Within the-conductor audit workflows

This plugin is automatically invoked when:
- Running `/security-audit:full-audit` (Teams 2)
- Running `/security-audit:quick-scan`
- Running custom SAST scans via `/scan:sast`

### Manual invocation

Trigger the `sast-scanning` skill to scan a codebase:

```
/scan:sast --path ./src --languages js,python
```

## Directory Structure

- **agents/**: SAST analyzer agents
- **commands/**: CLI entry points for scanning
- **skills/**: Reusable scanning skills (sast-scanning, pattern-matching)

## Integration Points

- Feeds findings to `persistence/severity_logger.py`
- Works with Code Review and Dependency Audit agents in parallel
- Severity levels follow the-conductor classification (CRITICAL, HIGH, MEDIUM, LOW, INFO)

## Requirements

- Bash/grep for pattern matching
- Access to source code repository
- Python 3.8+ for analysis engine

## Output

All findings are structured and logged with:
- Specific file path and line number
- CWE and OWASP Top 10 reference
- Remediation guidance
- Severity classification
