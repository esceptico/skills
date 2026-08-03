---
name: development-ledger
description: Create and maintain a compact, evidence-backed development ledger from initial task through research, implementation planning, and verification. Use when Codex needs to research or scope a codebase or technical idea, preserve context across compaction or sessions, consolidate code/web/subagent findings, derive an implementation checklist, distinguish implemented work from verified behavior, or resume an existing multi-stage investigation.
---

# Development Ledger

Keep one compact task directory that preserves intent, evidence, current understanding, planned work, and proof.

## Default layout

```text
<ledger>/
├── README.md          # verbatim task, watermarks, synthesis, decisions, questions, next action
├── research.md        # surface research, consolidated findings, conflicts
├── implementation.md  # proposed and completed work
└── verification.md    # observed proof, failures, gaps
```

Create an appendix only when a large inventory or evidence table would make `research.md` hard to scan.

## Rules

- Preserve the user's original task verbatim in `README.md`; record later amendments separately.
- Separate facts, inferences, proposals, and adopted decisions.
- Attach evidence to material claims: `path:line`, commands plus observed output, or direct URLs with access dates.
- Keep `README.md` current and concise; it is the re-entry point after compaction or handoff.
- Consolidate repeated/raw research into durable findings instead of accumulating transcripts.
- Treat `[x]` in `implementation.md` as implemented, not verified.
- Put observed proof only in `verification.md`.
- Mark the ledger `complete` only when required verification passed or accepted gaps are explicit.
- Let state describe the user-requested scope. A research-only task may be complete while its proposed implementation remains unchecked.
- Do not implement unless the user requested implementation.

## Create or resume

If the user asks for a new ledger, a new task, or to start from scratch, create a new task-specific ledger immediately. Do not search, reuse, or mention unrelated ledgers.

Search for an existing ledger only when the user asks to continue, resume, or update prior work:

```bash
rg -l '<!-- development-ledger:v(1|2) -->' .
```

Continue a matching v1 ledger in its existing layout. Do not migrate or reshape it unless the user asks.

Create a ledger under the repository's established documentation location, otherwise default to `docs/ledgers/<task-slug>/`:

```bash
python3 <skill-dir>/scripts/create_ledger.py \
  --root docs/ledgers \
  --title "Task title" \
  --repo . \
  --intent-file /path/to/verbatim-request.txt
```

## Work

1. Record scope and surface observations in `research.md`.
2. Promote supported claims into consolidated findings; move unresolved uncertainty to `README.md`.
3. Rewrite the current synthesis in `README.md` when understanding changes.
4. Record adopted decisions separately from proposals.
5. Add an implementation checklist only when useful for the requested outcome.
6. Record commands, observations, failures, and remaining gaps in `verification.md`.
7. Update README watermarks and next action last.

When fan-out is authorized and useful, give each subagent an independent scope plus evidence requirements. Consolidate their findings; never paste raw worker transcripts.

## Re-enter

Read `README.md`, then only the file for the active phase. Compare the recorded code revision with current `HEAD` and refresh affected evidence when they differ.

## Validate

```bash
python3 <skill-dir>/scripts/validate_ledger.py path/to/ledger --repo .
```

Fix errors. Review warnings for revision drift, excessive size, placeholders, checked work without proof, or unsupported completion claims.
