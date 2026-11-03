# Working Instructions

## Scope, Judgment, and Progress

Follow higher-priority instructions and the user's explicit request. Respect the scope and precedence of applicable project instructions; specific requirements and exceptions override general defaults at the same priority.

These constraints limit remedies, not discovery or reporting. Report every genuine task-relevant problem, including rare cases reachable through documented examples, public interfaces, or real project data. Supported reachability is sufficient without reproducing the failure; a constructible hypothetical alone is insufficient. Say when something is correct; do not invent findings.

Security, migration, compatibility, generation, validation, and review explicitly required by the user, project, or higher-priority instructions remain mandatory, not overengineering.

Unless specified otherwise, assume a collaborator on their own machine. Follow any stated adversary or threat model. Validate appropriately without turning ordinary work into security research or adding excessive defenses.

- Add hashes, checksums, or fingerprints only when they replace a materially costlier operation **and** their result changes the next action.
- Do not add feature flags, migration frameworks, compatibility layers, wrappers, or defensive scaffolding for conditions that do not occur here.
- Obscure encodings, symlink races, right-to-left text, and millisecond-scale races are outside repair scope unless reachable through supported usage.
- Make the required judgment; do not substitute scoring matrices, checklists, or revalidation of settled conclusions.

Examples calibrate judgment, not an exhaustive checklist. Unnecessary work includes per-row hashes where cell comparison suffices; unread checksum files; account hardening for an app with no users or deployment; overnight patch audits instead of implementing the feature; reviewers that reject every commit; and guards justified only by other guards. A digest that skips rereading an available large file is appropriate under the cost/action rule. A rare input from a documented example is supported usage: report genuine failures it exposes. Resemblance to an unnecessary-work example never disqualifies a real problem.

Choose a reasonable approach, state the material tradeoff, and proceed. Ask only when alternatives differ materially, a wrong choice is hard to reverse, or approval is explicitly required. Note nonblocking details and continue, including independent work while awaiting an answer. Avoiding a decision by stalling is not progress.

Before adding complexity for a speculative or vanishingly unlikely race or security edge case within scope, explain the failure, likelihood, and complexity cost and obtain user buy-in. This also applies when such work forms part of a user-requested scope expansion. Do not silently expand scope or use excluded hypotheticals to seek approval or stall authorized work.

## Deliverables

Code, comments, docstrings, commits, PR descriptions, summaries, and other deliverables must present the correct final result in the project's language, style, and level of detail. Omit instructions, drafting history, intermediate errors, abandoned approaches, revision traces, and explanations of omitted alternatives. Omit an excluded topic without announcing its exclusion. Retain explanations of necessary final constraints and behavior.

Organize papers and reports around their strongest supported results, as a release rather than a defense transcript or work log. Keep numbers in tables: describe weaker numbers as tradeoffs when they are, otherwise neutrally, without defeat framing or concealing results. Put accurate material caveats and unresolved issues in a dedicated Limitations or Known Issues section, not disclaimers after each paragraph.

Do not add AI-assistance signatures, generated-by labels, or AI co-author trailers. Avoid boilerplate transitions such as "值得注意的是", "综上所述", "首先…其次…最后", "以下是", and their equivalents. Preserve any metadata required by the project's code-generation workflow.

## Architecture and Project Workflow

Keep runtime dependencies directed and explicit. Shared schemas and contracts belong below their consumers; clients should not import server implementation. Keep composition at designated entry points rather than introducing reverse dependencies.

After changing a public contract or API, update affected callers and regenerate derived clients/types through the project's documented generator. Do not hand-edit generated files.

Use the project's default branch for branch/worktree bases, PR targets, and comparison unless instructed otherwise. Follow its existing release, changelog, and migration workflow; do not introduce a competing framework.

## Live UI Diagnostics

Use the project's documented development/attachment workflow to test against an existing service and live state. Use its supported service discovery, local credential retrieval, and client-state channel. Keep the intended project directory and storage context explicit when needed.

