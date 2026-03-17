# Backend API Security Plugin

**Purpose:** Comprehensive security testing for REST and GraphQL APIs.

## Overview

The Backend API Security plugin audits API endpoints for authentication enforcement, authorization controls, rate limiting, input validation, CORS misconfiguration, and insecure response headers. It performs both static analysis (code review) and dynamic testing (live endpoint probing) to identify API-specific vulnerabilities.

## Capabilities

- **Authentication auditing**: Verify all endpoints enforce proper auth mechanisms
- **Authorization testing**: Check role-based access control (RBAC) and attribute-based access control (ABAC)
- **Input validation**: Detect missing or weak input sanitization
- **Rate limiting**: Verify DDoS and brute-force protections
- **CORS analysis**: Identify overly permissive cross-origin policies
- **Response header review**: Check for security headers (HSTS, CSP, X-Frame-Options, etc.)
- **GraphQL security**: Field-level authorization, depth limiting, query complexity analysis
- **API versioning**: Identify deprecated endpoints with weaker security

## How to Use

### Within the-conductor audit workflows

This plugin is invoked when:
- Running `/security-audit:full-audit` (Team 2, parallel with SAST/Dependencies)
- Running `/security-audit:quick-scan`
- Running custom API audits via `/scan:api`

### Manual invocation

```
/scan:api --url https://api.example.com/v1 --type rest
/scan:api --url https://api.example.com/graphql --type graphql
```

## Directory Structure

- **agents/**: API analyzer agents (auth, validation, headers, etc.)
- **commands/**: CLI for API endpoint discovery and testing
- **skills/**: Reusable API audit skills (api-audit, auth-testing, header-analysis)

## Integration Points

- Works in parallel with SAST and Dependency agents
- Feeds findings to `persistence/severity_logger.py`
- Coordinates with Infrastructure team for network/rate-limiting configs

## Requirements

- Network access to API endpoints (in test/staging environment)
- API documentation or OpenAPI/Swagger spec (if available)
- curl or Python requests library for endpoint testing
- Python 3.8+ for analysis

## Output

Structured findings include:
- Endpoint URL and HTTP method
- Authentication/authorization status
- Specific vulnerability details
- CWE/OWASP reference
- Remediation steps
- Severity classification
