# Contributing to tri9-cog

Thanks for your interest in `tri9-cog` — a formalized ternary (3^9 = 19,683) cognitive coordinate
system for mapping, fingerprinting, and regenerating literary structure.

These guidelines cover how to contribute code, annotated data, and documentation. Please read this
whole page before opening an issue or a pull request. For questions, reach out to
**q1z2q3@gmail.com**.

---

## Getting started

### Prerequisites

- Python **>= 3.9**
- `git`
- (optional) a virtual environment: `python -m venv .venv && source .venv/bin/activate`

### Install for development

```bash
git clone https://github.com/q1z2q3-debug/tri9-cog.git
cd tri9-cog
pip install -e ".[dev]"        # editable install + pytest
```

If the editable install misbehaves in your environment (e.g. global-site-packages conflicts), you
can run the CLI from the source tree without installing:

```bash
PYTHONPATH=src python3 -m tri9cog --help
```

### Run the test suite

```bash
pytest                          # 18 tests, all green
```

The test suite (`tests/test_core.py`) covers encoding/decoding, validation, fingerprint entropy,
turning-point detection, blueprint strategies, and verification — and requires **no external files**,
so it runs anywhere.

### CLI quick reference

```bash
tri9cog fingerprint <nodes.csv>                       # structural fingerprint (entropy, mode, ...)
tri9cog blueprint --source fingerprint.json --strategy {isomorphic|mirror|variation} --nodes N
tri9cog verify new-story-nodes.csv --target blueprint.json
```

---

## Ways to contribute

1. **Code** — fix a bug, improve the engine (`src/tri9cog/`), or extend the CLI.
2. **Data** — add a new annotated text (nodes CSV + fingerprint/blueprint JSON) under `examples/`.
3. **Documentation** — improve the guides under `docs/`, the README, or this file.
4. **Research** — report results, replications, or case studies; see `paper/`.

### Adding a new annotated text

Follow the 4-step mapping workflow in `docs/mapping-guide.md`:

- Place your annotation under `examples/<work>/mapping/`:
  - `nodes.csv` — the scene/character nodes with 9-dimension coordinates;
  - `fingerprint.json` — output of `tri9cog fingerprint`;
  - `blueprint.json` — output of `tri9cog blueprint` (optional, for replication cases).
- Add a `README.md` in `examples/<work>/` stating the source/edition of the text.
- **Copyright:** only include full text that is in the public domain. For copyrighted or translated
  works (e.g. modern translations), contribute **coordinates and statistics only** — never the text
  itself. Follow the pattern of `examples/baiyun-gudu/` (coordinates only).
- Verify your annotation: run the fingerprint and check that the numbers in your `README.md`
  (entropy, unique codes, turning points) match the generated files.

---

## Issue & pull request workflow

### 1. Open an issue first for non-trivial changes

Small bug fixes or typo fixes may skip the issue. For new features, strategy changes, or mapping
extensions, describe:

- **What** you want to change and why;
- **How** it fits the existing framework (3 elements × 9 dimensions × 3 states);
- Any **benchmark/verification** you plan (e.g. which fingerprint numbers must stay stable).

### 2. Create a branch

```bash
git checkout -b feat/your-change
```

Keep changes focused: one logical change per PR.

### 3. Commit

Use conventional commit style, consistent with the project history:

```
feat(engine): add <new capability>
fix(cli): correct <behavior>
data(examples): add <work> annotation
docs(paper): update <section>
test(core): cover <case>
```

### 4. Verify before opening the PR

- `pytest` passes (18 tests, all green);
- No stray files: run `git status` and confirm only intended files are staged;
- No credentials or private data: never commit `.env`, tokens, or upload files
  (see `.gitignore`).

### 5. Open the pull request

Describe the change, reference the issue number if any, and note any numbers/benchmarks that are
expected to change (e.g. a new corpus's entropy). A maintainer will review; treat review comments
as requests for discussion, not rejections.

---

## Coding conventions

- Python: PEP 8; keep functions small and single-purpose;
- Type hints on public functions/methods;
- Docstrings: one concise sentence describing behavior and returns;
- **Simplicity first**: prefer straightforward implementations over clever ones; the framework's
  value is auditable structure, not obscurity;
- New transformations or strategies must ship with tests.

## Documentation conventions

- Keep the numeric claims provable: any entropy/count/turning-point number in docs must be
  reproducible from committed data via the CLI;
- Follow the existing structure of `docs/framework.md` and `docs/mapping-guide.md` when extending.

---

## License

`tri9-cog` is released under the **MIT License** — see [LICENSE](LICENSE). By contributing, you
agree that your contributions are licensed under the same terms. Annotated benchmark data is
released for open use (CC-BY-4.0 on the archived Zenodo release, https://doi.org/10.5281/zenodo.23172839);
if you contribute data, note its copyright status in the work's `README.md` as described above.

---

*Thank you for helping make literary structure measurable and reproducible.*