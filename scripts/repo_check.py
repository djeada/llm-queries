#!/usr/bin/env python3
"""Repository maintenance checks for llm-queries.

Uses only the Python standard library so the same command works locally and in
GitHub Actions without bootstrapping a project environment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content-registry.json"
CATALOG = ROOT / "CATALOG.md"
HEALTH = ROOT / "CONTENT_HEALTH.md"

CONTENT_ROOTS = (
    ("prompts", "Prompts"),
    ("skills", "Skills"),
    ("evaluations", "Evaluations"),
    ("local_setup_guides", "Local setup guides"),
    ("docs", "Documentation"),
    ("projects", "Projects"),
    ("resources", "Resources"),
    ("course_reviews", "Course reviews"),
    ("news", "News"),
    ("slides", "Slides"),
    ("snapshots", "Snapshots"),
)

ALLOWED_KINDS = {
    "prompt", "skill", "evaluation", "guide", "project-doc",
    "reference", "course-review", "news", "slide", "snapshot",
    "documentation", "glossary",
}
ALLOWED_FRESHNESS = {"evergreen", "version-sensitive", "dated"}
ALLOWED_STATUS = {"active", "experimental", "needs-review", "historical", "archived"}

INLINE_LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
FENCE_RE = re.compile(
    r"(^|\n)(?:\x60{3}|~~~).*?(?:\n(?:\x60{3}|~~~)(?=\n|$))",
    re.DOTALL,
)
LAST_VERIFIED_RE = re.compile(
    r"\*\*Last verified:\*\*\s*(\d{4}-\d{2}-\d{2})",
    re.IGNORECASE,
)
STATUS_RE = re.compile(
    r">\s*\*\*Status:\*\*\s*([a-z-]+)",
    re.IGNORECASE,
)
EXTERNAL_URL_RE = re.compile(r"https?://[^\s)>]+")
H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
EXPECTED_OUTPUT_RE = re.compile(
    r"^##\s+(?:Expected output|Oczekiwany wynik)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
PROMPT_FENCE_RE = re.compile(r"(?:\x60{3}|~~~)(?:text)?\s*\n", re.IGNORECASE)


def content_files() -> list[Path]:
    files: list[Path] = []
    for root_name, _ in CONTENT_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            relative = path.relative_to(ROOT)
            if relative == Path(root_name) / "README.md":
                continue
            files.append(relative)
    return sorted(files, key=lambda value: value.as_posix().lower())


def load_registry() -> dict[str, dict]:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError("content-registry.json is missing") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"content-registry.json is invalid JSON: {exc}") from exc

    if data.get("schema_version") != 1:
        raise ValueError("content-registry.json schema_version must be 1")

    entries = data.get("entries")
    if not isinstance(entries, dict):
        raise ValueError("content-registry.json entries must be an object")
    return entries


def parse_date(value: str, path: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(
            f"{path}: last_verified must use YYYY-MM-DD, got {value!r}"
        ) from exc


def check_registry(entries: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    discovered = {path.as_posix() for path in content_files()}
    registered = set(entries)

    for path in sorted(discovered - registered):
        errors.append(f"{path}: content file is missing from content-registry.json")
    for path in sorted(registered - discovered):
        errors.append(f"{path}: registry entry points to a missing content file")

    for path, meta in sorted(entries.items()):
        if not isinstance(meta, dict):
            errors.append(f"{path}: registry metadata must be an object")
            continue

        kind = meta.get("kind")
        freshness = meta.get("freshness")
        status = meta.get("status")
        review_days = meta.get("review_days")
        last_verified = meta.get("last_verified")

        if kind not in ALLOWED_KINDS:
            errors.append(f"{path}: invalid kind {kind!r}")
        if freshness not in ALLOWED_FRESHNESS:
            errors.append(f"{path}: invalid freshness {freshness!r}")
        if status not in ALLOWED_STATUS:
            errors.append(f"{path}: invalid status {status!r}")
        if review_days is not None and (
            not isinstance(review_days, int) or review_days <= 0
        ):
            errors.append(f"{path}: review_days must be a positive integer or null")
        if last_verified is not None:
            try:
                parse_date(last_verified, path)
            except ValueError as exc:
                errors.append(str(exc))

        source = ROOT / path
        source_text = (
            source.read_text(encoding="utf-8")
            if source.exists()
            else ""
        )

        if not H1_RE.search(source_text):
            errors.append(f"{path}: managed content needs a level-1 title")

        if status in {"experimental", "needs-review", "historical", "archived"}:
            match = STATUS_RE.search(source_text)
            if not match:
                errors.append(
                    f"{path}: {status} content must show a visible "
                    f"'> **Status:** {status}' banner"
                )
            elif match.group(1).lower() != status:
                errors.append(
                    f"{path}: visible status {match.group(1)!r} "
                    f"does not match registry status {status!r}"
                )

        if status == "historical" and not EXTERNAL_URL_RE.search(source_text):
            errors.append(
                f"{path}: historical content must include at least one source URL"
            )

        if kind == "prompt":
            if not EXPECTED_OUTPUT_RE.search(source_text):
                errors.append(
                    f"{path}: prompt content needs an Expected output section"
                )
            if not PROMPT_FENCE_RE.search(source_text):
                errors.append(
                    f"{path}: prompt content needs at least one fenced prompt block"
                )

        if freshness == "version-sensitive" and status == "active":
            if not last_verified:
                errors.append(
                    f"{path}: active version-sensitive content needs last_verified"
                )
            if not review_days:
                errors.append(
                    f"{path}: active version-sensitive content needs review_days"
                )
            if last_verified:
                match = LAST_VERIFIED_RE.search(source_text)
                if not match:
                    errors.append(
                        f"{path}: active version-sensitive content must show "
                        "'**Last verified:** YYYY-MM-DD' in the document"
                    )
                elif match.group(1) != last_verified:
                    errors.append(
                        f"{path}: visible Last verified date {match.group(1)} "
                        f"does not match registry {last_verified}"
                    )
    return errors


def build_catalog(entries: dict[str, dict]) -> str:
    grouped: dict[str, list[str]] = defaultdict(list)
    for path in sorted(entries):
        grouped[path.split("/", 1)[0]].append(path)

    lines = [
        "<!-- Generated by scripts/repo_check.py. Do not edit by hand. -->",
        "# Content Catalog",
        "",
        "Generated from the repository tree and content-registry.json.",
        "Run python3 scripts/repo_check.py --write-generated after adding, moving,",
        "removing, or reclassifying content.",
        "",
    ]
    for root_name, label in CONTENT_ROOTS:
        paths = grouped.get(root_name, [])
        lines.extend((f"## {label} ({len(paths)})", ""))
        for path in paths:
            meta = entries[path]
            lines.append(
                f"- [{path}]({path}) — {meta['status']}; {meta['freshness']}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def due_date(meta: dict) -> date | None:
    if not meta.get("last_verified") or not meta.get("review_days"):
        return None
    start = datetime.strptime(meta["last_verified"], "%Y-%m-%d").date()
    return start + timedelta(days=meta["review_days"])


def build_health(entries: dict[str, dict]) -> str:
    statuses = Counter(meta["status"] for meta in entries.values())
    freshness = Counter(meta["freshness"] for meta in entries.values())
    current = []
    needs_review = []
    experimental = []
    historical = []

    for path, meta in sorted(entries.items()):
        if meta["status"] == "needs-review":
            needs_review.append((path, meta))
        elif meta["status"] == "experimental":
            experimental.append((path, meta))
        elif meta["status"] in {"historical", "archived"}:
            historical.append((path, meta))
        if meta["status"] == "active" and meta["freshness"] == "version-sensitive":
            current.append((path, meta, due_date(meta)))

    lines = [
        "<!-- Generated by scripts/repo_check.py. Do not edit by hand. -->",
        "# Content Health",
        "",
        "This report makes maintenance debt visible without pretending historical",
        "material is current.",
        "",
        "## Summary",
        "",
        f"- Registered content files: **{len(entries)}**",
        f"- Active: **{statuses['active']}**",
        f"- Experimental: **{statuses['experimental']}**",
        f"- Needs review: **{statuses['needs-review']}**",
        f"- Historical / archived: **{statuses['historical'] + statuses['archived']}**",
        f"- Version-sensitive: **{freshness['version-sensitive']}**",
        "",
        "## Active version-sensitive content",
        "",
    ]

    if current:
        lines.extend([
            "| File | Last verified | Review every | Next review |",
            "| --- | --- | ---: | --- |",
        ])
        for path, meta, due in current:
            lines.append(
                f"| [{path}]({path}) | {meta['last_verified']} | "
                f"{meta['review_days']} days | {due.isoformat() if due else '—'} |"
            )
    else:
        lines.append("_None._")

    lines.extend(("", "## Needs review", ""))
    if needs_review:
        for path, meta in needs_review:
            lines.append(f"- [{path}]({path}) — {meta['kind']}; {meta['freshness']}")
    else:
        lines.append("_None._")

    lines.extend(("", "## Experimental content", ""))
    if experimental:
        for path, _ in experimental:
            lines.append(f"- [{path}]({path})")
    else:
        lines.append("_None._")

    lines.extend(("", "## Historical / dated material", ""))
    if historical:
        for path, _ in historical:
            lines.append(f"- [{path}]({path})")
    else:
        lines.append("_None._")

    lines.extend((
        "",
        "## Policy",
        "",
        "Normal pull-request CI checks registry coverage, links, and generated",
        "files. Scheduled CI also enables strict freshness checks; active",
        "version-sensitive content fails once its review date has passed.",
        "",
    ))
    return "\n".join(lines)


def strip_fenced_code(text: str) -> str:
    return FENCE_RE.sub("\n", text)


def link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")].strip()
    return target.split(maxsplit=1)[0] if target else ""


def iter_local_links(text: str):
    clean = strip_fenced_code(text)
    for match in INLINE_LINK_RE.finditer(clean):
        yield link_target(match.group(1))
    for match in REFERENCE_LINK_RE.finditer(clean):
        yield link_target(match.group(1))


def is_external(target: str) -> bool:
    lower = target.lower()
    return (
        not target
        or target.startswith("#")
        or lower.startswith(("http://", "https://", "mailto:", "data:", "tel:"))
    )


def check_internal_links() -> list[str]:
    errors: list[str] = []
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.parts
    )
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for target in iter_local_links(text):
            if is_external(target):
                continue
            target_path = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not target_path:
                continue
            resolved = (source.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(
                    f"{source.relative_to(ROOT)}: link escapes repository: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: missing local link target {target!r}"
                )
    return errors


def check_generated(entries: dict[str, dict]) -> list[str]:
    expected = {CATALOG: build_catalog(entries), HEALTH: build_health(entries)}
    errors = []
    for path, value in expected.items():
        if not path.exists():
            errors.append(
                f"{path.name} is missing. Run "
                "'python3 scripts/repo_check.py --write-generated'."
            )
        elif path.read_text(encoding="utf-8") != value:
            errors.append(
                f"{path.name} is out of date. Run "
                "'python3 scripts/repo_check.py --write-generated'."
            )
    return errors


def check_freshness(entries: dict[str, dict], today: date) -> list[str]:
    errors = []
    for path, meta in sorted(entries.items()):
        if meta["status"] != "active" or meta["freshness"] != "version-sensitive":
            continue
        due = due_date(meta)
        if due and today > due:
            errors.append(
                f"{path}: freshness review overdue since {due.isoformat()} "
                f"(last verified {meta['last_verified']})"
            )
    return errors


def write_generated(entries: dict[str, dict]) -> None:
    CATALOG.write_text(build_catalog(entries), encoding="utf-8")
    HEALTH.write_text(build_health(entries), encoding="utf-8")
    print("updated CATALOG.md and CONTENT_HEALTH.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-generated", action="store_true")
    parser.add_argument("--write-catalog", action="store_true")
    parser.add_argument("--strict-freshness", action="store_true")
    args = parser.parse_args()

    try:
        entries = load_registry()
    except ValueError as exc:
        print(f"repository checks failed:\n- {exc}", file=sys.stderr)
        return 1

    if args.write_generated or args.write_catalog:
        write_generated(entries)

    errors = [
        *check_registry(entries),
        *check_internal_links(),
        *check_generated(entries),
    ]
    if args.strict_freshness:
        errors.extend(check_freshness(entries, date.today()))

    if errors:
        print("repository checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("repository checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
