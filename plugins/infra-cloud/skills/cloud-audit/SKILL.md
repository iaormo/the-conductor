---
name: cloud-audit
description: "Triggered when auditing cloud and infrastructure configurations: Terraform, CloudFormation, Kubernetes YAML, Docker configs, IAM policies, encryption settings. Use in Team 3 parallel scan or infrastructure assessment."
---

# Cloud Audit Skill

## When to use

- Initial infrastructure-as-code security review before deployment
- Cloud account configuration compliance check
- Post-incident infrastructure security verification
- Container image and registry security assessment
- Kubernetes cluster hardening review
- Team 3 (Infrastructure) audit parallel phase

## Workflow

1. **Discovery**: Locate all IaC files (Terraform, CloudFormation, K8s YAML, Dockerfiles)
2. **Parsing**: Load configs into structured format
3. **Policy check**: Test against security baselines and best practices
4. **Live validation**: Cross-reference with actual cloud environment if accessible
5. **Misconfiguration detection**: Identify overly permissive settings
6. **Encryption audit**: Verify encryption at rest and in transit
7. **Secret scan**: Check for hardcoded credentials
8. **IAM analysis**: Review roles and permission boundaries
9. **Logging**: Submit structured findings to persistence layer

## Key audit patterns

### Terraform Security Checks

```bash
# Check for public S3 buckets
grep -r "acl\s*=\s*['\"]public" *.tf

# Verify encryption enabled
grep -r "encrypted\s*=\s*false\|encryption_key_id\s*=" *.tf | grep -v "# " | grep -v "= true"

# Check for overly permissive security groups
grep -r "cidr_blocks\s*=\s*\[\"0\.0\.0\.0" *.tf

# Verify logging enabled on resources
grep -r "enable_logging\s*=\s*false\|logging\s*{\s*}" *.tf | grep -v "= true"

# Check IAM policies for wildcards
grep -r '"Action":\s*"\*"\|"Resource":\s*"\*"' *.tf | grep -c '"'

# Find hardcoded secrets in variables
grep -r "sensitive\s*=\s*false\|secret\|password\|api_key" *.tf | grep -v "sensitive = true"
```

### Kubernetes YAML Security

```bash
# Check for privileged pods
grep -r "privileged:\s*true" *.yaml

# Verify NetworkPolicies exist
if ! grep -r "kind:\s*NetworkPolicy" *.yaml > /dev/null; then
  echo "WARNING: No NetworkPolicies found"
fi

# Check RBAC bindings for overpermissive roles
grep -r "kind:\s*ClusterRoleBinding" *.yaml
grep -r "verbs:\s*\[\s*\"\*\"\s*\]" *.yaml  # Wildcard actions

# Verify resource limits
grep -r "resources:\s*{" *.yaml | grep -v "limits:\|requests:"

# Check for default ServiceAccount usage
grep -r "serviceAccountName" *.yaml | grep -v "specific-sa"

# Verify Pod Security Standards
grep -r "apiVersion:\s*v1beta1\|securityContext" *.yaml | head -5
```

### Docker Image Analysis

```bash
# Check base image age and vulnerabilities
docker inspect myapp:latest | grep -i "image\|created"

# Verify multi-stage builds (smaller attack surface)
grep -c "FROM.*as" Dockerfile

# Check for RUN as root
grep "^RUN\|^USER" Dockerfile | grep -v "USER [0-9]"

# Scan for hardcoded secrets
grep -r "ARG.*PASSWORD\|ARG.*API_KEY\|ARG.*SECRET" Dockerfile

# Check for layer vulnerabilities
docker history myapp:latest | awk '{print $2}' | while read image; do
  docker inspect "$image" | grep "RepoDigests"
done

# Verify image is scanned
docker image inspect myapp:latest | grep -i "Vulnerability\|Scan"
```

### AWS Configuration Audit

