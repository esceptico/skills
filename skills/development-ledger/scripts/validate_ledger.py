#!/usr/bin/env python3
"""Validate a compact development ledger."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess


V2_HEADINGS = {
    "README.md": [
        "## Status",
        "## Original task",
        "## Amendments",
        "## Current synthesis",
        "## Decisions",
        "## Open questions",
        "## Next action",
    ],
    "research.md": ["## Surface research", "## Consolidated findings", "## Conflicts and gaps"],
    "implementation.md": ["## Intended outcome", "## Checklist", "## Notes"],
    "verification.md": ["## Status", "## Evidence", "## Failures and gaps", "## Outcome"],
}

V1_HEADINGS = {
    "README.md": ["## Status snapshot", "## Executive synthesis", "## Next action", "## Lifecycle files"],
    "01-intent.md": ["## Original request", "## Amendments", "## Interpreted objective", "## Constraints", "## Success conditions"],
    "02-research.md": ["## Research inbox", "## Surface research passes", "## Consolidated findings", "## Conflicts and uncertainties"],
    "03-questions.md": ["## Open questions", "## Resolved questions"],
    "04-synthesis.md": ["## Answer in one paragraph", "## Current model", "## Scope boundaries", "## Assumptions", "## Consequences for implementation"],
    "05-decisions.md": ["## Current decisions", "## Proposed decisions", "## Superseded decisions"],
    "06-implementation.md": ["## Intended outcome", "## Scope delta", "## Checklist", "## Execution order and dependencies", "## Implementation notes"],
    "07-verification.md": ["## Verification status", "## Required evidence", "## Failures and diagnosis", "## Remaining gaps", "## Final outcome"],
}

ALLOWED_STATES = {
    "researching",
    "needs-input",
    "ready-for-decision",
    "ready-for-implementation",
    "implementing",
    "verifying",
    "blocked",
    "complete",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", help="Ledger directory")
    parser.add_argument("--repo", default=".", help="Repository used to check revision drift")
    return parser.parse_args()


def git_head(repo: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def table_value(text: str, label: str) -> str | None:
    match = re.search(rf"^\|\s*{re.escape(label)}\s*\|\s*([^|]+?)\s*\|\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def main() -> int:
    args = parse_args()
    ledger = Path(args.ledger).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    contents: dict[str, str] = {}

    if not ledger.is_dir():
        raise SystemExit(f"Ledger directory not found: {ledger}")

    readme_path = ledger / "README.md"
    readme_preview = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    if "<!-- development-ledger:v2 -->" in readme_preview:
        required_headings = V2_HEADINGS
        state_label = "State"
        intent_file = "README.md"
        implementation_file = "implementation.md"
        verification_file = "verification.md"
    elif "<!-- development-ledger:v1 -->" in readme_preview:
        required_headings = V1_HEADINGS
        state_label = "Ledger status"
        intent_file = "01-intent.md"
        implementation_file = "06-implementation.md"
        verification_file = "07-verification.md"
    else:
        required_headings = V2_HEADINGS
        state_label = "State"
        intent_file = "README.md"
        implementation_file = "implementation.md"
        verification_file = "verification.md"
        errors.append("README.md: missing development-ledger:v1 or v2 marker")

    for filename, headings in required_headings.items():
        path = ledger / filename
        if not path.is_file():
            if filename in {"README.md", intent_file}:
                errors.append(f"missing required file: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        contents[filename] = text
        for heading in headings:
            if heading not in text:
                warnings.append(f"{filename}: template heading absent: '{heading}'; check whether it is relevant")
        lines = len(text.splitlines())
        limit = 160 if filename == "README.md" else 300
        if lines > 500:
            warnings.append(f"{filename}: {lines} lines; consider an appendix if bulky evidence obscures the findings")
        elif lines > limit:
            warnings.append(f"{filename}: {lines} lines; consolidation recommended above {limit}")
        if re.search(r"\{\{[A-Z0-9_]+\}\}", text):
            errors.append(f"{filename}: unresolved template token")

    readme = contents.get("README.md", "")

    state = table_value(readme, state_label)
    if state not in ALLOWED_STATES:
        errors.append(f"README.md: invalid or missing {state_label}: {state!r}")
    for label in ("Active phase", "Last updated", "Last consolidated", "Codebase revision", "Sources checked through"):
        if not table_value(readme, label):
            errors.append(f"README.md: missing watermark '{label}'")
    if "INTENT_NOT_CAPTURED" in contents.get(intent_file, ""):
        errors.append(f"{intent_file}: original user task has not been captured")

    implementation = contents.get(implementation_file, "")
    verification = contents.get(verification_file, "")
    checked_items = len(re.findall(r"^- \[[xX]\]", implementation, re.MULTILINE))
    evidence_rows = re.findall(r"^\|\s*V-[^\n]+", verification, re.MULTILINE)
    pass_rows = [row for row in evidence_rows if re.search(r"\|\s*pass(?: with [^|]+)?\s*\|", row, re.IGNORECASE)]
    nonpass_rows = [row for row in evidence_rows if re.search(r"\|\s*(fail|blocked|not-run|pending)\s*\|", row, re.IGNORECASE)]

    if checked_items and not evidence_rows:
        warnings.append("implementation has checked items but no tabular verification evidence was detected; review the recorded proof")
    if state == "complete":
        if not pass_rows:
            warnings.append("ledger is complete but no passing evidence row was detected; review completion evidence or user-accepted gaps")
        if nonpass_rows:
            warnings.append("ledger is complete with non-passing evidence; document accepted gaps")

    recorded_revision = table_value(readme, "Codebase revision")
    current_revision = git_head(Path(args.repo).resolve())
    if recorded_revision and recorded_revision != "unknown" and current_revision and recorded_revision != current_revision:
        warnings.append(f"codebase revision drift: ledger={recorded_revision[:12]} current={current_revision[:12]}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"INVALID: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"VALID: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
