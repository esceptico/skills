#!/usr/bin/env python3
"""Create, list, check, sync, and render development ledgers.

Markdown files are the source of truth. This tool only reads them, except
`new` (creates a ledger) and `sync` (records the current git revision).
"""

from __future__ import annotations

import argparse
from datetime import datetime
import html
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import webbrowser

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets" / "ledger-template"
VIEW_TEMPLATE = SKILL_DIR / "assets" / "view.html"

MARKER = "<!-- development-ledger:v2 -->"
STATES = ("researching", "implementing", "verifying", "blocked", "complete")
LEGACY_STATES = {
    "needs-input": "blocked",
    "ready-for-decision": "blocked",
    "ready-for-implementation": "implementing",
}
RESULTS = ("pass", "fail", "blocked", "not-run")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".tox", ".mypy_cache"}
NOT_CAPTURED = "INTENT_NOT_CAPTURED"
README_LIMIT, FILE_LIMIT = 160, 300


# ---------- git ----------

def git(cwd: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


# ---------- markdown parsing ----------

def sections(text: str) -> dict[str, str]:
    """Map each `## Heading` to its body."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.MULTILINE)
    return {parts[i]: parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def section(text: str, prefix: str) -> str | None:
    for heading, body in sections(text).items():
        if heading.lower().startswith(prefix.lower()):
            return body
    return None


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table(text: str) -> list[dict[str, str]]:
    """Parse the first markdown table in `text` into header-keyed rows."""
    lines = [line for line in text.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return []
    header = [cell.lower() for cell in split_row(lines[0])]
    rows = []
    for line in lines[2:]:
        cells = split_row(line)
        rows.append(dict(zip(header, cells)))
    return rows


class Ledger:
    def __init__(self, path: Path):
        self.path = path.resolve()
        self.files = {p.name: p.read_text(encoding="utf-8") for p in sorted(self.path.glob("*.md"))}
        self.readme = self.files.get("README.md", "")
        status = section(self.readme, "Status") or ""
        self.status = {row.get("field", ""): row.get("value", "") for row in table(status)}
        title = re.search(r"^# +(.+)$", self.readme, re.MULTILINE)
        self.title = title.group(1).strip() if title else self.path.name
        self.state = self.status.get("State", "")
        self.revision = self.status.get("Codebase revision", "")

    def items(self) -> list[dict[str, str]]:
        """Checklist items from implementation.md: id, title, done."""
        found = []
        for match in re.finditer(r"^- \[([ xX])\]\s+(.+)$", self.files.get("implementation.md", ""), re.MULTILINE):
            label = match.group(2).replace("**", "").strip()
            item_id = re.search(r"\bI-\d+\b", label)
            found.append({"id": item_id.group(0) if item_id else "", "title": label, "done": match.group(1) != " "})
        return found

    def evidence(self) -> list[dict[str, str]]:
        rows = table(section(self.files.get("verification.md", ""), "Evidence") or "")
        return [row for row in rows if row.get("id", "").startswith("V-")]

    def item_status(self) -> dict[str, str]:
        """Per item: todo, implemented, verified, or failing."""
        evidence = self.evidence()
        status = {}
        for item in self.items():
            results = [row.get("result", "").lower() for row in evidence
                       if item["id"] and re.search(rf"\b{item['id']}\b", " ".join(row.values()))]
            if "fail" in results:
                status[item["id"] or item["title"]] = "failing"
            elif "pass" in results:
                status[item["id"] or item["title"]] = "verified"
            else:
                status[item["id"] or item["title"]] = "implemented" if item["done"] else "todo"
        return status

    def drift(self) -> list[str] | None:
        """Files changed outside this ledger since the recorded revision; None if not comparable."""
        top = git(self.path, "rev-parse", "--show-toplevel")
        if not top or not self.revision or self.revision == "unknown":
            return None
        if git(self.path, "cat-file", "-e", f"{self.revision}^{{commit}}") is None:
            return ["<recorded revision not found in this repository>"]
        changed = git(Path(top), "diff", "--name-only", self.revision, "HEAD")
        # Ledger edits, this one's or another's, are not code drift.
        return [name for name in (changed or "").splitlines()
                if not is_ledger(Path(top) / Path(name).parent / "README.md")]

    def updated(self) -> str:
        if git(self.path, "status", "--porcelain", "--", "."):
            return "uncommitted"
        return git(self.path, "log", "-1", "--format=%cs", "--", ".") or "untracked"

    def check(self) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        if "README.md" not in self.files:
            return ["missing README.md"], []
        if MARKER not in self.readme:
            errors.append(f"README.md: missing marker {MARKER}")
        if self.state in LEGACY_STATES:
            warnings.append(f"state '{self.state}' is legacy; use '{LEGACY_STATES[self.state]}'")
        elif self.state not in STATES:
            errors.append(f"README.md: State must be one of {', '.join(STATES)}; found {self.state!r}")
        if not self.revision:
            errors.append("README.md: missing 'Codebase revision' in the Status table")
        for prefix in ("Original task", "Next action"):
            if section(self.readme, prefix) is None:
                errors.append(f"README.md: missing '## {prefix}' section")
        if NOT_CAPTURED in self.readme:
            errors.append("README.md: original task not captured verbatim")
        for name, text in self.files.items():
            if re.search(r"\{\{[A-Z0-9_]+\}\}", text):
                errors.append(f"{name}: unresolved template token")
            limit = README_LIMIT if name == "README.md" else FILE_LIMIT
            if len(text.splitlines()) > limit:
                warnings.append(f"{name}: over {limit} lines; consolidate")

        changed = self.drift()
        if changed:
            shown = ", ".join(changed[:5]) + (" …" if len(changed) > 5 else "")
            warnings.append(f"{plural(len(changed), 'file')} changed since {self.revision[:12]}: {shown}; "
                            "refresh affected evidence, then run `sync`")

        for row in self.evidence():
            if row.get("result", "").lower() not in RESULTS:
                warnings.append(f"{row['id']}: Result should be one of {', '.join(RESULTS)}")
        statuses = self.item_status()
        unproven = [key for key, value in statuses.items() if value == "implemented"]
        if unproven:
            warnings.append(f"checked without passing evidence: {', '.join(unproven)}")
        if self.state == "complete":
            failing = [key for key, value in statuses.items() if value == "failing"]
            open_rows = [row["id"] for row in self.evidence() if row.get("result", "").lower() != "pass"]
            if failing or open_rows:
                warnings.append(f"complete with failing or open evidence ({', '.join(failing + open_rows)}); "
                                "record the gaps the user accepted")
        return errors, warnings


def find_ledgers(root: Path) -> list[Path]:
    """Walk the tree directly so gitignored and hidden ledgers are found too."""
    if (root / "README.md").is_file() and is_ledger(root / "README.md"):
        return [root.resolve()]
    found = []
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        if "README.md" in files and is_ledger(Path(current) / "README.md"):
            found.append(Path(current).resolve())
    return found


def is_ledger(readme: Path) -> bool:
    try:
        with readme.open(encoding="utf-8") as handle:
            return MARKER in handle.read(4096)
    except (OSError, UnicodeDecodeError):
        return False


# ---------- commands ----------

def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return slug[:63].rstrip("-") or "task"


def cmd_new(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    slug = slugify(args.slug or args.title)
    destination = root / slug
    if destination.exists():
        raise SystemExit(f"Refusing to overwrite existing ledger: {destination}")

    intent = ""
    if args.intent_file == "-":
        intent = sys.stdin.read().rstrip()
    elif args.intent_file:
        intent = Path(args.intent_file).read_text(encoding="utf-8").rstrip()
    if args.intent_file and not intent:
        raise SystemExit("Intent is empty")
    intent = intent or f"{NOT_CAPTURED}: replace this line with the user's original request verbatim."

    anchor = next(p for p in (root, *root.parents) if p.exists())
    branch = git(anchor, "branch", "--show-current")
    revision = git(anchor, "rev-parse", "HEAD")
    values = {
        "{{TITLE}}": args.title,
        "{{CREATED_AT}}": datetime.now().astimezone().isoformat(timespec="minutes"),
        "{{BRANCH}}": branch or "unknown",
        "{{REVISION}}": revision or "unknown",
        "{{INTENT}}": intent,
    }

    root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{slug}-", dir=root))
    try:
        for template in sorted(TEMPLATE_DIR.glob("*.md")):
            content = template.read_text(encoding="utf-8")
            for token, value in values.items():
                content = content.replace(token, value)
            (temporary / template.name).write_text(content, encoding="utf-8")
        temporary.rename(destination)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    print(destination)
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    ledgers = [Ledger(path) for path in find_ledgers(Path(args.root))]
    if not ledgers:
        print("No ledgers found.")
        return 0
    for ledger in ledgers:
        changed = ledger.drift()
        drift = "?" if changed is None else f"{len(changed)} changed"
        next_action = plain(section(ledger.readme, "Next action") or "") or "-"
        print(f"{ledger.state or '?':<13} {ledger.updated():<12} {drift:<11} {os.path.relpath(ledger.path)}")
        print(f"{'':<13} next: {next_action}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    paths = find_ledgers(Path(args.path))
    if not paths:
        raise SystemExit(f"No ledger found at {args.path}")
    failed = False
    for path in paths:
        errors, warnings = Ledger(path).check()
        if len(paths) > 1:
            print(f"== {os.path.relpath(path)}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        print(f"{'INVALID' if errors else 'VALID'}: {len(errors)} error(s), {len(warnings)} warning(s)")
        failed = failed or bool(errors)
    return 1 if failed else 0


def cmd_sync(args: argparse.Namespace) -> int:
    path = Path(args.path).resolve()
    readme = path / "README.md"
    if not readme.is_file():
        raise SystemExit(f"No README.md in {path}")
    revision = git(path, "rev-parse", "HEAD")
    if not revision:
        raise SystemExit("Not inside a git repository with commits")
    text = readme.read_text(encoding="utf-8")
    for label, value in (("Codebase revision", revision), ("Codebase branch", git(path, "branch", "--show-current"))):
        if not value:
            continue
        text, count = re.subn(rf"^(\|\s*{label}\s*\|)[^|\n]*(\|)", rf"\g<1> {value} \g<2>", text, flags=re.MULTILINE)
        if not count:
            raise SystemExit(f"README.md: no '{label}' row in the Status table")
    readme.write_text(text, encoding="utf-8")
    print(f"Synced to {revision[:12]}")
    return 0


# ---------- rendering ----------

def inline(text: str) -> str:
    out = []
    for i, part in enumerate(re.split(r"(`[^`]+`)", text)):
        if i % 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        part = html.escape(part, quote=False)
        part = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", part)
        part = re.sub(r"\[([^\]]+)\]\(((?:https?://|\.{0,2}/|[\w.-]+\.md)[^)\s]*)\)",
                      lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', part)
        out.append(part)
    return "".join(out)


def cell(text: str) -> str:
    if text.lower() in RESULTS:
        return f'<span class="result {text.lower()}">{text.lower()}</span>'
    return inline(text)


def markdown(text: str) -> str:
    """Render the small markdown subset ledgers use. Everything is escaped."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    out: list[str] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            block = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(block))}</code></pre>")
        elif stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            i -= 1
            body = [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            cells = "".join("<tr>" + "".join(f"<td>{cell(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="table"><table><thead><tr>{head}</tr></thead><tbody>{cells}</tbody></table></div>')
        elif re.match(r"^#{1,6} ", stripped):
            level = min(len(stripped) - len(stripped.lstrip("#")) + 1, 6)
            out.append(f"<h{level}>{inline(stripped.lstrip('#').strip())}</h{level}>")
        elif re.match(r"^\s*([-*]|\d+\.) ", line):
            items = []
            while i < len(lines) and (re.match(r"^\s*([-*]|\d+\.) ", lines[i]) or lines[i].startswith("  ")):
                current = lines[i]
                depth = "nested" if current.startswith("  ") else ""
                content = re.sub(r"^\s*([-*]|\d+\.) ", "", current).strip()
                box = re.match(r"^\[([ xX])\] (.*)", content)
                if box:
                    mark = "☑" if box.group(1) != " " else "☐"
                    content = f'<span class="box">{mark}</span> {inline(box.group(2))}'
                else:
                    content = inline(content)
                items.append(f'<li class="{depth}">{content}</li>')
                i += 1
            i -= 1
            out.append(f"<ul>{''.join(items)}</ul>")
        elif stripped.startswith(">"):
            out.append(f"<blockquote>{inline(stripped.lstrip('> '))}</blockquote>")
        elif stripped:
            para = [stripped]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^\s*([-*|>#]|\d+\.|```)", lines[i + 1]):
                i += 1
                para.append(lines[i].strip())
            out.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    return "\n".join(out)


def plural(n: int, word: str) -> str:
    return f"{n} {word}{'' if n == 1 else 's'}"


def plain(text: str) -> str:
    """First line of a markdown body as plain text."""
    line = next((l.strip() for l in text.splitlines() if l.strip()), "")
    return re.sub(r"\*\*|`|^[-*] ", "", line)


def is_empty(body: str | None) -> bool:
    return not body or body.strip() in {"None.", "- None recorded.", "- None adopted.", "Not yet consolidated."}


def render_ledger(ledger: Ledger, anchor: str) -> str:
    e = html.escape
    errors, warnings = ledger.check()
    changed = ledger.drift()
    statuses = ledger.item_status()
    counts = {key: list(statuses.values()).count(key) for key in ("verified", "implemented", "failing", "todo")}
    total = max(len(statuses), 1)
    bar = "".join(f'<span class="seg {key}" style="flex:{n}"></span>' for key, n in counts.items() if n)
    legend = " · ".join(f"{n} {key}" for key, n in counts.items() if n)

    findings = "".join(f'<li class="err"><span class="dot"></span>{e(x)}</li>' for x in errors) + \
        "".join(f'<li class="warn"><span class="dot"></span>{e(x)}</li>' for x in warnings)
    # Drift details live in the findings list; the header only confirms a clean sync.
    drift = '<span class="sync">in sync</span>' if changed == [] else ""

    def card(title: str, prefix: str, cls: str = "") -> str:
        body = section(ledger.readme, prefix)
        if is_empty(body):
            return ""
        return f'<section class="card {cls}"><h3>{e(title)}</h3>{markdown(body)}</section>'

    rows = []
    for item in ledger.items():
        status = statuses.get(item["id"] or item["title"], "todo")
        title = re.sub(rf"^{item['id']}\s*[—:-]*\s*", "", item["title"]) if item["id"] else item["title"]
        rows.append(f'<li class="item {status}"><span class="dot"></span><span class="id">{e(item["id"])}</span>'
                    f'<span class="title">{inline(title)}</span><span class="tag">{status}</span></li>')
    items = "".join(rows)
    evidence = section(ledger.files.get("verification.md", ""), "Evidence")
    evidence = markdown(evidence) if ledger.evidence() else ""
    progress = "" if not (items or evidence) else f"""
  <section class="card">
    <h3>Progress</h3>
    {f'<div class="bar">{bar}</div><p class="legend">{e(legend)}</p><ul class="items">{items}</ul>' if items else ''}
    {f'<h3 class="sub">Evidence</h3>{evidence}' if evidence else ''}
  </section>"""
    research = section(ledger.files.get("research.md", ""), "Findings") or ""
    findings_card = (f'<section class="card"><h3>Research findings</h3>{markdown(research)}</section>'
                     if table(research) else "")
    files = "".join(
        f'<details><summary>{e(name)}</summary><div class="md">{markdown(text)}</div></details>'
        for name, text in ledger.files.items())
    next_class = "next-action done" if ledger.state == "complete" else "next-action"

    return f"""
<article class="ledger" id="{anchor}">
  <header>
    <div class="eyebrow">{e(os.path.relpath(ledger.path))}</div>
    <h2>{e(ledger.title)}</h2>
    <div class="meta">
      <span class="pill state-{e(ledger.state)}">{e(ledger.state or 'unknown')}</span>
      <span>Updated {e(ledger.updated())}</span>
      <span><code>{e(ledger.status.get('Codebase branch', '?'))}</code> @ <code>{e(ledger.revision[:7] or '?')}</code></span>
      {drift}
    </div>
  </header>
  {f'<ul class="findings">{findings}</ul>' if findings else ''}
  {card('Next action', 'Next action', next_class)}
  <div class="grid">
    {card('Original task', 'Original task', 'quote')}
    {card('Current synthesis', 'Current synthesis')}
    {card('Open questions', 'Open questions')}
    {card('Decisions', 'Decisions')}
    {card('Amendments', 'Amendments', 'quote')}
  </div>
  {progress}
  {findings_card}
  <section class="files"><h3>Files</h3>{files}</section>
</article>"""


def render_index(ledgers: list[Ledger]) -> str:
    e = html.escape
    rows = []
    for i, ledger in enumerate(ledgers):
        errors, warnings = ledger.check()
        flag = ('<span class="flag err" title="errors"></span>' if errors else
                '<span class="flag warn" title="warnings"></span>' if warnings else '<span class="flag"></span>')
        next_action = plain(section(ledger.readme, "Next action") or "")
        rows.append(f'<a class="row" href="#l{i}"><span class="pill state-{e(ledger.state)}">{e(ledger.state or "?")}</span>'
                    f'<span class="name">{e(ledger.title)}</span><span class="todo-next">{e(next_action)}</span>'
                    f'{flag}<span class="when">{e(ledger.updated())}</span></a>')
    states = [l.state for l in ledgers]
    summary = " · ".join([plural(len(ledgers), "ledger")] +
                         [f"{states.count(s)} {s}" for s in STATES if states.count(s)])
    return f'<section class="index"><p class="summary">{e(summary)}</p>{"".join(rows)}</section>'


def cmd_render(args: argparse.Namespace) -> int:
    paths = find_ledgers(Path(args.path))
    if not paths:
        raise SystemExit(f"No ledger found at {args.path}")
    ledgers = [Ledger(path) for path in paths]
    title = "Development Ledgers" if len(ledgers) > 1 else ledgers[0].title
    body = "".join(render_ledger(l, f"l{i}") for i, l in enumerate(ledgers))
    page = VIEW_TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("{{GENERATED}}", datetime.now().astimezone().strftime("%Y-%m-%d %H:%M"))
    page = page.replace("{{TITLE}}", html.escape(title))
    page = page.replace("{{NAV}}", render_index(ledgers) if len(ledgers) > 1 else "").replace("{{BODY}}", body)
    out = Path(args.output) if args.output else Path(tempfile.gettempdir()) / "development-ledger.html"
    out.write_text(page, encoding="utf-8")
    print(out)
    if args.open:
        webbrowser.open(out.resolve().as_uri())
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="create a ledger from the templates")
    new.add_argument("title")
    new.add_argument("--root", default="docs/ledgers", help="parent directory (default: docs/ledgers)")
    new.add_argument("--slug", help="directory name; defaults to a slug of the title")
    new.add_argument("--intent-file", help="file with the user's request verbatim; '-' reads stdin")
    new.set_defaults(func=cmd_new)

    lst = sub.add_parser("list", help="find ledgers, including gitignored ones")
    lst.add_argument("root", nargs="?", default=".")
    lst.set_defaults(func=cmd_list)

    check = sub.add_parser("check", help="validate one ledger or every ledger under a path")
    check.add_argument("path", nargs="?", default=".")
    check.set_defaults(func=cmd_check)

    sync = sub.add_parser("sync", help="record current HEAD after refreshing evidence")
    sync.add_argument("path")
    sync.set_defaults(func=cmd_sync)

    render = sub.add_parser("render", help="write a read-only HTML view")
    render.add_argument("path", nargs="?", default=".")
    render.add_argument("-o", "--output", help="output file (default: temp dir)")
    render.add_argument("--open", action="store_true", help="open in the browser")
    render.set_defaults(func=cmd_render)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
