# Control-Group Experiment: Genre and Language Discrimination in the 3⁹ Cognitive Space

**Status:** completed — v1.1 control study
**Date:** 2025-10-05
**Related:** `docs/reliability-report.md` (inter-annotator agreement), `examples/control-experiment/metrics.json`

---

## 1. Motivation

The inter-annotator reliability study (`docs/reliability-report.md`) showed that the 9-dimension rubric
`T1 T2 T3 S1 S2 S3 C1 C2 C3` (₃⁹ = 19,683-cell space) can be applied consistently by a single annotator
(k = 0.477 overall, T1 = 1.000, C1 = 0.868) when re-labeling the *Dream of the Red Chamber* (HLM) corpus.

A separate question remained: is the HLM fingerprint — entropy **1.3929**, 84 unique codes across 120 chapters,
triad entropy T≈1.4143 / S≈1.1550 / C≈1.5056, triad center (0,0,0) — **characteristic of this text**, or would
any novel land near the same coordinates? This control experiment answers that by running the identical
pipeline on two deliberately contrasting texts:

| Control | Language / era | Genre | Nodes | Sample |
| --- | --- | --- | --- | --- |
| `sanguoyanyi` | Classical Chinese, same dynasty-era register as HLM | historical/martial epic | 10 | chapters 1–10 |
| `baiyun-gudu` | Modern Chinese translation (Fan Ye) of Spanish (1967) | magic realism / modernist | 12 | chapter 1 (scenes) |

## 2. Method

1. **Text acquisition.** *Three Kingdoms* ch.1–10 from a public web edition (public domain, Luo Guanzhong);
   stored in `examples/sanguoyanyi/text/`. *One Hundred Years of Solitude* ch.1 (9,836 chars) located via
   public web reproduction of the Fan Ye translation; **used locally only, not committed** (copyright — see §5).
2. **Annotation.** Same rubric as HLM (`docs/mapping-guide.md`): one node per chapter (sanguo) / per scene
   (baiyun, 12 scene splits), each node assigned a 9-digit ternary coordinate → decimal code in [0, 19682].
   Files: `examples/sanguoyanyi/mapping/nodes.csv`, `examples/baiyun-gudu/mapping/nodes.csv`.
3. **Fingerprint.** `tri9cog fingerprint` → entropy (Shannon over unique codes), triad entropies, mode per
   dimension, triad center, turning points.
4. **Self-consistency.** `tri9cog blueprint --strategy isomorphic --nodes N` then `tri9cog verify`
   on the same nodes → the pipeline must reproduce itself (matched = N/N, mean Hamming = 0).
5. **Cross-discrimination.** For each control, a same-size blueprint is first generated from the HLM
   fingerprint (and the opposing control); then the control's nodes are verified against it. Low match +
   high mean Hamming distance = the fingerprints are text-specific, not genre-generic.

## 3. Results

### 3.1 Fingerprint comparison

| Metric | HLM (baseline, 120 ch) | Sanguo ch.1–10 | Baiyun ch.1 (12 scenes) |
| --- | --- | --- | --- |
| Nodes | 120 | 10 | 12 |
| Unique codes | 84 | 9 | 10 |
| Entropy H (bits) | **1.3929** | **1.4591** | **1.5391** |
| H(T) | 1.4143 | 1.5058 | 1.5245 |
| H(S) | 1.1550 | 1.2580 | 1.5391 |
| H(C) | 1.5056 | 1.1567 | 1.3844 |
| Triad center (mode) | (0,0,0) | (1,1,0) | (1,0,0) |
| Code range | [0, 18952] | [2919, 5457] | [973, 18945] |

**Reading.** HLM's entropy sits *below* both controls; the S (space) axis is the most compressed in HLM
(1.155) and the most dispersed in Baiyun (1.539), reflecting HLM's mostly static, domestic spatial structure
vs. the novel's world-spanning movement. Sanguo's C (causality) entropy is the lowest (1.157) — consistent
with its heavily character-driven, linear epic causality. The triad centers migrate from (0,0,0) in HLM
(outcome-driven inertia) toward (1,1,0) / (1,0,0) — i.e., controls are comparatively environment- and
mobility-driven.

