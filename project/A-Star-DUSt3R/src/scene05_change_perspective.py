from manim import *
import numpy as np

from theme import *


class Scene05ChangePerspective(Scene):
    """
    Actual narration duration: 00:00 -> 00:21

    00:00-00:05
    "Thay vì hỏi:
    Camera nằm ở đâu để từ đó ta dựng được 3D?"

    00:06-00:09
    "DUSt3R thử hỏi:
    Nếu ta dự đoán 3D trực tiếp trước thì sao?"

    00:09-00:11
    "Không phải camera pose trước."

    00:11-00:13
    "Không phải correspondence trước."

    00:13-00:17
    "Mà trực tiếp:
    Mỗi pixel này nằm ở đâu trong không gian 3D?"

    00:18-00:21
    "Đây là cú đổi góc nhìn trung tâm của DUSt3R."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.sentence_1()
        self.wait_until(6.0)

        self.sentence_2()
        self.wait_until(9.0)

        self.sentence_3()
        self.wait_until(11.0)

        self.sentence_4()
        self.wait_until(13.0)

        self.sentence_5()
        self.wait_until(18.0)

        self.sentence_6()
        self.wait_until(21.0)

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
    # 00:00 -> 00:05
    #
    # "Thay vì hỏi:
    # Camera nằm ở đâu để từ đó ta dựng được 3D?"
    # =========================================================

    def sentence_1(self):

        # Hai input image nhỏ phía trên.
        image_1 = self.make_image_card(
            accent=CYAN,
            variant=0,
        )

        image_2 = self.make_image_card(
            accent=VIOLET,
            variant=1,
        )

        image_1.scale(0.65)
        image_2.scale(0.65)

        image_1.move_to(
            LEFT * 2.0 + UP * 1.75
        )

        image_2.move_to(
            RIGHT * 2.0 + UP * 1.75
        )

        self.play_timed(
            FadeIn(
                image_1,
                shift=UP * 0.08,
            ),
            FadeIn(
                image_2,
                shift=UP * 0.08,
            ),
            run_time=0.60,
        )

        # -----------------------------------------------------
        # Classical question starts from camera pose.
        # -----------------------------------------------------

        cam1 = self.make_camera(
            LEFT * 2.8 + DOWN * 0.8,
            CYAN,
            -12 * DEGREES,
        )

        cam2 = self.make_camera(
            RIGHT * 2.8 + DOWN * 0.8,
            VIOLET,
            13 * DEGREES,
        )

        self.play_timed(
            FadeIn(
                cam1,
                scale=0.8,
            ),
            FadeIn(
                cam2,
                scale=0.8,
            ),
            run_time=0.55,
        )

        # Relationship between cameras.
        baseline = Line(
            cam1.get_center(),
            cam2.get_center(),
            color=MUTED,
            stroke_width=1,
            stroke_opacity=0.30,
        )

        self.play_timed(
            Create(
                baseline
            ),
            run_time=0.40,
        )

        # Camera pose symbols.
        pose_1 = MathTex(
            r"(R_1,t_1)",
            font_size=26,
            color=CYAN,
        )

        pose_2 = MathTex(
            r"(R_2,t_2)",
            font_size=26,
            color=VIOLET,
        )

        pose_1.next_to(
            cam1,
            DOWN,
            buff=0.20,
        )

        pose_2.next_to(
            cam2,
            DOWN,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(
                pose_1,
                shift=DOWN * 0.08,
            ),
            FadeIn(
                pose_2,
                shift=DOWN * 0.08,
            ),
            run_time=0.55,
        )

        # Rays are generated FROM known camera geometry.
        world_point = self.make_glow_point(
            ORIGIN + DOWN * 0.1,
            WHITE,
            radius=0.055,
        )

        ray1 = Line(
            cam1.get_center(),
            world_point.get_center(),
            color=CYAN,
            stroke_width=1.4,
            stroke_opacity=0.70,
        )

        ray2 = Line(
            cam2.get_center(),
            world_point.get_center(),
            color=VIOLET,
            stroke_width=1.4,
            stroke_opacity=0.70,
        )

        self.play_timed(
            Create(
                ray1
            ),
            Create(
                ray2
            ),
            run_time=0.60,
        )

        self.play_timed(
            GrowFromCenter(
                world_point
            ),
            run_time=0.35,
        )

        # Semantic question — restrained typography.
        classical = Text(
            "camera pose → 3D",
            font_size=22,
            color=MUTED,
        )

        classical.to_edge(
            DOWN,
            buff=0.45,
        )

        self.play_timed(
            FadeIn(
                classical,
                shift=UP * 0.05,
            ),
            run_time=0.40,
        )

        self.wait_timed(0.50)

        self.classical_group = VGroup(
            image_1,
            image_2,
            cam1,
            cam2,
            baseline,
            pose_1,
            pose_2,
            ray1,
            ray2,
            world_point,
            classical,
        )

        self.image_1 = image_1
        self.image_2 = image_2

    # =========================================================
    # 00:06 -> 00:09
    #
    # "DUSt3R thử hỏi:
    # Nếu ta dự đoán 3D trực tiếp trước thì sao?"
    # =========================================================

    def sentence_2(self):

        # Classical construction recedes.
        self.play_timed(
            self.classical_group.animate
            .scale(0.82)
            .set_opacity(0.14),
            run_time=0.55,
        )

        # Keep only the images conceptually important.
        self.image_1.set_opacity(1)
        self.image_2.set_opacity(1)

        self.play_timed(
            self.image_1.animate
            .scale(1.22)
            .move_to(LEFT * 2.45),

            self.image_2.animate
            .scale(1.22)
            .move_to(RIGHT * 2.45),

            run_time=0.55,
        )

        # New visual axis appears directly from images to 3D.
        center_point = self.make_glow_point(
            DOWN * 0.30,
            VIOLET,
            radius=0.06,
        )

        line_1 = Line(
            self.image_1.get_bottom(),
            center_point.get_center(),
            color=CYAN,
            stroke_width=1.2,
            stroke_opacity=0.45,
        )

        line_2 = Line(
            self.image_2.get_bottom(),
            center_point.get_center(),
            color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.45,
        )

        self.play_timed(
            Create(
                line_1
            ),
            Create(
                line_2
            ),
            run_time=0.50,
        )

        self.play_timed(
            GrowFromCenter(
                center_point
            ),
            run_time=0.35,
        )

        direct = VGroup(
            Text(
                "pixels",
                font_size=20,
                color=MUTED,
            ),
            Text(
                "→",
                font_size=24,
                color=CYAN,
            ),
            Text(
                "3D",
                font_size=26,
                color=VIOLET,
            ),
        ).arrange(
            RIGHT,
            buff=0.16,
        )

        direct.to_edge(
            DOWN,
            buff=0.48,
        )

        self.play_timed(
            FadeIn(
                direct,
                shift=UP * 0.08,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.10)

        self.direct_group = VGroup(
            line_1,
            line_2,
            center_point,
            direct,
        )

    # =========================================================
    # 00:09 -> 00:11
    #
    # "Không phải camera pose trước."
    # =========================================================

    def sentence_3(self):

        # Restore just camera pose elements,
        # then explicitly reject them.
        camera_pose_visual = VGroup(
            self.make_camera(
                LEFT * 1.0 + DOWN * 0.15,
                CYAN,
                -10 * DEGREES,
            ),
            MathTex(
                r"(R,t)",
                font_size=29,
                color=WHITE,
            ),
        )

        camera_pose_visual.arrange(
            RIGHT,
            buff=0.30,
        )

        camera_pose_visual.move_to(
            ORIGIN
        )

        self.play_timed(
            FadeOut(
                self.direct_group
            ),
            FadeIn(
                camera_pose_visual,
                scale=0.9,
            ),
            run_time=0.40,
        )

        strike = Line(
            camera_pose_visual.get_left()
            + LEFT * 0.15
            + DOWN * 0.15,
            camera_pose_visual.get_right()
            + RIGHT * 0.15
            + UP * 0.15,
            color=RED,
            stroke_width=2.0,
            stroke_opacity=0.72,
        )

        self.play_timed(
            Create(
                strike
            ),
            run_time=0.40,
        )

        self.play_timed(
            camera_pose_visual.animate
            .set_opacity(0.15)
            .shift(LEFT * 2.8),
            strike.animate
            .set_opacity(0.10)
            .shift(LEFT * 2.8),
            run_time=0.55,
        )

        self.wait_timed(0.20)

        self.camera_rejected = VGroup(
            camera_pose_visual,
            strike,
        )

    # =========================================================
    # 00:11 -> 00:13
    #
    # "Không phải correspondence trước."
    # =========================================================

    def sentence_4(self):

        # Correspondence representation.
        left_pixel = self.make_pixel(
            LEFT * 1.45,
            CYAN,
        )

        right_pixel = self.make_pixel(
            RIGHT * 1.45,
            VIOLET,
        )

        match = Line(
            left_pixel.get_center(),
            right_pixel.get_center(),
            color=CYAN_SOFT,
            stroke_width=1.5,
            stroke_opacity=0.55,
        )

        correspondence = VGroup(
            left_pixel,
            right_pixel,
            match,
        )

        self.play_timed(
            FadeIn(
                left_pixel
            ),
            FadeIn(
                right_pixel
            ),
            Create(
                match
            ),
            run_time=0.50,
        )

        strike = Line(
            correspondence.get_left()
            + LEFT * 0.15
            + DOWN * 0.22,
            correspondence.get_right()
            + RIGHT * 0.15
            + UP * 0.22,
            color=RED,
            stroke_width=2,
            stroke_opacity=0.70,
        )

        self.play_timed(
            Create(
                strike
            ),
            run_time=0.35,
        )

        self.play_timed(
            correspondence.animate
            .set_opacity(0.12)
            .shift(RIGHT * 2.8),
            strike.animate
            .set_opacity(0.08)
            .shift(RIGHT * 2.8),
            run_time=0.55,
        )

        self.wait_timed(0.20)

    # =========================================================
    # 00:13 -> 00:17
    #
    # "Mà trực tiếp:
    # Mỗi pixel này nằm ở đâu trong không gian 3D?"
    # =========================================================

    def sentence_5(self):

        # Everything peripheral fades.
        self.play_timed(
            FadeOut(
                *[
                    mob
                    for mob in self.mobjects
                    if mob not in [
                        self.image_1,
                        self.image_2,
                    ]
                ]
            ),
            self.image_1.animate.set_opacity(
                0.20
            ),
            self.image_2.animate.set_opacity(
                0.20
            ),
            run_time=0.35,
        )

        # -----------------------------------------------------
        # Single image plane becomes the focus.
        # -----------------------------------------------------

        plane = RoundedRectangle(
            width=4.6,
            height=2.8,
            corner_radius=0.08,
            stroke_color=CYAN,
            stroke_width=1.1,
            stroke_opacity=0.42,
            fill_color=CYAN,
            fill_opacity=0.015,
        )

        plane.move_to(
            ORIGIN
        )

        self.play_timed(
            FadeIn(
                plane,
                scale=1.02,
            ),
            run_time=0.40,
        )

        # Pixel grid, very subtle.
        grid = VGroup()

        cols = 12
        rows = 7

        for i in range(1, cols):
            x = interpolate(
                plane.get_left()[0],
                plane.get_right()[0],
                i / cols,
            )

            grid.add(
                Line(
                    [x, plane.get_bottom()[1], 0],
                    [x, plane.get_top()[1], 0],
                    color=GRID,
                    stroke_width=0.45,
                    stroke_opacity=0.25,
                )
            )

        for j in range(1, rows):
            y = interpolate(
                plane.get_bottom()[1],
                plane.get_top()[1],
                j / rows,
            )

            grid.add(
                Line(
                    [plane.get_left()[0], y, 0],
                    [plane.get_right()[0], y, 0],
                    color=GRID,
                    stroke_width=0.45,
                    stroke_opacity=0.25,
                )
            )

        self.play_timed(
            FadeIn(
                grid
            ),
            run_time=0.30,
        )

        # -----------------------------------------------------
        # "Mỗi pixel này..."
        # -----------------------------------------------------

        pixel_pos = (
            plane.get_center()
            + RIGHT * 0.55
            + UP * 0.25
        )

        selected_pixel = self.make_pixel(
            pixel_pos,
            CYAN,
        )

        self.play_timed(
            GrowFromCenter(
                selected_pixel
            ),
            run_time=0.35,
        )

        self.play_timed(
            Indicate(
                selected_pixel[-1],
                color=CYAN_SOFT,
                scale_factor=1.7,
            ),
            run_time=0.40,
        )

        # -----------------------------------------------------
        # "...nằm ở đâu trong không gian 3D?"
        #
        # Pixel lifts off image plane.
        # -----------------------------------------------------

        point3d_pos = (
            pixel_pos
            + RIGHT * 2.8
            + UP * 0.55
        )

        trajectory = CubicBezier(
            pixel_pos,
            pixel_pos + RIGHT * 0.8,
            point3d_pos + LEFT * 0.8 + DOWN * 0.3,
            point3d_pos,
        )

        point3d = self.make_glow_point(
            pixel_pos,
            VIOLET,
            radius=0.065,
        )

        self.add(
            point3d
        )

        self.play_timed(
            MoveAlongPath(
                point3d,
                trajectory,
            ),
            selected_pixel.animate.set_opacity(
                0.25
            ),
            run_time=0.70,
        )

        xyz = MathTex(
            r"(X,Y,Z)",
            font_size=31,
            color=WHITE,
        )

        xyz.next_to(
            point3d,
            RIGHT,
            buff=0.18,
        )

        self.play_timed(
            FadeIn(
                xyz,
                shift=RIGHT * 0.10,
            ),
            run_time=0.35,
        )

        # Small connection back to source pixel.
        lift_line = Line(
            pixel_pos,
            point3d.get_center(),
            color=VIOLET,
            stroke_width=1,
            stroke_opacity=0.28,
        )

        self.play_timed(
            Create(
                lift_line
            ),
            run_time=0.30,
        )

        self.wait_timed(0.15)

        self.pointmap_seed = VGroup(
            plane,
            grid,
            selected_pixel,
            point3d,
            xyz,
            lift_line,
        )

    # =========================================================
    # 00:18 -> 00:21
    #
    # "Đây là cú đổi góc nhìn trung tâm của DUSt3R."
    # =========================================================

    def sentence_6(self):

        # -----------------------------------------------------
        # One pixel becomes many.
        #
        # Seed of the pointmap idea for next scene.
        # -----------------------------------------------------

        plane = self.pointmap_seed[0]

        rng = np.random.default_rng(12)

        source_pixels = VGroup()
        destination_points = VGroup()
        connectors = VGroup()

        for i in range(22):

            x = rng.uniform(
                plane.get_left()[0] + 0.25,
                plane.get_right()[0] - 0.25,
            )

            y = rng.uniform(
                plane.get_bottom()[1] + 0.25,
                plane.get_top()[1] - 0.25,
            )

            source = np.array([
                x,
                y,
                0,
            ])

            # Simulated geometry:
            # different pixels lift by different amounts.
            depth = (
                0.5
                + 1.25
                * (
                    (x - plane.get_left()[0])
                    / plane.width
                )
            )

            dest = np.array([
                x + depth,
                y + 0.20 * np.sin(i),
                0,
            ])

            pixel = Square(
                side_length=0.07,
                stroke_width=0,
                fill_color=CYAN,
                fill_opacity=0.48,
            ).move_to(source)

            point = Dot(
                dest,
                radius=0.027,
                color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    depth / 1.8,
                ),
            )

            connector = Line(
                source,
                dest,
                stroke_color=VIOLET,
                stroke_width=0.55,
                stroke_opacity=0.10,
            )

            source_pixels.add(
                pixel
            )

            destination_points.add(
                point
            )

            connectors.add(
                connector
            )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        pixel,
                        scale=0.3,
                    )
                    for pixel in source_pixels
                ],
                lag_ratio=0.02,
            ),
            run_time=0.45,
        )

        self.play_timed(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(line),
                        GrowFromCenter(point),
                    )
                    for line, point in zip(
                        connectors,
                        destination_points,
                    )
                ],
                lag_ratio=0.025,
            ),
            run_time=0.80,
        )

        # Old representation/image plane dims,
        # direct 3D representation becomes dominant.
        self.play_timed(
            plane.animate.set_opacity(
                0.10
            ),
            self.pointmap_seed[1].animate.set_opacity(
                0.06
            ),
            source_pixels.animate.set_opacity(
                0.18
            ),
            destination_points.animate.scale(
                1.07
            ),
            run_time=0.50,
        )

        # DUSt3R name appears only at the end of the idea.
        dust3r = Text(
            "DUSt3R",
            font_size=23,
            color=WHITE,
        )

        dust3r.to_corner(
            UR,
            buff=0.50,
        )

        dust3r.set_opacity(
            0.72
        )

        self.play_timed(
            FadeIn(
                dust3r,
                shift=LEFT * 0.08,
            ),
            run_time=0.35,
        )

        self.wait_timed(0.40)

    # =========================================================
    # HELPERS
    # =========================================================

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
            fill_color="#10141D",
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
                0.5
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
            LEFT * 0.34,
            RIGHT * 0.34,
            color=color,
            stroke_width=1.2,
        )

        plane.shift(
            UP * 0.43
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

    def make_pixel(
        self,
        point,
        color,
    ):

        halo = Square(
            side_length=0.28,
            stroke_color=color,
            stroke_width=1,
            stroke_opacity=0.12,
        )

        core = Square(
            side_length=0.13,
            stroke_color=WHITE,
            stroke_width=0.7,
            fill_color=color,
            fill_opacity=1,
        )

        group = VGroup(
            halo,
            core,
        )

        group.move_to(
            point
        )

        return group

    def make_glow_point(
        self,
        point,
        color,
        radius=0.06,
    ):

        outer = Circle(
            radius=radius * 3.3,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        )

        mid = Circle(
            radius=radius * 2.0,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.07,
        )

        core = Dot(
            radius=radius,
            color=color,
        )

        group = VGroup(
            outer,
            mid,
            core,
        )

        group.move_to(
            point
        )

        return group