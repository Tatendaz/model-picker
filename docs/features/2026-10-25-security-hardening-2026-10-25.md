# Feature: Supply-chain hardening

**Branch:** security/hardening-2026-10-25
**Date:** 2026-10-25

## Summary

Slower, safer dependency updates and a workflow security scan in CI.

## What changed

- `.github/dependabot.yml`: monthly instead of weekly, `cooldown: default-days: 7`,
  `open-pull-requests-limit: 3`, and the actions group limited to minor and patch
  updates. Security updates ignore the cooldown.
- `.github/workflows/zizmor.yml`: scans `.github/workflows` on every PR and push to
  `main`, fails on high findings. zizmor 1.31.1 is installed from hash-pinned wheels
  (`.github/zizmor-requirements.txt`).
- `.coderabbit.yaml`: skip automatic CodeRabbit reviews on Dependabot PRs
  (`inheritance: true` keeps the web UI settings).
- `dependency-review.yml`: the pin comment now says `v5.0.0`, the tag the SHA points to.

## Motivation

This month's malware shipped as new versions of trusted packages. A 7-day cooldown
keeps a hijacked release out until it has been caught. zizmor catches unpinned actions
and template injection before they merge.

## Not done

- No package-manager cooldown: the plugin has no package dependencies.
