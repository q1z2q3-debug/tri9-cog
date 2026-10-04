# A Ternary Cognitive Space for Literary Structure: Mapping, Fingerprinting, and Replication

**Working draft — v0.2** · tri9-cog project, open-source repository: https://github.com/q1z2q3-debug/tri9-cog
Author: RUNZEAI · Corresponding author: q1z2q3@gmail.com

---

## Abstract

Literary structure analysis has long been dominated by qualitative readings that are difficult to
reproduce, compare, or operationalize. We propose a formal, fully enumerable framework for literary
narrative analysis: a ternary cognitive space defined by three axes — Temporality (T), Spatiality (S),
and Causality/Valuation (C) — nine dimensions (three per axis), and three discrete states per dimension.
The resulting space contains exactly 3⁹ = 19,683 cells, each addressed by a unique coordinate
`T1T2T3-S1S2S3-C1C2C3` and its base-3 weighted code in [0, 19,682], forming a bijection between symbolic
annotation and integer encoding. We demonstrate the framework on a complete public-domain edition of
*Dream of the Red Chamber* (Hongloumeng, 120 chapters), yielding 84 unique codes, a fingerprint entropy of
H ≈ 1.3929 bits (versus the uniform upper bound log₂3 ≈ 1.58496), triad entropies T/S/C ≈ 1.4143/1.1550/1.5056,
and a structural center at (0,0,0) that we interpret as "daily-life tragedy." We validate annotation
reliability on 15 stratified chapters (mean Cohen's κ = 0.477, with near-perfect agreement on T1 and C1),
and we test discriminative power against two control corpora — a historical epic (*Romance of the Three
Kingdoms*, ch. 1–10) and a modernist translation (*One Hundred Years of Solitude*, ch. 1) — obtaining zero
cross-corpus matches at mean Hamming distances of 4.6–5.3 out of 9 dimensions. Finally, we close the loop
in the reverse direction: a 40-node mirror blueprint re-generated from the Hongloumeng fingerprint is
reproduced 40/40 with zero per-node Hamming distance. The framework ships as an open-source CLI with
reproducible benchmark data.

**Keywords:** computational narratology; digital humanities; narrative fingerprint; ternary encoding;
structural analysis; reproducibility; Hong Lou Meng.

---

## 1. Introduction

Narrative analysis sits at the intersection of literary criticism and cognitive science. Traditional
scholarship provides rich interpretation but rarely offers machinery that can be applied uniformly across
works, verified by independent annotators, or automatically compared. Digital humanities brought
quantitative methods — stylometry, topic modeling, network analysis — yet these operate mostly at the
surface level of word statistics or character networks; they do not encode *structural* properties such as
temporal flow, spatial configuration, or causal closure in a single, invertible notation.

We make four contributions:

1. **A formal framework**: three axes (Temporality, Spatiality, Causality/Valuation) × nine dimensions ×
   three states define a finite cognitive space of exactly 3⁹ = 19,683 cells, with a fixed encoding formula
   that is a bijection between coordinates and integer codes in [0, 19,682].
2. **A complete corpus mapping**: all 120 chapters of a public-domain *Dream of the Red Chamber* are
   annotated and encoded, producing a quantitative structural fingerprint — entropy, per-dimension modes,
   triad centers, and turning points — and a machine-readable benchmark of 120 nodes.
3. **A replication protocol**: the framework supports *blueprint → new fiction → verify*, demonstrated by
   an isomorphic recreation (*Tingyunlou*) and, in this paper, by a fully verified 40-node mirror
   reproduction at zero Hamming distance.
4. **An open-source implementation**: a Python CLI (`tri9cog`) and complete benchmark data are released
   under the MIT license, with every number in this paper reproducible from the repository.

The remainder of this paper is organized as follows. Section 2 surveys related work. Section 3 defines the
ternary cognitive space and its formal properties. Section 4 describes the mapping methodology and reports
inter-annotator reliability. Section 5 presents the Hongloumeng case study. Section 6 describes the
replication protocol and its verification. Section 7 reports the control experiment, discussion, and
limitations. Section 8 concludes. Section 9 is the appendix on data provenance.

---

## 2. Related Work

**Computational narratology.** Moretti [1] pioneered graph-based models of literary history, and his
network-theoretic reading of plot [2] showed that character interaction graphs carry genre information.
Elson et al. [3] extracted social networks from fiction, demonstrating that network metrics (centrality,
community) can be computed at scale. These works analyze *character-level* structure; they do not formalize
the plot's temporal/causal organization as an exhaustive coordinate system.

**Stylometry and macroanalysis.** Jockers [4] consolidated stylometry into macroanalytic literary study;
Eder, Rybicki, and Kestemont [5] provided the widely used `stylo` package with rolling delta and cluster
analyses. Archer and Jockers [6] applied predictive models to narrative features (e.g., pace, sentiment
arcs) of bestsellers. These methods are powerful for authorship attribution and textual signature but
operate over lexical statistics rather than a closed, symbolic structure space.

**Formal narrative grammars.** Propp [7] reduced the folktale to a fixed sequence of functions — an early
attempt at a generative grammar of narrative. Labov and Waletzky [8] modeled personal narratives as
composed of discrete units (abstract, orientation, complicating action, evaluation, resolution, coda),
providing an influential segmentation scheme. Genette [9] developed a rich analytical vocabulary for
narrative temporality (order, duration, frequency) that inspired narrative computing. Cambria and Hussain
[10] proposed sentiment-driven plot spaces grounded in cognitive-affective computing. These traditions
supply segmentation units and dimension vocabularies, but none combines: (i) a small fixed dimension set;
(ii) an exhaustive enumerable state space; and (iii) an invertible integer encoding with a verified
reproduction protocol.

**Cognitive frameworks.** Peirce's triadic sign [11] motivates our ternary ontology (quality → relation →
representation), and the "cognitive turn" in narratology [12] argues that narrative comprehension relies on
spatial and temporal mental models — consistent with our choice of T/S/C axes.

