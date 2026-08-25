"""Seven independently renderable chapters for the DUSt3R video."""

from scenes.classical_geometry import ClassicalGeometryScene
from scenes.global_alignment import GlobalAlignmentScene
from scenes.intro import IntroScene
from scenes.network import NetworkScene
from scenes.pairwise import PairwiseScene
from scenes.pointmap import PointmapScene
from scenes.takeaways import TakeawaysScene


CHAPTERS = (
    IntroScene,
    ClassicalGeometryScene,
    PointmapScene,
    PairwiseScene,
    NetworkScene,
    GlobalAlignmentScene,
    TakeawaysScene,
)

__all__ = [scene.__name__ for scene in CHAPTERS] + ["CHAPTERS"]
