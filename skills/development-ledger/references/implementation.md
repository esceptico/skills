# Implementation phase

Use `06-implementation.md` for intended and completed changes. It is not verification evidence.

## Plan contract

Each checklist item must include:

- Stable ID such as `I-01`
- Concrete outcome
- Expected files or subsystem
- Constraints and dependencies
- Required verification IDs

Order items by dependency. Keep the top of the file abstract and place file-level steps below.

## Checkbox semantics

- `[ ]`: not implemented
- `[x]`: implementation completed or claimed complete

Checking an item does not mean behavior passed tests or met the goal. Record proof only in `07-verification.md` and link it back using the implementation ID.

## Scope changes

When implementation reveals new facts:

1. Update research or questions first.
2. Refresh synthesis and decisions if the model changed.
3. Revise the plan and record the scope delta.
4. Do not quietly expand the task beyond user intent.
