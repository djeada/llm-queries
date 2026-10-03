#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def load_module(workspace):
    spec = importlib.util.spec_from_file_location(
        "candidate_slugify",
        workspace / "slugify.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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

    cases = {
        "unicode-and-underscore": ("  Café déjà_vu!  ", "cafe-deja-vu"),
        "repeated-hyphens": ("one---two", "one-two"),
        "mixed-separators": (" alpha__ beta \t gamma ", "alpha-beta-gamma"),
        "punctuation": ("Hello, world... again?", "hello-world-again"),
        "leading-trailing": ("---Alpha---", "alpha"),
        "empty-fallback": ("___", "item"),
        "symbol-only-fallback": ("★ !!!", "item"),
    }

    for name, (value, expected) in cases.items():
        try:
            actual = module.slugify(value)
            passed = actual == expected
            detail = (
                "ok"
                if passed
                else f"expected {expected!r}, got {actual!r}"
            )
        except Exception as exc:
            passed = False
            detail = str(exc)
        checks.append(
            {
                "name": name,
                "passed": passed,
                "detail": detail,
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
