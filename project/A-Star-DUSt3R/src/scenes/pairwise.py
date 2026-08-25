"""Chapter 4 — the two views are predicted in one reference frame."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Brace,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    Scene,
    Text,
    Transform,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    chapter_title,
    confidence_halo,
    label_pill,
    make_axes,
    make_point_cloud,
    make_pointmap_positions,
)


class PairwiseScene(Scene):
    """Show why X¹,¹ and X²,¹ are more useful than independent depths."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]
        heading = chapter_title(
            "04 · Pairwise prediction",
            "Hai lời khai, một hệ tọa độ",
            accent=PALETTE["view_2"],
        ).to_corner(UP + LEFT, buff=0.45)
        self.play(FadeIn(heading, shift=RIGHT * 0.2))

        positions = make_pointmap_positions(rows=5, cols=7)
        cloud_a = make_point_cloud(positions, color=PALETTE["view_1"], radius=0.052, scale=0.84)
        cloud_b = make_point_cloud(positions, color=PALETTE["view_2"], radius=0.052, scale=0.84)
        cloud_a.shift(LEFT * 3.4 + DOWN * 0.25)
        cloud_b.rotate(0.28).scale(1.15).shift(RIGHT * 3.3 + DOWN * 0.05)

        axes_a = make_axes(PALETTE["view_1"], length=0.65, labels=True).next_to(cloud_a, DOWN, buff=0.15)
        axes_b = make_axes(PALETTE["view_2"], length=0.65, labels=True).next_to(cloud_b, DOWN, buff=0.15)
        local_a = label_pill("frame camera 1", accent=PALETTE["view_1"], font_size=19).next_to(cloud_a, UP)
        local_b = label_pill("frame camera 2", accent=PALETTE["view_2"], font_size=19).next_to(cloud_b, UP)

        self.play(
            LaggedStart(*[FadeIn(dot, scale=0.4) for dot in cloud_a], lag_ratio=0.02),
            LaggedStart(*[FadeIn(dot, scale=0.4) for dot in cloud_b], lag_ratio=0.02),
            FadeIn(axes_a),
            FadeIn(axes_b),
            run_time=1.8,
        )
        self.play(FadeIn(local_a), FadeIn(local_b))

        question = Text(
            "Hai depth map riêng → hai frame riêng",
            font_size=25,
            color=PALETTE["muted"],
        ).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(question))
        self.play(Indicate(axes_a), Indicate(axes_b), run_time=0.9)

        equation = Text(
            "f(I₁, I₂)  →  X¹,¹   +   X²,¹   +   confidence",
            font_size=31,
            color=PALETTE["ink"],
            weight="BOLD",
        ).to_edge(UP, buff=1.45)
        frame_note = Text(
            "cả hai output đều ở frame camera 1",
            font_size=23,
            color=PALETTE["view_1"],
        ).next_to(equation, DOWN, buff=0.15)
        self.play(Transform(question, equation), FadeIn(frame_note, shift=UP * 0.1), run_time=1.1)

        target_a = make_point_cloud(positions, color=PALETTE["view_1"], radius=0.056, scale=1.05)
        target_b = make_point_cloud(positions, color=PALETTE["view_2"], radius=0.047, scale=1.05)
        target_a.move_to(DOWN * 0.2)
        target_b.move_to(DOWN * 0.2 + RIGHT * 0.08 + UP * 0.03)
        common_axes = make_axes(PALETTE["view_1"], length=0.85, labels=True)
        common_axes.next_to(target_a, DOWN + LEFT, buff=-0.02)

        residuals = VGroup(
            *[
                Line(
                    target_a[i].get_center(),
                    target_b[i].get_center(),
                    color=PALETTE["confidence"],
                    stroke_opacity=0.38,
                    stroke_width=1.2,
                )
                for i in range(0, len(target_a), 5)
            ]
        )
        self.play(
            Transform(cloud_a, target_a),
            Transform(cloud_b, target_b),
            FadeOut(VGroup(axes_a, axes_b, local_a, local_b)),
            FadeIn(common_axes),
            run_time=2.0,
        )
        self.play(Create(residuals), run_time=0.8)
        self.play(Indicate(VGroup(cloud_a, cloud_b), color=PALETTE["world"], scale_factor=1.04))

        selected = [cloud_b[index] for index in (2, 12, 17, 23, 32)]
        levels = [0.2, 0.9, 1.0, 0.55, 0.15]
        halos = VGroup(*[confidence_halo(dot, level) for dot, level in zip(selected, levels)])
        conf_label = label_pill("confidence theo pixel", accent=PALETTE["confidence"], font_size=20)
        conf_label.move_to(RIGHT * 4.65 + DOWN * 2.25)
        self.play(LaggedStart(*[GrowFromCenter(halo) for halo in halos], lag_ratio=0.12), FadeIn(conf_label))
        self.play(
            selected[0].animate.set_opacity(0.28),
            selected[-1].animate.set_opacity(0.28),
            halos[0].animate.set_stroke(opacity=0.2),
            halos[-1].animate.set_stroke(opacity=0.2),
            run_time=0.9,
        )

        scale_cloud = VGroup(cloud_a.copy(), cloud_b.copy(), residuals.copy()).set_opacity(0.25)
        scale_cloud.scale(1.3).move_to(VGroup(cloud_a, cloud_b))
        scale_brace = Brace(scale_cloud, RIGHT, color=PALETTE["pair_frame"])
        scale_text = Text(
            "cùng hình dạng · chưa có metric scale",
            font_size=22,
            color=PALETTE["pair_frame"],
        ).next_to(scale_brace, RIGHT, buff=0.16)
        self.play(FadeIn(scale_cloud), FadeIn(scale_brace), FadeIn(scale_text), run_time=1.0)
        self.play(scale_cloud.animate.scale(1 / 1.3).move_to(VGroup(cloud_a, cloud_b)), run_time=1.2)

        normalized = Text(
            "loss so sánh hình học sau chuẩn hóa scale",
            font_size=24,
            color=PALETTE["ink"],
        ).to_edge(DOWN, buff=0.38)
        self.play(
            FadeOut(VGroup(scale_brace, scale_text, conf_label, frame_note)),
            FadeOut(scale_cloud),
            FadeIn(normalized, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(1.0)

        takeaway = Text(
            "Hai pointmap · cùng frame ảnh 1",
            font_size=32,
            color=PALETTE["world"],
            weight="BOLD",
        ).to_edge(DOWN, buff=0.4)
        self.play(Transform(normalized, takeaway), run_time=1.0)
        self.play(
            LaggedStart(*[Indicate(VGroup(cloud_a[i], cloud_b[i]), color=PALETTE["world"]) for i in (5, 12, 19, 27)], lag_ratio=0.18),
            run_time=1.8,
        )
        self.wait(1.0)
        self.play(
            FadeOut(VGroup(heading, question, normalized, cloud_a, cloud_b, common_axes, residuals, halos)),
            run_time=0.9,
        )
