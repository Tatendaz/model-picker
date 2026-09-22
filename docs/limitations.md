# Limitations

## No automatic switching

Model Picker suggests a model and effort. You change them yourself: in the
Codex desktop app or CLI, or with `/model` and `/effort` in Claude Code. There
is no automatic mode and no setting that enables one.

The plugin runs as a `UserPromptSubmit` hook. OpenAI documents three kinds of
output for that hook: extra context, messages, and blocking the prompt. None
of them changes the active model or reasoning effort
([hook reference](https://learn.chatgpt.com/docs/hooks#userpromptsubmit)).
Claude Code's version accepts a block decision, extra context and a session
title, plus messages, and none of those changes the model or effort either
([hook reference](https://code.claude.com/docs/en/hooks#userpromptsubmit)).
Its `PreModelSwitch` hook can allow or deny a switch you asked for, but it
cannot start one.

That is a limit of hooks, not of Codex as a whole. A separate client that
drives [Codex App Server](https://learn.chatgpt.com/docs/app-server#lifecycle-overview)
can pick a model when it starts each turn. The [roadmap](../ROADMAP.md)
describes that design; it is not built.

## The first turn is already running

The hook does not block the prompt. The turn that triggered a suggestion runs
on the model you had selected, so the plugin does not save the cost of that
turn. Switch before your next prompt, or stop the turn and resend.

## Claude Code specifics

- Hooks never receive the effort level, so the advisor assumes high, Claude
  Code's default for Sonnet, Opus and Fable. A suggestion for your current
  model at `xhigh` or `max` is shown as conditional.
- The model is known only after `SessionStart` or `PostModelSwitch` records it.
  `SessionStart` omits the model in `claude -p` runs and can omit it after
  `/clear`; until the next switch, only the first check of that session can
  alert.
- After installing the plugin mid-session, start a new session. The current
  session missed `SessionStart`.
- `/model <alias>` and `/effort <level>` save the choice as your default for new
  sessions. See [switching in Claude Code](configuration.md#switching-in-claude-code)
  for session-only switches.
- The callout in the reply depends on the model following an instruction.
  Haiku 4.5 skipped it in testing; the warning line under your prompt still
  appeared.
- Claude Code 2.1.251 or later is required, because `PostModelSwitch` first
  shipped in that version.

## Platform

macOS and Linux only. The session lock uses `fcntl`, which native Windows does
not have. Keychain lookup is macOS only; on Linux, use the environment
variable.

## Scope detection

Scope categories are regular expressions over the prompt text. They miss
changes that use other words, and a prompt that mentions "production" in
passing counts as integration scope. Periodic checks every fourth prompt catch
some of what the patterns miss.

## What has been verified

| Area | Status |
|---|---|
| Unit tests | Run in CI on Python 3.9 to 3.14 on Linux, and 3.9 and 3.14 on macOS |
| Live TypeSafe request | Passed on 2026-09-19 with a synthetic summarization prompt |
| Text escalation and chat callout | Checked by hand in Codex desktop and CLI on 2026-09-20 |
| Codex behaviour after Claude Code support | Old and new `advisor.py` compared on 1,500 random prompt sequences and 70 request cases on 2026-09-22: identical output, requests and state |
| Claude Code hook payloads | Captured from Claude Code 2.1.278 on 2026-09-22 with synthetic prompts (field names only) |
| Claude Code live check | Passed on 2026-09-22 in Claude Code 2.1.278 with real TypeSafe calls: headless alert, interactive recheck, session-only switch to Haiku, upgrade alert, mute |
| Voice handoff parsing | Covered by tests with synthetic events |
| Live voice delivery | Not yet verified end to end |
| Recommendation quality | Not yet compared against human labels; see the roadmap |
