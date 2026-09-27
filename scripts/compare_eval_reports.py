#!/usr/bin/env python3
"""Compare two llm-queries evaluation reports."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class ReportError(ValueError):
    pass


def load_report(path: Path) -> dict[str, Any]:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReportError(f"{path}: could not read report: {exc}") from exc

    if report.get("schema_version") not in {1, 2}:
        raise ReportError(
            f"{path}: unsupported schema_version {report.get('schema_version')!r}"
        )
    if not isinstance(report.get("results"), list):
        raise ReportError(f"{path}: missing results list")
    if not isinstance(report.get("summary"), dict):
        raise ReportError(f"{path}: missing summary")
    return report


def by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in report["results"]:
        case_id = row.get("id")
        if not isinstance(case_id, str):
            raise ReportError("result row missing string id")
        if case_id in rows:
            raise ReportError(f"duplicate result id {case_id!r}")
        rows[case_id] = row
    return rows


def label(report: dict[str, Any], fallback: str) -> str:
    value = report.get("label")
    return value if isinstance(value, str) and value.strip() else fallback


def score(row: dict[str, Any]) -> float:
    value = row.get("score", 0.0)
    return float(value) if isinstance(value, (int, float)) else 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--require-same-spec",
        action="store_true",
        help="Fail if spec SHA differs (schema v2 reports).",
    )
    args = parser.parse_args()

    try:
        baseline = load_report(args.baseline)
        candidate = load_report(args.candidate)
        left = by_id(baseline)
        right = by_id(candidate)
    except ReportError as exc:
        print(f"report comparison failed: {exc}", file=sys.stderr)
        return 2

    if args.require_same_spec:
        left_hash = baseline.get("spec_sha256")
        right_hash = candidate.get("spec_sha256")
        if left_hash and right_hash and left_hash != right_hash:
            print("report comparison failed: spec hashes differ", file=sys.stderr)
            return 2

    left_ids = set(left)
    right_ids = set(right)
    common = sorted(left_ids & right_ids)
    missing = sorted(left_ids - right_ids)
    added = sorted(right_ids - left_ids)

    regressions = []
    improvements = []
    changed_scores = []

    for case_id in common:
        before = left[case_id]
        after = right[case_id]
        before_pass = bool(before.get("passed"))
        after_pass = bool(after.get("passed"))

        if before_pass and not after_pass:
            regressions.append(case_id)
        elif not before_pass and after_pass:
            improvements.append(case_id)

        delta = score(after) - score(before)
        if abs(delta) > 1e-12:
            changed_scores.append((case_id, delta, score(before), score(after)))

    left_label = label(baseline, args.baseline.stem)
    right_label = label(candidate, args.candidate.stem)
    left_summary = baseline["summary"]
    right_summary = candidate["summary"]

    print(f"# Eval comparison: {left_label} -> {right_label}")
    print()
    print("| Metric | Baseline | Candidate |")
    print("| --- | ---: | ---: |")
    print(
        f"| Cases | {left_summary.get('cases', len(left))} | "
        f"{right_summary.get('cases', len(right))} |"
    )
    print(
        f"| Passed | {left_summary.get('passed', 0)} | "
        f"{right_summary.get('passed', 0)} |"
    )
    print(
        f"| Pass rate | {left_summary.get('pass_rate', 0):.4f} | "
        f"{right_summary.get('pass_rate', 0):.4f} |"
    )
    print(
        f"| Average check score | "
        f"{left_summary.get('average_check_score', 0):.4f} | "
        f"{right_summary.get('average_check_score', 0):.4f} |"
    )

    print()
    print("## Regressions")
    print()
    if regressions:
        for case_id in regressions:
            print(f"- {case_id}")
    else:
        print("_None._")

    print()
    print("## Improvements")
    print()
    if improvements:
        for case_id in improvements:
            print(f"- {case_id}")
    else:
        print("_None._")

    print()
    print("## Check-score changes")
    print()
    if changed_scores:
        print("| Case | Baseline | Candidate | Delta |")
        print("| --- | ---: | ---: | ---: |")
        for case_id, delta, before, after in sorted(
            changed_scores,
            key=lambda item: (item[1], item[0]),
        ):
            print(f"| {case_id} | {before:.4f} | {after:.4f} | {delta:+.4f} |")
    else:
        print("_None._")

    if missing:
        print()
        print("## Missing from candidate")
        print()
        for case_id in missing:
            print(f"- {case_id}")

    if added:
        print()
        print("## New in candidate")
        print()
        for case_id in added:
            print(f"- {case_id}")

    return 1 if regressions else 0


if __name__ == "__main__":
    raise SystemExit(main())
