# AGENTS.md

**Session state:** Agent Handoff SessionStart injects `docs/handoff/state.md`; do not reread it when injected. Then use this file and `docs/handoff/conventions.md`.

**Full conventions reference:** [`docs/handoff/conventions.md`](docs/handoff/conventions.md) - LLM-targeted pattern library. Check it before adding persistent patterns.

**Detailed review workflows:** not configured for this repo.

## Repo Notes

- Canonical design: `docs/design/DESIGN.md`; `docs/design/tech-stack-pyside6.md` is supplementary and operational.
- Before implementation work, read the relevant spec or plan from `docs/handoff/specs-plans.md` and any ADR that would be contradicted.
- The model layer stays Qt-free; see convention 1 and `.importlinter`.
- Python code is governed by the immutable [Python Coding 0.6 companion](https://github.com/L3DigitalNet/project-standards/blob/v5.11.0/standards/python-coding/versions/0.6/README.md); it is reference-only and intentionally not enabled in `.standards/`.
- Do not run `uv run pre-commit install`; run `uv run pre-commit run --all-files` directly.

## Session End

- Update only changed handoff facts in `docs/`.
- Add a compact row to `docs/handoff/sessions/<YYYY-MM>.md` for durable work.
- If bug docs change, run `python3 docs/handoff/bugs/_regen_index.py && git diff --exit-code docs/handoff/bugs/INDEX.md`.

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:agent-handoff -->
<!-- markdownlint-disable MD025 -->
# Agent Handoff

Use the repo-local `agent-handoff` skill at session startup and closeout. Do not reread state already injected by SessionStart. Keep project knowledge inside this repository and store credential references only, never values.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:agent-handoff -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:markdown-tooling -->
<!-- markdownlint-disable MD025 -->
# Markdown and structured-text tooling

Prettier owns physical formatting and markdownlint owns Markdown structure. Do not add overlapping tools.

Enabled checks: format, lint.
Markdown scope: `**/*.md`.
Structured-config scope: `**/*.json`, `**/*.jsonc`, `**/*.yml`, `**/*.yaml`.
Lint additionally skips generated directories: `.ruff_cache/**`, `node_modules/**`.

Declared exclusions:
- `.pytest_cache/**` (both): Generated pytest cache content is not repository documentation.
- `.venv/**` (both): The uv-managed virtual environment contains third-party package documentation.
- `.agents/**` (both): Package-owned agent assets must retain their released bytes.
- `.claude/**` (both): Harness configuration is outside the documentation corpus.
- `.codex/**` (both): Harness configuration is outside the documentation corpus.
- `.standards/**` (both): Control-plane outputs must retain their reconciled bytes.
- `.github/PULL_REQUEST_TEMPLATE.md` (both): The GitHub interaction template is maintained separately.
- `.github/workflows/format.yml` (format): The exclusive managed caller is not Prettier-stable in 5.8.0; see upstream issue 48.
- `.github/workflows/lint-markdown.yml` (format): The exclusive managed caller is not Prettier-stable in 5.8.0; see upstream issue 48.
- `.import_linter_cache/**` (format): Generated Import Linter cache content is not repository source.
- `AGENTS.md` (both): Agent instructions contain package-managed envelopes.
- `CLAUDE.md` (both): Agent instructions contain package-managed envelopes.
- `docs/STATUS.md` (both): Agent Handoff owns the live status document.
- `docs/TODO.md` (both): Agent Handoff owns the live task document.
- `docs/adr/template.md` (both): The authoring template intentionally contains placeholders.
- `docs/handoff/**` (both): Agent Handoff governs this knowledge corpus.

Check formatting over exactly that scope, with Git as the corpus authority:

```bash
git ls-files -z -- ':(glob)**/*.md' ':(glob)**/*.json' ':(glob)**/*.jsonc' ':(glob)**/*.yml' ':(glob)**/*.yaml' ':(glob,exclude).agents/**' ':(glob,exclude).claude/**' ':(glob,exclude).codex/**' ':(glob,exclude).github/PULL_REQUEST_TEMPLATE.md' ':(glob,exclude).github/workflows/format.yml' ':(glob,exclude).github/workflows/lint-markdown.yml' ':(glob,exclude).import_linter_cache/**' ':(glob,exclude).pytest_cache/**' ':(glob,exclude).standards/**' ':(glob,exclude).venv/**' ':(glob,exclude)AGENTS.md' ':(glob,exclude)CLAUDE.md' ':(glob,exclude)docs/STATUS.md' ':(glob,exclude)docs/TODO.md' ':(glob,exclude)docs/adr/template.md' ':(glob,exclude)docs/handoff/**' | xargs -0 -r npx prettier --check --
```

Without Git, bound the same scope by glob instead. Prettier's CLI has no negative pattern, so this form does not apply the declared format exclusions above; pass them through an `--ignore-path` file inside the repository:

```bash
npx prettier --check --no-error-on-unmatched-pattern -- '**/*.md' '**/*.json' '**/*.jsonc' '**/*.yml' '**/*.yaml'
```

Never check or write with a bare `.`: it reaches undeclared languages and Git-excluded scratch.

Lint Markdown structure over the same Git-tracked scope:

```bash
git ls-files -z -- ':(glob)**/*.md' ':(glob,exclude).ruff_cache/**' ':(glob,exclude)node_modules/**' ':(glob,exclude).agents/**' ':(glob,exclude).claude/**' ':(glob,exclude).codex/**' ':(glob,exclude).github/PULL_REQUEST_TEMPLATE.md' ':(glob,exclude).pytest_cache/**' ':(glob,exclude).standards/**' ':(glob,exclude).venv/**' ':(glob,exclude)AGENTS.md' ':(glob,exclude)CLAUDE.md' ':(glob,exclude)docs/STATUS.md' ':(glob,exclude)docs/TODO.md' ':(glob,exclude)docs/adr/template.md' ':(glob,exclude)docs/handoff/**' | sed -z 's|^|:|' | xargs -0 -r npx markdownlint-cli2 --no-globs
```

Never lint a bare recursive glob: it descends into any independent Git repository checked out below this one.

Run the enabled checks before claiming completion.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:markdown-tooling -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:python-tooling -->
<!-- markdownlint-disable MD025 -->
# Python tooling

Use uv for environments and dependency changes. Ruff owns formatting, linting, and imports.
Use basedpyright in strict mode for type checking. Do not add a competing Python gate.

Run before claiming completion:

```bash
uv run ruff format --check src tests scripts
uv run ruff check src tests scripts
uv run basedpyright
uv run coverage run -m pytest
uv run coverage report
uv run pip-audit
```

When the gate reports formatting or lint findings, run:

```bash
uv run ruff format src tests scripts
uv run ruff check src tests scripts --fix
```
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:python-tooling -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:markdown-frontmatter -->
<!-- markdownlint-disable MD025 -->
# Markdown Frontmatter

Managed Markdown in this repository carries YAML frontmatter under the Markdown Frontmatter Standard: the eleven required fields in canonical order, every scalar quoted, and an id of the form `{doc_type}-{6-char base36 token}-{slug}`.

Create a new managed document with `scripts/new-doc-id --scaffold --doc-type <type> <name>` from the repo-local skill at `.agents/skills/markdown-frontmatter/`. Read that skill's `SKILL.md` before hand-authoring or repairing a frontmatter block.

The gate is `project-standards validate`.

`AGENTS.md`, `CLAUDE.md`, and anything under `.agents/**`, `.claude/**`, or `.codex/**` never carry frontmatter.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:markdown-frontmatter -->

<!-- prettier-ignore-end -->
