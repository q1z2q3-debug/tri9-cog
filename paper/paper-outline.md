# A Ternary Cognitive Space for Literary Structure: Mapping, Fingerprinting, and Replication

**Paper Outline & Writing Plan** — v0.1 (draft for the tri9-cog open-source repository)

---

## Metadata

| Field | Value |
| --- | --- |
| Working title | A Ternary Cognitive Space for Literary Structure: Mapping, Fingerprinting, and Replication |
| Chinese title | 三元九维认知空间：文学结构的映射、指纹与再创作 |
| Author | RUNZEAI |
| Corresponding email | `q1z2q3@gmail.com` (identical to Zenodo archive metadata) |
| Framework | Ternary Cognitive Space (3 axes × 9 dimensions × 3 states = 3⁹ = 19,683 cells, codes 0–19,682) |
| Core datasets | Hongloumeng (120 chapters, 84 unique codes, entropy H ≈ 1.3929) · Tingyunlou (isomorphic re-creation) |
| Primary venues | JCLS (Journal of Computational Literary Studies) · DSH · DH annual conference · (secondary: ICCC) |
| License | MIT (data under CC-BY 4.0 plan) |

---

## Motivation (one sentence)

> We turn literary narrative analysis into a computable, reproducible formal framework — mapping stories into a 19,683-cell ternary cognitive space, fingerprinting their structure, and using a full 120-chapter corpus plus one isomorphic new work for bidirectional validation.

---

## Nine-Section Structure & Writing Plan

### 1. Introduction
- **Status: to write (draft exists in README / docs/framework.md)**
- Problem: literary structure analysis is often qualitative and non-reproducible.
- Contribution summary:
  1. A formal framework (3 axes × 9 dimensions × 3 states) with a fixed encoding formula;
  2. A complete 120-chapter mapping of *Hongloumeng* with quantitative fingerprint (entropy, modes, turning points);
  3. A replication protocol (blueprint → new fiction → verify) demonstrated by *Tingyunlou*;
  4. An open-source CLI + benchmark data (this repository).
- Paper roadmap statement.

### 2. Related Work
- **Status: to write (requires literature search)**
- Computational narratology: story graphs (Moretti), scene networks, actantial models.
- Stylometry & digital humanities: stylo / rolling delta, topic modeling, sentiment arcs (e.g., "The Bestseller Code").
- Formal frameworks for narrative: Propp morphology, Labov narrative units, Cambria's sentiment/plot space.
- Gap: no widely-adopted *cognitive*-flavored ternary coding that is both low-dimensional (9 dims) and fully enumerable (19,683 cells) with an inverse map (code → coordinate → story node).

### 3. The Ternary Cognitive Space Framework
- **Status: ready (docs/framework.md), needs formalization language**
- Definitions:
  - Three axes: T = Temporality (时序), S = Spatiality (空间), C = Causality/Valuation (因果价值);
  - Nine dimensions (each axis 3 dims): T1–T3, S1–S3, C1–C3, each taking states {0, 1, 2};
  - Coordinate notation `T1T2T3-S1S2S3-C1C2C3`; code = T1·3⁸ + T2·3⁷ + … + C3·3⁰ ∈ [0, 19682].
- Judgment criteria table for the nine dimensions (the annotation rubric).
- Four-step mapping protocol: segment nodes → annotate dimensions → encode & archive → chain the trajectory.
- Formal properties: bijection, Hamming distance between nodes, per-dimension mode, entropy (Shannon, log2).

### 4. Mapping Methodology
- **Status: ready (docs/mapping-guide.md) + needs inter-annotator agreement**
- Segmentation & annotation protocol (half-automatic; template CSV via CLI `tri9cog template`).
- **Inter-annotator reliability (P0, must-do before submission)**: a second annotator independently labels 10–20 chapters sampled across the corpus; report Cohen's κ and per-dimension agreement rates. Fallback: author-authorized rule-based re-check (semi-supervised) if no second human annotator is available.
- Data hygiene: coordinate CSV + code JSON published as open benchmark (see Appendix).

