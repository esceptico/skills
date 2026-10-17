---
name: bfs
description: "Research breadth-first: map alternatives, leads, or connections before going deep. Use for landscape scans, prior-art searches, unfamiliar topics, and finding promising paths through people, papers, or code."
version: 1.0.0
---

# Breadth-first research

Map the useful directions before committing to one. Use whatever sources and tools are available; no particular runtime or subagents are required. If one direction already dominates and the user wants it resolved, skip the survey and investigate that direction depth-first (the `dfs` skill, if installed).

## Explore

- Start from the user's question and what the answer needs to support. Use relevant existing context; keep the user's constraints and settled decisions in view.
- Identify the main alternatives or starting points. Give each a first pass before following one several steps deeper. For linked material, explore the current layer before expanding the next.
- Keep two short lists: leads not yet expanded, and sources already checked. Expand the next lead by relevance to the question, not by the order it appeared. Cycles and duplicate sources are not new leads.
- Keep brief notes on what each direction offers, its source, and the important unknowns. Drop a direction after its first pass when it does not bear on the question, and note why so it is not rediscovered.
- Search for competing explanations and existing solutions, not only support for the first promising idea. A new keyword or citation is useful when it changes the map, not merely because it exists.

## Compare and stop

- Use snippets and summaries to discover leads, not to support substantive conclusions. Open the underlying source before relying on a claim; say when access or coverage is incomplete.
- Distinguish observed connections from inferred ones. A follow, mention, or citation does not establish collaboration, endorsement, or independent confirmation.
- Compare directions against the original question. Stop expanding when new leads mostly repeat what you know and you can justify a shortlist. If the user asks for complete coverage, account for that scope rather than silently sampling it.
- Return the useful map or shortlist, ranked by fit to the question and strength of evidence: why each direction matters, source references, and gaps that could change the ranking. Say 'not found in the sources checked', not 'does not exist'.
- When depth is needed, carry the most promising unresolved question into a focused depth-first investigation (the `dfs` skill, if installed). Do not force a deep dive if the survey already answers the user.

Keep the method proportional to the task. No fixed number of branches, sources, or search rounds; notes can stay in the conversation unless the work needs a saved handoff.
