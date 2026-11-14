---
name: basis
description: "Design or repair software behavior with clear responsibilities and minimal machinery. Use when the same kind of bug is being fixed a second time, when a fix would add another flag, condition, or special case, when two places disagree about the same fact (two counts, two statuses, two copies of a rule), or when asked for a holistic fix, a behavior matrix, separation of concerns, a capability basis, reduced feature overlap or collinearity, or simplification of growing per-case rules. Applies to product behavior and architecture, not cosmetic cleanup."
---

# Basis

Cover the required behavior with a small set of responsibilities that compose. Give each fact one owner. Keep differences that change the outcome.

Write direct code for the current requirements. A complete result can be one correction with no new abstraction.

The skill uses two views of the system.

- **Behavior matrix.** What must happen for each combination of state, event, actor, and context that changes the outcome.
- **Capability basis.** The responsibilities and contracts that produce those outcomes without a separate mechanism for each case.

Cases find and test the model. They are not the architecture. The name comes from linear algebra, where a basis covers a space with no redundant vector. Here it means full coverage with no duplicate owner. It does not mean strict isolation or a numeric score for code.

## The two tests

Each judgment in this skill uses one of two tests. Apply them in this order.

**Responsibility test.** Are these one concept or two? Two things are one responsibility when they always change together for the same reason. They are two when either can change alone. This test decides what to merge and what to keep apart. Code that looks alike but changes for different reasons stays separate. Code that looks different but decides the same fact gets one owner.

**Structure test.** Does a responsibility need its own code? A responsibility is a way to reason about the system. It becomes a separate function, module, interface, or state machine only when one of these is true today:

- More than one place decides the same fact.
- Two or more existing callers need it.
- Its lifecycle differs from the code around it. For example, it must persist, restart, or be replaced separately.

When none is true, the responsibility stays in its current owner as a named branch or function. Possible future reuse does not count.

Two more rules follow from the tests.

- **Matrix or list.** Write a matrix when the outcome depends on a combination of two or more dimensions. With one dimension, write a short list of cases.
- **Widen or stop.** Check the siblings of each cell you change. The sibling rule is in the mapping section. Go beyond siblings only when evidence connects another path to the requirement or the defect, or when the user asks for a wider review.

## Establish the problem

Start from the outcome the user wants and the user's constraints. Read the existing behavior, owners, interfaces, and earlier decisions before you propose new code. Trace a few paths from input, through state changes, to what the user sees. Label each statement as observed behavior, intended behavior, or assumption.

Stay in the mode the user asked for. An audit produces findings. A design produces a proposal. An implementation request ends with verification.

"Holistic" means you also read the producers and consumers of the affected path. It does not mean you rewrite unrelated code. Start with the affected path and its owner.

## Map behavior before adding rules

Find the dimensions that change the outcome. Common ones are lifecycle, event kind, sender and recipient, scope, authority, delivery timing, and live or restored state. Take the dimensions from the system. Do not copy this list as a schema.

Use a few cases and counterexamples to find gaps. Do not list every combination by default. Group cases that have the same contract and the same outcome. Keep cases apart when they differ in authority, persistence, or what the user sees.

Remove an unreachable combination by naming the invariant that prevents it. A combination that a user or caller can still request is reachable. Give it a row whose outcome is a rejection by that invariant.

Before you add a guard for a state, ask if the system may be in that state. If it may, handle the state in the code that broke on it. If the state must never exist, a guard hides the defect. Find the code that produced the state and fix it there.

Owners that are independent can still constrain each other's order and eligibility. Different modules owning the facts does not make every combination or every order valid. Mark a combination as unknown when nothing shows the system supports it.

Use this row format:

| State/context + event | Expected transition and user outcome | Current behavior/evidence | Owning contract |
| --- | --- | --- | --- |

Check sequences as well as single states. Where they apply, cover late results, repeated delivery, interruption, reconnect, concurrent actors, and an action taken after the state changed. When you do not know the expected behavior, write it as a question or a labeled proposal. Do not invent a requirement.

**Fill the sibling cells.** When a fix changes one cell, check its siblings. Siblings are the same event in the other states, the same state with the other events, and the other callers of the same owner. Fix the siblings that fail the same way, in the same change, through the same owner. List the siblings that you checked and found correct.

**Name the cell before you add a modifier.** Before you add a flag, condition, or special case, name the matrix cell that needs it. If no cell fits, a dimension is missing. Add the dimension, not the modifier.

For UI work, compare with the components and interaction patterns around the change. State what users see, what they can inspect, and what they can act on.

## Find the basis in existing ownership

For each responsibility, name its authoritative fact or decision, its inputs, its outputs, its lifecycle, and its consumers. Use the current owner where it fits.

Check two things.

- **Overlap.** Do several paths decide the same thing, keep competing copies, or implement the same lifecycle again? Move that decision to one owner.
- **Coverage.** Do the responsibilities together produce each required outcome? Trace the required cases through them. A model that leaves out the hard cases is incomplete.

A step in a sequence is not an owner. Modules named after phases, such as load, validate, and save, each repeat the same domain rule. Give the rule to the module that holds that domain knowledge.

One fact can have several projections. Shared data, similar appearance, and similar code do not prove a duplicate responsibility. The responsibility test does.

Add an abstraction only where the structure test passes. Compare what the abstraction removes with what it adds in indirection, coordination, state, and migration cost. Keep domain differences visible in the code, and do not add an adapter layer for each one. Do not build a universal manager, a generic event store, or an interface with many flags. Each of these hides the old special cases and keeps them.

## Make the repair coherent

Use a direct correction, or a change to the existing contract, when it meets the requirement in full. Choose the simplest complete repair across the affected consumers. That is not always the repair with the fewest changed lines. For each restructuring, name the structure-test condition it meets.

Read a fact or decision from its authoritative source. Do not rebuild it from titles, prose, or incidental UI state. When you have no evidence, say that the fact is unknown.

Update the affected consumers in the same change. Remove a replaced path when its callers and compatibility obligations allow it, and follow the project's migration rules. Do not keep two authorities with one as a permanent fallback. When you merge, each caller keeps its scope, permissions, provenance, and acknowledgement meaning. A shared rule keeps each caller's selected entities and count units.

When the code branches on the same dimensions in more than one place, write the matrix into the code as a table, a state machine, or a tagged union. A new case is then a new row, not a new branch, and a type or a test can check that each row has an outcome.

After you move a decision to one owner, add a guard that fails when a second copy appears. Use a lint rule, a type, or a test. If no guard is practical, say so in the report.

## Challenge the result

Replay the cases and their siblings against the proposed design. Look for a counterexample inside the affected contract. Repeated exceptions that name a feature can show a missing dimension or a wrong owner. An ordinary domain condition can also be the simplest correct code.

Verify at the level of the claim. Use logic and transition checks for a contract, persistence checks for durable behavior, rendered inspection for UI, and live evidence for a live incident. Follow the local test rules. One passing example does not prove coverage. A mockup does not prove production behavior.

## Report

End each use of this skill with these three lines, even for a small fix. They show that you did the work.

- **Dimensions.** The dimensions that change the outcome, or "one dimension, no matrix".
- **Owners.** Each fact or decision involved and its one owner. Mark each owner that changed.
- **Cases replayed.** Each case and sibling, marked verified, failing, or unknown, with how you checked it.

Then state the solution and what is still uncertain. Add a matrix or an ownership table only when it makes the decision clearer. Stop when the requested behavior works and the checks pass.

Read [examples.md](references/examples.md) before the first use in a session. It has a worked example for each test and for the common ways to generalize too far.
