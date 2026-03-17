#!/usr/bin/env python3
"""
skill_auditor.py — the-conductor
Scans SKILL.md files for security risks before importing into the repo.

Usage:
    python3 skill_auditor.py --path ../plugins/security-scanning/skills
    python3 skill_auditor.py --path ../plugins/ --recursive
    python3 skill_auditor.py --file ../plugins/security-scanning/skills/owasp/SKILL.md
    python3 skill_auditor.py --path ../plugins/ --recursive --output audit_report.json

Severity levels:
    PASS  — No flags found. Safe to use.
    WARN  — Suspicious pattern found. Manual review recommended.
    BLOCK — High-risk pattern found. Do not use without remediation.
"""

import os
import re
import json
import argparse
import sys
from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)
from pathlib import Path

# ---------------------------------------------------------------------------
# Known safe npm registries and CDNs
# ---------------------------------------------------------------------------
SAFE_REGISTRIES = {
    "npmjs.com",
    "npm.pkg.github.com",
    "registry.npmjs.org",
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "esm.sh",
    "pypi.org",
    "files.pythonhosted.org",
}

# Known-safe npx packages (well-established, verified on npmjs.com)
KNOWN_SAFE_NPX = {
    "create-react-app",
    "create-next-app",
    "create-vite",
    "prettier",
    "eslint",
    "typescript",
    "ts-node",
    "nodemon",
    "jest",
    "vitest",
    "playwright",
    "cypress",
    "tailwindcss",
    "prisma",
    "drizzle-kit",
    "wrangler",
    "vercel",
    "netlify-cli",
    "aws-cdk",
    "cdk",
    "serverless",
    "terraform",
    "pulumi",
    "kubectl",
    "helm",
    "docker",
    "nx",
    "turbo",
    "lerna",
    "changesets",
    "semver",
    "husky",
    "lint-staged",
    "commitlint",
    "semantic-release",
    "release-it",
    "np",
    "tsc",
    "swc",
    "esbuild",
    "rollup",
    "webpack",
    "vite",
    "parcel",
    "rome",
    "biome",
    "oxlint",
    "claude-flow",
    "ruflo",
    "antigravity-awesome-skills",
    "skillkit",
    "anthropic",
    "openai",
    "langchain",
}

# ---------------------------------------------------------------------------
# Risk patterns
# ---------------------------------------------------------------------------
BLOCK_PATTERNS = [
    # Piped execution — highest risk
    (r"curl\s+.+\s*\|\s*(bash|sh|zsh|fish)", "PIPE_EXEC: curl piped to shell"),
    (r"wget\s+.+\s*\|\s*(bash|sh|zsh|fish)", "PIPE_EXEC: wget piped to shell"),
    (r"irm\s+.+\s*\|\s*iex", "PIPE_EXEC: PowerShell irm|iex pattern"),
    (r"Invoke-Expression\s+.+Invoke-WebRequest", "PIPE_EXEC: PowerShell web invoke"),

    # Hardcoded secrets
    (r"(api_key|apikey|api-key)\s*[=:]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]",
     "HARDCODED_SECRET: API key literal"),
    (r"(secret|password|passwd|token)\s*[=:]\s*['\"][a-zA-Z0-9_\-]{16,}['\"]",
     "HARDCODED_SECRET: credential literal"),
    (r"sk-[a-zA-Z0-9]{40,}", "HARDCODED_SECRET: OpenAI API key pattern"),
    (r"ghp_[a-zA-Z0-9]{36}", "HARDCODED_SECRET: GitHub personal access token"),
    (r"AKIA[0-9A-Z]{16}", "HARDCODED_SECRET: AWS access key"),

    # Dangerous eval/exec
    (r"eval\s*\(\s*fetch", "REMOTE_EXEC: eval(fetch()) pattern"),
    (r"exec\s*\(\s*urllib", "REMOTE_EXEC: exec(urllib) pattern"),

    # Exfiltration patterns
    (r"(curl|wget|http\.get)\s+.+(discord|slack|telegram|webhook).+\$\{?(HOME|USER|PATH|AWS)",
     "EXFIL: possible env var exfiltration to webhook"),
]

