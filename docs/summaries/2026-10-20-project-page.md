# Session: Project page on GitHub Pages

## Request

"Build a GitHub Pages project page for the public repo Tatendaz/model-picker,
ship it through a PR, and turn Pages on." The brief asked for the same look as
the claude-usage and yapui project pages, content taken only from the repo,
light and dark mode with a toggle, a mobile layout, Open Graph and Twitter
tags, a canonical link, a favicon, and a "Built by Tatenda Zhou" footer. It
also said not to touch PR #7 and to publish only numbers already on `main`.

## Changes

1. Read the claude-usage and yapui `docs/` folders on `main`. claude-usage has
   the theme toggle, so it was the template: a top-right toggle, a left-aligned
   hero with a specimen, sections split by hairlines, rows for "how it works",
   a facts table and a questions list.
2. Took the colours from `assets/brand/README.md`: Night `#0E0D10` and Paper
   `#FAF4E6` as the two backgrounds, Coral `#F2542D` as the one accent. Coral
   on Paper is about 3.4:1, so links and the primary button in the light theme
   use a darker coral, `#B8391A`.
3. Wrote `docs/index.html`, `docs/index.md` and `docs/404.html`, copied the
   lockups and icon into `docs/img/`, and rendered `docs/social-preview.png`
   with headless Chrome.
4. Checked the page in a local server at 1280 px and 375 px in both themes.
   Two fixes came out of that: the light and dark diagram both showed (a
   `display:block` rule beat the theme switch), and the status table scrolled
   sideways on a phone, so it now stacks below 560 px.

## Decisions

- The hero visual is the callout text the README quotes, set as a chat block,
  not a mock screenshot. The second visual is the repo's own sequence
  diagram, swapped by theme.
- The status section says a benchmark is not published yet. PR #7 holds one,
  but it is not on `main`.
- `.nojekyll` keeps GitHub Pages from rendering the existing docs Markdown as
  pages.
