# Jacobian subspaces between residual layers

The lab's core method. Helpers live in `lab.interp` (`~/src/labs/src/lab/interp.py`) (`jacobian`, `spectrum`,
`random_basis`, `ablate`, `next_token_loss`, `bootstrap`); the worked experiment is
`~/src/labs/templates/interp/experiment.py`. Extend those rather than writing new hooks.
What counts as evidence for a claim is the ml-research evidence standard
(`~/src/skills/skills/ml-research/references/mech-interp.md`); this file covers the method.

## What J measures

Let h_L[p] ∈ R^d be the residual after block L at position p (the lab convention: `layer L` =
output of block L = HF `hidden_states[L+1]` = TransformerLens `blocks.L.hook_resid_post`).
`interp.jacobian(model, tok, text, src, dst, pos)` returns

    J = ∂ h_dst[p] / ∂ h_src[p]   ∈ R^{d×d},   p = pos, evaluated at the clean h_src[p].

Only h_src at position p is freed; every other position keeps its clean value, and the
readout is the same position p. So J is the same-position Jacobian: it includes p attending to
its own key/value, but not how p's residual changes later positions q > p. For cross-position
influence you need ∂h_dst[q]/∂h_src[p], a different object (use a VJP from position q).

Structure worth keeping in mind:
- The skip path makes J = I + D, where D is the derivative of the writes of blocks src+1..dst.
  Directions the blocks ignore have gain ≈ 1, so the bulk of the spectrum sits near 1 and only
  the departures are informative. Also look at the SVD of J − I (what the blocks add).
- Pre-norm blocks read h through LayerNorm/RMSNorm. The LayerNorm Jacobian is
  diag(γ)/σ · (I − 11ᵀ/d − ĥĥᵀ/d), with ĥ = (h − μ1)/σ; RMSNorm's is diag(γ)/rms · (I − x̂x̂ᵀ/d).
  Both kill the radial direction (and LayerNorm also the all-ones direction), so the first
  block is blind to scaling h. Gains are also relative to ||h||, which grows with depth.
- Units: σ_i has units ||h_dst|| / ||h_src||. Normalise to σ₁ (as the template does) or to the
  norm ratio before comparing layers or models.

## Positions, prompts, averaging

- The template uses the last position of each prompt. Position 0 (BOS or the first token) often
  carries a huge-norm "sink" residual; exclude it from averages and treat it separately.
- Mean J then SVD (the template) finds directions whose input and output agree across prompts;
  sign or rotation differences between prompts cancel. The alternative without cancellation is
  the eigenbasis of G = (1/n) Σᵢ JᵢᵀJᵢ, i.e. the right singular vectors of the stacked matrix
  [J₁; …; Jₙ]/√n: v maximises the mean squared gain E‖Jᵢ v‖². If the two bases disagree, that
  itself is a finding (the map is prompt-specific).
- Prompts for building J and texts for measuring ablation should be disjoint. The template keeps
  them apart (`DEFAULT_PROMPTS` for J; `locked/eval.txt`, else `DEFAULT_EVAL`, for measuring).

## Cost

A full J costs one forward plus d reverse passes (one VJP per output row).
- `torch.autograd.functional.jacobian(f, x, vectorize=True)` batches the d VJPs with vmap:
  faster, memory ∝ d × activations. This is `interp.jacobian(..., vectorize=True)`.
- `torch.func.jacrev(f, chunk_size=c)` computes c rows per vmapped pass, trading memory for
  speed. `torch.func.jacfwd` does d JVPs instead (no stored activations; same count for square
  J). Check before use: vmap over a full HF forward can fail on in-place ops or fused attention
  kernels; the non-vectorised loop always works.
- When d is large (4096+) and you only need the top-k subspace, skip the full matrix.
  Randomised range finder with oversampling p ≈ 10: Y = JΩ with Ω ∈ R^{d×(k+p)} Gaussian
  (k+p JVPs via `torch.func.jvp`), Q = qr(Y); B = QᵀJ via k+p VJPs (row i = (Jᵀqᵢ)ᵀ);
  SVD of B gives σ and right singular vectors. One or two power iterations
  (Y ← J(JᵀY)) sharpen a slow decay. Cost ≈ 2(k+p)(q+1) passes instead of d.
