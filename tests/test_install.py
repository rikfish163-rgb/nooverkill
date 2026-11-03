import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("installer", ROOT / "install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "install.py"), *args], capture_output=True, text=True)

    def test_shared_file_update_is_idempotent_and_preserves_surroundings(self):
        existing = "# Team rules\nKeep this instruction.\n"
        installed = installer.update(existing, "first rule")
        self.assertTrue(installed.startswith(existing))
        self.assertEqual(installer.update(installed, "first rule"), installed)
        with_suffix = installed + "\nUser notes after the block.\n"
        updated = installer.update(with_suffix, "replacement rule")
        self.assertIn("replacement rule", updated)
        self.assertNotIn("first rule", updated)
        self.assertTrue(updated.startswith(existing))
        self.assertTrue(updated.endswith("\nUser notes after the block.\n"))
        removed = installer.update(updated, "", remove=True)
        self.assertNotIn(installer.BEGIN, removed)
        self.assertTrue(removed.startswith(existing))
        self.assertTrue(removed.endswith("\nUser notes after the block.\n"))

    def test_all_project_adapters_install_the_full_canonical_prompt(self):
        canonical = (ROOT / "RULES.md").read_text(encoding="utf-8").strip()
        for agent, data in installer.PLATFORMS.items():
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as directory:
                result = self.invoke("--agent", agent, "--project", directory)
                self.assertEqual(result.returncode, 0, result.stderr)
                target = Path(directory) / data["project"]
                text = target.read_text(encoding="utf-8")
                self.assertIn(canonical, text)
                if agent == "cursor":
                    self.assertTrue(text.startswith("---\n"))
                    self.assertIn("alwaysApply: true", text)
                self.assertEqual(self.invoke("--agent", agent, "--project", directory).returncode, 0)
                self.assertEqual(target.read_text(encoding="utf-8"), text)
                removed = self.invoke("--agent", agent, "--project", directory, "--remove")
                self.assertEqual(removed.returncode, 0, removed.stderr)
                self.assertFalse(target.exists())

    def test_crlf_content_is_preserved(self):
        existing = "# Existing\r\nKeep me.\r\n"
        result = installer.update(existing, "one\ntwo")
        self.assertTrue(result.startswith(existing))
        self.assertNotIn("\n", result.replace("\r\n", ""))
        self.assertEqual(installer.update(result, "one\ntwo"), result)

    def test_partial_markers_are_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "AGENTS.md"
            original = "# Existing\n" + installer.BEGIN + "\nunfinished"
            target.write_text(original, encoding="utf-8")
            result = self.invoke("--agent", "codex", "--project", directory)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(target.read_text(encoding="utf-8"), original)

    def test_dry_run_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.invoke("--agent", "claude", "--project", directory, "--dry-run")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((Path(directory) / "CLAUDE.md").exists())

    def test_codex_override_is_actionable(self):
        with tempfile.TemporaryDirectory() as directory:
            override = Path(directory) / "AGENTS.override.md"
            override.write_text("# Team override\n", encoding="utf-8")
            result = self.invoke("--agent", "codex", "--project", directory)
            self.assertEqual(result.returncode, 1)
            self.assertIn("--target", result.stderr)
            self.assertFalse((Path(directory) / "AGENTS.md").exists())
            result = self.invoke("--agent", "codex", "--target", str(override))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(override.read_text(encoding="utf-8").startswith("# Team override\n"))

    def test_shared_agents_do_not_duplicate_the_block(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(self.invoke("--agent", "codex", "--project", directory).returncode, 0)
            self.assertEqual(self.invoke("--agent", "opencode", "--project", directory).returncode, 0)
            text = (Path(directory) / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(text.count(installer.BEGIN), 1)

    def test_unmanaged_cursor_rule_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / ".cursor/rules/agent-scope.mdc"
            target.parent.mkdir(parents=True)
            target.write_text("---\nalwaysApply: false\n---\nExisting rule", encoding="utf-8")
            original = target.read_bytes()
            result = self.invoke("--agent", "cursor", "--project", directory)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(target.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
