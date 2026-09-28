# Roadmap

## Next: validate recommendation quality

- Expand real-world testing beyond the desktop and CLI escalation flows already verified.
- Extend the [benchmark](docs/benchmark.md) past bug fixes: reviews, refactors and
  non-coding work, where a lower-cost model may be enough.
- Measure plan-limit usage directly instead of pricing tokens at API rates.
- Add more provider adapters and configurable budget policies.

## Later: optional automatic routing

Build a separate Codex App Server launcher that receives the prompt, obtains a
recommendation, validates it against `model/list`, then calls `turn/start` with
explicit `model` and `effort`. Obtain fresh user confirmation before enabling this integration. Keep user overrides, fallback, and routing explanations.
Do not rewrite the global config on every prompt or claim that the desktop hook
can change the active model. Automatic routing through this plugin depends on a supported hook model-switch
operation becoming available. The [documented UserPromptSubmit outputs](https://learn.chatgpt.com/docs/hooks#userpromptsubmit)
do not expose one. A separate client can control turn selection through
[Codex App Server](https://learn.chatgpt.com/docs/app-server#lifecycle-overview).
No automatic-mode preference is offered until switching is implemented.

## Implemented: Claude Code support

The same script runs as a Claude Code plugin with Claude models, `/model` and
`/effort` callouts, and model tracking through `SessionStart` and
`PostModelSwitch`. Next: check the callout on Opus and Fable, and use the
effort level if Claude Code starts passing it to `UserPromptSubmit` hooks.

## Implemented: task-aware reassessment

Bounded request history, new-scope checks, periodic reassessment, upgrade and savings
alerts, cooldowns, duplicate suppression and session mute. Next: validate real-world scope
detection and alert quality, and verify live voice handoffs.
