---
name: development-ledger
description: Create and maintain a persistent, evidence-backed development ledger from initial task through research, synthesis, decisions, implementation planning, and verification. Use when Codex needs to research or scope a codebase or technical idea, preserve context across compaction or sessions, consolidate web/code/subagent findings, track open questions and decisions, derive an implementation checklist, distinguish implemented work from verified behavior, or resume an existing multi-stage development investigation.
---

# Development Ledger

Maintain one task directory whose files move from abstract context to implementation detail. Treat the ledger as the current reasoning record, not as a substitute for source code, tests, or version control.

## Core rules

- Preserve the user's original task prose verbatim in `01-intent.md`; record later amendments separately.
- Separate `fact`, `inference`, `proposal`, and `decision`. Never present one as another.
- Attach evidence to every material fact. Use repository paths and line numbers, commands and observed output, or direct source URLs with access dates.
- Keep `README.md` compact and current. It is the re-entry point after compaction or handoff.
- Consolidate research after each meaningful pass. Do not let the inbox become the durable record.
- Treat `[x]` in `06-implementation.md` as implemented, not verified.
- Put verification commands, observations, failures, and gaps only in `07-verification.md`.
- Mark the ledger `complete` only when required verification has observed evidence or the user explicitly accepts documented gaps.
- Do not implement merely because a ledger exists. Respect whether the user asked for research, planning, implementation, or verification.

## Locate or create the ledger

1. Search repository conventions and existing ledgers first:

   ```bash
   rg -l '<!-- development-ledger:v1 -->' .
   ```

2. Reuse the ledger that matches the task. Do not create a competing artifact.
3. If none exists, default to `docs/ledgers/<task-slug>/` unless the user or repository specifies another location.
4. Initialize from the bundled templates:

   ```bash
   python3 <skill-dir>/scripts/create_ledger.py \
     --root docs/ledgers \
     --title "Task title" \
     --repo .
   ```

5. Immediately replace the intent placeholder with the user's exact prose and update the status snapshot.

## Work by lifecycle phase

Read only the reference needed for the current phase:

- Research or optional fan-out: [references/research.md](references/research.md)
- Consolidating findings and synthesis: [references/consolidation.md](references/consolidation.md)
- Producing or updating implementation work: [references/implementation.md](references/implementation.md)
- Verifying observed behavior: [references/verification.md](references/verification.md)
- Re-entry, watermarks, staleness, and size control: [references/maintenance.md](references/maintenance.md)

Update files in this order when knowledge changes:

1. `01-intent.md` only for new user amendments, constraints, or clarified success conditions.
2. `02-research.md` with surface observations and evidence.
3. `03-questions.md` with newly opened or resolved questions.
4. `04-synthesis.md` with the current consolidated model; rewrite stale conclusions.
5. `05-decisions.md` only for adopted decisions and superseded history.
6. `06-implementation.md` with planned or completed changes.
7. `07-verification.md` with observed proof and remaining gaps.
8. `README.md` last, so its summary and watermarks reflect the detailed files.

## Re-enter after compaction or handoff

1. Read `README.md`.
2. Read `01-intent.md` and the file for the active lifecycle phase.
3. Check the recorded codebase revision against current `HEAD` and identify time-sensitive sources.
4. Read other lifecycle files only when the summary links to unresolved context.
5. Refresh stale evidence before relying on affected conclusions.

## Validate

Run the validator after creation, consolidation, implementation updates, and before handoff:

```bash
python3 <skill-dir>/scripts/validate_ledger.py path/to/ledger --repo .
```

Fix errors. Treat warnings as explicit review items; do not silently ignore revision drift, oversized files, placeholders, or a `complete` ledger without verification evidence.
