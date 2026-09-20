# Research loop

Adapted from Neel Nanda's research-process sequence ([Explore, Understand, Distill](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/hjMy4ZxS5ogA9cTYK), [Key Mindsets](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/cbBwwm4jW6AZctymL), [How to Write ML Papers](https://www.alignmentforum.org/s/5GT3yoYM9gRmMEKqL/p/eJGptPbbFPZGLpjsp)), John Schulman's [Opinionated Guide to ML Research](http://joschu.net/blog/opinionated-guide-ml-research.html), and Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) loop.

## Phases have different north stars

| Phase | North star | Enter when | Leave when |
| --- | --- | --- | --- |
| Explore | information gained per unit time | the question is vague or you cannot name competing hypotheses | you can name 2+ specific hypotheses and what would distinguish them |
| Understand | evidence for and against named hypotheses | hypotheses exist | you are personally convinced, and could say what a skeptic would object to |
| Distill | 1–3 claims a skeptic accepts | you are convinced | every claim has evidence you re-checked, and you can say why anyone should care |

Movement is bidirectional. An anomaly or an ill-posed hypothesis sends you back to Explore; that is progress, not failure. The most common error is behaving as if in Understand (designing one decisive test, answering one literal question) while still in Explore, where the right move is many cheap probes and lots of looking at data.

Exploration is the bulk of early work. Distillation starts well before the end, because writing reveals gaps.

## Explore well

- Ask, out loud and often: am I getting enough information per unit time? If not, change the experiment, not the effort.
- Prefer the quick-and-dirty version that shows signs of life today over the well-designed version that runs tomorrow.
- Attack the direction from several cheap angles rather than one long run. Ask how you would discover fastest that the direction is doomed, and do that first.
- Look at raw data and raw outputs for a long time before building machinery. Data problems explain results more often than methods do.
- Keep a running log of curiosities, and a separate highlights list. Patterns appear across entries.

## Timers

- Before any run over ~30 minutes: could a smaller run answer the same question?
- Several hours without learning something new: zoom out. Five minutes of brainstorming, then pick the highest-value next experiment.
- About a day of a throwaway direction with nothing visible: pivot. If an effect is real and large it usually shows up fast.
- Weekly for long campaigns: does today's work still serve the stated goal? Keep goals in three tiers (months, weeks, days) and check the small against the large.

## Skepticism drills

- Before testing a hypothesis, spend five minutes listing how it could be false. Test the boring alternative first.
- After a result, ask which hypothesis made this outcome more likely, not whether it "fits". Most of the probability mass is usually on an explanation you have not yet thought of.
- An exciting result is more likely to be wrong, not less. Re-run it with a different seed, a different prompt set, a shuffled-label control, and a matched random intervention before believing it.
- Ablate every component. If removing something changes nothing, it was not doing what you thought.
- Invest real effort in the strongest simple baseline. Beating a weak baseline is not a result.
- Report randomly sampled examples. A cherry-picked example is a hypothesis, not evidence.

## Statistical bar

For exploratory work, treat p < 0.001 as the bar for "probably real" and p between 0.005 and 0.05 as "interesting, replicate before claiming". An implausibly tiny p-value usually means broken independence (correlated samples, shared prompts), not a discovery. Run the pipeline on shuffled labels to see what noise produces. Report effect sizes and variation across seeds and splits; never invent error bars from one run.

## Iterative campaigns

When there is a fixed metric and a fixed per-experiment budget, run the autoresearch shape: propose one change with its reasoning, apply it, run the fixed budget, compare to the current best, keep if better and revert if not, log, repeat. Timid edits waste runs; make each change large enough to move the metric if the idea is right. Noise decides most of these comparisons, so measure the noise floor first (same config, different seeds) and do not keep a change inside it.

## When to write up

List everything learned. For each claim check that you can defend it with evidence you re-verified, and that the evidence is actually correct, before entering writing mode. Pick 1–3 claims; everything else supports them. Readers keep a few sentences, so choose those sentences.
