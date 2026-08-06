#!/usr/bin/env python3
"""Deterministic UI-polish signal scanner.

frontend-implementation/SKILL.md already instructs covering loading/empty/
error states, motion, focus, and responsiveness -- that doctrine existed
and was correct. It was still skipped in real use, because prose doctrine
only helps if an agent actually reads the routed skill before considering
UI work done; nothing forced that. security_gate.py doesn't rely on an
agent remembering to "be careful about secrets" -- it greps for patterns
regardless. This applies the same idea to UI polish: check for concrete,
detectable signals in the actual source, not just trust that the routed
skill was read.

This is a heuristic scanner, same honest limitation as security_gate.py:
it detects the *absence of a signal*, not the presence of good UX. A
project can pass every check here and still have a bad interface, and can
fail a check for a legitimate reason (e.g. a project with no forms has no
error-state signal to find). Use judgement on the findings; do not treat
a clean report as a substitute for actually looking at the interface.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CSS_SUFFIXES = {".css"}
COMPONENT_SUFFIXES = {".jsx", ".tsx", ".js", ".ts"}
IGNORED_PARTS = {".git", "node_modules", "dist", "build", "__pycache__"}

CSS_CHECKS = [
    ("responsive-breakpoints", re.compile(r"@media")),
    ("motion-transitions", re.compile(r"transition\s*:|@keyframes|animation\s*:")),
    ("reduced-motion-respect", re.compile(r"prefers-reduced-motion")),
    ("focus-visible", re.compile(r":focus-visible")),
]

COMPONENT_CHECKS = [
    ("loading-state-handling", re.compile(r"(?i)loading")),
    ("error-state-handling", re.compile(r"(?i)catch\s*(?:\([^)]*\))?\s*\{[^}]*set[A-Za-z]*[Ee]rror")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def iter_files(root: Path, suffixes: set[str]):
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        if any(part in IGNORED_PARTS for part in path.parts):
            continue
        yield path


def scan(root: Path) -> dict[str, Any]:
    css_text = ""
    for path in iter_files(root, CSS_SUFFIXES):
        css_text += path.read_text(encoding="utf-8", errors="ignore") + "\n"

    component_text = ""
    for path in iter_files(root, COMPONENT_SUFFIXES):
        component_text += path.read_text(encoding="utf-8", errors="ignore") + "\n"

    findings = []
    for name, pattern in CSS_CHECKS:
        findings.append({"check": name, "status": "PASS" if pattern.search(css_text) else "WARN"})
    for name, pattern in COMPONENT_CHECKS:
        findings.append({"check": name, "status": "PASS" if pattern.search(component_text) else "WARN"})

    return {
        "schema_version": "1.0",
        "scanned_at": utc_now(),
        "root": str(root),
        "findings": findings,
        "warnings": sum(1 for f in findings if f["status"] == "WARN"),
    }


def render_text(report: dict[str, Any]) -> str:
    lines = ["UI QUALITY GATE", f"Root: {report['root']}", ""]
    for finding in report["findings"]:
        lines.append(f"[{finding['status']}] {finding['check']}")
    lines.append("")
    lines.append(f"Warnings: {report['warnings']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(prog="ui_quality_gate")
    parser.add_argument("root", help="Frontend source directory to scan")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on-warn", action="store_true",
                         help="Exit non-zero if any check is WARN")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"FAIL: {root} does not exist")

    report = scan(root)
    print(json.dumps(report, indent=2) if args.json else render_text(report))

    if args.fail_on_warn and report["warnings"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
