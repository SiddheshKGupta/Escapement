from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from capability_router import (  # noqa: E402
    classify_tier,
    enumerated_scope_areas,
    route_prompt,
    select_doctrine,
)

CLINICAL_PROMPT = (
    "Build a clinical operations platform for a multi-site outpatient clinic "
    "group: patient registration and demographics, appointment scheduling "
    "across sites and clinicians, clinical encounter notes, consent capture "
    "and withdrawal, prescription records, and an audit trail. Staff roles "
    "include receptionist, nurse, clinician, and compliance officer with "
    "different access to clinical data."
)


class TierClassificationIsDomainNeutralTest(unittest.TestCase):
    """classify_tier()'s PROGRAM-vs-MATERIAL branch required 3+ hits from an
    IT-vocabulary list (workflow, dashboard, integration, RBAC, api, ...).
    Found by running a real clinical-platform request through the runtime: it
    scored 1 hit ("audit") and classified MATERIAL, so the default phase plan
    silently ended at VERIFY -- no POLISH, no RELEASE -- and the PROGRAM
    module registry never triggered. The technical-noun path is unchanged;
    enumerated_scope_areas() adds a domain-neutral signal alongside it: a
    request naming several distinct functional areas is a new product
    regardless of which domain's words it uses to name them."""

    def test_clinical_platform_classifies_program(self):
        self.assertEqual(classify_tier(CLINICAL_PROMPT), "PROGRAM")

    def test_logistics_platform_classifies_program(self):
        prompt = (
            "Build a warehouse logistics platform with pallet intake, "
            "putaway, dispatch routing, carrier integration, returns "
            "handling and stock audit."
        )
        self.assertEqual(classify_tier(prompt), "PROGRAM")

    def test_lending_system_classifies_program(self):
        prompt = (
            "Design a lending system covering origination, credit scoring, "
            "disbursement, collections and regulatory reporting."
        )
        self.assertEqual(classify_tier(prompt), "PROGRAM")

    def test_it_vocabulary_path_still_works(self):
        prompt = (
            "Build an internal automation platform with workflow, dashboard, "
            "RBAC, API integration and audit modules."
        )
        self.assertEqual(classify_tier(prompt), "PROGRAM")

    def test_single_feature_request_stays_material(self):
        for prompt in (
            "Add a user login endpoint that stores credentials in the database.",
            "Design a premium enterprise management dashboard with charts, "
            "responsive behaviour and subtle animations.",
            "Build a reconciliation report for invoices and payments.",
            "Implement a CSV export for the orders table with filters and pagination.",
        ):
            self.assertEqual(classify_tier(prompt), "MATERIAL", prompt)

    def test_micro_and_info_are_unaffected(self):
        self.assertEqual(classify_tier("Fix this typo in the header."), "MICRO")
        self.assertEqual(classify_tier("What does this five-line function do?"), "INFO")

    def test_enumeration_alone_does_not_force_program_without_a_product_verb(self):
        """A long list without "build/create/design/implement" + a product
        noun should not trip the domain-neutral branch -- it exists to widen
        detection of new products, not to reclassify any long sentence."""
        prompt = (
            "Explain patient registration, scheduling, consent, prescriptions "
            "and audit trails in this codebase."
        )
        self.assertGreaterEqual(enumerated_scope_areas(prompt), 4)
        self.assertNotEqual(classify_tier(prompt), "PROGRAM")


class DoctrinePackRejectionIsLabelledTest(unittest.TestCase):
    """select_doctrine() returned ranked[limit:] as the rejected tail with no
    rejected_because set, unlike select_skills(). harness_observability.py
    aggregates rejection_reasons with `if reason:` and silently dropped every
    budget-rejected pack from its trend -- the report meant to surface
    exactly that. Found while inspecting a real route's rejected list and
    seeing (id, None) pairs."""

    def test_budget_rejected_packs_carry_a_reason(self):
        _, rejected = select_doctrine(
            "Build a claims platform with intake, triage, adjudication, "
            "payment approval and reporting.",
            tier="PROGRAM", register="DUAL", phase="DISCOVER", limit=1,
        )
        self.assertTrue(rejected)
        for item in rejected:
            self.assertEqual(item.get("rejected_because"), "phase-pack-budget")

    def test_no_route_produces_a_null_rejection_reason(self):
        route = route_prompt(CLINICAL_PROMPT, phase_override="DISCOVER")
        for item in route["rejected"]:
            self.assertTrue(
                item.get("rejected_because"),
                f"{item.get('id')} rejected with no reason",
            )


class RegulatedDataRoutingTest(unittest.TestCase):
    """security-review's triggers (security, authentication, RBAC, PII, ...)
    never fired for a prompt about patient records, consent and per-role
    clinical-data access -- real security concerns described in domain
    language rather than security jargon. security-review is phase-eligible
    at RESEARCH/SPECIFY/PLAN/VERIFY/RELEASE (before implementation, not just
    after) but was never actually selected because its trigger score was 0."""

    def test_security_review_routes_for_phi_consent_language(self):
        for phase in ("RESEARCH", "SPECIFY", "PLAN", "VERIFY"):
            route = route_prompt(CLINICAL_PROMPT, phase_override=phase)
            skills = {item["id"] for item in route["native_skills"]}
            self.assertIn("security-review", skills, phase)

    def test_security_review_routes_before_implementation(self):
        route = route_prompt(CLINICAL_PROMPT, phase_override="SPECIFY")
        skills = {item["id"] for item in route["native_skills"]}
        self.assertIn("security-review", skills)

    def test_pii_trigger_still_works(self):
        route = route_prompt(
            "Build an API that exposes user PII including SSN and address.",
            phase_override="SPECIFY",
        )
        skills = {item["id"] for item in route["native_skills"]}
        self.assertIn("security-review", skills)


class DataHandlingMaterialQuestionTest(unittest.TestCase):
    """The five material questions were a fixed, domain-agnostic bank (users,
    success, domain/regulatory, constraints, authority). None asked what
    consent withdrawal or a deletion request must do to records already
    created -- a schema-shaping decision for any product touching PHI, PII,
    biometric or financial-account data. Adding a conditional sixth question
    that only surfaces (within the existing five-question cap) when the
    prompt names regulated personal data."""

    def question_ids(self, prompt):
        route = route_prompt(prompt, phase_override="DISCOVER")
        return [q["id"] for q in route["decision_brief"]["questions"]]

    def test_fires_for_regulated_personal_data(self):
        self.assertIn("data_handling", self.question_ids(CLINICAL_PROMPT))

    def test_does_not_fire_for_an_unrelated_prompt(self):
        self.assertNotIn(
            "data_handling",
            self.question_ids("Add a login endpoint that stores a password hash."),
        )

    def test_mentioning_withdrawal_as_a_feature_does_not_suppress_the_question(self):
        """A prior version of the guard treated the mere word "withdrawal" as
        proof the retention answer was already given -- exactly backwards for
        a prompt whose whole point is to build a withdrawal feature."""
        self.assertIn(
            "data_handling",
            self.question_ids("Build consent capture and withdrawal for patient records."),
        )

    def test_stating_the_actual_retention_answer_suppresses_the_question(self):
        prompt = (
            "Build patient records with a documented retention policy: "
            "consent-linked data blocked on withdrawal, retained per statute."
        )
        self.assertNotIn("data_handling", self.question_ids(prompt))

    def test_question_bank_still_caps_at_five(self):
        route = route_prompt(CLINICAL_PROMPT, phase_override="DISCOVER")
        self.assertLessEqual(len(route["decision_brief"]["questions"]), 5)


if __name__ == "__main__":
    unittest.main()
