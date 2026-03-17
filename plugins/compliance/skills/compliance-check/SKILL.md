---
name: compliance-check
description: "Triggered when performing compliance gap analysis against SOC 2, ISO 27001, PCI-DSS, HIPAA, or GDPR. Use during compliance audit phase or certification preparation."
---

# Compliance Check Skill

## When to use

- SOC 2 Type II audit preparation or annual renewal
- ISO 27001 certification readiness assessment
- PCI-DSS compliance validation for payment processing
- HIPAA audit for healthcare systems
- GDPR compliance verification for EU data subjects
- Team 4 (Compliance) audit phase
- Pre-certification gap analysis

## Workflow

1. **Scope**: Define target framework and systems in scope
2. **Control mapping**: Link system components to specific control requirements
3. **Evidence collection**: Gather documentation of control implementation
4. **Testing**: Verify controls are operating effectively
5. **Gap identification**: Document missing or partial controls
6. **Impact assessment**: Determine regulatory and business risk
7. **Remediation**: Define fix roadmap and implementation timeline
8. **Logging**: Submit compliance findings to persistence layer

## SOC 2 Control Categories

### Trust (CC — Common Criteria)

```bash
# CC1: Organization and Management
echo "Verify governance structure, roles, responsibilities"
grep -r "CISO\|Chief Information\|Security Officer" org_chart.pdf

# CC2: Communication and Information
echo "Check security policy distribution and acknowledgment"
ls -la /policies/information_security_policy.pdf

# CC3: Risk Assessment
echo "Review risk assessment documentation"
find /docs -name "*risk*assessment*.pdf" -o -name "*threat*model*.pdf"

# CC6: Logical Access Controls
echo "Verify user access controls and authentication"
grep -r "MFA\|Multi-factor\|2FA" /configs/auth/*.yaml
```

### Availability (A)

```bash
# A1: System Monitoring and Alerting
echo "Check monitoring tools and alerting thresholds"
grep -r "AlertManager\|DataDog\|NewRelic\|CloudWatch" /monitoring/

# A2: Capacity and Performance Planning
echo "Verify load testing and capacity planning"
find /docs -name "*capacity*plan*.pdf" -o -name "*load*test*.pdf"
```

### Processing Integrity (PI)

```bash
# PI1: Completeness and Accuracy
echo "Check data validation and audit trails"
grep -r "audit.*log\|validation.*schema" /src/

# PI2: Error Handling
echo "Verify error handling and retry logic"
grep -r "catch\|except\|error.*handler" /src/ | wc -l
```

### Confidentiality (C)

```bash
# C1: Data Classification
echo "Verify data is classified (public, internal, confidential, restricted)"
grep -r "data.*classification\|PII\|sensitive" /docs/

# C2: Encryption
echo "Check encryption of data at rest and in transit"
grep -r "encrypted\|TLS\|SSL" /configs/

# C3: Access Controls
echo "Verify least privilege implementation"
grep -r "role.*based\|RBAC\|permissions" /src/
```

### Confidentiality — User Privacy (P)

```bash
# P1: Privacy Policies and Procedures
echo "Check privacy notice and user consent"
find / -name "privacy_policy.pdf" -o -name "privacy_notice.pdf"

# P2: Data Collection and Processing
echo "Verify legitimate basis for processing"
grep -r "consent\|legitimate.*interest\|contract" /docs/

# P3: User Rights
echo "Verify mechanisms for data access/deletion requests"
grep -r "right.*to.*access\|right.*to.*forget\|DSAR\|SAR" /procedures/
```

## ISO 27001 Control Categories

### Information Security Policies (A.5)

```bash
# A.5.1: Management direction for information security
echo "Verify security policy exists and is approved"
find /docs -name "*information_security_policy*"

# Check policy covers required domains
for domain in "Classification" "Acceptable Use" "Access Control" "Incident Response" "Business Continuity"; do
  grep -q "$domain" /docs/information_security_policy.pdf && echo "✓ $domain" || echo "✗ $domain"
done
```

### Organization of Information Security (A.6)

```bash
# A.6.1: Internal Organization
echo "Verify CISO role, responsibilities, and reporting line"
grep -r "CISO\|Information Security Manager" /org/structure.pdf

# A.6.2: Mobile Devices and Teleworking
echo "Check policies for remote work and mobile device management"
find /policies -name "*remote*work*" -o -name "*mobile*device*" -o -name "*BYOD*"
```

### Asset Management (A.8)

```bash
# A.8.1: Responsibility for Assets
echo "Verify asset inventory and ownership"
ls -la /inventory/asset_register.csv

# A.8.2: Information Classification
echo "Check data classification labels"
grep -r "classification.*level\|data.*type" /configs/

# A.8.3: Media Handling
echo "Verify secure media disposal procedures"
find /procedures -name "*media*disposal*" -o -name "*destruction*"
```

