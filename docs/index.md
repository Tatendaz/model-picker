# Model Picker

**Model and effort suggestions for Codex and Claude Code that follow your task as it grows.** It asks TypeSafe's JEV model which model and effort fit the work, then tells you in chat. It never changes a setting.

[View on GitHub](https://github.com/Tatendaz/model-picker) [Install](#install)

When a Codex session turns into a multi-tenant architecture review, the reply starts with this:

> # 🔶 Model recommendation
>
> ---
>
> JEV recommends **gpt-6-astra / high**.
>
> Select it in the model picker if useful. **No settings were changed.**

## Who it is for

People who use Codex or Claude Code and keep one model selected for every kind of task. Start a short summary on a big model and the first check can point you to a lighter one. When the same session grows into an architecture review, it points you to a stronger one.

In Claude Code the callout names Claude models and the `/model` and `/effort` commands. You make the switch yourself.

## Install

You need macOS or Linux, Python 3.9 or later, and a [TypeSafe](https://docs.typesafe.ai/api) API key, billed separately from your Codex or Claude plan. Both hosts read the same key: export `TYPESAFE_API_KEY` where the host runs, or on macOS store it in Keychain:

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

Codex runs the hook only after you trust it: open `/hooks` in the Codex CLI and trust the `codex-model-advisor@model-picker` command. Claude Code needs no such step. Start a new session in either host; its first real prompt runs a check.

Or paste this to Claude Code or Codex and let it do the install:

```text
Install the Model Picker plugin from github.com/Tatendaz/model-picker. Add the marketplace, install the plugin for this host, then tell me how to store my TypeSafe API key and, in Codex, how to trust the hook.
```

## Use it

Checks run on their own. Three prompts change what happens:

| Send as a prompt | What happens |
|---|---|
| `model advisor recheck` | Reassesses your last request now and always shows the result. |
| `mute model advisor` | Silences alerts for this session. |
| `unmute model advisor` | Turns alerts back on. |

## How it works

One stdlib-only Python script, `advisor.py`, runs as a hook before each prompt in both hosts.

![Sequence: you send a prompt; Codex or Claude Code passes the event to advisor.py; advisor.py reads session state and the API key, sends a bounded snapshot to TypeSafe JEV, saves the result, and returns a warning plus a chat callout. You switch models yourself.](https://tatendaz.github.io/model-picker/diagrams/how-it-works-light.svg)

- **When it checks:** your first real prompt, any prompt that brings a new kind of scope (architecture, integration, migration, security, repeated failures), and every fourth prompt.
- **When it stays quiet:** replies such as "ok", repeats, prompts within 30 seconds of a check, and non-upgrades after the first check. Each suggestion shows once, with at most one upgrade alert every 15 minutes.
- **It never blocks:** after the check (5-second timeout) the turn runs on the model you selected, so a suggestion applies to your next turn. In Claude Code, two local hooks track your active model.

[Full rules in docs/how-it-works.md](https://github.com/Tatendaz/model-picker/blob/main/docs/how-it-works.md)

## Status

| | |
|---|---|
| Version | 0.3.0, released 2026-09-28. The first release, 0.1.0, shipped on 2026-09-20. [Releases](https://github.com/Tatendaz/model-picker/releases) |
| Hosts | Codex with plugin hooks, and Claude Code 2.1.257 or later. |
| Platforms | macOS and Linux. No native Windows: the session lock uses `fcntl`. |
| Tested | Unit tests run in CI on Python 3.9 to 3.14 on Linux, and 3.9 and 3.14 on macOS. The chat callout was checked by hand in the Codex desktop app and CLI, and live checks with real TypeSafe calls passed in Claude Code 2.1.278. |
| Not yet | Suggestions have not been compared against human labels, so they come from a classifier and can be wrong. A benchmark is not published yet. |

No host lets this hook switch models: `UserPromptSubmit` has no model or effort output. Claude Code does not tell hooks your effort level. [All limitations](https://github.com/Tatendaz/model-picker/blob/main/docs/limitations.md)

## Questions

### What leaves my machine?

On each check, sent to `api.typesafe.ai` under your key: the latest prompt (3,000 characters), the first task excerpt, the last four requests, your model and effort, and the previous suggestion. Session files stay local with mode 0600 in `~/.codex` or `~/.claude`. It never reads your source files or the full transcript, and there is no telemetry. [Privacy details](https://github.com/Tatendaz/model-picker/blob/main/docs/privacy.md)

### Can it switch the model for me?

No. The plugin runs as a `UserPromptSubmit` hook, and neither Codex nor Claude Code lets that hook change the active model or effort. You switch in the Codex model picker, or with `/model` and `/effort` in Claude Code.

### What does it cost?

The plugin is MIT licensed. Each check is one request to TypeSafe under your own API key, billed by TypeSafe separately from your Codex or Claude plan.

### How do I turn it off?

Send `mute model advisor` for the current session, or set `"enabled": false` in the host's `model-advisor.json`. To uninstall, disable the plugin and delete the files listed in [Configuration](https://github.com/Tatendaz/model-picker/blob/main/docs/configuration.md#uninstall).

## Built by Tatenda Zhou

Need help making AI coding agents reliable? [tatendaz@me.com](mailto:tatendaz@me.com?subject=Help%20making%20AI%20coding%20agents%20reliable)

[More work](https://tatendaz.github.io/) · [Follow on X](https://x.com/realtatendazhou) · [LinkedIn](https://www.linkedin.com/in/tatendazhou) · [Source on GitHub](https://github.com/Tatendaz/model-picker)

MIT licensed. Not affiliated with OpenAI, Anthropic or TypeSafe.
