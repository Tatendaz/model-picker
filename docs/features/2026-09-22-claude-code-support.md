# Feature: Claude Code support

**Branch:** feat/claude-code-support
**Date:** 2026-09-22

## Summary

Model Picker now also runs in Claude Code. It suggests Claude models and effort
levels (`claude-haiku-4-5`, `claude-sonnet-5`, `claude-opus-5`,
`claude-fable-5-1`) and tells you to switch with `/model` and `/effort`. Codex
behaviour does not change: the Codex hook file is byte-for-byte the same, and
the Codex path of `advisor.py` produces the same output, provider requests and
state as before.

## Motivation

The owner asked for the plugin to work in Claude Code for Anthropic models
without breaking Codex. Both hosts run command hooks on `UserPromptSubmit`, so
the same script can serve both if it knows which host called it.

## What changed

- `advisor.py` has a `HOSTS` table with a Codex and a Claude Code profile:
  models and efforts, rubric text, baseline, config and state paths, and callout
  wording. `--host claude` selects the Claude profile; the default stays
  `codex`.
- New plugin folder `plugins/claude-model-advisor/` with
  `.claude-plugin/plugin.json` and `hooks/hooks.json`. Its `scripts/` and
  `skills/` are symlinks into `plugins/codex-model-advisor/`.
- New root `.claude-plugin/marketplace.json` (marketplace `model-picker`,
  plugin `claude-model-advisor`).
- Claude Code runs three hooks, all with `--host claude`: `UserPromptSubmit`
  for checks, plus `SessionStart` and `PostModelSwitch`, which record the active
  model ID in session state with no network call.
- Claude Code state and config live in `~/.claude/model-advisor-state` and
  `~/.claude/model-advisor.json`, with `CLAUDE_ADVISOR_STATE_DIR` and
  `CLAUDE_ADVISOR_CONFIG` overrides. Same hashing, locking and mode 0600.
- The Claude callout reads "Switch with `/model opus` and `/effort high` if
  useful." Mute hints use `mute model advisor`, because Claude Code has a
  built-in `/advisor` command.
- When the effort is unknown, Claude Code assumes `high` (its default for
  Sonnet, Opus and Fable), so only `xhigh` or `max` for the current model
  produces a conditional alert. Codex keeps `medium`.
- `SKILL.md` covers both hosts. CI's manifest check now also validates the
  Claude marketplace, manifest and hooks, and fails if a Claude hook lacks
  `--host claude` or a Codex hook has any `--host`.
- 15 new tests. The 24 existing tests are unchanged.
- README, how-it-works, configuration, privacy, limitations, CONTRIBUTING,
  SECURITY, the issue and PR templates, the roadmap, and both diagrams
  (regenerated with Archify, light and dark) cover both hosts.

## Notes

The brief proposed a second hooks file inside the Codex plugin folder, named
from `.claude-plugin/plugin.json`, on the understanding that this replaces
`hooks/hooks.json`. Tested in Claude Code 2.1.278, it does not: Claude Code
loaded both files and ran both commands on every prompt, so the Codex hook would
also have run in Claude Code with the Codex rubric. The Claude plugin therefore
has its own folder, with symlinks so there is still one copy of the script and
skill. Claude Code dereferences symlinks that point elsewhere in the same
marketplace when it installs a plugin, and a local marketplace install in an
isolated config directory confirmed that.

Facts checked against real payloads captured from Claude Code 2.1.278 with a
throwaway hook and synthetic prompts:

- `UserPromptSubmit` has no `model` and no `effort` field, although one docs
  page shows both. The hooks reference agrees with the capture.
- `SessionStart` has `model` in interactive sessions and not in `claude -p`.
- `PostModelSwitch` has `from_model` and `to_model`, for example
  `claude-opus-5[1m]` and `claude-haiku-4-5-20251001`. The script strips the
  bracket suffix and the date.
- No hook fires on `/effort`, and hooks do not get `CLAUDE_EFFORT`.
- Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for plugin hooks
  (from the openai/codex source), so the host comes from the explicit flag, not
  the environment.
- Codex reads `.agents/plugins/marketplace.json` before
  `.claude-plugin/marketplace.json`, and `.codex-plugin/plugin.json` before
  `.claude-plugin/plugin.json`, so the new files do not change what Codex
  installs. Codex hook trust hashes the hook's command, timeout and status
  message, not the script, so Codex users do not need to trust the hook again.

State for Claude Code is under `~/.claude`, not `CLAUDE_PLUGIN_DATA` as the
brief suggested, because the skill's manual `--force` run happens outside a
hook, does not get that variable, and has to find the same session file.

`/model <alias>` and `/effort <level>` in Claude Code save the choice as the
default for new sessions. The docs point to the picker's session-only option.

To check Codex parity, the original and new `advisor.py` were run side by side
on 1,500 random prompt sequences (models, efforts, provider results, rechecks,
mutes, voice handoffs, config variants) and 70 provider-request cases. Outputs,
request bytes and state files matched in every case.
