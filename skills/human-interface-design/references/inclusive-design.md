# Inclusive design

Use this when a design decision could exclude people or when the task includes accessibility, personalization, localization, or user research.

## Close the inclusion gap

- Involve people with relevant disabilities and lived experiences. Do not infer all needs from guidelines, automated checks, or a nondisabled team’s simulation.
- Identify mismatches between the interface and a person’s abilities, environment, language, culture, or input method. Fix the mismatch in the system where possible instead of labeling the person an edge case.
- Support multiple senses. Pair visual, audio, haptic, and textual communication according to significance; never require a single channel for essential meaning.
- Provide customization when one presentation or interaction cannot serve everyone well. Preserve sensible accessible defaults and avoid making people rebuild the interface before use.
- Adopt platform accessibility semantics and APIs before inventing parallel accessibility UI. Custom controls must expose equivalent names, roles, values, actions, focus, and state.

## Verify, don’t declare

- Test representative tasks with keyboard or alternative input, screen reader, large text, increased contrast, reduced motion, and reduced transparency as relevant.
- Include empty, loading, error, destructive, and recovery states in assistive-technology testing; the ideal state is not sufficient.
- Pair automated audits with manual interaction and participation from affected people. Record what was directly tested and what remains inferred.
- Track inclusion debt explicitly when a known exclusion cannot be resolved now: affected people and task, impact, workaround, owner, and next decision point.
- For Apple-platform releases, keep accessibility support claims aligned with observed behavior and current Accessibility Nutrition Label requirements.

## Sources

- [Principles of inclusive app design](https://developer.apple.com/videos/play/wwdc2025/316/)
- [Accessibility developer resources](https://developer.apple.com/accessibility/)
- [Accessibility and Inclusion videos](https://developer.apple.com/videos/accessibility-inclusion/)
