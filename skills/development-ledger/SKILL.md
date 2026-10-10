---
name: development-ledger
description: Create or resume an evidence-backed task ledger when multi-stage work needs durable context across sessions or handoffs.
metadata:
  version: "2.0.0"
---

# Development Ledger

Keep a compact record of the user's intent, current understanding, decisions, work, and verification. Use it to support the requested work; a ledger does not add a separate approval checkpoint.

All commands use `python3 <skill-dir>/scripts/ledger.py` (standard library only).

## Create or resume

To continue prior work, use the supplied path, or find ledgers (gitignored ones included):

```bash
ledger.py list
```

Read `README.md`, then only the file needed for the active work. Run `ledger.py check <ledger>`: it lists files changed since the recorded revision. Refresh the evidence those changes affect, then record the new baseline with `ledger.py sync <ledger>`. Do not sync without that review.

For a new task, use the repository's documentation location, otherwise `docs/ledgers/`. Pass the user's request verbatim:

```bash
ledger.py new "Task title" --root docs/ledgers --intent-file - <<'EOF'
<the user's request, verbatim>
EOF
```

## Record what matters

The template is a starting point. Delete sections and phase files the task does not need. Keep the original intent and current state easy to find.

- **README.md:** verbatim original task and separate amendments, Status table, current synthesis, adopted decisions, open questions, and next action.
- **research.md:** consolidated findings with evidence and unresolved conflicts. Mark each as fact, inference, or proposal. Keep raw transcripts out.
- **implementation.md:** work items `I-01`, `I-02`, … within the user's scope. `[x]` means implemented, not verified.
- **verification.md:** evidence rows `V-01`, … whose Item column names the `I-` ids they prove. Result is `pass`, `fail`, `blocked`, or `not-run`. Record what you observed, including failures.

State is one of `researching`, `implementing`, `verifying`, `blocked`, `complete`. For `blocked`, say what blocks it and who can unblock it in Next action.

Attach evidence to material claims: `path:line`, commands with observed output, or URLs with access dates.

Use practical ASD-STE100 principles: short active sentences, one instruction per sentence, consistent terms. Preserve user text, quotations, code, commands, logs, and identifiers verbatim. Prefer clarity over formal compliance.

## Continue and complete

Preserve what another agent needs to continue. Keep the README current and consolidate outdated notes; retain the reasons for decisions that still matter. Continue through implementation and verification when already requested; research-only work ends with the research deliverable.

When a decision blocks work, record its origin (user requirement or agent-derived choice), rationale, and what it actually blocks. On re-entry or after contradictory evidence, reassess agent-derived prerequisites. A failed check does not automatically block independent work or invalidate a hypothesis. Record changes in interpretation with their evidence; a user objection or an agent concession is not proof.

Mark the ledger `complete` when the requested scope is satisfied and required verification passed, or the user accepted the remaining gaps (record them under Gaps). Proposed items may stay unchecked in a research-only ledger.

Before a handoff or completion, run `ledger.py check <ledger>`. Fix errors; assess warnings in context. The check verifies structure and links between items and evidence; it cannot establish that the work is complete.

## View

To give the user a read-only overview of one ledger or every ledger under a path:

```bash
ledger.py render [path] --open
```

The page shows state, next action, open questions, item progress (todo, implemented, verified, failing), check findings, and every file. Edit the markdown, not the page; re-render to refresh.

Ledgers marked `development-ledger:v1` use an older layout. Read them as prose; the tools support v2 only.
