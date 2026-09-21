# Diagrams

The README diagrams are [Archify](https://github.com/tt-a1i/archify)
specifications. Edit the JSON, never the SVG.

| Source | Type | Used in |
|---|---|---|
| `how-it-works.sequence.json` | sequence | README "How it works" |
| `data-flow.dataflow.json` | dataflow | README "What leaves your machine" |

Each source has three exports:

- `<name>-light.svg` and `<name>-dark.svg`: fixed palettes. The README picks
  one with `<picture>`, which follows the GitHub theme.
- `<name>.svg`: the auto-theme export, which follows the operating system
  colour scheme. Use it when embedding elsewhere.

## Regenerate

```sh
archify validate sequence docs/diagrams/how-it-works.sequence.json --quality showcase
archify deliver  sequence docs/diagrams/how-it-works.sequence.json /tmp/how-it-works.html --quality showcase
archify visual-check /tmp/how-it-works.html
```

Open the HTML, choose **Export → SVG**, and save it as
`docs/diagrams/how-it-works.svg`. Then write the fixed-palette pair:

```sh
python3 docs/diagrams/split_themes.py docs/diagrams/how-it-works.svg docs/diagrams/how-it-works
```

`split_themes.py` keeps the light-mode block of the auto-theme SVG for the
light file and removes it for the dark file. Repeat with `dataflow` for
`data-flow`. The HTML viewer and `*.visual-check.*` screenshots are local
build output and stay out of the repository.
