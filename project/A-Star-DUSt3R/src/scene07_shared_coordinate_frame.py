from manim import *
import numpy as np

from theme import *


class Scene07SharedCoordinateFrame(Scene):
    """
    00:00-00:04
    "DUSt3R còn làm một việc quan trọng hơn nữa."

    00:04-00:06
    "Với hai ảnh, nó tạo hai pointmap."

    00:06-00:12
    "Nhưng pointmap của ảnh thứ hai không nằm trong coordinate frame
    riêng của camera thứ hai."

    00:12-00:18
    "Cả hai pointmap đều được biểu diễn trong coordinate frame
    của camera thứ nhất."

    00:19-00:22
    "Điều này có nghĩa là hai geometry đã nằm trong cùng một hệ tọa độ."

    00:23-00:29
    "Relationship giữa hai viewpoint vì thế đã được encode ngầm
    trong chính geometry."

    00:29-00:33
    "Camera pose không còn là thứ bắt buộc phải biết trước khi có 3D."

    00:33-00:37
    "Nó trở thành thứ có thể được suy ra từ representation đó."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_scene()

        self.sentence_1()
        self.wait_until(4.0)

        self.sentence_2()
        self.wait_until(6.0)

        self.sentence_3()
        self.wait_until(12.0)

        self.sentence_4()
        self.wait_until(19.0)

        self.sentence_5()
        self.wait_until(23.0)

        self.sentence_6()
        self.wait_until(29.0)

        self.sentence_7()
        self.wait_until(33.0)

        self.sentence_8()
        self.wait_until(37.0)

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
        self.cols = 8
        self.rows = 5

        self.left_image = self.make_image_grid(
            center=LEFT * 3.3 + UP * 1.45,
            accent=CYAN,
            variant=0,
        )

        self.right_image = self.make_image_grid(
            center=RIGHT * 3.3 + UP * 1.45,
            accent=VIOLET,
            variant=1,
        )

        self.cam1_pos = np.array([
            -3.0,
            -1.65,
            0.0,
        ])

        self.cam2_pos = np.array([
            3.1,
            -1.65,
            0.0,
        ])

        self.camera1 = self.make_camera(
            self.cam1_pos,
            CYAN,
            angle=-8 * DEGREES,
        )

        self.camera2 = self.make_camera(
            self.cam2_pos,
            VIOLET,
            angle=11 * DEGREES,
        )

    # =========================================================
    # 00:00 -> 00:04
    #
    # "DUSt3R còn làm một việc quan trọng hơn nữa."
    # =========================================================

    def sentence_1(self):

        self.play_timed(
            FadeIn(
                self.left_image,
                shift=UP * 0.08,
            ),
            FadeIn(
                self.right_image,
                shift=UP * 0.08,
            ),
            run_time=0.75,
        )

        self.play_timed(
            FadeIn(
                self.camera1,
                scale=0.85,
            ),
            FadeIn(
                self.camera2,
                scale=0.85,
            ),
            run_time=0.55,
        )

        link = Line(
            self.left_image.get_right(),
            self.right_image.get_left(),
            color=MUTED,
            stroke_width=1,
            stroke_opacity=0.18,
        )

        self.play_timed(
            Create(
                link
            ),
            run_time=0.40,
        )

        pulse = link.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.4,
            opacity=0.55,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.65)

        self.initial_link = link

    # =========================================================
    # 00:04 -> 00:06
    #
    # "Với hai ảnh, nó tạo hai pointmap."
    # =========================================================

    def sentence_2(self):

        self.pointmap1 = self.make_pointmap_surface(
            center=LEFT * 2.3 + DOWN * 0.35,
            color_a=CYAN,
            color_b=BLUE,
            variant=0,
        )

        self.pointmap2 = self.make_pointmap_surface(
            center=RIGHT * 2.3 + DOWN * 0.35,
            color_a=VIOLET,
            color_b=MAGENTA,
            variant=1,
        )

        self.play_timed(
            FadeOut(
                self.initial_link
            ),
            FadeIn(
                self.pointmap1,
                shift=DOWN * 0.12,
            ),
            FadeIn(
                self.pointmap2,
                shift=DOWN * 0.12,
            ),
            run_time=0.90,
        )

        self.play_timed(
            self.left_image.animate.set_opacity(
                0.30
            ),
            self.right_image.animate.set_opacity(
                0.30
            ),
            run_time=0.35,
        )

    # =========================================================
    # 00:06 -> 00:12
    #
    # "Nhưng pointmap của ảnh thứ hai không nằm trong coordinate
    # frame riêng của camera thứ hai."
    # =========================================================

    def sentence_3(self):

        frame1 = self.make_coordinate_frame(
            self.cam1_pos + RIGHT * 0.35,
            CYAN,
            scale=0.85,
        )

        frame2 = self.make_coordinate_frame(
            self.cam2_pos + LEFT * 0.35,
            VIOLET,
            scale=0.85,
        )

        self.play_timed(
            FadeIn(
                frame1
            ),
            FadeIn(
                frame2
            ),
            run_time=0.55,
        )

        local_link = Line(
            frame2.get_center(),
            self.pointmap2.get_center(),
            color=VIOLET,
            stroke_width=1.3,
            stroke_opacity=0.34,
        )

        self.play_timed(
            Create(
                local_link
            ),
            run_time=0.50,
        )

        reject = Line(
            frame2.get_corner(DL) + LEFT * 0.12,
            frame2.get_corner(UR) + RIGHT * 0.12,
            color=RED,
            stroke_width=2.0,
            stroke_opacity=0.72,
        )

        self.play_timed(
            Create(
                reject
            ),
            run_time=0.45,
        )

        self.play_timed(
            frame2.animate.set_opacity(
                0.12
            ),
            local_link.animate.set_opacity(
                0.06
            ),
            reject.animate.set_opacity(
                0.25
            ),
            self.camera2.animate.set_opacity(
                0.35
            ),
            run_time=0.55,
        )

        self.play_timed(
            self.pointmap2.animate.set_opacity(
                1.0
            ),
            run_time=0.35,
        )

        self.wait_timed(0.60)

        self.frame1 = frame1
        self.frame2 = frame2
        self.local_link = local_link
        self.frame2_reject = reject

    # =========================================================
    # 00:12 -> 00:18
    #
    # "Cả hai pointmap đều được biểu diễn trong coordinate frame
    # của camera thứ nhất."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            self.frame1.animate.scale(
                1.15
            ),
            self.camera1.animate.set_opacity(
                1.0
            ),
            FadeOut(
                self.frame2_reject
            ),
            run_time=0.45,
        )

        shared_origin = np.array([
            -4.7,
            -2.0,
            0.0,
        ])

        shared_frame = self.make_coordinate_frame(
            shared_origin,
            CYAN,
            scale=1.18,
        )

        shared_frame.set_z_index(
            5
        )

        self.play_timed(
            ReplacementTransform(
                self.frame1,
                shared_frame,
            ),
            FadeOut(
                self.frame2
            ),
            FadeOut(
                self.local_link
            ),
            run_time=0.65,
        )

        self.play_timed(
            self.pointmap1.animate
            .scale(1.08)
            .move_to(
                LEFT * 0.95
                + DOWN * 0.05
            ),

            self.pointmap2.animate
            .scale(1.08)
            .move_to(
                RIGHT * 1.20
                + UP * 0.08
            ),

            self.left_image.animate.set_opacity(
                0.12
            ),

            self.right_image.animate.set_opacity(
                0.12
            ),

            run_time=1.10,
        )

        link1 = Line(
            shared_origin,
            self.pointmap1.get_center(),
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.22,
        )

        link2 = Line(
            shared_origin,
            self.pointmap2.get_center(),
            color=VIOLET,
            stroke_width=1.0,
            stroke_opacity=0.22,
        )

        self.play_timed(
            Create(
                link1
            ),
            Create(
                link2
            ),
            run_time=0.65,
        )

        pulse1 = link1.copy()

        pulse1.set_stroke(
            CYAN_SOFT,
            width=2.5,
            opacity=0.80,
        )

        pulse2 = link2.copy()

        pulse2.set_stroke(
            MAGENTA,
            width=2.5,
            opacity=0.80,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse1,
                time_width=0.25,
            ),
            ShowPassingFlash(
                pulse2,
                time_width=0.25,
            ),
            run_time=0.70,
        )

        self.wait_timed(0.35)

        self.shared_frame = shared_frame
        self.shared_link1 = link1
        self.shared_link2 = link2

    # =========================================================
    # 00:19 -> 00:22
    #
    # "Điều này có nghĩa là hai geometry đã nằm trong cùng
    # một hệ tọa độ."
    # =========================================================

    def sentence_5(self):

        self.play_timed(
            self.camera1.animate.set_opacity(
                0.25
            ),
            self.camera2.animate.set_opacity(
                0.12
            ),
            self.left_image.animate.set_opacity(
                0.05
            ),
            self.right_image.animate.set_opacity(
                0.05
            ),
            run_time=0.35,
        )

        shared_field = RoundedRectangle(
            width=7.0,
            height=3.6,
            corner_radius=0.18,
            stroke_color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.16,
            fill_color=CYAN,
            fill_opacity=0.012,
        )

        shared_field.move_to(
            self.pointmap1.get_center()
            + RIGHT * 1.0
        )

        self.play_timed(
            FadeIn(
                shared_field
            ),
            run_time=0.45,
        )

        self.play_timed(
            self.pointmap1.animate.set_opacity(
                0.92
            ),
            self.pointmap2.animate.set_opacity(
                0.92
            ),
            self.shared_link1.animate.set_opacity(
                0.38
            ),
            self.shared_link2.animate.set_opacity(
                0.38
            ),
            run_time=0.45,
        )

        self.play_timed(
            Indicate(
                self.shared_frame[-1],
                color=CYAN_SOFT,
                scale_factor=1.25,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.30)

        self.shared_field = shared_field

    # =========================================================
    # 00:23 -> 00:29
    #
    # "Relationship giữa hai viewpoint vì thế đã được encode
    # ngầm trong chính geometry."
    # =========================================================

    def sentence_6(self):

        pair_indices = [
            (5, 7),
            (11, 13),
            (20, 21),
        ]

        relations = VGroup()

        points1 = self.pointmap1[1]
        points2 = self.pointmap2[1]

        for idx1, idx2 in pair_indices:

            p1 = points1[idx1]
            p2 = points2[idx2]

            relation = CubicBezier(
                p1.get_center(),
                p1.get_center()
                + RIGHT * 0.65
                + UP * 0.18,

                p2.get_center()
                + LEFT * 0.65
                + DOWN * 0.12,

                p2.get_center(),
            )

            relation.set_stroke(
                WHITE,
                width=0.9,
                opacity=0.18,
            )

            relations.add(
                relation
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(
                        r
                    )
                    for r in relations
                ],
                lag_ratio=0.14,
            ),
            run_time=0.80,
        )

        relative_arrow = CurvedArrow(
            self.pointmap1.get_top()
            + UP * 0.10,

            self.pointmap2.get_top()
            + UP * 0.10,

            angle=-0.35,
            color=VIOLET,
            stroke_width=1.5,
            stroke_opacity=0.55,
        )

        # IMPORTANT:
        # Không dùng GrowArrow với CurvedArrow trong Manim 0.21.
        self.play_timed(
            Create(
                relative_arrow
            ),
            run_time=0.55,
        )

        self.play_timed(
            self.pointmap2.animate
            .rotate(
                -3 * DEGREES
            )
            .shift(
                RIGHT * 0.12
                + UP * 0.06
            ),
            run_time=0.70,
        )

        self.play_timed(
            relations.animate.set_opacity(
                0.42
            ),
            relative_arrow.animate.set_opacity(
                0.75
            ),
            run_time=0.45,
        )

        for relation in relations[:2]:

            pulse = relation.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.4,
                opacity=0.85,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.25,
                ),
                run_time=0.45,
            )

        self.wait_timed(0.55)

        self.geometry_relations = relations
        self.relative_arrow = relative_arrow

    # =========================================================
    # 00:29 -> 00:33
    #
    # "Camera pose không còn là thứ bắt buộc phải biết trước
    # khi có 3D."
    # =========================================================

    def sentence_7(self):

        pose1 = MathTex(
            r"(R_1,t_1)",
            font_size=28,
            color=CYAN,
        )

        pose2 = MathTex(
            r"(R_2,t_2)",
            font_size=28,
            color=VIOLET,
        )

        pose_group = VGroup(
            pose1,
            pose2,
        ).arrange(
            RIGHT,
            buff=0.45,
        )

        pose_group.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play_timed(
            FadeIn(
                pose_group,
                shift=UP * 0.08,
            ),
            run_time=0.45,
        )

        strike = Line(
            pose_group.get_left()
            + LEFT * 0.12
            + DOWN * 0.08,

            pose_group.get_right()
            + RIGHT * 0.12
            + UP * 0.08,

            color=RED,
            stroke_width=2,
            stroke_opacity=0.65,
        )

        self.play_timed(
            Create(
                strike
            ),
            run_time=0.40,
        )

        self.play_timed(
            pose_group.animate.set_opacity(
                0.15
            ),
            strike.animate.set_opacity(
                0.12
            ),
            self.pointmap1.animate.set_opacity(
                1
            ),
            self.pointmap2.animate.set_opacity(
                1
            ),
            run_time=0.60,
        )

        self.play_timed(
            FadeOut(
                pose_group
            ),
            FadeOut(
                strike
            ),
            run_time=0.45,
        )

        self.wait_timed(0.35)

    # =========================================================
    # 00:33 -> 00:37
    #
    # "Nó trở thành thứ có thể được suy ra từ representation đó."
    # =========================================================

    def sentence_8(self):

        self.play_timed(
            self.geometry_relations.animate.set_opacity(
                0.18
            ),
            self.shared_link1.animate.set_opacity(
                0.10
            ),
            self.shared_link2.animate.set_opacity(
                0.10
            ),
            run_time=0.35,
        )

        inferred_cam2 = self.make_camera(
            RIGHT * 4.65
            + DOWN * 1.65,

            VIOLET,
            angle=11 * DEGREES,
        )

        inferred_cam2.set_opacity(
            0
        )

        inference_arrow = CurvedArrow(
            self.pointmap2.get_right(),
            inferred_cam2.get_left(),
            angle=-0.25,
            color=VIOLET,
            stroke_width=1.5,
            stroke_opacity=0.55,
        )

        # IMPORTANT:
        # Create thay cho GrowArrow để tránh lỗi scale_tips.
        self.play_timed(
            Create(
                inference_arrow
            ),
            run_time=0.55,
        )

        self.play_timed(
            inferred_cam2.animate.set_opacity(
                0.90
            ),
            run_time=0.50,
        )

        inferred_pose = MathTex(
            r"\hat{R},\hat{t}",
            font_size=30,
            color=VIOLET,
        )

        inferred_pose.next_to(
            inferred_cam2,
            UP,
            buff=0.18,
        )

        self.play_timed(
            FadeIn(
                inferred_pose,
                shift=UP * 0.06,
            ),
            run_time=0.45,
        )

        pulse = inference_arrow.copy()

        pulse.set_stroke(
            MAGENTA,
            width=3,
            opacity=0.85,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.22,
            ),
            run_time=0.55,
        )

        self.play_timed(
            Indicate(
                inferred_cam2[-1],
                color=VIOLET,
                scale_factor=1.35,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.60)

    # =========================================================
    # IMAGE GRID
    # =========================================================

    def make_image_grid(
        self,
        center,
        accent,
        variant=0,
    ):

        width = 3.4
        height = 2.15

        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1,
            stroke_opacity=0.32,
            fill_color=SURFACE,
            fill_opacity=1,
        )

        frame.move_to(
            center
        )

        pixels = VGroup()

        cell_w = width / self.cols
        cell_h = height / self.rows

        left = center[0] - width / 2
        bottom = center[1] - height / 2

        for row in range(self.rows):
            for col in range(self.cols):

                x = (
                    left
                    + (col + 0.5)
                    * cell_w
                )

                y = (
                    bottom
                    + (
                        self.rows
                        - row
                        - 0.5
                    )
                    * cell_h
                )

                u = col / (
                    self.cols - 1
                )

                v = row / (
                    self.rows - 1
                )

                base = interpolate_color(
                    ManimColor("#283344"),
                    ManimColor("#56667A"),
                    0.45 * u
                    + 0.25 * v,
                )

                if variant == 1:
                    base = interpolate_color(
                        base,
                        ManimColor(VIOLET),
                        0.08,
                    )

                pixel = Square(
                    side_length=min(
                        cell_w,
                        cell_h,
                    ) * 0.90,
                    stroke_color="#596274",
                    stroke_width=0.35,
                    stroke_opacity=0.15,
                    fill_color=base,
                    fill_opacity=0.90,
                )

                pixel.move_to([
                    x,
                    y,
                    0,
                ])

                pixels.add(
                    pixel
                )

        return VGroup(
            frame,
            pixels,
        )

    # =========================================================
    # POINTMAP
    # =========================================================

    def make_pointmap_surface(
        self,
        center,
        color_a,
        color_b,
        variant=0,
    ):

        points = VGroup()
        mesh = VGroup()

        positions = []

        for row in range(self.rows):

            current_row = []

            for col in range(self.cols):

                u = col / (
                    self.cols - 1
                )

                v = row / (
                    self.rows - 1
                )

                x = (
                    u - 0.5
                ) * 3.0

                y = (
                    0.5 - v
                ) * 1.70

                depth = (
                    0.42
                    + 0.42
                    * np.sin(
                        np.pi * u
                    )
                    * np.cos(
                        np.pi
                        * v
                        * 0.85
                    )
                )

                if variant == 1:

                    depth += (
                        0.22
                        + 0.18 * u
                    )

                    x += (
                        0.22
                        + 0.18 * v
                    )

                screen_x = (
                    center[0]
                    + x
                    + depth * 0.52
                )

                screen_y = (
                    center[1]
                    + y
                    + depth * 0.28
                )

                p = np.array([
                    screen_x,
                    screen_y,
                    0,
                ])

                current_row.append(
                    p
                )

                color = interpolate_color(
                    ManimColor(
                        color_a
                    ),
                    ManimColor(
                        color_b
                    ),
                    u,
                )

                point = Dot(
                    p,
                    radius=0.026,
                    color=color,
                )

                points.add(
                    point
                )

            positions.append(
                current_row
            )

        for row in range(self.rows):
            for col in range(
                self.cols - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row][col + 1],
                        color=color_a,
                        stroke_width=0.65,
                        stroke_opacity=0.24,
                    )
                )

        for col in range(self.cols):
            for row in range(
                self.rows - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row + 1][col],
                        color=color_b,
                        stroke_width=0.65,
                        stroke_opacity=0.20,
                    )
                )

        return VGroup(
            mesh,
            points,
        )

    # =========================================================
    # COORDINATE FRAME
    # =========================================================

    def make_coordinate_frame(
        self,
        origin,
        color,
        scale=1.0,
    ):

        origin = np.array(
            origin,
            dtype=float,
        )

        x_axis = Arrow(
            origin,
            origin
            + RIGHT
            * 0.65
            * scale,
            buff=0,
            color=CYAN,
            stroke_width=1.3,
            max_tip_length_to_length_ratio=0.18,
        )

        y_axis = Arrow(
            origin,
            origin
            + UP
            * 0.65
            * scale,
            buff=0,
            color=VIOLET,
            stroke_width=1.3,
            max_tip_length_to_length_ratio=0.18,
        )

        z_axis = Arrow(
            origin,
            origin
            + LEFT
            * 0.34
            * scale
            + DOWN
            * 0.30
            * scale,
            buff=0,
            color=MAGENTA,
            stroke_width=1.3,
            max_tip_length_to_length_ratio=0.18,
        )

        origin_dot = Dot(
            origin,
            radius=0.038,
            color=color,
        )

        return VGroup(
            x_axis,
            y_axis,
            z_axis,
            origin_dot,
        )

    # =========================================================
    # CAMERA
    # =========================================================

    def make_camera(
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
            LEFT * 0.33,
            RIGHT * 0.33,
            color=color,
            stroke_width=1.2,
        )

        plane.shift(
            UP * 0.42
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