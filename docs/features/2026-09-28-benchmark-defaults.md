# Feature: Benchmark-backed defaults and savings suggestions

**Branch:** feat/benchmark-defaults
**Date:** 2026-09-28

## Summary

The advisor now suggests the settings that solved as many SWE-bench tasks for
less usage: Opus 5.5 at medium effort in Claude Code, and in Codex either Terra
at high effort or Astra at medium effort, chosen per task by JEV. It also tells
you when your setting costs more than the task needs, not only when it needs
more.

## Motivation

A SWE-bench Verified run of the 0.2 advisor showed that it never changed a
choice: JEV returned the baseline for all 50 tasks. The Claude baseline,
Sonnet 5 at medium effort, cost 36% more than Opus 5.5 at xhigh on the same
tasks and solved 12 fewer. The owner's own defaults, Opus at xhigh and Astra at
high, could drop to medium effort with no measurable loss: 44% and 18% less
usage on 50 held-out tasks. The 0.2 advisor could not say so, because it only
showed upgrades. [docs/benchmark.md](../benchmark.md) has the numbers.

## What changed

- New baselines: Astra / medium (Codex) and Opus / medium (Claude Code).
- Each host has a list of routes. Codex asks JEV to choose between Terra / high
  and Astra / medium with rubrics about whether the lower-cost setting is
  likely to fail, and escalates when JEV gives Astra at least 0.5
  (`escalate_threshold`). Claude Code has one route, so it sends no request.
- Alerts now cover cheaper settings too, worded "uses less of your plan", and
  `suggest_savings: false` turns them off.
- When the host event has no effort, the advisor reads the saved one from
  `~/.codex/config.toml` or `~/.claude/settings.json`, read-only.
- JEV now receives only the task text: the latest prompt, the first task
  excerpt and the last four requests. The current model, effort and previous
  suggestion are no longer sent.
- The `uncertain` answer is gone; the routes are the only options.
- Both manifests move to 0.3.0.

## Notes

The Codex route and threshold were tuned on the dev set, confirmed on a
held-out set, and checked again on a confirmation set across all SWE-bench
repositories. The harness and raw results live on the
`bench/swebench-usage` branch and are not part of this PR. Update the plugin in
each host to pick up 0.3.0.