### 3.2 Self-consistency

| Control | Verify vs own blueprint | Mean Hamming |
| --- | --- | --- |
| Sanguo ch.1–10 | 10/10 | 0.0 |
| Baiyun ch.1 | 12/12 | 0.0 |

The `fingerprint → blueprint → verify` loop is closed for both controls (as it was for HLM: 40/40 in v0.1),
confirming the metric is stable under isomorphic reproduction.

### 3.3 Cross-discrimination (vs HLM baseline and vs each other)

| Story nodes vs Target blueprint | Matched | Mean Hamming (of 9) | Entropy Δ (story − target) |
| --- | --- | --- | --- |
| Sanguo vs HLM(10) | 0/10 | **4.600** | −0.0484 |
| Baiyun vs HLM(12) | 0/12 | **5.083** | +0.0476 |
| Sanguo vs Baiyun(10) | 0/10 | **5.300** | −0.0810 |
| Baiyun vs Sanguo(12) | 0/12 | **5.333** | +0.1011 |
| *Self (both controls)* | *10/10, 12/12* | *0.0* | *0.0* |

**Reading.** Zero exact matches across all cross-pairs, with mean Hamming **4.6–5.3** (≈ half to more than
half of the 9 dimensions differ per node). The three texts occupy **disjoint neighborhoods** of the 19,683-cell
space; the fingerprint is discriminative at the level of individual works, not merely of "Chinese novels" or
"novels in general". The largest distance is sanguo↔baiyun (5.3), as expected from genre *and* language
differences; baiyun stays farther from HLM (5.08) than sanguo does (4.60), consistent with language/history
gradients (shared Classical-Chinese dynasty register narrows the gap, yet genre still separates them).

## 4. Conclusions

1. **Fingerprints are text-specific.** The HLM entropy 1.3929 and its (0,0,0) triad center are not generic;
   two contrasting controls both produce distinct fingerprints at statistically nontrivial Hamming distances.
2. **Genre and language leave separable traces.** Sanguo (same-era language, different genre) is closer to HLM
   than Baiyun (different language and century) is — but even sanguo is 0/10 matched, so genre itself shifts
   the coordinates meaningfully.
3. **Pipeline generalizes.** The same rubric, CLI and verification loop handle a classical epic and a
   modernist translation without modification, strengthening the framework's claim to be corpus-agnostic.

## 5. Copyright and reproducibility

- **Sanguo:** public domain (Luo Guanzhong, d. c. 1400); full text committed under `examples/sanguoyanyi/text/`.
- **Baiyun:** the Fan Ye translation (Nanhai, 2017) is **under copyright**. Only the abstract 9-dimension
  annotation, neutral scene labels and aggregate statistics are committed; **no translated text appears in the
  repository**. Annotation was performed locally from a public web reproduction (9,836 chars) for research
  discrimination purposes only.
- Reproduce: `tri9cog fingerprint examples/sanguoyanyi/mapping/nodes.csv` (and baiyun equivalent), then
  `tri9cog verify <nodes.csv> --target <blueprint.json>` with same-size blueprints as in §2.5.

## 6. Limitations

- Small sample: 10 (sanguo) and 12 (baiyun) nodes vs 120 (HLM); per-control entropy estimates have wider
  confidence bands. A longer baiyun excerpt or more chapters of sanguo would tighten estimates.
- Single annotator. Coordinates reflect one consistent reading; inter-annotator reliability (k = 0.477) was
  measured on HLM only, not on these controls.
- Mean Hamming is an average over nodes; it does not flag *which* dimensions drive separation per pair —
  a per-dimension disagreement breakdown is left as follow-up work.