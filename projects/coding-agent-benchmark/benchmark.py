#!/usr/bin/env python3
"""Provider-neutral benchmark harness for repository-editing coding agents."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CASES_ROOT = ROOT / "cases"


class BenchmarkError(RuntimeError):
    pass


def case_dir(case_id: str) -> Path:
    path = CASES_ROOT / case_id
    required = ("task.txt", "seed", "evaluator.py", "golden")
    if not path.is_dir() or any(not (path / item).exists() for item in required):
        raise BenchmarkError(f"unknown or incomplete case: {case_id}")
    return path


def case_ids() -> list[str]:
    if not CASES_ROOT.exists():
        return []
    result = []
    for path in sorted(CASES_ROOT.iterdir()):
        if not path.is_dir():
            continue
        try:
            case_dir(path.name)
        except BenchmarkError:
            continue
        result.append(path.name)
    return result


def read_task(case_id: str) -> str:
    return (case_dir(case_id) / "task.txt").read_text(encoding="utf-8").strip() + "\n"


def run_process(args, *, cwd, input_text=None, timeout=30.0):
    try:
        return subprocess.run(
            args,
            cwd=cwd,
            input=input_text,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BenchmarkError(f"failed to run {args!r}: {exc}") from exc


def init_git(workspace: Path) -> None:
    commands = [
        ["git", "init", "-q"],
        ["git", "config", "user.name", "Benchmark Seed"],
        ["git", "config", "user.email", "benchmark@example.invalid"],
        ["git", "add", "."],
        ["git", "commit", "-qm", "benchmark seed"],
    ]
    for command in commands:
        completed = run_process(command, cwd=workspace)
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise BenchmarkError(
                f"git setup failed: {' '.join(command)}: {detail}"
            )


def prepare(case_id: str, workspace: Path, *, force=False) -> Path:
    source = case_dir(case_id) / "seed"

    if workspace.exists() and any(workspace.iterdir()):
        if not force:
            raise BenchmarkError(
                f"workspace is not empty: {workspace}; use --force to replace it"
            )
        shutil.rmtree(workspace)

    workspace.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, workspace, dirs_exist_ok=True)
    (workspace / ".benchmark-task.txt").write_text(
        read_task(case_id),
        encoding="utf-8",
    )
    init_git(workspace)
    return workspace


def clear_python_bytecode(workspace: Path) -> None:
    for cache_dir in workspace.rglob("__pycache__"):
        if cache_dir.is_dir():
            shutil.rmtree(cache_dir)
    for pyc in workspace.rglob("*.pyc"):
        if pyc.is_file():
            pyc.unlink()


def load_evaluator_output(case_id: str, workspace: Path) -> dict[str, Any]:
    clear_python_bytecode(workspace)
    evaluator = case_dir(case_id) / "evaluator.py"
    completed = run_process(
        [sys.executable, str(evaluator), str(workspace)],
        cwd=ROOT,
    )
    if completed.returncode not in (0, 1):
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise BenchmarkError(f"evaluator crashed for {case_id}: {detail}")

    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise BenchmarkError(
            f"evaluator returned invalid JSON for {case_id}: {exc}"
        ) from exc

    if not isinstance(report, dict):
        raise BenchmarkError("evaluator report must be an object")
    if not isinstance(report.get("passed"), bool):
        raise BenchmarkError("evaluator report needs boolean passed")
    if not isinstance(report.get("checks"), list):
        raise BenchmarkError("evaluator report needs checks")
    score_value = report.get("score")
    if (
        not isinstance(score_value, (int, float))
        or not 0.0 <= float(score_value) <= 1.0
    ):
        raise BenchmarkError("evaluator score must be between 0 and 1")
    return report


def git_observation(workspace: Path) -> dict[str, Any]:
    if not (workspace / ".git").exists():
        return {
            "git_available": False,
            "changed_files": [],
            "status": [],
        }

    status = run_process(["git", "status", "--short"], cwd=workspace)
    names = run_process(["git", "diff", "--name-only", "HEAD"], cwd=workspace)
    diff_stat = run_process(["git", "diff", "--stat", "HEAD"], cwd=workspace)

    changed = [
        line.strip()
        for line in names.stdout.splitlines()
        if line.strip()
    ]
    return {
        "git_available": True,
        "changed_files": changed,
        "changed_file_count": len(changed),
        "status": [
            line.rstrip()
            for line in status.stdout.splitlines()
            if line.strip()
        ],
        "diff_stat": diff_stat.stdout.strip(),
    }


def score(case_id: str, workspace: Path) -> dict[str, Any]:
    if not workspace.is_dir():
        raise BenchmarkError(f"workspace does not exist: {workspace}")
    report = load_evaluator_output(case_id, workspace)
    return {
        "schema_version": 1,
        "case": case_id,
        **report,
        "workspace": str(workspace),
        "git": git_observation(workspace),
    }


def overlay_golden(case_id: str, workspace: Path) -> None:
    shutil.copytree(
        case_dir(case_id) / "golden",
        workspace,
        dirs_exist_ok=True,
    )


def self_test() -> dict[str, Any]:
    results = []
    with tempfile.TemporaryDirectory(prefix="coding-agent-benchmark-") as temp:
        root = Path(temp)
        for case_id in case_ids():
            workspace = root / case_id
            prepare(case_id, workspace)
            baseline = score(case_id, workspace)
            if baseline["passed"]:
                raise BenchmarkError(
                    f"{case_id}: untouched seed unexpectedly passes evaluator"
                )

            overlay_golden(case_id, workspace)
            golden = score(case_id, workspace)
            if not golden["passed"]:
                failed = [
                    item.get("name", "<unnamed>")
                    for item in golden["checks"]
                    if not item.get("passed")
                ]
                raise BenchmarkError(
                    f"{case_id}: golden solution does not pass: {failed}"
                )

            results.append(
                {
                    "case": case_id,
                    "baseline_score": baseline["score"],
                    "golden_score": golden["score"],
                    "golden_changed_files": golden["git"].get(
                        "changed_files",
                        [],
                    ),
                }
            )

    return {
        "schema_version": 1,
        "cases": len(results),
        "passed": True,
        "results": results,
    }


def invoke_agent(command, *, task, workspace, timeout):
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            input=task,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            env=os.environ.copy(),
        )
        return {
            "command": command,
            "exit_code": completed.returncode,
            "duration_seconds": round(time.monotonic() - started, 4),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "timed_out": False,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "exit_code": None,
            "duration_seconds": round(time.monotonic() - started, 4),
            "stdout": exc.stdout or "",
            "stderr": exc.stderr or "",
            "timed_out": True,
        }


def run_case(
    case_id,
    command,
    *,
    workspace,
    timeout,
    keep_workspace,
):
    temp = None
    if workspace is None:
        temp = tempfile.TemporaryDirectory(
            prefix=f"coding-agent-{case_id}-"
        )
        workspace = Path(temp.name)

    prepare(case_id, workspace, force=True)
    agent = invoke_agent(
        command,
        task=read_task(case_id),
        workspace=workspace,
        timeout=timeout,
    )
    report = score(case_id, workspace)
    report["agent"] = agent

    if temp is not None:
        if keep_workspace:
            persistent = Path(temp.name + "-kept")
            shutil.copytree(workspace, persistent)
            report["workspace"] = str(persistent)
        temp.cleanup()

    return report


def write_or_print(report, output):
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"wrote {output}")
    else:
        print(rendered, end="")


def parse_command(value):
    command = shlex.split(value)
    if not command:
        raise BenchmarkError("agent command must not be empty")
    return command


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="subcommand", required=True)

    sub.add_parser("list")

    p = sub.add_parser("prepare")
    p.add_argument("case")
    p.add_argument("workspace", type=Path)
    p.add_argument("--force", action="store_true")

    p = sub.add_parser("score")
    p.add_argument("case")
    p.add_argument("workspace", type=Path)
    p.add_argument("--output", type=Path)

    p = sub.add_parser("run")
    p.add_argument("case")
    p.add_argument("--command", required=True)
    p.add_argument("--workspace", type=Path)
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--keep-workspace", action="store_true")
    p.add_argument("--output", type=Path)

    p = sub.add_parser("run-all")
    p.add_argument("--command", required=True)
    p.add_argument("--timeout", type=float, default=300.0)
    p.add_argument("--output", type=Path)

    sub.add_parser("self-test")
    args = parser.parse_args()

    try:
        if args.subcommand == "list":
            for case_id in case_ids():
                print(case_id)
            return 0

        if args.subcommand == "prepare":
            workspace = prepare(
                args.case,
                args.workspace,
                force=args.force,
            )
            print(f"prepared {args.case} at {workspace}")
            print(f"task: {workspace / '.benchmark-task.txt'}")
            return 0

        if args.subcommand == "score":
            report = score(args.case, args.workspace)
            write_or_print(report, args.output)
            return 0 if report["passed"] else 1

        if args.subcommand == "self-test":
            write_or_print(self_test(), None)
            return 0

        command = parse_command(args.command)

        if args.subcommand == "run":
            report = run_case(
                args.case,
                command,
                workspace=args.workspace,
                timeout=args.timeout,
                keep_workspace=args.keep_workspace,
            )
            write_or_print(report, args.output)
            return 0 if report["passed"] else 1

        reports = [
            run_case(
                case_id,
                command,
                workspace=None,
                timeout=args.timeout,
                keep_workspace=False,
            )
            for case_id in case_ids()
        ]
        passed = sum(1 for report in reports if report["passed"])
        aggregate = {
            "schema_version": 1,
            "cases": len(reports),
            "passed": passed,
            "pass_rate": (
                round(passed / len(reports), 4)
                if reports
                else 0.0
            ),
            "total_changed_files": sum(
                report["git"].get("changed_file_count", 0)
                for report in reports
            ),
            "results": reports,
        }
        write_or_print(aggregate, args.output)
        return 0 if passed == len(reports) else 1

    except BenchmarkError as exc:
        print(f"benchmark error: {exc}", file=sys.stderr)
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