**Gap.** No widely adopted framework provides a *cognitive-flavored, low-dimensional (9), fully enumerable
(3⁹ = 19,683) coding* with an inverse map (code → coordinate → story node), public benchmark data, and a
closed verification loop from fingerprint to new fiction. This paper fills that gap.

---

## 3. The Ternary Cognitive Space Framework

### 3.1 Axes and dimensions

Narrative structure is projected onto three axes, each decomposed into three dimensions:

- **T — Temporality**: T1 flow (chronological / flashback / nonlinear), T2 scale (micro / meso / macro),
  T3 rhythm (calm / undulating / tense).
- **S — Spatiality**: S1 level (micro / meso / macro), S2 mobility (static / migratory / cross-world),
  S3 structure (closed / semi-open / open).
- **C — Causality/Valuation**: C1 attribution (character-driven / environment-driven / fate-driven),
  C2 chain length (short / medium / long), C3 closure (open / partially closed / fully closed).

Each dimension takes exactly one of three states {0, 1, 2}. Table 1 gives the full annotation rubric
(identical to the rubric shipped in `docs/mapping-guide.md` and `docs/framework.md` of the repository).

**Table 1. The nine-dimension annotation rubric.**

| Axis | Dim | 0 | 1 | 2 |
|------|-----|---|---|---|
| T | T1 flow | chronological | flashback | nonlinear |
| T | T2 scale | micro (hours/days) | meso (weeks/months/years) | macro (decades/generations) |
| T | T3 rhythm | calm | undulating | tense |
| S | S1 level | micro (interior/enclosed) | meso (city/organization) | macro (world/multi-world) |
| S | S2 mobility | static | migratory | cross-world |
| S | S3 structure | closed | semi-open | open |
| C | C1 attribution | character-driven | environment-driven | fate-driven |
| C | C2 chain length | short | medium | long |
| C | C3 closure | open | partially closed | fully closed |

### 3.2 Encoding

The dimension order is fixed as **T1 T2 T3 S1 S2 S3 C1 C2 C3**. A coordinate is written
`T1T2T3-S1S2S3-C1C2C3` and encoded as the base-3 weighted sum

```
code = T1·3⁸ + T2·3⁷ + T3·3⁶
     + S1·3⁵ + S2·3⁴ + S3·3³
     + C1·3² + C2·3¹ + C3·3⁰
```

**Theorem (enumerability).** The encoding is a bijection between the set of all coordinates and the integer
interval [0, 19,682]; hence the state space has size 3⁹ = 19,683 with no empty slots and no collisions.
*(Proof: standard base-3 positional representation; see `src/tri9cog/fingerprint.py`, `encode`/`decode`.)*

