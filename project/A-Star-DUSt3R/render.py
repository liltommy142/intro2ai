"""Single Manim entry point for chapter previews and the complete animatic."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import Scene


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from scenes import (  # noqa: E402  (src is intentionally added above)
    ClassicalGeometryScene as _ClassicalGeometryScene,
    GlobalAlignmentScene as _GlobalAlignmentScene,
    IntroScene as _IntroScene,
    NetworkScene as _NetworkScene,
    PairwiseScene as _PairwiseScene,
    PointmapScene as _PointmapScene,
    TakeawaysScene as _TakeawaysScene,
)


class IntroScene(_IntroScene):
    """CLI-discoverable proxy for chapter 1."""


class ClassicalGeometryScene(_ClassicalGeometryScene):
    """CLI-discoverable proxy for chapter 2."""


class PointmapScene(_PointmapScene):
    """CLI-discoverable proxy for chapter 3."""


class PairwiseScene(_PairwiseScene):
    """CLI-discoverable proxy for chapter 4."""


class NetworkScene(_NetworkScene):
    """CLI-discoverable proxy for chapter 5."""


class GlobalAlignmentScene(_GlobalAlignmentScene):
    """CLI-discoverable proxy for chapter 6."""


class TakeawaysScene(_TakeawaysScene):
    """CLI-discoverable proxy for chapter 7."""


CHAPTERS = (
    IntroScene,
    ClassicalGeometryScene,
    PointmapScene,
    PairwiseScene,
    NetworkScene,
    GlobalAlignmentScene,
    TakeawaysScene,
)


class FullVideo(Scene):
    """Render all seven chapters in narrative order.

    This is the visual animatic. Final pauses are synced after the recorded
    narration is available; the production script targets 9:20.
    """

    def construct(self) -> None:
        for index, chapter in enumerate(CHAPTERS):
            chapter.construct(self)
            if index < len(CHAPTERS) - 1:
                self.clear()


__all__ = [
    "IntroScene",
    "ClassicalGeometryScene",
    "PointmapScene",
    "PairwiseScene",
    "NetworkScene",
    "GlobalAlignmentScene",
    "TakeawaysScene",
    "FullVideo",
]
