# Reliability Report — Inter-Annotator Agreement of the Tri9-Cog Mapping

**Version**: 1.0 ・ **Date**: 2026-10-04
**Corpus**: *Hong Lou Meng* (120-chapter public-domain edition), chapters as mapping nodes.
**Scope**: agreement between the primary mapping (`examples/hongloumeng/mapping/nodes.csv`) and an independent re-annotation of a stratified sample of 15 chapters (`examples/hongloumeng/mapping/reannotation-15ch.csv`).

---

## 1. Purpose

The tri9-cog framework encodes any narrative node into 19683 possible coordinates
(`T1T2T3-S1S2S3-C1C2C3`, with `code = T1·3⁸ + … + C3·3⁰ ∈ [0, 19682]`). Because the
encoding is a bijection between the 9-dimensional label vector and the numeric code,
**code-level agreement is identical to coordinate-level agreement by construction**.
The purpose of this study is to quantify how *reproducible* the manual annotation is
under the rubric in `docs/mapping-guide.md`, before the framework is used for
fingerprinting, blueprinting, and replication workflows.

## 2. Sampling

- **Design**: stratified random sampling with a fixed seed (`random.Random(19683)`).
- **Strata**: chapters 1–40 (front volume), 41–80 (middle volume), 81–120 (rear volume); 5 chapters per stratum.
- **Sample**: chapters **1, 2, 19, 28, 36, 41, 48, 52, 54, 63, 81, 99, 104, 109, 118.**
- **Sample size**: n = 15 chapters (≈12.5% of the corpus).
- Chapters were extracted verbatim from the public-domain text; each chapter was read in full
  before annotation.

## 3. Method

- **Judging rubric**: `docs/mapping-guide.md` (9 dimensions × 3 levels: T1 flow, T2 scale, T3 tempo;
  S1 scope, S2 mobility, S3 struct; C1 attribution, C2 chain length, C3 closure).
- **Independent re-annotation**: the re-annotator assigned all 9 dimensions for the 15 sampled
  chapters **without consulting the primary mapping file** (`nodes.csv` was not opened during the
  re-annotation pass; the primary coordinates were only read afterward for comparison).
- **Metrics**:
  - per-dimension **raw agreement** `Po` (proportion of chapters where both annotations agree on that dimension);
  - per-dimension **Cohen's κ** (chance-corrected agreement on 3-class labels);
  - mean κ over the 9 dimensions;
  - **coordinate-level agreement** (all 9 dimensions equal; equals code-level agreement by the bijection above).

Interpretation bands follow Landis & Koch (1977): κ < 0.20 slight; 0.21–0.40 fair; 0.41–0.60 moderate;
0.61–0.80 substantial; > 0.81 almost perfect.

## 4. Results

### 4.1 Coordinate-level agreement

> **0 / 15** chapters received identical full 9-dimensional coordinates (0.0%).

This is **expected** for a 3⁹ = 19683-cell space: any single dimension flip moves the coordinate,
so exact coordinate agreement is a very strict criterion. The dimension-level statistics below are
the informative ones for rubric reliability.

### 4.2 Per-dimension agreement

| Dim | `Po` (raw) | `Pe` (chance) | **κ** | Primary → Re-annotation (label counts) |
| --- | ---: | ---: | ---: | --- |
| T1 flow | 1.000 | 0.760 | **+1.000** | {2:1, 1:1, 0:13} → identical |
| C1 attribution | 0.933 | 0.493 | **+0.868** | {2:1, 1:4, 0:10} → {2:1, 1:5, 0:9} |
| T3 tempo | 0.867 | 0.671 | **+0.595** | {1:13, 0:2} → {1:11, 0:4} |
| S3 struct | 0.800 | 0.560 | **+0.545** | {0:12, 1:3} → {0:9, 1:6} |
| S1 scope | 0.733 | 0.467 | **+0.500** | {0:7, 1:7, 2:1} → {0:4, 1:11} |
| T2 scale | 0.600 | 0.404 | **+0.328** | {0:5, 1:7, 2:3} → {0:5, 1:9, 2:1} |
| S2 mobility | 0.600 | 0.440 | **+0.286** | {0:9, 1:5, 2:1} → {0:6, 1:9} |
| C2 chain | 0.467 | 0.409 | **+0.098** | {1:8, 2:6, 0:1} → {1:11, 0:4} |
| C3 closure | 0.667 | 0.640 | **+0.074** | {0:11, 1:4} → {0:12, 1:3} |

**Mean κ over the 9 dimensions: 0.477 (moderate).**

### 4.3 Headline numbers (identical to `reliability-metrics.json`)

