# 🧭 Agent Scope

![Agent Scope — Do the work. Keep it proportionate.](site/banner.svg)

**Do the work. Keep it proportionate.**

[🌐 Website](https://rikfish163-rgb.github.io/agent-scope/) · [📜 Full rules](RULES.md) · [⚡ Core rules](rules/core.md) · [🇨🇳 中文](README.md)

Portable working instructions for coding agents, combining scope control, engineering conventions, purposeful verification, and final-result writing. The bad cases below explain the behaviors these instructions address. Community feedback focuses on problems and positive outcomes observed after using this repository’s prompts.

Report every genuine issue, including uncommon inputs reachable through supported usage. Bound the remedy, not discovery. Required security, compatibility, migration, and review work stays required. Prefer concrete judgment and continued delivery over speculative scaffolding or repeated audits.

## 🚀 Quick start: copy the prompt

Paste this block into your agent’s instruction file while preserving existing project instructions, or try it in the current conversation. Use `AGENTS.md` for Codex/OpenCode, `CLAUDE.md` for Claude Code, or `GEMINI.md` for Gemini CLI. See [platform instructions](hosts.md) for other hosts.

```text
# Agent Scope · Core

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

## 🔌 Command installation

Run from the target project directory. Requires Git and Python 3.9+, with no Python dependencies.

```bash
git clone https://github.com/rikfish163-rgb/agent-scope.git "$HOME/.local/share/agent-scope"
python3 "$HOME/.local/share/agent-scope/install.py" --agent codex --project .
```

Available adapters: `codex`, `claude`, `cursor`, `copilot`, `gemini`, `opencode`. Existing project text is preserved; reinstalling updates the managed block. Add `--profile core` for the nine core principles, or `--remove` to uninstall the block. Use `--dry-run` to preview the destination. Supported hosts also accept `--global`; custom hosts accept `--agent generic --target /path/to/instructions.md`.

On Windows PowerShell:

```powershell
git clone https://github.com/rikfish163-rgb/agent-scope.git "$env:LOCALAPPDATA\agent-scope"
py -3 "$env:LOCALAPPDATA\agent-scope\install.py" --agent codex --project .
```

The optional Gemini CLI extension loads `RULES.md` directly:

```bash
gemini extensions install https://github.com/rikfish163-rgb/agent-scope
```

Choose file installation or the extension, not both. [Platform sources, update/remove commands, and loading details](hosts.md).

## 🚫 Bad cases: behaviors to reduce

These are calibration examples of the behavior the prompt is intended to address.

| Situation | ❌ Disproportionate behavior | ✅ Appropriate action |
| --- | --- | --- |
| Comparing tables | Hash every row and maintain an index just to find differences | Compare the cells directly |
| Delivering a file | Add checksum files no process reads | Use a digest only when it saves a costlier operation and changes the next action |
| Exploring a local prototype | Build account defenses for an app without users or deployment | Finish the prototype and perform explicitly required security work |
| Implementing a feature | Audit the same patch all night without delivering the feature | Run purposeful checks, then continue delivery |
| Reviewing code | Reject every submission regardless of evidence | Report concrete findings; say when the change is correct |
| Fixing a behavior | Add guards justified only by previous guards | Validate once at the owning boundary |
| Choosing an implementation | Repeatedly escalate equally reasonable options | Choose, state the tradeoff, and proceed |
| Writing the deliverable | Include drafting history and disclaimers in every paragraph | Present the final result and collect material limitations |

🟢 Keep necessary work: a digest that avoids rereading a large file, and a genuine failure exposed by the project’s documented input, are valid. Judge the actual requirement, not the appearance of defense.

## 💬 Share what happened after using the prompt

🐛 [Report a usage problem / Bad case](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=bad-case.yml): problems that persist or appear after applying Agent Scope, including continued overengineering, missed necessary checks, suppressed real findings, over-correction, or conflicts with project requirements.

🌱 [Share a solved problem or positive outcome](https://github.com/rikfish163-rgb/agent-scope/issues/new?template=positive-case.yml): what was blocked before, what the agent did after using the prompt, and what improved or was delivered. Before/after excerpts are welcome; no invented measurements are needed.

Include the agent/model/version, prompt edition and version, loading method, task context, and relevant evidence. Illustrative examples remain separate from actual usage reports. See [CONTRIBUTING.md](CONTRIBUTING.md).

## 🛠️ Development


```bash
python3 -m unittest discover -s tests
node --check site/app.js
python3 scripts/build_site.py
python3 -m http.server 8000 --directory docs
```

The site is buildless HTML/CSS/JS with a standard-library Python content build. GitHub Pages serves `main:/docs`.

## ⚠️ Limitations

Instructions guide behavior; they do not guarantee compliance. Host limits, excluded sources, compaction, and more specific project rules can affect loading or behavior. Tests cover installer file operations and site content; compatibility documentation is not a claim of end-to-end testing on every client or measured model improvement.

MIT. See [LICENSE](LICENSE) and [attribution](THIRD_PARTY_NOTICES.md).
