---
name: dfs
description: "Research depth-first: follow one question through underlying evidence, dependencies, and counterexamples, then backtrack when answered or blocked. Use for investigating a claim, understanding a method, tracing code behavior, and resolving a promising research lead."
version: 1.0.0
---

# Depth-first research

Resolve one useful question by following its evidence deeply, without losing the question you started with. Use whatever sources and tools are available; no particular runtime or subagents are required.

## Investigate

- State the question and what evidence would answer it or change your mind. Begin with the strongest relevant lead and existing context, not a fresh survey unless one is needed.
- Read the underlying material, not just its summary. Follow the methods, assumptions, results, implementation, or dependencies that the conclusion actually relies on. Read relevant appendices and limitations; when complete coverage is requested, track what was and was not read.
- Follow a new subquestion when resolving it is necessary for the parent question. Keep a brief place to return to and defer interesting tangents that do not affect the answer.
- Seek counterexamples and alternative explanations. Distinguish what a source claims, what its evidence demonstrates, and what you infer. A proposal or readable signal is not proof of implemented behavior or causality.
- When reading alone cannot settle the question, identify the smallest useful check or experiment. Run it only within the user's authorization; otherwise report it as proposed, not completed.

## Backtrack and conclude

- When a branch is answered, contradicted, inaccessible, or no longer producing useful evidence, record why and return to its parent. Try another relevant lead rather than repeating the same unsuccessful path.
- Remember checked sources and unresolved questions so loops and repeated citations do not masquerade as progress. Revisit when new evidence gives a reason.
- Stop when the evidence supports an answer at the requested depth, or when the remaining uncertainty requires unavailable evidence. If the initial direction was wrong, widen the search rather than forcing a conclusion.
- Return the answer, the decisive evidence and source references, what could overturn it, and any unresolved limitation. Be explicit about reading coverage and which checks actually ran. Do not claim exhaustive verification from a targeted pass.

Keep the method proportional to the task. No fixed depth, source quota, mandatory experiment, or required note format; use existing notes when a saved handoff is useful.