- Coordinate-level agreement: **0/15 (0.0%)**
- Mean κ (9 dims): **0.4772**
- Strongest dimensions: T1 (κ = 1.000), C1 (κ = 0.868) — temporal flow and causal attribution are
  the most reproducible dimensions under the current rubric.
- Weakest dimensions: C2 (κ ≈ 0.10), C3 (κ ≈ 0.07) — chain length and closure judgment are the
  least reproducible.

## 5. Interpretation

1. **Rubric-robust dimensions**: T1 (temporal flow) and C1 (causal attribution) show near-perfect
   or substantial reliability. These are also the two dimensions that drive the most distinguishing
   macro-shape statistics in the fingerprint (entropy, turning points).
2. **Moderate dimensions**: T3, S1, S3, and T2 agree at "fair to moderate" level. Boundary cases
   (e.g., a span of several days vs. weeks; a garden within a compound vs. the city) explain most
   disagreements.
3. **Weak dimensions**: C2 and C3 suffer from (a) genuine boundary ambiguity (short vs. medium chain;
   "partially closed" vs. "open") and (b) skewed base rates — with almost no 0s in C2's primary
   distribution, chance agreement `Pe` is high and κ is severely deflated even when raw agreement
   is tolerable (C3 `Po` = 0.667 but κ = 0.074).
4. **Coordinate-level 0% is not a defect of the framework**: it is the mathematical consequence of a
   19683-cell space. For replication work, dimension-level agreement (or a distance-tolerant
   coordinate metric, e.g., Hamming distance ≤ 2) is the appropriate reliability target.

## 6. Limitations

- **Small sample**: n = 15 per dimension. κ estimates carry wide uncertainty; mean κ should be read
  as indicative, not conclusive.
- **Single re-annotator**: agreement here is between annotator A (primary) and annotator B
  (re-annotation), not a committee; a multi-annotator design with adjudication would yield tighter
  estimates and can be reported as A2 if conducted.
- **Chance correction with skewed margins**: for C2/C3, κ is deflated by high `Pe`; raw `Po`
  must be read alongside. Alternative indices (Gwet's AC1, Krippendorff's α with a proper
  distance function) are noted as follow-up options.
- **Same-framework bias**: both passes used the identical judging rubric; agreement estimates the
  *reliability of the rubric under faithful application*, not agreement against an external truth.

## 7. Recommendations for framework v1.1

1. Add **anchored exemplars** to the rubric for T2 (day⇄week boundary), C2 (short⇄medium⇄long),
   and C3 (open⇄partial⇄complete) to reduce boundary disagreement.
2. For fingerprint/blueprint workflows, report **per-dimension agreement thresholds** (e.g.,
   "blueprint verified" requires ≥ 5/9 dimensions equal, κ ≥ 0.6 for T1/C1) instead of demanding
   exact coordinate equality.
3. Consider a **2-annotator + adjudication** protocol for the replication guide when new corpora
   are mapped.

## 8. Data files

| File | Content |
| --- | --- |
| `examples/hongloumeng/mapping/nodes.csv` | Primary mapping, all 120 chapters (121 rows incl. header) |
| `examples/hongloumeng/mapping/reannotation-15ch.csv` | Independent re-annotation, 15 sampled chapters |
| `examples/hongloumeng/mapping/reliability-metrics.json` | Machine-readable per-dimension Po / κ / Pe and coordinate-level agreement |

## 9. Reproducing

```bash
python3 - <<'EOF'
import csv, json
from collections import Counter
DIMS = ['T1','T2','T3','S1','S2','S3','C1','C2','C3']
prim = {int(r['chapter']): r['coordinate'].replace('-','') for r in
        csv.DictReader(open('examples/hongloumeng/mapping/nodes.csv', encoding='utf-8'))}
rean = {int(r['chapter']): r['coordinate'].replace('-','') for r in
        csv.DictReader(open('examples/hongloumeng/mapping/reannotation-15ch.csv', encoding='utf-8'))}
chs = sorted(set(prim) & set(rean)); N = len(chs)
def kappa(a, b):
    ca, cb = Counter(a), Counter(b)
    Po = sum(x == y for x, y in zip(a, b)) / N
    Pe = sum(ca.get(l, 0) * cb.get(l, 0) for l in set(a) | set(b)) / N**2
    return (1.0 if Pe == 1 else (Po - Pe) / (1 - Pe)), Po, Pe
print('coordinate-level:', sum(prim[c] == rean[c] for c in chs), '/', N)
print('mean kappa:', round(sum(kappa([prim[c][i] for c in chs], [rean[c][i] for c in chs])[0]
      for i in range(9)) / 9, 4))
EOF
```