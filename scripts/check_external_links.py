#!/usr/bin/env python3
"""Check external Markdown links without third-party dependencies.

Designed primarily for scheduled maintenance. Hard missing responses (404/410)
fail the check; authentication blocks, rate limits, server errors, and network
failures are reported as warnings so a transient outage does not make the
repository unhealthy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
FENCE_RE = re.compile(
    r"(^|\n)(?:\x60{3}|~~~).*?(?:\n(?:\x60{3}|~~~)(?=\n|$))",
    re.DOTALL,
)
INLINE_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\((https?://[^)\s]+)\)")
REFERENCE_LINK_RE = re.compile(
    r"^\s*\[[^\]]+\]:\s*(https?://\S+)",
    re.MULTILINE,
)
AUTOLINK_RE = re.compile(r"<(https?://[^>\s]+)>")

SOFT_HTTP_CODES = {401, 403, 408, 425, 429}
HARD_HTTP_CODES = {404, 410}
USER_AGENT = "llm-queries-link-check/1.0 (+https://github.com/djeada/llm-queries)"


def markdown_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" not in path.parts:
            yield path


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("\n", text)


def normalize_url(url: str) -> str:
    return url.rstrip(".,;:")


def iter_urls(text: str) -> Iterable[str]:
    clean = strip_fenced_code(text)
    for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE, AUTOLINK_RE):
        for match in pattern.finditer(clean):
            yield normalize_url(match.group(1))


def should_skip(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    if any(token in url for token in ("YOUR_", "your-", "<", ">", "{", "}")):
        return True
    return False


def discover_links() -> dict[str, list[str]]:
    sources: dict[str, list[str]] = {}
    for path in markdown_files():
        relative = path.relative_to(ROOT).as_posix()
        for url in iter_urls(path.read_text(encoding="utf-8")):
            if should_skip(url):
                continue
            sources.setdefault(url, []).append(relative)
    return sources


def request_url(url: str, timeout: float) -> tuple[str, int | None, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}

    for method in ("HEAD", "GET"):
        request_headers = dict(headers)
        if method == "GET":
            request_headers["Range"] = "bytes=0-0"
        request = urllib.request.Request(
            url,
            headers=request_headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                code = response.getcode()
                return "ok", code, response.geturl()
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in {400, 405, 501}:
                continue
            if exc.code in HARD_HTTP_CODES:
                return "broken", exc.code, url
            if exc.code in SOFT_HTTP_CODES or exc.code >= 500:
                return "warning", exc.code, url
            return "warning", exc.code, url
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if method == "HEAD":
                continue
            return "warning", None, str(exc)

    return "warning", None, "no usable response"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument(
        "--max-links",
        type=int,
        default=0,
        help="Optional cap for local testing; 0 checks every discovered link.",
    )
    args = parser.parse_args()

    links = discover_links()
    urls = sorted(links)
    if args.max_links > 0:
        urls = urls[: args.max_links]

    results = []
    counts: Counter[str] = Counter()

    for index, url in enumerate(urls, start=1):
        status, code, detail = request_url(url, args.timeout)
        counts[status] += 1
        row = {
            "url": url,
            "status": status,
            "http_code": code,
            "detail": detail,
            "sources": links[url],
        }
        results.append(row)
        print(
            f"[{index}/{len(urls)}] {status.upper():7} "
            f"{code if code is not None else '-':>3} {url}"
        )

    report = {
        "schema_version": 1,
        "summary": {
            "checked": len(results),
            "ok": counts["ok"],
            "warning": counts["warning"],
            "broken": counts["broken"],
        },
        "results": results,
    }

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    if counts["warning"]:
        print(
            f"warnings: {counts['warning']} links could not be conclusively checked",
            file=sys.stderr,
        )
    if counts["broken"]:
        print(f"broken links: {counts['broken']}", file=sys.stderr)
        for row in results:
            if row["status"] == "broken":
                print(
                    f"- {row['url']} ({row['http_code']}) from "
                    f"{', '.join(row['sources'])}",
                    file=sys.stderr,
                )
        return 1

    print(
        f"external link check passed: {counts['ok']} ok, "
        f"{counts['warning']} warnings"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
