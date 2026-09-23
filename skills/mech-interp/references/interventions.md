# Interventions: patching, steering, interchange

Sketches follow `lab.interp` (`~/src/labs/src/lab/interp.py`): a forward hook on `interp.blocks(model)[L]` (the
residual after block L), `_hidden`/`_replace` for tuple or tensor block outputs, float32 maths,
a context manager that always removes the hook. A sketch that proves useful belongs in
`lab.interp` next to `ablate`. What a result shows (necessity, sufficiency, specificity) is
judged by the ml-research evidence standard (`~/src/skills/skills/ml-research/references/mech-interp.md`).

## Activation patching

```python
@contextlib.contextmanager
def patch(model, layer, source, positions, basis=None):
    """Write `source` ([seq, d], from another run) into the residual after block `layer` at
    `positions`. With `basis` ([k, d]) only the span of the basis is swapped."""
    q = None if basis is None else torch.linalg.qr(basis.float().T)[0].to(model.device)
    src = source.to(model.device).float()
    def hook(_, __, out):
        hs = _hidden(out)
        h = hs.float().clone()
        for p in positions:
            delta = src[p] - h[0, p]
            h[0, p] += delta if q is None else (delta @ q) @ q.T
        return _replace(out, h.to(hs.dtype))

    handle = interp.blocks(model)[layer].register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()
```

Get `source` with `interp.resid(model, tok, [text], layer)[0]`. The basis branch is resample
ablation h ← h + P(h′ − h) from `jacobian-subspaces.md`, so the same code serves subspace
patching. Clean and corrupt prompts need matching token positions for the patched span; check
`len(tok(text).input_ids)` and align on the positions you name, not on string offsets.

Two directions, two questions (m = metric, normalised as (m − m_corrupt)/(m_clean − m_corrupt)):
- Denoising: run on the corrupt input, patch in clean activations. Tests whether this site
  is sufficient to restore the behaviour given everything else corrupted. It finds sites where
  any one copy suffices (OR-like, redundant paths) and misses parts that only work jointly.
- Noising: run on the clean input, patch in corrupt activations. Tests whether this site is
  necessary. It finds jointly required parts (AND-like) and misses redundant ones, because a
  backup path covers the loss. Both on one grid is often the quickest look at redundancy.

Corruption: prefer counterfactual minimal pairs (same template, one entity swapped, same
length) to Gaussian noise on embeddings (ROME-style causal tracing). Noise puts every later
activation off-distribution, and the model's response to that is partly what you measure.

Metric: logit difference between the correct and the counterfactual answer is the default. It
is nearly linear in the final residual and does not saturate the way probability does. Use
next-token loss (`interp.next_token_loss`) when the claim is about general capability.

Sweeps: layers × positions with `patch(..., positions=[p])`, one forward per cell, logged as
`fig.heatmap(grid, x=tokens, y=layers, diverging=True, value_label="restored")`.

## Steering

```python
@contextlib.contextmanager
def steer(model, layer, direction, alpha, start=1):
    """Add alpha · unit(direction) to the residual after block `layer`, from position `start`."""
    v = (direction / direction.norm()).float().to(model.device)

    def hook(_, __, out):
        hs = _hidden(out)
        h = hs.float().clone()
        h[:, start if h.shape[1] > 1 else 0:] += alpha * v  # cached decode steps see 1 token
        return _replace(out, h.to(hs.dtype))
    ...  # register, yield, remove as above
```

- Directions: difference of class means at one layer (contrastive pairs), a Jacobian right
  singular vector, an SAE decoder row (`sae.W_dec[i]`), or a learned DAS direction.
- Scale: set alpha relative to the layer, not as a constant. The next block's norm divides by
  ‖h‖, so the effective push is about alpha/‖h‖, and ‖h‖ grows with depth. Sweep c in
  alpha = c · median‖h_L‖ (say c from 0.05 to 1 on a log grid) and also report alpha in units
  of the std of ⟨h, v⟩ over real data, so "steered 3 std beyond its natural range" is visible.
- `start=1` skips position 0: adding to a sink token can derail the whole sequence.
- Generation: with a KV cache every step after the prompt sees seq length 1, and that token is
  index 0 in the hook, hence the guard above. Without it, `start=1` silently steers the prompt
  only. Check by comparing cached and uncached greedy outputs on one prompt.
- Off-distribution checks, measured at every scale:
  - collateral damage: `interp.next_token_loss` on unrelated locked text, steered vs not;
  - KL(base ‖ steered) of next-token distributions on neutral prompts;
  - the norm of the steered residual against the distribution of natural norms;
  - a random unit direction at the same alpha (specificity), several seeds;
  - read the generations. A behaviour that only appears with incoherent text is disruption.
  Report the effect-vs-scale curve (`fig.line`), not one hand-picked alpha.

## Interchange interventions and DAS

An interchange intervention runs a base input, takes a representation from a source input, and
swaps it in. `patch(..., basis=Q)` above is one with a fixed subspace. Distributed Alignment
Search (DAS) learns the subspace: an orthonormal Q ∈ R^{d×k} is trained so that swapping PQ
from source into base makes the model output what a hypothesised high-level causal model
predicts for that base/source pair. Reach for it when:
- you have an explicit causal hypothesis with a variable that should be swappable (for
  example "the entity's attribute"), and counterfactual labels for pairs;
- the variable is plausibly distributed, not aligned with neurons, heads or a hand-built basis.

Hand-rolled DAS fits the lab style: `torch.nn.utils.parametrizations.orthogonal` on
`nn.Linear(d, k, bias=False)` keeps Q orthonormal, the hook applies h + QQᵀ(h_src − h), the model
stays frozen, and the loss is cross-entropy on the counterfactual label. Keep k small (1–16).

pyvene packages this with bookkeeping for positions, heads and components. The pattern from
the Orchestra files (check before use; argument names and the `interventions` dict keys differ
between their own examples, so print `intervenable.interventions.keys()`):

```python
import pyvene as pv
config = pv.IntervenableConfig(representations=[pv.RepresentationConfig(
    layer=8, component="block_output",
    intervention_type=pv.LowRankRotatedSpaceIntervention, low_rank_dimension=1)])
intervenable = pv.IntervenableModel(config, model)
optimizer = torch.optim.Adam(intervenable.get_trainable_parameters(), lr=1e-3)
_, out = intervenable(base=base_inputs, sources=[source_inputs],
                      unit_locations={"sources->base": ([[[p]]], [[[p]]])})
```

Cautions specific to learned subspaces:
- A trained Q can succeed by activating a dormant pathway rather than the one the model
  uses (the subspace-patching "interpretability illusion", Makelov et al. 2023). Test on held
  out pairs, compare against the same training on a random-init model, and check whether the
  found direction also varies naturally with the variable on unpatched data.
- Larger k fits more; report interchange accuracy against k, with a random Q of the same k.
- The Orchestra pyvene DAS tutorial trains a self-intervention toward a fixed token: that is
  steering by optimisation, not DAS, which needs base/source pairs and counterfactual labels.

Sources: Orchestra AI-Research-SKILLs 773a529 (MIT): pyvene/SKILL.md, pyvene/references/api.md, pyvene/references/tutorials.md, transformer-lens/references/tutorials.md, nnsight/references/tutorials.md, saelens/references/tutorials.md; lab `src/lab/interp.py`.