### Access Control (A.9)

```bash
# A.9.1: User Access Management
echo "Verify user provisioning/deprovisioning procedures"
grep -r "onboarding\|offboarding\|access.*request" /procedures/

# A.9.2: User Responsibility
echo "Check acceptable use policy and training"
find /policies -name "*acceptable*use*"

# A.9.4: Access Control Implementation
echo "Verify least privilege and MFA"
grep -r "MFA\|sudo.*group\|role.*based" /configs/auth/
```

## PCI-DSS Requirements

```bash
# PCI-DSS 1: Firewall Configuration
echo "Verify firewall rules document exists"
grep -r "firewall.*rule\|inbound\|outbound" /docs/network_diagram.pdf

# PCI-DSS 2: Default Credentials
echo "Check for default passwords in configs"
grep -r "password.*default\|admin:admin" /configs/ | grep -v "=== REDACTED ==="

# PCI-DSS 3: Cardholder Data Protection
echo "Verify encryption of stored card data"
grep -r "encrypt\|tokenize\|vault" /docs/pci_compliance.pdf

# PCI-DSS 6: Secure Development
echo "Check SAST scanning and code review process"
ls -la /reports/sast_scan_*.pdf
ls -la /reports/code_review_*.pdf

# PCI-DSS 8: User Authentication
echo "Verify strong authentication and MFA"
grep -r "MFA\|2FA\|multi.*factor" /configs/

# PCI-DSS 10: Logging and Monitoring
echo "Verify audit logging is enabled"
grep -r "audit.*log\|CloudTrail\|syslog" /configs/logging/
```

## HIPAA Safeguards

```bash
# Administrative Safeguards
echo "Verify privacy and security officers designated"
grep -r "Privacy Officer\|Security Officer" /org/

echo "Check security awareness training"
find /training -name "*.pdf" | head -5

# Physical Safeguards
echo "Verify facility access controls"
find /docs -name "*facility*access*"

# Technical Safeguards
echo "Check encryption of ePHI"
grep -r "encrypted\|TLS.*1\.2\|AES" /configs/

echo "Verify audit controls"
grep -r "audit.*log\|PHI.*access" /logging/

# Breach Notification
echo "Check incident response plan for breach notification"
find /procedures -name "*breach*notification*"
```

## GDPR Compliance Checks

```bash
# Article 5: Data Processing Principles
echo "Verify lawful basis for processing"
grep -r "lawful.*basis\|consent\|contract\|legal.*obligation" /docs/

# Article 13/14: Privacy Notice
echo "Check privacy notices provided to data subjects"
find / -name "*privacy*notice*" -o -name "*data*subject*information*"

# Article 25: Data Protection by Design
echo "Verify DPbD implementation"
grep -r "data.*protection.*impact\|DPIA\|privacy.*assessment" /docs/

# Article 28: Data Processing Agreement
echo "Verify DPAs with processors"
ls -la /contracts/dpa_*.pdf

# Article 32: Security of Processing
echo "Check encryption, access controls, monitoring"
grep -r "encrypt\|access.*control\|monitoring\|audit.*log" /configs/

# Article 33: Breach Notification Procedures
echo "Verify 72-hour breach reporting procedure"
grep -r "breach.*72.*hour\|incident.*response.*plan" /procedures/
```

## Output format

For each control, log:

```python
log_finding(
    agent_name="compliance-auditor",
    team="compliance",
    severity="[CRITICAL|HIGH|MEDIUM|LOW]",
    category="[control-gap|partial-implementation|documentation-missing|insufficient-evidence]",
    title="[Framework] [Control ID]: [Brief description]",
    detail="Control: [Requirement text]\nStatus: [Met|Partial|Gap]\nGap: [What's missing]",
    reference="[SOC 2 CC1.2|ISO 27001 A.5.1|PCI-DSS 6|HIPAA 164.308]",
    remediation="[Implementation steps and timeline]",
)
```

### Example output

```
Finding: SOC 2 CC6.1 — User Access Control Gap
Control: Restrict system access to authorized personnel
Status: PARTIAL
Gap: MFA is implemented for AWS but not for internal applications
NIST Reference: IA-2 Multi-Factor Authentication
Severity: HIGH
Remediation:
  1. Deploy MFA for VPN access (2 weeks)
  2. Add MFA to internal identity provider (3 weeks)
  3. Update access control policy (1 week)
  Timeline: 6 weeks to full compliance
Evidence Required: MFA implementation screenshots, policy document, test results
```

## Reference standards

- [SOC 2 Trust Service Criteria](https://www.aicpa.org/interestareas/informationsystems/auditabilitytrust/aicpasoc2report.html)
- [ISO 27001:2022](https://www.iso.org/standard/27001)
- [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [GDPR Official Text](https://gdpr-info.eu/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
