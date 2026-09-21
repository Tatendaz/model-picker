# Limitations

## No automatic switching

Model Picker suggests a model and effort. You change them in the Codex desktop
app or CLI. There is no automatic mode and no setting that enables one.

The plugin runs as a `UserPromptSubmit` hook. OpenAI documents three kinds of
output for that hook: extra context, messages, and blocking the prompt. None
of them changes the active model or reasoning effort
([hook reference](https://learn.chatgpt.com/docs/hooks#userpromptsubmit)).

That is a limit of hooks, not of Codex as a whole. A separate client that
drives [Codex App Server](https://learn.chatgpt.com/docs/app-server#lifecycle-overview)
can pick a model when it starts each turn. The [roadmap](../ROADMAP.md)
describes that design; it is not built.

## The first turn is already running

The hook does not block the prompt. The turn that triggered a suggestion runs
on the model you had selected, so the plugin does not save the cost of that
turn. Switch before your next prompt, or stop the turn and resend.

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
| Unit tests | Run in CI on Python 3.9 to 3.14, Linux and macOS |
| Live TypeSafe request | Passed on 2026-09-19 with a synthetic summarization prompt |
| Text escalation and chat callout | Checked by hand in Codex desktop and CLI on 2026-09-20 |
| Voice handoff parsing | Covered by tests with synthetic events |
| Live voice delivery | Not yet verified end to end |
| Recommendation quality | Not yet compared against human labels; see the roadmap |