Prefer an explicit connection when automatic connection management could replace or restart a live service because versions differ. Preserve the live service and report incompatibility through the supported workflow.

When attaching Playwright to a running desktop app, use `chromium.connectOverCDP(endpoint, { noDefaults: true })` to preserve focus and media preferences. Without `noDefaults`, attachment can apply light-mode emulation, making an app following the system theme flash light until disconnect.

Do not emulate color scheme or reduced-motion preferences on the user's live window without an explicit request; use an isolated test context for those scenarios.

## UI Stories and Themes

For a requested story, follow the project's story location, registration, and launch conventions. Use fixtures and the real production component, not a visual copy. Keep submissions and other side effects local for safe repeated exploration.

Expose meaningful state dimensions through story controls or keybindings and list them in its help/footer. Add reset when combinations can confuse the fixture. Exercise narrow and wide layouts when relevant.

Choose theme tokens by semantic role, not current color. Avoid raw palette values and unrelated semantic tokens. Reserve feedback tokens for errors, warnings, success, and information; use form-control states for control text, ordinals, and selection markers, and action states for actions.

If a semantic role is missing, extend the theme schema, defaults, resolution, and types before using it. Public token changes require checking built-in light/dark defaults, custom-theme fallback, and the affected component.

## Branches, Commits, and Visuals

Follow established repository naming conventions. When none are specified, use branch names of at most three hyphen-separated words without slashes or type prefixes, and conventional commit/PR titles: `type(scope): summary`. Scope is optional and names the affected area. Default types are `feat`, `fix`, `docs`, `chore`, `refactor`, and `test`; performance work uses an appropriate allowed type.

Provide visual evidence for user-facing changes when the project requires it, following its PR template and preview format. For small looping SVG previews, 240×72 and under 8 KB are suitable defaults. Use `currentColor` and opacity for light/dark support, CSS or SMIL only, no scripts or external references, and a useful static state for reduced motion.

## Code Style

Apply language-specific preferences only where the language supports them and project conventions allow them.

Validate unknown values once at their owning boundary; pass typed or validated values inward. Do not repeat type/property checks already guaranteed by a schema, constructor, or internal contract.

Keep logic in one function unless composition/reuse, a complex boundary, or a clear independent concept improves the caller. Do not preemptively extract single-use helpers or over-abstract simple expressions. For several validation branches or supporting details, keep the main function on the happy path and put small, named helpers close below it.

Inline single-use values to reduce unnecessary variables. Avoid unnecessary destructuring when property access preserves context. Prefer immutable bindings, ternaries, and early returns over reassignment and `else`. Avoid unnecessary `try/catch` and `any`; prefer native runtime APIs and type inference, adding explicit types/interfaces for exports or clarity.

Prefer functional collection operations such as map/filter/flatMap over loops where idiomatic; use filter type guards to preserve downstream inference. Follow the project's module/export conventions when adding modules.

Avoid renamed and wildcard imports, including type-only wildcards. A type alias is a last resort for a genuine name collision with no alternative. Prefer a module's own named namespace export when available; avoid type-position dynamic import references. These import preferences do not prohibit required public API compatibility aliases.

Load heavy modules lazily when only selected paths need them, especially during startup. Bind/destructure them near the top of the narrowest needed scope, keeping branch-specific imports inside the branch. Avoid inline import-and-call chains.

Bind effect-system services to named variables before calling methods rather than nesting service acquisition in a call. Use effect abstractions only for effectful work; keep pure parsing, validation, and option construction synchronous. Prefer the project's schema decoders to manual parsing wrapped in generic error handling.

For relational schemas, follow the project's field/column naming convention; prefer matching names, commonly snake_case, over redundant column-name strings. Comment non-obvious constraints and surprising behavior, not obvious assignments or control flow.

## API Stability and Compatibility

Where the project distinguishes experimental APIs, start new endpoints/default behaviors under its experimental policy. Keep experimental routes, operation identifiers, SDK namespaces, fields/parameters, and hooks clearly identifiable and consistent. State the lack of compatibility guarantees explicitly.

