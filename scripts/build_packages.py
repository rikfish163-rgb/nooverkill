#!/usr/bin/env python3
"""Build the standalone skill and plugin skill from the shared rules."""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build():
    template = (ROOT / "packaging/SKILL.md.in").read_text(encoding="utf-8")
    core = (ROOT / "rules/core.md").read_text(encoding="utf-8")
    body = template.replace("@@CORE@@", core.split("\n", 1)[1].strip())
    for relative in ("skills/agent-scope", "plugins/agent-scope/skills/agent-scope"):
        skill = ROOT / relative
        (skill / "references").mkdir(parents=True, exist_ok=True)
        (skill / "agents").mkdir(exist_ok=True)
        (skill / "SKILL.md").write_text(body, encoding="utf-8")
        shutil.copyfile(ROOT / "RULES.md", skill / "references/engineering.md")
        shutil.copyfile(ROOT / "packaging/openai.yaml", skill / "agents/openai.yaml")
        shutil.copyfile(ROOT / "LICENSE", skill / "LICENSE")
        shutil.copyfile(ROOT / "THIRD_PARTY_NOTICES.md", skill / "THIRD_PARTY_NOTICES.md")
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
        shutil.copyfile(ROOT / name, ROOT / "plugins/agent-scope" / name)


if __name__ == "__main__":
    build()
    print("Built: skills/agent-scope and plugins/agent-scope")
