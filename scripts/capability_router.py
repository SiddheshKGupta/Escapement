#!/usr/bin/env python3
"""Escapement v6.3 capability-strength router.

The router keeps each active phase small while making the complete lifecycle
rich in domain research, decision coaching, brainstorming, planning, specialist
agents, implementation skills and independent verification.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

VERSION = "6.3.0"

INFO_WORDS = [
    r"\bwhat is\b", r"\bexplain\b", r"\bstatus\b", r"\bshow me\b",
    r"\bwhere is\b", r"\bhow does\b",
]
MATERIAL_WORDS = [
    r"\bbuild\b", r"\bcreate\b", r"\bimplement\b", r"\badd\b",
    r"\bchange\b", r"\bupdate\b", r"\bfix\b", r"\bdebug\b",
    r"\brefactor\b", r"\breviews?\b", r"\bdesign\b", r"\btests?\b",
    r"\bverify\b", r"\bverification\b", r"\bvalidate\b",
    r"\bdeploy\b", r"\bintegrate\b", r"\banaly[sz]e\b", r"\baudit\b",
    r"\bplan\b", r"\bdraft\b", r"\bmigrate\b", r"\bwrite\b",
    r"\bpolish\b", r"\brewrite\b", r"\bproofread\b", r"\bfind\b",
    r"\binstall\b", r"\buse\b", r"\brecommend\b", r"\bdecide\b",
]
PROGRAM_WORDS = [
    r"\bnew\b.{0,50}\b(app|application|product|platform|module|system|agent)\b",
    r"\bfrom scratch\b", r"\bmajor transformation\b",
    r"\benterprise architecture\b", r"\boperating model transformation\b",
    r"\bmultiple modules\b",
]
MICRO_WORDS = [
    r"\btypo\b", r"\bcopy change\b", r"\bsmall change\b",
    r"\bisolated\b", r"\bone file\b", r"\bone component\b",
    r"\bminor\b", r"\bquick fix\b", r"\brename\b",
]
MATERIAL_RISK_WORDS = [
    r"\bschema\b", r"\bauth\b", r"\brbac\b", r"\bpermission\b",
    r"\bproduction\b", r"\bdependency\b", r"\bintegration\b",
    r"\bmigration\b", r"\bconfidential\b", r"\bpayment\b",
]
CONSULTING_WORDS = [
    r"\bconsult", r"\bbusiness\b", r"\bmanagement\b", r"\bgovernance\b",
    r"\brisk\b", r"\bcontrol\b", r"\bfinance\b", r"\baccount",
    r"\bprocess\b", r"\bworkflow\b", r"\boperating model\b",
    r"\brecommend", r"\bstakeholder\b", r"\bkpi\b", r"\bmis\b",
    r"\bindustry\b", r"\bstandard\b", r"\bmarket\b",
    r"\binvestment\b", r"\bportfolio\b", r"\bvaluation\b",
    r"\bxirr\b", r"\bunit economics\b", r"\bdue diligence\b",
    r"\bcontract\b", r"\blegal\b", r"\bcompliance\b",
    r"\bdata analysis\b", r"\banalytics\b",
]
ENGINEERING_WORDS = [
    r"\bcode\b", r"\barchitecture\b", r"\bapi\b", r"\bfrontend\b",
    r"\bbackend\b", r"\bdatabase\b", r"\bsecurity\b", r"\bdeploy",
    r"\btest\b", r"\bdebug\b", r"\brefactor\b", r"\bintegration\b",
    r"\bcomponent\b", r"\bui\b", r"\bux\b", r"\bdesign\b",
    r"\bbrand", r"\bdashboard\b", r"\bworkflow\b", r"\bproduct\b",
    r"\bplatform\b", r"\bmodule\b", r"\bagent\b",
]
ARTIFACT_WORDS = [
    r"\bemail\b", r"\breport\b", r"\bproposal\b", r"\bsop\b",
    r"\bpresentation\b", r"\bpowerpoint\b", r"\bppt\b",
    r"\bspreadsheet\b", r"\bexcel\b", r"\bword\b", r"\bdocx\b",
    r"\bpdf\b", r"\btracker\b",
]
RESEARCH_WORDS = [
    r"\bindustry standard", r"\bstandard\b", r"\bcurrent trend",
    r"\blatest\b", r"\bbenchmark\b", r"\bregulat", r"\bmarket practice",
    r"\bcompetitor\b", r"\bbest practice\b", r"\bresearch\b",
    r"\blast 30 days\b", r"\breddit\b", r"\byoutube\b", r"\bx\b",
]
BUILD_WORDS = [
    r"\bbuild\b", r"\bcreate\b", r"\bdesign\b", r"\bimplement\b",
    r"\bnew\b", r"\barchitecture\b", r"\bworkflow\b", r"\bplatform\b",
    r"\bmodule\b", r"\bagent\b",
]
PARALLEL_WORDS = [
    r"\bparallel\b", r"\bsubagent\b", r"\bagent team\b",
    r"\bmultiple workstreams\b", r"\bmultiple modules\b",
    r"\bdelegate\b",
]

DESIGN_WORDS = [
    r"\bdesign\b", r"\bui\b", r"\bux\b", r"\bfrontend\b",
    r"\bdashboard\b", r"\bbrand\b", r"\blayout\b",
    r"\btypography\b", r"\bcolour\b", r"\bcolor\b",
    r"\bresponsive\b", r"\baccessibility\b", r"\bcomponent\b",
]
MOTION_WORDS = [
    r"\banimat", r"\bmotion\b", r"\btransition\b", r"\beasing\b",
    r"\bgesture\b", r"\bgsap\b", r"\bscroll\b",
]
MINIMALISM_WORDS = [
    r"\bsimple\b", r"\bminimal\b", r"\byagni\b",
    r"\bover[- ]?engineer", r"\bbloat\b", r"\bboilerplate\b",
    r"\bsmallest\b", r"\bshortest\b",
]
WRITING_WORDS = [
    r"\bemail\b", r"\breport\b", r"\bproposal\b", r"\bcopy\b",
    r"\bwording\b", r"\bpolish\b", r"\brewrite\b",
    r"\bmicrocopy\b", r"\bslop\b",
]
BROWSER_WORDS = [
    r"\bbrowser\b", r"\bplaywright\b", r"\bcypress\b",
    r"\bstagehand\b", r"\be2e\b", r"\bend[- ]to[- ]end\b",
]
AGENT_BLUEPRINT_WORDS = [
    r"\bai agents?\b", r"\bagent blueprints?\b", r"\bdeploy agents?\b",
    r"\b500\+? agents?\b", r"\bmulti-agent\b",
]

RESOURCE_PHASES = {
    "karpathy-guidelines": {"DISCOVER", "PLAN", "IMPLEMENT", "VERIFY"},
    "ponytail": {"PLAN", "IMPLEMENT"},
    "superpowers": {"BRAINSTORM", "PLAN", "IMPLEMENT", "VERIFY", "RELEASE"},
    "github-spec-kit": {"DISCOVER", "SPECIFY", "PLAN"},
    "gsd-core": {"DISCOVER", "PLAN", "IMPLEMENT", "VERIFY", "RELEASE"},
    "task-observer": {"VERIFY", "RELEASE"},
    "claude-mem": {"ORIENT", "PLAN"},
    "graphify": {"ORIENT", "PLAN"},
    "context7": {"RESEARCH", "IMPLEMENT"},
    "last30days": {"RESEARCH"},
    "agent-reach": {"RESEARCH"},
    "500-ai-agents-projects": {"RESEARCH", "BRAINSTORM", "PLAN"},
    "ui-ux-pro-max": {"RESEARCH", "BRAINSTORM", "SPECIFY"},
    "taste-skill": {"BRAINSTORM", "IMPLEMENT"},
    "open-design": {"RESEARCH", "BRAINSTORM", "SPECIFY"},
    "impeccable": {"VERIFY", "POLISH"},
    "emil-kowalski-skill": {"SPECIFY", "IMPLEMENT", "VERIFY", "POLISH"},
    "frontend-design": {"IMPLEMENT"},
    "stop-slop": {"VERIFY", "POLISH"},
    "mobbin": {"RESEARCH"},
    "refero": {"RESEARCH"},
    "recent-designs": {"RESEARCH"},
    "penpot": {"RESEARCH", "BRAINSTORM", "SPECIFY"},
    "shadcn-ui": {"SPECIFY", "IMPLEMENT"},
    "21st-dev": {"RESEARCH", "SPECIFY", "IMPLEMENT"},
    "gsap": {"SPECIFY", "IMPLEMENT"},
    "headroom-js": {"IMPLEMENT"},
    "playwright": {"IMPLEMENT", "VERIFY"},
    "playwright-mcp": {"VERIFY"},
    "agent-browser": {"VERIFY"},
    "stagehand": {"IMPLEMENT", "VERIFY"},
    "cypress": {"IMPLEMENT", "VERIFY"},
    "puppeteer-mcp": {"VERIFY"},
    "everything-claude-code": {"BRAINSTORM", "PLAN", "IMPLEMENT", "VERIFY"},
    "ecc": {"BRAINSTORM", "PLAN", "IMPLEMENT", "VERIFY"},
    "voltagent-awesome-design-md": {"RESEARCH"},
    "500-ai-agents-projects": {"RESEARCH", "BRAINSTORM", "PLAN"},
    "strix": {"VERIFY"},
    "perplexity-bumblebee": {"RESEARCH", "VERIFY"},
    "perplexity-org": {"RESEARCH"},
    "perplexity-api-platform-developers": {"RESEARCH", "IMPLEMENT"},
    "perplexity-cli": {"RESEARCH"},
    "perplexity-modelcontextprotocol": {"RESEARCH", "IMPLEMENT"},
    "prime-intellect-prime-agent": {"PLAN", "IMPLEMENT"},
    "egonex-understand-anything": {"ORIENT", "DISCOVER", "RESEARCH", "VERIFY"},
    "evomap-evolver": {"VERIFY", "RELEASE"},
    "agency-agents": {"DISCOVER", "BRAINSTORM", "PLAN"},
    "nidhinjs-prompt-master": {"SPECIFY", "PLAN", "RELEASE"},
    "mattpocock-grilling": {"DISCOVER", "SPECIFY"},
    "cloudflare-os": {"RESEARCH", "SPECIFY"},
}


def find_root(start: Path | None = None) -> Path:
    starts = [start or Path.cwd(), Path(__file__).resolve().parent]
    for candidate_start in starts:
        for candidate in [candidate_start, *candidate_start.parents]:
            if (candidate / "AGENTS.md").exists() and (candidate / "catalog").exists():
                return candidate.resolve()
    return Path(__file__).resolve().parents[1]


ROOT = find_root()


def load_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain a JSON object")
    return value


def word_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8", errors="replace").split())


def matches(patterns: Iterable[str], text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def trigger_score(triggers: Iterable[str], text: str) -> tuple[int, list[str]]:
    """Match complete terms and phrases, never accidental substrings."""
    matched = []
    lowered = text.lower()
    for trigger in triggers:
        candidate = trigger.lower().strip()
        if not candidate:
            continue
        pattern = re.escape(candidate)
        pattern = pattern.replace(r"\ ", r"[\s_\-/]+")
        found = re.search(
            r"(?<![a-z0-9])" + pattern + r"(?![a-z0-9])",
            lowered,
            re.IGNORECASE,
        )
        if found:
            matched.append(trigger)
    return len(matched), matched


def simple_yaml(relative: str) -> dict[str, str]:
    path = ROOT / relative
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#") or raw.startswith((" ", "-")):
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def enumerated_scope_areas(prompt: str) -> int:
    """Count enumerated functional areas, without depending on vocabulary.

    The technical-noun list below only fires for prompts written in IT
    vocabulary. A product described in its own domain's language -- clinical
    (registration, encounters, consent, prescriptions), legal, logistics --
    scores near zero and under-classifies as MATERIAL, which silently drops
    POLISH and RELEASE from the phase plan and never triggers the PROGRAM
    module registry. Enumeration is the domain-neutral signal for "this
    describes several distinct areas of work".
    """
    listed = re.split(r",|\band\b", prompt, flags=re.IGNORECASE)
    return sum(1 for segment in listed if segment.strip())


def classify_tier(prompt: str) -> str:
    if not matches(MATERIAL_WORDS, prompt):
        return "INFO"
    if matches(PROGRAM_WORDS, prompt):
        return "PROGRAM"
    builds_a_product = bool(
        re.search(r"\b(build|create|design|implement)\b", prompt, re.IGNORECASE)
        and re.search(r"\b(platform|application|system|suite)\b", prompt, re.IGNORECASE)
    )
    technical_areas = len(re.findall(
        r"\b(workflow|dashboard|integration|rbac|audit|api|agent|automation|module|approval|document|reporting)\w*\b",
        prompt,
        re.IGNORECASE,
    ))
    if builds_a_product and (technical_areas >= 3 or enumerated_scope_areas(prompt) >= 4):
        return "PROGRAM"
    if matches(MICRO_WORDS, prompt) and not matches(MATERIAL_RISK_WORDS, prompt):
        return "MICRO"
    return "MATERIAL"


def classify_mode(tier: str) -> str:
    return {
        "INFO": "NONE",
        "MICRO": "EXECUTE",
        "MATERIAL": "DELTA",
        "PROGRAM": "FULL",
    }[tier]


def classify_register(prompt: str) -> str:
    artifact = matches(ARTIFACT_WORDS, prompt)
    consulting = matches(CONSULTING_WORDS, prompt)
    engineering = matches(ENGINEERING_WORDS, prompt)
    if artifact and not engineering:
        return "ARTIFACT"
    if consulting and engineering:
        return "DUAL"
    if consulting:
        return "CONSULTING"
    if engineering:
        return "ENGINEERING"
    return "ARTIFACT" if artifact else "ENGINEERING"


def active_profile() -> tuple[str, dict[str, Any]]:
    state = simple_yaml("PROJECT_STATE.yaml")
    profile_id = state.get("profile", "domain-expertise")
    path = ROOT / "profiles" / profile_id / "profile.json"
    if not path.exists():
        profile_id = "domain-expertise"
        path = ROOT / "profiles/domain-expertise/profile.json"
    return profile_id, json.loads(path.read_text(encoding="utf-8"))


def domain_context() -> dict[str, Any]:
    path = ROOT / "DOMAIN_CONTEXT.md"
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    incomplete = not text.strip() or "TBD" in text
    return {
        "path": "DOMAIN_CONTEXT.md",
        "incomplete": incomplete,
        "has_industry": "## Industry or Domain" in text and "## Industry or Domain\n\nTBD" not in text,
        "has_standards": (
            "## Applicable Laws, Regulations and Standards" in text
            and "## Applicable Laws, Regulations and Standards\n\n- TBD" not in text
        ),
        "has_trends": (
            "## Current Industry Practices and Trends" in text
            and "## Current Industry Practices and Trends\n\n- TBD" not in text
        ),
    }


def decision_questions(prompt: str, tier: str, register: str) -> list[dict[str, str]]:
    if tier in {"INFO", "MICRO"}:
        return []

    questions: list[dict[str, str]] = []
    lower = prompt.lower()

    if not re.search(r"\b(user|customer|employee|management|admin|operator|developer|candidate|client)s?\b", lower):
        questions.append({
            "id": "users",
            "question": "Who are the primary users and who makes the final decision?",
            "why": "User roles change workflows, permissions, information density and acceptance.",
            "recommended_default": "Identify one primary user, one management decision-maker and any approver.",
            "consequence": "Without this, the solution may optimise the wrong experience or authority model.",
        })

    if not re.search(r"\b(success|outcome|acceptance|target|metric|kpi|goal)\b", lower):
        questions.append({
            "id": "success",
            "question": "What measurable outcome would make this successful?",
            "why": "The outcome determines prioritisation and verification.",
            "recommended_default": "Define one operational outcome, one quality measure and one adoption or management measure.",
            "consequence": "Without measurable success, completion becomes subjective.",
        })

    context = domain_context()
    if context["incomplete"] and register in {"CONSULTING", "DUAL"}:
        questions.append({
            "id": "domain",
            "question": "Which industry, geography and regulatory context should govern the solution?",
            "why": "Standards, workflows, controls and terminology vary materially by domain and jurisdiction.",
            "recommended_default": "Use the organisation's primary operating industry and legal jurisdiction.",
            "consequence": "A generic design may conflict with local practice or mandatory requirements.",
        })

    if (
        re.search(r"\b(PHI|PII|patient|health record|medical record|consent|GDPR|HIPAA|DPDP|biometric|financial account|passport|personal data)\b", prompt, re.IGNORECASE)
        # Guard on the answer being specified, not on "withdrawal"/"consent" merely
        # being named as a feature to build -- those words describe the feature
        # this question exists to ask about, not an answer to it.
        and not re.search(r"\b(retention polic\w*|retain existing|erasure polic\w*|anonymi[sz]e)\b", lower)
    ):
        questions.append({
            "id": "data_handling",
            "question": "When a data subject withdraws consent or requests deletion, what must happen to records already created, and how long must they be retained regardless?",
            "why": "Regulated personal data (health, financial, biometric or PII) carries consent, retention and erasure obligations that shape the schema and audit design before code is written.",
            "recommended_default": "Block further use of consent-linked data, retain existing records to satisfy statutory retention, and log the consent-state change itself as an auditable event.",
            "consequence": "Deciding this after implementation risks unlawful retention of data that should be blocked, or unlawful deletion of records a regulator requires kept.",
        })

    if matches(BUILD_WORDS, prompt) and not re.search(r"\b(existing|current|legacy|stack|system|repository|integration|constraint)\b", lower):
        questions.append({
            "id": "constraints",
            "question": "What existing systems, data, integrations or delivery constraints must be preserved?",
            "why": "Constraints determine architecture, migration, cost and implementation sequence.",
            "recommended_default": "Preserve current systems of record and introduce the smallest reversible change.",
            "consequence": "Ignoring constraints can produce an attractive but unusable target state.",
        })

    if re.search(r"\b(workflow|approval|finance|payment|risk|security|compliance|data)\b", lower):
        questions.append({
            "id": "authority",
            "question": "Which decisions, thresholds or actions require human approval or segregation of duties?",
            "why": "Authority and control rules must be designed before automation.",
            "recommended_default": "Use maker-checker for material actions and explicit approval for irreversible or sensitive changes.",
            "consequence": "Automation may otherwise bypass accountability or create unacceptable risk.",
        })

    return questions[:5]


def infer_decision(prompt: str, tier: str, register: str) -> str:
    if tier == "INFO":
        return "Provide the requested information."
    if tier == "MICRO":
        return "Complete the bounded change without widening scope."
    if register == "ARTIFACT":
        return "Determine the artifact structure, evidence and formatting needed for the audience's decision."
    if register == "CONSULTING":
        return "Determine the business recommendation, operating implications and implementation path."
    if register == "DUAL":
        return "Select a solution that is both domain-correct and technically credible."
    return "Select the smallest technically sound implementation that satisfies the approved outcome."


def improved_prompt(prompt: str, tier: str, register: str, questions: list[dict[str, str]]) -> str:
    unresolved = "; ".join(item["question"] for item in questions) or "No material discovery questions remain."
    return (
        f"Work on this as a {tier} task in the {register} register. "
        f"Original request: {prompt.strip()} "
        "First inspect the repository and DOMAIN_CONTEXT.md. "
        f"Resolve or use recommended defaults for: {unresolved} "
        "Use authoritative domain standards and current evidence when they can change the decision. "
        "Explore materially different approaches before planning. "
        "Create a phase-based plan, use independent subagents only for non-conflicting tasks, "
        "implement with deterministic checks, and persist the final decisions and evidence."
    )


def research_plan(prompt: str, tier: str) -> dict[str, Any]:
    context = domain_context()
    explicit = matches(RESEARCH_WORDS, prompt)
    needed = tier in {"MATERIAL", "PROGRAM"} and (context["incomplete"] or explicit)
    sources = ["primary-web"]
    reasons = []

    if context["incomplete"]:
        reasons.append("DOMAIN_CONTEXT.md is incomplete")
    if explicit:
        reasons.append("the request depends on standards, benchmarks or current practice")

    if re.search(r"\b(last 30 days|current trend|latest|recent|emerging|community|sentiment)\b", prompt, re.IGNORECASE):
        sources.append("last30days")
    if re.search(r"\b(reddit|youtube|twitter|x\b|social|platform|community|user feedback|reviews)\b", prompt, re.IGNORECASE):
        sources.append("agent-reach")
    if re.search(r"\b(library|framework|sdk|api documentation|technical docs)\b", prompt, re.IGNORECASE):
        sources.append("context7")
    if re.search(r"\b(ai agent|agent project|agent blueprint|deploy agent|500 agents)\b", prompt, re.IGNORECASE):
        sources.append("500-ai-agents")

    queries = []
    if needed:
        queries = [
            "official standards, regulations or recognised professional guidance relevant to the decision",
            "current industry operating practices and comparable implementations",
            "recent technology or market shifts that may change the recommended approach",
        ]
    return {
        "needed": needed,
        "reasons": reasons,
        "sources": list(dict.fromkeys(sources)),
        "queries": queries,
        "authoritative_first": True,
    }


def initial_phase(prompt: str, tier: str, questions: list[dict[str, str]], research: dict[str, Any]) -> str:
    if tier == "INFO":
        return "INFO"
    if tier == "MICRO":
        return "IMPLEMENT"
    if questions:
        return "DISCOVER"
    if research["needed"]:
        return "RESEARCH"
    if matches(BUILD_WORDS, prompt):
        return "BRAINSTORM"
    return "PLAN"



def relevant_strategy_adapters(
    prompt: str,
    phase: str,
    tier: str,
    register: str,
    research: dict[str, Any],
) -> list[str]:
    """Select external methodology adapters only when their strength is relevant."""
    selected: list[str] = []
    design = matches(DESIGN_WORDS, prompt)
    engineering = register in {"ENGINEERING", "DUAL"}
    browser = matches(BROWSER_WORDS, prompt) or design
    agent_blueprint = matches(AGENT_BLUEPRINT_WORDS, prompt)
    spec_heavy = tier == "PROGRAM" or bool(
        re.search(
            r"\b(specification|requirements|PRD|BRD|FRS|constitution|acceptance criteria)\b",
            prompt,
            re.IGNORECASE,
        )
    )

    if phase in {"BRAINSTORM", "PLAN", "IMPLEMENT", "VERIFY", "RELEASE"}:
        selected.append("superpowers-sdlc")
    if spec_heavy and phase in {"DISCOVER", "SPECIFY", "PLAN"}:
        selected.append("github-spec-kit")
    if tier == "PROGRAM" and phase in {"DISCOVER", "PLAN", "IMPLEMENT", "VERIFY", "RELEASE"}:
        selected.append("gsd-core")
    if engineering and phase in {"DISCOVER", "PLAN", "IMPLEMENT", "VERIFY"}:
        selected.append("engineering-behaviour")
    if design and phase in {"RESEARCH", "BRAINSTORM", "SPECIFY", "IMPLEMENT", "VERIFY", "POLISH"}:
        selected.append("design-strength-orchestration")
    if browser and phase in {"IMPLEMENT", "VERIFY"}:
        selected.append("browser-verification")
    if phase == "RESEARCH" and "agent-reach" in research.get("sources", []):
        selected.append("agent-reach")
    if phase == "RESEARCH" and "last30days" in research.get("sources", []):
        selected.append("last30days")
    if agent_blueprint and phase in {"RESEARCH", "BRAINSTORM", "PLAN"}:
        selected.append("500-ai-agents")

    return list(dict.fromkeys(selected))

def phase_plan(
    prompt: str,
    tier: str,
    register: str,
    research: dict[str, Any],
    parallel: dict[str, Any],
) -> list[dict[str, Any]]:
    if tier == "INFO":
        return []
    if tier == "MICRO":
        phases = ["IMPLEMENT", "VERIFY"]
    elif tier == "PROGRAM":
        phases = [
            "ORIENT", "DISCOVER", "RESEARCH", "BRAINSTORM",
            "SPECIFY", "PLAN", "IMPLEMENT", "VERIFY", "POLISH", "RELEASE",
        ]
    else:
        phases = ["ORIENT", "DISCOVER"]
        if research["needed"]:
            phases.append("RESEARCH")
        if matches(BUILD_WORDS, prompt):
            phases.append("BRAINSTORM")
        if matches(BUILD_WORDS, prompt):
            phases.append("SPECIFY")
        phases.extend(["PLAN", "IMPLEMENT", "VERIFY"])
        if matches(DESIGN_WORDS, prompt) or matches(WRITING_WORDS, prompt):
            phases.append("POLISH")
        if re.search(r"\b(release|production|go-live|launch)\b", prompt, re.IGNORECASE):
            phases.append("RELEASE")

    definitions = {
        item["id"]: item
        for item in load_json("catalog/phase-capabilities.json")["phases"]
    }
    result = []
    for phase_id in phases:
        definition = definitions[phase_id]
        result.append({
            "id": phase_id,
            "purpose": definition["purpose"],
            "native_skills": definition.get("native_skills", []),
            "doctrine_packs": definition.get("doctrine_packs", []),
            "external_candidates": relevant_strategy_adapters(
                prompt, phase_id, tier, register, research
            ),
            "outputs": definition.get("outputs", []),
            "capability_strengths": [
                item["id"] for item in select_phase_strengths(
                    prompt, phase_id, tier, register, research, parallel
                )
            ],
        })
    return result


def parallel_assessment(prompt: str, tier: str) -> dict[str, Any]:
    requested = matches(PARALLEL_WORDS, prompt)
    potentially_useful = tier == "PROGRAM" or requested
    return {
        "requested": requested,
        "potentially_useful": potentially_useful,
        "decision": "evaluate-after-plan" if potentially_useful else "not-indicated",
        "requirements": [
            "independent tasks",
            "separate files or non-conflicting state",
            "explicit input and output contracts",
            "named integration owner",
            "whole-system verification after merge",
        ],
        "preferred_adapters": [
            "superpowers:subagent-driven-development",
            "superpowers:dispatching-parallel-agents",
        ] if potentially_useful else [],
    }



def installed_skill_names() -> set[str]:
    """Return repo-local native or external skill folder names."""
    names: set[str] = set()
    for base in (ROOT / "skills", ROOT / ".agents/skills", ROOT / ".claude/skills"):
        if not base.exists():
            continue
        for skill_file in base.glob("*/SKILL.md"):
            names.add(skill_file.parent.name)
    return names


def _strength_index() -> dict[str, dict[str, Any]]:
    return {
        item["id"]: item
        for item in load_json("catalog/skill-strengths.json")["capabilities"]
    }


def select_phase_strengths(
    prompt: str,
    phase: str,
    tier: str,
    register: str,
    research: dict[str, Any],
    parallel: dict[str, Any],
) -> list[dict[str, Any]]:
    """Select distinct capability strengths for the current phase."""
    index = _strength_index()
    selected: list[tuple[str, str, int]] = []

    def add(capability_id: str, reason: str, priority: int) -> None:
        if capability_id in index and all(item[0] != capability_id for item in selected):
            selected.append((capability_id, reason, priority))

    engineering = register in {"ENGINEERING", "DUAL"} or phase in {"PLAN", "IMPLEMENT", "VERIFY", "RELEASE"}
    design = matches(DESIGN_WORDS, prompt)
    motion = matches(MOTION_WORDS, prompt)
    writing = register == "ARTIFACT" or matches(WRITING_WORDS, prompt)
    browser = matches(BROWSER_WORDS, prompt) or design
    minimalism = matches(MINIMALISM_WORDS, prompt) or tier == "MICRO"

    if engineering:
        if phase in {"ORIENT", "DISCOVER"}:
            add("karpathy:think-before-coding", "baseline engineering judgement", 130)
        if phase == "PLAN":
            add("karpathy:simplicity-first", "avoid speculative architecture", 130)
            add("karpathy:goal-driven-execution", "define verifiable tasks", 125)
            add("superpowers:writing-plans", "phase-specialist planning", 120)
            if minimalism:
                add("ponytail:lite", "minimalism pressure requested or useful", 90)
        if phase == "IMPLEMENT":
            add("karpathy:surgical-changes", "keep implementation scoped", 130)
            add("karpathy:goal-driven-execution", "implement against checks", 125)
            add("superpowers:test-driven-development", "test-first implementation", 120)
            if parallel["requested"]:
                add("superpowers:dispatching-parallel-agents", "independent parallel work requested", 115)
            elif tier == "PROGRAM":
                add("superpowers:subagent-driven-development", "fresh task contexts for programme work", 110)
            if minimalism:
                add("ponytail:full", "reduce code and dependency bloat", 95)
        if phase == "VERIFY":
            add("superpowers:verification-before-completion", "evidence before completion", 130)
            add("superpowers:requesting-code-review", "independent review", 115)
        if phase == "RELEASE":
            add("superpowers:finishing-a-development-branch", "clean branch completion", 110)

    if phase == "BRAINSTORM":
        add("superpowers:brainstorming", "structured alternatives before planning", 130)

    if design:
        add("design-intelligence:constitution", "mandatory design authority", 200)
        if phase == "RESEARCH":
            add("ui-ux-pro-max:style-search", "search product-type design guidance", 125)
            if "dashboard" in prompt.lower() or "chart" in prompt.lower():
                add("ui-ux-pro-max:chart-and-data-viz", "data-visualisation guidance", 115)
        elif phase == "BRAINSTORM":
            add("taste:design-taste-frontend", "greenfield art direction and anti-slop dials", 120)
        elif phase == "SPECIFY":
            add("ui-ux-pro-max:design-system-generator", "design-system recommendation", 120)
            if motion:
                add("emil:animation-vocabulary", "precise motion specification", 100)
        elif phase == "IMPLEMENT":
            add("frontend-design:implementation", "approved frontend implementation", 120)
            if motion:
                add("emil:emil-design-eng", "purposeful motion implementation", 105)
        elif phase == "VERIFY":
            add("impeccable:audit", "deterministic design audit", 125)
            add("impeccable:harden", "edge-state and resilience review", 110)
            if motion:
                add("emil:review-animations", "strict motion review", 115)
            if browser:
                add("playwright:project-tests", "deterministic browser evidence", 105)
        elif phase == "POLISH":
            add("impeccable:polish", "final visual refinement", 125)
            add("impeccable:clarify", "final UX-writing refinement", 100)
            if motion:
                add("emil:improve-animations", "prioritised motion fixes", 105)

    if phase == "RESEARCH":
        for source in research.get("sources", []):
            mapping = {
                "context7": "context7:library-docs",
                "last30days": "last30days:recent-discourse",
                "agent-reach": "agent-reach:platform-research",
                "500-ai-agents": "500-ai-agents:blueprint-discovery",
            }
            if source in mapping:
                add(mapping[source], f"research source selected: {source}", 110)
        if matches(AGENT_BLUEPRINT_WORDS, prompt):
            add("500-ai-agents:blueprint-discovery", "agent blueprint discovery requested", 115)

    if writing and phase in {"VERIFY", "POLISH"}:
        add("stop-slop:final-lint", "final anti-generic-AI prose pass", 90)

    if phase == "VERIFY" and matches(BROWSER_WORDS, prompt):
        add("playwright:project-tests", "browser verification requested", 120)

    selected.sort(key=lambda item: (-item[2], item[0]))
    installed = installed_skill_names()
    result = []
    for capability_id, reason, priority in selected[:8]:
        item = index[capability_id]
        parent = item.get("parent")
        status = "internal"
        if parent and parent not in {"design-intelligence-constitution"}:
            candidate_names = {
                parent,
                capability_id.split(":", 1)[-1],
                capability_id.replace(":", "-"),
            }
            status = "installed" if installed.intersection(candidate_names) else "catalogued"
        result.append({
            **item,
            "reason": reason,
            "priority": priority,
            "status": status,
        })
    return result


def capability_readiness(
    native_skills: list[dict[str, Any]],
    strengths: list[dict[str, Any]],
) -> dict[str, Any]:
    installed = installed_skill_names()
    active_native = [item["id"] for item in native_skills]
    active_strengths = [item["id"] for item in strengths]
    missing_parents = []
    for item in strengths:
        parent = item.get("parent")
        if not parent or item["status"] in {"internal", "installed"}:
            continue
        if parent not in missing_parents:
            missing_parents.append(parent)
    return {
        "active_native_skills": active_native,
        "active_capability_strengths": active_strengths,
        "detected_skill_folders": sorted(installed),
        "external_install_or_load_candidates": missing_parents,
        "rule": "Candidates remain inactive until overlap, licence, security and approval review.",
    }

def eligible(item: dict[str, Any], tier: str, register: str, phase: str) -> bool:
    tiers = item.get("tiers", [])
    registers = item.get("registers", [])
    phases = item.get("phases", [])
    return (
        (not tiers or tier in tiers)
        and (not registers or register in registers)
        and (not phases or phase in phases)
    )


def select_doctrine(
    prompt: str,
    tier: str,
    register: str,
    phase: str,
    limit: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items = load_json("catalog/doctrine-packs.json")["packs"]
    ranked = []
    for item in items:
        if not eligible(item, tier, register, phase):
            continue
        score, matched = trigger_score(item.get("triggers", []), prompt)
        if score:
            ranked.append({**item, "score": score, "matched": matched})

    phase_defaults = {
        "DISCOVER": ["decision-intelligence", "domain-expertise"],
        "RESEARCH": ["domain-expertise"],
        "BRAINSTORM": ["decision-intelligence", "orchestration-strategy"],
        "PLAN": ["orchestration-strategy"],
        "IMPLEMENT": ["product-engineering"],
        "VERIFY": ["product-engineering"],
    }
    by_id = {item["id"]: item for item in items}
    for pack_id in phase_defaults.get(phase, []):
        if pack_id in by_id and all(item["id"] != pack_id for item in ranked):
            item = by_id[pack_id]
            if eligible(item, tier, register, phase):
                ranked.append({**item, "score": 0, "matched": ["phase-default"]})

    ranked.sort(key=lambda item: (-item["score"], -item.get("priority", 0), item["id"]))
    # Label the rejection like select_skills() does. Returning a bare tail slice
    # left rejected_because unset, so harness_observability.py -- which skips
    # falsy reasons -- silently dropped every budget-rejected pack from its
    # trend, the one report meant to surface exactly that.
    rejected = [
        {**item, "rejected_because": "phase-pack-budget"} for item in ranked[limit:]
    ]
    return ranked[:limit], rejected


def select_skills(
    prompt: str,
    tier: str,
    register: str,
    phase: str,
    limit: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items = load_json("catalog/native-skills.json")["skills"]
    by_id_all = {item["id"]: item for item in items}
    ranked = []
    for item in items:
        if not eligible(item, tier, register, phase):
            continue
        score, matched = trigger_score(item.get("triggers", []), prompt)
        if score:
            ranked.append({**item, "score": score, "matched": matched})

    # design-system and enterprise-ui-review/frontend-implementation declare
    # each other in "paired_with", but that field is documentation only --
    # nothing enforced it. A prompt using generic UI vocabulary ("frontend",
    # "React", "page", "component") without any design-specific word ("design",
    # "brand", "colour") triggered UI implementation skills with no design
    # decision ever surfaced to the user. design_system is only eligible at
    # BRAINSTORM/SPECIFY (before implementation exists to review), so the fix
    # has to run there, checking the same prompt UI-implementation skills will
    # later match on, not design_system's own (deliberately narrower) triggers.
    if phase in ("BRAINSTORM", "SPECIFY") and not any(item["id"] == "design-system" for item in ranked):
        ui_impl_triggers = set()
        for ui_skill_id in ("enterprise-ui-review", "frontend-implementation"):
            ui_skill = by_id_all.get(ui_skill_id)
            if ui_skill:
                ui_impl_triggers.update(ui_skill.get("triggers", []))
        _, ui_matched = trigger_score(sorted(ui_impl_triggers), prompt)
        if ui_matched:
            design_system_item = by_id_all.get("design-system")
            if design_system_item and eligible(design_system_item, tier, register, phase):
                ranked.append({
                    **design_system_item,
                    "score": 1,
                    "priority": 999,  # must survive the skill-budget cut, not merely compete for it
                    "matched": ["ui-implementation-requires-design-system"],
                })

    phase_defaults = {
        "DISCOVER": ["decision-coach", "project-discovery", "lifecycle-planning"],
        "RESEARCH": ["domain-research", "reference-router"],
        "BRAINSTORM": ["solution-brainstorming"],
        "SPECIFY": (
            ["artifact-production"]
            if register == "ARTIFACT"
            else ["product-specification"]
        ),
        "PLAN": ["delivery-planning"],
        "IMPLEMENT": (
            ["artifact-production"]
            if register == "ARTIFACT"
            else ["software-implementation"]
            if register in {"ENGINEERING", "DUAL"}
            else []
        ),
        "VERIFY": (
            ["artifact-production", "writing-quality"]
            if register == "ARTIFACT"
            else ["quality-engineering"]
            if register in {"ENGINEERING", "DUAL"}
            else []
        ),
        "POLISH": (
            ["artifact-production", "writing-quality"]
            if register == "ARTIFACT"
            else ["enterprise-ui-review"]
            if matches(DESIGN_WORDS, prompt)
            else []
        ),
        "RELEASE": ["release-readiness"],
    }
    by_id = {item["id"]: item for item in items}
    for skill_id in phase_defaults.get(phase, []):
        if skill_id in by_id and all(item["id"] != skill_id for item in ranked):
            item = by_id[skill_id]
            if eligible(item, tier, register, phase):
                ranked.append({**item, "score": 0, "matched": ["phase-default"]})

    ranked.sort(key=lambda item: (-item["score"], -item.get("priority", 0), item["id"]))
    selected, rejected, used_groups = [], [], set()
    for item in ranked:
        group = item.get("overlap_group")
        if group and group in used_groups:
            rejected.append({**item, "rejected_because": f"overlap:{group}"})
            continue
        if len(selected) >= limit:
            rejected.append({**item, "rejected_because": "phase-skill-budget"})
            continue
        selected.append(item)
        if group:
            used_groups.add(group)
    return selected, rejected


def select_external(prompt: str, phase: str, research: dict[str, Any], maximum: int = 6) -> list[dict[str, Any]]:
    registry = load_json("catalog/capability-registry.json")
    ranked = []
    tier = classify_tier(prompt)
    register = classify_register(prompt)
    phase_adapter_ids = set(
        relevant_strategy_adapters(prompt, phase, tier, register, research)
    )

    source_aliases = {
        "last30days": "last30days",
        "agent-reach": "agent-reach",
        "context7": "context7",
        "500-ai-agents": "500-ai-agents-projects",
    }
    desired = {source_aliases.get(item, item) for item in research.get("sources", [])}
    desired.update(phase_adapter_ids)

    for item in registry.get("resources", []):
        allowed_phases = RESOURCE_PHASES.get(item["id"])
        if allowed_phases and phase not in allowed_phases:
            continue
        score, matched = trigger_score(item.get("triggers", []), prompt)
        if item["id"] in desired:
            score += 3
            matched = list(matched) + ["phase-or-research-strategy"]
        if score:
            ranked.append({
                "id": item["id"],
                "name": item["name"],
                "source": item.get("source"),
                "status": item.get("status"),
                "activation": item.get("activation"),
                "overlap_group": item.get("overlap_group"),
                "score": score,
                "matched": matched,
            })

    # Strategy adapters may use different IDs from external registry entries.
    adapters = load_json("catalog/strategy-adapters.json")["adapters"]
    existing = {item["id"] for item in ranked}
    for adapter in adapters:
        if adapter["id"] in phase_adapter_ids and adapter["id"] not in existing:
            ranked.append({
                "id": adapter["id"],
                "name": adapter["name"],
                "source": adapter["source"],
                "status": adapter["status"],
                "activation": "phase-adapter-candidate",
                "overlap_group": adapter.get("overlap_group"),
                "score": 3,
                "matched": ["phase-strategy"],
            })

    ranked.sort(key=lambda item: (-item["score"], item["id"]))

    # Native skills already reject a second member of the same overlap group;
    # external candidates did not, so two competing tools could surface at
    # once. Membership comes from the formal group's members list rather than
    # the resource's own overlap_group tag -- the two use different keys
    # (graphify is tagged code-knowledge but governed by memory-and-knowledge).
    # Only SUBSTITUTE groups collapse; COMPLEMENTARY groups such as
    # research-freshness are designed to stack.
    substitute_group_of = {
        member: group["id"]
        for group in load_json("catalog/overlap-groups.json")["groups"]
        if group.get("relation") == "SUBSTITUTE"
        for member in group.get("members", [])
    }
    selected, used_groups = [], set()
    for item in ranked:
        group = substitute_group_of.get(item["id"])
        if group and group in used_groups:
            continue
        selected.append(item)
        if group:
            used_groups.add(group)
        if len(selected) >= maximum:
            break
    return selected


def estimate_cost(
    profile_id: str,
    packs: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    decision_brief_words: int,
) -> dict[str, Any]:
    """Separate automatic pack cost from skill invocation cost.

    The context pack contains skill pointers, not complete SKILL.md bodies.
    Native clients load selected skills only when invoked.
    """
    kernel = word_count(ROOT / "AGENTS.md")
    active_context = 220
    profile = word_count(ROOT / "profiles" / profile_id / "PROFILE.md")
    pack_costs = {item["id"]: word_count(ROOT / item["path"]) for item in packs}
    skill_file_costs = {
        item["id"]: word_count(ROOT / "skills" / item["id"] / "SKILL.md")
        for item in skills
    }
    skill_pointer_costs = {item["id"]: 18 for item in skills}
    automatic_total = (
        kernel
        + active_context
        + profile
        + decision_brief_words
        + sum(pack_costs.values())
        + sum(skill_pointer_costs.values())
    )
    invoked_skill_total = sum(skill_file_costs.values())
    return {
        "kernel": kernel,
        "active_context_estimate": active_context,
        "profile": profile,
        "decision_brief": decision_brief_words,
        "packs": pack_costs,
        "skill_pointers": skill_pointer_costs,
        "skills": skill_file_costs,
        "automatic_total": automatic_total,
        "invoked_skill_total": invoked_skill_total,
        "combined_total": automatic_total + invoked_skill_total,
        "total": automatic_total,
    }


def enforce_context_budget(
    profile: dict[str, Any],
    packs: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    profile_id: str,
    decision_brief_words: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    automatic_budget = int(profile.get("context_budget_words", 1800))
    skill_budget = int(profile.get("skill_context_budget_words", 1000))
    pruned = []

    while True:
        cost = estimate_cost(profile_id, packs, skills, decision_brief_words)

        if cost["invoked_skill_total"] > skill_budget and len(skills) > 1:
            removed = skills.pop()
            pruned.append({
                **removed,
                "rejected_because": "invoked-skill-context-budget",
            })
            continue

        if cost["automatic_total"] > automatic_budget and len(packs) > 1:
            removed = packs.pop()
            pruned.append({
                **removed,
                "rejected_because": "automatic-context-budget",
            })
            continue

        if cost["automatic_total"] > automatic_budget and len(skills) > 1:
            removed = skills.pop()
            pruned.append({
                **removed,
                "rejected_because": "automatic-context-budget",
            })
            continue

        return packs, skills, pruned, {
            **cost,
            "budget": automatic_budget,
            "automatic_budget": automatic_budget,
            "skill_budget": skill_budget,
            "over_budget": (
                cost["automatic_total"] > automatic_budget
                or cost["invoked_skill_total"] > skill_budget
            ),
        }


def route_prompt(prompt: str, phase_override: str | None = None) -> dict[str, Any]:
    tier = classify_tier(prompt)
    mode = classify_mode(tier)
    register = classify_register(prompt)
    profile_id, profile = active_profile()
    questions = decision_questions(prompt, tier, register)
    research = research_plan(prompt, tier)
    phase = phase_override or initial_phase(prompt, tier, questions, research)
    parallel = parallel_assessment(prompt, tier)
    phases = phase_plan(prompt, tier, register, research, parallel)

    brief = {
        "actual_decision": infer_decision(prompt, tier, register),
        "known_request": prompt.strip(),
        "questions": questions,
        "recommended_action": (
            "Answer the material questions or accept the recommended defaults, "
            "then continue through the phase plan."
            if questions else
            "Proceed to the current phase using the approved request and project evidence."
        ),
        "improved_prompt": improved_prompt(prompt, tier, register, questions),
    }
    brief_words = min(280, len(json.dumps(brief, ensure_ascii=False).split()))

    pack_limits = {"INFO": 0, "MICRO": 1, "MATERIAL": 3, "PROGRAM": 4}
    skill_limits = {"INFO": 0, "MICRO": 1, "MATERIAL": 5, "PROGRAM": 6}
    profile_pack_limit = int(
        profile.get("maximum_doctrine_packs_per_phase", pack_limits[tier])
    )
    profile_skill_limit = int(
        profile.get("maximum_native_skills_per_phase", skill_limits[tier])
    )
    pack_limit = min(pack_limits[tier], profile_pack_limit)
    skill_limit = min(skill_limits[tier], profile_skill_limit)

    packs, rejected_packs = select_doctrine(
        prompt, tier, register, phase, pack_limit
    )
    skills, rejected_skills = select_skills(
        prompt, tier, register, phase, skill_limit
    )
    packs, skills, budget_pruned, cost = enforce_context_budget(
        profile, list(packs), list(skills), profile_id, brief_words
    )
    phase_strengths = select_phase_strengths(
        prompt, phase, tier, register, research, parallel
    )
    readiness = capability_readiness(skills, phase_strengths)

    return {
        "schema_version": "3.0",
        "runtime_version": VERSION,
        "tier": tier,
        "mode": mode,
        "register": register,
        "material": tier != "INFO",
        "profile": profile_id,
        "current_phase": phase,
        "decision_brief": brief,
        "research_plan": research,
        "phase_plan": phases,
        "parallel_assessment": parallel,
        "doctrine_packs": packs,
        "native_skills": skills,
        "capability_strengths": phase_strengths,
        "capability_readiness": readiness,
        "external_candidates": select_external(prompt, phase, research),
        "rejected": rejected_packs + rejected_skills + budget_pruned,
        "context_cost": cost,
        "closure": {
            "required": tier != "INFO",
            "structured_checks_required": tier in {"MATERIAL", "PROGRAM"},
            "compact": tier == "MICRO",
        },
    }


def build_context_pack(prompt: str, route: dict[str, Any]) -> str:
    brief = route["decision_brief"]
    sections = [
        "# Active Context Pack",
        "",
        f"- Tier: `{route['tier']}`",
        f"- Mode: `{route['mode']}`",
        f"- Register: `{route['register']}`",
        f"- Profile: `{route['profile']}`",
        f"- Current phase: `{route['current_phase']}`",
        f"- Context estimate: `{route['context_cost']['total']} / {route['context_cost']['budget']} words`",
        "",
        "## Decision Brief",
        "",
        f"- Actual decision: {brief['actual_decision']}",
        f"- Request: {brief['known_request']}",
        f"- Recommended action: {brief['recommended_action']}",
        "",
    ]

    if brief["questions"]:
        sections.extend(["## Material Questions", ""])
        for index, item in enumerate(brief["questions"], 1):
            sections.extend([
                f"### {index}. {item['question']}",
                f"- Why: {item['why']}",
                f"- Recommended default: {item['recommended_default']}",
                f"- Consequence: {item['consequence']}",
                "",
            ])

    sections.extend([
        "## Improved Execution Prompt",
        "",
        brief["improved_prompt"],
        "",
        "## Research",
        "",
        f"- Needed: `{route['research_plan']['needed']}`",
        f"- Sources: {', '.join(route['research_plan']['sources'])}",
    ])
    for reason in route["research_plan"]["reasons"]:
        sections.append(f"- Reason: {reason}")

    profile_path = ROOT / "profiles" / route["profile"] / "PROFILE.md"
    if profile_path.exists():
        sections.extend([
            "",
            f"## Active Profile: {route['profile']}",
            "",
            profile_path.read_text(encoding="utf-8").strip(),
        ])

    sections.extend(["", "## Doctrine Loaded", ""])
    if not route["doctrine_packs"]:
        sections.append("Kernel only.")
    for pack in route["doctrine_packs"]:
        sections.extend([
            f"### {pack['id']}",
            "",
            (ROOT / pack["path"]).read_text(encoding="utf-8").strip(),
        ])

    sections.extend(["", "## Native Skills for Current Phase", ""])
    if not route["native_skills"]:
        sections.append("No native skill selected.")
    for skill in route["native_skills"]:
        sections.extend([
            f"- `{skill['id']}` — matched: {', '.join(skill.get('matched', []))}",
            f"  - Codex: `${skill['id']}`",
            f"  - Claude: `/{skill['id']}`",
            f"  - File: `skills/{skill['id']}/SKILL.md`",
        ])

    sections.extend(["", "## Capability Strengths for Current Phase", ""])
    if not route["capability_strengths"]:
        sections.append("No additional specialist capability selected.")
    for item in route["capability_strengths"]:
        sections.append(
            f"- `{item['id']}` — {item['strength']} "
            f"| status: `{item['status']}` | reason: {item['reason']}"
        )

    readiness = route["capability_readiness"]
    sections.extend(["", "## Skill and Readiness Audit", ""])
    sections.append(
        f"- Active native skills: {', '.join(readiness['active_native_skills']) or 'none'}"
    )
    sections.append(
        f"- Active capability strengths: {', '.join(readiness['active_capability_strengths']) or 'none'}"
    )
    sections.append(
        "- External install/load candidates: "
        + (", ".join(readiness["external_install_or_load_candidates"]) or "none")
    )
    sections.append(f"- Rule: {readiness['rule']}")

    sections.extend(["", "## Lifecycle Plan", ""])
    for phase in route["phase_plan"]:
        sections.append(
            f"- `{phase['id']}` — {phase['purpose']} "
            f"| skills: {', '.join(phase.get('native_skills', [])) or 'task-routed'} "
            f"| strengths: {', '.join(phase.get('capability_strengths', [])) or 'none'} "
            f"| external: {', '.join(phase.get('external_candidates', [])) or 'none'}"
        )

    sections.extend(["", "## External Candidates", ""])
    if not route["external_candidates"]:
        sections.append("None active.")
    for item in route["external_candidates"]:
        sections.append(
            f"- `{item['id']}` — {item['name']} — {item['activation']} — "
            f"{item.get('source') or 'source unresolved'}"
        )
    sections.append(
        "Candidates are not active until overlap, licence, security, installation "
        "and approval requirements are satisfied."
    )

    sections.extend([
        "",
        "## Parallel and Subagent Use",
        "",
        f"- Decision: `{route['parallel_assessment']['decision']}`",
    ])
    for requirement in route["parallel_assessment"]["requirements"]:
        sections.append(f"- Requirement: {requirement}")

    sections.extend([
        "",
        "## Closure",
        "",
        f"- Required: `{route['closure']['required']}`",
        f"- Structured checks required: `{route['closure']['structured_checks_required']}`",
        f"- Compact: `{route['closure']['compact']}`",
    ])
    return "\n".join(sections).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(prog="capability_router")
    parser.add_argument("prompt")
    parser.add_argument("--context", action="store_true")
    parser.add_argument("--phase", choices=["INFO", "ORIENT", "DISCOVER", "RESEARCH", "BRAINSTORM", "SPECIFY", "PLAN", "IMPLEMENT", "VERIFY", "RELEASE"])
    args = parser.parse_args()
    route = route_prompt(args.prompt, phase_override=args.phase)
    if args.context:
        print(build_context_pack(args.prompt, route))
    else:
        print(json.dumps(route, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
