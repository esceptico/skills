# Failure modes and self-review

Documented ways agents fail at research ([How Do Agents Fail on AutoResearch](https://arxiv.org/abs/2608.14905), overclaiming studies, METR reports, Sakana AI Scientist critiques, Nanda's list of junior-researcher mistakes, Orchestra's ARA rigor reviewer). The self-review below is short on purpose; it must change the report, and if none of its five questions changed anything, look again.

## Failure modes

- **Answering the literal question and stopping.** One paper check, one recommendation, no hypothesis, no experiment, no log.
- **Acting as if in Understand while still in Explore.** Designing one decisive test before there are real hypotheses.
- **Claims untraceable to artifacts.** Numbers in the report that no run directory, log, or primary-source section supports.
- **Superficial self-review.** A checklist restated as passed, with nothing in the report revised.
- **Metric hacking and circular validation.** Selecting against the test set, fitting the grader, leaking labels, changing what is measured rather than how well.
- **Cherry-picking.** One compelling example as the finding; the best seed as the result.
- **Excitement bias.** A surprising result treated as confirmation instead of a reason to re-run.
- **Timid or shotgun edits.** Changes too small to move the metric, or several changes in one run.
- **Rabbit-holing.** Hours on one anomaly with no zoom-out.
- **Unnecessary complexity.** An elaborate method where a simple one applied carefully would do.
- **Skipping the literature or the data.** Reinventing prior work; never looking at raw examples.
- **Erasing negatives.** Reverted, failed, or interrupted runs missing from the log.
- **Declaring done on budget exhaustion or on intent.** "I implemented it" is not "it works".
- **Overclaiming coverage.** Reporting on files or results that were not actually read or run.

## Self-review before reporting

Answer these in writing for anything larger than a quick answer, then edit the report.

1. For every number you lean on: baseline, repeats, conditions, and the artifact it came from. Remove or caveat any that lacks one.
2. Which claims come from your own runs, which from a worker, which from a source section you read, which from an abstract? Label them, and say what you did not read, run, or check.
3. What is the boring alternative explanation, and what ruled it out? Are the examples shown random?
4. Does the report claim more certainty than the phase supports? If the question was narrow, does it say what larger question it belongs to?
5. Does each claim have the kind of evidence its wording needs? "Causes" needs an isolating ablation, "generalizes" needs conditions that vary, "improves" needs a matched baseline, "typically" needs a representative sample. Does the metric measure what the claim says, or a narrower proxy of it? Does any claim lean on something the log marks reverted, and does any logged run cut against a claim without being mentioned? Rescope or cut whichever claim fails.
