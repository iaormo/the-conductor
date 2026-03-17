---
name: api-audit
description: "Triggered when auditing REST or GraphQL API security: authentication, authorization, input validation, rate limiting, CORS, response headers. Use in Team 2 parallel scan or standalone API assessment."
---

# API Audit Skill

## When to use

- Initial API security assessment before deployment
- Compliance verification for API endpoints
- Post-incident API security review
- Regular security checkpoint for public/partner APIs
- Team 2 (Software Security) audit parallel phase

## Workflow

1. **Discovery**: Identify all API endpoints (from code, OpenAPI spec, or network crawl)
2. **Authentication check**: Test each endpoint for auth requirement and enforcement
3. **Authorization testing**: Verify access controls (RBAC, tenant isolation, field-level checks)
4. **Input validation**: Test for injection, XXE, large payloads, malformed data
5. **Rate limiting**: Verify DDoS and brute-force protections
6. **CORS analysis**: Check cross-origin policies for over-permissiveness
7. **Header inspection**: Verify security headers (HSTS, CSP, X-Frame-Options, etc.)
8. **GraphQL-specific**: Field authorization, depth limits, query complexity (if GraphQL)
9. **Logging**: Classify findings and submit to persistence layer

## Key test patterns

### Authentication Testing

```bash
# Test unauthenticated access
curl -X GET https://api.example.com/v1/users \
  -H "Accept: application/json" -i

# Test with invalid token
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer invalid_token" -i

# Check auth method in code
grep -r "Authorization\|@auth\|requireAuth" src/
```

### Authorization Testing (RBAC)

```bash
# Test cross-tenant access
curl -X GET https://api.example.com/v1/orgs/other-tenant/data \
  -H "Authorization: Bearer user-token" -i

# Test role escalation
curl -X POST https://api.example.com/v1/admin/settings \
  -H "Authorization: Bearer regular-user-token" -d '{}' -i

# Verify field-level authorization
grep -r "tenantId\|orgId\|userId" src/controllers/ | grep -v "==\|==="
```

### Input Validation

```bash
# SQL Injection test
curl -X GET "https://api.example.com/v1/search?q='; DROP TABLE users--" -i

# XXE test
curl -X POST https://api.example.com/v1/upload \
  -H "Content-Type: application/xml" \
  -d '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>' -i

# Large payload test
python3 -c "print('x' * 1000000)" | curl -X POST https://api.example.com/v1/data -d @- -i

# Check validation in code
grep -r "validate\|sanitize\|escap" src/handlers/ | grep -v "test"
```

### Rate Limiting

```bash
# Brute force simulation
for i in {1..100}; do
  curl -s -X POST https://api.example.com/v1/auth/login \
    -d '{"user":"admin","pass":"wrong"}' -w "HTTP %{http_code}\n"
done | sort | uniq -c

# Check rate-limit headers
curl -i https://api.example.com/v1/data | grep -i "X-RateLimit\|RateLimit"
```

### CORS Configuration

```bash
# Check CORS headers
curl -i -X OPTIONS https://api.example.com/v1/data \
  -H "Origin: https://attacker.com" \
  | grep -i "Access-Control-Allow"

# Check for wildcard CORS
curl -i -X GET https://api.example.com/v1/data \
  | grep "Access-Control-Allow-Origin: \*"
```

### Security Headers

```bash
# Check for critical headers
curl -i https://api.example.com/v1/data | grep -E \
  "Strict-Transport-Security|X-Content-Type-Options|X-Frame-Options|Content-Security-Policy"

# Expected headers
# Strict-Transport-Security: max-age=31536000; includeSubDomains
# X-Content-Type-Options: nosniff
# X-Frame-Options: DENY or SAMEORIGIN
# Content-Security-Policy: appropriate policy
```

### GraphQL-Specific Checks

```bash
# Query complexity test
curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ user { posts { comments { author { posts { ... } } } } } }"}'

# Field authorization check
grep -r "@authorize\|checkPermission" src/resolvers/ | grep -v "test"

# Introspection security
curl -X POST https://api.example.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

## Output format

For each finding, log:

```python
log_finding(
    agent_name="api-auditor",
    team="software-security",
    severity="[CRITICAL|HIGH|MEDIUM|LOW]",
    category="[authentication|authorization|input-validation|rate-limiting|cors|headers|graphql]",
    title="[Brief API vulnerability title]",
    detail="Endpoint: [METHOD] [PATH]\nIssue: [Specific problem description]",
    reference="CWE-[number], OWASP API Top 10 API[X]",
    remediation="[Specific fix with code example]",
)
```

### Example output

```
Finding: Missing authentication on user list endpoint
Endpoint: GET /api/v1/users
Severity: CRITICAL
Issue: Endpoint returns full user list without authentication
CWE: CWE-306 (Missing Authentication)
OWASP: API1:2023 – Broken Object Level Authorization
Remediation: Add @requireAuth middleware to route handler
```

## Reference standards

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [NIST API Security Guidelines](https://csrc.nist.gov/publications/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
