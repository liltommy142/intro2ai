from manim import *
import numpy as np

from theme import *


class Scene08Architecture(Scene):
    """
    00:00-00:05
    "DUSt3R là một neural network dựa trên Transformer."

    00:05-00:10
    "Hai ảnh đi qua một Vision Transformer encoder dùng chung weights."

    00:10-00:14
    "Sau đó hai decoder trao đổi thông tin bằng cross-attention."

    00:15-00:20
    "Ta có thể hình dung mỗi branch như một người quan sát scene
    từ một góc khác."

    00:21-00:28
    "Mỗi bên tự hiểu view của mình, rồi liên tục hỏi bên kia:
    những gì tôi thấy liên quan thế nào đến những gì bạn thấy?"

    00:28-00:31
    "Cuối cùng, mỗi branch dự đoán một pointmap và một confidence map."

    00:32-00:40
    "Architecture trả lời câu hỏi “How?”, nhưng pointmap mới là lý do
    “Why?” khiến DUSt3R có thể unify nhiều bài toán."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_scene()

        self.sentence_1()
        self.wait_until(5.0)

        self.sentence_2()
        self.wait_until(10.0)

        self.sentence_3()
        self.wait_until(15.0)

        self.sentence_4()
        self.wait_until(21.0)

        self.sentence_5()
        self.wait_until(28.0)

        self.sentence_6()
        self.wait_until(32.0)

        self.sentence_7()
        self.wait_until(40.0)

    # =========================================================
    # TIMELINE
    # =========================================================

    def play_timed(self, *animations, run_time=1.0, **kwargs):
        self.play(
            *animations,
            run_time=run_time,
            **kwargs,
        )
        self.t += run_time

    def wait_timed(self, duration):
        if duration > 0:
            self.wait(duration)
            self.t += duration

    def wait_until(self, timestamp):
        remaining = timestamp - self.t

        if remaining > 0:
            self.wait_timed(remaining)

    # =========================================================
    # SETUP
    # =========================================================

    def setup_scene(self):
        self.image_a = self.make_image_card(
            accent=CYAN,
            variant=0,
        )

        self.image_b = self.make_image_card(
            accent=VIOLET,
            variant=1,
        )

        self.image_a.scale(0.62)
        self.image_b.scale(0.62)

        self.image_a.move_to(
            LEFT * 3.8 + UP * 1.65
        )

        self.image_b.move_to(
            RIGHT * 3.8 + UP * 1.65
        )

    # =========================================================
    # 00:00 -> 00:05
    #
    # "DUSt3R là một neural network dựa trên Transformer."
    # =========================================================

    def sentence_1(self):

        title = Text(
            "DUSt3R",
            font_size=30,
            color=WHITE,
        )

        title.move_to(
            UP * 2.6
        )

        # Tokens instead of boring neural-network circles.
        tokens = VGroup()

        for i in range(11):
            token = RoundedRectangle(
                width=0.34,
                height=0.34,
                corner_radius=0.05,
                stroke_color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    i / 10,
                ),
                stroke_width=0.8,
                stroke_opacity=0.40,
                fill_color=SURFACE_2,
                fill_opacity=0.70,
            )

            tokens.add(
                token
            )

        tokens.arrange(
            RIGHT,
            buff=0.10,
        )

        tokens.move_to(
            ORIGIN
        )

        self.play_timed(
            FadeIn(
                title,
                shift=UP * 0.08,
            ),
            run_time=0.45,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        token,
                        scale=0.65,
                    )
                    for token in tokens
                ],
                lag_ratio=0.04,
            ),
            run_time=0.75,
        )

        # Transformer-style all-to-all information exchange.
        links = VGroup()

        link_pairs = [
            (0, 5),
            (1, 8),
            (2, 6),
            (3, 10),
            (4, 7),
            (5, 9),
        ]

        for a, b in link_pairs:
            curve = CubicBezier(
                tokens[a].get_top(),
                tokens[a].get_top() + UP * 0.45,
                tokens[b].get_top() + UP * 0.45,
                tokens[b].get_top(),
            )

            curve.set_stroke(
                CYAN_SOFT,
                width=0.8,
                opacity=0.16,
            )

            links.add(
                curve
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(link)
                    for link in links
                ],
                lag_ratio=0.06,
            ),
            run_time=0.75,
        )

        self.play_timed(
            tokens.animate.scale(1.04),
            links.animate.set_opacity(0.28),
            run_time=0.35,
        )

        transformer = Text(
            "TRANSFORMER",
            font_size=19,
            color=MUTED,
        )

        transformer.next_to(
            tokens,
            DOWN,
            buff=0.30,
        )

        self.play_timed(
            FadeIn(
                transformer,
                shift=UP * 0.05,
            ),
            run_time=0.35,
        )

        self.wait_timed(0.65)

        self.intro_group = VGroup(
            title,
            tokens,
            links,
            transformer,
        )

    # =========================================================
    # 00:05 -> 00:10
    #
    # "Hai ảnh đi qua một Vision Transformer encoder
    # dùng chung weights."
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            FadeOut(
                self.intro_group
            ),
            FadeIn(
                self.image_a,
                shift=DOWN * 0.08,
            ),
            FadeIn(
                self.image_b,
                shift=DOWN * 0.08,
            ),
            run_time=0.55,
        )

        encoder = self.make_encoder()

        encoder.move_to(
            ORIGIN + DOWN * 0.20
        )

        input_a = Arrow(
            self.image_a.get_bottom(),
            encoder.get_left() + LEFT * 0.05 + UP * 0.18,
            buff=0.12,
            color=CYAN,
            stroke_width=1.3,
            max_tip_length_to_length_ratio=0.08,
        )

        input_b = Arrow(
            self.image_b.get_bottom(),
            encoder.get_right() + RIGHT * 0.05 + UP * 0.18,
            buff=0.12,
            color=VIOLET,
            stroke_width=1.3,
            max_tip_length_to_length_ratio=0.08,
        )

        self.play_timed(
            Create(
                input_a
            ),
            Create(
                input_b
            ),
            FadeIn(
                encoder,
                scale=0.94,
            ),
            run_time=0.75,
        )

        # Image patches turn into token streams.
        stream_a = self.make_token_stream(
            CYAN,
            count=7,
        )

        stream_b = self.make_token_stream(
            VIOLET,
            count=7,
        )

        stream_a.move_to(
            LEFT * 1.65 + DOWN * 0.20
        )

        stream_b.move_to(
            RIGHT * 1.65 + DOWN * 0.20
        )

        self.play_timed(
            LaggedStart(
                *[
                    GrowFromCenter(t)
                    for t in stream_a
                ],
                lag_ratio=0.05,
            ),
            LaggedStart(
                *[
                    GrowFromCenter(t)
                    for t in stream_b
                ],
                lag_ratio=0.05,
            ),
            run_time=0.65,
        )

        shared = Text(
            "shared weights",
            font_size=17,
            color=CYAN_SOFT,
        )

        shared.next_to(
            encoder,
            DOWN,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(
                shared,
                shift=UP * 0.05,
            ),
            run_time=0.35,
        )

        # Same encoder pulses once for both branches.
        pulse = encoder[0].copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.5,
            opacity=0.65,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.28,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.45)

        self.encoder = encoder
        self.encoder_input_a = input_a
        self.encoder_input_b = input_b
        self.stream_a = stream_a
        self.stream_b = stream_b
        self.shared_label = shared

    # =========================================================
    # 00:10 -> 00:14
    #
    # "Sau đó hai decoder trao đổi thông tin bằng cross-attention."
    # =========================================================

    def sentence_3(self):

        self.play_timed(
            self.image_a.animate.set_opacity(0.22),
            self.image_b.animate.set_opacity(0.22),
            self.encoder.animate.scale(0.82).shift(UP * 0.65),
            self.stream_a.animate.shift(LEFT * 1.25 + DOWN * 0.65),
            self.stream_b.animate.shift(RIGHT * 1.25 + DOWN * 0.65),
            FadeOut(
                self.shared_label
            ),
            run_time=0.50,
        )

        decoder_a = self.make_decoder(
            CYAN
        )

        decoder_b = self.make_decoder(
            VIOLET
        )

        decoder_a.move_to(
            LEFT * 2.45 + DOWN * 0.85
        )

        decoder_b.move_to(
            RIGHT * 2.45 + DOWN * 0.85
        )

        self.play_timed(
            FadeIn(
                decoder_a,
                scale=0.92,
            ),
            FadeIn(
                decoder_b,
                scale=0.92,
            ),
            run_time=0.55,
        )

        # Cross-attention links.
        cross_1 = CubicBezier(
            decoder_a.get_right(),
            decoder_a.get_right() + RIGHT * 0.9 + UP * 0.55,
            decoder_b.get_left() + LEFT * 0.9 + UP * 0.55,
            decoder_b.get_left(),
        )

        cross_1.set_stroke(
            CYAN_SOFT,
            width=1.4,
            opacity=0.60,
        )

        cross_2 = CubicBezier(
            decoder_b.get_left() + DOWN * 0.08,
            decoder_b.get_left() + LEFT * 0.9 + DOWN * 0.55,
            decoder_a.get_right() + RIGHT * 0.9 + DOWN * 0.55,
            decoder_a.get_right() + DOWN * 0.08,
        )

        cross_2.set_stroke(
            MAGENTA,
            width=1.4,
            opacity=0.55,
        )

        self.play_timed(
            Create(
                cross_1
            ),
            Create(
                cross_2
            ),
            run_time=0.65,
        )

        # Information pulses in opposite directions.
        pulse_1 = cross_1.copy().set_stroke(
            WHITE,
            width=3,
            opacity=0.80,
        )

        pulse_2 = cross_2.copy().set_stroke(
            WHITE,
            width=3,
            opacity=0.80,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse_1,
                time_width=0.22,
            ),
            ShowPassingFlash(
                pulse_2,
                time_width=0.22,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.45)

        self.decoder_a = decoder_a
        self.decoder_b = decoder_b
        self.cross_1 = cross_1
        self.cross_2 = cross_2

    # =========================================================
    # 00:15 -> 00:20
    #
    # "Ta có thể hình dung mỗi branch như một người quan sát
    # scene từ một góc khác."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            self.encoder.animate.set_opacity(0.12),
            self.cross_1.animate.set_opacity(0.16),
            self.cross_2.animate.set_opacity(0.16),
            run_time=0.35,
        )

        observer_a = self.make_observer(
            LEFT * 3.9 + UP * 0.70,
            CYAN,
            angle=-9 * DEGREES,
        )

        observer_b = self.make_observer(
            RIGHT * 3.9 + UP * 0.70,
            VIOLET,
            angle=9 * DEGREES,
        )

        scene_object = self.make_scene_object()

        scene_object.move_to(
            UP * 0.70
        )

        self.play_timed(
            FadeIn(
                observer_a,
                scale=0.85,
            ),
            FadeIn(
                observer_b,
                scale=0.85,
            ),
            FadeIn(
                scene_object,
                scale=0.92,
            ),
            run_time=0.65,
        )

        view_ray_a = Line(
            observer_a[-1].get_center(),
            scene_object.get_center(),
            color=CYAN,
            stroke_width=1,
            stroke_opacity=0.25,
        )

        view_ray_b = Line(
            observer_b[-1].get_center(),
            scene_object.get_center(),
            color=VIOLET,
            stroke_width=1,
            stroke_opacity=0.25,
        )

        self.play_timed(
            Create(
                view_ray_a
            ),
            Create(
                view_ray_b
            ),
            run_time=0.55,
        )

        # Each branch visually inherits one observer.
        link_a = Line(
            observer_a.get_bottom(),
            self.decoder_a.get_top(),
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.28,
        )

        link_b = Line(
            observer_b.get_bottom(),
            self.decoder_b.get_top(),
            color=VIOLET,
            stroke_width=1.0,
            stroke_opacity=0.28,
        )

        self.play_timed(
            Create(
                link_a
            ),
            Create(
                link_b
            ),
            run_time=0.45,
        )

        self.play_timed(
            self.decoder_a.animate.set_opacity(0.95),
            self.decoder_b.animate.set_opacity(0.95),
            run_time=0.35,
        )

        self.wait_timed(0.65)

        self.observer_a = observer_a
        self.observer_b = observer_b
        self.scene_object = scene_object
        self.view_ray_a = view_ray_a
        self.view_ray_b = view_ray_b
        self.observer_link_a = link_a
        self.observer_link_b = link_b

    # =========================================================
    # 00:21 -> 00:28
    #
    # "Mỗi bên tự hiểu view của mình, rồi liên tục hỏi bên kia:
    # những gì tôi thấy liên quan thế nào đến những gì bạn thấy?"
    # =========================================================

    def sentence_5(self):

        # Local understanding first.
        local_a = self.make_feature_cloud(
            self.decoder_a.get_center(),
            CYAN,
            seed=11,
        )

        local_b = self.make_feature_cloud(
            self.decoder_b.get_center(),
            VIOLET,
            seed=17,
        )

        self.play_timed(
            FadeOut(
                self.observer_link_a
            ),
            FadeOut(
                self.observer_link_b
            ),
            LaggedStart(
                *[
                    FadeIn(
                        p,
                        scale=0.4,
                    )
                    for p in local_a
                ],
                lag_ratio=0.04,
            ),
            LaggedStart(
                *[
                    FadeIn(
                        p,
                        scale=0.4,
                    )
                    for p in local_b
                ],
                lag_ratio=0.04,
            ),
            run_time=0.65,
        )

        # First query A -> B
        query_a = self.cross_1.copy()

        query_a.set_stroke(
            CYAN_SOFT,
            width=3.0,
            opacity=0.85,
        )

        self.play_timed(
            ShowPassingFlash(
                query_a,
                time_width=0.18,
            ),
            run_time=0.60,
        )

        # B responds
        query_b = self.cross_2.copy()

        query_b.set_stroke(
            MAGENTA,
            width=3.0,
            opacity=0.85,
        )

        self.play_timed(
            ShowPassingFlash(
                query_b,
                time_width=0.18,
            ),
            run_time=0.60,
        )

        # Repeated exchange.
        for _ in range(2):

            pulse_a = self.cross_1.copy().set_stroke(
                WHITE,
                width=2.6,
                opacity=0.70,
            )

            pulse_b = self.cross_2.copy().set_stroke(
                WHITE,
                width=2.6,
                opacity=0.70,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse_a,
                    time_width=0.16,
                ),
                ShowPassingFlash(
                    pulse_b,
                    time_width=0.16,
                ),
                run_time=0.55,
            )

        # Features reorganize as context is exchanged.
        self.play_timed(
            local_a.animate.scale(1.10),
            local_b.animate.scale(1.10),
            self.cross_1.animate.set_opacity(0.55),
            self.cross_2.animate.set_opacity(0.55),
            run_time=0.45,
        )

        # Link feature structures between branches.
        correspondences = VGroup()

        for i in [1, 4, 7]:
            j = (i + 2) % len(local_b)

            relation = Line(
                local_a[i].get_center(),
                local_b[j].get_center(),
                color=WHITE,
                stroke_width=0.8,
                stroke_opacity=0.14,
            )

            correspondences.add(
                relation
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(r)
                    for r in correspondences
                ],
                lag_ratio=0.16,
            ),
            run_time=0.65,
        )

        self.play_timed(
            correspondences.animate.set_opacity(
                0.32
            ),
            run_time=0.35,
        )

        self.wait_timed(0.80)

        self.local_a = local_a
        self.local_b = local_b
        self.feature_relations = correspondences

    # =========================================================
    # 00:28 -> 00:31
    #
    # "Cuối cùng, mỗi branch dự đoán một pointmap
    # và một confidence map."
    # =========================================================

    def sentence_6(self):

        self.play_timed(
            FadeOut(
                self.observer_a
            ),
            FadeOut(
                self.observer_b
            ),
            FadeOut(
                self.scene_object
            ),
            FadeOut(
                self.view_ray_a
            ),
            FadeOut(
                self.view_ray_b
            ),
            FadeOut(
                self.feature_relations
            ),
            self.decoder_a.animate.shift(
                UP * 0.65
            ),
            self.decoder_b.animate.shift(
                UP * 0.65
            ),
            run_time=0.45,
        )

        pointmap_a = self.make_pointmap(
            LEFT * 3.0 + DOWN * 1.25,
            CYAN,
            BLUE,
            seed=21,
        )

        pointmap_b = self.make_pointmap(
            RIGHT * 3.0 + DOWN * 1.25,
            VIOLET,
            MAGENTA,
            seed=29,
        )

        confidence_a = self.make_confidence_strip(
            pointmap_a.get_bottom()
            + DOWN * 0.35,
            CYAN,
            seed=7,
        )

        confidence_b = self.make_confidence_strip(
            pointmap_b.get_bottom()
            + DOWN * 0.35,
            VIOLET,
            seed=9,
        )

        arrow_a = Arrow(
            self.decoder_a.get_bottom(),
            pointmap_a.get_top(),
            buff=0.12,
            color=CYAN,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.08,
        )

        arrow_b = Arrow(
            self.decoder_b.get_bottom(),
            pointmap_b.get_top(),
            buff=0.12,
            color=VIOLET,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.08,
        )

        self.play_timed(
            Create(
                arrow_a
            ),
            Create(
                arrow_b
            ),
            FadeIn(
                pointmap_a,
                shift=DOWN * 0.10,
            ),
            FadeIn(
                pointmap_b,
                shift=DOWN * 0.10,
            ),
            run_time=0.70,
        )

        self.play_timed(
            FadeIn(
                confidence_a,
                shift=UP * 0.05,
            ),
            FadeIn(
                confidence_b,
                shift=UP * 0.05,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.35)

        self.pointmap_a = pointmap_a
        self.pointmap_b = pointmap_b
        self.confidence_a = confidence_a
        self.confidence_b = confidence_b

        self.output_arrow_a = arrow_a
        self.output_arrow_b = arrow_b

    # =========================================================
    # 00:32 -> 00:40
    #
    # "Architecture trả lời câu hỏi How?,
    # nhưng pointmap mới là lý do Why?..."
    # =========================================================

    def sentence_7(self):

        # First expose HOW: network machinery.
        architecture_group = VGroup(
            self.encoder,
            self.decoder_a,
            self.decoder_b,
            self.cross_1,
            self.cross_2,
            self.local_a,
            self.local_b,
            self.output_arrow_a,
            self.output_arrow_b,
        )

        how = Text(
            "HOW?",
            font_size=31,
            color=MUTED,
        )

        how.move_to(
            UP * 2.6
        )

        self.play_timed(
            FadeIn(
                how,
                shift=DOWN * 0.06,
            ),
            architecture_group.animate.set_opacity(
                0.72
            ),
            run_time=0.50,
        )

        self.play_timed(
            architecture_group.animate.set_opacity(
                0.12
            ),
            how.animate.set_opacity(
                0.18
            ),
            self.pointmap_a.animate.scale(
                1.10
            ),
            self.pointmap_b.animate.scale(
                1.10
            ),
            run_time=0.65,
        )

        # WHY becomes pointmap representation itself.
        why = Text(
            "WHY?",
            font_size=34,
            color=WHITE,
        )

        why.move_to(
            UP * 2.6
        )

        self.play_timed(
            Transform(
                how,
                why
            ),
            run_time=0.45,
        )

        # Confidence maps become secondary.
        self.play_timed(
            self.confidence_a.animate.set_opacity(
                0.30
            ),
            self.confidence_b.animate.set_opacity(
                0.30
            ),
            self.pointmap_a.animate.set_opacity(
                1.0
            ),
            self.pointmap_b.animate.set_opacity(
                1.0
            ),
            run_time=0.45,
        )

        # Pointmaps move inward and visually fuse into one representation idea.
        self.play_timed(
            self.pointmap_a.animate.move_to(
                LEFT * 1.75 + DOWN * 0.55
            ),
            self.pointmap_b.animate.move_to(
                RIGHT * 1.75 + DOWN * 0.55
            ),
            run_time=0.60,
        )

        bridge = Line(
            self.pointmap_a.get_right(),
            self.pointmap_b.get_left(),
            color=WHITE,
            stroke_width=1.2,
            stroke_opacity=0.30,
        )

        self.play_timed(
            Create(
                bridge
            ),
            run_time=0.40,
        )

        # Several downstream tasks emerge from pointmaps.
        task_names = [
            "pose",
            "depth",
            "matching",
            "3D",
        ]

        tasks = VGroup()

        task_positions = [
            LEFT * 4.3 + DOWN * 2.55,
            LEFT * 1.45 + DOWN * 2.55,
            RIGHT * 1.45 + DOWN * 2.55,
            RIGHT * 4.3 + DOWN * 2.55,
        ]

        pointmap_center = (
            self.pointmap_a.get_center()
            + self.pointmap_b.get_center()
        ) / 2

        task_links = VGroup()

        for name, pos in zip(
            task_names,
            task_positions,
        ):
            task = Text(
                name,
                font_size=18,
                color=MUTED,
            )

            task.move_to(
                pos
            )

            tasks.add(
                task
            )

            link = Line(
                pointmap_center,
                task.get_top(),
                color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    (
                        pos[0] + 5
                    ) / 10,
                ),
                stroke_width=0.9,
                stroke_opacity=0.16,
            )

            task_links.add(
                link
            )

        self.play_timed(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(link),
                        FadeIn(
                            task,
                            shift=UP * 0.05,
                        ),
                    )
                    for link, task in zip(
                        task_links,
                        tasks,
                    )
                ],
                lag_ratio=0.12,
            ),
            run_time=1.00,
        )

        # Final pointmap emphasis.
        pulse_a = self.pointmap_a[0].copy()

        pulse_a.set_stroke(
            CYAN_SOFT,
            width=2.0,
            opacity=0.55,
        )

        pulse_b = self.pointmap_b[0].copy()

        pulse_b.set_stroke(
            MAGENTA,
            width=2.0,
            opacity=0.55,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse_a,
                time_width=0.22,
            ),
            ShowPassingFlash(
                pulse_b,
                time_width=0.22,
            ),
            run_time=0.55,
        )

        self.play_timed(
            tasks.animate.set_opacity(
                0.70
            ),
            run_time=0.35,
        )

        self.wait_timed(1.10)

    # =========================================================
    # COMPONENTS
    # =========================================================

    def make_encoder(self):

        body = RoundedRectangle(
            width=3.25,
            height=1.05,
            corner_radius=0.13,
            stroke_color=CYAN,
            stroke_width=1.1,
            stroke_opacity=0.40,
            fill_color=SURFACE,
            fill_opacity=0.96,
        )

        label = Text(
            "ViT ENCODER",
            font_size=20,
            color=WHITE,
        )

        label.move_to(
            body
        )

        return VGroup(
            body,
            label,
        )

    def make_decoder(self, color):

        body = RoundedRectangle(
            width=2.30,
            height=1.10,
            corner_radius=0.13,
            stroke_color=color,
            stroke_width=1.1,
            stroke_opacity=0.48,
            fill_color=SURFACE,
            fill_opacity=0.95,
        )

        label = Text(
            "DECODER",
            font_size=19,
            color=WHITE,
        )

        label.move_to(
            body
        )

        return VGroup(
            body,
            label,
        )

    def make_token_stream(
        self,
        color,
        count=7,
    ):

        group = VGroup()

        for i in range(count):

            token = RoundedRectangle(
                width=0.20,
                height=0.20,
                corner_radius=0.035,
                stroke_color=color,
                stroke_width=0.7,
                stroke_opacity=0.40,
                fill_color=color,
                fill_opacity=0.10,
            )

            group.add(
                token
            )

        group.arrange(
            RIGHT,
            buff=0.07,
        )

        return group

    def make_observer(
        self,
        center,
        color,
        angle=0,
    ):

        center = np.array(
            center,
            dtype=float,
        )

        core = Dot(
            radius=0.045,
            color=color,
        )

        plane = Line(
            LEFT * 0.35,
            RIGHT * 0.35,
            color=color,
            stroke_width=1.2,
        )

        plane.shift(
            UP * 0.45
        )

        frustum = VGroup(
            Line(
                core.get_center(),
                plane.get_left(),
                color=color,
                stroke_width=1,
                stroke_opacity=0.65,
            ),
            Line(
                core.get_center(),
                plane.get_right(),
                color=color,
                stroke_width=1,
                stroke_opacity=0.65,
            ),
            plane,
            core,
        )

        frustum.rotate(
            angle
        )

        frustum.move_to(
            center
        )

        return frustum

    def make_scene_object(self):

        body = RoundedRectangle(
            width=1.65,
            height=0.78,
            corner_radius=0.13,
            stroke_color=WHITE,
            stroke_width=0.8,
            stroke_opacity=0.20,
            fill_color="#3A4355",
            fill_opacity=0.45,
        )

        top = Rectangle(
            width=1.05,
            height=0.38,
            stroke_width=0,
            fill_color="#59657A",
            fill_opacity=0.50,
        )

        top.next_to(
            body,
            UP,
            buff=-0.07,
        )

        return VGroup(
            body,
            top,
        )

    def make_feature_cloud(
        self,
        center,
        color,
        seed,
    ):

        rng = np.random.default_rng(
            seed
        )

        group = VGroup()

        for _ in range(9):

            p = Dot(
                radius=0.022,
                color=color,
            )

            p.move_to(
                center
                + np.array([
                    rng.uniform(-0.70, 0.70),
                    rng.uniform(-0.27, 0.27),
                    0,
                ])
            )

            group.add(
                p
            )

        return group

    def make_pointmap(
        self,
        center,
        color_a,
        color_b,
        seed=1,
    ):

        rows = 5
        cols = 8

        rng = np.random.default_rng(
            seed
        )

        points = VGroup()
        mesh = VGroup()

        positions = []

        for row in range(rows):

            line_positions = []

            for col in range(cols):

                u = col / (
                    cols - 1
                )

                v = row / (
                    rows - 1
                )

                x = (
                    u - 0.5
                ) * 2.65

                y = (
                    0.5 - v
                ) * 1.45

                depth = (
                    0.30
                    + 0.38
                    * np.sin(
                        np.pi * u
                    )
                    * np.cos(
                        np.pi * v
                    )
                    + rng.uniform(
                        -0.025,
                        0.025,
                    )
                )

                p = np.array([
                    center[0]
                    + x
                    + depth * 0.50,

                    center[1]
                    + y
                    + depth * 0.25,

                    0,
                ])

                line_positions.append(
                    p
                )

                color = interpolate_color(
                    ManimColor(color_a),
                    ManimColor(color_b),
                    u,
                )

                points.add(
                    Dot(
                        p,
                        radius=0.024,
                        color=color,
                    )
                )

            positions.append(
                line_positions
            )

        for row in range(rows):
            for col in range(cols - 1):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row][col + 1],
                        color=color_a,
                        stroke_width=0.6,
                        stroke_opacity=0.24,
                    )
                )

        for col in range(cols):
            for row in range(rows - 1):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row + 1][col],
                        color=color_b,
                        stroke_width=0.6,
                        stroke_opacity=0.20,
                    )
                )

        return VGroup(
            mesh,
            points,
        )

    def make_confidence_strip(
        self,
        center,
        color,
        seed=1,
    ):

        rng = np.random.default_rng(
            seed
        )

        cells = VGroup()

        for _ in range(12):

            confidence = rng.uniform(
                0.20,
                1.0,
            )

            cell = Rectangle(
                width=0.18,
                height=0.13,
                stroke_width=0,
                fill_color=color,
                fill_opacity=confidence * 0.70,
            )

            cells.add(
                cell
            )

        cells.arrange(
            RIGHT,
            buff=0.035,
        )

        cells.move_to(
            center
        )

        label = Text(
            "confidence",
            font_size=13,
            color=MUTED,
        )

        label.next_to(
            cells,
            LEFT,
            buff=0.16,
        )

        return VGroup(
            label,
            cells,
        )

    def make_image_card(
        self,
        accent=CYAN,
        variant=0,
    ):

        frame = RoundedRectangle(
            width=4.2,
            height=2.55,
            corner_radius=0.10,
            stroke_color="#303747",
            stroke_width=1,
            fill_color=SURFACE,
            fill_opacity=1,
        )

        floor = Polygon(
            [-2.0, -1.05, 0],
            [2.0, -1.05, 0],
            [0.75 + variant * 0.2, 0.15, 0],
            [-0.75 + variant * 0.2, 0.15, 0],
            fill_color="#1A202C",
            fill_opacity=1,
            stroke_width=0,
        )

        sofa = RoundedRectangle(
            width=1.15,
            height=0.42,
            corner_radius=0.06,
            stroke_width=0,
            fill_color="#5C687E",
            fill_opacity=0.72,
        )

        sofa.move_to(
            LEFT * (
                0.50
                - variant * 0.15
            )
            + DOWN * 0.35
        )

        window = Rectangle(
            width=0.75,
            height=0.62,
            stroke_color=accent,
            stroke_width=0.8,
            stroke_opacity=0.40,
            fill_color=accent,
            fill_opacity=0.025,
        )

        window.move_to(
            RIGHT * (
                1.05
                - variant * 0.15
            )
            + UP * 0.55
        )

        return VGroup(
            frame,
            floor,
            sofa,
            window,
        )