```bash
# List publicly accessible RDS instances
aws rds describe-db-instances \
  --query 'DBInstances[?PubliclyAccessible==`true`].DBInstanceIdentifier' \
  --output text

# Check for unencrypted EBS volumes
aws ec2 describe-volumes \
  --query 'Volumes[?Encrypted==`false`]' \
  --output json

# Verify bucket encryption
aws s3api get-bucket-encryption \
  --bucket my-bucket 2>&1 | grep -q "ServerSideEncryptionConfiguration" || \
  echo "CRITICAL: Bucket not encrypted"

# Check CloudTrail logging
aws cloudtrail describe-trails \
  --query 'trailList[?IsMultiRegionTrail==`false`]' \
  --output json

# Audit IAM user access keys age
aws iam list-access-keys --user-name USERNAME \
  --query 'AccessKeyMetadata[?CreateDate<`'$(date -d '90 days ago' -I)'`]'

# Check for overpermissive security groups
aws ec2 describe-security-groups \
  --query 'SecurityGroups[?IpPermissions[?FromPort==`0` && ToPort==`65535`]]'
```

### GCP Configuration Audit

```bash
# Check for public Cloud Storage buckets
gsutil ls -b -p $(gcloud config get-value project) | while read bucket; do
  gsutil iam get "$bucket" | grep "allUsers\|allAuthenticatedUsers"
done

# Verify VPC Flow Logs enabled
gcloud compute networks describe default --format="value(enable_flow_logs)"

# Check Firewall rules for overpermissiveness
gcloud compute firewall-rules list --format="table(name, allowed[].protocol, sourceRanges[])" | \
  grep "0.0.0.0/0"

# Verify KMS encryption on Compute instances
gcloud compute disks list --format="table(name, status, type)"
```

### Azure Configuration Audit

```bash
# Check for public blob storage
az storage blob list --account-name ACCOUNT \
  --container-name CONTAINER \
  --query "[?properties.publicAccess=='Blob'].name"

# Verify encryption on resources
az disk list --query "[?encryption.type!='EncryptionAtRestWithPlatformKey']"

# Check NSG rules for overpermissiveness
az network nsg rule list --resource-group RG \
  --nsg-name NSG \
  --query "[?sourceAddressPrefix=='*' && destinationPortRange=='*']"

# Verify Azure Key Vault soft delete
az keyvault show --name VAULT --query "properties.enableSoftDelete"
```

## Output format

For each finding, log:

```python
log_finding(
    agent_name="cloud-auditor",
    team="infrastructure",
    severity="[CRITICAL|HIGH|MEDIUM|LOW]",
    category="[misconfiguration|exposed-secrets|weak-encryption|overpermissive-iam|network-exposure]",
    title="[Brief infrastructure vulnerability title]",
    detail="File: [path]:[line] (or Resource: [cloud-resource])\nConfig: [snippet with issue highlighted]",
    reference="CWE-[number], [Cloud provider best practice]",
    remediation="[Specific fix with corrected config snippet]",
)
```

### Example output

```
Finding: S3 bucket is publicly accessible
Resource: prod-data-bucket (AWS S3)
Severity: CRITICAL
Issue: Bucket ACL allows public read/write access
AWS Reference: AWS best practice — Restrict S3 bucket access
Remediation:
  - Change ACL to private-read
  - Enable bucket versioning
  - Enable server-side encryption
```

## Reference standards

- [OWASP Infrastructure Security](https://cheatsheetseries.owasp.org/)
- [CIS Benchmarks](https://www.cisecurity.org/benchmarks/) (AWS, Azure, GCP, Kubernetes)
- [NIST Cloud Computing Security](https://csrc.nist.gov/publications/detail/sp/800-145/final)
- [Terraform Security Best Practices](https://www.terraform.io/cloud-docs/security)
- [Kubernetes Security Guidelines](https://kubernetes.io/docs/concepts/security/)
- [Container Security Standards](https://csrc.nist.gov/publications/detail/sp/800-190/final)
