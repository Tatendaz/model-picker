## What this changes

<!-- One or two sentences. Link an issue with "Closes #N" if there is one. -->

## Why

<!-- The problem being solved, or the capability being added. -->

## Checklist

- [ ] Branch is named `<type>/<slug>`: one of `feat/`, `fix/`, `docs/`, `chore/`, `refactor/`.
- [ ] `make test` passes locally.
- [ ] Source changes come with test changes. CI fails a source-only diff.
- [ ] `docs/features/<YYYY-MM-DD>-<slug>.md` and `docs/summaries/<YYYY-MM-DD>-<slug>.md` exist.
      `<slug>` is the branch name without its `feat/`-style prefix.
- [ ] `advisor.py` still imports only the standard library. CI checks this.
- [ ] Any new data sent to a provider is listed in `docs/privacy.md`.
- [ ] Codex behaviour is unchanged, or the change to it is described above.
- [ ] No API keys, real prompts, or session state files are in the diff. Tests use synthetic prompts.

## Notes for the reviewer

<!-- Tradeoffs, surprises, anything you want a second opinion on. Delete if not needed. -->
