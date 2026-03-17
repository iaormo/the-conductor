# Incident Response Security Plugin

**Purpose:** Security incident detection, triage, forensic analysis, and threat hunting.

## Overview

The Incident Response plugin provides automated and manual capabilities for incident investigation. It processes logs and alerts, performs timeline reconstruction, detects indicators of compromise (IOCs), analyzes attack patterns, and recommends containment strategies. It operates across network, system, and application logs to provide a complete incident picture.

## Capabilities

- **Incident triage**: Prioritize alerts, correlate events, assess impact
- **Log analysis**: Parse and analyze system, network, application, and security logs
- **Timeline reconstruction**: Build chronological narrative of attacker activity
- **IOC detection**: Identify malware hashes, IPs, domains, file paths across logs
- **Attack pattern analysis**: Link events to MITRE ATT&CK framework tactics/techniques
- **Lateral movement detection**: Find evidence of attackers moving between systems
- **Data exfiltration indicators**: Detect unusual network or data access patterns
- **Threat hunting**: Proactive search for compromise indicators
- **Containment recommendations**: Identify systems to isolate, credentials to reset, patches to apply

## How to Use

### Within the-conductor audit workflows

This plugin is invoked when:
- Running `/security-audit:full-audit` (Team 5, parallel with Forensics/Threat Hunt)
- Running `/incident-response:triage` (Team 5 only)
- Running custom incident investigations via `/incident:investigate`

### Manual invocation

```
/incident:investigate --type breach --time-range "2024-01-15 to 2024-01-17"
/incident:threat-hunt --ioc-file compromised_indicators.txt
/incident:analyze-logs --source siem --duration "last-24-hours"
```

## Directory Structure

- **agents/**: IR agents (Incident Lead, Forensics Analyst, Threat Hunter, Containment Specialist)
- **commands/**: CLI for incident investigation, log analysis, and threat hunting
- **skills/**: Reusable IR skills (ir-triage, forensics-analysis, threat-hunting)

## Integration Points

- Works in parallel with all other teams during full audit
- Feeds findings to `persistence/severity_logger.py`
- Coordinates with Security Scanning and Infrastructure teams for context
- Accesses logs from SIEM, EDR, WAF, and cloud platforms

## Requirements

- Access to SIEM (Splunk, ELK, Sumo Logic, etc.)
- EDR agent logs (CrowdStrike, Rapid7, etc.)
- System logs and event logs (Windows Event Log, syslog, auditd)
- Network logs (firewall, IDS/IPS, DNS, proxy)
- Application logs (web server, database, custom apps)
- Python 3.8+ for log analysis and correlation

## Output

Structured incident findings including:
- Timeline of events with precise timestamps
- IOC data (IPs, domains, hashes, file paths)
- MITRE ATT&CK framework mapping
- Affected systems and accounts
- Attack chain and progression
- Containment recommendations
- Impact assessment (data compromised, systems affected)
