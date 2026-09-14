---
name: human-interface-design
description: Design, review, or refine product interfaces using Apple Human Interface principles. Use for layout, navigation, controls, feedback, modality, onboarding, accessibility, typography, materials, input, and interaction behavior; do not use merely to imitate Apple’s visual style.
metadata:
  version: "1.1.0"
---

# Human Interface Design

Create interfaces that feel understandable, direct, forgiving, adaptable, and carefully made. Apply Apple’s reasoning to the product and platform in scope; do not turn every interface into an Apple visual imitation.

## Establish the human context

Identify the person’s goal, current context, platform, available space, input methods, and cost of mistakes. When reviewing an existing product, inspect the real interface, implementation, or canonical mockup when available. Distinguish observed problems from assumptions about users.

Use these principles to resolve tradeoffs, in order:

1. **Purpose:** Keep the person’s primary outcome obvious and close.
2. **Agency:** Allow exploration, escape, correction, and recovery.
3. **Responsibility:** Protect privacy, safety, data, attention, and trust.
4. **Familiarity:** Preserve platform conventions and internal consistency.
5. **Flexibility:** Adapt to context, ability, input, and available space.
6. **Simplicity:** Remove unnecessary complexity; don’t merely hide it.
7. **Craft:** Refine wording, alignment, state changes, motion, and performance.
8. **Delight:** Reinforce the intended feeling without obstructing the task.

## Design the whole interaction

Cover the path before polishing a screen:

- entry and orientation
- primary action and alternatives
- loading, empty, partial, success, and failure states
- cancellation, interruption, undo, and recovery
- return navigation and preservation of context
- keyboard, pointer, touch, assistive technology, and reduced-motion behavior as relevant

Prefer direct manipulation and immediate, local feedback. Keep controls near what they affect. Make destructive or consequential outcomes clear before commitment, but don’t interrupt expected, reversible actions with routine confirmation dialogs.

Use familiar system components and behaviors when they meet the need. A custom control must provide a material benefit and retain expected semantics, focus behavior, accessibility, and state communication.

## Apply concrete checks

Load only the guidance the task needs:

- Read [HIG checks](references/hig-checks.md) for layout, typography, accessibility, materials, feedback, modality, onboarding, search, or undo.
- Read [Design process](references/design-process.md) when shaping a product, information architecture, navigation, content hierarchy, or prototype.
- Read [Inclusive design](references/inclusive-design.md) when people’s abilities, languages, cultures, sensory needs, customization, or accessibility testing affect the work.
- Read [Interface writing](references/interface-writing.md) when naming features, actions, navigation, states, errors, onboarding, or settings.

For version-specific Apple work, check current [Design updates](https://developer.apple.com/design/whats-new/) and [Apple Design Resources](https://developer.apple.com/design/resources/) before prescribing components or specifications. Prefer current official kits, symbols, templates, and platform behavior over remembered values or visual approximation.

Treat visual hierarchy as functional. Reading order, alignment, spacing, grouping, contrast, and type should reveal what matters, what belongs together, and what happens next. Progressive disclosure should reduce decision load while keeping important actions discoverable.

Treat motion as feedback and spatial explanation. Start feedback immediately, preserve continuity, keep gesture-driven motion interruptible, and provide a non-vestibular reduced-motion equivalent. Avoid decorative motion that delays work or competes with content.

## Review mode

Lead with a short TL;DR sorted by severity. For each material finding, state:

- the observed behavior and affected human goal
- the principle or concrete guideline it conflicts with
- the smallest durable improvement
- evidence and confidence; label untested assumptions

Prioritize lost work, traps, unclear state, inaccessible interaction, broken platform expectations, and primary-task friction above visual polish. Mention strengths only when they inform what to preserve.

## Build mode

Reuse the product’s existing design system, platform primitives, and canonical interaction patterns. Implement the full relevant state model, not only the ideal screenshot. Preserve user work across interruption and failure. Verify behavior at representative sizes, with large text, keyboard or alternative input, and reduced motion when applicable.

## Completion

Finish when the primary task is clear and efficient, state and consequences are understandable, people can recover, the interface adapts to relevant contexts, and accessibility is verified to the available evidence depth. State any live, device, assistive-technology, or user-testing gaps explicitly.
