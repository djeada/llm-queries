#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def load_module(workspace):
    spec = importlib.util.spec_from_file_location(
        "candidate_config",
        workspace / "config.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def add_check(checks, name, fn):
    try:
        passed = bool(fn())
        detail = "ok" if passed else "unexpected result"
    except Exception as exc:
        passed = False
        detail = str(exc)
    checks.append({"name": name, "passed": passed, "detail": detail})


def main():
    workspace = Path(sys.argv[1])
    module = load_module(workspace)
    checks = []

    public = subprocess.run(
        [sys.executable, "-m", "unittest", "-q", "test_public.py"],
        cwd=workspace,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.append(
        {
            "name": "public-tests",
            "passed": public.returncode == 0,
            "detail": (public.stderr or public.stdout).strip() or "ok",
        }
    )

    add_check(
        checks,
        "cli-env-file-precedence",
        lambda: module.load_config(
            {"host": "file", "port": 7000, "debug": False},
            {"APP_HOST": "env", "APP_PORT": "7100", "APP_DEBUG": "true"},
            {"host": "cli", "port": 7200},
        )
        == {"host": "cli", "port": 7200, "debug": True},
    )

    add_check(
        checks,
        "partial-source-merge",
        lambda: module.load_config(
            {"host": "file", "port": 7000},
            {"APP_DEBUG": "ON"},
            {"port": 7300},
        )
        == {"host": "file", "port": 7300, "debug": True},
    )

    add_check(
        checks,
        "false-debug-parsing",
        lambda: module.load_config(env={"APP_DEBUG": "no"})["debug"] is False,
    )

    file_values = {"host": "file"}
    env = {"APP_HOST": "env"}
    cli = {"host": "cli"}
    before = (dict(file_values), dict(env), dict(cli))
    module.load_config(file_values, env, cli)
    inputs_ok = (file_values, env, cli) == before
    checks.append(
        {
            "name": "inputs-not-mutated",
            "passed": inputs_ok,
            "detail": "ok" if inputs_ok else "input dictionaries changed",
        }
    )

    passed_count = sum(item["passed"] for item in checks)
    report = {
        "passed": passed_count == len(checks),
        "score": passed_count / len(checks),
        "checks": checks,
        "metrics": {
            "checks": len(checks),
            "passed_checks": passed_count,
        },
    }
    print(json.dumps(report))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
