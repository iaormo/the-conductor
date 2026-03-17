# Compliance Security Plugin

**Purpose:** Regulatory compliance gap analysis and control validation.

## Overview

The Compliance plugin audits systems against major regulatory frameworks: SOC 2, ISO 27001, PCI-DSS, HIPAA, GDPR, and OWASP standards. It maps findings to specific control requirements, identifies gaps, and provides remediation roadmaps aligned with regulatory expectations.

## Capabilities

- **SOC 2 Type II auditing**: Trust, Integrity, Availability, Confidentiality, and Privacy controls
- **ISO 27001 alignment**: Information security management system (ISMS) controls
- **PCI-DSS compliance**: Payment card industry data security standards
- **HIPAA compliance**: Protected health information (PHI) handling and safeguards
- **GDPR compliance**: Personal data processing and privacy controls
- **OWASP Top 10 mapping**: Link findings to regulatory implications
- **Evidence collection**: Documentation of control implementation status
- **Gap analysis**: Clear inventory of what's missing for certification
- **Remediation planning**: Roadmap to achieve compliance

## How to Use

### Within the-conductor audit workflows

This plugin is invoked when:
- Running `/security-audit:full-audit` (Team 4, parallel with Privacy/Policy)
- Running `/compliance:gap-analysis` (Team 4 only)
- Running framework-specific audits via `/scan:compliance`

### Manual invocation

```
/scan:compliance --framework soc2 --type2 true
/scan:compliance --framework iso27001
/scan:compliance --framework pci-dss
/scan:compliance --framework hipaa
/scan:compliance --framework gdpr
```

## Directory Structure

- **agents/**: Compliance agents (SOC 2 Auditor, ISO Auditor, PCI Auditor, Privacy Officer)
- **commands/**: CLI for compliance assessments and evidence collection
- **skills/**: Reusable compliance skills (compliance-check, gap-analysis, evidence-mapping)

## Integration Points

- Works in parallel with Privacy and Policy agents
- Feeds findings to `persistence/severity_logger.py`
- Coordinates with all teams to verify control implementation
- Generates compliance dashboard and remediation schedules

## Requirements

- Access to system documentation and control implementations
- Process flow diagrams and data classification matrices
- Personnel interviews for process validation
- Audit logs and monitoring dashboards
- Python 3.8+ for analysis and reporting

## Output

Structured compliance findings including:
- Specific control requirement reference
- Current implementation status (Met, Partial, Gap)
- Affected systems or processes
- Business impact and regulatory risk
- Remediation requirements and timeline
- Evidence requirements for certification
