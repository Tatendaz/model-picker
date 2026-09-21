<div align="center">

# 🔶 Model Picker

**Codex model and effort suggestions that follow your task as it grows.**

A Codex plugin. When a task gets harder, it asks TypeSafe's JEV model which
Codex model and reasoning effort fit the work, then shows the answer in chat.
You make the switch. The plugin never changes a setting.

[![CI](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml/badge.svg)](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE)
[![Python: stdlib only](https://img.shields.io/badge/python-3.9%2B%20·%20zero%20deps-3776AB.svg)](plugins/codex-model-advisor/scripts/advisor.py)
[![Codex plugin](https://img.shields.io/badge/Codex-plugin-10a37f.svg)](https://learn.chatgpt.com/docs/hooks)

</div>

A short summary stays on your current model with no notice. When the same
session turns into a multi-tenant architecture review, you see this at the top
of the reply:

> # 🔶 Model recommendation
>
> ---
>
> JEV recommends **gpt-6-astra / high**.
>
> Select it in the model picker if useful. **No settings were changed.**

## Install

You need macOS or Linux, Python 3.9 or later, Codex with plugin hooks, and a
[TypeSafe](https://docs.typesafe.ai/api) API key. TypeSafe bills the key
separately from your Codex plan.

1. Add the marketplace and install the plugin:

   ```sh
   codex plugin marketplace add Tatendaz/model-picker
   codex plugin add codex-model-advisor@model-picker
   ```

2. Give the hook your API key. Either export `TYPESAFE_API_KEY` in the
   environment Codex runs in, or on macOS store it in Keychain:

   ```sh
   security add-generic-password -a "$USER" -s jev-codex-api-key -w
   ```

3. Trust the hook. Open `/hooks` in the Codex CLI, review the
   `codex-model-advisor@model-picker` UserPromptSubmit command, and trust it.
   Installing the plugin does not do this for you.

4. Start a new task. The first real prompt triggers a check.

The plugin ID stays `codex-model-advisor` for compatibility; the display name
is Model Picker. If you ran an older personal copy, disable it first so the
hook does not run twice.

## Use it

| Send this as a prompt | What happens |
|---|---|
| `model advisor recheck` | Reassesses your last request now and always shows the result. |
| `/advisor mute` | Silences alerts for this session. |
| `/advisor unmute` | Turns alerts back on. |

These are phrases the hook reads, not native Codex slash commands.

## How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/how-it-works-dark.svg">
  <img src="docs/diagrams/how-it-works-light.svg" width="100%" alt="Sequence: you send a prompt; Codex passes the event to advisor.py; advisor.py reads session state and the API key, sends a bounded snapshot to TypeSafe JEV, saves the result, and returns a warning plus a chat callout. You switch models yourself.">
</picture>

The hook checks your first real prompt, any prompt that brings a new kind of
scope (architecture, integration, migration, security, repeated failures), and
every fourth prompt. It stays quiet for replies such as "ok", repeated prompts,
prompts within 30 seconds of a check, and suggestions that are not an upgrade.
Each suggestion is shown once, and never more than one alert per 15 minutes.

The hook does not block your prompt. After the check (5-second provider
timeout) the turn runs on the model you selected, so a suggestion applies to
your next turn, or you can stop and resend.
[docs/how-it-works.md](docs/how-it-works.md) has the full rules.

## What leaves your machine

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/data-flow-dark.svg">
  <img src="docs/diagrams/data-flow-light.svg" width="100%" alt="Data flow: your prompt and API key enter advisor.py. It writes bounded excerpts to local session state, sends a bounded snapshot over HTTPS to TypeSafe JEV, and shows only an allowlisted model and effort label in Codex chat.">
</picture>

- **Sent to TypeSafe on each check:** your latest prompt (up to 3,000
  characters), the first task excerpt, the last four requests, the current
  model and effort, and the previous suggestion. It goes to `api.typesafe.ai`
  under your key and TypeSafe's terms.
- **Kept locally:** session files in `~/.codex/model-advisor-state`, mode
  0600. Context resets after 24 hours idle; delete the folder to erase it.
- **Never read:** your source files or the full transcript. No telemetry.
- **Off switch:** set `"enabled": false` in `~/.codex/model-advisor.json`, or
  disable the plugin.

Details: [docs/privacy.md](docs/privacy.md).

## Limits

- It cannot switch models for you. Codex's `UserPromptSubmit` hook has no
  output field that changes the model or effort. [Why](docs/limitations.md).
- Native Windows is not supported; the state lock uses `fcntl`.
- Suggestions come from a classifier and can be wrong. Your selection always
  decides which model runs.

## Documentation

| Page | Covers |
|---|---|
| [How it works](docs/how-it-works.md) | When checks run, alert rules, the TypeSafe request, voice handoffs |
| [Configuration](docs/configuration.md) | Config keys, environment variables, suggested Codex defaults |
| [Privacy and trust](docs/privacy.md) | Data sent, local state, hook trust, credentials |
| [Limitations](docs/limitations.md) | Automatic switching, what has been verified |
| [Diagrams](docs/diagrams/README.md) | Diagram sources and how to regenerate them |
| [Roadmap](ROADMAP.md) | Planned work |

## Uninstall

Disable or uninstall the plugin in Codex, then remove its local files:

```sh
rm -rf ~/.codex/model-advisor-state ~/.codex/model-advisor.json
security delete-generic-password -s jev-codex-api-key   # macOS, if you used Keychain
```

The plugin never edits other hooks or your Codex config.

## Contributing

`make test` runs the suite. It needs no network, key, or dependencies. See
[CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

MIT © Tatenda Zhou. Not affiliated with OpenAI or TypeSafe.