- ‖J‖_F² = E_z ‖Jz‖² with z ~ N(0, I) (Hutchinson): a cheap check on how much gain the top-k
  directions carry, Σ_{i≤k} σᵢ² / ‖J‖_F².
- `torch.autograd.functional.jvp` uses the double-backward trick and is slower; prefer
  `torch.func.jvp`.

## Reading the SVD

`S, Vh = interp.spectrum(J)`: J = U diag(S) Vh. Rows of Vh (right singular vectors) are
orthonormal directions in src space; vᵢ is moved to σᵢ uᵢ in dst space. The top-k rows span the
k-dim input subspace of largest gain. The decay of σᵢ/σ₁ (plot with `log_y`) says how
low-rank the map is: a knee at small k suggests a small subspace carries most of the gain.
Gain is not use: a high-gain direction the data never occupies does nothing. Check the variance
of ⟨h_src, vᵢ⟩ over real activations next to σᵢ.

## Removing a subspace

With Q ∈ R^{d×k} orthonormal (`ablate` orthonormalises any basis via QR), P = QQᵀ:
- Projection (zero in the subspace): h ← (I − P)h. This is `interp.ablate`. It sets the
  coordinates to 0, which may be far from any value the model sees if the subspace has a mean.
- Mean ablation: h ← h − P(h − μ), with μ the mean residual over a reference set (per position
  if position matters). Removes variation only; usually the fairer "information removed" test.
- Resample ablation: h ← h − P(h − h′), h′ from another input. Keeps the subspace on
  distribution; with h′ from a counterfactual input it is subspace patching (`interventions.md`).
`ablate` hooks every position by default. The Jacobian was built at one position, so either say
that or pass `ablate(model, layer, basis, position=p)` to test exactly the position studied.

## Controls specific to this method

The evidence standard lists the general controls; these are the ones this method needs.
- Random bases of the same k: `interp.random_basis(d, k, seed)`, several seeds (the template
  uses 5; more when the gap is small). Report the Jacobian effect against their spread.
- Removed norm: the residual is anisotropic (outlier dimensions, a large mean), so top-J
  directions may just remove more norm. Log ρ = ‖P(h − μ)‖ / ‖h‖ per token for every basis.
  Stronger controls: random bases matched on removed variance, and the top-k PCA basis of the
  activations (the most variance any k-dim projection can remove). Beating PCA at equal k says
  the gain structure matters, not just variance.
- Random-init weights: rerun the pipeline on `AutoModelForCausalLM.from_config(config)` (same
  architecture, untrained). If its spectrum also concentrates, the shape comes from the
  architecture (norms, skip path), not learning. Plot both spectra on one `fig.line`.
- Matched prompts: build J on one set and test on a held-out set; for specificity, also test
  on matched texts that lack the behaviour (same length and domain).
- Linearisation: J is local. For a direction v and ε over a range (fractions to multiples of
  the std of ⟨h_src, v⟩), compare Δ(ε) = h_dst(h_src + εv) − h_dst(h_src) with εJv. Report
  ‖Δ(ε) − εJv‖ / ‖εJv‖ and the cosine between them. An ablation is a finite step of size
  ‖P(h − μ)‖, so check ε at that size; if the linear prediction fails there, describe the
  result as "ablating this subspace", not "the Jacobian predicts".

## Pitfalls

- HF `hidden_states[-1]` for GPT-2 (and many HF decoders) is after the final norm (`ln_f`).
  `interp.resid` and `interp.jacobian` read block outputs through a hook, so they stay pre-norm
  even for the last block; code that mixes them with `hidden_states` mixes two spaces there.
  TransformerLens `hook_resid_post` of the last block is pre-norm, like `interp.resid`.
- dtype: bf16 has about 3 significant digits, so σᵢ/σ₁ below ~1e-2 is noise. `interp.load`
  defaults to float32; keep it for Jacobians. `f` casts the free variable to the model dtype,
  so a bf16 model quantises every probe.
- Tokenisation: the same text gives different lengths across tokenisers; "last position"
  means a different token per model. Log the decoded token at p.
- Each VJP backpropagates through the whole prefix up to `dst`, so cost grows with prompt
  length; short prompts give many more Jacobians per GPU-hour.

Sources: Orchestra AI-Research-SKILLs 773a529 (MIT): transformer-lens/SKILL.md, transformer-lens/references/api.md, nnsight/references/tutorials.md; lab `src/lab/interp.py`, `src/lab/templates/interp/`.
