---
name: ir-triage
description: "Triggered when triaging security incidents: log analysis, IOC detection, timeline reconstruction, attack pattern identification. Use during incident response or post-incident forensic analysis."
---

# Incident Response Triage Skill

## When to use

- Active security incident investigation and response
- Post-incident forensic analysis and root cause analysis
- Suspicious alert investigation and impact assessment
- Threat hunting for known or suspected compromise
- Lateral movement detection across systems
- Data exfiltration investigation
- Team 5 (Incident Response) audit phase

## Workflow

1. **Alert triage**: Categorize and prioritize incoming security alerts
2. **Initial assessment**: Determine incident scope and potential impact
3. **Log collection**: Gather relevant logs from SIEM, endpoints, networks
4. **Timeline building**: Reconstruct chronological sequence of events
5. **IOC analysis**: Identify malicious IPs, domains, file hashes, processes
6. **Pattern matching**: Link events to MITRE ATT&CK framework
7. **Correlation**: Find relationships between disparate log events
8. **Containment**: Recommend immediate isolation and remediation steps
9. **Logging**: Submit incident findings to persistence layer

## Key investigation patterns

### Log Analysis and Parsing

```bash
# Extract authentication events from syslog
grep "authentication\|auth\|login\|sudo" /var/log/auth.log | \
  awk '{print $1, $2, $3, $NF}' | sort | uniq -c | sort -rn

# Find failed login attempts
grep "Failed password" /var/log/auth.log | \
  awk '{print $11}' | sort | uniq -c | sort -rn | head -10

# Extract Windows Event Log failed logons
wevtutil qe Security "/q:*[System[(EventID=4625)]]" /c:100 /rd:true

# Parse web server access logs for suspicious patterns
awk -F'"' '{print $2}' access.log | grep -i "union\|select\|drop\|delete\|exec\|script" | \
  awk '{print $2}' | sort | uniq -c | sort -rn
```

### IOC Detection

```bash
# Find known malicious IP addresses
grep -r "192.168.1.100\|10.0.0.50" /var/log/ /var/log/syslog /auth.log 2>/dev/null | \
  awk '{print $1, $NF}' | sort | uniq

# Search for suspicious domains in DNS logs
grep -i "malware\.domain\|c2\.server\|phishing\.site" /var/log/dns.log | \
  cut -d' ' -f2 | sort | uniq -c

# Hunt for malware file hashes
while read hash; do
  grep -r "$hash" /var/log /audit.log 2>/dev/null
done < suspected_hashes.txt

# Find suspicious process executions
grep -r "powershell.*-enc\|cmd.*\/c\|bash.*-i\|nc.*-l" /var/log/process.log | \
  awk '{print $1, $NF}'
```

### Timeline Reconstruction

```bash
# Build combined timeline from multiple sources
(
  grep "user action" /var/log/auth.log | awk '{print $1, $2, $3, "AUTH:", $0}' ;
  grep "error\|failed\|denied" /var/log/syslog | awk '{print $1, $2, $3, "SYSLOG:", $0}' ;
  grep "failed\|success" /var/log/apache2/error.log | awk '{print $1, $2, $3, "WEB:", $0}'
) | sort | uniq > /tmp/incident_timeline.txt

# Find suspicious sequence within time window
awk 'NR==FNR { prev=$0; next } {
  if ((NR - FNR) < 100 && $0 ~ /suspicious_pattern/) print prev; print $0
}' /tmp/incident_timeline.txt /tmp/incident_timeline.txt | head -20
```

### MITRE ATT&CK Mapping

```bash
# Map findings to MITRE ATT&CK framework
# Reconnaissance
grep -r "nslookup\|dig\|whois\|nmap" /var/log/command_history | \
  awk '{print "Reconnaissance -> " $0}'

# Initial Access
grep -r "phishing\|exploit\|vulnerability" /var/log/security.log | \
  awk '{print "Initial Access -> " $0}'

# Execution
grep -r "exec\|spawn\|fork\|system\|powershell\|bash\|cmd" /var/log/process.log | \
  awk '{print "Execution -> " $0}'

# Persistence
grep -r "cron\|at\|launchd\|registry\|startup" /var/log/system.log | \
  awk '{print "Persistence -> " $0}'

# Privilege Escalation
grep -r "sudo\|su\|privilege\|elevation" /var/log/auth.log | \
  awk '{print "Privilege Escalation -> " $0}'

# Defense Evasion
grep -r "process\|injection\|obfuscation\|signed" /var/log/security.log | \
  awk '{print "Defense Evasion -> " $0}'

# Discovery
grep -r "enumerate\|query\|whoami\|dir\|ls\|cat.*passwd" /var/log/command_history | \
  awk '{print "Discovery -> " $0}'

# Lateral Movement
grep -r "ssh\|scp\|psexec\|wmi\|rpc" /var/log/network.log | \
  awk '{print "Lateral Movement -> " $0}'

# Collection
grep -r "archive\|compression\|screenshot\|clipboard" /var/log/process.log | \
  awk '{print "Collection -> " $0}'

# Exfiltration
grep -r "http\|https\|ftp\|sftp\|dns" /var/log/network.log | grep -i "outbound\|egress" | \
  awk '{print "Exfiltration -> " $0}'
```

