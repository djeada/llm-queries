#!/usr/bin/env python3
"""Compare two llm-queries evaluation reports."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


class ReportError(ValueError):
    pass


def load_report(path: Path) -> dict[str, Any]:
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ReportError(f"{path}: could not read report: {exc}") from exc

    if not isinstance(report, dict):
        raise ReportError(f"{path}: report must be an object")
    version = report.get("schema_version")
    if type(version) is not int or version not in {1, 2}:
        raise ReportError(
            f"{path}: unsupported schema_version {report.get('schema_version')!r}"
        )
    if not isinstance(report.get("results"), list) or not report["results"]:
        raise ReportError(f"{path}: results must be a non-empty list")
    if not isinstance(report.get("summary"), dict):
        raise ReportError(f"{path}: missing summary")
    return report


def by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in report["results"]:
        if not isinstance(row, dict):
            raise ReportError("result row must be an object")
        case_id = row.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ReportError("result row missing non-empty string id")
        if case_id in rows:
            raise ReportError(f"duplicate result id {case_id!r}")
        if not isinstance(row.get("passed"), bool):
            raise ReportError(f"{case_id}: passed must be a boolean")
        value = row.get("score")
        if type(value) not in (int, float) or not 0.0 <= value <= 1.0:
            raise ReportError(f"{case_id}: score must be a finite number between 0 and 1")
        rows[case_id] = row
    return rows


def label(report: dict[str, Any], fallback: str) -> str:
    value = report.get("label")
    return value if isinstance(value, str) and value.strip() else fallback


def score(row: dict[str, Any]) -> float:
    return float(row["score"])


def summary(rows: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Derive displayed metrics from the validated rows being compared."""
    passed = sum(row["passed"] for row in rows.values())
    return {
        "cases": len(rows),
        "passed": passed,
        "pass_rate": passed / len(rows),
        "average_check_score": sum(score(row) for row in rows.values()) / len(rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--require-same-spec",
        action="store_true",
        help="Require valid, matching spec SHA-256 hashes and identical case IDs.",
    )
    args = parser.parse_args()

    try:
        baseline = load_report(args.baseline)
        candidate = load_report(args.candidate)
        left = by_id(baseline)
        right = by_id(candidate)
        left_ids = set(left)
        right_ids = set(right)
        missing = sorted(left_ids - right_ids)
        added = sorted(right_ids - left_ids)

        if args.require_same_spec:
            for name, report in (("baseline", baseline), ("candidate", candidate)):
                digest = report.get("spec_sha256")
                if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                    raise ReportError(f"{name}: --require-same-spec needs a valid spec_sha256")
            if baseline["spec_sha256"].lower() != candidate["spec_sha256"].lower():
                raise ReportError("spec hashes differ")
            if missing or added:
                raise ReportError(
                    f"case IDs differ: missing from candidate {missing}; "
                    f"new in candidate {added}"
                )
    except ReportError as exc:
        print(f"report comparison failed: {exc}", file=sys.stderr)
        return 2

    common = sorted(left_ids & right_ids)

    regressions = []
    improvements = []
    changed_scores = []

    for case_id in common:
        before = left[case_id]
        after = right[case_id]
        before_pass = before["passed"]
        after_pass = after["passed"]

        if before_pass and not after_pass:
            regressions.append(case_id)
        elif not before_pass and after_pass:
            improvements.append(case_id)

        delta = score(after) - score(before)
        if abs(delta) > 1e-12:
            changed_scores.append((case_id, delta, score(before), score(after)))

    left_label = label(baseline, args.baseline.stem)
    right_label = label(candidate, args.candidate.stem)
    left_summary = summary(left)
    right_summary = summary(right)

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

    return 1 if regressions or missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
