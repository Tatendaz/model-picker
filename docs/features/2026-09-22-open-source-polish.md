# Feature: Open-source setup and README rewrite

The README drops from 171 lines and about 1,380 words to 120 lines and about
700: what the plugin does, an example callout, install, the three prompt
commands, two diagrams, a short data disclosure, limits, and a documentation
table.
Detail moved into `docs/how-it-works.md`, `docs/configuration.md`,
`docs/privacy.md` and `docs/limitations.md`, rewritten against the current
`advisor.py`. Two Archify diagrams (a sequence of one check, and a data-flow
map of what is stored and sent) ship as light and dark SVGs chosen with
`<picture>`, with sources and regeneration steps in `docs/diagrams/`.

CI follows the setup of the maintainer's other public repos. `tests.yml` became
`ci.yml`: actions pinned to full SHAs on current Node 24 releases (the old
`@v4`/`@v5` tags raised the Node 20 deprecation warning), push runs only on
`main`, a concurrency group, `persist-credentials: false`, Python 3.9 to 3.14 on
Linux plus 3.9 and 3.14 on macOS, and a lint job (ruff, stdlib-only import
check, manifest validation). New: `pr-gate.yml` (dated docs entries, new code
has new tests), Dependabot for GitHub Actions with the auto-merge and
dependency-review workflows, CODEOWNERS, issue forms, a PR template, a Code of
Conduct, and a fuller SECURITY.md. Four one-line compound statements in the
tests were split so ruff passes; behaviour is unchanged.
