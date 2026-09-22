# Privacy and trust

Model Picker sends parts of your prompts to a third-party API. This page lists
exactly what goes where.

## Sent to TypeSafe

Only on a check (see [when a check runs](how-it-works.md#when-a-check-runs)),
one HTTPS POST to the configured endpoint, `https://api.typesafe.ai/v1/systemone`
by default:

| Field | Limit |
|---|---|
| Latest prompt | 3,000 characters |
| First task excerpt of the session | 1,200 characters |
| Last four prompts | 1,000 characters each |
| Current model and effort | as the host reports them, or `unknown` |
| Previous suggestion | model and effort only |
| Routing rubric | fixed text per host, the same for every user |

In Claude Code, the current model is the ID recorded by the model-tracking
hooks (below), and the effort is always `unknown` because Claude Code does not
pass it to hooks.

The request carries your API key as a bearer token. What TypeSafe keeps, and
for how long, follows TypeSafe's terms for your account. Redirects are refused,
so the request cannot be forwarded to another host.

Nothing else leaves your machine. The hook does not read source files, the
full transcript, or tool output, and it has no telemetry.

## Model tracking in Claude Code

Two extra hooks run only in Claude Code. `SessionStart` reads the event's
`model` field and `PostModelSwitch` reads `to_model`. Each stores the model ID
(for example `claude-opus-5`) in the session file and makes no network call.
They read no prompt text, and they ignore the other fields in the event, such
as the transcript path.

## Stored locally

| What | Codex | Claude Code |
|---|---|---|
| Session state | `~/.codex/model-advisor-state/<sha256 of session id>.json` | `~/.claude/model-advisor-state/<sha256 of session id>.json` |
| Lock files | same folder, `.json.lock` | same folder, `.json.lock` |
| Your config | `~/.codex/model-advisor.json` (optional) | `~/.claude/model-advisor.json` (optional) |

Session files are mode 0600 and hold the excerpts listed above plus check,
alert and mute metadata. The file name is a hash, so a crafted session ID
cannot write outside the folder. Context resets after 24 hours idle, but files
stay until you delete them:

```sh
rm -rf ~/.codex/model-advisor-state ~/.claude/model-advisor-state
```

## What enters the model's context

Only on an alert, and only allowlisted strings: the model name, the effort
level, and a fixed instruction to show the callout. Prompt excerpts and
TypeSafe's raw response never enter the model context in either host.

## Credentials

The key comes from `TYPESAFE_API_KEY` (or the variable named by
`api_key_env`), then from macOS Keychain service `jev-codex-api-key` under your
login account. Both hosts use the same default service, so one Keychain item
serves both; set `keychain_service` in a host's config to use another. It is read at run time, sent only to the configured endpoint,
and never logged or written to disk by the plugin. Error messages shown to you
never include exception text, so a failing request cannot echo the key.
Uninstalling the plugin does not remove the Keychain item.

## Hook trust

In Codex, installing or enabling the plugin does not let the hook run. In the
Codex CLI, open `/hooks`, review the `codex-model-advisor@model-picker`
UserPromptSubmit command and trust it. Trusting it lets that script read its
Keychain item, send the excerpts above to TypeSafe, and write state to
`~/.codex`. Codex ties trust to the hook's command, timeout and status message,
not to the script's contents. A changed hook definition may need a new review.
Do not turn off hook trust checks globally to make this plugin run.

Claude Code has no per-hook trust step: once `claude-model-advisor` is
enabled, its three hooks run in every session, in folders you have trusted.
They can read the Keychain item, send the excerpts above to TypeSafe, and write
state to `~/.claude`. Read
[`hooks/hooks.json`](../plugins/claude-model-advisor/hooks/hooks.json) before
you install, and use `/plugin` to disable the plugin.

To report a security problem, see [SECURITY.md](../SECURITY.md).
