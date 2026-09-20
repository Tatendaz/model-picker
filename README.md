# Model Picker

A recommendation-only Codex plugin. A session-aware command
hook periodically asks a configured JEV endpoint which Codex model and effort suit the request.
The recommendation is emitted as a hook warning and supplied to the assistant for a brief chat notice. You change the model yourself.
The hook does not block the prompt: the first turn continues on your selected model.
Recommendations therefore help you choose subsequent turns, or interrupt and resubmit.
It does not claim to save the cost of the already-selected first turn.

## Requirements and setup

macOS or Linux, Python 3.9 or later, Codex with UserPromptSubmit hooks, and a TypeSafe API key. The built-in defaults use
`https://api.typesafe.ai/v1/systemone` with `jev-latest`. No Python dependencies.

1. Add the marketplace and install the plugin:

   ```sh
   codex plugin marketplace add Tatendaz/model-picker
   codex plugin add codex-model-advisor@model-picker
   ```

   The display name is **Model Picker**. The stable plugin ID remains
   `codex-model-advisor` for compatibility. Disable any older personal copy before
   enabling this copy, so the hook does not run twice.
2. Optionally copy `plugins/codex-model-advisor/config.example.json` to `~/.codex/model-advisor.json`
   to override the defaults. No model or endpoint configuration is required.
3. Supply `TYPESAFE_API_KEY` in the hook environment, or on macOS store the key in
   Keychain under service `jev-codex-api-key` and your login account.
4. Review and trust the plugin command through `/hooks` in Codex CLI.
5. Start a new task. Look for the highlighted model recommendation when an upgrade is suggested.

The TypeSafe API key is separate from your Codex subscription. Configure it only in
your environment or Keychain, never in the repository. Native Windows is not
supported because the state lock uses `fcntl`.

Optional environment variables: `CODEX_ADVISOR_CONFIG` overrides the config path;
`CODEX_ADVISOR_STATE_DIR` overrides the private state directory.

Suggested Codex defaults in `~/.codex/config.toml`:

```toml
model = "gpt-5.6-terra"
model_reasoning_effort = "medium"
```

Existing threads and explicit app/profile selections can override global defaults.
The plugin never changes those settings itself.

## Example

A simple summary may stay on Terra without a notice. If the task grows into a
multi-tenant architecture review, Model Picker may suggest a stronger model:

> # 🔶 Model recommendation
>
> ---
>
> JEV recommends **gpt-6-astra / high**.
>
> Select it in the model picker if useful. **No settings were changed.**

Send **model advisor recheck** for an immediate reassessment. This is a prompt
phrase, not a terminal shell command. Recommendations are fallible and may vary.

## Behaviour

- Checks the first substantive prompt, new scope signals, and every four substantive prompts.
- Skips acknowledgements and duplicates, with a 30-second minimum between checks.
- Alerts for model or effort upgrades. If the current effort is unavailable, a high-effort recommendation is conditional and shown once per target, subject to cooldown.
- Send `model advisor recheck` to reassess the last substantive request immediately and show the result. This explicit request bypasses cooldown and duplicate suppression.
- Suppresses repeated targets and uses a 15-minute alert cooldown.
- `/advisor mute` and `/advisor unmute` are recognized prompt phrases, not native slash commands.
- `--force` explicitly requests a recommendation regardless of suppression.
- Uses a five-second provider timeout and a ten-second hook timeout.
- A provider failure on the first check or explicit recheck emits a baseline notice;
  later automatic checks fail quietly. A fallback is not a task-specific JEV verdict.
- Validates returned model/effort against a conservative allowlist. Configure
  `allowed_models` to restrict this further to models your account actually offers.
- Honors explicit model preferences in the classifier instructions, but recommendations
  remain fallible. Your selection always controls execution.
- State stores the initial prompt excerpt (1,200 characters), the latest four prompt
  excerpts (1,000 characters each), and recommendation/suppression metadata. Files
  have mode 0600 and use hashed session filenames. Context resets after 24 hours of
  inactivity on the next invocation; files are not automatically deleted in idle sessions.
- State stays outside the repository. Delete `~/.codex/model-advisor-state` to erase it.
- No source files or full transcript are read. Concurrent invocations use a session lock.

## Data sent to the provider

Enabling the hook sends a bounded snapshot to TypeSafe on qualifying checks:
the latest prompt (up to 3,000 characters), initial task excerpt, last four request
excerpts, current model/effort when available, and prior recommendation. The routing
rubric is fixed. Prompt text is private task data; provider retention follows TypeSafe's
policies. Credentials are never logged. HTTP redirects are rejected.

