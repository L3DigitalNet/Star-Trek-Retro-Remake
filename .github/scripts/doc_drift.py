#!/usr/bin/env python3
"""
Document drift detector for Star-Trek-Retro-Remake.

Runs four focused semantic analyses using Ollama (localhost:11434):
  1. Version/dependency consistency (README vs pyproject.toml)
  2. Feature status accuracy (README claims vs source modules present)
  3. Installation instruction validity (steps, package names, paths)
  4. Broken documentation links (README references vs files on disk)

Designed to run in GitHub Actions on the self-hosted Hetzner runner, which
has direct localhost access to Ollama — no auth, no SSH tunnel required.

Creates/updates a GitHub issue labelled "doc-drift" with findings.
Always exits 0 — drift is a report, not a build failure.

Caller: .github/workflows/doc-drift.yml
"""
from __future__ import annotations

import http.client
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

OLLAMA_HOST = "127.0.0.1"
OLLAMA_PORT = 11434
OLLAMA_MODEL = "qwen3:14b"
DRIFT_LABEL = "doc-drift"

# Repo root is 3 levels up from this file (.github/scripts/doc_drift.py)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


# ── Ollama ────────────────────────────────────────────────────────────────────


def ollama_available() -> bool:
    try:
        conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=5)
        conn.request("GET", "/api/tags")
        return conn.getresponse().status == 200
    except OSError:
        return False


def ollama(prompt: str) -> str:
    """Call Ollama generate endpoint; return response text."""
    payload = json.dumps(
        {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            # Low temperature for consistent, factual structured output
            "options": {"temperature": 0.1, "num_predict": 1024},
        }
    ).encode()

    try:
        conn = http.client.HTTPConnection(OLLAMA_HOST, OLLAMA_PORT, timeout=120)
        conn.request(
            "POST", "/api/generate", body=payload, headers={"Content-Type": "application/json"}
        )
        raw = conn.getresponse().read().decode()
        return json.loads(raw).get("response", "")
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"  Ollama error: {exc}", file=sys.stderr)
        return ""


def parse_json_response(text: str) -> dict:
    """Extract JSON object from Ollama response; handles surrounding prose."""
    text = text.strip()
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Extract from fenced code block or bare braces
    for pattern in (r"```json\s*(\{.*?\})\s*```", r"(\{[^{}]*\})"):
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
    print(f"  Could not parse JSON from response: {text[:200]}", file=sys.stderr)
    return {}


# ── Context gathering ─────────────────────────────────────────────────────────


def gather_context() -> dict:
    readme_path = REPO_ROOT / "README.md"
    pyproject_path = REPO_ROOT / "pyproject.toml"
    src_dir = REPO_ROOT / "STRR" / "src"

    readme = readme_path.read_text() if readme_path.exists() else ""
    pyproject = pyproject_path.read_text() if pyproject_path.exists() else ""

    # Source module tree (paths relative to repo root, no content)
    source_tree = ""
    if src_dir.exists():
        py_files = sorted(
            str(p.relative_to(REPO_ROOT))
            for p in src_dir.rglob("*.py")
            if "__pycache__" not in str(p)
        )
        source_tree = "\n".join(py_files)

    # All markdown/doc files that actually exist on disk
    existing_docs = sorted(
        str(p.relative_to(REPO_ROOT))
        for p in REPO_ROOT.rglob("*.md")
        if ".git" not in str(p) and "__pycache__" not in str(p)
    )

    # Extract all relative file links from the README for targeted link checking
    # Matches [text](path) where path doesn't start with http
    readme_links = re.findall(r"\[([^\]]+)\]\((?!https?://)([^)]+)\)", readme)

    return {
        "readme": readme,
        "pyproject": pyproject,
        "source_tree": source_tree,
        "existing_docs": "\n".join(existing_docs),
        "readme_links": readme_links,  # list of (text, path) tuples
    }


# ── Analysis passes ───────────────────────────────────────────────────────────


