# Blocked Skills Log

Skills that were reviewed and excluded from the-conductor due to security risks found by `skill_auditor.py`.

## Format

| Date | Source Repo | Skill Name | Reason | Rule Triggered |
|------|-------------|-----------|--------|---------------|
| - | - | - | - | - |

## Reference incident

**Oct 17, 2025** — `wshobson/agents` commit `65e5cb0` shipped 47 LLM-generated skills
with no human review. Two skills (`react-modernization`, `dependency-upgrade`) referenced
`npx react-codeshift` — a non-existent npm package that could be registered by a threat
actor (slopsquatting). Source: [Aikido Security report](https://www.aikido.dev/blog/agent-skills-spreading-hallucinated-npx-commands).

This is why every skill imported into the-conductor goes through `tools/skill_auditor.py` first.
