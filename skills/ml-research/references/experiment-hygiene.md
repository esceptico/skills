# Experiment hygiene

The ladder below is Karpathy's [Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/), with agent-loop rules from [autoresearch](https://github.com/karpathy/autoresearch) and Cognition's [Kevin-32B](https://cognition.com/blog/kevin-32b) loop. Training fails silently: everything can be syntactically right and still wrong, and the only defense is a paranoid, ordered set of checks.

## Before the first run

First, run the existing pipeline unchanged and record its number as run zero; everything else is measured against it. Then:

1. **Become one with the data.** Spend real time scanning examples, label distributions, duplicates, corrupt items, and biases. Look at the exact tensors that enter the network, after preprocessing and augmentation.
2. **Skeleton and dumb baselines.** Fix the seed. Turn augmentation and other fanciness off. Pick the simplest model that can possibly work. Verify loss at init matches the expected value (for example `-log(1/n_classes)`). Initialize well.
3. **Three baselines before any idea:** a human or heuristic baseline, an input-independent baseline (zero or shuffled inputs, which must be worse), and the dumbest end-to-end model.
4. **Overfit one batch.** Two or three examples to near-zero loss, and check the predictions match the labels. If this fails, nothing downstream is trustworthy.
5. **Check monotonic capacity.** More capacity should lower training loss. Check that the intended change is actually enabled in the resolved config.
6. **Use backprop to chart dependencies.** A gradient that should be zero and is not means leakage across the batch dimension or a similar bug.

## During iteration

- **One change at a time.** Add one feature, one signal, or one trick, confirm the expected effect, then the next. A run that changes two things answers no question.
- **Don't be a hero.** Copy the nearest working recipe from the most related paper, Adam at 3e-4, and standard defaults. Distrust learning-rate decay defaults borrowed from a different dataset size.
- **Fixed budget, fixed metric, frozen evaluator.** Compare runs at the same wall-clock or token budget. One headline metric decides the verdict; a small fixed set of guard checks (a held-out split, the train-versus-validation gap, output length or format, throughput) decides whether the win is real. Fix both, and the evaluation code, before the first run and do not touch them during the campaign. Evaluate on the full evaluation set, not a smoothed batch number.
- **Measure the noise floor first.** Repeat the baseline with different seeds. A change inside that band is not a win, whatever the direction.
- **Correctness before performance.** A run that fails its correctness checks gets no performance score. Compile, unit-test, and sanity-check outputs before timing or benchmarking. Structural checks guard against "wins" that changed what was measured rather than how well.
- **Typed feedback.** A failed run gets its error trace and a fix attempt. A passed run gets a measurement and an improvement attempt. Do not treat both the same.
- **Verdict.** Keep an improvement over the current best outside the noise floor under matched conditions; it becomes the new baseline. Inside the noise floor is inconclusive. A crashed or voided run is failed. Everything else is reverted, and every outcome goes in the log with its reason.

## Regularize, then tune, then squeeze

Order of returns: more real data, then augmentation, then pretrained weights, then dropout or weight decay, then early stopping. Random search over grid search. Ensembles and longer training come last. Do not tune before the pipeline passes the checks above.

## Reproducibility

Record for every run: code revision, model and data revisions, resolved configuration, seeds, dependency versions, hardware, and the exact commands. A repository name or a moving branch pins nothing. Same-execution repeatability is not cross-path equality across shapes, dtypes, or kernels; state which one you measured. Retain failed runs and the config that produced them.

## Progress view for campaigns

For campaigns with comparable runs, keep a running-best staircase with every attempt visible (kept, reverted, inconclusive, failed), so the picture includes the failures and the selection noise, not only the wins. A single run needs no chart.
