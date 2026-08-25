"""Chapter 3 — a pixel field becomes a field of 3D coordinates."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Scene,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    chapter_title,
    label_pill,
    make_axes,
    make_pixel_grid,
    make_point_cloud,
    make_pointmap_positions,
)


class PointmapScene(Scene):
    """Explain the W×H×3 representation by preserving pixel identity."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]

        heading = chapter_title(
            "03 · Đổi câu hỏi",
            "Mỗi pixel nằm ở đâu trong 3D?",
            accent=PALETTE["view_1"],
        ).to_corner(UP + LEFT, buff=0.45)
        self.play(FadeIn(heading, shift=RIGHT * 0.2), run_time=0.8)

        grid = make_pixel_grid(rows=5, cols=7, cell_size=0.42)
        grid.shift(LEFT * 3.7 + DOWN * 0.35)
        image_tag = label_pill("ảnh RGB", accent=PALETTE["view_1"], font_size=20)
        image_tag.next_to(grid, DOWN, buff=0.22)
        self.play(LaggedStart(*[FadeIn(cell, scale=0.75) for cell in grid], lag_ratio=0.025))
        self.play(FadeIn(image_tag), run_time=0.5)

        hero_index = 17
        hero = grid[hero_index]
        self.play(Indicate(hero, color=PALETTE["world"], scale_factor=1.35), run_time=0.9)

        pixel_copy = hero.copy().scale(1.55).move_to(RIGHT * 0.25 + UP * 0.75)
        rgb = Text("(r, g, b)", font_size=25, color=PALETTE["muted"])
        rgb.next_to(pixel_copy, UP, buff=0.16)
        self.play(TransformFromCopy(hero, pixel_copy), FadeIn(rgb, shift=UP * 0.1))

        origin = pixel_copy.get_center() + RIGHT * 0.45
        ray = Line(origin, RIGHT * 3.25 + DOWN * 0.1, color=PALETTE["muted"], stroke_opacity=0.5)
        depth_point = Dot(ray.point_from_proportion(0.68), radius=0.075, color=PALETTE["view_1"])
        depth_arrow = Arrow(
            origin,
            depth_point.get_center(),
            buff=0.05,
            color=PALETTE["view_1"],
            stroke_width=3,
        )
        depth_label = Text("depth: một số d", font_size=25, color=PALETTE["view_1"])
        depth_label.next_to(depth_arrow, DOWN, buff=0.18)
        self.play(Create(ray), GrowArrow(depth_arrow), FadeIn(depth_point), FadeIn(depth_label))
        self.wait(0.8)

        axes = make_axes(PALETTE["world"], length=0.78, labels=True)
        axes.move_to(depth_point)
        xyz = Text("pointmap: (x, y, z)", font_size=27, color=PALETTE["world"])
        xyz.next_to(axes, DOWN, buff=0.28)
        self.play(
            FadeOut(depth_arrow),
            Transform(depth_label, xyz),
            FadeIn(axes, scale=0.5),
            run_time=1.1,
        )
        self.play(Indicate(VGroup(depth_point, axes), color=PALETTE["world"]), run_time=0.8)

        self.play(
            FadeOut(VGroup(pixel_copy, rgb, ray, depth_point, axes, depth_label)),
            grid.animate.shift(LEFT * 0.15),
            run_time=0.8,
        )

        positions = make_pointmap_positions(rows=5, cols=7)
        cloud = make_point_cloud(
            positions,
            color=PALETTE["view_1"],
            radius=0.065,
            scale=1.08,
        ).shift(RIGHT * 3.05 + DOWN * 0.2)
        cloud_tag = label_pill("pointmap  H × W × 3", accent=PALETTE["world"], font_size=20)
        cloud_tag.next_to(cloud, DOWN, buff=0.32)

        bridges = VGroup()
        for index in (7, 12, 17, 22, 27):
            bridges.add(
                Line(
                    grid[index].get_center(),
                    cloud[index].get_center(),
                    color=PALETTE["muted"],
                    stroke_width=1.2,
                    stroke_opacity=0.35,
                )
            )
        self.play(
            LaggedStart(
                *[TransformFromCopy(grid[index], cloud[index]) for index in range(len(grid))],
                lag_ratio=0.025,
            ),
            run_time=2.2,
        )
        self.play(Create(bridges), FadeIn(cloud_tag), run_time=1.0)

        correspondence = Text(
            "pixel  ↔  điểm 3D",
            font_size=28,
            color=PALETTE["ink"],
            weight="BOLD",
        ).move_to(DOWN * 3.15)
        one_to_one = Text(
            "không phải point cloud vô danh",
            font_size=21,
            color=PALETTE["muted"],
        ).next_to(correspondence, DOWN, buff=0.12)
        self.play(FadeIn(correspondence, shift=UP * 0.15), FadeIn(one_to_one))
        self.play(
            LaggedStart(
                *[Indicate(VGroup(grid[i], cloud[i]), color=PALETTE["world"], scale_factor=1.2) for i in (7, 17, 27)],
                lag_ratio=0.35,
            ),
            run_time=2.0,
        )
        self.wait(1.2)

        self.play(
            FadeOut(VGroup(heading, grid, image_tag, bridges, cloud_tag, correspondence, one_to_one)),
            cloud.animate.move_to(ORIGIN).scale(1.25).rotate(-0.12),
            run_time=1.2,
        )
        reveal = Text(
            "DUSt3R hồi quy hình học trực tiếp",
            font_size=36,
            color=PALETTE["ink"],
            weight="BOLD",
        ).to_edge(DOWN, buff=0.62)
        self.play(FadeIn(reveal, shift=UP * 0.2), cloud.animate.rotate(0.24), run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(VGroup(cloud, reveal)), run_time=0.8)
