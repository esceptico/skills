# Tooling: which library for which job

Snippets marked "Orchestra" are copied from the Orchestra AI-Research-SKILLs files; those files
are not always consistent with each other or with current releases, so the version notes matter.
Pin versions in the experiment's `requirements.txt` and log them in the run.

| need | default | why |
|---|---|---|
| Jacobians, subspace ablation, patching, steering on HF models up to what fits on one GPU | plain torch hooks, `lib/interp.py` | exact HF weights, full autograd, no reimplementation to trust |
| models too large to host, forward-only questions | nnsight + NDIF | the same trace code runs remotely |
| head/neuron circuits, attention patterns, DLA, pretrained SAE hook names | TransformerLens | named hook for every activation |
| learned subspaces (DAS), shareable intervention configs | pyvene, or hand-rolled DAS | trainable rotations with position/head bookkeeping |
| pretrained SAEs as a basis or a control | SAELens | releases indexed by hook name |

## Plain torch hooks (lab default)

`interp.load(name)` loads float32, eval mode, frozen parameters; `interp.blocks(model)` finds the
block list for GPT-2 (`transformer.h`), Llama/Qwen/Mistral (`model.layers`), NeoX
(`gpt_neox.layers`) and multimodal wrappers (`model.language_model.layers`). A new family means
one more path there. Block outputs are a tuple in some transformers versions and a tensor in others;
`_hidden`/`_replace` handle both, so new hooks should use them. `from_pretrained(dtype=...)` needs
transformers >= 4.56 (older versions spell it `torch_dtype`).

## nnsight

```python
from nnsight import LanguageModel                          # Orchestra, nnsight>=0.5.0
model = LanguageModel("openai-community/gpt2", device_map="auto")
with model.trace("The Eiffel Tower is in"):
    h5 = model.transformer.h[5].output[0].save()           # Llama: model.model.layers[i]
    model.transformer.h[8].output[0][:] *= 0.5             # in-place edit = intervention
    logits = model.output.save()
with model.trace("The meaning of life is", remote=True):   # NDIF
    h40 = model.model.layers[40].output[0].save()
with model.session(remote=True):                           # several traces, one request
    ...
```
- Read values only through `.save()`; they are available after the `with` block exits.
- `output[0]` assumes the block returns a tuple. If your transformers version returns a tensor,
  `[0]` silently selects batch element 0. Print `model._model` and one output's shape first.
- Several prompts in one trace: `with model.trace() as tracer:` then `with tracer.invoke(text):`.
- NDIF: API key via `NDIF_API_KEY`. The Orchestra files give both `CONFIG.API_KEY = key` and
  `CONFIG.set_default_api_key(key)`; check which your version has. The hosted model list
  changes (Orchestra lists Llama-3.1 8B/70B/405B and DeepSeek-R1); check ndif.us.
- What runs remotely: traces, reads, in-place edits, patching across invokes, sessions.
  Gradients: Orchestra says `.retain_grad()`/`.backward()` are not supported for remote or vLLM
  execution; check current NDIF docs before planning anything autograd-based there. Without
  gradients, a Jacobian-vector product can still be estimated by central differences,
  Jv ≈ (f(h + εv) − f(h − εv)) / 2ε, two forwards per direction. In bf16 pick ε well above
  bf16 resolution of ‖h‖ and check that halving ε changes the estimate little.
- Generation with interventions: the Orchestra snippet calls `model.generate(...)` inside a
  `trace`; check the current nnsight docs for the generate context before use.
- `trace(..., timeout=300)` appears once in Orchestra; check before use.

## TransformerLens

```python
from transformer_lens import HookedTransformer             # Orchestra, transformer-lens>=2.0
model = HookedTransformer.from_pretrained("gpt2-small")
logits, cache = model.run_with_cache(tokens, names_filter=lambda n: "resid_post" in n)
logits = model.run_with_hooks(tokens, fwd_hooks=[("blocks.5.hook_resid_post", hook_fn)])
model.reset_hooks()                                        # hooks added with add_hook persist
```
- Hook fn signature is `hook_fn(activation, hook)`, returning the new activation.
- Lab `layer L` = `blocks.L.hook_resid_post` = `blocks.{L+1}.hook_resid_pre`.
- Families listed by Orchestra: GPT-2, LLaMA/Llama-2, Pythia, GPT-Neo/J, Mistral/Mixtral, Phi,
  Qwen, OPT, Gemma (50+ total). TL reimplements each model, so check its logits against HF on
  a few prompts before trusting a new or recent architecture. v3 (alpha) adds TransformerBridge
  for arbitrary modules; treat it as unstable.
