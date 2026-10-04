"""Command-line interface for tri9cog."""

from __future__ import annotations

import argparse
import json
import sys

from .annotate import make_template, DIM_ORDER
from .fingerprint import (
    fingerprint,
    load_nodes,
    fingerprint_from_csv,
    save_json,
)
from .replicate import build_blueprint, verify_story, STRATEGIES


def _cmd_fingerprint(args) -> int:
    fp = fingerprint_from_csv(args.input, top_turns=args.top_turns)
    if args.out:
        save_json(fp, args.out)
    else:
        print(json.dumps(fp, ensure_ascii=False, indent=2))
    return 0


def _cmd_blueprint(args) -> int:
    with open(args.source, encoding="utf-8") as f:
        src = json.load(f)
    blue = build_blueprint(
        src,
        strategy=args.strategy,
        nodes=args.nodes,
        vary_dims=args.vary_dims,
        seed=args.seed,
    )
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(blue, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(blue, ensure_ascii=False, indent=2))
    return 0


def _cmd_verify(args) -> int:
    rows = load_nodes(args.input)
    blue = json.load(open(args.target, encoding="utf-8"))
    report = verify_story(rows, blue)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _cmd_template(args) -> int:
    try:
        with open(args.nodes, encoding="utf-8") as f:
            node_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        node_ids = [f"node_{i+1}" for i in range(args.count)]
    make_template(node_ids, args.out)
    print(f"template written: {args.out} ({len(node_ids)} nodes, dims: {','.join(DIM_ORDER)})")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="tri9cog", description="Triadic Cognitive Space (三元九维认知空间) CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_fp = sub.add_parser("fingerprint", help="compute structural fingerprint from a node CSV")
    p_fp.add_argument("input", help="node CSV with `coordinate` column")
    p_fp.add_argument("-o", "--out", help="output JSON path")
    p_fp.add_argument("--top-turns", type=int, default=10)
    p_fp.set_defaults(func=_cmd_fingerprint)

    p_bl = sub.add_parser("blueprint", help="generate a story blueprint from a fingerprint")
    p_bl.add_argument("--source", required=True, help="fingerprint JSON")
    p_bl.add_argument("--strategy", choices=STRATEGIES, default="isomorphic")
    p_bl.add_argument("--nodes", type=int, default=None)
    p_bl.add_argument("--vary-dims", nargs="*", default=None)
    p_bl.add_argument("--seed", type=int, default=19683)
    p_bl.add_argument("-o", "--out", help="output blueprint JSON")
    p_bl.set_defaults(func=_cmd_blueprint)

    p_v = sub.add_parser("verify", help="self-check a new story against a blueprint")
    p_v.add_argument("input", help="new story node CSV")
    p_v.add_argument("--target", required=True, help="blueprint JSON")
    p_v.add_argument("-o", "--out", help="output report JSON")
    p_v.set_defaults(func=_cmd_verify)

    p_t = sub.add_parser("template", help="generate an empty annotation template CSV")
    p_t.add_argument("--nodes", default=None, help="file with one node id per line")
    p_t.add_argument("--count", type=int, default=12, help="fallback count when --nodes omitted")
    p_t.add_argument("--out", default="template.csv")
    p_t.set_defaults(func=_cmd_template)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())