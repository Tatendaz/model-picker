# Feature: Supply-chain hardening

**Branch:** security/hardening-2026-10-25
**Date:** 2026-10-25

## Summary

Slower, safer dependency updates and a workflow security scan in CI.

## What changed

- `.github/dependabot.yml`: monthly instead of weekly, `cooldown: default-days: 7`,
  `open-pull-requests-limit: 3`, and the actions group limited to minor and patch
  updates. Security updates ignore the cooldown.
- `.github/workflows/zizmor.yml`: scans `.github/workflows` on every pull request targeting
  `main` and every push to `main`, fails on high findings or on a workflow it can't parse.
  The read-only token turns on online audits (impostor commits, known-vulnerable actions). zizmor 1.31.1 is installed from hash-pinned wheels
  (`.github/zizmor-requirements.txt`).
- `.github/workflows/merge-when-clean.yml` (shared template, unchanged): merges Dependabot
  PRs and the owner's `security/*` or `automerge`-labelled PRs once CI is green, a real
  review ran on the head (CodeRabbit "Review completed" or `review-failover` success) and
  0 threads are open. Merges made with `GITHUB_TOKEN` start no other workflows.
- `dependency-review.yml`: the pin comment now says `v5.0.0`, the tag the SHA points to.
- Removed `.github/workflows/dependabot-auto-merge.yml`: it merged Dependabot patch and minor
  PRs on green CI with no review. `merge-when-clean.yml` now covers Dependabot PRs, skips
  major updates, and requires a real review.

## Motivation

This month's malware shipped as new versions of trusted packages. A 7-day cooldown
keeps a hijacked release out until it has been caught. zizmor catches unpinned actions
and template injection before they merge.

## Not done

- No package-manager cooldown: the plugin has no package dependencies.
- Dependabot PRs are not added to a CodeRabbit ignore list: they need CodeRabbit's
  auto-review (or its rate-limit failover) so the merge job can merge them.
