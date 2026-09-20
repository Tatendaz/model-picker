# Contributing

Open an issue describing the problem and expected behaviour, then submit a focused
pull request with relevant tests. Keep the default mode recommendation-only. Do not
log prompts, credentials, full provider responses, or exception bodies. Provider
integrations must use synthetic test prompts. Document any new data sharing.
Run `python3 -m unittest discover -s plugins/codex-model-advisor/tests -v` before submitting.

Keep plugin code under `plugins/codex-model-advisor/`. Include feature notes in
`docs/features/` and a brief change summary in `docs/summaries/` for behavioral changes.
