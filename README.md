<div align="center">

<h1><picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/brand/lockup-dark.png">
  <img src="assets/brand/lockup-light.png" width="380" alt="Model Picker">
</picture></h1>

**Model and effort suggestions for Codex and Claude Code that follow your task as it grows.**

When a task gets harder, it asks TypeSafe's JEV model which of your host's models and
effort levels fit the work, then shows the answer in chat. You make the switch; the plugin never changes a setting.

[![CI](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml/badge.svg)](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE) [![Python: stdlib only](https://img.shields.io/badge/python-3.9%2B%20·%20zero%20deps-3776AB.svg)](plugins/codex-model-advisor/scripts/advisor.py) [![Codex plugin](https://img.shields.io/badge/Codex-plugin-10a37f.svg)](https://learn.chatgpt.com/docs/hooks) [![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757.svg)](https://code.claude.com/docs/en/plugins)

</div>

A short summary stays on your current model with no notice. When the session turns into a
multi-tenant architecture review, the reply starts with this (Claude Code names Claude models and `/model` and `/effort`):

> # 🔶 Model recommendation
>
> ---
>
> JEV recommends **gpt-6-astra / high**.
>
> Select it in the model picker if useful. **No settings were changed.**

## Install

You need macOS or Linux, Python 3.9 or later, and a
[TypeSafe](https://docs.typesafe.ai/api) API key, billed separately from your
Codex or Claude plan. Both hosts read the same key: export `TYPESAFE_API_KEY`
where the host runs, or on macOS store it in Keychain:

```sh
security add-generic-password -a "$USER" -s jev-codex-api-key -w
```

Then add the plugin to your host:

```sh
# Codex (with plugin hooks), in a terminal
codex plugin marketplace add Tatendaz/model-picker
codex plugin add codex-model-advisor@model-picker

# Claude Code (2.1.257 or later), inside a session
/plugin marketplace add Tatendaz/model-picker
/plugin install claude-model-advisor@model-picker
```

Codex runs the hook only after you trust it: open `/hooks` in the Codex CLI and
trust the `codex-model-advisor@model-picker` command. Claude Code needs no such
step. Start a new session in either host; its first real prompt runs a check.

Or paste this to Claude Code or Codex and let it do the install:

> Install the Model Picker plugin from github.com/Tatendaz/model-picker. Add the
> marketplace, install the plugin for this host, then tell me how to store my
> TypeSafe API key and, in Codex, how to trust the hook.

## Use it

| Send as a prompt | What happens |
|---|---|
| `model advisor recheck` | Reassesses your last request now and always shows the result. |
| `mute model advisor` | Silences alerts for this session. |
| `unmute model advisor` | Turns alerts back on. |

## How it works

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/how-it-works-dark.svg">
  <img src="docs/diagrams/how-it-works-light.svg" width="100%" alt="Sequence: you send a prompt; Codex or Claude Code passes the event to advisor.py; advisor.py reads session state and the API key, sends a bounded snapshot to TypeSafe JEV, saves the result, and returns a warning plus a chat callout. You switch models yourself.">
</picture>

The hook checks your first real prompt, any prompt that brings a new kind of
scope (architecture, integration, migration, security, repeated failures), and
every fourth prompt. It stays quiet for replies such as "ok", repeats, prompts
within 30 seconds of a check, and suggestions that are not an upgrade. Each
suggestion shows once, and at most one alert every 15 minutes.

It never blocks your prompt: after the check (5-second timeout) the turn runs on
the model you selected, so a suggestion applies to your next turn. In Claude
Code, two local hooks track your active model. [Full rules](docs/how-it-works.md).

## What leaves your machine

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/data-flow-dark.svg">
  <img src="docs/diagrams/data-flow-light.svg" width="100%" alt="Data flow: your prompt and API key enter advisor.py. It writes bounded excerpts to local session state, sends a bounded snapshot with your API key over HTTPS to TypeSafe JEV, and shows only an allowlisted model and effort label in chat.">
</picture>

- **Sent to `api.typesafe.ai` on each check, under your key:** the latest prompt
  (3,000 characters), the first task excerpt, the last four requests, your model and effort, and the previous suggestion.
- **Kept locally:** session files, mode 0600, in `~/.codex` or `~/.claude`.
- **Never read:** your source files or the full transcript. No telemetry.
- **Off switch:** `"enabled": false` in the host's `model-advisor.json`.
  [Privacy details](docs/privacy.md).

## Limits

No host lets this hook switch models: `UserPromptSubmit` has no model or effort output
([why](docs/limitations.md)). Claude Code does not tell hooks your effort level. No native Windows.
Suggestions come from a classifier and can be wrong.

## Documentation

| Page | Covers |
|---|---|
| [How it works](docs/how-it-works.md) | Check rules, alert rules, the TypeSafe request, both hosts |
| [Configuration](docs/configuration.md) | Config keys, environment variables, host defaults, uninstall |
| [Privacy and trust](docs/privacy.md) | Data sent, local state, hook trust, credentials |
| [Limitations](docs/limitations.md) | Automatic switching, what has been verified |
| [Brand assets](assets/brand/README.md) | Logo files, colour, clearspace, how to redraw them |

To uninstall, disable the plugin and delete the files in [Configuration](docs/configuration.md#uninstall).
`make test` runs the suite with no network or key. [Diagram sources](docs/diagrams/README.md).

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Roadmap](ROADMAP.md) ·
MIT © Tatenda Zhou · Not affiliated with OpenAI, Anthropic or TypeSafe.