def check_version_and_deps(ctx: dict) -> list[str]:
    """Versions, Python requirements, and dependency names/versions."""
    print("  Checking version and dependency consistency...")
    response = ollama(f"""
You are a documentation auditor. Compare version numbers and dependency information
between the README and pyproject.toml. Be specific and factual.

pyproject.toml (source of truth):
{ctx['pyproject']}

README content:
{ctx['readme'][:3000]}

Return ONLY a JSON object with this exact structure, no other text:
{{"issues": ["specific issue 1", "specific issue 2"]}}

Look for: wrong version numbers, wrong package names (e.g. "pygame" vs "pygame-ce"),
wrong Python version requirements, outdated version pins.
If everything is consistent, return {{"issues": []}}.
""")
    return parse_json_response(response).get("issues", [])


def check_feature_status(ctx: dict) -> list[str]:
    """README feature claims vs what source modules actually exist."""
    print("  Checking feature status accuracy...")
    response = ollama(f"""
You are a documentation auditor. The README describes game features and their
development status (Completed / In Progress / Planned). Cross-reference these
claims against the actual source modules that exist in the repository.

Source modules that exist:
{ctx['source_tree']}

README development status section and feature descriptions:
{ctx['readme'][2000:5500]}

Return ONLY a JSON object with this exact structure, no other text:
{{"issues": ["specific issue 1", "specific issue 2"]}}

Look for: features marked "In Progress" or "Planned" that have source files
implementing them; features claimed "Completed" with no corresponding source
module; major source modules not mentioned in the README at all.
If the README is accurate, return {{"issues": []}}.
""")
    return parse_json_response(response).get("issues", [])


def check_install_instructions(ctx: dict) -> list[str]:
    """Installation steps, paths, package names, and entry points."""
    print("  Checking installation instructions...")
    response = ollama(f"""
You are a documentation auditor. Check whether the installation instructions
in the README are accurate given the actual project structure in pyproject.toml.

pyproject.toml (source of truth for install commands, entry points, paths):
{ctx['pyproject']}

README installation section:
{ctx['readme'][1500:4000]}

Return ONLY a JSON object with this exact structure, no other text:
{{"issues": ["specific issue 1", "specific issue 2"]}}

Look for: wrong directory names in cd commands, wrong package names in pip commands,
wrong entry point command names, wrong Python version requirements,
references to paths or files that don't match the actual structure.
If instructions are accurate, return {{"issues": []}}.
""")
    return parse_json_response(response).get("issues", [])


def check_doc_links(ctx: dict) -> list[str]:
    """Broken relative file links in the README."""
    print("  Checking documentation links...")
    issues: list[str] = []

    # Do the link check directly in Python — no need to ask Ollama for this
    # (it's a deterministic filesystem check, not a semantic analysis)
    existing_set = set(ctx["existing_docs"].splitlines())

    for link_text, link_path in ctx["readme_links"]:
        # Strip anchors (#section)
        clean_path = link_path.split("#")[0].strip()
        if not clean_path:
            continue
        # Check actual filesystem — existing_set is .md only, so use Path.exists()
        if not (REPO_ROOT / clean_path).exists():
            issues.append(
                f'README link "[{link_text}]({link_path})" points to '
                f'"{clean_path}" which does not exist on disk'
            )

    # Also ask Ollama for semantic link accuracy (paths that exist but may be wrong)
    if ctx["readme_links"]:
        links_summary = "\n".join(f"  [{t}]({p})" for t, p in ctx["readme_links"][:20])
        response = ollama(f"""
You are a documentation auditor. The README references the following doc files.
Identify any that seem misplaced or point to the wrong location based on the
actual docs inventory.

README links:
{links_summary}

Files that actually exist:
{ctx['existing_docs']}

Return ONLY a JSON object with this exact structure, no other text:
{{"issues": ["specific issue 1", "specific issue 2"]}}

Only report issues where a file exists at a different path than linked.
If all paths look correct, return {{"issues": []}}.
""")
        issues.extend(parse_json_response(response).get("issues", []))

    return issues