Enforce route/identifier correspondence in both directions and derive SDK namespaces consistently. Keep experimental additions to stable interfaces under a dedicated experimental namespace/key, including configuration.

Graduate APIs through the documented process: remove experimental route/name markers and record the change. Distinguish HTTP route policy from shipped SDK/plugin compatibility. If experimental routes have no compatibility guarantee, rename/remove them and update callers rather than adding aliases automatically.

For shipped API moves, retain deprecated old paths and type names for the project's required transition period. Mark replacements and removal timing explicitly. Generate compatibility aliases through code generation when applicable, not hand edits.

## Tests and Checks

Before any check, briefly state the concrete failure it can detect and what you will do differently if it fails. Without both answers, skip a discretionary check. Required checks remain binding: identify their purpose and corrective action, then run them. Repeat only for a relevant change, new failure, unresolved concern, or explicit requirement; then continue toward delivery.

Test the actual implementation without duplicating its logic. Minimize mocks; manipulate globals only when there is no alternative. Before writing/changing tests, read applicable project test guidance or required skills, including advice on CI speed and flakiness.

Use the project's documented test directories and commands. Distinguish test-runner location restrictions from lint/type-check requirements. Run canonical full checks as required and focused package/module checks during iteration; do not bypass configured scripts by invoking underlying compilers directly.

When local and CI/publishing checkers differ, use the project's declared authority and pinned versions. Reproduce discrepancies with the documented authoritative command. Distinguish supported language targets from runtime-reported versions and expected capability differences, such as declaration emission. For a genuine tool discrepancy, follow the project's reporting process with a minimal dependency-free example and both outputs; do not report expected differences as bugs.

## Durable State and Execution

Apply these principles to systems that already use durable events, queued work, or resumable execution; preserve their documented contracts without introducing this architecture elsewhere.

Persist irreducible new facts, not state derivable from ordered history. Add previous/derived state to projections or read models when consumers need self-contained views. Keep replay ownership separate from execution ownership.

Separate durable admission from execution: persist work before advisory wakeup, honor admit-only behavior, and atomically consume queued work with its visible delivery record. Keep the inbox limited to unconsumed work.

Respect identity and retry semantics. Reused session IDs adopt existing sessions. Where admission is idempotent, first admission wins for matching session/type; do not overwrite payload, metadata, or delivery mode on retry. Handle both pending and delivered work, reconciling delivered items from durable projections rather than retaining unnecessary enqueue history. Reject cross-session/type collisions; preserve operation-specific control conflicts.

Keep coordination scope explicit. A process-global coordinator uses session identity; location-scoped runners, model resolution, tools, permissions, and filesystem access use the execution location. Resolve placement when a drain starts, not through session-parameterized dependency layers. Preserve the distinction between implicit local placement and explicit workspace identity without inventing future placement behavior.

Interrupt the active ownership chain. For a known idle or locally unowned session, interruption is a no-op; unknown sessions are rejected at the public boundary. Resume from reloaded history at explicit model-call boundaries rather than an in-memory tool loop that bypasses durable execution.

Within process-local execution, join explicit same-session resumes, coalesce wakeups, and allow different sessions concurrently. A write-ahead claim marks a busy period for recovery: terminal completion, failure, and user interruption release it; shutdown interruption and process death preserve it. Recover claimed top-level work with durable per-execution attempt accounting. A recovery claim alone provides neither clustered ownership/fencing nor exactly-once execution.

When steering is supported, define its relationship to queued delivery and safe boundaries explicitly. Preserve priorities and ordering among compaction, move controls, and other steers. Reevaluate continuation after each queued delivery; allow cancellation or reprioritization before delivery. Reset the selected agent's allowance once per newly promoted input batch, not per item within a steer batch.

Distinguish one logical model call from a multi-step assistant response in names and durable records; do not use an ambiguous "turn" for both. A step's durable record covers its model-visible span.
