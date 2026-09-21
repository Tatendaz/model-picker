# Contributing

Open an issue first for anything beyond a small fix, so we can agree on the
approach before you write code.

## Setup

No install step. The plugin and its tests use only the Python standard
library, and the tests never touch the network, Keychain or your real state
directory.

```sh
make test   # python3 -m unittest discover -s plugins/codex-model-advisor/tests -v
make lint   # needs ruff; CI pins ruff 0.14.2
```

## Rules

- Keep it recommendation-only. The hook must never change the model, effort or
  Codex config.
- No third-party imports in `advisor.py`, and no dependency manifest. CI checks
  both.
- Never log prompts, credentials, full provider responses or exception text.
- Tests and examples use synthetic prompts only.
- If a change sends more data to a provider, update
  [docs/privacy.md](docs/privacy.md) in the same PR.
- Plugin code stays under `plugins/codex-model-advisor/`.

## Pull requests

1. Branch as `<type>/<slug>`, where type is `feat`, `fix`, `docs`, `chore` or
   `refactor`.
2. Add tests with any source change. CI fails a source-only diff.
3. Add `docs/features/<YYYY-MM-DD>-<slug>.md` (what changed and why) and
   `docs/summaries/<YYYY-MM-DD>-<slug>.md` (how it came about). The PR gate
   checks both, named for your branch slug.
4. Fill in the PR template.

By contributing you agree your work is released under the [MIT License](LICENSE)
and that you follow the [Code of Conduct](CODE_OF_CONDUCT.md).