WARN_PATTERNS = [
    # npx with unknown package — handled separately in check_npx_packages()
    # Suspicious curl without pipe (could be legit download)
    (r"curl\s+-[^\s]*[fsSL]+\s+https?://", "CURL_DOWNLOAD: external curl download"),
    (r"wget\s+https?://[^'\"\s]+\.(sh|py|js|exe|bat|ps1)",
     "WGET_SCRIPT: downloading executable script"),

    # External URLs outside safe registries
    (r"https?://(?!(" + "|".join(re.escape(r) for r in SAFE_REGISTRIES) + r"))[^\s'\"]+",
     "EXTERNAL_URL: URL outside known safe registries"),

    # chmod +x on downloaded files
    (r"chmod\s+\+x\s+", "CHMOD: making file executable"),

    # sudo usage
    (r"\bsudo\b", "SUDO: elevated privilege command"),

    # rm -rf
    (r"rm\s+-[rRf]{2,}\s+[/~$]", "DESTRUCTIVE: recursive force delete"),

    # env var injection
    (r"process\.env\.[A-Z_]{4,}", "ENV_ACCESS: accessing environment variables"),
    (r"\$\{?[A-Z_]{4,}\}?", "ENV_ACCESS: shell environment variable expansion"),
]

# ---------------------------------------------------------------------------
# NPX package validator
# ---------------------------------------------------------------------------
def extract_npx_packages(content):
    """Extract all package names from npx commands."""
    pattern = r"npx\s+(?:-y\s+|--yes\s+)?([a-zA-Z0-9@][a-zA-Z0-9/_\-@.]*)"
    matches = re.findall(pattern, content)
    packages = []
    for match in matches:
        # Strip version specifiers like @1.2.3
        name = re.sub(r"@[\d.]+.*$", "", match)
        # Handle scoped packages like @org/pkg
        if name.startswith("@"):
            packages.append(name)
        else:
            # Just the package name, no args
            name = name.split("/")[0]
            packages.append(name)
    return list(set(packages))


def check_npx_packages(content):
    """Flag npx packages not in the known-safe list."""
    findings = []
    packages = extract_npx_packages(content)
    for pkg in packages:
        # Strip scope for comparison
        base = pkg.lstrip("@").split("/")[-1] if "/" in pkg else pkg.lstrip("@")
        if base not in KNOWN_SAFE_NPX and pkg not in KNOWN_SAFE_NPX:
            findings.append({
                "severity": "WARN",
                "rule": "UNKNOWN_NPX_PACKAGE",
                "detail": f"npx package '{pkg}' not in known-safe list — verify on npmjs.com",
                "recommendation": "Run: npm view " + pkg + " to confirm it exists and is legitimate",
            })
    return findings


# ---------------------------------------------------------------------------
# Core scanner
# ---------------------------------------------------------------------------
def scan_file(filepath):
    """Scan a single SKILL.md file. Returns a result dict."""
    path = Path(filepath)
    result = {
        "file": str(path),
        "status": "PASS",
        "findings": [],
        "scanned_at": utcnow().isoformat() + "Z",
        "line_count": 0,
    }

    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result["status"] = "ERROR"
        result["findings"].append({
            "severity": "ERROR",
            "rule": "READ_ERROR",
            "detail": str(e),
            "recommendation": "Check file permissions and encoding.",
        })
        return result

    lines = content.splitlines()
    result["line_count"] = len(lines)

    # Check BLOCK patterns
    for pattern, label in BLOCK_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                result["findings"].append({
                    "severity": "BLOCK",
                    "rule": label,
                    "line": i,
                    "content": line.strip()[:120],
                    "recommendation": "Remove or replace this pattern before using this skill.",
                })

    # Check WARN patterns
    for pattern, label in WARN_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                # Skip if it's in a comment that's clearly explanatory
                stripped = line.strip()
                if stripped.startswith("#") and "example" in stripped.lower():
                    continue
                result["findings"].append({
                    "severity": "WARN",
                    "line": i,
                    "rule": label,
                    "content": line.strip()[:120],
                    "recommendation": "Review manually. May be legitimate but verify intent.",
                })

    # Check npx packages
    npx_findings = check_npx_packages(content)
    result["findings"].extend(npx_findings)

    # Determine overall status
    severities = [f["severity"] for f in result["findings"]]
    if "BLOCK" in severities:
        result["status"] = "BLOCK"
    elif "WARN" in severities:
        result["status"] = "WARN"
    else:
        result["status"] = "PASS"

    return result


