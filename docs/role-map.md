# the-conductor — 16-Role Architecture Reference

## Overview

```
CISO Orchestrator (queen)
│
├── Team 1: Command
│   ├── Security Program Manager
│   └── Risk Officer
│
├── Team 2: Software Security (parallel)
│   ├── SAST Engineer
│   ├── Dependency Auditor
│   ├── Secure Code Reviewer
│   └── API Security Analyst
│
├── Team 3: Infrastructure (parallel)
│   ├── Cloud Security Architect
│   ├── Network Security Engineer
│   └── Secrets & IAM Auditor
│
├── Team 4: Compliance (parallel)
│   ├── Compliance Analyst
│   ├── Privacy Officer
│   └── Policy Enforcer
│
└── Team 5: Incident Response (parallel)
    ├── IR Lead
    ├── Forensics Analyst
    └── Threat Hunter
```

## Role reference

| # | Role | Team | Agent File | Status | Primary Frameworks |
|---|------|------|-----------|--------|-------------------|
| 1 | CISO Orchestrator | Command | `ciso-orchestrator.md` | Built | All |
| 2 | Security Program Manager | Command | `security-program-manager.md` | Built | NIST CSF |
| 3 | Risk Officer | Command | `risk-officer.md` | Built | ISO 27005 |
| 4 | SAST Engineer | Software | `sast-engineer.md` | Built | CWE, OWASP |
| 5 | Dependency Auditor | Software | `dependency-auditor.md` | Built | OWASP A06 |
| 6 | Secure Code Reviewer | Software | `secure-code-reviewer.md` | Built | OWASP Top 10 |
| 7 | API Security Analyst | Software | `api-security-analyst.md` | Built | OWASP API Top 10 |
| 8 | Cloud Security Architect | Infra | `cloud-security-architect.md` | Added | CIS Benchmarks, CSA |
| 9 | Network Security Engineer | Infra | `network-security-engineer.md` | Added | NIST, CIS |
| 10 | Secrets & IAM Auditor | Infra | `secrets-iam-auditor.md` | Added | CWE-798, OWASP |
| 11 | Compliance Analyst | Compliance | `compliance-analyst.md` | Added | OWASP, SOC2, ISO 27001 |
| 12 | Privacy Officer | Compliance | `privacy-officer.md` | Added | GDPR, CCPA |
| 13 | Policy Enforcer | Compliance | `policy-enforcer.md` | Added | OWASP, CWE |
| 14 | IR Lead | IR | `ir-lead.md` | Added | NIST SP 800-61 |
| 15 | Forensics Analyst | IR | `forensics-analyst.md` | Added | SANS FOR508 |
| 16 | Threat Hunter | IR | `threat-hunter.md` | Added | MITRE ATT&CK |

## Execution modes

| Command | Teams | Speed | Use case |
|---------|-------|-------|----------|
| `/security-audit:full-audit` | All 5 | Full | Quarterly audit, pre-certification |
| `/security-audit:quick-scan` | 2 + 3 | Fast | Pre-deploy gate, PR review |
| `/compliance:gap-analysis` | 4 only | Medium | Compliance readiness |
| `/incident-response:triage` | 5 only | Fast | Suspected incident |

## Finding flow

```
Agent detects finding
       ↓
persistence/severity_logger.py
       ↓
persistence/audit.db (SQLite)
       ↓
CISO Orchestrator synthesizes
       ↓
persistence/dashboard.py
       ↓
Terminal dashboard / HTML report
```

## Severity SLAs

| Severity | Human review required | Remediation SLA |
|----------|----------------------|-----------------|
| CRITICAL | Immediate escalation | Same session |
| HIGH | Yes — before session ends | 24 hours |
| MEDIUM | Yes — scheduled review | 7 days |
| LOW | Next audit cycle | 30 days |
| INFO | Optional | Next cycle |
