# Research phase

Use `02-research.md` for evidence gathering. Keep surface observations distinct from consolidated findings.

## Research pass

For each pass, record:

- Question or scope
- Sources inspected
- Surface observations
- Negative evidence or paths ruled out
- Follow-up questions

For code, cite `path:line` and record relevant runtime commands or output. For web sources, use direct URLs and access dates. For user-provided material, identify the message or artifact.

## Finding contract

Promote useful observations into a finding with:

- Stable ID such as `F-01`
- Type: `fact` or `inference`
- Claim
- Evidence
- Implication for the task
- Confidence: `high`, `medium`, or `low`
- Last checked timestamp or code revision

Proposals belong in synthesis until adopted. Adopted decisions belong in `05-decisions.md`.

## Optional fan-out

Use subagents only when available, authorized by the active environment, and the work divides into independent scopes. Give each worker:

- Outcome
- Scope and exclusions
- Evidence requirements
- Expected concise return format

Require workers to return findings, evidence, uncertainties, and conflicts. The primary agent consolidates their output; never paste raw worker transcripts into the ledger.
