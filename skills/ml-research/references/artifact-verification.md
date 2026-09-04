# Artifact verification

Use when an answer depends on a model, dataset, codebase, or reproduced result. Report the evidence level per artifact or claim:

- **Exists:** the exact artifact resolves at an authoritative source.
- **Inspected:** relevant files, configuration, license, data schema, or implementation were read. State what was checked.
- **Runs:** the relevant path executed successfully in a stated environment. A smoke test establishes only the path it exercised.
- **Result reproduced:** execution matched a specified result within a stated tolerance under a recorded evaluation protocol. Name the result, conditions, and observed difference.

Mark inaccessible or unchecked evidence explicitly. Attribute third-party execution reports to their source; do not imply that you ran them. One working artifact does not verify the rest of a pipeline.

For reproducible recommendations or experiments, record immutable code/model/dataset revisions where available, relevant configuration, dependencies, and evaluation inputs. A repository name or moving branch alone does not pin the artifact. State missing pins when exact reproduction remains uncertain.

Choose verification depth according to the requested claim and execution authorization. Artifact inspection can be sufficient for a literature review; do not launch experiments merely to earn a stronger label.
