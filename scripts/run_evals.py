#!/usr/bin/env python3
"""Small dependency-free evaluation runner for llm-queries.

The runner intentionally does not know about a particular model provider.
It can:
- validate JSONL evaluation specs
- score previously captured responses
- invoke any local command that reads a prompt from stdin and writes a response
  to stdout

This keeps benchmark definitions reusable across local models, APIs wrapped by
small scripts, and agent harnesses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CHECK_TYPES = {
    "exact",
    "contains_all",
    "contains_any",
    "contains_none",
    "regex",
    "json_keys",
    "max_chars",
    "line_count",
    "bullet_count",
}


class SpecError(ValueError):
    pass


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SpecError(
                    f"{path}:{line_number}: invalid JSON: {exc.msg}"
                ) from exc

            if not isinstance(row, dict):
                raise SpecError(f"{path}:{line_number}: each row must be an object")

            case_id = row.get("id")
            if not isinstance(case_id, str) or not case_id.strip():
                raise SpecError(f"{path}:{line_number}: missing non-empty id")
            if case_id in seen:
                raise SpecError(f"{path}:{line_number}: duplicate id {case_id!r}")
            seen.add(case_id)

            prompt = row.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                raise SpecError(f"{path}:{line_number}: missing non-empty prompt")

            category = row.get("category")
            if not isinstance(category, str) or not category.strip():
                raise SpecError(f"{path}:{line_number}: missing non-empty category")

            checks = row.get("checks")
            if not isinstance(checks, list) or not checks:
                raise SpecError(f"{path}:{line_number}: checks must be a non-empty list")

            for index, check in enumerate(checks):
                validate_check(path, line_number, index, check)

            rows.append(row)

    if not rows:
        raise SpecError(f"{path}: no evaluation cases found")
    return rows


def validate_check(path: Path, line_number: int, index: int, check: Any) -> None:
    label = f"{path}:{line_number}:check[{index}]"
    if not isinstance(check, dict):
        raise SpecError(f"{label}: check must be an object")

    check_type = check.get("type")
    if check_type not in CHECK_TYPES:
        raise SpecError(f"{label}: unsupported check type {check_type!r}")

    if check_type == "exact":
        if not isinstance(check.get("value"), str):
            raise SpecError(f"{label}: exact requires string value")

    if check_type in {"contains_all", "contains_any", "contains_none"}:
        values = check.get("values")
        if (
            not isinstance(values, list)
            or not values
            or not all(isinstance(value, str) and value for value in values)
        ):
            raise SpecError(f"{label}: {check_type} requires non-empty string values")

    if check_type == "regex":
        pattern = check.get("pattern")
        if not isinstance(pattern, str) or not pattern:
            raise SpecError(f"{label}: regex requires pattern")
        try:
            re.compile(pattern)
        except re.error as exc:
            raise SpecError(f"{label}: invalid regex: {exc}") from exc

    if check_type == "json_keys":
        keys = check.get("keys")
        if (
            not isinstance(keys, list)
            or not keys
            or not all(isinstance(key, str) and key for key in keys)
        ):
            raise SpecError(f"{label}: json_keys requires non-empty string keys")

    if check_type in {"max_chars", "line_count", "bullet_count"}:
        value = check.get("value")
        if not isinstance(value, int) or value < 0:
            raise SpecError(f"{label}: {check_type} requires non-negative integer value")


def normalize_text(value: str, case_sensitive: bool) -> str:
    return value if case_sensitive else value.casefold()


def run_check(response: str, check: dict[str, Any]) -> tuple[bool, str]:
    check_type = check["type"]
    case_sensitive = bool(check.get("case_sensitive", False))
    haystack = normalize_text(response, case_sensitive)

    if check_type == "exact":
        expected = normalize_text(check["value"], case_sensitive)
        actual = normalize_text(response.strip(), case_sensitive)
        passed = actual == expected
        return passed, "exact match" if passed else f"expected {check['value']!r}"

    if check_type in {"contains_all", "contains_any", "contains_none"}:
        values = [
            normalize_text(value, case_sensitive)
            for value in check["values"]
        ]
        matches = [value in haystack for value in values]

        if check_type == "contains_all":
            passed = all(matches)
            missing = [
                check["values"][i]
                for i, match in enumerate(matches)
                if not match
            ]
            return passed, "all required text present" if passed else f"missing {missing}"

        if check_type == "contains_any":
            passed = any(matches)
            return passed, "at least one required text present" if passed else (
                f"none of {check['values']} found"
            )

        passed = not any(matches)
        present = [
            check["values"][i]
            for i, match in enumerate(matches)
            if match
        ]
        return passed, "forbidden text absent" if passed else f"found forbidden {present}"

    if check_type == "regex":
        flags = 0 if case_sensitive else re.IGNORECASE
        passed = re.search(check["pattern"], response, flags) is not None
        return passed, "regex matched" if passed else f"no match for {check['pattern']!r}"

    if check_type == "json_keys":
        try:
            parsed = json.loads(response)
        except json.JSONDecodeError as exc:
            return False, f"response is not JSON: {exc.msg}"
        if not isinstance(parsed, dict):
            return False, "top-level JSON value is not an object"
        missing = [key for key in check["keys"] if key not in parsed]
        return (not missing), "required JSON keys present" if not missing else f"missing keys {missing}"

    if check_type == "max_chars":
        passed = len(response) <= check["value"]
        return passed, f"{len(response)} chars <= {check['value']}" if passed else (
            f"{len(response)} chars > {check['value']}"
        )

    lines = [line for line in response.splitlines() if line.strip()]
    if check_type == "line_count":
        passed = len(lines) == check["value"]
        return passed, f"{len(lines)} lines" if passed else (
            f"expected {check['value']} non-empty lines, got {len(lines)}"
        )

    if check_type == "bullet_count":
        bullets = [
            line for line in lines
            if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line)
        ]
        passed = len(bullets) == check["value"]
        return passed, f"{len(bullets)} bullets" if passed else (
            f"expected {check['value']} bullets, got {len(bullets)}"
        )

    raise AssertionError(f"unhandled check type {check_type}")


def score_case(case: dict[str, Any], response: str) -> dict[str, Any]:
    checks = []
    for check in case["checks"]:
        passed, detail = run_check(response, check)
        checks.append({
            "type": check["type"],
            "passed": passed,
            "detail": detail,
        })

    passed_count = sum(1 for check in checks if check["passed"])
    score = passed_count / len(checks)
    return {
        "id": case["id"],
        "category": case["category"],
        "passed": passed_count == len(checks),
        "score": round(score, 4),
        "checks": checks,
        "response": response,
    }


def load_responses(path: Path) -> dict[str, str]:
    responses: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SpecError(
                    f"{path}:{line_number}: invalid JSON: {exc.msg}"
                ) from exc
            if not isinstance(row, dict):
                raise SpecError(f"{path}:{line_number}: row must be an object")
            case_id = row.get("id")
            response = row.get("response")
            if not isinstance(case_id, str) or not isinstance(response, str):
                raise SpecError(
                    f"{path}:{line_number}: rows require string id and response"
                )
            responses[case_id] = response
    return responses


def invoke_command(command: list[str], prompt: str, timeout: float) -> str:
    try:
        completed = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out after {timeout}s") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise RuntimeError(
            f"command exited {completed.returncode}: {stderr or 'no stderr'}"
        )
    return completed.stdout.strip()


def git_commit() -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[1],
            text=True,
            capture_output=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    value = completed.stdout.strip()
    return value if completed.returncode == 0 and value else None


def parse_metadata(values: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for value in values:
        key, separator, item = value.partition("=")
        if not separator or not key.strip():
            raise SpecError(
                f"metadata must use KEY=VALUE form, got {value!r}"
            )
        key = key.strip()
        if key in metadata:
            raise SpecError(f"duplicate metadata key {key!r}")
        metadata[key] = item
    return metadata


def build_report(
    spec_path: Path,
    results: list[dict[str, Any]],
    mode: str,
    command: list[str] | None,
    label: str | None,
    metadata: dict[str, str],
) -> dict[str, Any]:
    passed = sum(1 for result in results if result["passed"])
    average = sum(result["score"] for result in results) / len(results)
    spec_bytes = spec_path.read_bytes()
    return {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "spec": str(spec_path),
        "spec_sha256": hashlib.sha256(spec_bytes).hexdigest(),
        "git_commit": git_commit(),
        "label": label,
        "metadata": metadata,
        "mode": mode,
        "command": command,
        "summary": {
            "cases": len(results),
            "passed": passed,
            "pass_rate": round(passed / len(results), 4),
            "average_check_score": round(average, 4),
        },
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path, help="JSONL evaluation specification")
    parser.add_argument(
        "--responses",
        type=Path,
        help="Score JSONL rows shaped as {'id': ..., 'response': ...}",
    )
    parser.add_argument(
        "--command",
        help="Command that reads one prompt from stdin and writes one response to stdout",
    )
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--label", help="Human-readable run/model label")
    parser.add_argument(
        "--meta",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Reproducibility metadata; may be repeated",
    )
    parser.add_argument("--min-pass-rate", type=float, default=0.0)
    args = parser.parse_args()

    if args.responses and args.command:
        parser.error("choose either --responses or --command, not both")
    if not 0.0 <= args.min_pass_rate <= 1.0:
        parser.error("--min-pass-rate must be between 0 and 1")

    try:
        cases = load_jsonl(args.spec)
        metadata = parse_metadata(args.meta)
    except (OSError, SpecError) as exc:
        print(f"evaluation spec invalid: {exc}", file=sys.stderr)
        return 2

    if not args.responses and not args.command:
        print(f"evaluation spec valid: {len(cases)} cases")
        return 0

    response_map: dict[str, str] = {}
    command: list[str] | None = None
    mode: str

    if args.responses:
        try:
            response_map = load_responses(args.responses)
        except (OSError, SpecError) as exc:
            print(f"response file invalid: {exc}", file=sys.stderr)
            return 2
        mode = "responses"
    else:
        command = shlex.split(args.command)
        if not command:
            parser.error("--command must not be empty")
        mode = "command"

    results = []
    for case in cases:
        try:
            if mode == "responses":
                if case["id"] not in response_map:
                    raise RuntimeError("missing response")
                response = response_map[case["id"]]
            else:
                assert command is not None
                response = invoke_command(command, case["prompt"], args.timeout)
            result = score_case(case, response)
        except RuntimeError as exc:
            result = {
                "id": case["id"],
                "category": case["category"],
                "passed": False,
                "score": 0.0,
                "checks": [],
                "response": "",
                "error": str(exc),
            }
        results.append(result)

    report = build_report(
        args.spec,
        results,
        mode,
        command,
        args.label,
        metadata,
    )
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered, end="")

    pass_rate = report["summary"]["pass_rate"]
    return 0 if pass_rate >= args.min_pass_rate else 1


if __name__ == "__main__":
    raise SystemExit(main())
