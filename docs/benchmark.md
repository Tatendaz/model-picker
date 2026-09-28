# Benchmark behind the defaults

The defaults and routes in `advisor.py` come from SWE-bench Verified runs on
2026-09-28 with Codex CLI 0.157 and 0.158 and Claude Code 2.1.283. Every patch
was graded with the official SWE-bench harness.

## Method

- **Task sets.** Dev: the 50 tasks of SWE-bench Verified mini (25 Django, 25
  Sphinx). Held-out: 50 other Verified tasks from the same two projects with
  the same difficulty mix. Confirmation: 50 more Verified tasks drawn across all
  of its repositories.
- **Rules fixed in advance.** Candidate settings and routing rules were chosen
  on the dev set and written down before any held-out or confirmation run.
- **Usage.** Each run's tokens were priced at API list prices, so every
  saving here is an API-cost estimate, not a measured plan-limit change.
  Neither vendor publishes how each model counts against the 5-hour and
  weekly limits. If they track API cost, the same percentage applies to both.
- **Isolation.** Each agent worked in its own checkout and ran tests in the
  task's Docker image with no network. Some Codex runs searched the disk for
  other checkouts during the dev sweep; those runs were discarded and rerun
  with a permission profile that denies reads outside the workspace, which
  every held-out and confirmation run used.

## Results

Solved tasks out of 50, and usage against the setting in the first row of
each block.

| Host | Setting | Dev | Held-out | Confirmation |
|---|---|---|---|---|
| Claude Code | Opus 5.5, xhigh effort | 49, baseline | 48, baseline | 48, baseline |
| Claude Code | **Opus 5.5, medium effort** | **50, 38% less** | **47, 44% less** | **48, 41% less** |
| Claude Code | Opus 5.5, low effort | 44, 59% less | 44, 57% less | not run |
| Claude Code | Sonnet 5, medium effort | 37, 36% more | not run | not run |
| Codex | Astra, high effort | 43, baseline | 42, baseline | 44, baseline |
| Codex | **JEV route: Terra high or Astra medium** | **41, 28% less** | **42, 32% less** | **43, 35% less** |
| Codex | Astra, medium effort | 42, 16% less | 42, 18% less | 43, 22% less |
| Codex | Terra, high effort | 38, 61% less | 37, 67% less | 40, 70% less |
| Codex | Terra, medium effort | 33, 71% less | not run | not run |

The confirmation set spans Django, SymPy, matplotlib, scikit-learn, xarray,
astropy, requests and pytest. On it, the 95% range of the Opus medium saving
was 33 to 49% and of the Codex route saving 27 to 43%, from a paired bootstrap
over tasks. Across all 150 tasks, Opus medium solved 145 against 145 at xhigh,
and the Codex route solved 126 against 129 at Astra high.

## What the picker does with this

- **Claude Code:** it recommends Opus 5.5 at medium effort. Sonnet 5 used 3.6
  times the tokens of Opus 5.5 on the same tasks and solved 12 fewer. Routing
  Opus down to low effort for tasks JEV rated easy lost 3 tasks on the
  held-out set, and routing up to xhigh added usage without solving more, so
  there is one route and no JEV call.
- **Codex:** JEV picks between Terra at high effort and Astra at medium effort
  for each task, escalating when it gives Astra at least a 0.5 probability.
  The rule was fixed before the held-out and confirmation runs. It gave up 3
  of 129 tasks for 28 to 35% less usage than Astra at high effort, against 2
  tasks for 16 to 22% with Astra at medium effort on every task.

## JEV rubrics

The original rubric described each model by task category ("everyday coding",
"complex debugging") and asked for the least expensive adequate pair. JEV
returned the host's baseline for all 50 dev tasks, including the 8 rated at an
hour or more, so it never suggested an upgrade. Rubrics that ask whether a
lower-cost setting is likely to fail rank the tasks that setting fails above
the ones it solves with an AUC near 0.8 for Opus at low effort and near 0.7 for
Terra and Astra.

## Limits

- 50 tasks per set, one run per task and setting, bug fixes only. Agent runs
  vary from run to run.
- Plan-limit weights per model are not published; API price is the proxy.
- The picker cannot switch models. It saves usage only when you act on a
  suggestion, and the turn that triggered it runs on your current setting.
