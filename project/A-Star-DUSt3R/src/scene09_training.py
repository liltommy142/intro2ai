from manim import *
import numpy as np

from theme import *


class Scene09Training(Scene):
    """
    Audio: Đoạn 9.wav
    Duration: 33.80s

    00:00.00-00:07.17
    "Trong lúc training, DUSt3R không cần một bộ loss riêng
    cho từng task như depth, pose hay matching."

    00:07.75-00:08.99
    "Ý tưởng chính đơn giản hơn:"

    00:09.55-00:14.75
    "predicted 3D point càng xa ground-truth 3D point,
    loss càng lớn."

    00:15.74-00:22.11
    "Vì scale tuyệt đối có thể mơ hồ,
    prediction và ground truth được normalize trước khi so sánh."

    00:22.84-00:27.65
    "Và vì không phải pixel nào cũng dễ,
    model còn học một confidence cho từng pixel."

    00:28.51-00:33.80
    "Nó vừa học reconstruction,
    vừa học vùng nào trong reconstruction đáng tin hơn."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.sentence_1()
        self.wait_until(7.75)

        self.sentence_2()
        self.wait_until(9.55)

        self.sentence_3()
        self.wait_until(15.74)

        self.sentence_4()
        self.wait_until(22.84)

        self.sentence_5()
        self.wait_until(28.51)

        self.sentence_6()
        self.wait_until(33.80)

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
    # 00:00 -> 00:07.17
    #
    # "không cần một bộ loss riêng cho từng task..."
    # =========================================================

    def sentence_1(self):

        # Pointmap ở trung tâm: đây mới là thứ model train.
        pointmap = self.make_pointmap(
            center=ORIGIN + UP * 0.25,
        )

        self.play_timed(
            FadeIn(
                pointmap,
                scale=0.96,
            ),
            run_time=0.70,
        )

        # Ba task truyền thống xuất hiện xung quanh.
        depth = self.make_task(
            "DEPTH",
            LEFT * 4.2 + DOWN * 1.75,
            CYAN,
        )

        pose = self.make_task(
            "POSE",
            DOWN * 2.05,
            VIOLET,
        )

        matching = self.make_task(
            "MATCHING",
            RIGHT * 4.2 + DOWN * 1.75,
            MAGENTA,
        )

        tasks = VGroup(
            depth,
            pose,
            matching,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        task,
                        shift=UP * 0.08,
                    )
                    for task in tasks
                ],
                lag_ratio=0.12,
            ),
            run_time=0.75,
        )

        # Mỗi task giả sử có loss riêng.
        loss_depth = MathTex(
            r"\mathcal{L}_{depth}",
            font_size=24,
            color=CYAN,
        ).next_to(
            depth,
            UP,
            buff=0.15,
        )

        loss_pose = MathTex(
            r"\mathcal{L}_{pose}",
            font_size=24,
            color=VIOLET,
        ).next_to(
            pose,
            UP,
            buff=0.15,
        )

        loss_matching = MathTex(
            r"\mathcal{L}_{match}",
            font_size=24,
            color=MAGENTA,
        ).next_to(
            matching,
            UP,
            buff=0.15,
        )

        losses = VGroup(
            loss_depth,
            loss_pose,
            loss_matching,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(x)
                    for x in losses
                ],
                lag_ratio=0.12,
            ),
            run_time=0.65,
        )

        # DUSt3R không cần cách chia đó.
        strike_1 = Line(
            loss_depth.get_corner(DL),
            loss_depth.get_corner(UR),
            color=RED,
            stroke_width=1.8,
            stroke_opacity=0.72,
        )

        strike_2 = Line(
            loss_pose.get_corner(DL),
            loss_pose.get_corner(UR),
            color=RED,
            stroke_width=1.8,
            stroke_opacity=0.72,
        )

        strike_3 = Line(
            loss_matching.get_corner(DL),
            loss_matching.get_corner(UR),
            color=RED,
            stroke_width=1.8,
            stroke_opacity=0.72,
        )

        self.play_timed(
            LaggedStart(
                Create(strike_1),
                Create(strike_2),
                Create(strike_3),
                lag_ratio=0.12,
            ),
            run_time=0.75,
        )

        self.play_timed(
            tasks.animate.set_opacity(0.12),
            losses.animate.set_opacity(0.12),
            VGroup(
                strike_1,
                strike_2,
                strike_3,
            ).animate.set_opacity(0.10),
            pointmap.animate.scale(1.08),
            run_time=0.55,
        )

        # Clear peripheral task machinery.
        self.play_timed(
            FadeOut(tasks),
            FadeOut(losses),
            FadeOut(strike_1),
            FadeOut(strike_2),
            FadeOut(strike_3),
            run_time=0.45,
        )

        self.pointmap = pointmap

    # =========================================================
    # 00:07.75 -> 00:08.99
    #
    # "Ý tưởng chính đơn giản hơn:"
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            self.pointmap.animate
            .scale(0.80)
            .shift(LEFT * 4.0),
            run_time=0.55,
        )

        pred = self.make_world_point(
            LEFT * 0.9,
            CYAN,
            radius=0.075,
        )

        gt = self.make_world_point(
            RIGHT * 2.0 + UP * 0.65,
            VIOLET,
            radius=0.075,
        )

        self.play_timed(
            GrowFromCenter(pred),
            GrowFromCenter(gt),
            run_time=0.45,
        )

        self.pred = pred
        self.gt = gt

    # =========================================================
    # 00:09.55 -> 00:14.75
    #
    # "predicted 3D point càng xa ground-truth...
    # loss càng lớn."
    # =========================================================

    def sentence_3(self):

        pred_label = Text(
            "prediction",
            font_size=18,
            color=CYAN,
        ).next_to(
            self.pred,
            DOWN,
            buff=0.20,
        )

        gt_label = Text(
            "ground truth",
            font_size=18,
            color=VIOLET,
        ).next_to(
            self.gt,
            UP,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(pred_label),
            FadeIn(gt_label),
            run_time=0.45,
        )

        # Error vector.
        error_line = DashedLine(
            self.pred[-1].get_center(),
            self.gt[-1].get_center(),
            color=RED,
            dash_length=0.10,
            dashed_ratio=0.55,
            stroke_width=1.6,
        )

        error_label = MathTex(
            r"\text{error}",
            font_size=23,
            color=RED,
        )

        error_label.move_to(
            error_line.get_center()
            + UP * 0.28
        )

        self.play_timed(
            Create(error_line),
            FadeIn(error_label),
            run_time=0.65,
        )

        # Large distance -> visually strong error.
        self.play_timed(
            error_line.animate.set_stroke(
                width=3.0,
                opacity=0.85,
            ),
            run_time=0.45,
        )

        # Prediction pulled toward ground truth.
        target_pos = (
            self.gt.get_center()
            + LEFT * 0.42
            + DOWN * 0.12
        )

        self.play_timed(
            self.pred.animate.move_to(
                target_pos
            ),
            run_time=1.05,
            rate_func=smooth,
        )

        # Update line manually after movement.
        shorter_error = DashedLine(
            self.pred[-1].get_center(),
            self.gt[-1].get_center(),
            color=RED,
            dash_length=0.08,
            dashed_ratio=0.55,
            stroke_width=1.5,
            stroke_opacity=0.45,
        )

        self.play_timed(
            ReplacementTransform(
                error_line,
                shorter_error,
            ),
            error_label.animate
            .scale(0.82)
            .set_opacity(0.45),
            run_time=0.45,
        )

        # Final convergence.
        final_pos = (
            self.gt.get_center()
            + LEFT * 0.08
        )

        self.play_timed(
            self.pred.animate.move_to(
                final_pos
            ),
            FadeOut(shorter_error),
            FadeOut(error_label),
            run_time=0.75,
        )

        self.play_timed(
            Indicate(
                self.gt[-1],
                color=WHITE,
                scale_factor=1.35,
            ),
            run_time=0.40,
        )

        self.pred_label = pred_label
        self.gt_label = gt_label

    # =========================================================
    # 00:15.74 -> 00:22.11
    #
    # "scale tuyệt đối có thể mơ hồ...
    # normalize trước khi so sánh."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            FadeOut(self.pointmap),
            FadeOut(self.pred),
            FadeOut(self.gt),
            FadeOut(self.pred_label),
            FadeOut(self.gt_label),
            run_time=0.45,
        )

        # Same shape, different scale.
        small_cloud = self.make_cloud(
            center=LEFT * 3.3,
            scale=0.72,
            color=CYAN,
        )

        large_cloud = self.make_cloud(
            center=RIGHT * 3.3,
            scale=1.45,
            color=VIOLET,
        )

        self.play_timed(
            FadeIn(
                small_cloud,
                scale=0.85,
            ),
            FadeIn(
                large_cloud,
                scale=1.10,
            ),
            run_time=0.70,
        )

        # Same topology/shape highlighted.
        self.play_timed(
            small_cloud.animate.set_opacity(0.95),
            large_cloud.animate.set_opacity(0.95),
            run_time=0.35,
        )

        # Scale indicators.
        small_scale = MathTex(
            r"s",
            font_size=27,
            color=CYAN,
        ).next_to(
            small_cloud,
            DOWN,
            buff=0.25,
        )

        large_scale = MathTex(
            r"10s",
            font_size=27,
            color=VIOLET,
        ).next_to(
            large_cloud,
            DOWN,
            buff=0.25,
        )

        self.play_timed(
            FadeIn(small_scale),
            FadeIn(large_scale),
            run_time=0.40,
        )

        # normalize
        normalize = Text(
            "normalize",
            font_size=20,
            color=WHITE,
        )

        normalize.move_to(
            ORIGIN + DOWN * 2.2
        )

        self.play_timed(
            FadeIn(
                normalize,
                shift=UP * 0.06,
            ),
            run_time=0.35,
        )

        # Both converge to common normalized scale.
        self.play_timed(
            small_cloud.animate
            .scale(1.0 / 0.72)
            .move_to(ORIGIN),

            large_cloud.animate
            .scale(1.0 / 1.45)
            .move_to(ORIGIN),

            small_scale.animate.set_opacity(0),
            large_scale.animate.set_opacity(0),

            run_time=1.25,
            rate_func=smooth,
        )

        # Same geometry now overlaps.
        self.play_timed(
            small_cloud.animate.set_opacity(0.55),
            large_cloud.animate.set_opacity(0.55),
            run_time=0.40,
        )

        overlap_flash = Circle(
            radius=1.25,
            stroke_color=WHITE,
            stroke_width=1.2,
            stroke_opacity=0.20,
        ).move_to(
            ORIGIN
        )

        self.play_timed(
            FadeIn(
                overlap_flash,
                scale=0.75,
            ),
            run_time=0.30,
        )

        self.play_timed(
            overlap_flash.animate
            .scale(1.35)
            .set_opacity(0),
            run_time=0.40,
        )

        self.wait_timed(0.35)

        self.small_cloud = small_cloud
        self.large_cloud = large_cloud
        self.normalize_label = normalize

    # =========================================================
    # 00:22.84 -> 00:27.65
    #
    # "không phải pixel nào cũng dễ...
    # confidence cho từng pixel."
    # =========================================================

    def sentence_5(self):

        self.play_timed(
            FadeOut(self.small_cloud),
            FadeOut(self.large_cloud),
            FadeOut(self.normalize_label),
            run_time=0.40,
        )

        grid = self.make_confidence_grid()

        grid.move_to(
            ORIGIN
        )

        self.play_timed(
            FadeIn(
                grid,
                scale=0.97,
            ),
            run_time=0.65,
        )

        # Select easy vs uncertain regions.
        easy_ring = SurroundingRectangle(
            VGroup(
                grid[18],
                grid[19],
                grid[26],
                grid[27],
            ),
            buff=0.06,
            color=CYAN,
            stroke_width=1.2,
            stroke_opacity=0.65,
        )

        uncertain_ring = SurroundingRectangle(
            VGroup(
                grid[5],
                grid[6],
                grid[13],
                grid[14],
            ),
            buff=0.06,
            color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.65,
        )

        self.play_timed(
            Create(easy_ring),
            Create(uncertain_ring),
            run_time=0.55,
        )

        high = Text(
            "high confidence",
            font_size=17,
            color=CYAN,
        ).next_to(
            easy_ring,
            DOWN,
            buff=0.16,
        )

        low = Text(
            "low confidence",
            font_size=17,
            color=VIOLET,
        ).next_to(
            uncertain_ring,
            UP,
            buff=0.16,
        )

        self.play_timed(
            FadeIn(high),
            FadeIn(low),
            run_time=0.45,
        )

        # Confidence visualization takes over.
        self.play_timed(
            LaggedStart(
                *[
                    cell.animate.set_opacity(
                        0.25 + 0.75 * self.confidences[i]
                    )
                    for i, cell in enumerate(grid)
                ],
                lag_ratio=0.015,
            ),
            run_time=0.85,
        )

        self.play_timed(
            FadeOut(easy_ring),
            FadeOut(uncertain_ring),
            FadeOut(high),
            FadeOut(low),
            run_time=0.35,
        )

        self.wait_timed(0.35)

        self.confidence_grid = grid

    # =========================================================
    # 00:28.51 -> 00:33.80
    #
    # "vừa học reconstruction,
    # vừa học vùng nào ... đáng tin hơn."
    # =========================================================

    def sentence_6(self):

        # Split one representation into geometry + certainty,
        # without turning it into two unrelated outputs.
        self.play_timed(
            self.confidence_grid.animate
            .scale(0.80)
            .move_to(LEFT * 3.4),
            run_time=0.55,
        )

        reconstructed = self.make_pointmap(
            center=RIGHT * 2.8,
        )

        self.play_timed(
            FadeIn(
                reconstructed,
                shift=RIGHT * 0.10,
            ),
            run_time=0.65,
        )

        # Same grid topology correspondence.
        mappings = VGroup()

        source_indices = [
            8,
            19,
            28,
            39,
        ]

        point_group = reconstructed[1]

        for idx, point_idx in zip(
            source_indices,
            [5, 12, 20, 29],
        ):
            line = Line(
                self.confidence_grid[idx].get_center(),
                point_group[point_idx].get_center(),
                color=WHITE,
                stroke_width=0.8,
                stroke_opacity=0.16,
            )

            mappings.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in mappings
                ],
                lag_ratio=0.12,
            ),
            run_time=0.65,
        )

        # Geometry on the right.
        geometry_label = Text(
            "geometry",
            font_size=19,
            color=VIOLET,
        )

        geometry_label.next_to(
            reconstructed,
            UP,
            buff=0.20,
        )

        confidence_label = Text(
            "confidence",
            font_size=19,
            color=CYAN,
        )

        confidence_label.next_to(
            self.confidence_grid,
            UP,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(confidence_label),
            FadeIn(geometry_label),
            run_time=0.40,
        )

        # Pulse across correspondence:
        # each prediction carries both geometry + confidence.
        for line in mappings[:2]:

            pulse = line.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.5,
                opacity=0.80,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.24,
                ),
                run_time=0.45,
            )

        self.play_timed(
            self.confidence_grid.animate.set_opacity(
                0.82
            ),
            reconstructed.animate.set_opacity(
                0.95
            ),
            run_time=0.40,
        )

        self.wait_timed(0.60)

    # =========================================================
    # COMPONENTS
    # =========================================================

    def make_task(
        self,
        label,
        position,
        color,
    ):

        dot = Dot(
            position,
            radius=0.045,
            color=color,
        )

        text = Text(
            label,
            font_size=17,
            color=MUTED,
        )

        text.next_to(
            dot,
            DOWN,
            buff=0.13,
        )

        return VGroup(
            dot,
            text,
        )

    def make_world_point(
        self,
        point,
        color,
        radius=0.06,
    ):

        glow_large = Circle(
            radius=radius * 3.5,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        )

        glow_small = Circle(
            radius=radius * 2.0,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.075,
        )

        core = Dot(
            radius=radius,
            color=color,
        )

        group = VGroup(
            glow_large,
            glow_small,
            core,
        )

        group.move_to(
            point
        )

        return group

    def make_cloud(
        self,
        center,
        scale,
        color,
    ):

        # Deterministic shape.
        base = [
            [-0.95, -0.35],
            [-0.72, 0.15],
            [-0.48, 0.52],
            [-0.20, -0.10],
            [0.05, 0.35],
            [0.28, -0.45],
            [0.52, 0.05],
            [0.76, 0.46],
            [0.96, -0.18],
            [0.40, 0.62],
            [-0.45, -0.58],
        ]

        cloud = VGroup()

        for i, p in enumerate(base):

            c = interpolate_color(
                ManimColor(color),
                ManimColor(WHITE),
                0.12 + 0.25 * (i / len(base)),
            )

            dot = Dot(
                radius=0.045,
                color=c,
            )

            dot.move_to(
                np.array([
                    p[0],
                    p[1],
                    0,
                ])
                * scale
                + center
            )

            cloud.add(
                dot
            )

        # A few edges make shape equality clearer.
        edges = VGroup()

        connections = [
            (0, 1),
            (1, 2),
            (1, 3),
            (3, 4),
            (3, 5),
            (4, 6),
            (6, 7),
            (6, 8),
            (4, 9),
            (3, 10),
        ]

        for a, b in connections:

            edges.add(
                Line(
                    cloud[a].get_center(),
                    cloud[b].get_center(),
                    color=color,
                    stroke_width=0.8,
                    stroke_opacity=0.18,
                )
            )

        return VGroup(
            edges,
            cloud,
        )

    def make_confidence_grid(self):

        rows = 5
        cols = 8

        rng = np.random.default_rng(
            42
        )

        grid = VGroup()

        self.confidences = []

        for row in range(rows):
            for col in range(cols):

                # Make top-right region uncertain,
                # center/lower area more reliable.
                distance_uncertain = np.sqrt(
                    (col - 5.7) ** 2
                    + (row - 0.6) ** 2
                )

                confidence = np.clip(
                    0.25
                    + 0.11 * distance_uncertain
                    + rng.uniform(-0.08, 0.08),
                    0.18,
                    0.95,
                )

                self.confidences.append(
                    confidence
                )

                color = interpolate_color(
                    ManimColor(VIOLET),
                    ManimColor(CYAN),
                    confidence,
                )

                cell = Square(
                    side_length=0.55,
                    stroke_color="#343C4B",
                    stroke_width=0.55,
                    stroke_opacity=0.35,
                    fill_color=color,
                    fill_opacity=0.55,
                )

                grid.add(
                    cell
                )

        grid.arrange_in_grid(
            rows=rows,
            cols=cols,
            buff=0.035,
        )

        return grid

    def make_pointmap(
        self,
        center,
    ):

        rows = 5
        cols = 8

        positions = []
        points = VGroup()
        mesh = VGroup()

        for row in range(rows):

            row_positions = []

            for col in range(cols):

                u = col / (
                    cols - 1
                )

                v = row / (
                    rows - 1
                )

                x = (
                    u - 0.5
                ) * 3.4

                y = (
                    0.5 - v
                ) * 2.0

                depth = (
                    0.42
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

                row_positions.append(
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
                row_positions
            )

        # Horizontal mesh.
        for row in range(rows):
            for col in range(cols - 1):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row][col + 1],
                        color=CYAN,
                        stroke_width=0.65,
                        stroke_opacity=0.20,
                    )
                )

        # Vertical mesh.
        for col in range(cols):
            for row in range(rows - 1):

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