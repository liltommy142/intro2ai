"""A geometric view of DUSt3R's post-processing global alignment."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Line,
    RoundedRectangle,
    Scene,
    Text,
    Transform,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    chapter_title,
    label_pill,
    make_axes,
    make_point_cloud,
    make_pointmap_positions,
)


def _image_node(index: int, center: np.ndarray) -> VGroup:
    """A compact view node, deliberately abstract rather than a paper screenshot."""
    accent = PALETTE["view_1"] if index % 2 == 0 else PALETTE["view_2"]
    tile = RoundedRectangle(
        width=0.58,
        height=0.44,
        corner_radius=0.07,
        stroke_color=accent,
        stroke_width=1.8,
        fill_color=PALETTE["surface_2"],
        fill_opacity=1,
    )
    horizon = Line(LEFT * 0.2, RIGHT * 0.2, color=PALETTE["muted"], stroke_width=1)
    horizon.move_to(tile).shift(DOWN * 0.05)
    tag = Text(str(index + 1), font_size=16, color=PALETTE["ink"]).next_to(tile, DOWN, buff=0.06)
    return VGroup(tile, horizon, tag).move_to(center)


class GlobalAlignmentScene(Scene):
    """Align noisy pair frames into one shared world coordinate frame."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]

        heading = chapter_title(
            "06 · Hậu xử lý đa ảnh",
            "Từ nhiều pair-frame đến một thế giới",
            accent=PALETTE["world"],
        )
        heading.to_corner(UP + LEFT, buff=0.42)
        self.play(FadeIn(heading, shift=DOWN * 0.12))

        node_centers = [
            LEFT * 5.45 + UP * 1.4,
            LEFT * 4.2 + UP * 2.2,
            LEFT * 3.45 + UP * 0.65,
            LEFT * 4.55 + DOWN * 0.95,
            LEFT * 5.8 + DOWN * 0.55,
        ]
        nodes = VGroup(*[_image_node(index, center) for index, center in enumerate(node_centers)])
        pairs = [(0, 1), (1, 2), (0, 3), (2, 3), (3, 4), (0, 4)]
        graph_edges = VGroup()
        for edge_index, (first, second) in enumerate(pairs):
            line = Line(
                nodes[first].get_center(),
                nodes[second].get_center(),
                color=PALETTE["low_confidence"] if edge_index == 4 else PALETTE["pair_frame"],
                stroke_width=2.2,
                stroke_opacity=0.88 if edge_index != 4 else 0.2,
            )
            graph_edges.add(line)
        graph_label = label_pill("graph các cặp liên quan", accent=PALETTE["pair_frame"], font_size=18)
        graph_label.next_to(nodes, DOWN, buff=0.2)
        self.play(Create(graph_edges), FadeIn(nodes), FadeIn(graph_label))

        pair_tag = label_pill("pointmap theo cặp · frame cục bộ", accent=PALETTE["pair_frame"], font_size=20)
        pair_tag.move_to(RIGHT * 1.25 + UP * 2.15)
        positions = make_pointmap_positions(rows=4, cols=6)
        cloud_specs = [
            (RIGHT * 0.25 + UP * 0.65, 0.48, 0.18),
            (RIGHT * 2.25 + UP * 0.3, 0.43, -0.24),
            (RIGHT * 1.25 + DOWN * 1.12, 0.45, 0.1),
        ]
        local_clouds = VGroup()
        for center, scale, angle in cloud_specs:
            cloud = make_point_cloud(positions, color=PALETTE["pair_frame"], radius=0.035, scale=scale)
            cloud.rotate(angle).move_to(center)
            local_clouds.add(cloud)
        local_clouds[2].set_opacity(0.24)
        local_frame_axes = VGroup(*[make_axes(PALETTE["pair_frame"], length=0.3).move_to(cloud.get_center()) for cloud in local_clouds])
        local_frame_axes[2].set_opacity(0.24)
        self.play(FadeIn(pair_tag), FadeIn(local_clouds, scale=0.82), FadeIn(local_frame_axes))

        world_anchor = RIGHT * 1.15 + DOWN * 0.05
        world_axes = make_axes(PALETTE["world"], length=0.78, labels=True).move_to(world_anchor)
        world_label = label_pill("hệ tọa độ toàn cục", accent=PALETTE["world"], font_size=21)
        world_label.next_to(world_axes, UP, buff=0.24)
        residuals = VGroup()
        residual_targets = [
            world_anchor + np.array([-0.55, 0.25, 0]),
            world_anchor + np.array([0.62, 0.07, 0]),
            world_anchor + np.array([-0.05, -0.55, 0]),
        ]
        for cloud, target in zip(local_clouds, residual_targets):
            residuals.add(Line(cloud.get_center(), target, color=PALETTE["low_confidence"], stroke_width=3.2))
        self.play(Create(world_axes), FadeIn(world_label), Create(residuals))

        aligned_clouds = VGroup()
        for index, target in enumerate(residual_targets):
            aligned = make_point_cloud(positions, color=PALETTE["world"], radius=0.037, scale=0.53)
            aligned.rotate(0.03 * (index - 1)).move_to(target)
            aligned_clouds.add(aligned)
        residual_dots = VGroup(*[
            make_point_cloud([(0, 0, 0)], color=PALETTE["low_confidence"], radius=0.012).move_to(target)
            for target in residual_targets
        ])
        self.play(
            *[Transform(source, target) for source, target in zip(local_clouds, aligned_clouds)],
            *[Transform(axis, make_axes(PALETTE["world"], length=0.22).move_to(target)) for axis, target in zip(local_frame_axes, residual_targets)],
            *[Transform(residual, dot) for residual, dot in zip(residuals, residual_dots)],
            FadeOut(pair_tag),
            run_time=1.7,
        )

        postprocess = label_pill("hậu xử lý · global alignment", accent=PALETTE["confidence"], font_size=19)
        postprocess.move_to(RIGHT * 1.15 + DOWN * 2.0)
        gauge = Text("gauge: ∏ σₑ = 1", font_size=23, color=PALETTE["ink"])
        gauge.next_to(postprocess, DOWN, buff=0.13)
        self.play(FadeIn(postprocess, shift=UP * 0.12), FadeIn(gauge))

        inset = RoundedRectangle(
            width=4.15,
            height=1.52,
            corner_radius=0.14,
            stroke_color=PALETTE["surface_2"],
            stroke_width=1.4,
            fill_color=PALETTE["surface"],
            fill_opacity=0.96,
        ).to_edge(RIGHT, buff=0.24).shift(DOWN * 0.2)
        inset_title = Text("residual đang đo gì?", font_size=17, color=PALETTE["muted"])
        inset_title.next_to(inset, UP, buff=0.08).align_to(inset, LEFT)
        divider = Line(inset.get_top() + DOWN * 0.72, inset.get_bottom() + UP * 0.18, color=PALETTE["surface_2"], stroke_width=1)
        divider.move_to(inset.get_center())

        ba_label = Text("BA · residual 2D", font_size=14, color=PALETTE["pose"])
        ba_label.move_to(inset.get_center() + LEFT * 1.02 + UP * 0.38)
        ba_target = make_point_cloud([(0, 0, 0)], color=PALETTE["ink"], radius=0.05).move_to(inset.get_center() + LEFT * 1.18 + DOWN * 0.16)
        ba_prediction = make_point_cloud([(0, 0, 0)], color=PALETTE["pose"], radius=0.045).move_to(inset.get_center() + LEFT * 0.68 + DOWN * 0.03)
        ba_residual = Line(ba_target.get_center(), ba_prediction.get_center(), color=PALETTE["low_confidence"], stroke_width=2.5)

        ga_label = Text("GA · residual 3D", font_size=14, color=PALETTE["world"])
        ga_label.move_to(inset.get_center() + RIGHT * 1.02 + UP * 0.38)
        ga_axes = make_axes(PALETTE["world"], length=0.3).move_to(inset.get_center() + RIGHT * 0.75 + DOWN * 0.18)
        ga_target = make_point_cloud([(0, 0, 0)], color=PALETTE["ink"], radius=0.05).move_to(ga_axes.get_center())
        ga_prediction = make_point_cloud([(0, 0, 0)], color=PALETTE["pair_frame"], radius=0.045).move_to(ga_axes.get_center() + RIGHT * 0.48 + UP * 0.2)
        ga_residual = Line(ga_target.get_center(), ga_prediction.get_center(), color=PALETTE["low_confidence"], stroke_width=2.5)
        self.play(
            FadeIn(inset),
            FadeIn(inset_title),
            FadeIn(ba_label),
            FadeIn(ba_target),
            FadeIn(ba_prediction),
            Create(ba_residual),
            FadeIn(ga_label),
            FadeIn(ga_axes),
            FadeIn(ga_target),
            FadeIn(ga_prediction),
            Create(ga_residual),
        )
        self.play(
            Transform(ba_residual, Line(ba_target.get_center(), ba_target.get_center(), color=PALETTE["confidence"])),
            Transform(ga_residual, Line(ga_target.get_center(), ga_target.get_center(), color=PALETTE["confidence"])),
            ga_prediction.animate.move_to(ga_target),
            ba_prediction.animate.move_to(ba_target),
            run_time=0.9,
        )
        self.wait(0.7)
