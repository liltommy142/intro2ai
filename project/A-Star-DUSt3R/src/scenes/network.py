"""Chapter 5 — two transformer branches exchange evidence."""

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
    Flash,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Scene,
    ShowPassingFlash,
    Text,
    Transform,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    chapter_title,
    confidence_halo,
    label_pill,
    make_point_cloud,
    make_pointmap_positions,
    make_token_grid,
)


class NetworkScene(Scene):
    """Make cross-attention visible without turning the chapter into a diagram."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]
        heading = chapter_title(
            "05 · Kiến trúc",
            "Để hai ảnh thật sự đối thoại",
            accent=PALETTE["pose"],
        ).to_corner(UP + LEFT, buff=0.45)
        self.play(FadeIn(heading, shift=RIGHT * 0.2))

        tokens_a = make_token_grid(PALETTE["view_1"]).scale(0.95).shift(LEFT * 4.7 + UP * 1.05)
        tokens_b = make_token_grid(PALETTE["view_2"]).scale(0.95).shift(LEFT * 4.7 + DOWN * 1.05)
        labels = VGroup(
            label_pill("I₁ patches", accent=PALETTE["view_1"], font_size=18).next_to(tokens_a, LEFT),
            label_pill("I₂ patches", accent=PALETTE["view_2"], font_size=18).next_to(tokens_b, LEFT),
        )
        self.play(
            LaggedStart(*[FadeIn(token, scale=0.6) for token in tokens_a], lag_ratio=0.03),
            LaggedStart(*[FadeIn(token, scale=0.6) for token in tokens_b], lag_ratio=0.03),
            FadeIn(labels),
            run_time=1.4,
        )

        enc_a = RoundedRectangle(
            width=1.35,
            height=1.05,
            corner_radius=0.15,
            stroke_color=PALETTE["view_1"],
            fill_color=PALETTE["surface_2"],
            fill_opacity=1,
        ).move_to(LEFT * 2.45 + UP * 1.05)
        enc_b = enc_a.copy().set_stroke(PALETTE["view_2"]).move_to(LEFT * 2.45 + DOWN * 1.05)
        enc_text_a = Text("ViT encoder", font_size=20, color=PALETTE["ink"]).move_to(enc_a)
        enc_text_b = enc_text_a.copy().move_to(enc_b)
        shared = Line(enc_a.get_bottom(), enc_b.get_top(), color=PALETTE["world"], stroke_width=4)
        shared_note = Text("shared weights", font_size=18, color=PALETTE["world"])
        shared_note.next_to(shared, RIGHT, buff=0.12)
        self.play(
            tokens_a.animate.move_to(enc_a),
            tokens_b.animate.move_to(enc_b),
            FadeOut(labels),
            FadeIn(VGroup(enc_a, enc_b, enc_text_a, enc_text_b)),
            run_time=1.1,
        )
        self.play(Create(shared), FadeIn(shared_note), run_time=0.7)
        self.play(Indicate(enc_a, color=PALETTE["world"]), Indicate(enc_b, color=PALETTE["world"]))

        decoded_a = make_token_grid(PALETTE["view_1"]).move_to(RIGHT * 0.45 + UP * 1.05)
        decoded_b = make_token_grid(PALETTE["view_2"]).move_to(RIGHT * 0.45 + DOWN * 1.05)
        lane_a = Line(enc_a.get_right(), decoded_a.get_left(), color=PALETTE["view_1"], stroke_opacity=0.55)
        lane_b = Line(enc_b.get_right(), decoded_b.get_left(), color=PALETTE["view_2"], stroke_opacity=0.55)
        self.play(
            Transform(tokens_a, decoded_a),
            Transform(tokens_b, decoded_b),
            Create(lane_a),
            Create(lane_b),
            FadeOut(VGroup(enc_text_a, enc_text_b)),
            run_time=1.3,
        )

        self_note_a = label_pill("self-attention", accent=PALETTE["view_1"], font_size=17).next_to(tokens_a, UP)
        self_note_b = label_pill("self-attention", accent=PALETTE["view_2"], font_size=17).next_to(tokens_b, DOWN)
        self.play(FadeIn(self_note_a), FadeIn(self_note_b))
        self.play(
            LaggedStart(*[Indicate(tokens_a[i], color=PALETTE["view_1"], scale_factor=1.3) for i in (1, 7, 12)], lag_ratio=0.15),
            LaggedStart(*[Indicate(tokens_b[i], color=PALETTE["view_2"], scale_factor=1.3) for i in (2, 8, 13)], lag_ratio=0.15),
            run_time=1.2,
        )

        cross_pairs = ((1, 3), (6, 8), (9, 10), (13, 12))
        attention_lines = VGroup(
            *[
                Line(
                    tokens_a[a].get_center(),
                    tokens_b[b].get_center(),
                    color=PALETTE["pose"],
                    stroke_width=2.2,
                    stroke_opacity=0.38,
                )
                for a, b in cross_pairs
            ]
        )
        cross_note = label_pill("cross-attention", accent=PALETTE["pose"], font_size=19)
        cross_note.move_to(RIGHT * 2.1)
        self.play(FadeOut(VGroup(self_note_a, self_note_b)), FadeIn(cross_note))
        self.play(Create(attention_lines), run_time=0.8)
        for _ in range(2):
            self.play(
                *[
                    ShowPassingFlash(line.copy().set_stroke(width=6, opacity=1), time_width=0.45)
                    for line in attention_lines
                ],
                run_time=0.9,
            )
            self.play(
                LaggedStart(*[Flash(tokens_b[b], color=PALETTE["pose"], flash_radius=0.28) for _, b in cross_pairs], lag_ratio=0.12),
                run_time=0.8,
            )

        repeat = Text("lặp qua nhiều decoder blocks", font_size=20, color=PALETTE["muted"])
        repeat.next_to(cross_note, DOWN, buff=0.18)
        self.play(FadeIn(repeat))

        head_a = label_pill("3D + C", accent=PALETTE["view_1"], font_size=19).move_to(RIGHT * 3.05 + UP * 1.05)
        head_b = label_pill("3D + C", accent=PALETTE["view_2"], font_size=19).move_to(RIGHT * 3.05 + DOWN * 1.05)
        arrows = VGroup(
            Arrow(tokens_a.get_right(), head_a.get_left(), buff=0.1, color=PALETTE["view_1"]),
            Arrow(tokens_b.get_right(), head_b.get_left(), buff=0.1, color=PALETTE["view_2"]),
        )
        self.play(FadeIn(head_a), FadeIn(head_b), Create(arrows), run_time=0.8)

        positions = make_pointmap_positions(rows=4, cols=5)
        output_a = make_point_cloud(positions, color=PALETTE["view_1"], radius=0.04, scale=0.55)
        output_b = make_point_cloud(positions, color=PALETTE["view_2"], radius=0.04, scale=0.55)
        output_a.move_to(RIGHT * 5.3 + UP * 1.05)
        output_b.move_to(RIGHT * 5.3 + DOWN * 1.05)
        self.play(
            ReplacementTransform(head_a, output_a),
            ReplacementTransform(head_b, output_b),
            FadeOut(arrows),
            run_time=1.2,
        )
        halos = VGroup(
            confidence_halo(output_a[3], 0.9),
            confidence_halo(output_a[15], 0.25),
            confidence_halo(output_b[7], 0.8),
            confidence_halo(output_b[19], 0.2),
        )
        self.play(LaggedStart(*[FadeIn(halo, scale=0.3) for halo in halos], lag_ratio=0.12))

        pipeline = VGroup(
            enc_a,
            enc_b,
            shared,
            shared_note,
            lane_a,
            lane_b,
            tokens_a,
            tokens_b,
            attention_lines,
            cross_note,
            repeat,
            output_a,
            output_b,
            halos,
        )
        self.play(pipeline.animate.scale(0.78).shift(UP * 0.12), run_time=1.0)

        training_strip = Rectangle(
            width=11.7,
            height=1.05,
            stroke_color=PALETTE["surface_2"],
            fill_color=PALETTE["surface"],
            fill_opacity=0.96,
        ).to_edge(DOWN, buff=0.3)
        train_text = Text(
            "8.5M image pairs  ·  scale-normalized 3D regression  ·  C·error − α log C",
            font_size=22,
            color=PALETTE["ink"],
        ).move_to(training_strip)
        train_emphasis = Text(
            "confidence là trọng số học được — không phải xác suất đã calibrated",
            font_size=18,
            color=PALETTE["confidence"],
        ).next_to(training_strip, DOWN, buff=0.1)
        self.play(FadeIn(training_strip, shift=UP * 0.2), FadeIn(train_text))
        self.play(FadeIn(train_emphasis))
        self.wait(1.2)

        final = Text(
            "Encoder dùng chung trọng số. Decoder mới là nơi hai view trao đổi.",
            font_size=27,
            color=PALETTE["world"],
            weight="BOLD",
        ).to_edge(DOWN, buff=0.42)
        self.play(FadeOut(VGroup(training_strip, train_text, train_emphasis)), FadeIn(final))
        self.play(
            ShowPassingFlash(attention_lines.copy().set_stroke(width=7, opacity=1), time_width=0.6),
            run_time=1.4,
        )
        self.wait(0.8)
        self.play(FadeOut(VGroup(heading, pipeline, final)), run_time=0.9)
