"""Tests for the brand assets and the script that draws them.

These run without fontTools and without the Shantell Sans font: they cover the
geometry and the SVG assembly in ``assets/brand/build.py``, and they check that
every committed asset is still a well-formed, correctly coloured SVG. A
hand-edited or truncated asset fails here.
"""

import importlib.util
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
BRAND = REPO / "assets" / "brand"

_spec = importlib.util.spec_from_file_location("brand_build", BRAND / "build.py")
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)

VARIANTS = ("sticker", "sticker-grain", "light", "dark", "mono")


class PenLoopTests(unittest.TestCase):
    def test_starts_with_a_move_and_four_curves(self):
        d = build.pen_loop(39, 35, 26, 24)
        self.assertTrue(d.startswith("M"))
        self.assertEqual(d.count("C"), 4)

    def test_overshoots_its_own_start(self):
        """The last point is past the first one, so the stroke crosses itself."""
        d = build.pen_loop(39, 35, 26, 24)
        points = re.findall(r"(-?\d+\.?\d*) (-?\d+\.?\d*)", d)
        start = (float(points[0][0]), float(points[0][1]))
        end = (float(points[-1][0]), float(points[-1][1]))
        self.assertNotEqual(start, end)
        self.assertLess(end[1], start[1], "the stroke should finish above where it began")

    def test_scales_with_the_radii(self):
        small = build.pen_loop(0, 0, 10, 10)
        large = build.pen_loop(0, 0, 20, 20)
        self.assertNotEqual(small, large)


class BoundsTests(unittest.TestCase):
    def test_measures_the_offset_copy_and_the_keyline(self):
        art = [build.el("M10 10 L20 20", "stroke", 4.0, build.INK, off=(3.0, -3.0))]
        tight = build.bounds(art, key=0)
        wide = build.bounds(art, key=11.0)
        self.assertEqual(tight[0], 10 - 2.0)
        self.assertEqual(tight[1], 10 - 3.0 - 2.0, "the upward offset should raise the top")
        self.assertEqual(tight[2], 20 + 3.0 + 2.0, "the rightward offset should widen the right")
        self.assertEqual(wide[0], tight[0] - 11.0)
        self.assertEqual(wide[3], tight[3] + 11.0)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.art = [build.el("M0 0 L10 10", "stroke", 5.0, build.INK, off=(2.0, -2.0))]

    def test_keyline_pass_only_when_asked(self):
        with_key = build.render(self.art, build.INK, build.CORAL, key=11.0)
        without = build.render(self.art, build.INK, build.CORAL, key=0)
        self.assertIn(build.PAPER, with_key)
        self.assertNotIn(build.PAPER, without)

    def test_keyline_is_wider_than_the_stroke(self):
        out = build.render(self.art, build.INK, build.CORAL, key=11.0)
        widths = [float(w) for w in re.findall(r'stroke-width="([\d.]+)"', out)]
        self.assertEqual(max(widths), 5.0 + 22.0)

    def test_offset_copy_is_shifted_and_uses_the_accent(self):
        out = build.render(self.art, build.INK, build.CORAL, key=0)
        self.assertIn('transform="translate(2.0 -2.0)"', out)
        self.assertIn(build.CORAL, out)

    def test_grain_only_wraps_the_offset_copy(self):
        plain = build.render(self.art, build.INK, build.CORAL, key=0, grain=False)
        grainy = build.render(self.art, build.INK, build.CORAL, key=0, grain=True)
        self.assertNotIn("url(#gr)", plain)
        self.assertEqual(grainy.count("url(#gr)"), 1)

    def test_element_without_offset_gets_no_accent_copy(self):
        art = [build.el("M0 0 L10 10", "stroke", 5.0, build.INK)]
        out = build.render(art, build.INK, build.CORAL, key=0)
        self.assertNotIn(build.CORAL, out)

    def test_document_carries_the_measured_viewbox_and_a_title(self):
        doc = build.document("<path/>", (-5.4, -10.6, 92.4, 90.6), "Model Picker icon")
        self.assertIn('viewBox="-5.4 -10.6 92.4 90.6"', doc)
        self.assertIn("<title>Model Picker icon</title>", doc)


