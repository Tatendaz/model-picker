# Security policy

Model Picker runs as a trusted Codex or Claude Code hook, reads an API key, and
sends prompt excerpts to TypeSafe. That trust surface gets a written policy.

## Reporting a vulnerability

Do not open a public issue for a security problem. Use GitHub's private form:
[Report a vulnerability](https://github.com/Tatendaz/model-picker/security/advisories/new).
If that form is unavailable to you, open a
[Private contact request](https://github.com/Tatendaz/model-picker/issues/new?template=private_contact.yml)
with the topic "Security" and no details, and you will be invited to a private
thread.

Include the release tag or commit, your OS, the host (Codex desktop or CLI, or
Claude Code and its version), what you did and what happened. Never include an
API key, a real prompt, or a session state file; describe prompts in general
terms or use a synthetic one.

This is a single-maintainer project with no SLA or bug bounty. Reports are
acknowledged within a few days, and reporters are credited in release notes
unless they ask not to be.

## Supported versions

Only the latest release is supported.

## What the hook promises

Anything that breaks one of these statements is a vulnerability:

1. The API key is read at run time from the configured environment variable or
   macOS Keychain, sent only to the configured HTTPS endpoint, and never
   logged, printed or written to disk.
2. Only the fields listed in [docs/privacy.md](docs/privacy.md) are sent, each
   within its stated length limit. HTTP redirects are refused.
3. Only allowlisted model and effort labels and fixed text enter the model
   context in either host. Prompt excerpts and provider output never do.
4. Session state stays under the state directory with mode 0600, whatever the
   session ID contains.
5. The hook never changes the model, effort, config or other hooks in Codex or
   Claude Code, and never reads source files or the transcript.
6. The Claude Code model-tracking hooks (`SessionStart`, `PostModelSwitch`)
   store only a model ID and make no network call.
7. `advisor.py` imports only the Python standard library. CI checks this.

## Not vulnerabilities

- TypeSafe receiving the excerpts in item 2. That is the documented purpose;
  its retention follows TypeSafe's terms.
- A local attacker who can already run code as you or read your home
  directory.
- A wrong or unhelpful model suggestion. Report that as a bug.
