# Maintenance and re-entry

## Watermarks

Keep these current in `README.md`:

- Ledger phase and status
- Last updated
- Last consolidated
- Codebase branch and revision
- Sources checked through
- Next action

Timestamps show age; revisions detect code drift. When current `HEAD` differs from the recorded revision, identify which findings and conclusions depend on changed code before relying on them.

## Status values

- `researching`
- `needs-input`
- `ready-for-decision`
- `ready-for-implementation`
- `implementing`
- `verifying`
- `blocked`
- `complete`

## Size control

- Keep `README.md` under 120 lines.
- Consolidate lifecycle files when they exceed 250 lines.
- Treat a lifecycle file above 500 lines as invalid until it is compressed or supporting evidence is moved to a linked appendix.
- Preserve the standard files even when an appendix exists.

## Handoff

Before handoff, validate the ledger, update watermarks, and state the exact next action. A fresh agent should regain the task by reading `README.md`, `01-intent.md`, and the active lifecycle file.
