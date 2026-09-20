# Failure modes and self-review

Documented ways agents fail at research ([How Do Agents Fail on AutoResearch](https://arxiv.org/abs/2608.14905), overclaiming studies, METR reports, Sakana AI Scientist critiques, Nanda's list of junior-researcher mistakes). The self-review below must change the report; a checklist that passes everything on the first try was not run.

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
- **Skipping the literature or the data.** Reinventing prior work; never looking at raw examples.
- **Erasing negatives.** Reverted, failed, or interrupted runs missing from the log.
- **Declaring done on budget exhaustion or on intent.** "I implemented it" is not "it works".
- **Overclaiming coverage.** Reporting on files or results that were not actually read or run.

## Self-review before reporting

Answer each in writing, then edit the report accordingly.

1. Which phase was I in, and does the report claim more certainty than that phase supports?
2. For every number: baseline, seeds or repeats, evaluation conditions, and the artifact it came from. Remove or caveat any that lacks one.
3. What is the boring alternative explanation, and which check ruled it out?
4. Which claims come from my own runs, which from a subagent, which from a paper section I read, which from an abstract or snippet? Label them.
5. What did I not read, not run, or not check? Say so.
6. Are the examples shown random samples?
7. Which of the failure modes above did this session commit, even partially? Fix or disclose.
8. If the user asked a narrow question, did I also state the larger question it belongs to and what the next experiment would be?
