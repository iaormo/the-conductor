---
name: sast-scanning
description: "Triggered when scanning source code for common injection, XSS, command injection, and credential patterns. Use when starting security analysis phase of audit."
---

# SAST Scanning Skill

## When to use

- Initial code security assessment in software security audits
- Rapid vulnerability pattern detection across large codebases
- Compliance scanning for OWASP Top 10 vulnerabilities
- Quick detection of hardcoded secrets before deeper review
- Team 2 (Software Security) audit initialization

## Workflow

1. **Scope**: Determine target language(s) and path(s) to scan
2. **Pattern matching**: Run curated grep patterns for each vulnerability class
3. **Filtering**: Remove false positives based on context (test files, comments, safe patterns)
4. **Mapping**: Cross-reference findings to CWE and OWASP Top 10
5. **Severity assignment**: Classify each finding using the-conductor severity scale
6. **Logging**: Submit findings to persistence layer with structured format

## Key patterns

### SQL Injection (CWE-89)
```bash
grep -r "execute\s*(\s*['\"].*\+" src/  # Python: string concatenation to execute()
grep -r "query\s*(\s*['\"].*\+" src/    # JavaScript: query() with concatenation
grep -r "Statement\|PreparedStatement" src/  # Java: check for parameterized queries
```

### Cross-Site Scripting (CWE-79)
```bash
grep -r "innerHTML\s*=" src/            # Direct DOM manipulation
grep -r "dangerouslySetInnerHTML" src/  # React unsafe HTML
grep -r "\$(.*)" src/                   # Unescaped template literals
grep -r "eval\s*(" src/                 # JavaScript eval() usage
```

### Command Injection (CWE-78)
```bash
grep -r "exec\|system\|shell\s*=" src/ # Shell execution functions
grep -r "spawn\|fork" src/              # Unsafe process spawning
grep -r "os\.system\|subprocess\.call" src/  # Python shell calls
```

### Hardcoded Secrets (CWE-798)
```bash
grep -r "password\s*[=:]" src/ --ignore-case  # Hardcoded passwords
grep -r "api[_-]?key\s*[=:]" src/ --ignore-case  # API keys
grep -r "secret\s*[=:]" src/ --ignore-case    # Secret values
grep -r "BEGIN PRIVATE KEY\|BEGIN RSA KEY" src/  # Embedded keys
```

### Weak Cryptography (CWE-327, CWE-326)
```bash
grep -r "MD5\|SHA1\|DES" src/           # Weak hash/cipher algorithms
grep -r "crypto\.randomBytes\(16\)" src/  # Weak random generation
grep -r "Math\.random\(" src/           # Unsafe randomness in security context
```

### Path Traversal (CWE-22)
```bash
grep -r "path\.join.*req\|os\.path\.join.*user" src/  # Unsafe path operations
grep -r "readFile\|readFileSync.*req" src/  # File read with user input
```

## Output format

For each finding, log:

```python
log_finding(
    agent_name="sast-scanner",
    team="software-security",
    severity="[CRITICAL|HIGH|MEDIUM|LOW]",
    category="[injection|xss|command-injection|credential-leak|weak-crypto|path-traversal]",
    title="[Brief vulnerability title]",
    detail="[File path]:[line-number] — [code snippet with context]",
    reference="CWE-[number], OWASP Top 10 A[X]",
    remediation="[Specific fix guidance with code example]",
)
```

### Example output

```
Finding: SQL Injection in login endpoint
File: src/auth/login.py:47
Code: cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
CWE: CWE-89
OWASP: A03:2021 – Injection
Severity: CRITICAL
Remediation: Use parameterized queries: cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
```

## False positive handling

Ignore matches in:
- Test files (test_*.py, *.test.js, __tests__/)
- Documentation and comments
- Configuration files (safe patterns like password validators)
- Dead code or disabled sections

## Reference standards

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/publications/detail/sp/800-218/final)
