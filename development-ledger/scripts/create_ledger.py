#!/usr/bin/env python3
"""Create a development ledger from the bundled lifecycle templates."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unicodedata


TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "ledger-template"


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug[:63].rstrip("-") or "task"


def git_value(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "unknown"
    except (FileNotFoundError, subprocess.CalledProcessError):
        return "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default="docs/ledgers", help="Parent directory for ledgers")
    parser.add_argument("--title", required=True, help="Human-readable task title")
    parser.add_argument("--slug", help="Directory name; defaults to a slug of the title")
    parser.add_argument("--repo", default=".", help="Repository used for paths and git watermarks")
    parser.add_argument("--intent-file", help="UTF-8 file containing original user prose verbatim")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(args.repo).resolve()
    root = Path(args.root)
    if not root.is_absolute():
        root = repo / root
    slug = slugify(args.slug or args.title)
    destination = root / slug

    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing ledger: {destination}")
    if not TEMPLATE_DIR.is_dir():
        raise SystemExit(f"Template directory not found: {TEMPLATE_DIR}")

    if args.intent_file:
        intent = Path(args.intent_file).read_text(encoding="utf-8").rstrip()
        if not intent:
            raise SystemExit("Intent file is empty")
    else:
        intent = "INTENT_NOT_CAPTURED: replace this line with the user's original request verbatim."

    now = datetime.now().astimezone().isoformat(timespec="seconds")
    revision = git_value(repo, "rev-parse", "HEAD")
    branch = git_value(repo, "branch", "--show-current")
    if branch == "unknown":
        branch = git_value(repo, "rev-parse", "--abbrev-ref", "HEAD")

    replacements = {
        "{{TITLE}}": args.title,
        "{{SLUG}}": slug,
        "{{CREATED_AT}}": now,
        "{{UPDATED_AT}}": now,
        "{{REVISION}}": revision,
        "{{BRANCH}}": branch,
        "{{INTENT}}": intent,
    }

    root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{slug}-", dir=root))
    try:
        for template in sorted(TEMPLATE_DIR.iterdir()):
            if not template.is_file():
                continue
            content = template.read_text(encoding="utf-8")
            for token, value in replacements.items():
                content = content.replace(token, value)
            if re.search(r"\{\{[A-Z0-9_]+\}\}", content):
                raise RuntimeError(f"Unresolved template token in {template.name}")
            (temporary / template.name).write_text(content, encoding="utf-8")
        temporary.rename(destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
