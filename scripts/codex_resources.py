#!/usr/bin/env python3
"""Codex App Server resource telemetry and five-hour-window policy.

The adapter keeps live host data, fixture data, and unobservable state distinct.
It uses only the Python standard library and the documented JSONL App Server
transport.
"""

from __future__ import annotations

import argparse
from collections import deque
import json
import os
import queue
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

FIVE_HOUR_WINDOW_MINS = 300
CONSERVE_AT_PERCENT = 75.0
CONVERGE_AT_PERCENT = 90.0
EXHAUSTED_AT_PERCENT = 100.0
STATE_RELATIVE = Path(".agent/runtime/codex-resources.json")


class AppServerError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "AGENTS.md").exists() and (candidate / "scripts").is_dir():
            return candidate
    return current


def _window(limit_id: str, bucket: str, value: dict[str, Any]) -> dict[str, Any] | None:
    duration = value.get("windowDurationMins")
    used = value.get("usedPercent")
    if not isinstance(duration, (int, float)) or not isinstance(used, (int, float)):
        return None
    return {
        "limit_id": limit_id,
        "bucket": bucket,
        "used_percent": float(used),
        "window_duration_mins": int(duration),
        "resets_at": value.get("resetsAt"),
    }


def extract_windows(rate_limits_result: dict[str, Any]) -> list[dict[str, Any]]:
    buckets = rate_limits_result.get("rateLimitsByLimitId")
    if isinstance(buckets, dict) and buckets:
        items = list(buckets.items())
    else:
        single = rate_limits_result.get("rateLimits")
        items = [] if not isinstance(single, dict) else [
            (str(single.get("limitId") or "codex"), single)
        ]

    windows: list[dict[str, Any]] = []
    for limit_id, limit_value in items:
        if not isinstance(limit_value, dict):
            continue
        for bucket in ("primary", "secondary"):
            value = limit_value.get(bucket)
            if isinstance(value, dict):
                normalized = _window(str(limit_id), bucket, value)
                if normalized:
                    windows.append(normalized)
    return windows


def normalize_resource_snapshot(
    rate_limits_result: dict[str, Any],
    usage_result: dict[str, Any],
    *,
    source: str,
    observed_at: str | None = None,
) -> dict[str, Any]:
    windows = extract_windows(rate_limits_result)
    return {
        "schema_version": "1.0",
        "source": source,
        "observed_at": observed_at or utc_now(),
        "rate_limits": rate_limits_result,
        "usage": usage_result,
        "windows": windows,
        "five_hour_windows": [
            item for item in windows
            if item["window_duration_mins"] == FIVE_HOUR_WINDOW_MINS
        ],
    }