# ── GitHub issue management ────────────────────────────────────────────────────


def ensure_label() -> None:
    """Create the doc-drift label if it doesn't exist yet."""
    subprocess.run(
        [
            "gh", "label", "create", DRIFT_LABEL,
            "--color", "e4e669",
            "--description", "Documentation is out of sync with the codebase",
            "--force",  # no-op if it already exists
        ],
        capture_output=True,
    )


def find_existing_issue() -> int | None:
    result = subprocess.run(
        ["gh", "issue", "list", "--label", DRIFT_LABEL, "--state", "open",
         "--json", "number", "--limit", "1"],
        capture_output=True, text=True,
    )
    try:
        issues = json.loads(result.stdout)
        return issues[0]["number"] if issues else None
    except (json.JSONDecodeError, IndexError, KeyError):
        return None


def build_issue_body(all_issues: list[str]) -> str:
    rows = "\n".join(f"| {i} | {issue} |" for i, issue in enumerate(all_issues, 1))
    return f"""\
## Documentation Drift Report

Automated analysis found **{len(all_issues)}** inconsistenc{'y' if len(all_issues) == 1 else 'ies'} \
between the documentation and current codebase.

| # | Finding |
|---|---------|
{rows}

---
_Generated by [doc-drift workflow](/.github/workflows/doc-drift.yml) · \
model: {OLLAMA_MODEL}_
"""


def post_or_update_issue(all_issues: list[str], existing: int | None) -> None:
    title = f"Doc drift: {len(all_issues)} issue{'s' if len(all_issues) != 1 else ''} found"
    body = build_issue_body(all_issues)

    if existing:
        subprocess.run(
            ["gh", "issue", "edit", str(existing), "--title", title, "--body", body],
            check=True,
        )
        subprocess.run(
            ["gh", "issue", "comment", str(existing),
             "--body", f"Refreshed: {len(all_issues)} issue(s) on latest scan."],
        )
        print(f"  Updated existing issue #{existing}: {title}")
    else:
        subprocess.run(
            ["gh", "issue", "create", "--title", title, "--body", body,
             "--label", DRIFT_LABEL],
            check=True,
        )
        print(f"  Created new doc-drift issue: {title}")


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    print("=== Doc Drift Detector ===")
    print(f"Repo root: {REPO_ROOT}")

    if not ollama_available():
        print("ERROR: Ollama not reachable at 127.0.0.1:11434 — is this running on the Hetzner runner?",
              file=sys.stderr)
        return 1

    print("\nGathering repository context...")
    ctx = gather_context()

    print("\nRunning analysis passes:")
    all_issues: list[str] = []
    all_issues.extend(check_version_and_deps(ctx))
    all_issues.extend(check_feature_status(ctx))
    all_issues.extend(check_install_instructions(ctx))
    all_issues.extend(check_doc_links(ctx))

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_issues = [x for x in all_issues if not (x in seen or seen.add(x))]  # type: ignore[func-returns-value]

    print(f"\nFound {len(unique_issues)} issue(s):")
    for i, issue in enumerate(unique_issues, 1):
        print(f"  {i}. {issue}")

    if not os.environ.get("GITHUB_TOKEN"):
        print("\nNo GITHUB_TOKEN — skipping issue management (dry run).")
        return 0

    ensure_label()
    existing = find_existing_issue()

    if not unique_issues:
        print("\nNo drift detected.")
        if existing:
            subprocess.run(
                ["gh", "issue", "close", str(existing),
                 "--comment", "All clear — no drift detected on latest scan."],
            )
            print(f"  Closed existing issue #{existing}")
        return 0

    post_or_update_issue(unique_issues, existing)
    # Always exit 0 — drift is informational, not a blocking failure
    return 0


if __name__ == "__main__":
    sys.exit(main())
