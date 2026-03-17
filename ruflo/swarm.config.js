/**
 * the-conductor — ruflo swarm configuration
 * 40-agent, 7-division business operations topology
 *
 * Install ruflo: npm install -g ruflo@latest
 * Add MCP:       claude mcp add ruflo -- npx -y ruflo@latest mcp start
 * Init:          npx ruflo@latest init --config ruflo/swarm.config.js
 */

module.exports = {
  // -------------------------------------------------------------------------
  // Core topology
  // -------------------------------------------------------------------------
  topology: "hierarchical",   // Queen node (Master) + team workers
  maxAgents: 40,              // 7 divisions: security(16) + bizdev(4) + delivery(4) + dev(4) + data(4) + marketing(4) + automation(4)
  strategy: "specialized",    // Clear role separation — reduces drift
  antiDrift: true,            // Prevent agents going off-task
  consensusMode: "coordinator", // Master orchestrator makes final calls

  // -------------------------------------------------------------------------
  // Queen node — Master Orchestrator
  // -------------------------------------------------------------------------
  coordinator: {
    name: "master-orchestrator",
    agentFile: ".claude/agents/ciso-orchestrator.md",
    role: "queen",
    responsibilities: [
      "scope-definition",
      "division-assignment",
      "finding-synthesis",
      "report-generation",
      "escalation-decisions",
      "pipeline-coordination",
    ],
  },

  // -------------------------------------------------------------------------
  // Teams (worker pools)
  // -------------------------------------------------------------------------
  teams: [
    {
      id: "software-security",
      label: "Team 2 — Software Security",
      parallel: true,           // All 4 run simultaneously
      maxWorkers: 4,
      agents: [
        {
          name: "sast-engineer",
          agentFile: ".claude/agents/sast-engineer.md",
          tools: ["grep", "view", "bash"],
        },
        {
          name: "dependency-auditor",
          agentFile: ".claude/agents/dependency-auditor.md",
          tools: ["view", "bash"],
        },
        {
          name: "secure-code-reviewer",
          agentFile: ".claude/agents/secure-code-reviewer.md",
          tools: ["grep", "view"],
        },
        {
          name: "api-security-analyst",
          agentFile: ".claude/agents/api-security-analyst.md",
          tools: ["bash", "view"],
        },
      ],
    },
    {
      id: "infra-cloud",
      label: "Team 3 — Infrastructure",
      parallel: true,
      maxWorkers: 3,
      agents: [
        {
          name: "cloud-security-architect",
          agentFile: ".claude/agents/cloud-security-architect.md",
          tools: ["bash", "view"],
        },
        {
          name: "network-security-engineer",
          agentFile: ".claude/agents/network-security-engineer.md",
          tools: ["bash", "view"],
        },
        {
          name: "secrets-iam-auditor",
          agentFile: ".claude/agents/secrets-iam-auditor.md",
          tools: ["grep", "view", "bash"],
        },
      ],
    },
    {
      id: "compliance",
      label: "Team 4 — Compliance",
      parallel: true,
      maxWorkers: 3,
      agents: [
        {
          name: "compliance-analyst",
          agentFile: ".claude/agents/compliance-analyst.md",
          tools: ["view"],
        },
        {
          name: "privacy-officer",
          agentFile: ".claude/agents/privacy-officer.md",
          tools: ["view"],
        },
        {
          name: "policy-enforcer",
          agentFile: ".claude/agents/policy-enforcer.md",
          tools: ["grep", "view"],
        },
      ],
    },
    {
      id: "incident-response",
      label: "Team 5 — Incident Response",
      parallel: true,
      maxWorkers: 3,
      agents: [
        {
          name: "ir-lead",
          agentFile: ".claude/agents/ir-lead.md",
          tools: ["view", "bash"],
        },
        {
          name: "forensics-analyst",
          agentFile: ".claude/agents/forensics-analyst.md",
          tools: ["grep", "view", "bash"],
        },
        {
          name: "threat-hunter",
          agentFile: ".claude/agents/threat-hunter.md",
          tools: ["grep", "view", "bash"],
        },
      ],
    },
    {
      id: "business-development",
      label: "Division 2 — Business Development",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "prospecting-agent",
          agentFile: ".claude/agents/prospecting-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "lead-enrichment-agent",
          agentFile: ".claude/agents/lead-enrichment-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "outreach-sequencing-agent",
          agentFile: ".claude/agents/outreach-sequencing-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "crm-sync-agent",
          agentFile: ".claude/agents/crm-sync-agent.md",
          tools: ["bash", "view"],
        },
      ],
    },
    {
      id: "client-delivery",
      label: "Division 3 — Client Delivery",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "project-manager-agent",
          agentFile: ".claude/agents/project-manager-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "sow-generator-agent",
          agentFile: ".claude/agents/sow-generator-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "invoice-agent",
          agentFile: ".claude/agents/invoice-agent.md",
          tools: ["bash", "view"],
        },
        {
          name: "client-reporting-agent",
          agentFile: ".claude/agents/client-reporting-agent.md",
          tools: ["bash", "view"],
        },
      ],
    },
    {
      id: "development",
      label: "Division 4 — Development & Engineering",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "code-generation-agent",
          agentFile: ".claude/agents/code-generation-agent.md",
          tools: ["bash", "view", "write", "grep", "edit"],
        },
        {
          name: "code-review-agent",
          agentFile: ".claude/agents/code-review-agent.md",
          tools: ["bash", "view", "grep"],
        },
        {
          name: "cicd-pipeline-agent",
          agentFile: ".claude/agents/cicd-pipeline-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "documentation-agent",
          agentFile: ".claude/agents/documentation-agent.md",
          tools: ["view", "write", "grep", "bash"],
        },
      ],
    },
    {
      id: "data-analytics",
      label: "Division 5 — Data & Analytics",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "data-extraction-agent",
          agentFile: ".claude/agents/data-extraction-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "bi-dashboard-agent",
          agentFile: ".claude/agents/bi-dashboard-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "market-research-agent",
          agentFile: ".claude/agents/market-research-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "competitive-intel-agent",
          agentFile: ".claude/agents/competitive-intel-agent.md",
          tools: ["bash", "view", "write"],
        },
      ],
    },
    {
      id: "marketing",
      label: "Division 6 — Marketing & Content",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "content-writer-agent",
          agentFile: ".claude/agents/content-writer-agent.md",
          tools: ["view", "write", "bash"],
        },
        {
          name: "email-campaign-agent",
          agentFile: ".claude/agents/email-campaign-agent.md",
          tools: ["view", "write", "bash"],
        },
        {
          name: "social-media-agent",
          agentFile: ".claude/agents/social-media-agent.md",
          tools: ["view", "write", "bash"],
        },
        {
          name: "seo-analyst-agent",
          agentFile: ".claude/agents/seo-analyst-agent.md",
          tools: ["bash", "view", "write", "grep"],
        },
      ],
    },
    {
      id: "automation",
      label: "Division 7 — Automation & Integration",
      parallel: true,
      maxWorkers: 4,
      agents: [
        {
          name: "workflow-automation-agent",
          agentFile: ".claude/agents/workflow-automation-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "api-integration-agent",
          agentFile: ".claude/agents/api-integration-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "scheduling-agent",
          agentFile: ".claude/agents/scheduling-agent.md",
          tools: ["bash", "view", "write"],
        },
        {
          name: "notification-alert-agent",
          agentFile: ".claude/agents/notification-alert-agent.md",
          tools: ["bash", "view", "write"],
        },
      ],
    },
  ],

  // -------------------------------------------------------------------------
  // Memory & persistence
  // -------------------------------------------------------------------------
  memory: {
    backend: "sqlite",
    path: "./persistence/audit.db",
    // All agent findings route through the Python logger
    hooks: {
      onFinding: "python3 persistence/severity_logger.py --event finding",
      onTaskComplete: "python3 persistence/severity_logger.py --event task_complete",
      onAuditComplete: "python3 persistence/severity_logger.py --event audit_complete",
    },
  },

  // -------------------------------------------------------------------------
  // Execution defaults
  // -------------------------------------------------------------------------
  defaults: {
    timeout: 300,             // 5 min per agent task
    retries: 2,
    failOnError: false,       // Let other teams continue if one fails
    batchOperations: true,    // Always batch — never sequential spawning
  },

  // -------------------------------------------------------------------------
  // Workflows
  // -------------------------------------------------------------------------
  workflows: {
    "full-audit": {
      description: "Full 16-agent security audit across all teams",
      sequence: ["software-security", "infra-cloud", "compliance", "incident-response"],
      parallel: false,          // Teams run in sequence, agents within teams parallel
      synthesize: true,
    },
    "quick-scan": {
      description: "Fast scan — Teams 2 + 3 only (software + infra)",
      sequence: ["software-security", "infra-cloud"],
      parallel: true,           // Both teams run simultaneously
      synthesize: true,
    },
    "compliance-only": {
      description: "Compliance gap analysis — Team 4 only",
      sequence: ["compliance"],
      parallel: false,
      synthesize: false,
    },
    "ir-triage": {
      description: "Incident response triage — Team 5 only",
      sequence: ["incident-response"],
      parallel: false,
      synthesize: false,
    },
    "lead-gen": {
      description: "Full prospect-to-outreach lead generation pipeline",
      sequence: ["business-development"],
      parallel: false,
      synthesize: true,
    },
    "client-onboard": {
      description: "Client onboarding — SOW, project setup, billing",
      sequence: ["client-delivery"],
      parallel: false,
      synthesize: true,
    },
    "dev-assist": {
      description: "Development assistance — code gen, review, CI/CD, docs",
      sequence: ["development"],
      parallel: false,
      synthesize: true,
    },
    "data-research": {
      description: "Data extraction, BI dashboards, market research",
      sequence: ["data-analytics"],
      parallel: false,
      synthesize: true,
    },
    "marketing-campaign": {
      description: "Content, email campaigns, social media, SEO",
      sequence: ["marketing"],
      parallel: false,
      synthesize: true,
    },
    "automate": {
      description: "Workflow automation, API integration, scheduling, alerts",
      sequence: ["automation"],
      parallel: false,
      synthesize: true,
    },
    "full-service": {
      description: "All 7 divisions — complete business operations",
      sequence: ["software-security", "infra-cloud", "compliance", "incident-response", "business-development", "client-delivery", "development", "data-analytics", "marketing", "automation"],
      parallel: false,
      synthesize: true,
    },
  },
};