### Attack Chain Analysis

```bash
# Identify attack progression from logs
echo "=== ATTACK CHAIN RECONSTRUCTION ==="
echo ""

echo "Step 1: Initial Compromise"
grep "vulnerability\|exploit\|phishing" /var/log/security.log | head -1

echo "Step 2: Code Execution"
grep "powershell\|bash\|exec" /var/log/process.log | head -1

echo "Step 3: Persistence"
grep "cron\|registry\|startup" /var/log/system.log | head -1

echo "Step 4: Privilege Escalation"
grep "sudo\|privilege.*escalation" /var/log/auth.log | head -1

echo "Step 5: Discovery"
grep "enumerate\|query\|whoami" /var/log/command_history | head -1

echo "Step 6: Lateral Movement"
grep "ssh\|psexec\|wmi" /var/log/network.log | head -1

echo "Step 7: Data Exfiltration"
grep "outbound.*http\|egress.*ftp" /var/log/network.log | head -1
```

### Lateral Movement Detection

```bash
# Find unusual network connections from single source
netstat -an | grep ESTABLISHED | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | \
  awk '$1 > 10 {print "SUSPICIOUS: " $2 " has " $1 " outbound connections"}'

# Find connections to unusual ports
grep -r "22\|139\|445\|3389\|5985\|5986" /var/log/network.log | \
  grep -v "standard.*ssh\|standard.*rdp" | awk '{print "Unusual port: " $0}'

# Detect pass-the-hash or credential reuse
grep -r "authentication.*success" /var/log/auth.log | \
  awk '{print $NF}' | sort | uniq -c | sort -rn | \
  awk '$1 > 5 {print "Possible credential reuse: " $2 " used " $1 " times"}'
```

### Data Exfiltration Indicators

```bash
# Monitor large data transfers
netstat -an | grep ESTABLISHED | while read line; do
  remote_ip=$(echo $line | awk '{print $5}' | cut -d: -f1)
  bytes=$(ss -K | grep $remote_ip | awk '{sum += $NF} END {print sum}')
  if [[ $bytes -gt 1000000 ]]; then
    echo "Large transfer to $remote_ip: $bytes bytes"
  fi
done

# Check DNS exfiltration patterns
grep -r "unusually.*long\|domain.*length\|subdomain.*cascade" /var/log/dns.log | \
  awk '{print "DNS exfil indicator: " $0}'

# Find unusual database queries
grep -r "SELECT.*INTO\|EXPORT\|COPY\|BACKUP" /var/log/database.log | \
  awk '{print "Data export: " $0}'
```

## Output format

For each incident finding, log:

```python
log_finding(
    agent_name="incident-responder",
    team="incident-response",
    severity="[CRITICAL|HIGH|MEDIUM|LOW]",
    category="[initial-access|execution|persistence|privilege-escalation|discovery|lateral-movement|exfiltration|impact]",
    title="[Brief incident/TTp description]",
    detail="Timeline: [start time] -> [end time]\nIOCs: [IPs, domains, hashes, file paths]\nAffected: [systems/users]\nATT&CK: [Tactic:Technique]",
    reference="MITRE ATT&CK [T1234], CWE-[number]",
    remediation="[Immediate containment steps, credential resets, patches, IR contact info]",
)
```

### Example output

```
Finding: Suspected Data Exfiltration via Outbound HTTPS
Timeline: 2024-01-16 03:15 — 03:47 (32 minutes)
IOCs:
  Source IP: 10.1.2.50 (finance-db-server)
  Destination IP: 203.0.113.42 (C2 server — known malicious)
  Processes: sqlserver.exe, cmd.exe, powershell.exe
Affected Systems: finance-db-server, 2 workstations
MITRE ATT&CK: T1041 Exfiltration Over C2 Channel
Severity: CRITICAL
Containment Steps:
  1. Isolate finance-db-server immediately
  2. Block 203.0.113.42 at firewall
  3. Reset credentials for DB admin accounts
  4. Preserve logs for forensics
  5. Begin data breach assessment
IR Contact: incident-commander@company.com, (555) 123-4567
```

## Reference standards

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [NIST Incident Handling](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [CIS Incident Response Guide](https://www.cisecurity.org/cis-incident-response-guide/)
- [OWASP Incident Response](https://cheatsheetseries.owasp.org/cheatsheets/Incident_Response_Cheat_Sheet.html)