class CommittedAssetTests(unittest.TestCase):
    def svg_files(self):
        files = sorted(BRAND.glob("*.svg"))
        self.assertTrue(files, "no SVGs found in assets/brand")
        return files

    def test_every_variant_is_present(self):
        for name in ("lockup", "icon"):
            for variant in VARIANTS:
                self.assertTrue((BRAND / f"{name}-{variant}.svg").exists(),
                                f"missing {name}-{variant}.svg")

    def test_every_svg_parses_and_is_labelled(self):
        for path in self.svg_files():
            root = ET.parse(path).getroot()
            self.assertTrue(root.get("viewBox"), f"{path.name} has no viewBox")
            self.assertTrue(root.get("aria-label"), f"{path.name} has no aria-label")

    def test_wordmark_is_outlined_so_no_font_is_needed(self):
        for variant in VARIANTS:
            text = (BRAND / f"lockup-{variant}.svg").read_text()
            self.assertNotIn("<text", text)
            self.assertNotIn("font-family", text)

    def test_mono_variants_inherit_the_current_colour(self):
        for name in ("lockup", "icon"):
            text = (BRAND / f"{name}-mono.svg").read_text()
            self.assertIn("currentColor", text)
            self.assertEqual(re.findall(r"#[0-9A-Fa-f]{6}", text), [],
                             f"{name}-mono.svg should carry no fixed colours")

    def test_light_and_dark_use_the_documented_inks(self):
        for name in ("lockup", "icon"):
            light = (BRAND / f"{name}-light.svg").read_text()
            dark = (BRAND / f"{name}-dark.svg").read_text()
            self.assertIn(build.INK, light)
            self.assertIn(build.PAPER, dark)
            self.assertIn(build.CORAL, light)
            self.assertIn(build.CORAL, dark)

    def test_only_the_grain_variants_carry_a_filter(self):
        for path in self.svg_files():
            text = path.read_text()
            if path.stem.endswith("sticker-grain"):
                self.assertIn("feTurbulence", text)
            else:
                self.assertNotIn("feTurbulence", text)

    def test_nothing_is_clipped_by_the_viewbox(self):
        """The die-cut edge is a wide stroke that sits outside the artwork. If the
        viewBox is measured from the artwork alone, that edge gets cut off."""
        for path in self.svg_files():
            root = ET.parse(path).getroot()
            vx, vy, vw, vh = (float(n) for n in root.get("viewBox").split())
            x0, y0, x1, y1 = self.drawn_bounds(root)
            self.assertGreaterEqual(round(x0, 2), round(vx, 2), f"{path.name} clipped on the left")
            self.assertGreaterEqual(round(y0, 2), round(vy, 2), f"{path.name} clipped at the top")
            self.assertLessEqual(round(x1, 2), round(vx + vw, 2), f"{path.name} clipped on the right")
            self.assertLessEqual(round(y1, 2), round(vy + vh, 2), f"{path.name} clipped at the bottom")

    def drawn_bounds(self, root):
        xs, ys = [], []

        def walk(node, dx, dy):
            shift = node.get("transform", "")
            match = re.match(r"translate\((-?[\d.]+)\s+(-?[\d.]+)\)", shift)
            if match:
                dx += float(match.group(1))
                dy += float(match.group(2))
            if node.tag.endswith("path") and node.get("d"):
                half = float(node.get("stroke-width", 0)) / 2
                nums = [float(n) for n in re.findall(r"-?\d+\.?\d*", node.get("d"))]
                for x, y in zip(nums[0::2], nums[1::2]):
                    xs.extend([x + dx - half, x + dx + half])
                    ys.extend([y + dy - half, y + dy + half])
            for child in node:
                walk(child, dx, dy)

        walk(root, 0.0, 0.0)
        return min(xs), min(ys), max(xs), max(ys)

    def test_readme_documents_the_palette(self):
        readme = (BRAND / "README.md").read_text()
        for colour in (build.CORAL, build.INK, build.PAPER):
            self.assertIn(colour, readme)


if __name__ == "__main__":
    unittest.main()
