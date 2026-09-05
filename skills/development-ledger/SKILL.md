---
name: development-ledger
description: Create or resume an evidence-backed task ledger when multi-stage work needs durable context across sessions or handoffs.
metadata:
  version: "1.1.0"
---

# Development Ledger

Keep a compact record of the user's intent, current understanding, decisions, work, and verification. Use it to support the requested work; a ledger does not add a separate approval checkpoint.

## Create or resume

For a new task, create a task-specific ledger. Search existing ledgers only when continuing prior work; use the supplied path when available:

```bash
rg -l '<!-- development-ledger:v(1|2) -->' .
```

Resume the existing layout, including v1. Read `README.md`, then only the file needed for the active work. Compare the recorded revision with current `HEAD` and refresh affected evidence.

Use the repository's established documentation location, otherwise `docs/ledgers/<task-slug>/`:

```bash
python3 <skill-dir>/scripts/create_ledger.py \
  --root docs/ledgers \
  --title "Task title" \
  --repo . \
  --intent-file /path/to/verbatim-request.txt
```

## Record what matters

Adapt the detail to the task. The template is a starting point; omit irrelevant sections or phase files rather than filling them for completeness. Keep the original intent and current state easy to find.

- **README.md:** verbatim original task and separate amendments, current synthesis, adopted decisions, open questions, revision watermarks, and next action.
- **research.md:** consolidated findings with evidence and unresolved conflicts. Distinguish facts, inferences, and proposals; keep raw transcripts out of the ledger.
- **implementation.md:** planned and completed work within the user's scope. `[x]` means implemented, not verified.
- **verification.md:** observed checks, results, failures, and remaining gaps. Reference this proof from completion claims.

Attach evidence to material claims: `path:line`, commands with observed output, or direct URLs with access dates. Add an appendix only when an inventory would obscure the findings.

Use practical ASD-STE100 principles: short active sentences, one instruction per sentence, and consistent terms. Preserve user text, quotations, code, commands, logs, and identifiers verbatim. Prefer clarity over formal compliance; do not claim ASD-STE100 certification.

## Continue and complete

Preserve what another agent needs to continue. Keep the README current and consolidate outdated notes as understanding changes; retain the reasons for decisions that still matter. Continue through implementation and verification when already requested; research-only work ends with the research deliverable.

Mark the ledger `complete` when the requested scope is satisfied and required verification passed, or the user accepted the remaining gaps. Proposed implementation may remain unchecked in a completed research-only ledger.

Validate the final ledger or a handoff with:

```bash
python3 <skill-dir>/scripts/validate_ledger.py path/to/ledger --repo .
```

Fix errors; assess warnings in context. The validator checks structure and flags possible gaps; it cannot establish that the work is complete.