### 5. Empirical Case Study: Hongloumeng
- **Status: ready (examples/hongloumeng/*) — results verified against the engine**
- Corpus: 120 chapters (public-domain edition, source documented).
- Results: 120 nodes → 84 unique codes; entropy H ≈ 1.3929 (observed) vs uniform upper bound log₂3 ≈ 1.58496; triad entropies T ≈ 1.4143 / S ≈ 1.1550 / C ≈ 1.5056; central tendency "daily-life tragedy" (重心 0/0/0).
- Turning-point analysis: 116→117 (9 dims), 115→116 (8), 5→6 (8), 119→120 (7), 118→119 (7) — alignment with the narrative climax (chapters 96–119).
- Character trajectories & distribution analysis (six analysis modes).

### 6. Replication: from Blueprint to New Fiction
- **Status: ready (docs/replication-guide.md, examples/tingyunlou/, CLI verified)**
- Blueprint strategies: isomorphic (copy path) / mirror (0↔2 per axis) / variation (vary chosen dims, seeded).
- Closed loop: `tri9cog fingerprint` → `blueprint` → write new fiction → `verify` (per-node Hamming distance, entropy delta, mode delta, turning-point hits).
- Case: *Tingyunlou* — full isomorphic re-creation workflow with verification report.
- Optional: LLM text-generation interface (planned v0.3) using the coordinate blueprint as a hard constraint.

### 7. Discussion
- **Status: to write**
- Discriminative power: run 1–2 control novels (e.g., *Sanguo Yanyi* excerpt, *One Hundred Years of Solitude* excerpt) through the same pipeline and show distinct fingerprints (entropy / mode / turning signatures differ across structural types).
- Limitations: annotation subjectivity without κ; semantic quality of generated text; Chinese-corpus scope; scaling to short stories & non-narrative forms.
- Threat to validity & how the open benchmark mitigates it.

### 8. Conclusion
- **Status: to write**
- Summary of contributions; roadmap to v1.0 (batch replication workflow); invite community annotation & extensions (multi-language corpora).

### 9. Appendix
- **Status: partially ready (data files in examples/) — needs packaging**
- A: full 120-chapter mapping table (chapter, title, coordinate, code) — CSV in `examples/hongloumeng/mapping/nodes.csv`;
- B: fingerprint JSON (`fingerprint.json`) with entropy/modes/turning points;
- C: annotation rubric & expanded per-dimension examples;
- D: replication blueprint sample (`blueprint.json`, mirror strategy, 40 nodes);
- E: Zenodo DOI plan for the final data archive (Zenodo token available; archive metadata uses corresponding email `q1z2q3@gmail.com`).

---

## Writing Plan & Milestones

| Stage | Deliverable | Status |
| --- | --- | --- |
| 0 (now) | Open repository: framework docs + Hongloumeng data + Tingyunlou case | ✅ done (this repo) |
| 1 | **Inter-annotator reliability** (κ on 10–20 chapters) | ⏳ pending — authorized sampling, awaiting execution |
| 2 | **Control experiment** (1–2 control novels through pipeline) | ⏳ pending |
| 3 | Write sections 3–6 first (framework/mapping/case/replication, data-backed) | next, after open-sourcing |
| 4 | Literature search & draft sections 1–2, 7–8 | after data sections |
| 5 | Package appendix as open benchmark + Zenodo archive (DOI) | before submission |
| 6 | Submit to JCLS or DH (annual conference); roadmap after reviews | target timeline: see below |

**Target timeline (indicative):** open-source repo (this commit) → reliability & control experiments (weeks 1–4) → full draft (weeks 5–10) → Zenodo archive & submission (weeks 11–14).

---

## Open Questions for the Owner
1. Second annotator: use an invited human annotator, or authorize rule-based re-annotation by the assistant (per the default decision: proceed with rule-based sampling)?
2. Control corpus: which excerpt lengths and which novels (default: *Sanguo Yanyi* ch. 1–10 excerpt + *One Hundred Years of Solitude* ch. 1 excerpt)?
3. Language of the final manuscript: English (default, per prior preference) with Chinese abstract + Chinese title as appendix metadata?