def _validated_window(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    limit_id = value.get("limit_id")
    bucket = value.get("bucket")
    used_percent = value.get("used_percent")
    duration = value.get("window_duration_mins")
    resets_at = value.get("resets_at")
    if not isinstance(limit_id, str) or not limit_id:
        return None
    if bucket not in {"primary", "secondary"}:
        return None
    if isinstance(used_percent, bool) or not isinstance(used_percent, (int, float)):
        return None
    if isinstance(duration, bool) or not isinstance(duration, int):
        return None
    if resets_at is not None and (
        isinstance(resets_at, bool) or not isinstance(resets_at, (int, float))
    ):
        return None
    return value


def _validated_five_hour_windows(state: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(state, dict):
        return []
    raw = state.get("five_hour_windows")
    if not isinstance(raw, list):
        raw = state.get("windows", [])
    if not isinstance(raw, list):
        return []
    validated = []
    for value in raw:
        window = _validated_window(value)
        if window and window["window_duration_mins"] == FIVE_HOUR_WINDOW_MINS:
            validated.append(window)
    return validated


def assess_resource_policy(
    state: dict[str, Any] | None,
    *,
    now_epoch: float | None = None,
) -> dict[str, Any]:
    now_value = time.time() if now_epoch is None else now_epoch
    windows = _validated_five_hour_windows(state)
    if not windows:
        return {
            "mode": "UNOBSERVED",
            "action": "no-enforcement",
            "block_new_turn": False,
            "needs_refresh": True,
            "governing_window": None,
            "reason": "No Codex rate-limit window is available.",
        }

    active = []
    for item in windows:
        reset = item.get("resets_at")
        if isinstance(reset, (int, float)) and reset <= now_value:
            continue
        active.append(item)
    if not active:
        return {
            "mode": "STALE",
            "action": "refresh-required",
            "block_new_turn": False,
            "needs_refresh": True,
            "governing_window": None,
            "reason": "All persisted Codex rate-limit windows have expired.",
        }

    governing = max(active, key=lambda item: float(item.get("used_percent", 0)))
    used = float(governing.get("used_percent", 0))
    if used >= EXHAUSTED_AT_PERCENT:
        mode, action, blocked = "EXHAUSTED", "warn-user-100-percent", False
    elif used >= CONVERGE_AT_PERCENT:
        mode, action, blocked = "CONVERGE", "warn-user-90-percent", False
    elif used >= CONSERVE_AT_PERCENT:
        mode, action, blocked = "CONSERVE", "warn-user-75-percent", False
    else:
        mode, action, blocked = "NORMAL", "normal-execution", False
    return {
        "mode": mode,
        "action": action,
        "block_new_turn": blocked,
        "needs_refresh": False,
        "governing_window": governing,
        "five_hour_window": governing.get("window_duration_mins") == FIVE_HOUR_WINDOW_MINS,
        "reason": (
            f"Codex {governing['bucket']} window is {used:g}% used and resets at "
            f"{governing.get('resets_at')}."
        ),
    }


def apply_resource_policy(route: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    route["resource_policy"] = policy
    return route


def write_resource_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _validated_resource_state(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    if value.get("schema_version") != "1.0":
        return None
    if value.get("source") not in {"LIVE_HOST_DATA", "FIXTURE", "MOCK"}:
        return None
    if not isinstance(value.get("observed_at"), str):
        return None
    if not isinstance(value.get("rate_limits"), dict):
        return None
    if not isinstance(value.get("usage"), dict):
        return None
    for key in ("windows", "five_hour_windows"):
        raw = value.get(key)
        if not isinstance(raw, list):
            return None
        if any(_validated_window(item) is None for item in raw):
            return None
    return value


def load_resource_state(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return _validated_resource_state(value)


def _reader(stream: Any, messages: queue.Queue[Any]) -> None:
    try:
        for line in stream:
            if not line.strip():
                continue
            try:
                messages.put(json.loads(line))
            except json.JSONDecodeError as exc:
                messages.put(AppServerError(f"Invalid App Server JSON: {exc}"))
    finally:
        messages.put(EOFError("Codex App Server closed its output."))


def _drain_stderr(
    stream: Any,
    chunks: deque[str],
    lock: threading.Lock | None = None,
) -> None:
    while True:
        chunk = stream.read(4096)
        if not chunk:
            return
        if lock is None:
            chunks.append(chunk)
        else:
            with lock:
                chunks.append(chunk)


def _wait_for_response(
    messages: queue.Queue[Any],
    request_id: int,
    timeout_seconds: float,
    notifications: list[dict[str, Any]],
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise AppServerError(f"Timed out waiting for App Server request {request_id}.")
        try:
            message = messages.get(timeout=remaining)
        except queue.Empty as exc:
            raise AppServerError(
                f"Timed out waiting for App Server request {request_id}."
            ) from exc
        if isinstance(message, BaseException):
            raise AppServerError(str(message))
        if message.get("id") != request_id:
            if "method" in message and "id" not in message:
                notifications.append(message)
            continue
        if "error" in message:
            raise AppServerError(
                f"App Server {request_id} failed: {json.dumps(message['error'])}"
            )
        result = message.get("result")
        return result if isinstance(result, dict) else {}


def query_resource_state(
    command: Sequence[str],
    *,
    source: str = "LIVE_HOST_DATA",
    timeout_seconds: float = 15,
) -> dict[str, Any]:
    if not command:
        raise AppServerError("Codex App Server command is empty.")
    try:
        process = subprocess.Popen(
            list(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )
    except OSError as exc:
        raise AppServerError(f"Unable to start Codex App Server: {exc}") from exc

    if process.stdin is None or process.stdout is None or process.stderr is None:
        process.kill()
        raise AppServerError("Codex App Server stdio was not available.")
    messages: queue.Queue[Any] = queue.Queue()
    notifications: list[dict[str, Any]] = []
    thread = threading.Thread(
        target=_reader,
        args=(process.stdout, messages),
        daemon=True,
    )
    thread.start()
    stderr_chunks: deque[str] = deque(maxlen=16)
    stderr_lock = threading.Lock()
    stderr_thread = threading.Thread(
        target=_drain_stderr,
        args=(process.stderr, stderr_chunks, stderr_lock),
        daemon=True,
    )
    stderr_thread.start()

    def send(message: dict[str, Any]) -> None:
        process.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        process.stdin.flush()

    try:
        send({
            "method": "initialize",
            "id": 0,
            "params": {
                "clientInfo": {
                    "name": "escapement",
                    "title": "Escapement",
                    "version": "6.3.0",
                }
            },
        })
        _wait_for_response(messages, 0, timeout_seconds, notifications)
        send({"method": "initialized", "params": {}})
        send({"method": "account/rateLimits/read", "id": 1})
        rate_limits = _wait_for_response(messages, 1, timeout_seconds, notifications)
        send({"method": "account/usage/read", "id": 2})
        usage = _wait_for_response(messages, 2, timeout_seconds, notifications)

        for notification in notifications:
            if notification.get("method") == "account/rateLimits/updated":
                params = notification.get("params")
                if isinstance(params, dict) and isinstance(params.get("rateLimits"), dict):
                    rate_limits["rateLimits"] = params["rateLimits"]
        return normalize_resource_snapshot(
            rate_limits,
            usage,
            source=source,
        )
    except AppServerError as exc:
        with stderr_lock:
            stderr_tail = "".join(stderr_chunks)[-4096:]
        if stderr_tail:
            sanitized_tail = "".join(
                character if character.isprintable() else " "
                for character in stderr_tail
            )
            raise AppServerError(
                f"{exc}\nApp Server stderr tail: {sanitized_tail}"
            ) from exc
        raise
    finally:
        try:
            process.stdin.close()
        except OSError:
            pass
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
        stderr_thread.join(timeout=2)
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="codex_resources")
    sub = parser.add_subparsers(dest="command", required=True)

    read = sub.add_parser("read")
    read.add_argument("--codex-command", default=os.getenv("CODEX_COMMAND", "codex"))
    read.add_argument("--state")
    read.add_argument("--timeout", type=float, default=15)

    status = sub.add_parser("status")
    status.add_argument("--state")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = find_root()
    state_path = Path(args.state).resolve() if args.state else root / STATE_RELATIVE
    if args.command == "status":
        state = load_resource_state(state_path)
        print(json.dumps({
            "state": state,
            "policy": assess_resource_policy(state),
        }, indent=2, ensure_ascii=False))
        return 0 if state else 3

    try:
        state = query_resource_state(
            [args.codex_command, "app-server"],
            timeout_seconds=args.timeout,
        )
    except AppServerError as exc:
        print(json.dumps({
            "source": "NOT_OBSERVABLE",
            "error": str(exc),
            "state_path": str(state_path),
        }, indent=2), file=sys.stderr)
        return 2
    write_resource_state(state_path, state)
    print(json.dumps({
        "state": state,
        "policy": assess_resource_policy(state),
        "state_path": str(state_path),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
