# Session: Open-source setup and README rewrite

## Request

"Can you do a full review of how this repo is set up, since it's open source
now? Also review the README and make sure it meets my standards for
open-source repos. For this, check how I usually like to set up other repos. I
think the README might be too long and lacking diagrams; use archify to
generate them where needed. Also check CI/CD."

## Changes

Surveyed claude-usage, codeandconfirm, promptups, yapui and mission-control
for the usual README shape, community files, workflows and repo settings, and
checked current README guidance online. Rewrote the README to that shape and
moved reference detail into four docs pages. Built two Archify diagrams, passed
showcase validation and the browser visual check, exported them, and split each
into light and dark SVGs. Replaced the CI workflow and added the PR gate,
Dependabot, templates and policy files copied from claude-usage and yapui.

## Decisions

- The Archify HTML viewers are not committed (about 700 KB each); the JSON
  sources regenerate them.
- Dependabot gets a `dependabot.yml` for GitHub Actions only. The other repos
  rely on security updates alone, but SHA pins need version updates to stay
  current.
- Repository settings (topics, private vulnerability reporting, Dependabot
  alerts, a protect-main ruleset, social preview) are left for the owner to
  approve.
