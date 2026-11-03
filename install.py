#!/usr/bin/env python3
"""Install, update, or remove the Agent Scope block in an agent instruction file."""

import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PLATFORMS = json.loads((ROOT / "platforms.json").read_text(encoding="utf-8"))
BEGIN = "<!-- agent-scope:start -->"
END = "<!-- agent-scope:end -->"


def read_text(path):
    if not path.exists():
        return ""
    with path.open(encoding="utf-8", newline="") as handle:
        return handle.read()


def span(text):
    starts, ends = text.count(BEGIN), text.count(END)
    if not starts and not ends:
        return None
    if starts != 1 or ends != 1 or text.index(BEGIN) > text.index(END):
        raise ValueError("The Agent Scope markers are incomplete or duplicated. Repair that block before updating it.")
    start, end = text.index(BEGIN), text.index(END) + len(END)
    if text[end:end + 2] == "\r\n":
        end += 2
    elif text[end:end + 1] == "\n":
        end += 1
    return start, end


def destination(args):
    if args.target:
        return Path(args.target).expanduser().absolute()
    if args.agent == "generic":
        raise ValueError("The generic adapter requires --target pointing to the host's instruction file.")
    platform = PLATFORMS[args.agent]
    if not args.global_scope:
        return Path(args.project).expanduser().absolute() / platform["project"]
    if "global" not in platform:
        raise ValueError(f"{platform['name']} has no global-file adapter here. Use --project or --target.")
    if args.agent == "codex" and os.environ.get("CODEX_HOME"):
        return Path(os.environ["CODEX_HOME"]).expanduser() / "AGENTS.md"
    return Path.home() / platform["global"]


def update(text, body, preamble="", remove=False):
    region = span(text)
    if remove:
        if region is None:
            return text
        return text[:region[0]] + text[region[1]:]
    newline = "\r\n" if "\r\n" in text else "\n"
    block = newline.join([BEGIN, body.rstrip().replace("\r\n", "\n").replace("\n", newline), END, ""])
    if region:
        return text[:region[0]] + block + text[region[1]:]
    if preamble and text.strip():
        raise ValueError("The dedicated rule file already contains unmanaged content. Choose another --target ending in .mdc, or add the rules manually.")
    prefix = text if text else preamble.replace("\n", newline)
    separator = "" if not prefix else newline if prefix.endswith(newline) else newline * 2
    return prefix + separator + block


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=[*PLATFORMS, "generic"], required=True)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--project", default=".", help="Target project directory (default: current directory)")
    scope.add_argument("--global", dest="global_scope", action="store_true", help="Install to this agent's user-level file")
    scope.add_argument("--target", help="Explicit instruction file for a custom host/location")
    parser.add_argument("--profile", choices=["full", "core"], default="full")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true", help="Show the destination without writing")
    action.add_argument("--remove", action="store_true", help="Remove only the Agent Scope block")
    args = parser.parse_args(argv)
    try:
        target = destination(args)
        if args.agent == "codex" and target.name == "AGENTS.md" and target.with_name("AGENTS.override.md").exists() and not args.remove:
            raise ValueError("AGENTS.override.md shadows this destination. Use --target with that file, or resolve the override first.")
        if args.agent == "cursor" and target.suffix != ".mdc":
            raise ValueError("Cursor project-rule targets must end in .mdc.")
        source = ROOT / ("RULES.md" if args.profile == "full" else "rules/core.md")
        original = read_text(target)
        preamble = PLATFORMS.get(args.agent, {}).get("preamble", "")
        result = update(original, source.read_text(encoding="utf-8"), preamble, args.remove)
        if result == original:
            print(f"Unchanged: {target}")
            return 0
        if args.dry_run:
            print(f"Would install {args.profile} rules: {target}")
            return 0
        if args.remove and result.strip() in ("", preamble.strip()):
            target.unlink()
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("w", encoding="utf-8", newline="") as handle:
                handle.write(result)
        print(f"{'Removed' if args.remove else 'Installed ' + args.profile}: {target}")
        if not args.remove:
            print("Only the Agent Scope block was added or replaced. Reload the agent's instructions or start a new session.")
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
