# Session: Benchmark-backed defaults and savings suggestions

**Branch:** feat/benchmark-defaults
**Date:** 2026-09-28

## Prompts

1. "Is there a way to measure how much Model Picker reduces usage? Maybe https://www.swebench.com/submit.html"
2. "OK, do 1 for me and let me know what usage savings one can expect to get, for Codex and for Claude (weekly and 5h)."
3. "Do option 1, test Opus medium as the Claude default. Can you optimize the setup so that we get the highest token and usage savings without losing quality? You can use the SWE-bench test and optimize."
4. "You can experiment with changing the model descriptions that get sent to JEV as well."
5. "OK, do 1 and 2."
6. "And also update Model Picker for Codex and Claude after merging it."

## Steps taken

Built a SWE-bench harness in a worktree on `bench/swebench-usage`: Codex and
Claude Code agents fix each task in a copy of the repository and run tests in
the task's Docker image through a file relay, and the official harness grades
the patches. Ran 200 agent runs on SWE-bench Verified mini, then a sweep of
seven more settings, then fixed candidate rules in a file and ran them on 50
held-out tasks and on a confirmation set of 50 tasks across all repositories.

Tested five JEV rubrics, including a picker-format one with rewritten model
descriptions, by asking JEV about every task and replaying its probabilities
against the graded results.

Found that some Codex runs searched the disk for other checkouts of the task;
added an audit, reran the affected runs under a read-deny permission profile,
and wrote a separate report for OpenAI.

Changed `advisor.py` (routes, savings alerts, saved-effort reading, smaller
JEV state), rewrote the affected tests and added eight, and updated the README
and every doc page that described the old baselines or rubric.

## Decisions

- Opus 5.5 at medium effort is the only Claude route. JEV routing to low
  effort looked free on the dev set but lost 3 tasks on the held-out set, and
  routing up to xhigh added usage without solving more.
- The rubric text sent to JEV is exactly the one the benchmark scored, and the
  JEV state holds only task text, as in the benchmark.
- Savings alerts are on by default, since the measured savings come from
  lowering the setting; `suggest_savings` turns them off.
- The saved effort is read from the host's own settings file, read-only,
  because neither host passes the effort to hooks.
