from manim import *
import numpy as np

from theme import *


class Scene02Problem(Scene):
    """
    Actual narration duration: 00:00 -> 00:24

    00:00-00:01
    "Hãy nhìn vào một pixel."

    00:01-00:04
    "Nó có vị trí. Nó có màu."

    00:05-00:07
    "Nhưng phép chiếu camera đã làm mất một thứ: độ sâu."

    00:08-00:15
    "Điểm ngoài đời tương ứng với pixel đó có thể ở rất gần,
    rất xa, hoặc ở bất kỳ đâu trên cùng một tia đi ra từ camera."

    00:17-00:20
    "Một ảnh 2D là kết quả của việc ép thế giới 3D
    lên một mặt phẳng."

    00:20-00:24
    "Và reconstruction là cố gắng đảo ngược phép biến đổi đó."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_geometry()

        self.sentence_1()
        self.wait_until(1.0)

        self.sentence_2()
        self.wait_until(5.0)

        self.sentence_3()
        self.wait_until(8.0)

        self.sentence_4()
        self.wait_until(17.0)

        self.sentence_5()
        self.wait_until(20.0)

        self.sentence_6()
        self.wait_until(24.0)

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
    # STATIC GEOMETRY
    # =========================================================

    def setup_geometry(self):
        self.camera_center = np.array([-5.1, -0.15, 0.0])

        self.camera_core = Dot(
            self.camera_center,
            radius=0.055,
            color=CYAN,
        )

        glow_1 = Circle(
            radius=0.18,
            stroke_width=0,
            fill_color=CYAN,
            fill_opacity=0.055,
        ).move_to(self.camera_center)

        glow_2 = Circle(
            radius=0.31,
            stroke_width=0,
            fill_color=CYAN,
            fill_opacity=0.018,
        ).move_to(self.camera_center)

        self.camera_glow = VGroup(
            glow_2,
            glow_1,
            self.camera_core,
        )

        plane_x = -1.7

        self.plane = Line(
            [plane_x, -2.15, 0],
            [plane_x, 2.15, 0],
            color="#586174",
            stroke_width=1.35,
            stroke_opacity=0.72,
        )

        self.plane_glow = Line(
            [plane_x, -2.15, 0],
            [plane_x, 2.15, 0],
            color=CYAN,
            stroke_width=6,
            stroke_opacity=0.025,
        )

        self.pixel_point = np.array([
            plane_x,
            0.48,
            0.0,
        ])

        self.pixel = self.make_pixel(
            self.pixel_point
        )

        top = np.array([
            plane_x,
            1.65,
            0.0,
        ])

        bottom = np.array([
            plane_x,
            -1.65,
            0.0,
        ])

        self.frustum = VGroup(
            Line(
                self.camera_center,
                top,
                color=CYAN,
                stroke_width=1,
                stroke_opacity=0.15,
            ),
            Line(
                self.camera_center,
                bottom,
                color=CYAN,
                stroke_width=1,
                stroke_opacity=0.15,
            ),
        )

    # =========================================================
    # 00:00 -> 00:01
    #
    # "Hãy nhìn vào một pixel."
    # =========================================================

    def sentence_1(self):

        self.play_timed(
            FadeIn(
                self.camera_glow,
                scale=0.8,
            ),
            Create(
                self.plane_glow
            ),
            Create(
                self.plane
            ),
            Create(
                self.frustum
            ),
            run_time=0.42,
        )

        self.play_timed(
            GrowFromCenter(
                self.pixel
            ),
            run_time=0.28,
        )

        self.play_timed(
            Indicate(
                self.pixel[-1],
                color=CYAN,
                scale_factor=1.55,
            ),
            run_time=0.30,
        )

    # =========================================================
    # 00:01 -> 00:04
    #
    # "Nó có vị trí. Nó có màu."
    # =========================================================

    def sentence_2(self):

        uv = MathTex(
            r"(u,v)",
            font_size=31,
            color=WHITE,
        )

        uv.next_to(
            self.pixel,
            UP + RIGHT,
            buff=0.25,
        )

        connector = Line(
            self.pixel.get_center(),
            uv.get_left(),
            color=CYAN,
            stroke_width=0.8,
            stroke_opacity=0.35,
        )

        self.play_timed(
            Create(
                connector
            ),
            FadeIn(
                uv,
                shift=RIGHT * 0.08,
            ),
            run_time=0.55,
        )

        rgb = MathTex(
            r"[r,\ g,\ b]",
            font_size=29,
            color=CYAN_SOFT,
        )

        rgb.next_to(
            uv,
            DOWN,
            aligned_edge=LEFT,
            buff=0.13,
        )

        self.play_timed(
            FadeIn(
                rgb,
                shift=RIGHT * 0.08,
            ),
            self.pixel[-1].animate.set_fill(
                VIOLET,
                opacity=1,
            ),
            run_time=0.55,
        )

        self.play_timed(
            self.pixel[-1].animate.set_fill(
                CYAN,
                opacity=1,
            ),
            run_time=0.35,
        )

        self.wait_timed(0.55)

        self.uv = uv
        self.rgb = rgb
        self.info_connector = connector

    # =========================================================
    # 00:05 -> 00:07
    #
    # "Nhưng phép chiếu camera đã làm mất một thứ:
    # độ sâu."
    # =========================================================

    def sentence_3(self):

        # Tách z ra riêng để có thể animate độc lập.
        xyz = MathTex(
            r"(u,v,",
            r"z",
            r")",
            font_size=33,
            color=WHITE,
        )

        xyz[1].set_color(
            VIOLET
        )

        xyz.move_to(
            self.uv
        )

        self.play_timed(
            FadeOut(
                self.rgb
            ),
            FadeOut(
                self.info_connector
            ),
            Transform(
                self.uv,
                xyz,
            ),
            run_time=0.50,
        )

        # Tạo một bản z riêng đúng tại vị trí hiện tại,
        # rồi làm nó trôi đi và biến mất.
        z_lost = xyz[1].copy()

        z_lost.set_color(
            VIOLET
        )

        self.add(
            z_lost
        )

        self.play_timed(
            z_lost.animate
            .shift(RIGHT * 0.45)
            .set_opacity(0),
            run_time=0.45,
        )

        self.remove(
            z_lost
        )

        # Làm chính z trong biểu thức cũng biến mất.
        self.play_timed(
            self.uv[1].animate.set_opacity(
                0
            ),
            run_time=0.25,
        )

        depth_axis = DashedLine(
            self.pixel_point,
            self.pixel_point + RIGHT * 6.5,
            dash_length=0.09,
            dashed_ratio=0.45,
            color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.20,
        )

        self.play_timed(
            Create(
                depth_axis
            ),
            run_time=0.40,
        )

        self.play_timed(
            depth_axis.animate.set_opacity(
                0.06
            ),
            self.uv.animate.set_opacity(
                0.35
            ),
            run_time=0.40,
        )

        self.depth_axis = depth_axis

    # =========================================================
    # 00:08 -> 00:15
    #
    # "Điểm ngoài đời tương ứng với pixel đó có thể ở rất gần,
    # rất xa, hoặc ở bất kỳ đâu trên cùng một tia đi ra
    # từ camera."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            FadeOut(
                self.uv
            ),
            run_time=0.35,
        )

        direction = (
            self.pixel_point
            - self.camera_center
        )

        direction /= np.linalg.norm(
            direction
        )

        ray_end = (
            self.camera_center
            + direction * 12
        )

        ray_glow_large = Line(
            self.camera_center,
            ray_end,
            color=CYAN,
            stroke_width=10,
            stroke_opacity=0.025,
        )

        ray_glow_small = Line(
            self.camera_center,
            ray_end,
            color=CYAN,
            stroke_width=5,
            stroke_opacity=0.06,
        )

        ray_core = Line(
            self.camera_center,
            ray_end,
            color=CYAN,
            stroke_width=1.7,
            stroke_opacity=0.90,
        )

        self.ray = VGroup(
            ray_glow_large,
            ray_glow_small,
            ray_core,
        )

        self.play_timed(
            Create(
                self.ray
            ),
            self.pixel.animate.scale(
                1.15
            ),
            run_time=0.85,
        )

        # -----------------------------------------------------
        # "rất gần"
        # -----------------------------------------------------

        near_position = (
            self.camera_center
            + direction * 5.2
        )

        self.near = self.make_world_point(
            near_position,
            CYAN_SOFT,
        )

        self.play_timed(
            GrowFromCenter(
                self.near
            ),
            run_time=0.50,
        )

        self.play_timed(
            Flash(
                self.near[-1],
                color=CYAN_SOFT,
                line_length=0.10,
                num_lines=7,
            ),
            run_time=0.45,
        )

        # -----------------------------------------------------
        # "rất xa"
        # -----------------------------------------------------

        far_position = (
            self.camera_center
            + direction * 10.5
        )

        self.far = self.make_world_point(
            far_position,
            VIOLET,
        )

        self.play_timed(
            GrowFromCenter(
                self.far
            ),
            run_time=0.55,
        )

        self.play_timed(
            self.near.animate.scale(
                1.14
            ),
            self.far.animate.scale(
                0.88
            ),
            run_time=0.45,
        )

        # -----------------------------------------------------
        # "hoặc ở bất kỳ đâu trên cùng một tia"
        # -----------------------------------------------------

        positions = [
            6.15,
            7.05,
            8.00,
            8.95,
            9.75,
        ]

        extras = VGroup()

        for i, distance in enumerate(
            positions
        ):
            position = (
                self.camera_center
                + direction * distance
            )

            color = interpolate_color(
                ManimColor(CYAN),
                ManimColor(VIOLET),
                i / (
                    len(positions) - 1
                ),
            )

            point = self.make_world_point(
                position,
                color,
                radius=0.048,
            )

            point.set_opacity(
                0.50
            )

            extras.add(
                point
            )

        self.play_timed(
            LaggedStart(
                *[
                    GrowFromCenter(
                        p
                    )
                    for p in extras
                ],
                lag_ratio=0.13,
            ),
            run_time=1.25,
        )

        all_candidates = VGroup(
            self.near,
            *extras,
            self.far,
        )

        self.play_timed(
            all_candidates.animate.set_opacity(
                0.78
            ),
            run_time=0.45,
        )

        pulse = ray_core.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=3,
            opacity=0.75,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.85,
        )

        self.play_timed(
            all_candidates.animate.set_opacity(
                0.95
            ),
            run_time=0.35,
        )

        self.wait_timed(
            0.45
        )

        self.candidates = all_candidates

    # =========================================================
    # 00:17 -> 00:20
    #
    # "Một ảnh 2D là kết quả của việc ép thế giới 3D
    # lên một mặt phẳng."
    # =========================================================

    def sentence_5(self):

        self.play_timed(
            self.plane.animate.set_stroke(
                CYAN,
                width=1.8,
                opacity=0.90,
            ),
            self.plane_glow.animate.set_opacity(
                0.08
            ),
            run_time=0.35,
        )

        projected = self.candidates.copy()

        self.add(
            projected
        )

        self.play_timed(
            *[
                point.animate
                .move_to(
                    self.pixel_point
                )
                .scale(
                    0.35
                )
                .set_opacity(
                    0.28
                )
                for point in projected
            ],
            run_time=1.20,
            rate_func=smooth,
        )

        compression_ring = Circle(
            radius=0.16,
            stroke_color=CYAN,
            stroke_width=1.5,
            stroke_opacity=0.8,
        )

        compression_ring.move_to(
            self.pixel_point
        )

        self.play_timed(
            FadeOut(
                projected
            ),
            self.pixel.animate.scale(
                1.28
            ),
            FadeIn(
                compression_ring
            ),
            run_time=0.35,
        )

        self.play_timed(
            compression_ring.animate
            .scale(
                3.0
            )
            .set_opacity(
                0
            ),
            self.pixel.animate.scale(
                1 / 1.28
            ),
            run_time=0.50,
        )

        self.remove(
            compression_ring
        )

        self.play_timed(
            self.candidates.animate.set_opacity(
                0.14
            ),
            self.ray.animate.set_opacity(
                0.18
            ),
            run_time=0.35,
        )

    # =========================================================
    # 00:20 -> 00:24
    #
    # "Và reconstruction là cố gắng đảo ngược
    # phép biến đổi đó."
    # =========================================================

    def sentence_6(self):

        self.play_timed(
            FadeOut(
                self.candidates
            ),
            FadeOut(
                self.ray
            ),
            FadeOut(
                self.depth_axis
            ),
            run_time=0.45,
        )

        self.play_timed(
            Indicate(
                self.pixel[-1],
                color=CYAN,
                scale_factor=1.65,
            ),
            run_time=0.55,
        )

        direction = (
            self.pixel_point
            - self.camera_center
        )

        direction /= np.linalg.norm(
            direction
        )

        ray_end = (
            self.camera_center
            + direction * 12
        )

        reverse_ray = VGroup(
            Line(
                self.pixel_point,
                ray_end,
                color=CYAN,
                stroke_width=7,
                stroke_opacity=0.025,
            ),
            Line(
                self.pixel_point,
                ray_end,
                color=CYAN,
                stroke_width=3.5,
                stroke_opacity=0.07,
            ),
            Line(
                self.pixel_point,
                ray_end,
                color=CYAN,
                stroke_width=1.6,
                stroke_opacity=0.85,
            ),
        )

        self.play_timed(
            Create(
                reverse_ray
            ),
            run_time=0.70,
        )

        reconstruction_points = VGroup()

        for i, distance in enumerate(
            [
                5.2,
                6.2,
                7.3,
                8.5,
                9.6,
                10.5,
            ]
        ):
            point = (
                self.camera_center
                + direction * distance
            )

            color = interpolate_color(
                ManimColor(CYAN),
                ManimColor(VIOLET),
                i / 5,
            )

            reconstruction_points.add(
                self.make_world_point(
                    point,
                    color,
                    radius=0.052,
                )
            )

        self.play_timed(
            LaggedStart(
                *[
                    GrowFromCenter(
                        p
                    )
                    for p in reconstruction_points
                ],
                lag_ratio=0.10,
            ),
            run_time=1.05,
        )

        self.play_timed(
            ShowPassingFlash(
                reverse_ray[-1]
                .copy()
                .set_stroke(
                    CYAN_SOFT,
                    width=3,
                ),
                time_width=0.30,
            ),
            reconstruction_points.animate.set_opacity(
                0.82
            ),
            run_time=0.65,
        )

        self.wait_timed(
            0.60
        )

    # =========================================================
    # COMPONENTS
    # =========================================================

    def make_pixel(self, point):

        halo_large = Square(
            side_length=0.38,
            stroke_color=CYAN,
            stroke_width=1,
            stroke_opacity=0.05,
        )

        halo_medium = Square(
            side_length=0.25,
            stroke_color=CYAN,
            stroke_width=1,
            stroke_opacity=0.16,
        )

        core = Square(
            side_length=0.14,
            stroke_color=CYAN_SOFT,
            stroke_width=0.9,
            fill_color=CYAN,
            fill_opacity=1,
        )

        group = VGroup(
            halo_large,
            halo_medium,
            core,
        )

        group.move_to(
            point
        )

        return group

    def make_world_point(
        self,
        point,
        color,
        radius=0.06,
    ):

        outer = Circle(
            radius=radius * 3.2,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        )

        middle = Circle(
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
            middle,
            core,
        )

        group.move_to(
            point
        )

        return group