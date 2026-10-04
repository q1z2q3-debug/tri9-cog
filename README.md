# tri9-cog — Triadic Cognitive Space (三元九维认知空间)

**A formalized ternary cognitive coordinate system for literary structure: 3 elements × 9 dimensions × 3 states = 19,683 status cells. Read, measure, fingerprint, and regenerate stories.**

## What is this?

Most literary analysis is intuitive: *"I understood this novel, but I can't say exactly what the understanding is."*

`tri9-cog` makes that "understanding" **tangible, computable, and reproducible** — a coordinate system where every plot node and character state maps to a unique ternary code in a 19,683-cell state space (`3^9`).

| Layer | Constituent | Notes |
| --- | --- | --- |
| 3 elements (三元) | Time T · Space S · Causality C | The three fundamental perspectives |
| 9 dimensions (九维) | T1–T3, S1–S3, C1–C3 | Each element decomposes into 3 dimensions |
| 3 states (三态) | `0` · `1` · `2` | Each dimension takes exactly 3 discrete states |
| 19,683 cells | `code = T1·3⁸ + … + C3·3⁰` | Every node/person maps to a unique coordinate `T1T2T3-S1S2S3-C1C2C3` (0–19682, no gaps, no duplicates) |

## Why 19,683?

9 dimensions × 3 states each = `3^9 = 19683` complete combinations — the full state space of the framework. Any scene, any character state, any story eventually lands on exactly one of these 19,683 coordinates.

## What can you do with it?

1. **Map** — annotate any novel's plot nodes and characters into 9-dimension coordinates (4-step mapping workflow).
2. **Analyze** — compute 6 quantitative analyses: dimension distribution, state path, transition magnitude, structural fingerprint (mode + entropy H), character trajectory comparison, key node marking.
3. **Recreate** — extract a source's structural fingerprint, then regenerate a new story that preserves, mirrors, or varies the fingerprint (isomorphic / mirror / variation strategies), with a self-check pass back through the same coordinate system.

## Quick start

```bash
# (v0.1) Install
pip install -e .

# Map a novel → structural fingerprint
tri9cog fingerprint examples/hongloumeng/mapping/nodes.csv

# Generate a story blueprint from a fingerprint
tri9cog blueprint --source fingerprint.json --strategy mirror --nodes 40

# Verify a new story against a target blueprint
tri9cog verify new-story-nodes.csv --target blueprint.json
```

## Repository layout

```
tri9-cog/
├── README.md
├── LICENSE                  # MIT
├── pyproject.toml
├── docs/                    # framework, mapping guide, replication guide
├── examples/
│   ├── hongloumeng/         # Dream of the Red Chamber: public-domain text + 120-chapter mapping & analyses
│   └── tingyunlou/          # A new (recreated) novel following the same fingerprint
├── src/tri9cog/             # v0.1 engine: annotate / fingerprint / replicate
├── tests/
├── scripts/
└── paper/                   # Paper outline (computational narratology / digital humanities)
```

## Worked example: Dream of the Red Chamber (《红楼梦》)

The full public-domain 120-chapter text and its complete mapping live under `examples/hongloumeng/`:

- **84 unique coordinates** across 120 chapters (range 0–18952)
- **Entropy H ≈ 1.3929** — "daily-life tragedy": entropy below a uniform distribution, stable and weighted toward a few home states
- Structure in one line: *time flows forward (115/120), space enclosed (107/120), characters drive causality (80/120), long foreshadowing chains, open endings (70/120)*
- Key structural turning points identified via max transition magnitude: ch.5→6 (8 dims), ch.98→99 (6), ch.116→117 (9), ch.119→120 (7)
- Character trajectories: Baoyu's vaulting arc peaks at ch.117; Daiyu shows zero state transitions for 43 chapters

## Why open source?

- **Reproducibility** — every number above is recomputable from the released mapping tables (CSV/JSON) and the framework rules.
- **Benchmark** — the 120-chapter mapping serves as a public benchmark for computational narratology.
- **Interoperability** — plug your own texts, annotation tools, or LLM generators into the pipeline.

## Roadmap

- **v0.1 (this release)** — analysis engine: annotation support, fingerprint/entropy/turning-point computation, blueprint generation, verify; full Hong Lou Meng corpus.
- **v0.2** — replication strategies (isomorphic / mirror / variation) as structured blueprints.
- **v0.3** — LLM text-generation adapter + self-check loop.
- **v1.0** — end-to-end "replicate a classic's structure → produce a new work" workflow.
- **Paper** — full academic paper planned (computational narratology / digital humanities); open data released here in advance.

## Contributing

Issues, pull requests, and third-party mapping contributions are welcome. When adding a new annotated text, please follow `docs/mapping-guide.md`.

## Contact

📮 **q1z2q3@gmail.com**

## License

MIT — see [LICENSE](LICENSE).

---

*Text of Dream of the Red Chamber is the public-domain 120-chapter edition (author Cao Xueqin, d. ~1763; continuation attributed to Gao E, d. ~1815). Distributed for research purposes with the public-domain notice.*