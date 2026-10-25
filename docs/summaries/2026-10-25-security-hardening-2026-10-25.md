# Session: Supply-chain hardening

## Request

"After you finish the sweep for all your repos, read HARDENING.md and do it for each of
your repos: Dependabot config with 7-day cooldown, package-manager cooldown, CI lockdown
(npm ci, SHA pins, least permissions, zizmor job, gitleaks job on private repos)."

## Changes

- Checked each key first: `cooldown`, `default-days`, `open-pull-requests-limit`,
  `update-types` against the SchemaStore Dependabot schema, and
  `reviews.auto_review.ignore_usernames` against CodeRabbit's schema.v2.json.
- Validated the new `dependabot.yml` against the schema.
- Ran actionlint and zizmor 1.31.1 locally (zizmor exits 14 on a high finding, 0 here).
  actionlint caught a YAML error (`:all: ` read as a mapping) that zizmor skipped silently.
