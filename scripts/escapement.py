#!/usr/bin/env python3
"""Escapement v6.3 command-line interface.

Standard-library only.

This CLI manages:
- safe project installation and updates;
- doctor and repair;
- skill synchronisation;
- routing explanations;
- executable evaluations;
- defensive security checks;
- local run viewing;
- specification scaffolding;
- optional extensions, presets, and bundles;
- external reference and agent-pattern catalogues.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import py_compile
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

VERSION = "6.3.0"
INSTALL_RECORD = ".escapement-install.json"

ROOT_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "AGENT_RUNTIME.md",
    "SECURITY.md",
    "VERSION",
    ".claude/settings.json",
    ".github/copilot-instructions.md",
    "GEMINI.md",
]

MANAGED_PREFIXES = [
    ".agents/skills",
    ".claude/skills",
    ".codex",
    ".claude-plugin",
    ".codex-plugin",
    ".escapement",
    "skills",
    "scripts",
    "catalog",
    "docs/standards",
    "docs/templates",
    "docs/doctrine",
    "docs/CAPABILITY_MAP.md",
    "docs/ORIGINS.md",
    "docs/architecture",
    "docs/releases",
    "docs/REFERENCE_CATALOG.md",
    "profiles",
    "schemas",
    "evals",
    "extensions",
    "presets",
    "bundles",
]

PROJECT_SEEDS = {
    "PROJECT_STATE.yaml": "docs/templates/PROJECT_STATE.template.yaml",
    "PROJECT_CONTEXT.md": "docs/templates/PROJECT_CONTEXT.template.md",
    "DOMAIN_CONTEXT.md": "docs/templates/DOMAIN_CONTEXT.template.md",
    "feature_list.json": "docs/templates/feature-list.template.json",
    "SESSION_HANDOFF.md": "docs/templates/SESSION_HANDOFF.template.md",
    "THIRD_PARTY_NOTICES.md": "THIRD_PARTY_NOTICES.md",
    ".gitignore": ".gitignore",
    "docs/specs/CONSTITUTION.md": "docs/templates/spec/CONSTITUTION.template.md",
    "docs/decisions/DECISION_LOG.md": None,
    "docs/plans/.gitkeep": None,
    ".agent/runtime/ACTIVE_CONTEXT.md": "docs/templates/runtime/ACTIVE_CONTEXT.template.md",
    ".agent/runtime/CONTEXT_PACK.md": "docs/templates/runtime/CONTEXT_PACK.template.md",
    ".agent/runtime/SESSION_MEMORY.md": "docs/templates/runtime/SESSION_MEMORY.template.md",
}

NATIVE_HOSTS = [".agents", ".claude"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def find_root() -> Path:
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        for candidate in [start, *start.parents]:
            if (candidate / "AGENTS.md").exists() and (candidate / "VERSION").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


SOURCE_ROOT = find_root()


def normalize(path: Path) -> str:
    return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_target(value: str) -> Path:
    target = Path(value).expanduser().resolve()
    if target == Path(target.anchor):
        raise SystemExit("FAIL: refusing to use a filesystem root as target.")
    target.mkdir(parents=True, exist_ok=True)
    return target


def managed_files(source_root: Path = SOURCE_ROOT) -> list[str]:
    files = set(ROOT_FILES)
    for prefix in MANAGED_PREFIXES:
        path = source_root / prefix
        if path.is_file():
            files.add(prefix)
        elif path.exists():
            for child in path.rglob("*"):
                if child.is_file() and "__pycache__" not in child.parts:
                    files.add(normalize(child.relative_to(source_root)))
    return sorted(files)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def seed_content(source_relative: str | None) -> str:
    if source_relative is None:
        return (
            "# Decision Log\n\n"
            "| Date | Decision | Reason | Impact | Approver |\n"
            "|---|---|---|---|---|\n"
        )
    return (SOURCE_ROOT / source_relative).read_text(encoding="utf-8")


def install_record(target: Path) -> dict[str, Any] | None:
    value = read_json(target / INSTALL_RECORD)
    return value if isinstance(value, dict) else None


def make_record(target: Path, installed_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "product": "Escapement",
        "version": VERSION,
        "installed_at": utc_now(),
        "source": str(SOURCE_ROOT),
        "managed_files": installed_hashes,
        "project_owned_files": sorted(PROJECT_SEEDS),
    }


def copy_managed_fresh(target: Path, *, force: bool = False) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative in managed_files():
        source = SOURCE_ROOT / relative
        destination = target / relative
        if destination.exists() and not force:
            raise SystemExit(
                f"FAIL: managed file already exists: {relative}. "
                "Use update, repair, or init --force-managed."
            )
        copy_file(source, destination)
        hashes[relative] = sha256_file(destination)
    return hashes


def create_seeds(target: Path) -> list[str]:
    created = []
    for destination_relative, source_relative in PROJECT_SEEDS.items():
        destination = target / destination_relative
        if destination.exists():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(seed_content(source_relative), encoding="utf-8")
        created.append(destination_relative)
    return created


def backup_files(target: Path, relatives: Iterable[str]) -> Path | None:
    relatives = list(relatives)
    if not relatives:
        return None
    backup_root = target / ".escapement" / "backups" / timestamp()
    for relative in relatives:
        source = target / relative
        if source.exists():
            copy_file(source, backup_root / relative)
    return backup_root


def plan_update(target: Path, source_root: Path = SOURCE_ROOT) -> dict[str, list[str]]:
    record = install_record(target)
    if not record:
        raise SystemExit(
            f"FAIL: {INSTALL_RECORD} missing. Initialise the project first."
        )
    installed = record.get("managed_files", {})
    if not isinstance(installed, dict):
        installed = {}

    plan = {
        "add": [],
        "update": [],
        "unchanged": [],
        "conflict": [],
        "remove_from_framework": [],
    }
    source_files = set(managed_files(source_root))
    installed_files = set(installed)

    for relative in sorted(source_files):
        source = source_root / relative
        destination = target / relative
        source_hash = sha256_file(source)
        if not destination.exists():
            plan["add"].append(relative)
            continue
        target_hash = sha256_file(destination)
        previous_hash = installed.get(relative)
        if target_hash == source_hash:
            plan["unchanged"].append(relative)
        elif previous_hash and target_hash == previous_hash:
            plan["update"].append(relative)
        else:
            plan["conflict"].append(relative)

    for relative in sorted(installed_files - source_files):
        plan["remove_from_framework"].append(relative)
    return plan


def print_plan(plan: dict[str, list[str]]) -> None:
    for key in ("add", "update", "conflict", "remove_from_framework", "unchanged"):
        print(f"{key}: {len(plan[key])}")
        for relative in plan[key][:20]:
            print(f"  - {relative}")
        if len(plan[key]) > 20:
            print(f"  ... {len(plan[key]) - 20} more")


def command_version(_: argparse.Namespace) -> int:
    print(VERSION)
    return 0


def command_init(args: argparse.Namespace) -> int:
    target = safe_target(args.target)
    if install_record(target) and not args.force_managed:
        print("Escapement is already installed. Use update or repair.")
        return 1

    conflicts = [
        relative for relative in managed_files()
        if (target / relative).exists()
    ]
    if conflicts and not args.force_managed:
        print("FAIL: managed paths already exist:", file=sys.stderr)
        for relative in conflicts[:20]:
            print(f"  - {relative}", file=sys.stderr)
        print("Use --force-managed only after reviewing and backing up.", file=sys.stderr)
        return 1

    backup = backup_files(target, conflicts) if conflicts else None
    hashes = copy_managed_fresh(target, force=args.force_managed)
    seeds = create_seeds(target)
    write_json(target / INSTALL_RECORD, make_record(target, hashes))

    print(f"Installed Escapement {VERSION} into {target}")
    print(f"Managed files: {len(hashes)}")
    print(f"Project seed files created: {len(seeds)}")
    if backup:
        print(f"Backup: {backup}")
    print("Next: edit PROJECT_STATE.yaml and PROJECT_CONTEXT.md, then run doctor.")
    return 0


def command_update(args: argparse.Namespace) -> int:
    target = safe_target(args.target)
    plan = plan_update(target)
    print_plan(plan)
    if not args.apply:
        print("Preview only. Add --apply to update safe managed files.")
        return 0

    overwrite = list(plan["update"])
    if args.force_managed:
        overwrite.extend(plan["conflict"])
    backup = backup_files(target, overwrite)

    for relative in plan["add"] + overwrite:
        copy_file(SOURCE_ROOT / relative, target / relative)

    record = install_record(target) or {}
    hashes: dict[str, str] = {}
    for relative in managed_files():
        destination = target / relative
        if destination.exists():
            hashes[relative] = sha256_file(destination)
    record.update(make_record(target, hashes))
    record["updated_at"] = utc_now()
    write_json(target / INSTALL_RECORD, record)
    seeds = create_seeds(target)

    print(f"Applied: {len(plan['add']) + len(overwrite)}")
    print(f"Conflicts skipped: {0 if args.force_managed else len(plan['conflict'])}")
    print(f"Seed files created: {len(seeds)}")
    if backup:
        print(f"Backup: {backup}")
    return 0


def command_repair(args: argparse.Namespace) -> int:
    target = safe_target(args.target)
    record = install_record(target)
    if not record:
        print(f"FAIL: {INSTALL_RECORD} missing.", file=sys.stderr)
        return 1
    restored = []
    for relative in managed_files():
        destination = target / relative
        if not destination.exists():
            copy_file(SOURCE_ROOT / relative, destination)
            restored.append(relative)
    seeds = create_seeds(target)
    hashes = {
        relative: sha256_file(target / relative)
        for relative in managed_files()
        if (target / relative).exists()
    }
    record["managed_files"] = hashes
    record["repaired_at"] = utc_now()
    record["version"] = VERSION
    write_json(target / INSTALL_RECORD, record)
    print(f"Restored managed files: {len(restored)}")
    print(f"Created missing seeds: {len(seeds)}")
    return 0


def skill_names(root: Path) -> list[str]:
    skills_root = root / "skills"
    return sorted(
        path.parent.name
        for path in skills_root.glob("*/SKILL.md")
        if path.is_file()
    )


def sync_skills(root: Path, *, check_only: bool = False) -> tuple[int, list[str]]:
    drift: list[str] = []
    for name in skill_names(root):
        canonical = root / "skills" / name / "SKILL.md"
        canonical_hash = sha256_file(canonical)
        for host in NATIVE_HOSTS:
            target = root / host / "skills" / name / "SKILL.md"
            if not target.exists() or sha256_file(target) != canonical_hash:
                drift.append(normalize(target.relative_to(root)))
                if not check_only:
                    copy_file(canonical, target)
    return len(drift), drift


def command_sync_skills(args: argparse.Namespace) -> int:
    count, drift = sync_skills(SOURCE_ROOT, check_only=args.check)
    if drift:
        for relative in drift:
            print(relative)
    if args.check:
        print(f"Drifted native skill files: {count}")
        return 1 if count else 0
    print(f"Synchronised native skill files: {count}")
    return 0


def command_explain(args: argparse.Namespace) -> int:
    sys.path.insert(0, str(SOURCE_ROOT / "scripts"))
    from capability_router import route_prompt

    route = route_prompt(args.prompt)
    print(json.dumps(route, indent=2))
    return 0



def command_capability_audit(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SOURCE_ROOT / "scripts" / "capability_audit.py"),
        args.prompt,
    ]
    if args.markdown:
        command.append("--markdown")
    if args.output:
        command.extend(["--output", args.output])
    return subprocess.run(command, cwd=SOURCE_ROOT, check=False).returncode


def command_codex_resources(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SOURCE_ROOT / "scripts" / "codex_resources.py"),
        args.resource_command,
    ]
    if args.state:
        command.extend(["--state", args.state])
    if args.resource_command == "read":
        if args.codex_command:
            command.extend(["--codex-command", args.codex_command])
        command.extend(["--timeout", str(args.timeout)])
    return subprocess.run(command, cwd=SOURCE_ROOT, check=False).returncode


def command_eval(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SOURCE_ROOT / "scripts" / "eval_harness.py"),
        "run",
    ]
    if args.resume:
        command.append("--resume")
    if args.suite:
        command.extend(["--suite", args.suite])
    return subprocess.run(command, cwd=SOURCE_ROOT, check=False).returncode


def command_security(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SOURCE_ROOT / "scripts" / "security_gate.py"),
        "--fail-on",
        args.fail_on,
    ]
    if args.json:
        command.append("--json")
    return subprocess.run(command, cwd=SOURCE_ROOT, check=False).returncode


def command_observability(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SOURCE_ROOT / "scripts" / "harness_observability.py"),
        "--root",
        args.root,
    ]
    if args.json:
        command.append("--json")
    return subprocess.run(command, check=False).returncode


def command_ablate(args: argparse.Namespace) -> int:
    command = [sys.executable, str(SOURCE_ROOT / "scripts" / "ablation_harness.py")]
    if args.component:
        command += ["run", args.component]
        if args.json:
            command.append("--json")
        if args.keep:
            command.append("--keep")
    else:
        command.append("list")
    return subprocess.run(command, check=False).returncode


def command_view(args: argparse.Namespace) -> int:
    command = [sys.executable, str(SOURCE_ROOT / "scripts" / "local_viewer.py")]
    if args.no_open:
        command.append("--no-open")
    if args.port is not None:
        command.extend(["--port", str(args.port)])
    return subprocess.run(command, cwd=SOURCE_ROOT, check=False).returncode


def component_roots(component_type: str) -> Path:
    mapping = {
        "extension": SOURCE_ROOT / "extensions",
        "preset": SOURCE_ROOT / "presets",
        "bundle": SOURCE_ROOT / "bundles",
    }
    return mapping[component_type]


def component_manifest(component_type: str, name: str) -> tuple[Path, dict[str, Any]]:
    root = component_roots(component_type) / name
    manifest = read_json(root / "component.json")
    if not isinstance(manifest, dict):
        raise SystemExit(f"FAIL: component not found: {component_type}/{name}")
    return root, manifest


def command_component_list(args: argparse.Namespace) -> int:
    types = [args.type] if args.type else ["extension", "preset", "bundle"]
    for component_type in types:
        base = component_roots(component_type)
        for manifest_path in sorted(base.glob("*/component.json")):
            manifest = read_json(manifest_path, {})
            print(
                f"{component_type}/{manifest.get('name')} "
                f"{manifest.get('version')} — {manifest.get('description')}"
            )
    return 0


def command_component_info(args: argparse.Namespace) -> int:
    _, manifest = component_manifest(args.type, args.name)
    print(json.dumps(manifest, indent=2))
    return 0


def command_component_install(args: argparse.Namespace) -> int:
    target = safe_target(args.target)
    component_root, manifest = component_manifest(args.type, args.name)
    if manifest.get("approval_required") and not args.approved:
        print(
            "FAIL: this component requires explicit approval. Re-run with --approved "
            "after reviewing its source, licence, security, network, and credentials.",
            file=sys.stderr,
        )
        return 1
    files_root = component_root / str(manifest.get("files_root", "files"))
    installed = []
    skipped = []
    for source in sorted(files_root.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(files_root)
        destination = target / relative
        if destination.exists() and not args.force:
            skipped.append(normalize(relative))
            continue
        copy_file(source, destination)
        installed.append(normalize(relative))

    # Skills supplied under files/skills are fanned out into both native hosts.
    skills_source = files_root / "skills"
    if skills_source.exists():
        for source in skills_source.glob("*/SKILL.md"):
            name = source.parent.name
            for host in NATIVE_HOSTS:
                destination = target / host / "skills" / name / "SKILL.md"
                if destination.exists() and not args.force:
                    continue
                copy_file(source, destination)

    receipt = target / ".escapement" / "components" / args.type / f"{args.name}.json"
    write_json(receipt, {
        "component": manifest,
        "installed_at": utc_now(),
        "files": installed,
        "skipped": skipped,
    })
    print(f"Installed files: {len(installed)}")
    print(f"Skipped existing files: {len(skipped)}")
    print(f"Receipt: {receipt}")
    return 0


def load_external_catalog() -> dict[str, Any]:
    # external-resources.json is deprecated (marked so in its own JSON, in favour of
    # this file) and has fallen behind: 47 resources vs. this file's 54.
    value = read_json(SOURCE_ROOT / "catalog" / "capability-registry.json", {})
    return value if isinstance(value, dict) else {}


def load_agent_catalog() -> dict[str, Any]:
    value = read_json(SOURCE_ROOT / "catalog" / "agent-patterns.json", {})
    return value if isinstance(value, dict) else {}


def load_native_skill_catalog() -> dict[str, Any]:
    value = read_json(SOURCE_ROOT / "catalog" / "native-skills.json", {})
    return value if isinstance(value, dict) else {}


def skill_description(skill_id: str) -> str:
    """The one-line human description lives in the skill's own SKILL.md
    frontmatter -- native-skills.json only carries routing data (triggers,
    phases, overlap group), so a browsing user needs this, not that."""
    path = SOURCE_ROOT / "skills" / skill_id / "SKILL.md"
    if not path.exists():
        return ""
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        return ""
    for line in parts[1].splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def catalog_items(catalog: str) -> list[dict[str, Any]]:
    if catalog == "resources":
        return load_external_catalog().get("resources", [])
    if catalog == "skills":
        return load_native_skill_catalog().get("skills", [])
    return load_agent_catalog().get("patterns", [])


def command_catalog_list(args: argparse.Namespace) -> int:
    items = catalog_items(args.catalog)
    if args.catalog == "resources":
        for item in items:
            print(
                f"{item.get('id')}: {item.get('name')} | {item.get('license')} | "
                f"{', '.join(item.get('use_modes', []))}"
            )
    elif args.catalog == "skills":
        for item in items:
            phases = ", ".join(item.get("phases", []))
            print(f"{item['id']}: {skill_description(item['id'])} | phases: {phases}")
    else:
        for item in items:
            print(f"{item.get('id')}: {item.get('name')} | {item.get('category')}")
    return 0


def search_item(item: dict[str, Any], query: str) -> bool:
    text = json.dumps(item, ensure_ascii=False).lower()
    return all(token in text for token in query.lower().split())


def command_catalog_search(args: argparse.Namespace) -> int:
    items = catalog_items(args.catalog)
    if args.catalog == "skills":
        items = [{**item, "description": skill_description(item["id"])} for item in items]
    matches = [item for item in items if search_item(item, args.query)]
    for item in matches:
        print(json.dumps(item, indent=2, ensure_ascii=False))
    print(f"Matches: {len(matches)}")
    return 0 if matches else 1


def render_template(template: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def command_spec_constitution(args: argparse.Namespace) -> int:
    target = Path(args.root).expanduser().resolve()
    destination = target / "docs" / "specs" / "CONSTITUTION.md"
    if destination.exists() and not args.force:
        print(f"Exists: {destination}")
        return 0
    source = SOURCE_ROOT / "docs/templates/spec/CONSTITUTION.template.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    print(destination)
    return 0


def feature_dir(target: Path, name: str) -> Path:
    safe = "".join(char if char.isalnum() or char in "-_" else "-" for char in name)
    return target / "docs" / "specs" / safe


def command_spec_create(args: argparse.Namespace) -> int:
    target = Path(args.root).expanduser().resolve()
    directory = feature_dir(target, args.name)
    destination = directory / "SPEC.md"
    if destination.exists() and not args.force:
        print(f"Exists: {destination}")
        return 0
    template = (SOURCE_ROOT / "docs/templates/spec/SPEC.template.md").read_text(
        encoding="utf-8"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render_template(template, {"NAME": args.name, "GOAL": args.goal}),
        encoding="utf-8",
    )
    print(destination)
    return 0


def command_spec_plan(args: argparse.Namespace) -> int:
    target = Path(args.root).expanduser().resolve()
    directory = feature_dir(target, args.name)
    if not (directory / "SPEC.md").exists():
        print("FAIL: create SPEC.md first.", file=sys.stderr)
        return 1
    destination = directory / "PLAN.md"
    template = (SOURCE_ROOT / "docs/templates/spec/PLAN.template.md").read_text(
        encoding="utf-8"
    )
    if not destination.exists() or args.force:
        destination.write_text(
            render_template(template, {"NAME": args.name}),
            encoding="utf-8",
        )
    print(destination)
    return 0


def command_spec_tasks(args: argparse.Namespace) -> int:
    target = Path(args.root).expanduser().resolve()
    directory = feature_dir(target, args.name)
    if not (directory / "SPEC.md").exists() or not (directory / "PLAN.md").exists():
        print("FAIL: create SPEC.md and PLAN.md first.", file=sys.stderr)
        return 1
    destination = directory / "TASKS.md"
    template = (SOURCE_ROOT / "docs/templates/spec/TASKS.template.md").read_text(
        encoding="utf-8"
    )
    if not destination.exists() or args.force:
        destination.write_text(
            render_template(template, {"NAME": args.name}),
            encoding="utf-8",
        )
    print(destination)
    return 0


def command_doctor(args: argparse.Namespace) -> int:
    target = Path(args.root).expanduser().resolve()
    failures = 0
    warnings = 0
    print("ESCAPEMENT DOCTOR")
    print(f"Version: {VERSION}")
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 10):
        print("[FAIL] Python 3.10+ required")
        failures += 1
    else:
        print("[PASS] Python version")

    required = [
        "AGENTS.md",
        "CLAUDE.md",
        "AGENT_RUNTIME.md",
        "PROJECT_STATE.yaml",
        "PROJECT_CONTEXT.md",
        "feature_list.json",
        "DOMAIN_CONTEXT.md",
        ".codex/hooks.json",
        ".claude/settings.json",
        ".github/copilot-instructions.md",
        "GEMINI.md",
        "scripts/agent_runtime.py",
        "scripts/codex_resources.py",
        "scripts/run_check.py",
        "scripts/feature_list.py",
        "catalog/capability-registry.json",
        "schemas/codex-resource-state.schema.json",
    ]
    for relative in required:
        ok = (target / relative).exists()
        print(f"[{'PASS' if ok else 'FAIL'}] {relative}")
        failures += int(not ok)

    for relative in (".codex/hooks.json", ".claude/settings.json"):
        path = target / relative
        if path.exists():
            try:
                json.loads(path.read_text(encoding="utf-8"))
                print(f"[PASS] JSON {relative}")
            except Exception as exc:
                print(f"[FAIL] JSON {relative}: {exc}")
                failures += 1

    count, drift = sync_skills(target, check_only=True)
    if count:
        print(f"[FAIL] native skill drift: {count}")
        failures += count
        for relative in drift[:10]:
            print(f"  - {relative}")
    else:
        print("[PASS] native skills synchronised")

    feature_process = subprocess.run(
        [sys.executable, str(target / "scripts/feature_list.py"), "check"],
        cwd=target,
        text=True,
        capture_output=True,
        check=False,
    ) if (target / "scripts/feature_list.py").exists() else None
    if feature_process and feature_process.returncode == 0:
        print("[PASS] feature list")
    else:
        print("[FAIL] feature list")
        failures += 1

    state_text = (target / "PROJECT_STATE.yaml").read_text(
        encoding="utf-8", errors="replace"
    ) if (target / "PROJECT_STATE.yaml").exists() else ""
    if "project_name: TBD" in state_text:
        print("[WARN] project name is still TBD")
        warnings += 1

    marker = install_record(target)
    if marker:
        print(f"[PASS] install record version {marker.get('version')}")

        # Existence and version-string checks above cannot detect that an installed
        # copy's managed files (scripts/, catalog/, etc.) have silently drifted from
        # the source clone's current content -- a fix landing in the source after
        # this project was installed leaves the old, unpatched bytes here with no
        # warning. The install record already stores the source path used at
        # install time; use it to run the same comparison `update` does.
        source_path = marker.get("source")
        source_root = Path(source_path).expanduser() if source_path else None
        if source_root and (source_root / "scripts/escapement.py").exists():
            plan = plan_update(target, source_root=source_root)
            stale = len(plan["update"]) + len(plan["conflict"]) + len(plan["add"])
            if stale:
                print(f"[WARN] {stale} managed file(s) differ from the source install")
                for relative in (plan["update"] + plan["add"])[:10]:
                    print(f"  - {relative}")
                for relative in plan["conflict"][:10]:
                    print(f"  - {relative} (locally modified -- needs --force-managed)")
                print(f"  Run: python {source_root}/scripts/escapement.py update {target} --apply")
                warnings += 1
            else:
                print("[PASS] managed files match the source install")
        elif source_root:
            print(f"[WARN] recorded source no longer reachable: {source_root}")
            warnings += 1
    elif target != SOURCE_ROOT:
        print(f"[WARN] {INSTALL_RECORD} missing")
        warnings += 1

    print(f"\nFailures: {failures}")
    print(f"Warnings: {warnings}")
    return 1 if failures else 0


def command_self_test(_: argparse.Namespace) -> int:
    failures = 0
    scripts = sorted((SOURCE_ROOT / "scripts").glob("*.py"))
    for script in scripts:
        try:
            py_compile.compile(str(script), doraise=True)
            print(f"[PASS] compile {script.name}")
        except py_compile.PyCompileError as exc:
            print(f"[FAIL] compile {script.name}: {exc}")
            failures += 1

    steps = [
        [sys.executable, "scripts/feature_list.py", "check"],
        [sys.executable, "scripts/eval_harness.py", "run", "--fail-fast"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
    ]
    for command in steps:
        process = subprocess.run(
            command,
            cwd=SOURCE_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        name = " ".join(command[1:])
        if process.returncode == 0:
            print(f"[PASS] {name}")
        else:
            print(f"[FAIL] {name}")
            print(process.stdout[-1500:])
            print(process.stderr[-1500:], file=sys.stderr)
            failures += 1

    with tempfile.TemporaryDirectory(prefix="escapement-selftest-") as temp:
        target = Path(temp) / "project"
        process = subprocess.run(
            [sys.executable, str(Path(__file__)), "init", str(target)],
            cwd=SOURCE_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if process.returncode:
            print("[FAIL] fresh init")
            failures += 1
        else:
            doctor = subprocess.run(
                [sys.executable, str(target / "scripts/escapement.py"), "doctor", "--root", str(target)],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            if doctor.returncode:
                print("[FAIL] fresh install doctor")
                print(doctor.stdout[-1500:])
                failures += 1
            else:
                print("[PASS] fresh install doctor")

    print(f"Failures: {failures}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="escapement")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("version").set_defaults(func=command_version)

    init = sub.add_parser("init")
    init.add_argument("target")
    init.add_argument("--force-managed", action="store_true")
    init.set_defaults(func=command_init)

    update = sub.add_parser("update")
    update.add_argument("target")
    update.add_argument("--apply", action="store_true")
    update.add_argument("--force-managed", action="store_true")
    update.set_defaults(func=command_update)

    repair = sub.add_parser("repair")
    repair.add_argument("target")
    repair.set_defaults(func=command_repair)

    doctor = sub.add_parser("doctor")
    doctor.add_argument("--root", default=".")
    doctor.set_defaults(func=command_doctor)

    observability = sub.add_parser("observability")
    observability.add_argument("--root", default=".")
    observability.add_argument("--json", action="store_true")
    observability.set_defaults(func=command_observability)

    ablate = sub.add_parser("ablate")
    ablate.add_argument("component", nargs="?", help="omit to list ablatable components")
    ablate.add_argument("--json", action="store_true")
    ablate.add_argument("--keep", action="store_true")
    ablate.set_defaults(func=command_ablate)

    sync = sub.add_parser("sync-skills")
    sync.add_argument("--check", action="store_true")
    sync.set_defaults(func=command_sync_skills)

    explain = sub.add_parser("explain")
    explain.add_argument("prompt")
    explain.set_defaults(func=command_explain)

    capability_audit = sub.add_parser("capability-audit")
    capability_audit.add_argument("prompt")
    capability_audit.add_argument("--markdown", action="store_true")
    capability_audit.add_argument("--output")
    capability_audit.set_defaults(func=command_capability_audit)

    codex_resources = sub.add_parser("codex-resources")
    codex_resources_sub = codex_resources.add_subparsers(
        dest="resource_command",
        required=True,
    )
    resource_read = codex_resources_sub.add_parser("read")
    resource_read.add_argument("--codex-command")
    resource_read.add_argument("--state")
    resource_read.add_argument("--timeout", type=float, default=15)
    resource_read.set_defaults(func=command_codex_resources)
    resource_status = codex_resources_sub.add_parser("status")
    resource_status.add_argument("--state")
    resource_status.set_defaults(func=command_codex_resources)

    eval_parser = sub.add_parser("eval")
    eval_parser.add_argument("--resume", action="store_true")
    eval_parser.add_argument("--suite")
    eval_parser.set_defaults(func=command_eval)

    security = sub.add_parser("security")
    security.add_argument(
        "--fail-on",
        choices=["info", "low", "medium", "high", "critical"],
        default="high",
    )
    security.add_argument("--json", action="store_true")
    security.set_defaults(func=command_security)

    view = sub.add_parser("view")
    view.add_argument("--port", type=int)
    view.add_argument("--no-open", action="store_true")
    view.set_defaults(func=command_view)

    component = sub.add_parser("component")
    component_sub = component.add_subparsers(dest="component_command", required=True)
    component_list = component_sub.add_parser("list")
    component_list.add_argument("--type", choices=["extension", "preset", "bundle"])
    component_list.set_defaults(func=command_component_list)
    info = component_sub.add_parser("info")
    info.add_argument("type", choices=["extension", "preset", "bundle"])
    info.add_argument("name")
    info.set_defaults(func=command_component_info)
    install = component_sub.add_parser("install")
    install.add_argument("type", choices=["extension", "preset", "bundle"])
    install.add_argument("name")
    install.add_argument("target")
    install.add_argument("--approved", action="store_true")
    install.add_argument("--force", action="store_true")
    install.set_defaults(func=command_component_install)

    catalog = sub.add_parser("catalog")
    catalog_sub = catalog.add_subparsers(dest="catalog_command", required=True)
    catalog_list = catalog_sub.add_parser("list")
    catalog_list.add_argument(
        "--catalog",
        choices=["resources", "patterns", "skills"],
        default="resources",
    )
    catalog_list.set_defaults(func=command_catalog_list)
    catalog_search = catalog_sub.add_parser("search")
    catalog_search.add_argument("query")
    catalog_search.add_argument(
        "--catalog",
        choices=["resources", "patterns", "skills"],
        default="resources",
    )
    catalog_search.set_defaults(func=command_catalog_search)

    spec = sub.add_parser("spec")
    spec_sub = spec.add_subparsers(dest="spec_command", required=True)
    constitution = spec_sub.add_parser("constitution")
    constitution.add_argument("--root", default=".")
    constitution.add_argument("--force", action="store_true")
    constitution.set_defaults(func=command_spec_constitution)
    create = spec_sub.add_parser("create")
    create.add_argument("--name", required=True)
    create.add_argument("--goal", required=True)
    create.add_argument("--root", default=".")
    create.add_argument("--force", action="store_true")
    create.set_defaults(func=command_spec_create)
    plan = spec_sub.add_parser("plan")
    plan.add_argument("--name", required=True)
    plan.add_argument("--root", default=".")
    plan.add_argument("--force", action="store_true")
    plan.set_defaults(func=command_spec_plan)
    tasks = spec_sub.add_parser("tasks")
    tasks.add_argument("--name", required=True)
    tasks.add_argument("--root", default=".")
    tasks.add_argument("--force", action="store_true")
    tasks.set_defaults(func=command_spec_tasks)

    sub.add_parser("self-test").set_defaults(func=command_self_test)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
