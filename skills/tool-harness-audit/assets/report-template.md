# Tool Harness Audit Report

**Harness:** `<name>`  
**Audit date:** `<YYYY-MM-DD>`  
**Auditor:** `<name/agent>`  
**Scope:** `<full harness / integration / tool family / workflows>`  
**Repository revision:** `<commit>`  
**Evidence window:** `<dates>`  
**Models/providers tested:** `<list>`  
**Execution contexts tested:** `<chat / automations / memory / other>`  
**Strict/constrained modes tested:** `<off / provider modes / allowlisted tools>`  
**Security/privacy review:** `<separate audit complete / planned / required / out of scope>`  
**Evidence ledger:** `<path or URL>`

> Formatting rule: use labeled sections and bullet records by default. Markdown tables are optional, never required. For large machine-generated inventories, attach CSV or JSONL and summarize the important coverage facts here.

## Executive summary

- **Overall assessment:** `<usable / degraded / unsafe / unverified>`
- **Highest-risk finding:** `<one sentence>`
- **Highest-leverage fix:** `<one sentence>`
- **Agentic verification:** `<complete / partial / absent>`
- **Coverage limitation:** `<one sentence>`

## Scope and evidence

### Sources reviewed

- `<tool manifest or MCP schema>`
- `<source paths>`
- `<trace project/query and window>`
- `<tests/evals>`
- `<incidents or agent reports>`

### Testing constraints

- `<read-only policy, unavailable systems, unsafe writes not performed, etc.>`

### Sampling rationale

- **Audit budget:** `<time / calls / tool count / environments>`
- **Stopping rule:** `<coverage/threshold condition>`
- **Usage window/source:** `<trace project and dates>`
- **Usage coverage:** `<tools/groups covering N% of calls>`
- **Execution contexts:** `<chat / automations / memory / other>`
- **Contract cohorts:** `<schema path + transformations + provider + validator + formatter + risk class>`
- **Reliability sample:** `<failed traces, incidents, agent reports, risky writes>`
- **Long-tail sample:** `<random or systematic low-frequency coverage>`
- **Known bias:** `<missing telemetry or unrepresented workflows>`

## Contract cohort coverage

Repeat this block for each cohort.

### Cohort: `<name>`

- **Members/count:** `<complete list, attached inventory ref, and N>`
- **Shared contract:** `<schema/adapter/validator/formatter/risk>`
- **Representatives tested:** `<tools>`
- **Known exceptions checked:** `<exceptions>`
- **Coverage status:** `<Directly tested / Automatically checked / Cohort-covered / Intentionally sampled out / Untestable / Unavailable / Not applicable>`
- **Evidence:** `<ref>`

## Workflow coverage

Repeat this block for each workflow.

### Workflow: `<name>`

- **Tools/path:** `<tools>`
- **Predefined acceptance criteria:** `<criteria set before testing>`
- **Outcome:** `<Pass / Degraded / Fail / Not tested>`
- **Coverage status:** `<status>`
- **Evidence confidence:** `<High / Medium / Low>`
- **Tool calls:** `<N>`
- **Output size:** `<tokens/bytes>`
- **Evidence:** `<refs>`
- **Notes:** `<notes>`

Minimum workflow set where applicable:

- Search → inspect
- No-results recovery
- Pagination / large result
- Read → preview → mutate → verify
- Failure → recovery

## Findings

List findings in priority order. Repeat the detailed block below; do not require a summary table.

### Finding `<N>` — `<title>`

- **Affected workflow/tool:** `<...>`
- **Principle:** `<...>`
- **Responsible layer:** `<confirmed or suspected layer>`
- **Observed outcome:** `<Pass / Degraded / Fail / Not tested>`
- **Coverage status:** `<Directly tested / Automatically checked / Cohort-covered / Intentionally sampled out / Untestable / Unavailable / Not applicable>`
- **Evidence confidence:** `<High / Medium / Low>`
- **Evidence type:** `<Runtime-confirmed / Deterministic-code/test-confirmed / Strongly implicated / Inconclusive / Hypothesis>`
- **Severity:** `<High / Medium / Low>`

**Evidence**

```text
Exact call, error, trace IDs, source paths/lines, and result excerpts.
```

**Impact**

`<How this changes agent behavior or user outcome.>`

**Fix**

`<Smallest durable change; note cross-cutting applicability.>`

