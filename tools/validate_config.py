#!/usr/bin/env python3
"""
validate_config.py — the-conductor configuration validator
Cross-references all components to catch configuration drift.

Usage: python3 tools/validate_config.py

Exit codes:
  0 = All checks pass (GREEN)
  1 = Warnings found (YELLOW)
  2 = Critical failures found (RED)
"""

import sys
import re
from pathlib import Path

RED, YELLOW, CYAN, GREEN, RESET, BOLD = "\033[91m", "\033[93m", "\033[96m", "\033[92m", "\033[0m", "\033[1m"


class ConfigValidator:
    def __init__(self, base_path="."):
        self.base = Path(base_path)
        self.failures, self.warnings, self.passes = [], [], []
        self.agent_files = self._load_agent_files()
        self.swarm_config = self._load_swarm_config()
        self.valid_categories = self._load_valid_categories()
        self.command_files = self._load_command_files()
        self.claude_md = self._load_claude_md()

    def _load_agent_files(self):
        agents = {}
        agents_dir = self.base / ".claude" / "agents"
        if not agents_dir.exists():
            self.failures.append(f"Agents directory not found: {agents_dir}")
            return agents
        return {f.stem: f for f in agents_dir.glob("*.md")}

    def _load_swarm_config(self):
        config = {"coordinator_name": None, "team_ids": set(), "agents": set()}
        swarm_file = self.base / "ruflo" / "swarm.config.js"
        if not swarm_file.exists():
            self.failures.append(f"Swarm config not found: {swarm_file}")
            return config
        try:
            content = swarm_file.read_text()
            coord_match = re.search(r'name:\s*"([^"]+)".*?role:\s*"queen"', content, re.DOTALL)
            if coord_match:
                config["coordinator_name"] = coord_match.group(1)
            config["team_ids"] = set(re.findall(r'id:\s*"([^"]+)"', content))
            config["agents"] = set(re.findall(r'name:\s*"([^"]+)"', content)) - {"security-program-manager", "master-orchestrator"}
            config["agents"].update(re.findall(r'name:\s*"([^"]+)"', content))
        except Exception as e:
            self.failures.append(f"Error parsing swarm config: {e}")
        return config

    def _load_valid_categories(self):
        categories = set()
        logger_file = self.base / "persistence" / "severity_logger.py"
        if not logger_file.exists():
            self.failures.append(f"Logger file not found: {logger_file}")
            return categories
        try:
            content = logger_file.read_text()
            match = re.search(r'VALID_CATEGORIES\s*=\s*\{(.*?)\}', content, re.DOTALL)
            if match:
                categories = set(re.findall(r'"([^"]+)"', match.group(1)))
        except Exception as e:
            self.failures.append(f"Error parsing logger: {e}")
        return categories

    def _load_command_files(self):
        commands_dir = self.base / ".claude" / "commands"
        return {f.stem for f in commands_dir.glob("*.md")} if commands_dir.exists() else set()

    def _load_claude_md(self):
        claude_file = self.base / "CLAUDE.md"
        if not claude_file.exists():
            self.failures.append(f"CLAUDE.md not found: {claude_file}")
            return ""
        return claude_file.read_text()

    def check_agent_registration(self):
        file_agents = set(self.agent_files.keys())
        registered = self.swarm_config["agents"]

        # Coordinator check
        if self.swarm_config["coordinator_name"]:
            self.passes.append(f"✓ Coordinator '{self.swarm_config['coordinator_name']}' registered")

        # Missing registration
        missing_reg = file_agents - registered - {self.swarm_config["coordinator_name"]}
        for agent in sorted(missing_reg):
            self.warnings.append(f"Agent file exists but not registered in swarm.config: {agent}.md")

        # Missing files
        missing_files = registered - file_agents
        for agent in sorted(missing_files):
            self.failures.append(f"Agent '{agent}' registered in swarm.config but no file: .claude/agents/{agent}.md")

        if not missing_files and not missing_reg and self.swarm_config["coordinator_name"]:
            self.passes.append(f"✓ All {len(registered)} agents registered in swarm.config")
        return len(missing_files) == 0

    def check_category_validity(self):
        invalid_cats = {}
        for agent_name, agent_file in sorted(self.agent_files.items()):
            try:
                content = agent_file.read_text()
                for category in re.findall(r'category="([^"]+)"', content):
                    if category not in self.valid_categories:
                        invalid_cats.setdefault(category, []).append(agent_name)
            except Exception as e:
                self.warnings.append(f"Error reading {agent_name}: {e}")

        for category in sorted(invalid_cats.keys()):
            self.failures.append(f"Invalid category '{category}' used in: {', '.join(invalid_cats[category])}")

        if not invalid_cats:
            self.passes.append(f"✓ All agent categories valid ({len(self.valid_categories)} allowed)")
        return len(invalid_cats) == 0

    def check_team_validity(self):
        invalid_teams = {}
        for agent_name, agent_file in sorted(self.agent_files.items()):
            try:
                content = agent_file.read_text()
                for team in re.findall(r'team="([^"]+)"', content):
                    if team not in self.swarm_config["team_ids"]:
                        invalid_teams.setdefault(team, []).append(agent_name)
            except Exception as e:
                self.warnings.append(f"Error reading {agent_name}: {e}")

        for team in sorted(invalid_teams.keys()):
            self.failures.append(f"Invalid team '{team}' referenced in: {', '.join(invalid_teams[team])}")

        if not invalid_teams:
            self.passes.append(f"✓ All agent team references valid ({len(self.swarm_config['team_ids'])} teams)")
        return len(invalid_teams) == 0

    def check_command_mapping(self):
        doc_commands = set()
        for line in self.claude_md.split('\n'):
            match = re.match(r'\s*/([a-z\-]+)(?::([a-z\-]+))?', line)
            if match:
                cmd = f"{match.group(1)}:{match.group(2)}" if match.group(2) else match.group(1)
                doc_commands.add(cmd)

        known_composites = {
            'compliance:gap-analysis', 'client:project-status', 'automate:workflow',
            'lead-gen:quick', 'dev:assist', 'data:research', 'marketing:campaign', 'report:generate'
        }

        missing = doc_commands - known_composites
        file_parts = set()
        for cmd in doc_commands:
            if ':' in cmd:
                file_parts.update(cmd.split(':'))
            else:
                file_parts.add(cmd)

        for cmd in sorted(missing):
            if ':' in cmd:
                ns, subcmd = cmd.split(':')
                if not any(subcmd in f or f in subcmd for f in self.command_files):
                    self.failures.append(f"Command documented ({cmd}) but no implementation file")
            else:
                if not any(cmd in f or f in cmd for f in self.command_files):
                    self.failures.append(f"Command documented (/{cmd}) but no implementation file")

        orphaned = self.command_files - file_parts
        for f in sorted(orphaned):
            if not any(fp in f or f in fp for fp in file_parts):
                self.warnings.append(f"Command file {f}.md exists but no CLAUDE.md reference")

        if not missing:
            self.passes.append(f"✓ All {len(doc_commands)} documented commands have implementations")
        return len([m for m in missing if m not in known_composites]) == 0

    def check_workflow_validity(self):
        swarm_file = self.base / "ruflo" / "swarm.config.js"
        if not swarm_file.exists():
            return True
        try:
            content = swarm_file.read_text()
            matches = re.findall(r'"([^"]+)":\s*\{[^}]*sequence:\s*\[([^\]]+)\]', content)
            invalid = []
            for wf_name, seq_str in matches:
                for team_id in re.findall(r'"([^"]+)"', seq_str):
                    if team_id not in self.swarm_config["team_ids"]:
                        invalid.append(f"Workflow '{wf_name}' references invalid team: {team_id}")
            for err in invalid:
                self.failures.append(err)
            if not invalid and matches:
                self.passes.append(f"✓ All {len(matches)} workflow sequences reference valid teams")
            return len(invalid) == 0
        except Exception as e:
            self.warnings.append(f"Error validating workflows: {e}")
            return True

    def run_all_checks(self):
        print(f"\n{BOLD}{'═' * 65}{RESET}")
        print(f"{BOLD}the-conductor Configuration Validator{RESET}")
        print(f"{BOLD}{'═' * 65}{RESET}\n")

        checks = [
            (self.check_agent_registration, "[1/5] Agent Registration..."),
            (self.check_category_validity, "[2/5] Category Validity..."),
            (self.check_team_validity, "[3/5] Team Validity..."),
            (self.check_command_mapping, "[4/5] Command Mapping..."),
            (self.check_workflow_validity, "[5/5] Workflow Validation..."),
        ]
        all_pass = True
        for check_func, label in checks:
            print(f"{CYAN}{label}{RESET}")
            all_pass = check_func() and all_pass

        self._print_results()
        return 0 if (not self.failures and not self.warnings) else (1 if not self.failures else 2)

    def _print_results(self):
        print(f"\n{BOLD}{'─' * 65}{RESET}\n")
        if self.passes:
            print(f"{GREEN}PASS:{RESET}")
            for msg in self.passes:
                print(f"  {GREEN}✓{RESET} {msg}")
            print()
        if self.warnings:
            print(f"{YELLOW}WARNINGS:{RESET}")
            for msg in self.warnings:
                print(f"  {YELLOW}⚠{RESET} {msg}")
            print()
        if self.failures:
            print(f"{RED}FAILURES:{RESET}")
            for msg in self.failures:
                print(f"  {RED}✗{RESET} {msg}")
            print()
        print(f"{BOLD}{'─' * 65}{RESET}")
        print(f"{BOLD}Summary:{RESET} {GREEN}{len(self.passes)} passed{RESET}, "
              f"{YELLOW}{len(self.warnings)} warnings{RESET}, {RED}{len(self.failures)} failures{RESET}")

        if self.failures:
            print(f"\n{RED}{BOLD}Exit code: 2 (FAILURES){RESET}")
        elif self.warnings:
            print(f"\n{YELLOW}{BOLD}Exit code: 1 (WARNINGS){RESET}")
        else:
            print(f"\n{GREEN}{BOLD}Exit code: 0 (ALL PASS){RESET}")


def main():
    current = Path.cwd()
    base_path = current
    for path in [current, current.parent, current.parent.parent]:
        if (path / "CLAUDE.md").exists() and (path / "ruflo" / "swarm.config.js").exists():
            base_path = path
            break
    validator = ConfigValidator(str(base_path))
    sys.exit(validator.run_all_checks())


if __name__ == "__main__":
    main()
