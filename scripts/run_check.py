#!/usr/bin/env python3
"""Run a deterministic command and persist a content-addressed check record."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def stable_record_id(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"check:{hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:32]}"


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="run_check")
    parser.add_argument("--name", required=True)
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--cwd", default=".")
    parser.add_argument("--timeout", type=int, default=0)
    parser.add_argument(
        "--shell",
        help="Run one trusted shell command string instead of argv after --.",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.shell and args.command:
        print("FAIL: choose --shell or argv after --, not both.", file=sys.stderr)
        return 2

    command_argv = list(args.command)
    if command_argv and command_argv[0] == "--":
        command_argv = command_argv[1:]

    if not args.shell and not command_argv:
        print("FAIL: no command supplied.", file=sys.stderr)
        return 2

    cwd = (ROOT / args.cwd).resolve()
    try:
        cwd.relative_to(ROOT.resolve())
    except ValueError:
        print("FAIL: --cwd must remain inside the repository.", file=sys.stderr)
        return 2
    if not cwd.exists():
        print(f"FAIL: cwd does not exist: {cwd}", file=sys.stderr)
        return 2

    started_at = utc_now()
    started_monotonic = time.monotonic()
    provisional = hashlib.sha256(
        f"{args.name}|{started_at}|{args.shell or command_argv}".encode("utf-8")
    ).hexdigest()[:16]
    output_dir = ROOT / ".agent" / "evidence" / "checks" / provisional
    output_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = output_dir / "stdout.txt"
    stderr_path = output_dir / "stderr.txt"

    try:
        completed = subprocess.run(
            args.shell if args.shell else command_argv,
            cwd=cwd,
            shell=bool(args.shell),
            text=True,
            capture_output=True,
            timeout=args.timeout or None,
            check=False,
        )
        exit_code = int(completed.returncode)
        stdout_text = completed.stdout or ""
        stderr_text = completed.stderr or ""
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout_text = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr_text = (
            ((exc.stderr or "") if isinstance(exc.stderr, str) else "")
            + f"\nCommand timed out after {args.timeout} seconds.\n"
        )

    stdout_path.write_text(stdout_text, encoding="utf-8")
    stderr_path.write_text(stderr_text, encoding="utf-8")
    completed_at = utc_now()
    command_value: str | list[str] = args.shell if args.shell else command_argv

    identity = {
        "name": args.name,
        "command": command_value,
        "started_at": started_at,
        "completed_at": completed_at,
        "exit_code": exit_code,
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_sha256": sha256_file(stderr_path),
    }
    record = {
        "record_type": "check",
        "record_id": stable_record_id(identity),
        "schema_version": "1.0",
        "name": args.name,
        "command": command_value,
        "command_display": args.shell or shlex.join(command_argv),
        "cwd": relative(cwd),
        "scope": args.scope,
        "started_at": started_at,
        "completed_at": completed_at,
        "duration_seconds": round(time.monotonic() - started_monotonic, 3),
        "exit_code": exit_code,
        "result": "PASS" if exit_code == 0 else "FAIL",
        "stdout_path": relative(stdout_path),
        "stderr_path": relative(stderr_path),
        "stdout_sha256": identity["stdout_sha256"],
        "stderr_sha256": identity["stderr_sha256"],
    }

    record_path = output_dir / "record.json"
    record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(relative(record_path))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