def find_skill_files(root_path, recursive=False):
    """Find all SKILL.md files under root_path."""
    root = Path(root_path)
    if root.is_file():
        return [root]
    if recursive:
        return list(root.rglob("SKILL.md")) + list(root.rglob("*.skill.md"))
    else:
        return list(root.glob("**/SKILL.md"))


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------
def print_summary(results):
    totals = {"PASS": 0, "WARN": 0, "BLOCK": 0, "ERROR": 0}
    for r in results:
        totals[r["status"]] = totals.get(r["status"], 0) + 1

    print("\n" + "=" * 60)
    print("  the-conductor — Skill Audit Report")
    print("  " + utcnow().strftime("%Y-%m-%d %H:%M UTC"))
    print("=" * 60)
    print(f"  Files scanned : {len(results)}")
    print(f"  PASS          : {totals['PASS']}")
    print(f"  WARN          : {totals['WARN']}")
    print(f"  BLOCK         : {totals['BLOCK']}")
    if totals["ERROR"]:
        print(f"  ERROR         : {totals['ERROR']}")
    print("=" * 60)

    for r in results:
        status_icon = {"PASS": "✓", "WARN": "⚠", "BLOCK": "✗", "ERROR": "!"}.get(r["status"], "?")
        print(f"\n{status_icon} [{r['status']}] {r['file']}")
        for f in r["findings"]:
            line_ref = f"  line {f['line']}" if "line" in f else ""
            print(f"    [{f['severity']}] {f['rule']}{line_ref}")
            print(f"    → {f['detail'] if 'detail' in f else f.get('content', '')[:80]}")
            print(f"    ✎ {f['recommendation']}")

    print("\n" + "=" * 60)
    if totals["BLOCK"] > 0:
        print(f"  ✗ ACTION REQUIRED: {totals['BLOCK']} file(s) BLOCKED. Do not import.")
    if totals["WARN"] > 0:
        print(f"  ⚠ REVIEW NEEDED:  {totals['WARN']} file(s) need manual review.")
    if totals["PASS"] == len(results):
        print("  ✓ ALL CLEAR: All files passed. Safe to import.")
    print("=" * 60 + "\n")


def save_report(results, output_path):
    report = {
        "generated_at": utcnow().isoformat() + "Z",
        "tool": "the-conductor/skill_auditor.py",
        "summary": {
            "total": len(results),
            "pass": sum(1 for r in results if r["status"] == "PASS"),
            "warn": sum(1 for r in results if r["status"] == "WARN"),
            "block": sum(1 for r in results if r["status"] == "BLOCK"),
            "error": sum(1 for r in results if r["status"] == "ERROR"),
        },
        "results": results,
    }
    Path(output_path).write_text(json.dumps(report, indent=2))
    print(f"  Report saved: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Scan SKILL.md files for security risks before importing into the-conductor.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 skill_auditor.py --path ../plugins/security-scanning/skills
  python3 skill_auditor.py --path ../plugins/ --recursive
  python3 skill_auditor.py --file ../plugins/owasp/SKILL.md
  python3 skill_auditor.py --path ../plugins/ --recursive --output report.json
  python3 skill_auditor.py --path ~/Downloads/wshobson-agents --recursive --output audit.json
        """,
    )
    parser.add_argument("--path", help="Directory to scan")
    parser.add_argument("--file", help="Single SKILL.md file to scan")
    parser.add_argument("--recursive", action="store_true",
                        help="Recursively scan all subdirectories")
    parser.add_argument("--output", default="audit_report.json",
                        help="Output JSON report path (default: audit_report.json)")
    parser.add_argument("--quiet", action="store_true",
                        help="Only print summary, suppress per-finding output")
    parser.add_argument("--fail-on-warn", action="store_true",
                        help="Exit code 1 if any WARN found (use in CI)")

    args = parser.parse_args()

    if not args.path and not args.file:
        parser.print_help()
        sys.exit(1)

    # Collect files
    if args.file:
        skill_files = [Path(args.file)]
    else:
        skill_files = find_skill_files(args.path, recursive=args.recursive)

    if not skill_files:
        print(f"No SKILL.md files found in: {args.path}")
        sys.exit(0)

    print(f"\nScanning {len(skill_files)} skill file(s)...")

    results = []
    for f in sorted(skill_files):
        result = scan_file(f)
        results.append(result)
        if not args.quiet:
            icon = {"PASS": "✓", "WARN": "⚠", "BLOCK": "✗", "ERROR": "!"}.get(result["status"], "?")
            print(f"  {icon} {result['status']:5s}  {f}")

    print_summary(results)
    save_report(results, args.output)

    # Exit codes for CI integration
    has_blocks = any(r["status"] == "BLOCK" for r in results)
    has_warns = any(r["status"] == "WARN" for r in results)

    if has_blocks:
        sys.exit(2)  # BLOCK = exit 2
    if args.fail_on_warn and has_warns:
        sys.exit(1)  # WARN with --fail-on-warn = exit 1
    sys.exit(0)


if __name__ == "__main__":
    main()
