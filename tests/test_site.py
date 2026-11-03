import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("builder", ROOT / "scripts/build_site.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class SiteTests(unittest.TestCase):
    def test_built_page_carries_exact_rules_and_working_local_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            target = builder.build(directory)
            page = (target / "index.html").read_text(encoding="utf-8")
            payload = re.search(r'<script id="scope-data" type="application/json">(.*?)</script>', page, re.S).group(1)
            data = json.loads(payload)
            self.assertEqual(data["rules"]["full"], (ROOT / "RULES.md").read_text(encoding="utf-8"))
            self.assertEqual((target / "RULES.md").read_text(encoding="utf-8"), data["rules"]["full"])
            self.assertEqual((target / "CORE.md").read_text(encoding="utf-8"), data["rules"]["core"])
            self.assertNotIn("@@", page)
            ids = set(re.findall(r'\bid="([^"]+)"', page))
            for anchor in re.findall(r'href="#([^"]+)"', page):
                self.assertIn(anchor, ids)
            for asset in re.findall(r'(?:href|src)="([^"]+)"', page):
                if asset.startswith(("http", "#")):
                    continue
                self.assertTrue((target / asset).is_file(), asset)

    def test_cases_have_distinct_ids_and_explicit_evidence(self):
        cases = json.loads((ROOT / "cases/catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual({case["kind"] for case in cases}, {"bad", "positive"})
        for case in cases:
            for key in ["id", "kind", "family", "title", "task", "behavior", "reason", "action", "evidence", "source", "source_label"]:
                self.assertTrue(case.get(key), (case.get("id"), key))
            self.assertIn(case["evidence"], {"illustrative", "observed"})
            self.assertEqual(urlparse(case["source"]).scheme, "https")

    def test_core_retains_the_nine_rules(self):
        core = (ROOT / "rules/core.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'^(\d)\. ', core, re.M), list("123456789"))
        self.assertIn("reproduction is unnecessary", core)
        self.assertIn("remain mandatory", core)
        self.assertIn("next action", core)


if __name__ == "__main__":
    unittest.main()
