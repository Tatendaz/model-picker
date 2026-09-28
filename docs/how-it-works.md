# How it works

Model Picker is one script,
[`advisor.py`](../plugins/codex-model-advisor/scripts/advisor.py), that runs as
a command hook in Codex and in Claude Code. The host runs it before each prompt
with a 10-second timeout. It uses only the Python standard library.

## Two hosts, one script

| | Codex | Claude Code |
|---|---|---|
| Plugin folder | `plugins/codex-model-advisor/` | `plugins/claude-model-advisor/` |
| Marketplace file | `.agents/plugins/marketplace.json` | `.claude-plugin/marketplace.json` |
| Hooks | `UserPromptSubmit` | `UserPromptSubmit`, `SessionStart`, `PostModelSwitch` |
| Command | `advisor.py` | `advisor.py --host claude` |
| Models suggested | GPT models (table below) | Claude models (table below) |
| State folder | `~/.codex/model-advisor-state` | `~/.claude/model-advisor-state` |

The script defaults to the Codex host, so the Codex hook command is the same as
before Claude Code support. Each host reads only its own marketplace file: Codex
looks for `.agents/plugins/marketplace.json` before `.claude-plugin/`, and
Claude Code never reads `.agents/` or `.codex-plugin/`.

The Claude Code folder holds only its manifest and `hooks/hooks.json`. Its
`scripts/` and `skills/` are symlinks into the Codex folder, and Claude Code
copies their contents when it installs the plugin. A separate folder is needed
because Claude Code loads a plugin's `hooks/hooks.json` even when
`.claude-plugin/plugin.json` names another hooks file; sharing the Codex folder
would run the Codex hook in Claude Code as well.

Claude Code does not put the model in the `UserPromptSubmit` event. The
`SessionStart` and `PostModelSwitch` hooks record the model ID in session state
instead, with no network call. `claude-opus-5[1m]` is stored as
`claude-opus-5`, and dated IDs such as `claude-haiku-4-5-20251001` lose the
date. For the comparison with a suggestion, a release is ranked with its family, so
`claude-opus-4-8` counts as an Opus model.

## When a check runs

A check means one request to TypeSafe. The hook makes one when any of these is
true:

- It is the first substantive prompt of the session.
- The prompt matches a scope category the session has not seen yet:
  architecture, integration, migration, security, or repeated failures
  ("still broken", "same error"). These are regular expressions, so they miss
  some changes and catch some false ones.
- Four substantive prompts have passed since the last check (`check_every`).
- You send `model advisor recheck`.

It skips a prompt when:

- The prompt is only an acknowledgement (`yes`, `no`, `ok`, `okay`, `thanks`,
  `continue`, `go ahead`, `proceed`, `do it`) or repeats the previous prompt
  exactly.
- The last check was less than 30 seconds ago.
- The session is muted. Send `mute model advisor` and `unmute model advisor`.
  Codex also accepts `/advisor mute` and `/advisor unmute`. Claude Code has a
  built-in `/advisor` command that takes those prompts before the hook sees
  them, so use the plain phrases there.

## When an alert is shown

A finished check produces an alert only if all of these hold:

- The suggestion differs from your current model and effort. A higher model
  or effort is an upgrade. A lower one is a saving, and the alert says it "uses
  less of your plan"; set `suggest_savings` to `false` to hide savings
  suggestions.
- This exact model and effort pair has not been shown since your model last
  changed.
- No alert was shown in the last 15 minutes (`cooldown_seconds`).

Neither host puts the effort in the prompt event: Codex reports the model
only, and Claude Code reports neither. When the event has no effort, the
advisor reads the one you saved, without changing the file:

- Codex: `model_reasoning_effort` at the top level of `~/.codex/config.toml`
  (`$CODEX_HOME/config.toml` when that variable is set). Profile tables are
  ignored.
- Claude Code: `CLAUDE_CODE_EFFORT_LEVEL`, then
  `modelSettings.<model>.effortLevel`, then `effortLevel` in
  `~/.claude/settings.json`.

