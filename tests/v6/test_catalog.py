from __future__ import annotations

import json
import unittest
from pathlib import Path


class ReferenceCatalogueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]
        self.catalog = json.loads(
            (self.root / "catalog/external-resources.json").read_text(
                encoding="utf-8"
            )
        )

    def test_resources_are_unique_and_actionable(self) -> None:
        resources = self.catalog["resources"]
        ids = [item["id"] for item in resources]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(resources), 23)
        for item in resources:
            self.assertTrue(item["url"].startswith("https://"))
            self.assertTrue(item["license"])
            self.assertTrue(item["use_when"])
            self.assertTrue(item["how_to_use"])
            self.assertTrue(item["do_not"])
            self.assertTrue(item["triggers"])

    def test_unlicensed_resource_is_restricted(self) -> None:
        item = next(
            value for value in self.catalog["resources"]
            if value["id"] == "perplexity-cli"
        )
        self.assertEqual(item["license_status"], "unverified-restrict-copying")
        self.assertNotIn("adapt", item["use_mode"])


if __name__ == "__main__":
    unittest.main()
