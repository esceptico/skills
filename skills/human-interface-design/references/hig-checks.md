# HIG checks

Use only the sections relevant to the task. These checks summarize current Apple Human Interface Guidelines; consult the linked source when platform-specific details matter.

## Freshness and source fidelity

- Treat bundled measurements and component guidance as a starting point, not proof of the current platform contract.
- For version-specific Apple work, check [What’s new in design](https://developer.apple.com/design/whats-new/) and record the platform/version that informed consequential decisions.
- Use current official [Apple Design Resources](https://developer.apple.com/design/resources/) for UI kits, production templates, fonts, SF Symbols, and technology-specific assets. Do not redraw or approximate a standard asset when a canonical source exists.

## Layout and navigation

- Put important content first in the natural reading order.
- Use alignment, indentation, proximity, negative space, and containers to express hierarchy and relationships.
- Keep controls visually distinct from content and physically close to what they affect.
- Use progressive disclosure for secondary complexity, not for the primary action or critical state.
- Adapt to available space, orientation, window configuration, locale, and text size. Do not branch layout only by named device.
- Preserve recognizable content and control positions across adaptations; use motion to explain transitions.
- Every view should make location, destinations, available content, and escape clear.

Source: [Layout](https://developer.apple.com/design/human-interface-guidelines/layout)

## Typography

- Create hierarchy with size, weight, color, leading, and placement as a system.
- Minimize typefaces and avoid light weights for small or critical text.
- Prefer system text styles when platform-native behavior matters.
- Support optical sizing and Dynamic Type or the platform equivalent.
- Let containers grow and adjacent items stack instead of clipping enlarged text.
- Test hierarchy and legibility at the smallest and largest supported sizes.

Apple’s baseline guidance:

| Platform | Default | Minimum |
| --- | ---: | ---: |
| iOS / iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

Source: [Typography](https://developer.apple.com/design/human-interface-guidelines/typography)

## Accessibility

- Make the interface intuitive, perceivable through more than one channel, and adaptable to user preferences.
- Support text enlargement of at least 200%, or 140% on watchOS, without loss of content or function.
- Meet at least 4.5:1 contrast for ordinary text and 3:1 for large or bold text; verify light, dark, and increased-contrast appearances.
- Never communicate meaning with color, sound, motion, or position alone.
- Supply meaningful names, values, roles, reading order, focus order, and state changes for assistive technology.
- Provide sufficiently large targets and separation; preserve equivalent keyboard, pointer, touch, voice, or assistive paths as relevant.
- Respect reduced motion, reduced transparency, increased contrast, captions, and other system preferences.

Apple’s control-size guidance:

| Platform | Default | Minimum |
| --- | ---: | ---: |
| iOS / iPadOS | 44×44 pt | 28×28 pt |
| macOS | 28×28 pt | 20×20 pt |
| tvOS | 66×66 pt | 56×56 pt |
| visionOS | 60×60 pt | 28×28 pt |
| watchOS | 44×44 pt | 28×28 pt |

Source: [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

## Materials and visual depth

- Use material to explain hierarchy and preserve context, not as decoration.
- Keep Liquid Glass or analogous translucent treatment in the functional layer: navigation and controls above content.
- Use standard or opaque materials inside the content layer.
- Apply custom glass sparingly. Prefer the regular, legible variant; reserve highly transparent treatment for rich media with verified contrast.
- Let system accessibility settings alter transparency and contrast without breaking hierarchy.
- Do not stack multiple competing translucent surfaces.

Source: [Materials](https://developer.apple.com/design/human-interface-guidelines/materials)

## Feedback and status

- Communicate current status, completion, warning, error, and recovery in proportion to significance.
- Put passive status near the object or action it describes.
- Use alerts only for critical, preferably actionable information.
- Confirm significant completion; don’t celebrate every routine success.
- Explain why an action cannot proceed and what the person can do next.
- Make feedback multimodal and accessible where practical.

Source: [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

## Modality

- Use a modal only when separation or focused commitment provides a clear benefit.
- Keep the task short and narrowly scoped, with an obvious platform-conventional dismissal path.
- Preserve the parent context and protect unsaved user-generated work.
- Avoid deep navigation inside a modal and never stack ordinary modals or alerts.
- Name the modal task clearly; let one modal dismiss before another appears.

Source: [Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

## Onboarding and help

- Prefer an interface that teaches itself.
- Teach by letting people safely perform the real interaction.
- Prefer contextual tips near the relevant control over a long introductory tour.
- Keep prerequisite onboarding brief and make tutorials skippable and recoverable later.
- Provide useful defaults and postpone nonessential permissions, setup, ratings, and purchases until context makes them meaningful.

Source: [Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)

## Undo and recovery

- Make the result of undo and redo predictable with specific labels when useful.
- Show the affected content, even if it moved offscreen.
- Support multiple levels of undo and batch reversal for logically grouped changes where appropriate.
- Prefer familiar platform commands and shortcuts over custom mechanisms.
- Recovery is part of the core state model, not an error-message afterthought.

Source: [Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)

## Search

- Give search a primary position when it is central to the product.
- Prefer one clearly identified global search, with local search only where sections are meaningfully distinct.
- Show the current scope and offer useful suggestions or recent searches.
- Protect search-history privacy and let people clear it.
- Preserve the person’s query and context when moving between results and details.

Source: [Searching](https://developer.apple.com/design/human-interface-guidelines/searching)

## Primary source index

- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles)
- [Patterns](https://developer.apple.com/design/human-interface-guidelines/patterns)
- [Components](https://developer.apple.com/design/human-interface-guidelines/components)
- [Inputs](https://developer.apple.com/design/human-interface-guidelines/inputs)
