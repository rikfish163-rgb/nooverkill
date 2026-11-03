#!/usr/bin/env python3
"""Build the static GitHub Pages site from canonical rules and case data."""

import html
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://rikfish163-rgb.github.io/nooverkill/"


def search_metadata(language):
    english = language == "en"
    url = SITE + ("en/" if english else "")
    title = "NoOverkill — AI Coding Rules for Claude Code, Codex & Cursor" if english else "NoOverkill · AI 编码反过度设计规则 | Claude Code、Codex、Cursor"
    description = (
        "Reduce AI coding overengineering with portable rules, Agent Skills and plugins for Claude Code, Codex, Cursor, Copilot, Gemini CLI and OpenCode. Copy the prompt or install it."
        if english else
        "让 AI 少折腾，把代码做完。NoOverkill 提供可复制的反过度设计提示词、Skill 和 Plugin，支持 Claude Code、Codex、Cursor 等六个平台，保留必要校验与真实问题反馈。"
    )
    title, description = html.escape(title, quote=True), html.escape(description, quote=True)
    return f'''<title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="zh-CN" href="{SITE}">
  <link rel="alternate" hreflang="en" href="{SITE}en/">
  <link rel="alternate" hreflang="x-default" href="{SITE}en/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="NoOverkill">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="{'en_US' if english else 'zh_CN'}">
  <meta property="og:image" content="{SITE}social-preview.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="NoOverkill — Less overengineering. More working code.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE}social-preview.png">'''


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
    page = template.replace("@@HEAD@@", search_metadata("zh-CN")).replace("@@RULES@@", html.escape(rules["full"])).replace("@@DATA@@", payload)
    (target / "index.html").write_text(page, encoding="utf-8")
    (target / "en").mkdir(exist_ok=True)
    english = (ROOT / "site/en.html").read_text(encoding="utf-8").replace("@@HEAD@@", search_metadata("en")).replace("@@CORE@@", html.escape(rules["core"]))
    (target / "en/index.html").write_text(english, encoding="utf-8")
    for name in ["app.js", "copy.js", "style.css", "mark.svg", "social-preview.png"]:
        shutil.copyfile(ROOT / "site" / name, target / name)
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE}</loc></url>
  <url><loc>{SITE}en/</loc></url>
</urlset>
'''
    (target / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (target / "RULES.md").write_text(rules["full"], encoding="utf-8")
    (target / "CORE.md").write_text(rules["core"], encoding="utf-8")
    (target / ".nojekyll").write_text("")
    return target


if __name__ == "__main__":
    print(f"Built: {build()}")
