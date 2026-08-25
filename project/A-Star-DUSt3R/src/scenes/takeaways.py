"""Final DUSt3R takeaways, with benchmark claims kept in their exact settings."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Line,
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
    make_benchmark_glyph,
    make_camera,
    make_pixel_grid,
    make_point_cloud,
    make_pointmap_positions,
)


def _depth_icon() -> VGroup:
    bars = VGroup()
    for index, height in enumerate((0.28, 0.5, 0.82, 0.58)):
        bar = Line(DOWN * height / 2, UP * height / 2, color=PALETTE["confidence"], stroke_width=7)
        bar.shift(RIGHT * (index - 1.5) * 0.18)
        bars.add(bar)
    return VGroup(bars, Text("độ sâu = z", font_size=18, color=PALETTE["ink"]).next_to(bars, DOWN, buff=0.15))


def _matching_icon() -> VGroup:
    left = VGroup(*[make_point_cloud([(0, 0, 0)], color=PALETTE["view_1"], radius=0.045).shift(LEFT * 0.38 + UP * offset) for offset in (0.19, 0, -0.19)])
    right = VGroup(*[make_point_cloud([(0, 0, 0)], color=PALETTE["view_2"], radius=0.045).shift(RIGHT * 0.38 + UP * offset) for offset in (0.19, 0, -0.19)])
    links = VGroup(*[Line(first.get_center(), second.get_center(), color=PALETTE["pair_frame"], stroke_width=1.7) for first, second in zip(left, right)])
    return VGroup(left, right, links, Text("mutual NN", font_size=18, color=PALETTE["ink"]).next_to(links, DOWN, buff=0.18))


def _pose_icon() -> VGroup:
    camera = make_camera(PALETTE["pose"], scale=0.7).shift(LEFT * 0.28)
    axes = make_axes(PALETTE["world"], length=0.35).shift(RIGHT * 0.37)
    label = Text("focal + pose", font_size=18, color=PALETTE["ink"])
    label.next_to(VGroup(camera, axes), DOWN, buff=0.16)
    return VGroup(camera, axes, label)


def _multiview_icon() -> VGroup:
    positions = make_pointmap_positions(rows=2, cols=3)
    local_a = make_point_cloud(positions, color=PALETTE["pair_frame"], radius=0.032, scale=0.28).shift(LEFT * 0.36 + UP * 0.1)
    local_b = make_point_cloud(positions, color=PALETTE["pair_frame"], radius=0.032, scale=0.28).shift(LEFT * 0.16 + DOWN * 0.23)
    world = make_point_cloud(positions, color=PALETTE["world"], radius=0.035, scale=0.3).shift(RIGHT * 0.4)
    arrow = Arrow(LEFT * 0.02, RIGHT * 0.22, color=PALETTE["confidence"], buff=0.02, stroke_width=2.3)
    label = Text("đa ảnh", font_size=18, color=PALETTE["ink"])
    label.next_to(VGroup(local_a, local_b, world), DOWN, buff=0.14)
    return VGroup(local_a, local_b, arrow, world, label)


class TakeawaysScene(Scene):
    """Close with the pointmap's downstream products and scoped evidence."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]
        heading = chapter_title(
            "07 · Kết quả và kết luận",
            "Pointmap là một giao diện hình học",
            accent=PALETTE["view_1"],
        )
        heading.to_corner(UP + LEFT, buff=0.42)
        self.play(FadeIn(heading, shift=DOWN * 0.12))

        pixels = make_pixel_grid(rows=4, cols=5, cell_size=0.24, view_color=PALETTE["view_1"], variant=1)
        pixels.move_to(LEFT * 0.95 + UP * 0.2)
        cloud = make_point_cloud(make_pointmap_positions(rows=4, cols=5), color=PALETTE["world"], radius=0.043, scale=0.46)
        cloud.move_to(RIGHT * 0.9 + UP * 0.2)
        arrow = Arrow(pixels.get_right(), cloud.get_left(), color=PALETTE["pair_frame"], buff=0.2, stroke_width=3)
        core_label = label_pill("pointmap · mỗi pixel một điểm 3D", accent=PALETTE["world"], font_size=20)
        core_label.next_to(VGroup(pixels, cloud), DOWN, buff=0.28)
        self.play(FadeIn(pixels), Create(arrow), FadeIn(cloud, scale=0.75), FadeIn(core_label))

        core = VGroup(pixels, arrow, cloud, core_label)
        destinations = [
            LEFT * 4.6 + UP * 1.5,
            RIGHT * 4.55 + UP * 1.5,
            LEFT * 4.6 + DOWN * 1.5,
            RIGHT * 4.55 + DOWN * 1.5,
        ]
        icons = VGroup(_depth_icon(), _matching_icon(), _pose_icon(), _multiview_icon())
        spokes = VGroup()
        for icon, destination in zip(icons, destinations):
            icon.move_to(destination)
            spokes.add(Arrow(cloud.get_center(), icon.get_center(), color=PALETTE["muted"], buff=0.22, stroke_width=1.8))
        self.play(core.animate.scale(0.8).shift(UP * 0.18), run_time=0.55)
        self.play(
            *[Create(spoke) for spoke in spokes],
            *[FadeIn(icon, scale=0.78) for icon in icons],
            run_time=1.35,
        )

        evidence_label = label_pill("một model · nhiều đầu ra hình học", accent=PALETTE["confidence"], font_size=19)
        evidence_label.move_to(DOWN * 2.95)
        self.play(FadeIn(evidence_label))
        self.wait(0.35)

        branches = VGroup(core, icons, spokes, evidence_label)
        dimmed_branches = branches.copy().set_opacity(0.08).scale(0.86).shift(UP * 0.1)
        self.play(Transform(branches, dimmed_branches), run_time=0.65)

        nyud = make_benchmark_glyph(
            "NYUD-v2",
            "6.50\n94.09",
            "Rel↓ / δ1.25↑ · transfer",
            accent=PALETTE["confidence"],
        ).scale(0.82)
        pose = make_benchmark_glyph(
            "CO3Dv2 · GA",
            "96.2\n86.8",
            "RRA@15 / RTA@15 · 10 frames",
            accent=PALETTE["pose"],
        ).scale(0.82)
        dtu = make_benchmark_glyph(
            "DTU · zero-shot",
            "2.677\n.805\n1.741",
            "accuracy / completeness / overall · mm",
            accent=PALETTE["world"],
        ).scale(0.71)
        metrics = VGroup(nyud, pose, dtu).arrange(RIGHT, buff=1.0)
        metrics.move_to(DOWN * 0.15)
        for glyph in metrics:
            self.play(FadeIn(glyph, scale=0.72), run_time=0.55)

        dtu_caveat = Text("sau GT evaluation alignment · đánh đổi accuracy chuyên biệt", font_size=17, color=PALETTE["muted"])
        dtu_caveat.next_to(dtu, DOWN, buff=0.36)
        self.play(FadeIn(dtu_caveat, shift=UP * 0.08))

        self.play(FadeOut(branches), FadeOut(metrics), FadeOut(dtu_caveat), FadeOut(heading), run_time=0.55)
        camera = make_camera(PALETTE["muted"], scale=1.2).shift(LEFT * 3.1)
        prerequisite = Text("camera setup\nđiều kiện đầu vào", font_size=28, color=PALETTE["muted"], line_spacing=0.8)
        prerequisite.next_to(camera, DOWN, buff=0.28)
        transition = Arrow(LEFT * 0.75, RIGHT * 0.75, color=PALETTE["world"], buff=0.1, stroke_width=4)
        downstream_axes = make_axes(PALETTE["world"], length=0.72, labels=True).shift(RIGHT * 3.05)
        downstream = Text("camera setup\nđại lượng có thể suy ra", font_size=28, color=PALETTE["ink"], line_spacing=0.8)
        downstream.next_to(downstream_axes, DOWN, buff=0.28)
        final_line = Text("DUSt3R thay đổi thứ cần biết trước.", font_size=32, color=PALETTE["ink"], weight="BOLD")
        final_line.to_edge(DOWN, buff=0.55)
        citation = Text(
            "Wang et al. · DUSt3R · CVPR 2024",
            font_size=18,
            color=PALETTE["muted"],
        ).to_edge(UP, buff=0.48)
        self.play(FadeIn(camera), FadeIn(prerequisite), Create(transition), FadeIn(downstream_axes), FadeIn(downstream))
        self.play(FadeIn(final_line, shift=UP * 0.14))
        self.play(FadeIn(citation), run_time=0.6)
        self.wait(1.2)
