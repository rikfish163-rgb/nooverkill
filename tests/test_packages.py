import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/agent-scope"


class PackageTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "install.py"), "--kind", "skill", *args], capture_output=True, text=True)

    def test_every_host_installs_a_complete_skill_and_removes_it(self):
        platforms = json.loads((ROOT / "platforms.json").read_text(encoding="utf-8"))
        for agent, data in platforms.items():
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                result = self.invoke("--agent", agent, "--project", directory)
                self.assertEqual(result.returncode, 0, result.stderr)
                target = Path(directory) / data["skill_project"]
                for source in SKILL.rglob("*"):
                    if source.is_file():
                        self.assertEqual((target / source.relative_to(SKILL)).read_bytes(), source.read_bytes())
                again = self.invoke("--agent", agent, "--project", directory)
                self.assertEqual(again.returncode, 0, again.stderr)
                self.assertIn("Unchanged skill", again.stdout)
                removed = self.invoke("--agent", agent, "--project", directory, "--remove")
                self.assertEqual(removed.returncode, 0, removed.stderr)
                self.assertFalse(target.exists())

    def test_updates_replace_bundle_files_and_removal_preserves_user_additions(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "agent-scope"
            args = ["--agent", "generic", "--target", str(target)]
            self.assertEqual(self.invoke(*args).returncode, 0)
            reference = target / "references/engineering.md"
            reference.write_text("Older working agreement", encoding="utf-8")
            notes = target / "references/my-notes.md"
            notes.write_text("Keep my notes", encoding="utf-8")
            result = self.invoke(*args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(reference.read_bytes(), (ROOT / "RULES.md").read_bytes())
            self.assertEqual(self.invoke(*args, "--remove").returncode, 0)
            self.assertEqual(notes.read_text(encoding="utf-8"), "Keep my notes")
            self.assertFalse((target / "SKILL.md").exists())

    def test_unrelated_skill_is_not_overwritten_or_removed(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "agent-scope"
            target.mkdir()
            entry = target / "SKILL.md"
            entry.write_text("Unrelated instructions", encoding="utf-8")
            for action in ([], ["--remove"]):
                result = self.invoke("--agent", "generic", "--target", str(target), *action)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(entry.read_text(encoding="utf-8"), "Unrelated instructions")

    def test_dry_run_and_invalid_options_do_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "agent-scope"
            args = ["--agent", "generic", "--target", str(target)]
            self.assertEqual(self.invoke(*args, "--dry-run").returncode, 0)
            self.assertNotEqual(self.invoke(*args, "--profile", "core").returncode, 0)
            self.assertFalse(target.exists())
            result = self.invoke("--agent", "generic", "--target", str(Path(directory) / "wrong-name"))
            self.assertNotEqual(result.returncode, 0)

    def test_personal_paths_use_skill_locations(self):
        platforms = json.loads((ROOT / "platforms.json").read_text(encoding="utf-8"))
        for agent, data in platforms.items():
            with self.subTest(agent=agent):
                result = self.invoke("--agent", agent, "--global", "--dry-run")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(Path.home() / data["skill_global"]), result.stdout)

    def test_marketplaces_resolve_self_contained_packages_with_canonical_rules(self):
        portable = json.loads((ROOT / "plugins/agent-scope/plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / "plugins/agent-scope/.claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual((portable["name"], portable["version"]), (claude["name"], claude["version"]))
        for relative in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            catalog = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            source = catalog["plugins"][0]["source"]
            plugin = ROOT / (source["path"] if isinstance(source, dict) else source)
            bundled = plugin / "skills/agent-scope"
            self.assertTrue((plugin / "LICENSE").is_file())
            for path in SKILL.rglob("*"):
                if path.is_file():
                    self.assertEqual((bundled / path.relative_to(SKILL)).read_bytes(), path.read_bytes())
            self.assertEqual((bundled / "references/engineering.md").read_bytes(), (ROOT / "RULES.md").read_bytes())
            core = (ROOT / "rules/core.md").read_text(encoding="utf-8").split("\n", 1)[1].strip()
            self.assertIn(core, (bundled / "SKILL.md").read_text(encoding="utf-8"))
