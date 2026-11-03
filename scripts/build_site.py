#!/usr/bin/env python3
"""Build the static GitHub Pages site from canonical rules and case data."""

import html
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(destination=None):
    target = Path(destination) if destination else ROOT / "docs"
    target.mkdir(parents=True, exist_ok=True)
    rules = {
        "full": (ROOT / "RULES.md").read_text(encoding="utf-8"),
        "core": (ROOT / "rules/core.md").read_text(encoding="utf-8"),
    }
    data = {
        "rules": rules,
        "platforms": json.loads((ROOT / "platforms.json").read_text(encoding="utf-8")),
        "cases": json.loads((ROOT / "cases/catalog.json").read_text(encoding="utf-8")),
    }
    payload = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    template = (ROOT / "site/index.html").read_text(encoding="utf-8")
    page = template.replace("@@RULES@@", html.escape(rules["full"])).replace("@@DATA@@", payload)
    (target / "index.html").write_text(page, encoding="utf-8")
    for name in ["app.js", "style.css", "mark.svg"]:
        shutil.copyfile(ROOT / "site" / name, target / name)
    (target / "RULES.md").write_text(rules["full"], encoding="utf-8")
    (target / "CORE.md").write_text(rules["core"], encoding="utf-8")
    (target / ".nojekyll").write_text("")
    return target


if __name__ == "__main__":
    print(f"Built: {build()}")
