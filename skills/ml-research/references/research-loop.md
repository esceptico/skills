# Research loop

Adapted from Neel Nanda's research-process sequence ([Explore, Understand, Distill](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/hjMy4ZxS5ogA9cTYK), [Key Mindsets](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL), [How To Become A Mechanistic Interpretability Researcher](https://www.alignmentforum.org/posts/jP9KDyMkchuv6tHwm/how-to-become-a-mechanistic-interpretability-researcher), [Statistical Suggestions](https://www.alignmentforum.org/posts/GxhtzqMwdTHo6326y/statistical-suggestions-for-mech-interp-research-and-beyond), [How to Write ML Papers](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/eJGptPbbFPZGLpjsp)), John Schulman's [Opinionated Guide to ML Research](http://joschu.net/blog/opinionated-guide-ml-research.html), and Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) loop. The numbers below are rules of thumb, not gates.

## Phases have different north stars

| Phase | North star | You are here when | Move on when |
| --- | --- | --- | --- |
| Ideation | a problem worth answering | the question is new to you | you can say why it matters, what is already known, and the specific unknown |
| Explore | information gained per unit time | the question is vague or you cannot name competing hypotheses | you can name two or more specific hypotheses and what would distinguish them |
| Understand | evidence for and against named hypotheses | hypotheses exist | you are fairly convinced and can say what a skeptic would object to |
| Distill | 1–3 claims a skeptic accepts | you have a claim worth defending | every claim rests on evidence you re-checked, and you can say why anyone should care |

Movement is bidirectional. An anomaly or an ill-posed hypothesis sends you back to Explore; that is progress, not failure. Exploration is the bulk of early work, but start writing before you are fully convinced: drafting reveals the gaps, so distillation begins well before the end.

Prefer goal-driven research (pick the problem, then whatever method serves it) over idea-driven research unless you have an unusual angle. Hold a small standing budget for side directions and spend it there instead of thrashing the main line; recognise a dead end without switching problems every day.

## Explore well

- Ask, often: am I getting enough information per unit time? If not, change the experiment, not the effort.
- Prefer the quick-and-dirty version that shows signs of life today over the well-designed version that runs tomorrow.
- Attack the direction from several cheap angles rather than one long run. Ask how you would discover fastest that the direction is doomed, and do that first.
- Look at raw data and raw outputs for a long time before building machinery. Data problems explain results more often than methods do.
- Keep a running note of curiosities and a separate highlights list. Patterns appear across entries.

## Timers

- Before an experiment of more than roughly half an hour, stop and ask whether this is really the fastest way to gain information.
- Learned nothing in a couple of hours: pivot to another approach. Two or three approaches dead: it is fine to pick another problem. Stuck: five minutes of brainstorming, then the highest-value next probe.
- Real, large effects usually show up within a day of a throwaway direction. If nothing has, move on.
- For long campaigns, check weekly that today's work still serves the goal. Keeping goals in three tiers (months, weeks, days) makes the check easy.

## Skepticism drills

- Before testing a hypothesis, spend five minutes listing how it could be false, and test the boring alternative first.
- After a result, ask which hypothesis made this outcome more likely, not whether it "fits". Most of the probability mass is usually on an explanation you have not thought of yet.
- An exciting result is more likely to be wrong, not less. Before believing it, repeat it under at least one change it should survive: another seed, another prompt set, shuffled labels, or a matched random intervention.
- Ablate what you claim matters. If removing it changes nothing, it was not doing what you thought.
- Invest in the strongest simple baseline. Beating a weak one is not a result.
- Show randomly sampled examples. A cherry-picked example is a hypothesis, not evidence, unless the claim is only that at least one such example exists.

## Statistical bar

A p-value between 0.01 and 0.05 means collect more data, not claim; data is usually cheap, so aim for 0.001. An implausibly tiny p-value usually means broken independence (correlated samples, shared prompts) rather than a discovery. Permutation-test the pipeline on shuffled labels to see what noise alone produces. Report effect sizes and variation across seeds and splits; never invent error bars from one run.

## Iterative campaigns

When there is a fixed metric and a fixed per-experiment budget, run the autoresearch shape: propose one change with its reasoning, apply it, run the fixed budget, compare to the current best, keep if better and revert if not, log, repeat. The loop is only as good as its evaluator: before the campaign, confirm the evaluator is automatic, frozen, seeded, and separates known-good from known-bad, and measure the noise floor (same config, different seeds). Without that the loop cannot run; say so and propose a manual protocol instead. Timid edits waste runs; make each change large enough to move the metric if the idea is right. Noise decides most of these comparisons, so a change inside the noise floor is inconclusive, whatever its sign.

## When to write up

List everything learned. For each claim check that you can defend it with evidence you re-verified, and that the evidence is actually correct, before entering writing mode. Pick 1–3 claims; everything else supports them. Readers keep a few sentences, so choose those sentences.
