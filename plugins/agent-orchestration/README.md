# Agent Orchestration Plugin

**Purpose:** Multi-agent workflow management, team coordination, and parallel execution.

## Overview

The Agent Orchestration plugin manages the Ruflo swarm topology that powers the-conductor. It handles agent spawning, task distribution across teams, progress monitoring, failure recovery, and result synthesis. This plugin ensures that 16 specialist agents work efficiently in parallel without conflicts or data races.

## Capabilities

- **Hierarchical orchestration**: CISO Orchestrator as queen node with 5 team leads
- **Parallel execution**: Spawn agents within teams simultaneously, sequence teams as needed
- **Progress monitoring**: Real-time tracking of agent status and findings
- **Failure handling**: Automatic retry, graceful degradation, fallback strategies
- **Task batching**: Optimal distribution of work to avoid bottlenecks
- **Result synthesis**: Merge findings from parallel agents into coherent reports
- **Anti-drift mechanisms**: Ensure agents stay focused on assigned scope
- **Session persistence**: All findings logged to central database

## How to Use

### Within the-conductor audit workflows

This plugin is the backbone of:
- `/security-audit:full-audit` — orchestrates all 16 agents across 5 teams
- `/security-audit:quick-scan` — manages Teams 2 and 3 in parallel
- `/compliance:gap-analysis` — controls Team 4 execution
- `/incident-response:triage` — manages Team 5 workflow

### Manual invocation

```
/orchestrate:spawn-team --team 2 --agents sast-scanner,dependency-auditor,code-reviewer,api-analyst
/orchestrate:monitor --team 2
/orchestrate:synthesize --teams 2,3
```

## Directory Structure

- **agents/**: Orchestration agents (CISO Orchestrator, Team Leads, Monitor, Synthesizer)
- **commands/**: CLI for workflow control and monitoring
- **skills/**: Reusable orchestration skills (swarm-management, progress-tracking, synthesis)

## Integration Points

- Central authority for all team coordination
- Manages communication between Teams 2-5
- Feeds aggregated findings to `persistence/severity_logger.py`
- Queries audit state from `persistence/dashboard.py`

## Requirements

- Python 3.8+ for agent lifecycle management
- SQLite access to `persistence/audit.db`
- Bash for parallel task scheduling
- File system for session state tracking

## Workflow Order (Full Audit)

```
1. CISO Orchestrator initializes audit scope
2. Team 2 (Software Security) runs 4 agents in parallel
3. Team 3 (Infrastructure) runs 3 agents in parallel
4. Team 4 (Compliance) runs 3 agents in parallel
5. Team 5 (Incident Response) runs 3 agents in parallel
6. CISO Orchestrator synthesizes all findings into report
```

## Output

- Agent status updates in real-time
- Structured findings via persistence layer
- Final audit report with all findings organized by severity and category
