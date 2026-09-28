# Feature: Lighter suggestion on the first check

**Branch:** feat/first-check-lighter-suggestion
**Date:** 2026-09-29

## Summary

The first check of a session can now suggest a lighter model or effort, not
only an upgrade. Later checks stay upgrade-only. Version 0.3.0.

## Motivation

Until now every automatic alert was an upgrade. A session that started on Opus
5.5 or Astra for a short summary got no notice, even when JEV picked a smaller
model, so the plugin could not help anyone who starts every thread on the
biggest setting. The launch video already shows this case.

## What changed

- `advisor.py`: on the first check, a suggestion below the current model, or
  below a reported effort on the same model, shows as an alert with the line
  "This task looks lighter than your current setting." A lower effort is never
  inferred from an unknown one.
- A lighter alert does not start the 15-minute cooldown, so an upgrade soon
  after still shows.
- New config key `suggest_lower` (default `true`). `false` keeps every
  automatic alert an upgrade.
- `model advisor recheck` also shows the lighter line when it applies.
- Tests: first-check lighter alert, later checks stay quiet, opt-out, cooldown
  left open for upgrades, and an Opus 5.5 `[1m]` session that gets a Sonnet
  suggestion. Three older tests now expect the first-check alert.
- Docs: README, how it works, configuration, roadmap, example config.
- Both plugin manifests: 0.2.0 to 0.3.0, so `/plugin update` picks this up.

## Notes

Opus 5.5 support was already in 0.2.0 (`claude-opus-5-5`, alias `opus`,
default effort medium). Installs still on 0.1.0 know only `claude-opus-5` and
treat an Opus 5.5 session as an unknown model; update the plugin.

The README "How it works" diagram still says "No upgrade" under "When it stays
quiet". Its Archify source was not regenerated in this change.
