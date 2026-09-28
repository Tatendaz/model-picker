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
- **Usage.** Each run's tokens were priced at API list prices. Neither vendor
  publishes how each model counts against plan limits, so API price stands in
  for plan usage. The same percentage then applies to the 5-hour and the
  weekly limit, because both count the same usage.
- **Isolation.** Each agent worked in its own checkout and ran tests in the
  task's Docker image with no network. Some Codex runs searched the disk for
  other checkouts during the dev sweep; those runs were discarded and rerun
  with a permission profile that denies reads outside the workspace, which
  every held-out and confirmation run used.

## Results

Solved tasks out of 50, and usage against the setting in the first row of
each block.

| Host | Setting | Dev | Held-out |
|---|---|---|---|
| Claude Code | Opus 5.5, xhigh effort | 49, baseline | 48, baseline |
| Claude Code | **Opus 5.5, medium effort** | **50, 38% less** | **47, 44% less** |
| Claude Code | Opus 5.5, low effort | 44, 59% less | 44, 57% less |
| Claude Code | Sonnet 5, medium effort | 37, 36% more | not run |
| Codex | Astra, high effort | 43, baseline | 42, baseline |
| Codex | **Astra, medium effort** | **42, 16% less** | **42, 18% less** |
| Codex | Terra, high effort | 38, 61% less | 37, 67% less |
| Codex | Terra, medium effort | 33, 71% less | not run |

On the held-out set the 95% range of the Opus medium saving was 35 to 53%, and
of the Astra medium saving 10 to 25%, from a paired bootstrap over tasks.

## What the picker does with this

- **Claude Code:** it recommends Opus 5.5 at medium effort. Sonnet 5 used 3.6
  times the tokens of Opus 5.5 on the same tasks and solved 12 fewer. Routing
  Opus down to low effort for tasks JEV rated easy lost 3 tasks on the
  held-out set, and routing up to xhigh added usage without solving more, so
  there is one route and no JEV call.
- **Codex:** JEV picks between Terra at high effort and Astra at medium effort
  for each task, escalating when it gives Astra at least a 0.5 probability.
  Tuned on the dev set, this solved 41 dev and 42 held-out tasks at 28 and 32%
  less usage than Astra at high effort.

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
