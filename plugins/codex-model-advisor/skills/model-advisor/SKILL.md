---
name: model-advisor
description: Explain model advisor recommendations or manually reassess model and effort for a task when requested.
---
# Model advisor

This plugin recommends models; it cannot change the active model or effort.
It runs in Codex and in Claude Code, and each host gets suggestions for its own
models.

When this turn includes a completed Model Advisor hook result, report that result
using the supplied bold Markdown blockquote at the start of the response. Preserve
the 🔶 icon, top-level heading (#), and horizontal line beneath the heading. Show it
once, separated from the task response by a blank line. Do not repeat it in both
commentary and final. Do not run another check or replace it with a fallback.
The phrase `model advisor recheck` is handled by the UserPromptSubmit hook.
If no result is supplied, say the hook result is missing; do not claim JEV failed.

For a separately requested manual assessment without a hook result, run
`scripts/advisor.py --force` from the plugin root with JSON on stdin.
In Claude Code, also pass `--host claude`. In Codex, pass no host flag.
Use the actual current session ID from the runtime, never an invented placeholder.
If the ID is unavailable, ask the user to send `model advisor recheck` instead.
Include hook_event_name UserPromptSubmit, session_id, and a brief task prompt.
Use json.dumps and structured subprocess input, never shell interpolation.
Do not send file contents or full conversation history.

Manual execution may require permission to write advisor state outside the workspace
and access Keychain/network. Follow the host permission workflow when needed.
A local execution failure is not proof of a JEV outage. Never replace a successful
hook result with the baseline because a separate manual execution failed.
Explain recommendations as external advice. The user changes settings: in Codex
with the model picker, in Claude Code with `/model` and `/effort`.

## Manual changes only

Automatic switching is unavailable in this hook-based plugin. Do not offer an
opt-in, save a switching preference, or claim that automatic mode is active.
The former setup/manual/automatic/settings prompt commands have been removed.
If asked about them, explain that model changes are manual.
In neither host does the documented UserPromptSubmit output have a model or
effort override:
https://learn.chatgpt.com/docs/hooks#userpromptsubmit
https://code.claude.com/docs/en/hooks#userpromptsubmit
In Codex, a separate App Server client could control turn selection, but it is
not part of this plugin.
