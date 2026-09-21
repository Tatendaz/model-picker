"""Split an Archify auto-theme SVG export into fixed light and dark files."""
import sys
from pathlib import Path

MARK = "@media (prefers-color-scheme: light) {"

def split(auto_path, prefix):
    text = Path(auto_path).read_text()
    start = text.index(MARK)
    depth, i = 0, start + len(MARK) - 1
    while True:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                break
        i += 1
    inner = text[start + len(MARK):i]
    assert MARK not in text[i:], "more than one light media block"
    Path(prefix + "-light.svg").write_text(text[:start] + inner + text[i + 1:])
    Path(prefix + "-dark.svg").write_text(text[:start] + text[i + 1:])

split(sys.argv[1], sys.argv[2])
