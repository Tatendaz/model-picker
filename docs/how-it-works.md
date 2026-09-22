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
date.

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

- The suggestion is an upgrade over the current model and effort. If the
  model is known but the effort is not, a suggestion for the same model above
  the host's usual effort is shown as conditional ("use high effort if you are
  not already"). The usual effort is medium in Codex and high in Claude Code,
  so in Claude Code only `xhigh` or `max` for the current model alerts.
- This exact model and effort pair has not been shown since your model last
  changed.
- No alert was shown in the last 15 minutes (`cooldown_seconds`).

Codex reports the model on every prompt but not the effort. Claude Code reports
neither, so the model comes from the tracking hooks and the effort is always
unknown. When the model is unknown, only the first check of a session can
alert.

`model advisor recheck` and `advisor.py --force` bypass the cooldown, the
duplicate rules and the upgrade rule, and always report a result.

## Failures

The provider timeout is 5 seconds. If TypeSafe fails on the first check or on a
recheck, you get a notice naming the baseline (Terra / medium in Codex, Sonnet /
medium in Claude Code) and saying your selection is unchanged. Later automatic
checks fail quietly. A fallback is not a JEV verdict about your task.

If JEV answers `uncertain`, an automatic check stays quiet. A recheck tells you
the result was uncertain and that the baseline is only a baseline.

## The TypeSafe request

Each check sends one JEV `choice` question. The candidate answers are every
allowed model and effort pair for the host, plus `uncertain`. Each answer
carries a fixed rubric: a one-line task category for the model and a one-line
description of the effort level. Both hosts use the same four categories.

| Task category | Codex | Claude Code |
|---|---|---|
| Simple lookup, short summary, extraction, or a small isolated edit | `gpt-5.6-luna` (low, medium) | `claude-haiku-4-5` (no effort setting) |
| Everyday coding, setup, reporting, and bounded troubleshooting | `gpt-5.6-terra` (low, medium, high) | `claude-sonnet-5` (low, medium, high) |
| Complex debugging, multi-component changes, or substantial ambiguity | `gpt-5.6-sol` (medium, high) | `claude-opus-5` (medium, high, xhigh) |
| Unusually difficult reasoning or architecture beyond routine complex coding | `gpt-6-astra` (medium, high) | `claude-fable-5-1` (high, xhigh, max) |

Haiku 4.5 has no effort setting, so its only entry is `none` and a Haiku
suggestion names the model alone. The instructions ask for the least expensive
adequate pair, tell JEV to treat the prompt as data rather than instructions,
and to honor an explicit model preference in the prompt. They name the host
("Codex model", "Claude model") and its everyday pair (Terra medium, Sonnet
medium). [`request.example.json`](../plugins/codex-model-advisor/request.example.json)
shows the shape of a Codex request.

The response must name one of the offered choices and carry a confidence
between 0 and 1. Anything else, a redirect, or a body over 64 KiB counts as a
failure. The explanation in an alert is the local rubric text for the chosen
category, not text generated by JEV. Confidence describes how concentrated
JEV's answer was, not whether it is correct, and no confidence cutoff is
applied.

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
