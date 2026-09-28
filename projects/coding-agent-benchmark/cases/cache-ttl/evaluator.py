#!/usr/bin/env python3
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


class FakeClock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


def load_module(workspace):
    spec = importlib.util.spec_from_file_location(
        "candidate_cache",
        workspace / "cache.py",
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def add_check(checks, name, fn):
    try:
        fn()
        passed = True
        detail = "ok"
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

    def expiry_boundary():
        clock = FakeClock()
        cache = module.TTLCache(10, clock)
        cache.set("k", "v")
        clock.advance(10)
        assert cache.get("k") is None
        assert len(cache) == 0

    def refresh_on_set():
        clock = FakeClock()
        cache = module.TTLCache(10, clock)
        cache.set("k", "old")
        clock.advance(8)
        cache.set("k", "new")
        clock.advance(5)
        assert cache.get("k") == "new"
        clock.advance(5)
        assert cache.get("k") is None

    def length_prunes():
        clock = FakeClock()
        cache = module.TTLCache(5, clock)
        cache.set("old", 1)
        clock.advance(4)
        cache.set("new", 2)
        assert len(cache) == 2
        clock.advance(1)
        assert len(cache) == 1
        assert cache.get("new") == 2

    def keys_expire_independently():
        clock = FakeClock()
        cache = module.TTLCache(3, clock)
        cache.set("a", 1)
        clock.advance(2)
        cache.set("b", 2)
        clock.advance(1)
        assert cache.get("a") is None
        assert cache.get("b") == 2

    add_check(checks, "expires-at-boundary", expiry_boundary)
    add_check(checks, "set-replaces-and-refreshes", refresh_on_set)
    add_check(checks, "length-counts-live-items", length_prunes)
    add_check(checks, "keys-expire-independently", keys_expire_independently)

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
