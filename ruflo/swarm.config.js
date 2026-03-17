/**
 * the-conductor — ruflo swarm configuration
 * 16-role CISO security audit topology
 *
 * Install ruflo: npm install -g ruflo@latest
 * Add MCP:       claude mcp add ruflo -- npx -y ruflo@latest mcp start
 * Init:          npx ruflo@latest init --config ruflo/swarm.config.js
 */

module.exports = {
  // -------------------------------------------------------------------------
  // Core topology
  // -------------------------------------------------------------------------
  topology: "hierarchical",   // Queen node (CISO) + team workers
  maxAgents: 16,              // Matches the 16-role architecture
  strategy: "specialized",    // Clear role separation — reduces drift
  antiDrift: true,            // Prevent agents going off-task
  consensusMode: "coordinator", // CISO orchestrator makes final calls

  // -------------------------------------------------------------------------
  // Queen node — CISO Orchestrator
  // -------------------------------------------------------------------------
  coordinator: {
    name: "ciso-orchestrator",
    agentFile: ".claude/agents/ciso-orchestrator.md",
    role: "queen",
    responsibilities: [
      "scope-definition",
      "team-assignment",
      "finding-synthesis",
      "report-generation",
      "escalation-decisions",
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
  // Audit workflows
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
  },
};