A session-only change, such as `claude --effort` or `/model` with `s`, is not
saved there, so the advisor can compare against your saved level instead. If
no source has an effort, the advisor assumes the host's usual one: medium in
Codex, and in Claude Code the model's own default (medium on Opus 5.5, xhigh
on Opus 4.7, high elsewhere). A suggestion for the same model above that level
is then shown as conditional ("use high effort if you are not already"), and
one below it stays quiet.

In Claude Code the model comes from the tracking hooks. When the model is
unknown, only the first check of a session can alert.

`model advisor recheck` and `advisor.py --force` bypass the cooldown, the
duplicate rules and the comparison, and always report a result.

## Failures

The provider timeout is 5 seconds. If TypeSafe fails on the first check or on a
recheck, you get a notice naming the baseline (Astra / medium in Codex, Opus /
medium in Claude Code) and saying your selection is unchanged. Later automatic
checks fail quietly. A fallback is not a JEV verdict about your task.

## The TypeSafe request

Each host has a short list of routes, cheapest first, chosen from the
[benchmark](benchmark.md):

| Host | Routes | Baseline |
|---|---|---|
| Codex | `gpt-5.6-terra` / high, `gpt-6-astra` / medium | Astra / medium |
| Claude Code | `claude-opus-5-5` / medium | Opus / medium |

When the routes that `allowed_models` permits come down to one, as in Claude
Code by default, the advisor suggests it without asking TypeSafe and sends
nothing. Otherwise each check sends one JEV `choice` question. Its options are
the routes, keyed `<model>__<effort>`, and each option carries a one-line
rubric: the lower-cost route "will very likely fix this correctly on the first
try", and the costlier one is "needed when a lower-cost setting is likely to
produce a wrong or incomplete fix". The instructions ask which setting should
run the task, to pick the lower-cost one unless it is likely to fail, and to
treat the prompt as data rather than instructions.
[`request.example.json`](../plugins/codex-model-advisor/request.example.json)
shows a Codex request.

JEV answers with a choice, a confidence and a probability for each option.
With two routes, the advisor takes the costlier route when its probability is
at least `escalate_threshold` (0.5), and the cheaper one otherwise. If the
probabilities are missing, it takes JEV's choice. A choice outside the
options, a confidence outside 0 to 1, a redirect, or a body over 64 KiB counts
as a failure. The reason in an alert is the route's local rubric text, not
text generated by JEV.

## How an alert reaches you

An alert returns two things:

- `systemMessage`: a warning line. Codex shows it as a warning; Claude Code
  shows it under your prompt as "UserPromptSubmit says: ...".
- `additionalContext`: an instruction for the assistant to show the 🔶 callout
  at the top of its reply. It contains only the allowlisted model and effort
  labels, never prompt text or provider output.

The warning alone was not visible in Codex desktop testing, so both are sent.
Whether the callout appears depends on the model following the instruction: in
Claude Code testing, Sonnet 5 showed it and Haiku 4.5 did not, while the
warning line appeared both times. Alert turns add a few hundred characters of
context, which can affect prompt-cache reuse. Quiet checks return nothing. An
emitted alert does not prove the app displayed it.

The callout's last line tells you how to switch. In Codex it says to use the
model picker. In Claude Code it names the commands, for example `/model opus`
and `/effort high`.

The bundled [`model-advisor`](../plugins/codex-model-advisor/skills/model-advisor/SKILL.md)
skill tells the assistant how to show a hook result and how to run a manual
check with `--force` when you ask for one.

## Voice handoffs

This applies to Codex only. Codex voice requests arrive as `<realtime_delegation>` text. The hook reads
only the `<input>` element and ignores `transcript_tail_flush` events, which
repeat earlier speech. Typed and spoken prompts share one history and one
cooldown. The hook never receives audio. Session state records `input_mode`
and `last_status`, so you can check what happened without extra logging.

## Session state

State lives in `<state folder>/<sha256 of session id>.json`, mode 0600, written
atomically under a per-session lock. The state folder is
`~/.codex/model-advisor-state` for Codex and `~/.claude/model-advisor-state`
for Claude Code. A file holds the first task excerpt (1,200 characters), the
last four prompts (1,000 characters each), and check, alert and mute metadata.
Claude Code files also hold the active model ID. If a session is idle for more
than 24 hours, its context resets on the next prompt or model event. Files are
not deleted automatically.