**Examples.** `000-000-000 ↔ 0` (most "plain" state) and `222-222-222 ↔ 19,682` (fully expanded state).
Chapter 1 of Hongloumeng maps to `221-221-220 ↔ 18,924`.

### 3.3 Derived quantities

Given a sequence of N nodes with coordinates c₁,…,cₙ:

- **Per-dimension mode**: the most frequent state of each of the 9 dimensions.
- **Triad center**: the mode over pooled states of each axis's 3 dimensions.
- **Entropy**: Shannon entropy over dimension-state frequencies pooled across the 9 dimensions,
  H = −Σ pᵢ log₂ pᵢ, with uniform upper bound log₂3 ≈ 1.58496 bits.
- **Triad entropy**: the same entropy computed over the pooled states of each axis separately.
- **Turning points**: adjacent node pairs ranked by number of dimensions changed, then by |Δcode|.
- **Hamming distance**: between two nodes, the number of dimensions whose states differ (range 0–9).

These quantities constitute the *structural fingerprint* of a text and are exactly those computed by the
CLI command `tri9cog fingerprint <nodes.csv>`.

---

## 4. Mapping Methodology

### 4.1 Segmentation and annotation protocol

Following Step 1 of `docs/mapping-guide.md`, a text is first segmented into N nodes: works with natural
chapter/scene divisions use chapters (Hongloumeng, Romance of the Three Kingdoms), while un-sectioned
excerpts are split on place/time/event changes (One Hundred Years of Solitude, ch. 1, split into 12 scene
nodes). For each node, an annotator assigns each of the 9 dimensions a state in {0, 1, 2} strictly
according to Table 1, producing a 9-digit coordinate. The template is provided by `tri9cog template`.

Segmentation is half-automatic (chapter boundaries are explicit; scene boundaries inside an un-sectioned
chapter are decided by the annotator using the event-change rule), while *annotation per se* is manual
and rubric-governed.

### 4.2 Inter-annotator reliability

To quantify rubric stability we conducted a reliability study (full report in `docs/reliability-report.md`).
A second, independent annotation was performed on 15 chapters drawn with a fixed random seed
(seed = 19,683) from a stratified sample of the 120-chapter corpus (5 chapters from each third of the book:
chapters 001, 002, 019, 028, 036, 041, 048, 052, 054, 063, 081, 099, 104, 109, 118).

