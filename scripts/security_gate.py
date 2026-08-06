#!/usr/bin/env python3
"""Defensive, local Escapement security gate."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SEVERITY = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
TEXT_SUFFIXES = {
    ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".sh", ".ps1", ".env",
}
IGNORED_PARTS = {
    ".git", "node_modules", ".venv", "venv", "dist", "build", ".agent",
    "__pycache__", ".pytest_cache",
    # update/repair --force-managed back up the previous file under
    # .escapement/backups/<timestamp>/ before overwriting it. security_gate.py
    # itself contains its own detection regexes as literal string content, so
    # a backup copy of security_gate.py matches its own patterns (e.g.
    # powershell-download-exec) -- a deterministic false positive on every
    # backup of this file, in every project that has ever run update/repair.
    "backups",
}

SECRET_PATTERNS = [
    ("private-key", "critical", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws-access-key", "high", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token", "high", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")),
    # anthropic-key must be checked before openai-key: both start "sk-", so an
    # Anthropic key (sk-ant-...) already matched openai-key's bare \bsk-...\b
    # pattern and was reported under the wrong provider's label -- caught, but
    # misleadingly, on a framework built primarily for Claude Code/Anthropic's
    # own tooling. openai-key now excludes the ant- prefix so each secret gets
    # exactly one correct label, not a double or mislabeled report.
    ("anthropic-key", "high", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}\b")),
    ("openai-key", "high", re.compile(r"\bsk-(?!ant-)[A-Za-z0-9_-]{20,}\b")),
    ("perplexity-key", "high", re.compile(r"\bpplx-[A-Za-z0-9_-]{20,}\b")),
    # The keyword is intentionally not \b-bounded on its leading edge: \b requires a
    # non-word character immediately before the match, but an underscore (as in
    # admin_password, db_secret, stripe_api_key) IS a word character, so a plain
    # \bpassword\b silently misses every prefixed identifier -- which is the common
    # naming convention, not the exception. (?:^|[^a-zA-Z]) accepts start-of-line or
    # any separator, including underscores, while still requiring a real word to
    # precede the keyword (so "secretary = ..." can still match; this pattern is
    # medium severity and does not fail --fail-on high on its own).
    ("generic-secret-assignment", "medium", re.compile(
        r"(?i)(?:^|[^a-zA-Z])(api[_-]?key|secret|password|token)(?:[a-zA-Z_]*)?"
        r"\s*[:=]\s*[\"'][^\"'\n]{12,}[\"']"
    )),
]

RISKY_COMMANDS = [
    ("remote-pipe-shell", "high", re.compile(r"(?i)\b(curl|wget)\b[^\n|]*\|\s*(bash|sh|zsh)\b")),
    ("recursive-force-delete", "high", re.compile(r"\brm\s+-rf\s+[/~]")),
    ("world-writable", "medium", re.compile(r"\bchmod\s+(?:-R\s+)?777\b")),
    ("powershell-download-exec", "high", re.compile(r"(?i)Invoke-Expression|iex\s*\(")),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def is_candidate(path: Path) -> bool:
    if any(part in IGNORED_PARTS for part in path.parts):
        return False
    if path.name.startswith(".env") or path.suffix.lower() in TEXT_SUFFIXES:
        return True
    return path.name in {"Dockerfile", "Makefile"}


def add_finding(
    findings: list[dict[str, Any]],
    *,
    finding_id: str,
    severity: str,
    category: str,
    path: str,
    line: int | None,
    message: str,
    remediation: str,
) -> None:
    findings.append({
        "id": finding_id,
        "severity": severity,
        "category": category,
        "path": path,
        "line": line,
        "message": message,
        "remediation": remediation,
    })


def scan_text_file(path: Path, findings: list[dict[str, Any]]) -> None:
    # Do not flag the scanner's own detection regexes as repository findings.
    if path.resolve() == Path(__file__).resolve():
        return
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    rel = relative(path)
    for line_number, line in enumerate(text.splitlines(), 1):
        # Avoid flagging clearly fake/documented placeholders.
        placeholder = any(
            token in line.lower()
            for token in ("your-api-key", "example", "placeholder", "fake", "redacted")
        )
        for name, severity, pattern in SECRET_PATTERNS:
            if not placeholder and pattern.search(line):
                add_finding(
                    findings,
                    finding_id=f"{name}:{rel}:{line_number}",
                    severity=severity,
                    category="secret",
                    path=rel,
                    line=line_number,
                    message=f"Possible {name} detected.",
                    remediation="Remove the value, rotate it, and use approved secret storage.",
                )
        for name, severity, pattern in RISKY_COMMANDS:
            if pattern.search(line):
                add_finding(
                    findings,
                    finding_id=f"{name}:{rel}:{line_number}",
                    severity=severity,
                    category="command",
                    path=rel,
                    line=line_number,
                    message=f"Risky command pattern: {name}.",
                    remediation="Replace with a checksum-pinned, reviewed, least-privilege workflow.",
                )


def scan_hooks(findings: list[dict[str, Any]]) -> None:
    for rel in (".codex/hooks.json", ".claude/settings.json"):
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            add_finding(
                findings,
                finding_id=f"invalid-hook-json:{rel}",
                severity="high",
                category="hook",
                path=rel,
                line=None,
                message=f"Invalid hook JSON: {exc}",
                remediation="Repair the project hook configuration before approval.",
            )
            continue
        text = json.dumps(data)
        if "agent_runtime.py" not in text and "escapement-hook" not in text:
            add_finding(
                findings,
                finding_id=f"unexpected-hook:{rel}",
                severity="medium",
                category="hook",
                path=rel,
                line=None,
                message="Hook configuration does not reference the Escapement runtime.",
                remediation="Review every hook command and remove unapproved executables.",
            )
        if "http://" in text or "https://" in text:
            add_finding(
                findings,
                finding_id=f"network-hook:{rel}",
                severity="high",
                category="hook",
                path=rel,
                line=None,
                message="Project hook configuration contains a network URL.",
                remediation="Do not perform network installation or remote execution from lifecycle hooks.",
            )


def scan_mcp(findings: list[dict[str, Any]]) -> None:
    candidates = [
        ".mcp.json",
        "mcp.json",
        ".claude/settings.json",
        ".codex-plugin/plugin.json",
        ".claude-plugin/plugin.json",
    ]
    for rel in candidates:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            data = json.loads(text)
        except Exception:
            data = {}

        server_blocks = []
        if isinstance(data, dict):
            for key in ("mcpServers", "mcp_servers"):
                value = data.get(key)
                if isinstance(value, dict):
                    server_blocks.append(value)

        for servers in server_blocks:
            for name, config in servers.items():
                config_text = json.dumps(config)
                if "http://" in config_text or "https://" in config_text:
                    add_finding(
                        findings,
                        finding_id=f"remote-mcp:{rel}:{name}",
                        severity="medium",
                        category="mcp",
                        path=rel,
                        line=None,
                        message=f"Remote MCP endpoint is configured: {name}.",
                        remediation="Verify owner, tools, authentication, data flow, and approval before use.",
                    )
                if isinstance(config, dict) and isinstance(config.get("env"), dict) and config.get("env"):
                    add_finding(
                        findings,
                        finding_id=f"mcp-env:{rel}:{name}",
                        severity="medium",
                        category="mcp",
                        path=rel,
                        line=None,
                        message=f"MCP configuration includes environment values: {name}.",
                        remediation="Ensure secrets are references, not committed literal values.",
                    )


def main() -> int:
    parser = argparse.ArgumentParser(prog="security_gate")
    parser.add_argument(
        "--fail-on",
        choices=list(SEVERITY),
        default="high",
        help="Exit non-zero when a finding at or above this severity exists.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, Any]] = []
    for path in ROOT.rglob("*"):
        if path.is_file() and is_candidate(path):
            scan_text_file(path, findings)
    scan_hooks(findings)
    scan_mcp(findings)

    findings.sort(
        key=lambda item: (-SEVERITY[item["severity"]], item["path"], item.get("line") or 0)
    )
    report = {
        "record_type": "security-report",
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "root": str(ROOT),
        "fail_on": args.fail_on,
        "findings": findings,
        "counts": {
            severity: sum(1 for item in findings if item["severity"] == severity)
            for severity in SEVERITY
        },
    }
    report_path = ROOT / ".agent" / "security" / "report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("ESCAPEMENT SECURITY GATE")
        for item in findings:
            location = item["path"] + (
                f":{item['line']}" if item.get("line") else ""
            )
            print(f"[{item['severity'].upper()}] {location} — {item['message']}")
        print(f"\nReport: {relative(report_path)}")
        print(f"Findings: {len(findings)}")

    threshold = SEVERITY[args.fail_on]
    return 1 if any(SEVERITY[item["severity"]] >= threshold for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
