<div align="center">

# 🔶 Model Picker

**Model and effort suggestions for Codex and Claude Code that follow your task as it grows.**

It suggests the setting that solved as many SWE-bench tasks for less usage,
and asks TypeSafe's JEV model when a Codex task needs the stronger one. It
tells you when your setting costs more than the task needs, and when it needs
more. You make the switch; the plugin never changes a setting.

[![CI](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml/badge.svg)](https://github.com/Tatendaz/model-picker/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-111111.svg)](LICENSE) [![Python: stdlib only](https://img.shields.io/badge/python-3.9%2B%20·%20zero%20deps-3776AB.svg)](plugins/codex-model-advisor/scripts/advisor.py)
[![Codex plugin](https://img.shields.io/badge/Codex-plugin-10a37f.svg)](https://learn.chatgpt.com/docs/hooks) [![Claude Code plugin](https://img.shields.io/badge/Claude%20Code-plugin-D97757.svg)](https://code.claude.com/docs/en/plugins)

</div>

If you run Opus 5.5 at xhigh effort in Claude Code, the first reply of a
session starts with this (in Codex it names GPT models and the model picker):

> # 🔶 Model recommendation
>
> ---
>
> Model Picker recommends **claude-opus-5-5 / medium** to save usage.
>
> Switch with `/model opus` and `/effort medium` if useful. **No settings were changed.**

In the [benchmark](docs/benchmark.md), Opus 5.5 at medium effort solved 47 of
50 held-out tasks against 48 at xhigh, for 44% less usage. In Codex, Astra at
medium effort matched Astra at high effort for 18% less.

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
within 30 seconds of a check, and suggestions that match your current setting.
Each suggestion shows once, and at most one alert every 15 minutes.

It never blocks your prompt: after the check (5-second timeout) the turn runs on
the model you selected, so a suggestion applies to your next turn. In Claude
Code, two local hooks track your active model. [Full rules](docs/how-it-works.md).

## What leaves your machine

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/data-flow-dark.svg">
  <img src="docs/diagrams/data-flow-light.svg" width="100%" alt="Data flow: your prompt and API key enter advisor.py. It writes bounded excerpts to local session state, sends a bounded snapshot with your API key over HTTPS to TypeSafe JEV, and shows only an allowlisted model and effort label in chat.">
</picture>

- **Sent to `api.typesafe.ai` on each Codex check, under your key:** the latest
  prompt (3,000 characters), the first task excerpt and the last four requests.
  Claude Code checks send nothing: it has one route.
- **Read locally:** the effort you saved in the host's settings, to compare.
- **Kept locally:** session files, mode 0600, in `~/.codex` or `~/.claude`.
- **Never read:** your source files or the full transcript. No telemetry.
- **Off switch:** `"enabled": false` in the host's `model-advisor.json`.
  [Privacy details](docs/privacy.md).

## Limits

No host lets this hook switch models: `UserPromptSubmit` has no model or effort
output ([why](docs/limitations.md)). Neither host tells hooks your effort, so
the advisor reads the level you saved. No native Windows. Suggestions rest on
150 benchmark tasks and a classifier, and can be wrong for your work.

## Documentation

| Page | Covers |
|---|---|
| [How it works](docs/how-it-works.md) | Check rules, alert rules, the TypeSafe request, both hosts |
| [Configuration](docs/configuration.md) | Config keys, environment variables, host defaults, uninstall |
| [Privacy and trust](docs/privacy.md) | Data sent, local state, hook trust, credentials |
| [Limitations](docs/limitations.md) | Automatic switching, what has been verified |
| [Benchmark](docs/benchmark.md) | The SWE-bench runs behind the defaults and routes |

To uninstall, disable the plugin and delete the files in
[Configuration](docs/configuration.md#uninstall). `make test` runs the suite with
no network or key. [Diagram sources](docs/diagrams/README.md).

[Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [Roadmap](ROADMAP.md) ·
MIT © Tatenda Zhou · Not affiliated with OpenAI, Anthropic or TypeSafe.