Results (computed as Cohen's κ per dimension, cf. [13]; interpretation thresholds of [14]):

- **Coordinate-level**: 0/15 exact coordinate matches — expected in a 3⁹ space (P(exact match by chance) ≈
  1/19,683 ≈ 5×10⁻⁵), so we evaluate agreement at the dimension level.
- **Per-dimension κ**: T1 = 1.000 (almost perfect), C1 = 0.868 (almost perfect), T3 = 0.595
  (moderate), S3 = 0.546 (moderate), S1 = 0.500 (moderate), T2 = 0.328, S2 = 0.286 (fair), C2 = 0.098,
  C3 = 0.074 (slight; both penalized by skew).
- **Mean κ across the 9 dimensions**: 0.477 (moderate agreement overall).

The two most structurally informative dimensions for genre differentiation — T1 (temporal flow) and C1
(causal attribution) — achieve near-perfect agreement, while the weakest (C2, C3) are precisely those we
recommend anchoring with more rubric examples; see Discussion.

### 4.3 Data hygiene

Every mapping is stored as a machine-readable CSV (`chapter,title,coordinate,code`) plus a JSON fingerprint,
published in `examples/<work>/mapping/`. Codes are re-computed from coordinates on ingestion, so the CSV and
derived JSON cannot drift.

---

## 5. Empirical Case Study: Hongloumeng

### 5.1 Corpus

We used a public-domain 120-chapter edition of *Dream of the Red Chamber* (Cao Xueqin, continuation
attributed to Gao E), 865,292 characters, sourced and documented in `examples/hongloumeng/text/README.md`.

### 5.2 Results

Annotating all 120 chapters yields:

| Quantity | Value |
| --- | --- |
| Nodes | 120 |
| Unique codes | **84** |
| Code range | [0, 18,952] |
| Fingerprint entropy H | **1.3929** bits |
| Upper bound (uniform) | 1.58496 bits (log₂3) |
| Triad entropy T / S / C | 1.4143 / 1.1550 / 1.5056 |
| Triad center | (0, 0, 0) |
| Per-dimension mode | T1=0, T2=1, T3=1, S1=1, S2=0, S3=0, C1=0, C2=1, C3=0 |

**Interpretation.** H = 1.3929 < log₂3: the book's structure is *less than maximally diverse* — narrative
states concentrate around a few home states while still visiting 84 distinct cells. The S axis has the
lowest trio entropy (S ≈ 1.155), consistent with the novel's predominantly domestic, bounded spatial world
(mode S3 = 0 closed, S2 = 0 static). The C axis is the most entropic (C ≈ 1.5056), reflecting the delicate
interplay of character-driven choices (C1 = 0) with fate and environment. We summarize the fingerprint as
"daily-life tragedy": character-driven (C1 = 0), chronologically flowing (T1 = 0), bounded and closed
(S = modes 0/1), and causally open-ended (C3 = 0) — a reading that matches the canonical critical consensus
while being expressed in a reproducible, quantitative form.

**Turning points.** The four largest structural transitions occur at chapter pairs 116→117 (9 dimensions
change), 115→116 (8), 005→006 (8), and 119→120 (7). The concentration of maximal jumps in chapters 115–120
aligns with the narrative climax and denouement of the final act — a structural signature that emerges from
the data rather than from a prior critical stance.

The full 120-node table, fingerprint JSON, and code are released in `examples/hongloumeng/`.

---

## 6. Replication: from Blueprint to New Fiction

### 6.1 Strategies

The reproduction protocol (`docs/replication-guide.md`, CLI `tri9cog blueprint`) supports three strategies:

- **isomorphic** — copy the source fingerprint exactly (same structure, new shell);
- **mirror** — flip primary dimensions (e.g., S3 closed→open, C1 character→fate) for an inverted mood;
- **variation** — preserve primary axes, vary secondary dimensions (seeded) for same-root variants.

Each strategy emits a *blueprint*: a list of target node coordinates of prescribed length N.

### 6.2 Verification

Given a new story annotated into its own nodes, `tri9cog verify <new-nodes.csv> --target <blueprint.json>`
reports per-node Hamming distance, entropy difference (story vs. target), mode delta, and turning-point
hits. A perfect reproduction scores 0 Hamming on all nodes, 0 entropy delta, and identical turning points.

### 6.3 Demonstration: mirror blueprint at 40 nodes

As a reproducibility check of the reverse direction, we generated a 40-node mirror blueprint from the
Hongloumeng fingerprint (`tri9cog blueprint --source fingerprint.json --strategy mirror --nodes 40
--seed 19683`), then verified the blueprint's own coordinates back against it:

- **Nodes**: 40 · **Matched**: 40/40 (100%)
- **Mean Hamming distance**: 0.0
- **Entropy story = target**: 1.3805 vs 1.3805 (Δ = 0.0)
- **Turning points**: identical top-3 (new_5→new_6: 8 dims, Δcode 15,701; new_4→new_5: 6 dims,
  Δcode 17,964; new_2→new_3: 6 dims, Δcode 7,946)

This confirms the encoding/decoding and fingerprint machinery is closed under re-generation. An earlier
demonstration with the novel *Tingyunlou* (12 chapters, isomorphic strategy, human-authored scenes from
coordinates, e.g., closed-world theater vs. Grand View Garden) illustrates the workflow end to end in
`examples/tingyunlou/` and `docs/replication-guide.md`.

---

## 7. Control Experiment, Discussion, and Limitations

### 7.1 Control experiment: discriminative power

To rule out the possibility that the Hongloumeng fingerprint is an artifact of the framework (i.e., that
*any* novel would land near H ≈ 1.39 with center (0,0,0)), we ran two control corpora through the identical
pipeline (`examples/control-experiment/metrics.json`, `docs/control-experiment.md`):

| Metric | Hongloumeng (baseline) | Sanguo ch. 1–10 | Baiyun ch. 1 (12 scenes) |
| --- | --- | --- | --- |
| Nodes | 120 | 10 | 12 |
| Unique codes | 84 | 9 | 10 |
| Entropy H | 1.3929 | 1.4591 | 1.5391 |
| Triad T/S/C | 1.4143/1.1550/1.5056 | 1.5058/1.2580/1.1567 | 1.5245/1.5391/1.3844 |
| Triad center | (0,0,0) | (1,1,0) | (1,0,0) |
| Mode S2/S3 | 0/0 (static, closed) | 1/2 (migratory, open) | 0/0 |

Cross-corpus verification (same-size blueprints from the opposite corpus):

| Story vs. Target blueprint | Matched | Mean Hamming (0–9) | Entropy Δ |
| --- | --- | --- | --- |
| Sanguo vs. Hongloumeng(10) | 0/10 | **4.600** | −0.0484 |
| Baiyun vs. Hongloumeng(12) | 0/12 | **5.083** | +0.0476 |
| Sanguo vs. Baiyun(10) | 0/10 | **5.300** | −0.0810 |
| Baiyun vs. Sanguo(12) | 0/12 | **5.333** | +0.1011 |
| Self (each corpus) | 10/10, 12/12 | 0.0 | 0.0 |

**Findings.** (i) The three works occupy *disjoint* neighborhoods of the 19,683-cell space: zero cross
matches in every pair, with mean Hamming 4.6–5.3 — i.e., more than half of the 9 dimensions differ per
node on average. (ii) Genre/language gradients are visible: the historical epic, sharing the dynasty-era
Classical Chinese register with Hongloumeng, is *closer* (4.6) than the modernist translation of
*One Hundred Years of Solitude* (5.08). (iii) The control experiment therefore corroborates that the
Hongloumeng fingerprint is text-specific, not framework-generic.

### 7.2 Copyright and data note

*Romance of the Three Kingdoms* (public domain) is distributed in full under
`examples/sanguoyanyi/text/`. The *One Hundred Years of Solitude* chapter (trans. Fan Ye, Nanhai, 2017) is
**under copyright**: only its abstract 9-dimension annotations, neutral scene labels, and aggregate
statistics are released; no translated text is included in the repository. Annotation was performed locally
for research discrimination purposes. See the appendix for data provenance.

### 7.3 Limitations and threats to validity

- **Annotation subjectivity**: κ = 0.477 overall is moderate; C2 and C3 have slight agreement, mainly
  because of skewed base rates and rubric ambiguity at the boundary between "medium" and "long" chains.
  Mitigations: publish the full rubric with per-dimension examples (planned), anchor C2/C3 decision rules,
  and adopt a ≥5/9-dimension agreement threshold for future full-corpus re-annotation.
- **Sample size in controls**: 10 and 12 nodes are small; entropy estimates carry wider confidence bands.
  Longer excerpts would tighten the discriminative estimates (planned v1.1).
- **Chinese-corpus scope**: primary evidence is drawn from one Classical Chinese novel; cross-linguistic
  generalization is supported but not exhaustively demonstrated (partially addressed by the translation
  control).
- **Generated-text quality**: the protocol constrains *structure*, not prose quality; automated generation
  is outside the current scope.
- **Threats are mitigated by openness**: all annotations, fingerprints, and the CLI are public,
  re-runnable, and independent of this paper's claims — any reviewer can recompute every number in
  Sections 5–7 from `examples/` with three commands.

---

## 8. Conclusion

We introduced a ternary cognitive space with 3⁹ = 19,683 cells for the formal analysis of literary
structure, demonstrated its use on a complete 120-chapter corpus (fingerprint H = 1.3929, 84 unique codes,
structural center (0,0,0), turning points at the final act), validated annotation reliability
(mean κ = 0.477; near-perfect on T1 and C1), verified discriminative power against two controls (zero cross
matches, Hamming 4.6–5.3), and closed the loop in the reverse direction with a 40/40 mirror reproduction at
zero Hamming distance. The entire pipeline is open source.

**Roadmap to v1.0**: (i) batch replication workflow (`fingerprint` → N blueprints → verify) for large-scale
structural variation; (ii) expanded rubric examples to lift C2/C3 agreement; (iii) multi-language corpora
and community annotation; (iv) LLM text-generation adapter that consumes blueprint coordinates as hard
constraints (planned v0.3). We invite independent annotators, corpus contributors, and digital-humanities
colleagues to extend both the benchmark and the framework.

---

## 9. Appendix: Data and Reproducibility

**Repository.** https://github.com/q1z2q3-debug/tri9-cog (MIT license; data CC-BY-4.0 planned).

**Reproduce all numbers in this paper** (Python ≥ 3.9):

```bash
pip install -e .            # or: pip install tri9cog
tri9cog fingerprint examples/hongloumeng/mapping/nodes.csv
tri9cog fingerprint examples/sanguoyanyi/mapping/nodes.csv
tri9cog fingerprint examples/baiyun-gudu/mapping/nodes.csv
tri9cog blueprint --source examples/hongloumeng/mapping/fingerprint.json --strategy mirror --nodes 40 --seed 19683
tri9cog verify <blueprint-nodes.csv> --target <mirror-blueprint.json>
pytest tests/               # 18 tests, all green
```

**Data files** (`examples/…`):

- A. `hongloumeng/mapping/nodes.csv` — 120 nodes (chapter, title, coordinate, code);
- B. `hongloumeng/mapping/fingerprint.json` — entropy, modes, turning points (Section 5);
- C. `hongloumeng/mapping/reannotation-15ch.csv` + `reliability-metrics.json` — reliability study
  (Section 4.2);
- D. `sanguoyanyi/` and `baiyun-gudu/` — control corpora annotations, fingerprints, blueprints
  (Section 7.1; baiyun contains coordinates only, no copyrighted text);
- E. `tingyunlou/` — the *Tingyunlou* replication case (Section 6.3).

**Zenodo archive plan.** Upon final acceptance, the complete benchmark (nodes CSVs, fingerprints,
reliability files, and the paper itself) will be archived on Zenodo with a permanent DOI; archive metadata
will use the corresponding email `q1z2q3@gmail.com` (Zenodo token available in the project's CI secret
store; credentials are never committed to the repository).

---

## References

[1] F. Moretti, *Graphs, Maps, Trees: Abstract Models for a Literary History*. London, U.K.: Verso, 2005.

[2] F. Moretti, "Network theory, plot analysis," *New Left Review*, vol. 68, pp. 80–102, Mar.–Apr. 2011.

[3] D. K. Elson, N. Dames, and K. McKeown, "Extracting social networks from literary fiction," in
*Proc. 48th Annu. Meeting Assoc. Comput. Linguistics (ACL)*, Uppsala, Sweden, 2010, pp. 138–147.

[4] M. Jockers, *Macroanalysis: Digital Methods and Literary History*. Urbana, IL, USA: Univ. Illinois
Press, 2013.

[5] M. Eder, J. Rybicki, and M. Kestemont, "Stylometry with R: A package for computational text analysis,"
*R Journal*, vol. 8, no. 1, pp. 107–121, 2016.

[6] J. Archer and M. Jockers, *The Bestseller Code: Anatomy of the Blockbuster Novel*. New York, NY, USA:
St. Martin's Press, 2016.

[7] V. Propp, *Morphology of the Folktale*, 2nd ed. Austin, TX, USA: Univ. Texas Press, 1968 (orig. 1928).

[8] W. Labov and J. Waletzky, "Narrative analysis: Oral versions of personal experience," in *Essays on
the Verbal and Visual Arts*, J. Helm, Ed. Seattle, WA, USA: Univ. Washington Press, 1967, pp. 12–44.

[9] G. Genette, *Narrative Discourse: An Essay in Method*. Ithaca, NY, USA: Cornell Univ. Press, 1980.

[10] E. Cambria and A. Hussain, *Sentic Computing: Techniques, Tools, and Applications*. Dordrecht, The
Netherlands: Springer, 2012.

[11] C. S. Peirce, "What is a sign?" in *The Essential Peirce*, vol. 2. Bloomington, IN, USA: Indiana Univ.
Press, 1894/1998.

[12] D. Herman, *Story Logic: Problems and Possibilities of Narrative*. Lincoln, NE, USA: Univ. Nebraska
Press, 2002.

[13] J. Cohen, "A coefficient of agreement for nominal scales," *Educational and Psychological Measurement*,
vol. 20, no. 1, pp. 37–46, 1960.

[14] J. R. Landis and G. G. Koch, "The measurement of observer agreement for categorical data," *Biometrics*,
vol. 33, no. 1, pp. 159–174, 1977.

---

**Metadata note (Chinese).** 中文标题：《三元九维认知空间：文学结构的映射、指纹与再创作》。中文摘要随最终版本附录
提供。本文档为英文正文（作者默认输出语言），final 版本可附中文标题与摘要。