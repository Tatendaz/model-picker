# Feature: Project page on GitHub Pages

**Branch:** feat/project-page
**Date:** 2026-10-20

## Summary

A one-page site for Model Picker at https://tatendaz.github.io/model-picker/,
served by GitHub Pages from `main:/docs`. It follows the layout of the other
project pages on tatendaz.github.io (claude-usage, yapui).

## Motivation

The repo had no homepage URL. A short page gives people a link to share that
explains what the plugin does, how to install it, and what it does not do,
without reading the whole README.

## What changed

- `docs/index.html`: the page. Light and dark themes follow the system setting,
  with a toggle that remembers the choice. Sections: what it does, who it is
  for, install (copied from the README), the three prompts, how it works with
  the repo's sequence diagram, status, questions, and an author footer.
- `docs/index.md`: the same content as Markdown, linked with
  `rel="alternate" type="text/markdown"`.
- `docs/404.html`: a not-found page with links back.
- `docs/.nojekyll`: serve the files as they are. Without it, Jekyll would
  render every Markdown file under `docs/` as a page.
- `docs/img/`: copies of `lockup-light.svg`, `lockup-dark.svg` and
  `icon-sticker.svg` (as `icon.svg`), plus 32 px and 180 px PNG icons. Pages
  serves only `docs/`, so the brand files had to be copied in.
- `docs/social-preview.png`: 1200 x 630 Open Graph image, rendered from the
  dark lockup, the tagline and the example callout.

## Notes

- Every claim on the page comes from the README, `docs/how-it-works.md`,
  `docs/limitations.md`, `docs/privacy.md` and the release list. The page says
  a benchmark is not published yet; PR #7 (`docs/benchmark.md`) is still open
  and this branch does not touch that file.
- The copied brand files in `docs/img/` must be refreshed by hand if
  `assets/brand/build.py` redraws them.
- No code or tests changed.
