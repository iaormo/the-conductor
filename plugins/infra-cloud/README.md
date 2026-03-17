# Infrastructure & Cloud Security Plugin

**Purpose:** Security assessment of cloud configurations, infrastructure-as-code, containers, and network topology.

## Overview

The Infrastructure & Cloud plugin audits Terraform, CloudFormation, Kubernetes manifests, Docker configurations, and live cloud environment settings. It identifies misconfigurations, overly permissive access controls, unencrypted data paths, exposed secrets, and non-compliance with cloud provider security best practices.

## Capabilities

- **IaC scanning**: Terraform, CloudFormation, ARM templates, Pulumi
- **Kubernetes auditing**: RBAC policies, network policies, pod security, admission controllers
- **Container analysis**: Docker image vulnerabilities, insecure runtime settings, base image hardening
- **Cloud account auditing**: AWS, Azure, GCP configuration and permission review
- **Network segmentation**: Security group/NSG/firewall rule analysis
- **Encryption verification**: TLS/SSL, data-at-rest encryption, key management
- **Secret detection**: Hardcoded credentials in configs, API keys in image layers
- **IAM analysis**: Overly permissive roles, dormant accounts, privilege escalation risks

## How to Use

### Within the-conductor audit workflows

This plugin is invoked when:
- Running `/security-audit:full-audit` (Team 3, parallel with Network/Secrets)
- Running `/security-audit:quick-scan`
- Running infrastructure-specific audits via `/scan:cloud`

### Manual invocation

```
/scan:cloud --type terraform --path ./infrastructure/
/scan:cloud --type kubernetes --path ./k8s/
/scan:cloud --type docker --image myapp:latest
/scan:cloud --type aws --account prod
```

## Directory Structure

- **agents/**: Cloud security agents (Cloud IaC Auditor, K8s Security, Container Analyzer, IAM Reviewer)
- **commands/**: CLI for cloud environment scanning
- **skills/**: Reusable cloud audit skills (cloud-audit, k8s-security, docker-analysis)

## Integration Points

- Works in parallel with Network and Secrets/IAM agents
- Feeds findings to `persistence/severity_logger.py`
- Coordinates with Compliance team for regulatory controls
- Uses cloud provider APIs/CLIs for live environment checks

## Requirements

- Terraform/CloudFormation parsing libraries
- Kubernetes client library
- Docker CLI and image analysis tools
- Cloud provider CLIs (aws-cli, gcloud, az)
- Python 3.8+ for analysis engine
- Credentials to access cloud accounts (in secure vault)

## Output

Structured findings with:
- Specific configuration file and line number (for IaC)
- Resource name and account (for cloud environments)
- Security impact and exploitability
- CWE/OWASP reference
- Remediation code snippets
- Severity classification