- `from_pretrained` defaults to `fold_ln=True, center_writing_weights=True, center_unembed=True`.
  The function is unchanged but the residual basis is not HF's: centring should remove each
  residual vector's mean over d (verify on one prompt against HF minus its mean). Directions,
  Jacobians and norms from TL do not transfer to HF activations one for one; pass the three
  flags as False when comparing with lab hooks.
- `hook_resid_post` of the last block is before `ln_final`; HF `hidden_states[-1]` is after.

## pyvene

`import pyvene as pv` (Orchestra, pyvene>=0.1.8). Pattern: `pv.IntervenableConfig(representations=
[pv.RepresentationConfig(layer, component, intervention_type, ...)])`, `pv.IntervenableModel(
config, hf_model)`, then `_, out = intervenable(base=..., sources=[...], unit_locations=...)`.
Components include `block_output`, `mlp_output`, `attention_output`, `head_attention_value_output`.
Intervention types include `VanillaIntervention`, `AdditionIntervention`, `ZeroIntervention`,
`CollectIntervention`, `LowRankRotatedSpaceIntervention` (DAS). See `interventions.md` for
when it earns its keep. Several Orchestra examples look inconsistent (intervention dict keys, a
causal-tracing loop whose base and source are both the clean input); treat them as shapes.

## SAELens

```python
from sae_lens import SAE
loaded = SAE.from_pretrained("gpt2-small-res-jb", "blocks.8.hook_resid_pre")  # device="cuda" optional
sae = loaded[0] if isinstance(loaded, tuple) else loaded   # as in interp.sae_basis
feats = sae.encode(acts)   # [..., d_sae];  sae.decode(feats) -> [..., d_in];  sae.W_dec: [d_sae, d_in]
```
- Return type: older releases return `(sae, cfg_dict, sparsity)`; 6.x returns the SAE alone
  (the tuple moved to a separate method; check its name in your version). The Orchestra files
  declare `sae-lens>=6.0.0` yet unpack three values in most examples, so the isinstance guard
  in `interp.sae_basis` is the safe form.
- Hook site: `blocks.8.hook_resid_pre` is lab `layer 7`. SAEs trained on TransformerLens
  activations saw the processed (centred) residual; for HF activations, subtract each vector's
  mean over d first, and check `sae.cfg` for an activation normalisation setting.
- Training config fields (`architecture`, `l1_coefficient`, `hook_layer`, ghost grads) in the
  Orchestra examples follow the pre-6 flat `LanguageModelSAERunnerConfig`; check before use.

SAE health, measured on your own held-out text at the site you use:
- L0: mean number of active features per token, `(feats > 0).sum(-1).float().mean()`.
- Reconstruction: explained variance 1 − ‖x − x̂‖² / ‖x − x̄‖², and loss recovered
  (L_zero − L_sae) / (L_zero − L_clean), where L_sae is next-token loss with x̂ spliced in (a hook
  returning `sae.decode(sae.encode(h))`) and L_zero with zero ablation at that site.
- Dead features: never active over a large token sample (say 10⁶ tokens); report the fraction.
- Orchestra's rough targets (L0 50–200, loss recovered 80–95%, dead < 5%) depend on width and
  architecture. What matters for a control is that the SAE is healthy on your data: a basis
  that reconstructs poorly there is a weak comparison.

Sources: Orchestra AI-Research-SKILLs 773a529 (MIT): nnsight/SKILL.md, nnsight/references/{README,api,tutorials}.md, transformer-lens/SKILL.md, transformer-lens/references/{README,api,tutorials}.md, pyvene/SKILL.md, pyvene/references/{README,api,tutorials}.md, saelens/SKILL.md, saelens/references/{README,api,tutorials}.md; lab `lib/interp.py`, `templates/interp/requirements.txt`.
