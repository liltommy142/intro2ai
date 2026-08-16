from manim import *
import numpy as np

from theme import *


class Scene12ExtremeViewpoints(Scene):
    """
    Audio: Đoạn 12.wav
    Duration: 28.88s
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.sentence_1()
        self.wait_until(9.31)

        self.sentence_2()
        self.wait_until(15.42)

        self.sentence_3()
        self.wait_until(22.75)

        self.sentence_4()
        self.wait_until(28.88)

    # =========================================================
    # TIMING
    # =========================================================

    def play_timed(self, *animations, run_time=1.0, **kwargs):
        self.play(*animations, run_time=run_time, **kwargs)
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
    # 00:00 -> 00:08.36
    #
    # Extreme viewpoints
    # =========================================================

    def sentence_1(self):

        scene_object = self.make_scene_geometry()

        self.play_timed(
            FadeIn(
                scene_object,
                scale=0.92,
            ),
            run_time=0.70,
        )

        cam_a = self.make_camera(
            LEFT * 4.3 + DOWN * 1.4,
            CYAN,
            angle=-18 * DEGREES,
        )

        cam_b = self.make_camera(
            RIGHT * 4.3 + UP * 1.3,
            VIOLET,
            angle=155 * DEGREES,
        )

        self.play_timed(
            FadeIn(cam_a, scale=0.85),
            FadeIn(cam_b, scale=0.85),
            run_time=0.60,
        )

        # Wide angle between viewpoints.
        ray_a = Line(
            cam_a[-1].get_center(),
            scene_object.get_center(),
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.28,
        )

        ray_b = Line(
            cam_b[-1].get_center(),
            scene_object.get_center(),
            color=VIOLET,
            stroke_width=1.0,
            stroke_opacity=0.28,
        )

        self.play_timed(
            Create(ray_a),
            Create(ray_b),
            run_time=0.55,
        )

        # Image cards from very different perspectives.
        image_a = self.make_view_card(
            LEFT * 3.6 + UP * 1.75,
            CYAN,
            variant=0,
        )

        image_b = self.make_view_card(
            RIGHT * 3.6 + DOWN * 1.65,
            VIOLET,
            variant=1,
        )

        self.play_timed(
            FadeIn(
                image_a,
                shift=DOWN * 0.08,
            ),
            FadeIn(
                image_b,
                shift=UP * 0.08,
            ),
            run_time=0.65,
        )

        # Attempt classical matching.
        matches = VGroup()

        points_a = [
            image_a.get_center() + np.array([-0.45, 0.20, 0]),
            image_a.get_center() + np.array([0.10, -0.10, 0]),
            image_a.get_center() + np.array([0.48, 0.28, 0]),
        ]

        points_b = [
            image_b.get_center() + np.array([-0.40, -0.20, 0]),
            image_b.get_center() + np.array([0.08, 0.16, 0]),
            image_b.get_center() + np.array([0.42, -0.26, 0]),
        ]

        dots_a = VGroup(
            *[
                Dot(
                    p,
                    radius=0.035,
                    color=CYAN,
                )
                for p in points_a
            ]
        )

        dots_b = VGroup(
            *[
                Dot(
                    p,
                    radius=0.035,
                    color=VIOLET,
                )
                for p in points_b
            ]
        )

        self.play_timed(
            FadeIn(dots_a),
            FadeIn(dots_b),
            run_time=0.40,
        )

        # Only one weak match survives.
        weak_match = DashedLine(
            dots_a[1].get_center(),
            dots_b[1].get_center(),
            color=MUTED,
            dash_length=0.10,
            stroke_width=1.0,
            stroke_opacity=0.25,
        )

        self.play_timed(
            Create(
                weak_match
            ),
            run_time=0.45,
        )

        self.play_timed(
            weak_match.animate.set_opacity(
                0.08
            ),
            dots_a.animate.set_opacity(
                0.25
            ),
            dots_b.animate.set_opacity(
                0.25
            ),
            run_time=0.40,
        )

        # Despite little matching, geometry starts to appear.
        reconstruction = self.make_pointmap_surface(
            center=ORIGIN + DOWN * 0.20,
        )

        reconstruction.set_opacity(
            0
        )

        self.add(
            reconstruction
        )

        self.play_timed(
            reconstruction.animate.set_opacity(
                0.90
            ),
            run_time=0.85,
        )

        self.play_timed(
            reconstruction.animate.scale(
                1.05
            ),
            run_time=0.35,
        )

        self.wait_timed(0.55)

        self.cam_a = cam_a
        self.cam_b = cam_b

        self.image_a = image_a
        self.image_b = image_b

        self.scene_object = scene_object
        self.reconstruction = reconstruction

        self.ray_a = ray_a
        self.ray_b = ray_b

        self.dots_a = dots_a
        self.dots_b = dots_b
        self.weak_match = weak_match

    # =========================================================
    # 00:09.31 -> 00:14.51
    #
    # "không chỉ đang lặp lại triangulation cổ điển"
    # =========================================================

    def sentence_2(self):

        # Bring classical triangulation idea forward.
        self.play_timed(
            self.reconstruction.animate.set_opacity(
                0.22
            ),
            self.scene_object.animate.set_opacity(
                0.15
            ),
            self.image_a.animate.set_opacity(
                0.16
            ),
            self.image_b.animate.set_opacity(
                0.16
            ),
            run_time=0.35,
        )

        point = Dot(
            ORIGIN,
            radius=0.06,
            color=WHITE,
        )

        tri_ray_a = Line(
            self.cam_a[-1].get_center(),
            point.get_center(),
            color=CYAN,
            stroke_width=1.4,
            stroke_opacity=0.65,
        )

        tri_ray_b = Line(
            self.cam_b[-1].get_center(),
            point.get_center(),
            color=VIOLET,
            stroke_width=1.4,
            stroke_opacity=0.65,
        )

        self.play_timed(
            Create(tri_ray_a),
            Create(tri_ray_b),
            GrowFromCenter(point),
            run_time=0.70,
        )

        triangulation_label = Text(
            "TRIANGULATION",
            font_size=22,
            color=MUTED,
        )

        triangulation_label.next_to(
            point,
            DOWN,
            buff=0.35,
        )

        self.play_timed(
            FadeIn(
                triangulation_label
            ),
            run_time=0.35,
        )

        # Cross it out as the sole explanation.
        strike = Line(
            triangulation_label.get_left()
            + LEFT * 0.15
            + DOWN * 0.10,

            triangulation_label.get_right()
            + RIGHT * 0.15
            + UP * 0.10,

            color=RED,
            stroke_width=2.0,
            stroke_opacity=0.65,
        )

        self.play_timed(
            Create(strike),
            run_time=0.45,
        )

        self.play_timed(
            VGroup(
                tri_ray_a,
                tri_ray_b,
                point,
                triangulation_label,
                strike,
            ).animate.set_opacity(
                0.16
            ),
            run_time=0.40,
        )

        self.wait_timed(0.45)

    # =========================================================
    # 00:15.42 -> 00:21.94
    #
    # learned geometric / shape priors
    # =========================================================

    def sentence_3(self):

        # Clear classical construction.
        self.play_timed(
            FadeOut(
                self.cam_a
            ),
            FadeOut(
                self.cam_b
            ),
            FadeOut(
                self.ray_a
            ),
            FadeOut(
                self.ray_b
            ),
            FadeOut(
                self.dots_a
            ),
            FadeOut(
                self.dots_b
            ),
            FadeOut(
                self.weak_match
            ),
            self.image_a.animate.set_opacity(
                0.30
            ),
            self.image_b.animate.set_opacity(
                0.30
            ),
            self.reconstruction.animate.set_opacity(
                0.82
            ),
            run_time=0.45,
        )

        # Training examples orbit around the reconstruction.
        examples = VGroup()

        positions = [
            LEFT * 4.4 + UP * 2.2,
            LEFT * 4.6 + DOWN * 2.0,
            RIGHT * 4.5 + UP * 2.0,
            RIGHT * 4.5 + DOWN * 2.0,
        ]

        colors = [
            CYAN,
            BLUE,
            VIOLET,
            MAGENTA,
        ]

        for i, (pos, color) in enumerate(
            zip(
                positions,
                colors,
            )
        ):
            example = self.make_shape_example(
                pos,
                color,
                i,
            )

            examples.add(
                example
            )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        ex,
                        scale=0.85,
                    )
                    for ex in examples
                ],
                lag_ratio=0.10,
            ),
            run_time=0.85,
        )

        # Information flows inward.
        prior_links = VGroup()

        for ex in examples:

            line = CubicBezier(
                ex.get_center(),
                ex.get_center()
                + (ORIGIN - ex.get_center()) * 0.35
                + UP * 0.20,

                self.reconstruction.get_center()
                + (ex.get_center() - ORIGIN) * 0.18,

                self.reconstruction.get_center(),
            )

            line.set_stroke(
                WHITE,
                width=0.8,
                opacity=0.12,
            )

            prior_links.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in prior_links
                ],
                lag_ratio=0.08,
            ),
            run_time=0.70,
        )

        for line in prior_links[:3]:

            pulse = line.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.5,
                opacity=0.70,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.20,
                ),
                run_time=0.35,
            )

        self.play_timed(
            self.reconstruction.animate.scale(
                1.08
            ),
            examples.animate.set_opacity(
                0.30
            ),
            run_time=0.45,
        )

        self.wait_timed(0.55)

        self.examples = examples
        self.prior_links = prior_links

    # =========================================================
    # 00:22.75 -> 00:28.88
    #
    # "model đã học một phần về việc
    # thế giới 3D thường được cấu trúc như thế nào."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            FadeOut(
                self.image_a
            ),
            FadeOut(
                self.image_b
            ),
            FadeOut(
                self.examples
            ),
            FadeOut(
                self.prior_links
            ),
            self.reconstruction.animate
            .scale(1.15)
            .move_to(ORIGIN),
            run_time=0.55,
        )

        # Reveal structural regularities.
        structure_lines = VGroup()

        points = self.reconstruction[1]

        for a, b in [
            (2, 9),
            (9, 16),
            (16, 23),
            (5, 12),
            (12, 19),
            (19, 26),
        ]:

            line = Line(
                points[a].get_center(),
                points[b].get_center(),
                color=WHITE,
                stroke_width=1.0,
                stroke_opacity=0.18,
            )

            structure_lines.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in structure_lines
                ],
                lag_ratio=0.08,
            ),
            run_time=0.80,
        )

        # A soft "world structure" field.
        field = Circle(
            radius=1.90,
            stroke_color=VIOLET,
            stroke_width=1.1,
            stroke_opacity=0.14,
            fill_color=VIOLET,
            fill_opacity=0.01,
        )

        field.move_to(
            self.reconstruction
        )

        self.play_timed(
            FadeIn(
                field,
                scale=0.85,
            ),
            run_time=0.45,
        )

        # Geometry settles.
        self.play_timed(
            self.reconstruction.animate.set_opacity(
                1.0
            ),
            structure_lines.animate.set_opacity(
                0.32
            ),
            run_time=0.45,
        )

        label = Text(
            "LEARNED 3D STRUCTURE",
            font_size=20,
            color=WHITE,
        )

        label.next_to(
            self.reconstruction,
            DOWN,
            buff=0.40,
        )

        self.play_timed(
            FadeIn(
                label,
                shift=UP * 0.06,
            ),
            run_time=0.45,
        )

        pulse = field.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.4,
            opacity=0.40,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.50)

    # =========================================================
    # HELPERS
    # =========================================================

    def make_camera(
        self,
        center,
        color,
        angle=0,
    ):

        core = Dot(
            radius=0.045,
            color=color,
        )

        plane = Line(
            LEFT * 0.36,
            RIGHT * 0.36,
            color=color,
            stroke_width=1.2,
        )

        plane.shift(
            UP * 0.46
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

    def make_view_card(
        self,
        center,
        accent,
        variant=0,
    ):

        frame = RoundedRectangle(
            width=3.0,
            height=1.85,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1.0,
            stroke_opacity=0.32,
            fill_color=SURFACE,
            fill_opacity=0.94,
        )

        if variant == 0:

            shape = Polygon(
                [-1.15, -0.50, 0],
                [0.90, -0.50, 0],
                [0.45, 0.36, 0],
                [-0.72, 0.25, 0],
                fill_color="#596579",
                fill_opacity=0.40,
                stroke_width=0,
            )

        else:

            shape = Polygon(
                [-0.85, -0.48, 0],
                [1.20, -0.22, 0],
                [0.55, 0.55, 0],
                [-0.38, 0.28, 0],
                fill_color="#596579",
                fill_opacity=0.40,
                stroke_width=0,
            )

            shape.rotate(
                -17 * DEGREES
            )

        group = VGroup(
            frame,
            shape,
        )

        group.move_to(
            center
        )

        return group

    def make_scene_geometry(self):

        floor = Polygon(
            [-1.5, -0.8, 0],
            [1.5, -0.8, 0],
            [0.95, 0.25, 0],
            [-0.85, 0.25, 0],
            stroke_color=MUTED,
            stroke_width=0.8,
            stroke_opacity=0.25,
            fill_color=SURFACE_2,
            fill_opacity=0.35,
        )

        object_a = RoundedRectangle(
            width=1.0,
            height=0.65,
            corner_radius=0.08,
            stroke_color=CYAN,
            stroke_width=0.8,
            stroke_opacity=0.35,
            fill_color=CYAN,
            fill_opacity=0.025,
        )

        object_a.move_to(
            LEFT * 0.45
            + DOWN * 0.10
        )

        object_b = Rectangle(
            width=0.65,
            height=1.0,
            stroke_color=VIOLET,
            stroke_width=0.8,
            stroke_opacity=0.35,
            fill_color=VIOLET,
            fill_opacity=0.025,
        )

        object_b.move_to(
            RIGHT * 0.70
            + UP * 0.15
        )

        return VGroup(
            floor,
            object_a,
            object_b,
        )

    def make_pointmap_surface(
        self,
        center,
    ):

        rows = 5
        cols = 7

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
                ) * 3.0

                y = (
                    0.5 - v
                ) * 1.8

                depth = (
                    0.35
                    + 0.50
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
                        radius=0.03,
                        color=color,
                    )
                )

            positions.append(
                current
            )

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

    def make_shape_example(
        self,
        center,
        color,
        variant,
    ):

        group = VGroup()

        if variant == 0:
            pts = [
                [-0.55, -0.35],
                [-0.35, 0.28],
                [0.05, 0.52],
                [0.48, 0.18],
                [0.38, -0.42],
                [-0.12, -0.55],
            ]

        elif variant == 1:
            pts = [
                [-0.50, -0.40],
                [-0.55, 0.15],
                [-0.12, 0.48],
                [0.40, 0.35],
                [0.55, -0.25],
                [0.05, -0.50],
            ]

        elif variant == 2:
            pts = [
                [-0.60, -0.12],
                [-0.30, 0.42],
                [0.20, 0.50],
                [0.55, 0.05],
                [0.25, -0.45],
                [-0.30, -0.40],
            ]

        else:
            pts = [
                [-0.55, -0.45],
                [-0.40, 0.20],
                [0.00, 0.55],
                [0.48, 0.28],
                [0.55, -0.35],
                [-0.10, -0.52],
            ]

        dots = VGroup()

        for p in pts:

            dot = Dot(
                np.array([
                    p[0],
                    p[1],
                    0,
                ])
                + center,
                radius=0.032,
                color=color,
            )

            dots.add(
                dot
            )

        edges = VGroup()

        for i in range(len(dots)):

            edges.add(
                Line(
                    dots[i].get_center(),
                    dots[
                        (i + 1)
                        % len(dots)
                    ].get_center(),
                    color=color,
                    stroke_width=0.7,
                    stroke_opacity=0.22,
                )
            )

        group.add(
            edges,
            dots,
        )

        return group