# Session: Lighter suggestion on the first check

**Branch:** feat/first-check-lighter-suggestion
**Date:** 2026-09-29

## Prompts

1. "Let's create the launch copy for X and LinkedIn for model-picker. I want to
   use the video rendered here ... In the comment we can add what the
   suggestion looks like and links to the repo and that it's open source."
2. "Make your suggestions to make the copy more punchy and viral-worthy, high
   engagement."
3. "I'm not posting about benchmark. I want to introduce my new open-source
   project and the fact that it's powered by JEV."
4. "Also, what do you mean it doesn't suggest a lower model anymore?"
5. "1, and can you add Claude Code Opus 5.5 support."

## Steps taken

While writing launch copy, found that automatic alerts were upgrade-only
(`advisor.py`, `if not upgrade and not force`), so the video's Fable-to-Sonnet
suggestion could only appear after a recheck. The owner chose option 1: allow
a lighter suggestion on the first check of each session.

Changed the alert rule in `advisor.py`, added the `suggest_lower` key, updated
three tests and added five, and updated the docs. Checked that Opus 5.5 was
already supported on main; the owner's installed copy was 0.1.0, which is why
their session showed a suggestion on an unknown model. Bumped both manifests to
0.3.0.

## Decisions

- Lighter suggestions only on the first check. Later checks follow the task as
  it grows, which is the plugin's main job.
- No lighter effort from an unknown effort. Claude Code never reports effort,
  so a same-model effort drop there would be a guess.
- A lighter alert leaves the cooldown alone. Otherwise a user who takes the
  advice would miss an upgrade for 15 minutes.
- Opt-out config key instead of a new default-off feature, because the owner
  wants this behaviour on by default.
