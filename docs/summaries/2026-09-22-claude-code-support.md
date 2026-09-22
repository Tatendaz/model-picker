# Session: Claude Code support

## Request

"How long would it take to make this also work in Claude Code for Anthropic
models too, without breaking Codex functionality? And how do you propose it be
done?"

The owner approved the proposed design and had it built in a separate git
worktree on `feat/claude-code-support`, from a written brief. The session's own
prompt: "Read your task brief ... and do the task it describes. Work only in
this worktree. Start by verifying the Claude Code hook facts and capturing real
payload shapes, then build, test, and follow the brief's finish steps."

## Changes

Captured `UserPromptSubmit`, `SessionStart`, `PreModelSwitch` and
`PostModelSwitch` payloads from Claude Code 2.1.278 with a throwaway plugin in a
scratch folder, recording field names only. Checked the Claude Code docs and the
openai/codex source with two research agents. Tested how Claude Code loads
plugin hooks and symlinks.

Added host profiles to `advisor.py`, the `claude-model-advisor` plugin folder,
the Claude marketplace file, model tracking on `SessionStart` and
`PostModelSwitch`, 15 tests, the CI manifest check for Claude, and docs for both
hosts. Regenerated both diagrams with Archify. Compared the old and new script
on 1,500 random Codex prompt sequences. Ran live checks in Claude Code with real
TypeSafe calls, headless and interactive.

## Decisions

- Separate Claude plugin folder instead of a second hooks file in the Codex
  folder. Claude Code runs `hooks/hooks.json` even when `plugin.json` names
  another hooks file, so one folder would run the Codex hook in Claude Code too.
- The host comes from a `--host claude` flag, not from environment variables:
  Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA`.
- Claude Code state lives in `~/.claude/model-advisor-state`, not
  `CLAUDE_PLUGIN_DATA`, so a manual `--force` run finds the same file.
- Claude Code's unknown effort is treated as `high`, its default, so same-model
  alerts fire only for `xhigh` and `max`.
- Haiku 4.5 has no effort setting and is offered as `claude-haiku-4-5` /
  `none`.
- The plain phrases `mute model advisor` and `unmute model advisor` are the
  documented mute commands, because Claude Code's built-in `/advisor` command
  takes `/advisor mute` before the hook sees it.
