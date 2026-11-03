# Repository Working Notes

Use RULES.md for the shared working principles. It is the canonical full prompt; platform adapters must not rewrite its content.

This repository uses Python's standard library and buildless HTML/CSS/JavaScript. Run `python3 scripts/build_packages.py` after changes to rules or packaging sources, then `python3 -m unittest discover -s tests` for installer and package behavior. Run `python3 scripts/build_site.py` to rebuild the GitHub Pages site in docs/, and `node --check site/app.js` after JavaScript edits. Do not edit derived docs/ assets or bundled skill contents directly. Skill sources live in packaging/, RULES.md, and rules/core.md; plugin manifests and marketplace catalogs are maintained in place.

Preserve the distinction between illustrative cases, submitted community reports, and accepted evidence. Never invent model results or treat every added check as overengineering. Read CONTRIBUTING.md before adding a case.
