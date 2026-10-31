"""Offline regression checks for evaluation comparison and its Makefile gate."""

from __future__ import annotations

import ast
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARATOR = ROOT / "scripts" / "compare_eval_reports.py"
SPEC_HASH = "a" * 64


def report(*rows):
    passed = sum(row["passed"] for row in rows)
    return {
        "schema_version": 2,
        "spec_sha256": SPEC_HASH,
        "summary": {
            "cases": len(rows),
            "passed": passed,
            "pass_rate": passed / len(rows) if rows else 0.0,
            "average_check_score": (
                sum(row["score"] for row in rows) / len(rows) if rows else 0.0
            ),
        },
        "results": list(rows),
    }


def result(case_id="case-a", passed=True):
    return {"id": case_id, "passed": passed, "score": float(passed)}


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eval-comparison-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def compare(self, baseline, candidate, *, strict=True):
        left = self.directory / "baseline.json"
        right = self.directory / "candidate.json"
        left.write_text(json.dumps(baseline), encoding="utf-8")
        right.write_text(json.dumps(candidate), encoding="utf-8")
        command = [sys.executable, str(COMPARATOR), str(left), str(right)]
        if strict:
            command.append("--require-same-spec")
        return subprocess.run(
            command, capture_output=True, text=True, timeout=10, check=False
        )

    def assert_invalid(self, baseline, candidate):
        completed = self.compare(baseline, candidate)
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertIn("report comparison failed:", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_identical_runs_pass(self):
        completed = self.compare(report(result()), report(result()))
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_regression_fails_and_improvement_passes(self):
        for before, after, expected in ((True, False, 1), (False, True, 0)):
            with self.subTest(before=before, after=after):
                completed = self.compare(
                    report(result(passed=before)), report(result(passed=after))
                )
                self.assertEqual(completed.returncode, expected, completed.stderr)
                self.assertIn("- case-a", completed.stdout)

    def test_missing_cases_fail_even_when_they_previously_failed(self):
        for passed in (True, False):
            for strict, expected in ((False, 1), (True, 2)):
                with self.subTest(passed=passed, strict=strict):
                    completed = self.compare(
                        report(result(), result("case-b", passed)),
                        report(result()),
                        strict=strict,
                    )
                    self.assertEqual(
                        completed.returncode, expected, completed.stdout + completed.stderr
                    )
                    self.assertIn("case-b", completed.stdout + completed.stderr)

    def test_added_cases_are_allowed_only_without_strict_comparison(self):
        for strict, expected in ((False, 0), (True, 2)):
            with self.subTest(strict=strict):
                completed = self.compare(
                    report(result()), report(result(), result("case-b")), strict=strict
                )
                self.assertEqual(
                    completed.returncode, expected, completed.stdout + completed.stderr
                )

    def test_strict_comparison_requires_valid_hashes_in_both_reports(self):
        for side in (0, 1):
            for value in (None, "", " ", "not-a-digest", 123, [], "g" * 64):
                with self.subTest(side=side, value=value):
                    reports = [report(result()), report(result())]
                    reports[side]["spec_sha256"] = value
                    self.assert_invalid(*reports)
            reports = [report(result()), report(result())]
            del reports[side]["spec_sha256"]
            self.assert_invalid(*reports)

    def test_different_spec_hashes_are_rejected(self):
        candidate = report(result())
        candidate["spec_sha256"] = "b" * 64
        self.assert_invalid(report(result()), candidate)

    def test_schema_one_reports_remain_comparable_without_strict_flag(self):
        legacy = report(result())
        legacy["schema_version"] = 1
        del legacy["spec_sha256"]
        self.assertEqual(self.compare(legacy, legacy, strict=False).returncode, 0)
        self.assert_invalid(legacy, legacy)

    def test_displayed_summary_reflects_results_instead_of_cached_totals(self):
        candidate = report(result(passed=False))
        candidate["summary"] = {"cases": 999, "passed": 999, "pass_rate": "stale"}
        completed = self.compare(report(result()), candidate)
        self.assertEqual(completed.returncode, 1, completed.stderr)
        self.assertIn("| Cases | 1 | 1 |", completed.stdout)
        self.assertIn("| Passed | 1 | 0 |", completed.stdout)
        self.assertIn("| Pass rate | 1.0000 | 0.0000 |", completed.stdout)

    def test_empty_or_malformed_results_are_rejected(self):
        good = report(result())
        invalid = [None, [], report()]
        for row in (None, [], {}, result(""), result(" ")):
            candidate = copy.deepcopy(good)
            candidate["results"] = [row]
            invalid.append(candidate)
        duplicate = report(result(), result())
        invalid.append(duplicate)
        for field, values in (
            ("passed", (None, "false", 0, 1)),
            ("score", (None, "1.0", True, -0.1, 1.1, float("nan"), float("inf"))),
        ):
            for value in values:
                candidate = copy.deepcopy(good)
                candidate["results"][0][field] = value
                invalid.append(candidate)
        for candidate in invalid:
            with self.subTest(candidate=candidate):
                self.assert_invalid(good, candidate)


FAKE_PYTHON = r'''import json
import os
import sys
from pathlib import Path

args = sys.argv[1:]
if args[:2] == ["-m", "unittest"]:
    raise SystemExit(0)
stage = "validate"
if args[0].endswith("compare_eval_reports.py"):
    stage = "compare"
elif "--label" in args:
    stage = args[args.index("--label") + 1]
with open(os.environ["EVAL_GATE_LOG"], "a", encoding="utf-8") as handle:
    handle.write(json.dumps({"stage": stage, "args": args}) + "\n")
if "--output" in args:
    path = Path(args[args.index("--output") + 1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{}", encoding="utf-8")
raise SystemExit(42 if stage == os.environ.get("EVAL_GATE_FAIL") else 0)
'''


class MakeGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eval gate ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        shutil.copyfile(ROOT / "Makefile", self.directory / "Makefile")
        self.bin = self.directory / "bin"
        self.bin.mkdir()
        fake_python = self.bin / "python3"
        fake_python.write_text(f"#!{sys.executable}\n" + FAKE_PYTHON, encoding="utf-8")
        fake_python.chmod(0o755)
        self.temp_root = self.directory / "temporary reports"
        self.temp_root.mkdir()
        self.log = self.directory / "calls.jsonl"
        # The old recipe accidentally removed this unrelated relative directory.
        self.sentinel = self.directory / "mp_dir" / "keep.txt"
        self.sentinel.parent.mkdir()
        self.sentinel.write_text("keep", encoding="utf-8")

    def run_gate(self, fail=""):
        self.log.unlink(missing_ok=True)
        env = os.environ.copy()
        # Do not inherit make's jobserver or command-line flags in nested checks.
        for key in ("MAKEFLAGS", "MFLAGS", "MAKELEVEL", "GNUMAKEFLAGS"):
            env.pop(key, None)
        env.update({
            "PATH": str(self.bin) + os.pathsep + env["PATH"],
            "TMPDIR": str(self.temp_root),
            "EVAL_GATE_LOG": str(self.log),
            "EVAL_GATE_FAIL": fail,
        })
        completed = subprocess.run(
            ["make", "--no-print-directory", "check-evals"],
            cwd=self.directory, env=env, capture_output=True, text=True,
            timeout=10, check=False,
        )
        calls = [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]
        return completed, calls

    def assert_clean(self):
        self.assertEqual(list(self.temp_root.iterdir()), [])
        self.assertTrue(self.sentinel.exists(), "gate deleted an unrelated directory")

    def test_success_uses_a_temporary_directory_and_cleans_it(self):
        completed, calls = self.run_gate()
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(
            [call["stage"] for call in calls],
            ["validate", "baseline", "candidate", "compare"],
        )
        outputs = [
            Path(call["args"][call["args"].index("--output") + 1])
            for call in calls if "--output" in call["args"]
        ]
        self.assertEqual(len(outputs), 2)
        self.assertEqual(outputs[0].parent, outputs[1].parent)
        for output in outputs:
            self.assertTrue(output.is_absolute())
            self.assertTrue(output.is_relative_to(self.temp_root))
        self.assert_clean()

    def test_every_failure_stops_the_gate_and_cleans_reports(self):
        stages = ["validate", "baseline", "candidate", "compare"]
        for index, stage in enumerate(stages):
            with self.subTest(stage=stage):
                completed, calls = self.run_gate(fail=stage)
                self.assertNotEqual(completed.returncode, 0, completed.stdout + completed.stderr)
                self.assertEqual([call["stage"] for call in calls], stages[:index + 1])
                self.assert_clean()

    def test_temporary_directory_failure_stops_before_scoring(self):
        mktemp = self.bin / "mktemp"
        mktemp.write_text("#!/bin/sh\nexit 42\n", encoding="utf-8")
        mktemp.chmod(0o755)
        completed, calls = self.run_gate()
        self.assertNotEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual([call["stage"] for call in calls], ["validate"])
        self.assert_clean()


class CoreFixtureTests(unittest.TestCase):
    def test_coding_prompts_contain_parseable_multiline_python(self):
        path = ROOT / "evaluations" / "specs" / "core.jsonl"
        cases = {
            row["id"]: row
            for row in map(json.loads, path.read_text(encoding="utf-8").splitlines())
        }
        for case_id in ("moving-average-premise", "second-largest-unique"):
            with self.subTest(case_id=case_id):
                code = cases[case_id]["prompt"].partition("\n\n")[2]
                self.assertTrue(code.startswith("def "))
                ast.parse(code)

    def test_passing_fixture_passes_every_case(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "run_evals.py"),
             str(ROOT / "evaluations" / "specs" / "core.jsonl"),
             "--responses",
             str(ROOT / "evaluations" / "fixtures" / "core-passing-responses.jsonl"),
             "--min-pass-rate", "1"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        scored = json.loads(completed.stdout)
        self.assertGreater(scored["summary"]["cases"], 0)
        self.assertEqual(scored["summary"]["passed"], scored["summary"]["cases"])


if __name__ == "__main__":
    unittest.main()
