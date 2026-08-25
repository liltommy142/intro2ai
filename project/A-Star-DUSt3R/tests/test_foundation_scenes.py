"""Fast contracts for the seven production Manim chapters."""

from __future__ import annotations

import importlib
import importlib.util
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))


class FoundationSceneTests(unittest.TestCase):
    def test_story_chapters_are_importable_manim_scenes(self) -> None:
        """Catch missing or renamed chapters before a costly render."""
        scene_classes = {
            "scenes.intro": "IntroScene",
            "scenes.classical_geometry": "ClassicalGeometryScene",
            "scenes.pointmap": "PointmapScene",
            "scenes.pairwise": "PairwiseScene",
            "scenes.network": "NetworkScene",
            "scenes.global_alignment": "GlobalAlignmentScene",
            "scenes.takeaways": "TakeawaysScene",
        }

        from manim import Scene

        for module_name, class_name in scene_classes.items():
            with self.subTest(module=module_name):
                self.assertIsNotNone(importlib.util.find_spec(module_name))
                module = importlib.import_module(module_name)
                self.assertTrue(issubclass(getattr(module, class_name), Scene))

    def test_visual_language_has_real_pixel_to_point_geometry(self) -> None:
        """The central metaphor must be data-driven, not a text placeholder."""
        visuals = importlib.import_module("scenes.visuals")

        grid = visuals.make_pixel_grid(rows=3, cols=4, cell_size=0.2)
        points = visuals.make_pointmap_positions(rows=3, cols=4)

        self.assertEqual(len(grid), 12)
        self.assertEqual(len(points), 12)
        self.assertGreater(len({round(point[2], 3) for point in points}), 3)
        self.assertEqual(visuals.PALETTE["view_1"], "#42C6FF")
        self.assertEqual(visuals.PALETTE["view_2"], "#FFB84D")

    def test_scene_sources_do_not_require_a_latex_installation(self) -> None:
        """This workspace intentionally renders equations with Pango text."""
        scene_dir = PROJECT_ROOT / "src" / "scenes"
        for source in scene_dir.glob("*.py"):
            self.assertNotIn("MathTex", source.read_text(encoding="utf-8"))

    def test_network_scene_constructs_without_mobject_type_errors(self) -> None:
        """Execute every animation endpoint without writing a movie."""
        from manim import tempconfig
        from scenes.network import NetworkScene

        with tempconfig(
            {
                "dry_run": True,
                "disable_caching": True,
                "skip_animations": True,
                "write_to_movie": False,
            }
        ):
            NetworkScene().render()

    def test_render_entry_point_exposes_every_chapter(self) -> None:
        """Manim must discover individual chapters as well as FullVideo."""
        expected = {
            "IntroScene",
            "ClassicalGeometryScene",
            "PointmapScene",
            "PairwiseScene",
            "NetworkScene",
            "GlobalAlignmentScene",
            "TakeawaysScene",
            "FullVideo",
        }
        from manim import tempconfig
        from manim.utils.module_ops import scene_classes_from_file

        with tempconfig({"scene_names": sorted(expected)}):
            discovered = {
                scene.__name__
                for scene in scene_classes_from_file(PROJECT_ROOT / "render.py")
            }
        self.assertEqual(discovered, expected)


if __name__ == "__main__":
    unittest.main()
