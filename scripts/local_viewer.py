#!/usr/bin/env python3
"""Privacy-first local Escapement run viewer."""

from __future__ import annotations

import argparse
import html
import json
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()


def read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def read_jsonl(path: Path, limit: int = 200):
    if not path.exists():
        return []
    records = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError:
            pass
    return records


def build_data() -> dict:
    return {
        "project_state": (ROOT / "PROJECT_STATE.yaml").read_text(
            encoding="utf-8", errors="replace"
        ) if (ROOT / "PROJECT_STATE.yaml").exists() else "",
        "feature_list": read_json(ROOT / "feature_list.json"),
        "current_turn": read_json(ROOT / ".agent/runtime/current-turn.json"),
        "session_handoff": (ROOT / "SESSION_HANDOFF.md").read_text(
            encoding="utf-8", errors="replace"
        ) if (ROOT / "SESSION_HANDOFF.md").exists() else "",
        "turns": read_jsonl(ROOT / ".agent/runtime/turns.jsonl"),
        "skill_runs": read_jsonl(ROOT / "logs/skill-usage.jsonl"),
        "eval_summary": read_json(ROOT / ".agent/evals/summary.json"),
        "security_report": read_json(ROOT / ".agent/security/report.json"),
    }


def page(token: str) -> str:
    data = build_data()
    escaped = html.escape(json.dumps(data, indent=2, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Escapement Local Viewer</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f5f5f7;color:#1c1c1f}}
header{{background:#53284f;color:white;padding:24px 32px}}
main{{max-width:1200px;margin:auto;padding:24px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}}
.card{{background:white;border:1px solid #dddde3;border-radius:10px;padding:16px;overflow:auto}}
h1,h2{{margin-top:0}} pre{{white-space:pre-wrap;word-break:break-word;font-size:12px}}
.small{{opacity:.8;font-size:13px}}
</style>
</head>
<body>
<header><h1>Escapement Local Viewer</h1><div class="small">Local-only · no analytics · no external assets</div></header>
<main>
<div class="grid">
<div class="card"><h2>Feature State</h2><pre>{html.escape(json.dumps(data.get("feature_list"), indent=2))}</pre></div>
<div class="card"><h2>Current Turn</h2><pre>{html.escape(json.dumps(data.get("current_turn"), indent=2))}</pre></div>
<div class="card"><h2>Evaluation</h2><pre>{html.escape(json.dumps(data.get("eval_summary"), indent=2))}</pre></div>
<div class="card"><h2>Security</h2><pre>{html.escape(json.dumps(data.get("security_report"), indent=2))}</pre></div>
<div class="card"><h2>Session Handoff</h2><pre>{html.escape(data.get("session_handoff") or "")}</pre></div>
<div class="card"><h2>Recent Skill Runs</h2><pre>{html.escape(json.dumps(data.get("skill_runs"), indent=2))}</pre></div>
</div>
<details class="card" style="margin-top:16px"><summary>Raw local data</summary><pre>{escaped}</pre></details>
</main>
</body>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(prog="local_viewer")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()
    token = secrets.token_urlsafe(24)

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            if query.get("token", [""])[0] != token:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b"Forbidden")
                return
            if parsed.path == "/api/data":
                payload = json.dumps(build_data(), ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(payload)
                return
            payload = page(token).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format, *args):
            return

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    host, port = server.server_address
    url = f"http://{host}:{port}/?token={token}"
    print(url)
    if not args.no_open:
        threading.Timer(0.25, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
