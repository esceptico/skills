# Tool Harness Audit

Use the sections relevant to the requested scope. Omit empty sections; attach large inventories or logs rather than expanding the main report.

## Assessment

- **Scope and revision:** `<harness, tools/workflows, revision>`
- **Result:** `<main conclusion and most useful next action>`
- **Evidence:** `<source review, deterministic checks, agentic runs>`
- **Limitations:** `<untested paths and what the evidence cannot establish>`

## Findings

Repeat for each material finding, in priority order.

### `<severity> — <title>`

- **Affected tool/workflow:** `<scope>`
- **Impact:** `<observable failure or cost>`
- **Evidence and confidence:** `<source location, call/result, test or trace; High/Medium/Low>`
- **Cause:** `<confirmed layer or explicitly labeled hypothesis>`
- **Fix:** `<smallest durable change>`
- **Verification:** `<check that would establish the fix; observed result if executed>`

## Coverage

For focused reviews, list the inspected and untested paths. For broad reviews, include cohort membership/counts, reviewed representatives, known exceptions, and sampling rationale.

- **Tool/cohort/workflow:** `<name and members or inventory reference>`
- **Coverage:** `<directly tested / statically checked / cohort-inferred / sampled out / unavailable>`
- **Workflow outcome:** `<Pass / Degraded / Fail / Not tested>`
- **Evidence:** `<reference and limits of generalization>`

## Agentic evaluation

Include when performed; otherwise state the gap in coverage.

- **Environment:** `<model/version, provider/mode, schema revision, fixture/live state>`
- **Task and acceptance criteria:** `<intent and expected result>`
- **Results:** `<successes/attempts, relevant costs, representative failures>`
- **Limits:** `<variance, missing environments, unsupported reliability claims>`

## Next actions

List prioritized fixes and unresolved evidence needs. Separate harness defects from unrelated backend incidents. Note concrete security hazards without claiming security assurance.

## Sources

- `<path, URL, test result, or trace>`
