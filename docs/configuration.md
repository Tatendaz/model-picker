# Configuration

Model Picker works with no config file. To change a default, copy
[`config.example.json`](../plugins/codex-model-advisor/config.example.json) to
`~/.codex/model-advisor.json` for Codex or `~/.claude/model-advisor.json` for
Claude Code, and edit it. Each host reads only its own file. Keys you leave out
keep their defaults.

## Config keys

| Key | Default | Notes |
|---|---|---|
| `enabled` | `true` | `false` turns the hook into a no-op. |
| `endpoint` | `https://api.typesafe.ai/v1/systemone` | Must be HTTPS with no user or password in the URL. |
| `model` | `jev-latest` | TypeSafe model name. |
| `api_key_env` | `TYPESAFE_API_KEY` | Environment variable the key is read from. |
| `keychain_service` | `jev-codex-api-key` | macOS Keychain service, tried when the variable is unset. The account is your login name. |
| `max_prompt_chars` | `6000` | Cap on the latest prompt sent, clamped to 1 to 12,000. The hook already cuts the prompt to 3,000 characters, so only values below 3,000 change anything. |
| `check_every` | `4` | Periodic check interval, in substantive prompts. Minimum 1. |
| `cooldown_seconds` | `900` | Minimum gap between alerts. `0` disables the cooldown. |
| `allowed_models` | the host's four models | Restricts suggestions, for example to the models your account offers. |

`allowed_models` maps a model to its allowed efforts. It can only narrow the
host's built-in list; an unknown model or effort makes every check fail:

```json
{
  "allowed_models": {
    "gpt-5.6-terra": ["medium", "high"],
    "gpt-5.6-sol": ["medium", "high"]
  }
}
```

The Codex list is `gpt-5.6-luna` (low, medium), `gpt-5.6-terra` (low, medium,
high), `gpt-5.6-sol` (medium, high) and `gpt-6-astra` (medium, high).

The Claude Code list is `claude-haiku-4-5` (none), `claude-sonnet-5` (low,
medium, high), `claude-opus-5` (medium, high, xhigh) and `claude-fable-5-1`
(high, xhigh, max). Haiku has no effort setting, so write its entry as
`"claude-haiku-4-5": ["none"]`.

## Environment variables

| Variable | Effect |
|---|---|
| `TYPESAFE_API_KEY` | The API key, or whichever name `api_key_env` sets. |
| `CODEX_ADVISOR_CONFIG` | Path to the Codex config file instead of `~/.codex/model-advisor.json`. |
| `CODEX_ADVISOR_STATE_DIR` | Directory for Codex session state instead of `~/.codex/model-advisor-state`. |
| `CLAUDE_ADVISOR_CONFIG` | Path to the Claude Code config file instead of `~/.claude/model-advisor.json`. |
| `CLAUDE_ADVISOR_STATE_DIR` | Directory for Claude Code session state instead of `~/.claude/model-advisor-state`. |

Claude Code state does not go in `CLAUDE_PLUGIN_DATA`, because a manual
`--force` run from the skill does not get that variable, and both runs must
share one session file.

## Suggested Codex defaults

Suggestions are upgrades from your current selection, so start from a mid
setting. In `~/.codex/config.toml`:

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
```

Existing threads and explicit app or profile selections can override these
defaults. The plugin never edits this file.

## Switching in Claude Code

Claude Code runs Sonnet, Opus and Fable at high effort unless you set another
default. Hooks cannot see the effort, so the advisor assumes high. `/model opus` and
`/effort high` also save the choice as your default for new sessions. To
change only the current session, open `/model` with no argument, pick a model
and press `s`, or start Claude Code with `--model` and `--effort`.

## Plugin ID

The Codex marketplace entry is `codex-model-advisor@model-picker`. The plugin
ID stayed `codex-model-advisor` for compatibility with earlier installs; the
display name is Model Picker. If you ran an older personal copy, disable it
before enabling this one, or the hook runs twice on every prompt.

The Claude Code entry is `claude-model-advisor@model-picker`. Install it only
in Claude Code; Codex does not list it, because Codex reads
`.agents/plugins/marketplace.json` first.

## Turn it off

- For one session: send `mute model advisor` (Codex also accepts
  `/advisor mute`).
- Everywhere in one host: set `"enabled": false` in that host's config, or
  disable the plugin there. In Claude Code, `enabled: false` also stops the
  model-tracking hooks from writing state.

## Uninstall

Disable or uninstall the plugin in each host, then remove its local files:

```sh
rm -rf ~/.codex/model-advisor-state ~/.codex/model-advisor.json      # Codex
rm -rf ~/.claude/model-advisor-state ~/.claude/model-advisor.json    # Claude Code
security delete-generic-password -s jev-codex-api-key   # macOS, if you used Keychain
```

In Claude Code, `/plugin uninstall claude-model-advisor@model-picker` removes
the plugin and `/plugin marketplace remove model-picker` removes the
marketplace. The plugin never edits other hooks or either host's config, so
nothing else needs undoing.