Snapshots remain outside Codex's model context. Qualifying alerts return a UI
`systemMessage` plus bounded `additionalContext` containing allowlisted model and
effort labels and a request to report them. Quiet checks return no output. The plugin cannot guarantee cache hits or cache
reuse after a model switch. It never switches models or changes effort automatically.

`check_every` (default 4) and `cooldown_seconds` (default 900) are configurable.
Scope signals are heuristics and periodic checks can miss subtle or rapid changes.
Alerts have been verified in Codex desktop and CLI. Rendering varies by client.

## Disable or uninstall

Set `enabled` to `false` in the advisor config, disable this plugin in Codex, or
uninstall it from the plugin UI. You may then remove the advisor config and state
folder. The plugin never edits unrelated hooks or removes Keychain credentials.

## Development

```sh
python3 -m unittest discover -s plugins/codex-model-advisor/tests -v
```

Tests cover fallback, once-per-session checks, manual rechecks, output validation,
credential handling boundaries and private state. A live TypeSafe smoke test passed on 2026-09-19 using a synthetic summarization
prompt and the Keychain credential. Text escalation and chat delivery were manually
verified in desktop and CLI on 2026-09-20. Voice parsing has synthetic test coverage;
live voice delivery remains unverified.

## Open source

MIT licensed. Contributions are welcome. Credentials, personal usage reports, and
private configuration stay outside the repository. This repository is a plugin
marketplace source; it is not a listing in the official OpenAI plugin directory.

See [ROADMAP.md](ROADMAP.md) for automatic routing plans and
[CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

References: [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[App Server](https://learn.chatgpt.com/docs/app-server).

## TypeSafe integration

One Choice question selects a supported model/effort pair. The endpoint returns
`answers.route.choice` and confidence. Explanations are local category descriptions,
not generated JEV reasoning. Confidence describes distribution concentration, not
proven correctness; no arbitrary confidence cutoff is imposed. An explicit uncertain
choice uses the Terra/medium baseline. See [TypeSafe API](https://docs.typesafe.ai/api).

## Voice handoffs and hook trust

The advisor recognizes Codex `<realtime_delegation>` handoffs. It evaluates only
`<input>`, ignoring duplicated transcript deltas and `transcript_tail_flush` events.
Typed and spoken requests share one history and cooldown. It receives text handoffs,
not raw audio; it cannot monitor speech that has not been handed to the agent.
State includes `input_mode` and `last_status` for checking execution without extra logs.

Installation and enablement do not grant hook trust. Open `/hooks` in the Codex CLI,
review the `codex-model-advisor@model-picker` UserPromptSubmit command and trust it.
This permits the reviewed script to read its Keychain credential, send bounded
request excerpts to TypeSafe, and write private local advisor state. A changed hook
definition may require a new review. Never bypass all hook trust to enable this plugin.

Voice normalization is tested with synthetic handoff events. Actual voice dispatch
still needs end-to-end verification.

### Chat delivery

Alerts emit both a hook warning and a short instruction for the assistant to report
the allowlisted model and effort in a bold Markdown blockquote at the start of the reply. Suppressed checks add no model context.
This replaces warning-only delivery, which was not visible in desktop testing.
Alert turns add a small amount of context and may affect cache reuse.
The manual skill reuses a completed hook result instead of making a second request.
An emitted alert is not confirmation that the app displayed it.

### Why automatic switching is unavailable

This plugin only recommends a model and reasoning effort. Users change their
selection manually in Codex desktop or CLI. There is no automatic-mode setting.

The plugin runs through `UserPromptSubmit`. OpenAI documents context injection,
messages, and prompt blocking for that hook, but no output field for changing the
active model or reasoning effort. Therefore the documented hook interface does
not provide the switching operation this plugin would need.
See [OpenAI's UserPromptSubmit documentation](https://learn.chatgpt.com/docs/hooks#userpromptsubmit).

This is a limitation of this hook-based integration, not a claim that automatic
routing is impossible in all Codex integrations. A separate client controlling
Codex App Server can select a model when starting a turn. That would require a
different integration and is not implemented here. See
[OpenAI's App Server lifecycle documentation](https://learn.chatgpt.com/docs/app-server#lifecycle-overview)
and [the roadmap](ROADMAP.md).
