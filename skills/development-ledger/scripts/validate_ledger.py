#!/usr/bin/env python3
"""Validate the structure, watermarks, and completion claims of a development ledger."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess


REQUIRED_HEADINGS = {
    "README.md": ["## Status snapshot", "## Executive synthesis", "## Next action", "## Lifecycle files"],
    "01-intent.md": ["## Original request", "## Amendments", "## Interpreted objective", "## Constraints", "## Success conditions"],
    "02-research.md": ["## Research inbox", "## Surface research passes", "## Consolidated findings", "## Conflicts and uncertainties"],
    "03-questions.md": ["## Open questions", "## Resolved questions"],
    "04-synthesis.md": ["## Answer in one paragraph", "## Current model", "## Scope boundaries", "## Assumptions", "## Consequences for implementation"],
    "05-decisions.md": ["## Current decisions", "## Proposed decisions", "## Superseded decisions"],
    "06-implementation.md": ["## Intended outcome", "## Scope delta", "## Checklist", "## Execution order and dependencies", "## Implementation notes"],
    "07-verification.md": ["## Verification status", "## Required evidence", "## Failures and diagnosis", "## Remaining gaps", "## Final outcome"],
}

ALLOWED_STATUSES = {
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

    for filename, headings in REQUIRED_HEADINGS.items():
        path = ledger / filename
        if not path.is_file():
            errors.append(f"missing required file: {filename}")
            continue
        text = path.read_text(encoding="utf-8")
        contents[filename] = text
        for heading in headings:
            if heading not in text:
                errors.append(f"{filename}: missing heading beginning with '{heading}'")
        line_count = len(text.splitlines())
        limit = 120 if filename == "README.md" else 250
        if line_count > 500:
            errors.append(f"{filename}: {line_count} lines; must compress or split supporting evidence")
        elif line_count > limit:
            warnings.append(f"{filename}: {line_count} lines; consolidation recommended above {limit}")
        if re.search(r"\{\{[A-Z0-9_]+\}\}", text):
            errors.append(f"{filename}: unresolved template token")

    readme = contents.get("README.md", "")
    if "<!-- development-ledger:v1 -->" not in readme:
        errors.append("README.md: missing development-ledger marker")

    status = table_value(readme, "Ledger status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"README.md: invalid or missing Ledger status: {status!r}")
    for label in ("Active phase", "Last updated", "Last consolidated", "Codebase revision", "Sources checked through"):
        if not table_value(readme, label):
            errors.append(f"README.md: missing watermark '{label}'")

    intent = contents.get("01-intent.md", "")
    if "INTENT_NOT_CAPTURED" in intent:
        errors.append("01-intent.md: original user intent has not been captured")

    implementation = contents.get("06-implementation.md", "")
    verification = contents.get("07-verification.md", "")
    checked_items = len(re.findall(r"^- \[[xX]\]", implementation, re.MULTILINE))
    verification_rows = re.findall(r"^\|\s*V-[^\n]+", verification, re.MULTILINE)
    pass_rows = [row for row in verification_rows if re.search(r"\|\s*pass\s*\|", row, re.IGNORECASE)]
    nonpass_rows = [row for row in verification_rows if re.search(r"\|\s*(fail|blocked|not-run)\s*\|", row, re.IGNORECASE)]

    if checked_items and not verification_rows:
        warnings.append("implementation has checked items but verification has no evidence rows")
    if status == "complete":
        if not pass_rows:
            errors.append("ledger is complete but no passing verification evidence is recorded")
        if nonpass_rows:
            warnings.append("ledger is complete with non-passing verification rows; confirm accepted gaps are explicit")

    recorded_revision = table_value(readme, "Codebase revision")
    current_revision = git_head(Path(args.repo).resolve())
    if recorded_revision and recorded_revision != "unknown" and current_revision and recorded_revision != current_revision:
        warnings.append(
            f"codebase revision drift: ledger={recorded_revision[:12]} current={current_revision[:12]}"
        )

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