**Verification**

- `<deterministic schema/unit/contract test>`
- `<agentic regression task>`
- `<negative or repeated-run control>`

## Cross-cutting fixes

Repeat for each fix.

### Cross-cutting fix: `<title>`

- **Priority:** `<P0 / P1 / P2>`
- **Findings addressed:** `<finding refs>`
- **Responsible owner/boundary:** `<layer/team>`
- **Required change:** `<fix>`
- **Verification gate:** `<test/eval>`

## Tool-specific fixes

Repeat for each fix.

### Tool-specific fix: `<tool>`

- **Priority:** `<P0 / P1 / P2>`
- **Required change:** `<fix>`
- **Evidence:** `<ref>`
- **Verification:** `<test>`

## Instrumentation and evidence gaps

Repeat for each gap.

### Evidence gap: `<title>`

- **Missing evidence:** `<gap>`
- **Why it matters:** `<what cannot be distinguished>`
- **Required instrumentation/experiment:** `<discriminating evidence>`

Do not list an unverified causal theory as a product fix. State the discriminating evidence required.

## Security/privacy audit boundary

This ergonomics audit does **not** establish that the harness is secure or privacy-safe.

- **Separate review status:** `<complete / planned / required / out of scope>`
- **Obvious hazards surfaced here:** `<authorization, tenant scope, secrets, untrusted content, trace data, destructive actions>`
- **Required handoff:** `<owner / audit / threat model / remediation>`

## Unrelated reliability incidents

Keep backend/integration incidents that surfaced during the audit separate from harness ergonomics findings.

Repeat for each incident.

### Incident: `<title>`

- **Layer:** `<sync / database / upstream / other>`
- **Evidence:** `<ref>`
- **Suggested owner/action:** `<action>`

## Positive patterns to standardize

Repeat for each pattern.

### Positive pattern: `<tool or pattern>`

- **Why it works:** `<reason>`
- **Where to reuse it:** `<tools/cohorts>`
- **Protection:** `<regression or standard>`

## Evaluation environment

- **Model/provider and adapter versions:** `<...>`
- **Tool-catalog/schema fingerprints:** `<...>`
- **Skill/system-prompt version:** `<...>`
- **State:** `<controlled fixture / live mutable environment>`
- **Runs and sampling settings:** `<N / temperature / seed where supported>`
- **Predefined acceptance thresholds:** `<...>`
- **Distribution/confidence reporting:** `<...>`

## Regression eval candidates

Repeat for each distinct failure cohort or materially different intent/risk case.

### Eval case: `<name>`

- **Failure cohort:** `<cohort/finding refs>`
- **User intent:** `<intent>`
- **Available tools/discovery state:** `<...>`
- **Expected tool path:** `<path>`
- **Valid argument constraints:** `<constraints>`
- **Expected result properties:** `<assertions>`
- **Forbidden behavior:** `<dummy values, wrong tool, unsafe write, etc.>`
- **Injected failure/recovery expectation:** `<...>`
- **Acceptance threshold:** `<...>`

## Recommended sequence

1. `<ownership/schema safety>`
2. `<output bounds/results>`
3. `<errors/recovery>`
4. `<observability>`
5. `<agentic eval gate>`

## Sources

- `<source name — path/URL/trace>`
- `<source name — path/URL/trace>`

## Appendix: generated baseline catalog

Include every tool where a manifest/source inventory is available. Record uncataloged populations and why they are missing.

For large harnesses, prefer an attached machine-generated CSV or JSONL artifact. Otherwise repeat this compact record:

### Tool: `<name>`

- **Declared intent:** `<intent>`
- **Side-effect class:** `<read / write / destructive / open-world>`
- **Contract cohort:** `<cohort>`
- **Coverage status:** `<status>`
- **Representative/evidence:** `<tool/ref>`
- **Source:** `<path>`

## Appendix: detailed sampled inventory

Include sampled tools, cohort representatives, consequential/security-sensitive tools, and known exceptions—not every tool by default.

Repeat this record:

### Detailed tool: `<name>`

- **Intent:** `<intent>`
- **Description/prerequisites:** `<summary>`
- **Inputs/defaults/conditional rules:** `<summary>`
- **Output/continuation:** `<summary>`
- **Side effects/authorization:** `<summary>`
- **Related/overlapping tools:** `<tools>`
- **Implementation/schema source:** `<path>`
