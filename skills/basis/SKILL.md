---
name: basis
description: "Design or repair software behavior with clear responsibilities and minimal machinery. Use when asked for a holistic fix, a behavior matrix, separation of concerns, a capability basis, reduced feature overlap or collinearity, or simplification of growing per-case rules. Applies to product behavior and architecture, not merely cosmetic cleanup."
---

# Basis

Cover the required behavior with a small set of cohesive responsibilities that compose. Reduce duplicate authority without erasing meaningful differences.

Prefer straightforward code for current requirements. A complete result may be one direct correction with no new abstraction.

Two views work together:

- **Behavior matrix:** what must happen across meaningful combinations of states, events, actors, and contexts.
- **Capability basis:** which responsibilities and contracts explain those outcomes without a separate mechanism for every case.

Cases discover and challenge the model; they are not the architecture. The linear-algebra analogy concerns non-redundancy and coverage. It does not require literal orthogonality, complete isolation, or mathematical scoring of code.

## Establish the actual problem

Start from the user's intended outcome and constraints. Inspect existing behavior, owners, interfaces, and prior decisions before proposing new machinery. Trace representative paths from input through state changes to the user's experience. Distinguish observed behavior, intended behavior, and assumptions.

Keep the work in the requested mode: an audit produces findings; a design produces a proposal; an implementation request proceeds through verification.

“Holistic” widens the investigation to relevant producers and consumers, not to an unrelated rewrite. Start with the affected path and its actual owner. Expand only when evidence connects another path to the requirement or defect, or the user asks for a wider review. Stop when the affected contract and required cases are explained.

## Map behavior before adding rules

Identify dimensions that actually change the outcome. Examples include lifecycle, event kind, source/recipient relation, scope, authority, delivery timing, and live versus restored state. Derive the dimensions from the system; do not install this list as its schema.

Use a few representative cases and counterexamples to expose gaps. Build a matrix only when interacting dimensions make it useful; do not enumerate a Cartesian product by default. Exclude unreachable combinations using their actual invariant. Group cases with the same contract and outcome while retaining distinctions that change authority, persistence, or user experience.

Independent owners can still have ordering and eligibility constraints. Do not infer that every combination or reversed sequence is valid merely because different modules own its facts; label unsupported combinations as unknown.

A useful compact row is:

| State/context + event | Expected transition and user outcome | Current behavior/evidence | Owning contract |
| --- | --- | --- | --- |

Examine sequences as well as snapshots. Where relevant, cover late results, repeated delivery, interruption, reconnect, concurrent actors, and an action taken after the underlying state changed. Unknown expected behavior stays an explicit question or labeled proposal, not an invented requirement.

For UI work, compare with the actual surrounding components and interaction patterns. Define what users see, can inspect, and can act on. A quiet presentation must not silently discard information the product promises to preserve.

## Find the basis in existing ownership

For each proposed responsibility, identify its authoritative fact or decision, inputs, outputs, lifecycle, and consumers. The test for one responsibility versus two: two things are one responsibility when they always change together for the same reason, and two when either can change alone. A responsibility is a reasoning boundary, not automatically a new module, layer, interface, or state machine. Reuse the current owner where it already fits.

Check both sides:

- **Overlap:** do several paths independently decide the same thing, own competing copies, or reimplement the same lifecycle? Consolidate that decision at its proper owner.
- **Coverage:** can the responsibilities compose to produce every required outcome? Trace the required cases through them. A model that omits awkward cases is incomplete even if it is elegant.

Multiple projections of one fact are legitimate. Shared data, similar appearance, or similar code does not by itself establish duplicate responsibility. Likewise, delivery, visibility, acknowledgement, and resolution may require distinct state even when they concern the same event.

Generalize only around a demonstrated common responsibility or capability gap. Weigh what an abstraction removes or enables against added indirection, coordination, state, and migration cost. Similar syntax or hypothetical future reuse is insufficient; small local repetition can be clearer than coupling distinct policies. Separate caller lifecycles can still share stateless decoding. Keep domain differences explicit without automatically adding adapter layers. Reject a universal manager, generic event store, or flag-heavy interface that merely hides all the previous special cases.

## Make the repair coherent

Prefer a direct correction or change to the existing contract when it fully meets the requirement. Choose the least complex complete repair across affected consumers, not merely the fewest changed lines. Any restructuring names the demonstrated gap it closes.

Prefer a fact or decision from its authoritative source over heuristics that reconstruct it from titles, prose, or incidental UI state. Similar labels do not prove identical entities or completed work. When evidence is absent, preserve that uncertainty.

Update affected consumers together. Retire superseded paths when callers and compatibility obligations permit; follow the project's migration rules. Do not leave competing authorities as a permanent fallback. Preserve distinct scope, permissions, provenance, and acknowledgement meanings during consolidation.

When sharing a reader or predicate, preserve each caller's selected entities, count units, and eligibility rules. Replacing a scoped view with a query over every record can make its count agree while silently changing its meaning.

## Challenge the result

Replay the meaningful cases against the proposed composition. Seek a counterexample within the affected contract. Repeated feature-name exceptions can reveal a missing dimension or wrong owner; an ordinary domain condition can be the simplest correct implementation.

Verify at the level of the claim: logic and transition checks for contracts, persistence checks for durable behavior, rendered inspection for UI, live evidence for live incidents. Follow local test rules. Passing one example does not establish coverage; a mockup does not establish production behavior.

Report briefly: the solution, material evidence, any ownership changes, and what was verified or remains uncertain. Use a small matrix or ownership table only when it clarifies the decision. Stop when the requested behavior and appropriate checks are satisfied.

For examples of useful distinctions and over-generalization traps, read [examples.md](references/examples.md).
