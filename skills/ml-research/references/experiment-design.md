# Experiment design

Choose experiments for what they can teach within the available budget.

- **Question:** identify the uncertainty and how different outcomes would change the next decision.
- **Comparison:** check the resolved configuration and baseline revision, including whether the intended change is actually enabled.
- **Stopping:** choose a useful evaluation horizon and justified stopping criteria. Early curves can mislead when schedules differ; distinguish interrupted runs from negative results. Stop broken or uninformative runs when warranted.
- **Transfer:** treat small-scale gains as provisional. When the decision depends on deployment scale or efficiency, check relevant scale and actual compute, time, or memory costs. A scaling study is not required for every idea.

Adapted from [George Grigorev's experiment-design article](https://x.com/iamgrigorev/status/2071688181628678468).

## Keep experiment prerequisites justified

Start with the smallest end-to-end pilot that can change the research decision. Validate basic task behavior before building machinery needed only for later causal or confirmatory claims. Protect held-out data and retain failed runs; exploratory train-only work need not satisfy every final-claim gate.

For a blocking check, state what failure would invalidate and which next actions actually depend on it. Before extending a failed check, inspect its comparison and assumptions. Separate model/task failure, implementation failure, and an unsuitable test. A recorded prerequisite is revisable when its rationale fails; preserve the original result and document the prospective replacement rather than changing its outcome.

For numerical controls, distinguish repeatability of the same execution from agreement between different shapes, cache schedules, dtypes, or kernels. Determinism alone does not imply cross-path bit equality. Use a matched execution with an identity intervention to isolate hook effects; establish replay fidelity separately with task-relevant measurements. A passing fake-model test establishes the contract, not real-backend equivalence.

Delegate the uncertainty to resolve and the dependent next decision, not only a list of implementation requirements. When work expands, compare the expected information from further infrastructure with the next feasible experiment. Report what was learned and what remains untested before test counts or bookkeeping.


Before loading weights or starting paid compute, verify the deployed source/schema hashes, dependency versions, resolved generation flags, and complete prompt construction against a plan prepared before deployment. Use one rendering path for pilot and full runs; do not manually rebuild partial prefix records. Retain the resolved configuration with results.

Choose a small balanced behavioral screen and explicit shortcut/format stopping rules before scaling. Compare observed choices with fixed-label and position baselines only when target labels vary appropriately. Passing a screen does not establish task viability or confirmatory significance. Describe split generalization from actual held-out factors, not aspirational protocol wording; shared templates or vocabulary cannot support claims about unseen templates or vocabulary.


## Show experiment progress

For iterative campaigns with comparable measured runs, maintain an annotated progress chart alongside the experiment log. Prefer the running-best staircase with every attempt visible, as a compact view of what improved and what regressed. Update it when new evaluated results arrive; a single run or research-only request does not need a chart.

- Plot experiment order on x and the named metric with units and direction on y. Use separate panels for different metrics, datasets, evaluation protocols, or budgets that are not directly comparable. Add cumulative cost or elapsed time when efficiency matters.
- Show every measured attempt as a point, distinguishing accepted, rejected, and inconclusive results with marker shapes as well as color. Put failed runs without valid scores in a separate status strip; never invent a zero score.
- Draw a step line for the best eligible result so far, starting at the baseline. Update it only when a comparable run passes the stated quality gates and improves the metric (maximum or minimum as appropriate). A rejected high score must not raise the line. Distinguish a noise-sensitive observed best from a verified improvement; include uncertainty or repeated-run variation when available.
- Label improvements with the concrete change and run ID. Keep other labels in a short accompanying table: run, change, score, disposition/reason, evidence link. Treat annotations as descriptions of changes, not proof of their causal effect.
- Generate the chart from recorded results, retain negative attempts, and mark evaluation changes as new series. Keep sealed evaluations separate from tuning history. An upward staircase alone hides failed attempts and selection noise; the points and decision table are part of the view.
