from manim import *
import numpy as np

from theme import *


class Scene13Conclusion(Scene):
    """
    Audio: Đoạn 13.wav
    Duration: 49.83s
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        # audio begins around 0.21s
        self.wait_until(0.21)

        self.sentence_1()
        self.wait_until(4.06)

        self.sentence_2()
        self.wait_until(6.80)

        self.sentence_3()
        self.wait_until(9.41)

        self.sentence_4()
        self.wait_until(13.93)

        self.sentence_5()
        self.wait_until(19.91)

        self.sentence_6()
        self.wait_until(23.32)

        self.sentence_7()
        self.wait_until(30.09)

        self.sentence_8()
        self.wait_until(36.59)

        self.sentence_9()
        self.wait_until(41.49)

        self.sentence_10()
        self.wait_until(44.70)

        self.sentence_11()
        self.wait_until(49.83)

    # =========================================================
    # TIMING
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
    # 00:00.21 -> 00:03.47
    #
    # "không bắt đầu từ Transformer."
    # =========================================================

    def sentence_1(self):

        # Brief callback to architecture.
        encoder = self.make_block(
            "ViT",
            LEFT * 2.2,
            CYAN,
        )
        decoder_a = self.make_block(
            "DECODER",
            RIGHT * 0.2 + UP * 0.65,
            BLUE,
            width=1.75,
        )

        decoder_b = self.make_block(
            "DECODER",
            RIGHT * 0.2 + DOWN * 0.65,
            VIOLET,
            width=1.75,
        )

        link_a = Line(
            encoder.get_right(),
            decoder_a.get_left(),
            color=MUTED,
            stroke_width=1,
            stroke_opacity=0.28,
        )

        link_b = Line(
            encoder.get_right(),
            decoder_b.get_left(),
            color=MUTED,
            stroke_width=1,
            stroke_opacity=0.28,
        )

        cross = Line(
            decoder_a.get_bottom(),
            decoder_b.get_top(),
            color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.35,
        )

        architecture = VGroup(
            encoder,
            decoder_a,
            decoder_b,
            link_a,
            link_b,
            cross,
        )

        self.play_timed(
            FadeIn(
                architecture,
                scale=0.94,
            ),
            run_time=0.75,
        )

        transformer_label = Text(
            "TRANSFORMER",
            font_size=22,
            color=MUTED,
        )

        transformer_label.next_to(
            architecture,
            DOWN,
            buff=0.45,
        )

        self.play_timed(
            FadeIn(
                transformer_label
            ),
            run_time=0.40,
        )

        # Architecture deliberately recedes.
        self.play_timed(
            architecture.animate
            .scale(0.88)
            .set_opacity(0.18),

            transformer_label.animate.set_opacity(
                0.12
            ),

            run_time=0.55,
        )

        self.wait_timed(0.45)

        self.architecture = architecture
        self.transformer_label = transformer_label

    # =========================================================
    # 00:04.06 -> 00:06.19
    #
    # "Tôi sẽ bắt đầu từ representation."
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            FadeOut(
                self.architecture
            ),
            FadeOut(
                self.transformer_label
            ),
            run_time=0.35,
        )

        pointmap = self.make_pointmap(
            center=ORIGIN,
        )

        self.play_timed(
            FadeIn(
                pointmap,
                scale=0.92,
            ),
            run_time=0.65,
        )

        label = Text(
            "REPRESENTATION",
            font_size=23,
            color=WHITE,
        )

        label.next_to(
            pointmap,
            UP,
            buff=0.42,
        )

        self.play_timed(
            FadeIn(
                label,
                shift=UP * 0.06,
            ),
            run_time=0.40,
        )

        pulse = pointmap[0].copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.1,
            opacity=0.55,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.20,
            ),
            run_time=0.45,
        )

        self.pointmap = pointmap
        self.representation_label = label

    # =========================================================
    # 00:06.80 -> 00:08.41
    #
    # "3D vision truyền thống thường cố giải từng câu hỏi riêng:"
    # =========================================================

    def sentence_3(self):

        self.play_timed(
            self.pointmap.animate
            .scale(0.65)
            .move_to(DOWN * 2.35)
            .set_opacity(0.16),

            self.representation_label.animate.set_opacity(
                0.10
            ),

            run_time=0.45,
        )

        classical_label = Text(
            "CLASSICAL 3D VISION",
            font_size=20,
            color=MUTED,
        )

        classical_label.to_edge(
            UP,
            buff=0.55,
        )

        self.play_timed(
            FadeIn(
                classical_label
            ),
            run_time=0.35,
        )

        self.classical_label = classical_label

    # =========================================================
    # 00:09.41 -> 00:13.32
    #
    # matching? camera? depth?
    # =========================================================

    def sentence_4(self):

        matching = self.make_question(
            "MATCHING?",
            LEFT * 4.1 + UP * 0.25,
            CYAN,
        )

        camera = self.make_question(
            "CAMERA?",
            ORIGIN + UP * 0.25,
            VIOLET,
        )

        depth = self.make_question(
            "DEPTH?",
            RIGHT * 4.1 + UP * 0.25,
            MAGENTA,
        )

        questions = VGroup(
            matching,
            camera,
            depth,
        )

        self.play_timed(
            FadeIn(
                matching,
                shift=UP * 0.10,
            ),
            run_time=0.45,
        )

        self.play_timed(
            FadeIn(
                camera,
                shift=UP * 0.10,
            ),
            run_time=0.45,
        )

        self.play_timed(
            FadeIn(
                depth,
                shift=UP * 0.10,
            ),
            run_time=0.45,
        )

        # Visually separate them.
        separators = VGroup(
            DashedLine(
                LEFT * 2.05 + DOWN * 0.75,
                LEFT * 2.05 + UP * 1.25,
                color=DIM,
                stroke_opacity=0.25,
            ),
            DashedLine(
                RIGHT * 2.05 + DOWN * 0.75,
                RIGHT * 2.05 + UP * 1.25,
                color=DIM,
                stroke_opacity=0.25,
            ),
        )

        self.play_timed(
            Create(
                separators
            ),
            run_time=0.45,
        )

        self.wait_timed(0.45)

        self.questions = questions
        self.question_separators = separators

    # =========================================================
    # 00:13.93 -> 00:19.22
    #
    # "rồi ghép các câu trả lời lại để dựng scene."
    # =========================================================

    def sentence_5(self):

        # Answers emerge separately.
        match_result = self.make_small_visual(
            LEFT * 4.1 + DOWN * 1.25,
            CYAN,
            "match",
        )

        pose_result = self.make_small_visual(
            DOWN * 1.25,
            VIOLET,
            "pose",
        )

        depth_result = self.make_small_visual(
            RIGHT * 4.1 + DOWN * 1.25,
            MAGENTA,
            "depth",
        )

        results = VGroup(
            match_result,
            pose_result,
            depth_result,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        r,
                        shift=DOWN * 0.06,
                    )
                    for r in results
                ],
                lag_ratio=0.15,
            ),
            run_time=0.80,
        )

        # Then manually combine toward center.
        merge_lines = VGroup()

        for result in results:

            line = Line(
                result.get_center(),
                DOWN * 0.55,
                color=result[0].get_color(),
                stroke_width=1,
                stroke_opacity=0.20,
            )

            merge_lines.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in merge_lines
                ],
                lag_ratio=0.12,
            ),
            run_time=0.65,
        )

        reconstruction = self.make_pointmap(
            center=DOWN * 0.65,
        )

        reconstruction.scale(
            0.42
        )

        self.play_timed(
            FadeIn(
                reconstruction,
                scale=0.8,
            ),
            run_time=0.60,
        )

        # Feels sequential and assembled.
        for line in merge_lines:

            pulse = line.copy()

            pulse.set_stroke(
                WHITE,
                width=2.4,
                opacity=0.70,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.18,
                ),
                run_time=0.30,
            )

        self.play_timed(
            reconstruction.animate.scale(
                1.12
            ),
            run_time=0.35,
        )

        self.wait_timed(0.45)

        self.classical_results = results
        self.classical_merge_lines = merge_lines
        self.classical_reconstruction = reconstruction

    # =========================================================
    # 00:19.91 -> 00:22.69
    #
    # "DUSt3R thử một thứ tự khác:"
    # =========================================================

    def sentence_6(self):

        # Classical pipeline peels away.
        old_world = VGroup(
            self.classical_label,
            self.questions,
            self.question_separators,
            self.classical_results,
            self.classical_merge_lines,
            self.classical_reconstruction,
        )

        self.play_timed(
            old_world.animate
            .scale(0.82)
            .set_opacity(0.08),

            self.pointmap.animate
            .set_opacity(1.0)
            .scale(1 / 0.65)
            .move_to(ORIGIN),

            run_time=0.70,
        )

        self.play_timed(
            FadeOut(
                old_world
            ),
            run_time=0.35,
        )

        # Clean reset.
        self.play_timed(
            self.pointmap.animate.scale(
                0.92
            ),
            run_time=0.35,
        )

        self.wait_timed(0.35)

    # =========================================================
    # 00:23.32 -> 00:29.45
    #
    # "đặt các pixel vào một representation 3D chung."
    # =========================================================

    def sentence_7(self):

        self.play_timed(
            FadeOut(
                self.pointmap
            ),
            run_time=0.35,
        )

        # 2D image grid.
        grid = self.make_pixel_grid()

        grid.move_to(
            LEFT * 3.2
        )

        self.play_timed(
            FadeIn(
                grid,
                scale=0.96,
            ),
            run_time=0.55,
        )

        # 3D representation destination.
        pointmap = self.make_pointmap(
            center=RIGHT * 2.6,
        )

        pointmap.set_opacity(
            0
        )

        self.add(
            pointmap
        )

        mapping_lines = VGroup()

        sample_indices = [
            5,
            13,
            21,
            29,
            37,
        ]

        target_indices = [
            4,
            11,
            19,
            27,
            34,
        ]

        target_points = pointmap[1]

        for src_idx, dst_idx in zip(
            sample_indices,
            target_indices,
        ):

            line = Line(
                grid[src_idx].get_center(),
                target_points[dst_idx].get_center(),
                color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    src_idx / 40,
                ),
                stroke_width=0.8,
                stroke_opacity=0.20,
            )

            mapping_lines.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in mapping_lines
                ],
                lag_ratio=0.10,
            ),
            run_time=0.75,
        )

        # Full pointmap appears from pixels.
        self.play_timed(
            pointmap.animate.set_opacity(
                0.95
            ),
            grid.animate.set_opacity(
                0.40
            ),
            run_time=0.85,
        )

        # Pixel-to-3D pulses.
        for line in mapping_lines[:3]:

            pulse = line.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.6,
                opacity=0.80,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.20,
                ),
                run_time=0.35,
            )

        self.play_timed(
            pointmap.animate.scale(
                1.05
            ),
            run_time=0.35,
        )

        self.wait_timed(0.45)

        self.final_grid = grid
        self.final_pointmap = pointmap
        self.pixel_mapping_lines = mapping_lines

    # =========================================================
    # 00:30.09 -> 00:35.57
    #
    # "các bài toán ... hệ quả của cùng một geometry."
    # =========================================================

    def sentence_8(self):

        self.play_timed(
            FadeOut(
                self.final_grid
            ),
            FadeOut(
                self.pixel_mapping_lines
            ),
            self.final_pointmap.animate.move_to(
                ORIGIN
            ),
            run_time=0.55,
        )

        # Tasks emerge FROM representation.
        task_data = [
            (
                "DEPTH",
                UP * 2.45,
                CYAN,
            ),
            (
                "MATCHING",
                LEFT * 4.0,
                CYAN_SOFT,
            ),
            (
                "CAMERA POSE",
                RIGHT * 4.0,
                VIOLET,
            ),
            (
                "RECONSTRUCTION",
                DOWN * 2.45,
                MAGENTA,
            ),
        ]

        tasks = VGroup()
        links = VGroup()

        for name, pos, color in task_data:

            task = Text(
                name,
                font_size=18,
                color=color,
            )

            task.move_to(
                pos
            )

            line = Line(
                self.final_pointmap.get_center(),
                task.get_center(),
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.22,
            )

            tasks.add(
                task
            )

            links.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(line),
                        FadeIn(
                            task,
                            scale=0.9,
                        ),
                    )
                    for line, task in zip(
                        links,
                        tasks,
                    )
                ],
                lag_ratio=0.14,
            ),
            run_time=1.20,
        )

        # One geometry, many interpretations.
        for line in links:

            pulse = line.copy()

            pulse.set_stroke(
                WHITE,
                width=2.5,
                opacity=0.70,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.18,
                ),
                run_time=0.25,
            )

        geometry_ring = Circle(
            radius=1.75,
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.13,
        )

        geometry_ring.move_to(
            self.final_pointmap
        )

        self.play_timed(
            Create(
                geometry_ring
            ),
            run_time=0.45,
        )

        self.play_timed(
            tasks.animate.set_opacity(
                0.82
            ),
            self.final_pointmap.animate.scale(
                1.04
            ),
            run_time=0.35,
        )

        self.wait_timed(0.45)

        self.final_tasks = tasks
        self.final_task_links = links
        self.geometry_ring = geometry_ring

    # =========================================================
    # 00:36.59 -> 00:40.90
    #
    # "Geometric 3D Vision Made Easy"
    # =========================================================

    def sentence_9(self):

        self.play_timed(
            self.final_tasks.animate.set_opacity(
                0.18
            ),
            self.final_task_links.animate.set_opacity(
                0.08
            ),
            self.geometry_ring.animate.set_opacity(
                0.08
            ),
            self.final_pointmap.animate
            .scale(0.82)
            .shift(DOWN * 0.8)
            .set_opacity(0.32),
            run_time=0.55,
        )

        title = Text(
            "Geometric 3D Vision",
            font_size=39,
            color=WHITE,
        )

        subtitle = Text(
            "Made Easy",
            font_size=39,
            color=CYAN_SOFT,
        )

        title.move_to(
            UP * 0.75
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.14,
        )

        self.play_timed(
            FadeIn(
                title,
                shift=UP * 0.08,
            ),
            run_time=0.65,
        )

        self.play_timed(
            FadeIn(
                subtitle,
                shift=UP * 0.08,
            ),
            run_time=0.55,
        )

        underline = Line(
            subtitle.get_left(),
            subtitle.get_right(),
            color=VIOLET,
            stroke_width=1.3,
            stroke_opacity=0.55,
        )

        underline.next_to(
            subtitle,
            DOWN,
            buff=0.18,
        )

        self.play_timed(
            Create(
                underline
            ),
            run_time=0.45,
        )

        self.wait_timed(0.50)

        self.paper_title = title
        self.paper_subtitle = subtitle
        self.paper_underline = underline

    # =========================================================
    # 00:41.49 -> 00:44.08
    #
    # "Không phải 3D vision bỗng trở nên dễ."
    # =========================================================

    def sentence_10(self):

        # "Made Easy" loses emphasis for a moment.
        self.play_timed(
            self.paper_subtitle.animate.set_color(
                MUTED
            ),
            self.paper_subtitle.animate.set_opacity(
                0.35
            ),
            run_time=0.45,
        )

        not_magic = Text(
            "not magic",
            font_size=18,
            color=MUTED,
        )

        not_magic.next_to(
            self.paper_subtitle,
            RIGHT,
            buff=0.35,
        )

        self.play_timed(
            FadeIn(
                not_magic
            ),
            run_time=0.35,
        )

        self.play_timed(
            FadeOut(
                not_magic
            ),
            run_time=0.35,
        )

        self.wait_timed(0.35)

    # =========================================================
    # 00:44.70 -> 00:49.83
    #
    # "representation tốt ... nhiều bước đơn giản hơn."
    # =========================================================

    def sentence_11(self):

        self.play_timed(
            FadeOut(
                self.paper_title
            ),
            FadeOut(
                self.paper_subtitle
            ),
            FadeOut(
                self.paper_underline
            ),
            FadeOut(
                self.final_tasks
            ),
            FadeOut(
                self.final_task_links
            ),
            FadeOut(
                self.geometry_ring
            ),

            self.final_pointmap.animate
            .move_to(ORIGIN)
            .scale(1.20)
            .set_opacity(1),

            run_time=0.70,
        )

        # Final thesis:
        # complex pipeline collapses into one representation.
        labels = VGroup(
            Text(
                "matching",
                font_size=17,
                color=CYAN,
            ),
            Text(
                "depth",
                font_size=17,
                color=CYAN_SOFT,
            ),
            Text(
                "pose",
                font_size=17,
                color=VIOLET,
            ),
            Text(
                "reconstruction",
                font_size=17,
                color=MAGENTA,
            ),
        )

        labels[0].move_to(
            LEFT * 4.6 + UP * 1.4
        )

        labels[1].move_to(
            LEFT * 4.6 + DOWN * 1.4
        )

        labels[2].move_to(
            RIGHT * 4.6 + UP * 1.4
        )

        labels[3].move_to(
            RIGHT * 4.6 + DOWN * 1.4
        )

        self.play_timed(
            FadeIn(
                labels
            ),
            run_time=0.45,
        )

        # Everything collapses into representation.
        self.play_timed(
            labels[0].animate
            .move_to(self.final_pointmap)
            .scale(0.40)
            .set_opacity(0),

            labels[1].animate
            .move_to(self.final_pointmap)
            .scale(0.40)
            .set_opacity(0),

            labels[2].animate
            .move_to(self.final_pointmap)
            .scale(0.40)
            .set_opacity(0),

            labels[3].animate
            .move_to(self.final_pointmap)
            .scale(0.40)
            .set_opacity(0),

            run_time=1.20,
            rate_func=smooth,
        )

        # Pointmap gives final subtle pulse.
        pulse = self.final_pointmap[0].copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.5,
            opacity=0.65,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.20,
            ),
            run_time=0.55,
        )

        dust3r = Text(
            "DUSt3R",
            font_size=34,
            color=WHITE,
        )

        dust3r.next_to(
            self.final_pointmap,
            DOWN,
            buff=0.50,
        )

        tagline = Text(
            "Geometric 3D Vision Made Easy",
            font_size=18,
            color=MUTED,
        )

        tagline.next_to(
            dust3r,
            DOWN,
            buff=0.14,
        )

        self.play_timed(
            FadeIn(
                dust3r,
                shift=UP * 0.07,
            ),
            FadeIn(
                tagline,
                shift=UP * 0.05,
            ),
            run_time=0.65,
        )

        # Let final frame breathe.
        self.wait_timed(0.85)

    # =========================================================
    # HELPERS
    # =========================================================

    def make_block(
        self,
        label,
        center,
        color,
        width=1.45,
    ):

        box = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.10,
            stroke_color=color,
            stroke_width=1,
            stroke_opacity=0.40,
            fill_color=SURFACE,
            fill_opacity=0.90,
        )

        text = Text(
            label,
            font_size=17,
            color=WHITE,
        )

        group = VGroup(
            box,
            text,
        )

        text.move_to(
            box
        )

        group.move_to(
            center
        )

        return group

    def make_question(
        self,
        text,
        center,
        color,
    ):

        dot = Dot(
            radius=0.045,
            color=color,
        )

        label = Text(
            text,
            font_size=22,
            color=WHITE,
        )

        group = VGroup(
            dot,
            label,
        ).arrange(
            DOWN,
            buff=0.20,
        )

        group.move_to(
            center
        )

        return group

    def make_small_visual(
        self,
        center,
        color,
        mode,
    ):

        if mode == "match":

            left = Dot(
                LEFT * 0.35,
                radius=0.035,
                color=color,
            )

            right = Dot(
                RIGHT * 0.35,
                radius=0.035,
                color=color,
            )

            line = Line(
                left,
                right,
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.45,
            )

            group = VGroup(
                line,
                left,
                right,
            )

        elif mode == "pose":

            origin = Dot(
                radius=0.035,
                color=color,
            )

            arm = Line(
                origin,
                RIGHT * 0.55,
                color=color,
                stroke_width=1.2,
            )

            group = VGroup(
                origin,
                arm,
            )

        else:

            bars = VGroup()

            heights = [
                0.25,
                0.45,
                0.70,
                0.42,
            ]

            for h in heights:

                bar = Rectangle(
                    width=0.13,
                    height=h,
                    stroke_width=0,
                    fill_color=color,
                    fill_opacity=0.65,
                )

                bars.add(
                    bar
                )

            bars.arrange(
                RIGHT,
                buff=0.08,
                aligned_edge=DOWN,
            )

            group = bars

        group.move_to(
            center
        )

        return group

    def make_pixel_grid(self):

        rows = 5
        cols = 8

        grid = VGroup()

        for row in range(rows):

            for col in range(cols):

                u = col / (
                    cols - 1
                )

                v = row / (
                    rows - 1
                )

                color = interpolate_color(
                    ManimColor("#273343"),
                    ManimColor("#64768B"),
                    0.60 * u + 0.20 * v,
                )

                cell = Square(
                    side_length=0.36,
                    stroke_color="#596273",
                    stroke_width=0.4,
                    stroke_opacity=0.20,
                    fill_color=color,
                    fill_opacity=0.90,
                )

                grid.add(
                    cell
                )

        grid.arrange_in_grid(
            rows=rows,
            cols=cols,
            buff=0.025,
        )

        return grid

    def make_pointmap(
        self,
        center,
    ):

        rows = 5
        cols = 8

        points = VGroup()
        mesh = VGroup()

        positions = []

        for row in range(rows):

            current = []

            for col in range(cols):

                u = col / (
                    cols - 1
                )

                v = row / (
                    rows - 1
                )

                x = (
                    u - 0.5
                ) * 3.5

                y = (
                    0.5 - v
                ) * 2.0

                depth = (
                    0.38
                    + 0.48
                    * np.sin(
                        np.pi * u
                    )
                    * np.cos(
                        np.pi * v
                    )
                )

                p = np.array([
                    center[0]
                    + x
                    + depth * 0.55,

                    center[1]
                    + y
                    + depth * 0.28,

                    0,
                ])

                current.append(
                    p
                )

                color = interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    u,
                )

                points.add(
                    Dot(
                        p,
                        radius=0.028,
                        color=color,
                    )
                )

            positions.append(
                current
            )

        # horizontal topology
        for row in range(rows):

            for col in range(
                cols - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row][col + 1],
                        color=CYAN,
                        stroke_width=0.65,
                        stroke_opacity=0.20,
                    )
                )

        # vertical topology
        for col in range(cols):

            for row in range(
                rows - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row + 1][col],
                        color=VIOLET,
                        stroke_width=0.65,
                        stroke_opacity=0.18,
                    )
                )

        return VGroup(
            mesh,
            points,
        )
