# Configuration

Model Picker works with no config file. To change a default, copy
[`config.example.json`](../plugins/codex-model-advisor/config.example.json) to
`~/.codex/model-advisor.json` and edit it. Keys you leave out keep their
defaults.

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
| `allowed_models` | all four models | Restricts suggestions, for example to the models your account offers. |

`allowed_models` maps a model to its allowed efforts. It can only narrow the
built-in list; an unknown model or effort makes every check fail:

```json
{
  "allowed_models": {
    "gpt-5.6-terra": ["medium", "high"],
    "gpt-5.6-sol": ["medium", "high"]
  }
}
```

The built-in list is `gpt-5.6-luna` (low, medium), `gpt-5.6-terra` (low,
medium, high), `gpt-5.6-sol` (medium, high) and `gpt-6-astra` (medium, high).

## Environment variables

| Variable | Effect |
|---|---|
| `TYPESAFE_API_KEY` | The API key, or whichever name `api_key_env` sets. |
| `CODEX_ADVISOR_CONFIG` | Path to the config file instead of `~/.codex/model-advisor.json`. |
| `CODEX_ADVISOR_STATE_DIR` | Directory for session state instead of `~/.codex/model-advisor-state`. |

## Suggested Codex defaults

Suggestions are upgrades from your current selection, so start from a mid
setting. In `~/.codex/config.toml`:

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
```

Existing threads and explicit app or profile selections can override these
defaults. The plugin never edits this file.

## Turn it off

- For one session: send `/advisor mute`.
- Everywhere: set `"enabled": false`, or disable the plugin in Codex.
- To remove it, see [Uninstall](../README.md#uninstall).
