# 🧭 NoOverkill — AI Coding Rules Against Overengineering

![NoOverkill — Less overengineering. More working code.](site/banner.svg)

**Less overengineering. More working code.**

Rules, skills & plugins for **Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and OpenCode**.

[🌐 Website](https://rikfish163-rgb.github.io/nooverkill/en/) · [📜 Full rules](RULES.md) · [⚡ Core rules](rules/core.md) · [🇨🇳 中文](README.md)

Portable working instructions for coding agents, combining scope control, engineering conventions, purposeful verification, and final-result writing. Community feedback focuses on problems and positive outcomes observed after using this repository’s prompts.

Report every genuine issue, including uncommon inputs reachable through supported usage. Bound the remedy, not discovery. Required security, compatibility, migration, and review work stays required. Prefer concrete judgment and continued delivery over speculative scaffolding or repeated audits.

## 🚀 Quick start: copy the prompt

Paste this block into your agent’s instruction file while preserving existing project instructions, or try it in the current conversation. Use `AGENTS.md` for Codex/OpenCode, `CLAUDE.md` for Claude Code, or `GEMINI.md` for Gemini CLI. See [platform instructions](hosts.md) for other hosts.

```text
# NoOverkill · Core

Follow higher-priority instructions and explicit user requests. Specific project requirements override these general defaults. These rules limit remedies, never the discovery or reporting of genuine problems.

1. Report real problems, including rare cases reachable through documented examples, public interfaces, or actual project data. Reachability is enough; reproduction is unnecessary. A hypothetical construction alone is insufficient. Say when something is correct; do not manufacture findings.
2. Unless the project states otherwise, assume a cooperating operator on their own machine. Follow its actual threat model. Validate appropriately without speculative security hardening.
3. Add hashes, checksums, or fingerprints only when they replace a materially costlier operation AND their result changes the next action. Do not add feature flags, migration frameworks, compatibility layers, wrappers, or guards for conditions that do not occur here.
4. Obscure encodings, symlink races, right-to-left text, and millisecond races are outside repair scope unless supported use makes them reachable. An uncommon real case still counts.
5. Make the required judgment. Do not substitute scoring tables, checklists, or repeated validation of settled conclusions. Before a check, state the concrete failure it detects and what you will do differently if it occurs; otherwise skip a discretionary check. Repeat only for relevant changes, new failures, unresolved concerns, or explicit requirements.
6. Security, migration, compatibility, generation, validation, and review explicitly required by the user, project, or higher-priority instructions remain mandatory. They are the work, not overengineering.
7. Choose a reasonable approach, state the material tradeoff, and proceed. Ask only for materially different options, hard-to-reverse choices, or required approval. Record nonblocking details and continue independent work. Do not stall to avoid choosing. Before adding in-scope speculative race/security complexity, explain the failure, likelihood, and cost and obtain required buy-in; do not reopen excluded hypotheticals.
8. Present final results directly in the project's style. Lead papers and reports with their strongest supported results. Keep numbers in tables; explain actual tradeoffs and state other weaker numbers neutrally. Consolidate material caveats in Limitations or Known Issues. Omit excluded topics without announcing the omission.
9. Keep instructions, intermediate errors, abandoned approaches, revision history, and explanations of omitted alternatives out of code, comments, docstrings, commits, PRs, and summaries. Do not add AI-assistance signatures or formulaic transitions. Retain necessary final constraints, accurate limitations, and required generator metadata.

Calibration examples, not a rejection checklist: row hashes where cell comparison suffices; unread checksums; account hardening for an app without users/deployment; overnight audits with no feature; a reviewer that rejects everything; guards justified only by guards. Conversely, a digest that avoids rereading a large available file and a failing input from the project's documented example are legitimate. Never dismiss a real finding merely because it resembles an unnecessary-work example.
```

This is the core version. [RULES.md](RULES.md) also contains the engineering topics and their applicability conditions.

## 🔌 Choose an installation

| Form | Behavior | Hosts |
| --- | --- | --- |
| 📜 Rules | Persistent project instructions; full or core text | Six file adapters |
| 🧩 Skill | Core principles on invocation; full engineering reference on demand | Six skill adapters |
| 📦 Plugin | Host-managed distribution of the same skill | Codex and Claude Code |

Usually choose one entry point. The display name is **NoOverkill**; the Skill and Plugin installation ID is `agent-scope`. Installing a plugin makes its skill available; it does not append the full rules to every conversation.

### 📦 Native plugins

Run in your **system terminal**, from any directory. Requires Git and a host version with plugin commands.

**Codex:**

```bash
codex plugin marketplace add rikfish163-rgb/nooverkill
codex plugin add agent-scope@agent-scope
```

**Claude Code:**

```bash
claude plugin marketplace add rikfish163-rgb/nooverkill
claude plugin install agent-scope@agent-scope --scope user
```

The first command registers this repository as a marketplace; the second installs its plugin. In `agent-scope@agent-scope`, the left name is the plugin and the right name is the marketplace. Start a new session, then select **NoOverkill** in Codex or type `/agent-scope:agent-scope` followed by your task in Claude Code chat.

### 📜 Rule files / 🧩 Standalone skill

Requires Git and Python 3.9+, with no Python dependencies. Download the tool once, from any directory:

```bash
# macOS / Linux · Bash / Zsh
git clone https://github.com/rikfish163-rgb/nooverkill.git "$HOME/.local/share/agent-scope"
```

Replace `/absolute/path/to/project` with your **target project**, not the downloaded tool repository. Choose one:

```bash
# Append the full prompt to the target project's AGENTS.md, preserving existing instructions
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --kind rules --project "/absolute/path/to/project"
```

```bash
# Install the complete skill folder at .agents/skills/agent-scope/ in the target project
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --kind skill --project "/absolute/path/to/project"
```

Replace `codex` with `claude`, `cursor`, `copilot`, `gemini`, or `opencode`. Rules accept `--profile core`; skills include the core and full reference together. Start a new session, then invoke a standalone skill with `$agent-scope` in Codex or `/agent-scope` in Claude Code.

<details>
<summary>🪟 Windows PowerShell</summary>

Download once and replace `C:\path\to\project` with your target project:

```powershell
git clone https://github.com/rikfish163-rgb/nooverkill.git "$env:LOCALAPPDATA\agent-scope"
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --kind rules --project "C:\path\to\project"
```

Change `--kind rules` to `--kind skill` for a standalone skill.

</details>

Use `--project .` only when already in the target project. Use `--global` instead for a personal installation. Update the tool checkout with `git pull --ff-only`, then repeat the original installer command. Append `--remove` to that command to uninstall.

[📖 Platform paths, complete update/remove commands, and Gemini extension](hosts.md) · [🧩 Skill package](skills/agent-scope) · [📦 Plugin package](plugins/agent-scope)

## 💬 Share what happened after using the prompt

🐛 [Report a usage problem / Bad case](https://github.com/rikfish163-rgb/nooverkill/issues/new?template=bad-case.yml): problems that persist or appear after applying NoOverkill, including continued overengineering, missed necessary checks, suppressed real findings, over-correction, or conflicts with project requirements.

🌱 [Share a solved problem or positive outcome](https://github.com/rikfish163-rgb/nooverkill/issues/new?template=positive-case.yml): what was blocked before, what the agent did after using the prompt, and what improved or was delivered. Before/after excerpts are welcome; no invented measurements are needed.

Include the agent/model/version, prompt edition and version, loading method, task context, and relevant evidence. Illustrative examples remain separate from actual usage reports. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 🛠️ Development

Run from this repository root; on Windows, replace `python3` with `py -3`.

```bash
python3 scripts/build_packages.py
python3 -m unittest discover -s tests
node --check site/app.js
python3 scripts/build_site.py
python3 -m http.server 8000 --directory docs
```

The site is buildless HTML/CSS/JS with a standard-library Python content build. GitHub Pages serves `main:/docs`.

## ⭐ Support the project

If NoOverkill helped you finish a task or cut unnecessary work, [star the repository](https://github.com/rikfish163-rgb/nooverkill) and share an excerpt. Real usage problems and positive outcomes help others judge where these instructions are useful.

## ⚠️ Limitations

Instructions guide behavior; they do not guarantee compliance. Host limits, excluded sources, compaction, and more specific project rules can affect loading or behavior. Tests cover installer file operations, package contents, and site content; compatibility documentation is not a claim of end-to-end testing on every client or measured model improvement.

MIT. See [LICENSE](LICENSE) and [attribution](THIRD_PARTY_NOTICES.md).
