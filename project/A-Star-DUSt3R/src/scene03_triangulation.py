from manim import *
import numpy as np

from theme import *


class Scene03Triangulation(Scene):
    """
    Actual narration duration: 00:00 -> 00:22

    00:00-00:02
    "Bây giờ thêm một camera thứ hai."

    00:03-00:06
    "Cùng một điểm 3D xuất hiện ở hai vị trí khác nhau trên hai ảnh."

    00:07-00:11
    "Nếu biết hai camera nằm ở đâu, ta có thể dựng một tia từ mỗi camera."

    00:11-00:15
    "Nơi hai tia gặp nhau cho ta vị trí của điểm đó trong không gian."

    00:15-00:22
    "Đó là triangulation, và là lý do hai góc nhìn mang lại nhiều
    thông tin 3D hơn một góc nhìn."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_geometry()

        self.sentence_1()
        self.wait_until(3.0)

        self.sentence_2()
        self.wait_until(7.0)

        self.sentence_3()
        self.wait_until(11.0)

        self.sentence_4()
        self.wait_until(15.0)

        self.sentence_5()
        self.wait_until(22.0)

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
    # BASE GEOMETRY
    # =========================================================

    def setup_geometry(self):
        # Ground truth 3D point
        self.world_point_pos = np.array([0.3, 1.05, 0.0])

        # Camera positions
        self.cam1_pos = np.array([-4.6, -1.45, 0.0])
        self.cam2_pos = np.array([4.6, -1.45, 0.0])

        # Image plane positions
        self.plane1_x = -2.45
        self.plane2_x = 2.45

        self.cam1 = self.make_camera_frustum(
            center=self.cam1_pos,
            plane_x=self.plane1_x,
            color=CYAN,
        )

        self.cam2 = self.make_camera_frustum(
            center=self.cam2_pos,
            plane_x=self.plane2_x,
            color=VIOLET,
            facing_left=True,
        )

        self.world_point = self.make_world_point(
            self.world_point_pos,
            WHITE,
            radius=0.065,
        )

    # =========================================================
    # 00:00 -> 00:02
    #
    # "Bây giờ thêm một camera thứ hai."
    # =========================================================

    def sentence_1(self):

        # Establish camera 1 first
        self.play_timed(
            FadeIn(
                self.cam1,
                scale=0.92,
            ),
            run_time=0.55,
        )

        # Camera 2 slides in, not just fade
        self.cam2.shift(RIGHT * 1.0)

        self.play_timed(
            FadeIn(
                self.cam2,
                shift=LEFT * 0.15,
                scale=0.92,
            ),
            self.cam2.animate.shift(LEFT * 1.0),
            run_time=0.95,
        )

        self.play_timed(
            self.cam1.animate.set_opacity(0.85),
            self.cam2.animate.set_opacity(0.85),
            run_time=0.25,
        )

        self.wait_timed(0.25)

    # =========================================================
    # 00:03 -> 00:06
    #
    # "Cùng một điểm 3D xuất hiện ở hai vị trí khác nhau trên hai ảnh."
    # =========================================================

    def sentence_2(self):

        # Ground-truth 3D point appears
        self.play_timed(
            GrowFromCenter(
                self.world_point
            ),
            run_time=0.45,
        )

        # Compute line-of-sight intersections with image planes
        p1 = self.intersect_with_vertical_plane(
            self.cam1_pos,
            self.world_point_pos,
            self.plane1_x,
        )

        p2 = self.intersect_with_vertical_plane(
            self.cam2_pos,
            self.world_point_pos,
            self.plane2_x,
        )

        self.pixel1_pos = p1
        self.pixel2_pos = p2

        # Projection guides
        proj1 = Line(
            self.cam1_pos,
            self.world_point_pos,
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.16,
        )

        proj2 = Line(
            self.cam2_pos,
            self.world_point_pos,
            color=VIOLET,
            stroke_width=1.0,
            stroke_opacity=0.16,
        )

        self.play_timed(
            Create(proj1),
            Create(proj2),
            run_time=0.55,
        )

        pixel1 = self.make_pixel(
            self.pixel1_pos,
            CYAN,
        )

        pixel2 = self.make_pixel(
            self.pixel2_pos,
            VIOLET,
        )

        self.play_timed(
            GrowFromCenter(pixel1),
            GrowFromCenter(pixel2),
            run_time=0.45,
        )

        # Highlight difference in image positions
        offset1 = MathTex(
            r"u_1",
            font_size=26,
            color=CYAN,
        ).next_to(
            pixel1,
            UP,
            buff=0.15,
        )

        offset2 = MathTex(
            r"u_2",
            font_size=26,
            color=VIOLET,
        ).next_to(
            pixel2,
            UP,
            buff=0.15,
        )

        self.play_timed(
            FadeIn(offset1),
            FadeIn(offset2),
            run_time=0.35,
        )

        self.play_timed(
            Indicate(
                pixel1[-1],
                color=CYAN,
                scale_factor=1.35,
            ),
            Indicate(
                pixel2[-1],
                color=VIOLET,
                scale_factor=1.35,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.30)

        self.pixel1 = pixel1
        self.pixel2 = pixel2
        self.proj1 = proj1
        self.proj2 = proj2
        self.u1 = offset1
        self.u2 = offset2

    # =========================================================
    # 00:07 -> 00:11
    #
    # "Nếu biết hai camera nằm ở đâu, ta có thể dựng một tia
    # từ mỗi camera."
    # =========================================================

    def sentence_3(self):

        self.play_timed(
            FadeOut(self.u1),
            FadeOut(self.u2),
            self.proj1.animate.set_opacity(0.06),
            self.proj2.animate.set_opacity(0.06),
            run_time=0.35,
        )

        # Rays extend beyond pixels
        ray1_end = self.extend_ray(
            self.cam1_pos,
            self.pixel1_pos,
            9.5,
        )

        ray2_end = self.extend_ray(
            self.cam2_pos,
            self.pixel2_pos,
            9.5,
        )

        self.ray1 = self.make_glow_line(
            self.cam1_pos,
            ray1_end,
            CYAN,
        )

        self.ray2 = self.make_glow_line(
            self.cam2_pos,
            ray2_end,
            VIOLET,
        )

        # First ray
        self.play_timed(
            Create(self.ray1),
            run_time=0.85,
        )

        # Second ray
        self.play_timed(
            Create(self.ray2),
            run_time=0.85,
        )

        # Show camera locations are known
        cam1_ring = Circle(
            radius=0.18,
            stroke_color=CYAN,
            stroke_width=1.2,
            stroke_opacity=0.65,
        ).move_to(self.cam1_pos)

        cam2_ring = Circle(
            radius=0.18,
            stroke_color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.65,
        ).move_to(self.cam2_pos)

        self.play_timed(
            FadeIn(cam1_ring, scale=0.7),
            FadeIn(cam2_ring, scale=0.7),
            run_time=0.35,
        )

        self.play_timed(
            cam1_ring.animate.scale(1.7).set_opacity(0),
            cam2_ring.animate.scale(1.7).set_opacity(0),
            run_time=0.45,
        )

        self.wait_timed(0.15)

    # =========================================================
    # 00:11 -> 00:15
    #
    # "Nơi hai tia gặp nhau cho ta vị trí của điểm đó trong không gian."
    # =========================================================

    def sentence_4(self):

        # Dim everything except rays
        self.play_timed(
            self.cam1.animate.set_opacity(0.35),
            self.cam2.animate.set_opacity(0.35),
            self.pixel1.animate.set_opacity(0.35),
            self.pixel2.animate.set_opacity(0.35),
            run_time=0.35,
        )

        # Pulse along both rays into the intersection
        ray1_pulse = self.ray1[-1].copy().set_stroke(
            CYAN_SOFT,
            width=3.2,
        )

        ray2_pulse = self.ray2[-1].copy().set_stroke(
            MAGENTA,
            width=3.2,
        )

        self.play_timed(
            ShowPassingFlash(
                ray1_pulse,
                time_width=0.22,
            ),
            ShowPassingFlash(
                ray2_pulse,
                time_width=0.22,
            ),
            run_time=0.75,
        )

        # Intersection locks
        lock_ring = Circle(
            radius=0.14,
            stroke_color=WHITE,
            stroke_width=1.6,
        ).move_to(
            self.world_point_pos
        )

        lock_halo = Circle(
            radius=0.34,
            stroke_color=WHITE,
            stroke_width=1.0,
            stroke_opacity=0.12,
        ).move_to(
            self.world_point_pos
        )

        self.play_timed(
            GrowFromCenter(lock_halo),
            GrowFromCenter(lock_ring),
            self.world_point.animate.scale(1.3),
            run_time=0.45,
        )

        self.play_timed(
            lock_halo.animate.scale(2.0).set_opacity(0),
            lock_ring.animate.scale(1.4).set_opacity(0),
            run_time=0.55,
        )

        # Tiny xyz label, not a title card
        xyz = MathTex(
            r"(X,Y,Z)",
            font_size=28,
            color=WHITE,
        )

        xyz.next_to(
            self.world_point,
            UP,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(
                xyz,
                shift=UP * 0.08,
            ),
            run_time=0.35,
        )

        self.play_timed(
            self.world_point.animate.set_opacity(1),
            run_time=0.25,
        )

        self.wait_timed(0.30)

        self.xyz = xyz

    # =========================================================
    # 00:15 -> 00:22
    #
    # "Đó là triangulation, và là lý do hai góc nhìn mang lại
    # nhiều thông tin 3D hơn một góc nhìn."
    # =========================================================

    def sentence_5(self):

        # -----------------------------------------------------
        # "Đó là triangulation"
        # -----------------------------------------------------

        triangle = Polygon(
            self.cam1_pos,
            self.world_point_pos,
            self.cam2_pos,
            stroke_color=WHITE,
            stroke_width=1.1,
            stroke_opacity=0.30,
            fill_color=VIOLET,
            fill_opacity=0.025,
        )

        self.play_timed(
            FadeIn(
                triangle
            ),
            run_time=0.45,
        )

        triangulation_label = Text(
            "TRIANGULATION",
            font_size=21,
            color=WHITE,
        )

        triangulation_label.set_opacity(0.82)

        triangulation_label.to_edge(
            UP,
            buff=0.55,
        )

        self.play_timed(
            FadeIn(
                triangulation_label,
                shift=DOWN * 0.08,
            ),
            run_time=0.45,
        )

        # -----------------------------------------------------
        # Compare one view vs two views
        # -----------------------------------------------------

        # One-view ambiguity ghosts
        one_view_candidates = VGroup()

        direction = (
            self.world_point_pos
            - self.cam1_pos
        )
        direction /= np.linalg.norm(direction)

        for d in [4.4, 5.3, 6.1, 7.1]:
            p = self.cam1_pos + direction * d

            dot = Dot(
                p,
                radius=0.045,
                color=CYAN,
            )

            dot.set_opacity(0.18)

            one_view_candidates.add(dot)

        self.play_timed(
            FadeIn(
                one_view_candidates
            ),
            self.ray2.animate.set_opacity(0.08),
            self.cam2.animate.set_opacity(0.12),
            run_time=0.55,
        )

        # Show ambiguity when using only camera 1
        self.play_timed(
            LaggedStart(
                *[
                    Indicate(
                        p,
                        color=CYAN,
                        scale_factor=1.5,
                    )
                    for p in one_view_candidates
                ],
                lag_ratio=0.08,
            ),
            run_time=0.75,
        )

        # Bring second view back, all ambiguity collapses
        self.play_timed(
            self.cam2.animate.set_opacity(0.85),
            self.ray2.animate.set_opacity(1),
            FadeOut(
                one_view_candidates
            ),
            self.world_point.animate.scale(1.18),
            run_time=0.75,
        )

        # Quick convergence visual
        pulse1 = self.ray1[-1].copy().set_stroke(
            CYAN_SOFT,
            width=3,
        )

        pulse2 = self.ray2[-1].copy().set_stroke(
            MAGENTA,
            width=3,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse1,
                time_width=0.20,
            ),
            ShowPassingFlash(
                pulse2,
                time_width=0.20,
            ),
            run_time=0.55,
        )

        # Final semantic contrast
        one_view = Text(
            "1 view  →  ambiguity",
            font_size=19,
            color=MUTED,
        )

        two_views = Text(
            "2 views → 3D constraint",
            font_size=21,
            color=CYAN_SOFT,
        )

        comparison = VGroup(
            one_view,
            two_views,
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.10,
        )

        comparison.to_corner(
            DR,
            buff=0.55,
        )

        self.play_timed(
            FadeIn(
                comparison,
                shift=LEFT * 0.08,
            ),
            run_time=0.55,
        )

        self.play_timed(
            Indicate(
                self.world_point[-1],
                color=WHITE,
                scale_factor=1.45,
            ),
            run_time=0.55,
        )

        self.wait_timed(1.40)

    # =========================================================
    # HELPERS
    # =========================================================

    def make_camera_frustum(
        self,
        center,
        plane_x,
        color,
        facing_left=False,
    ):
        center = np.array(center, dtype=float)

        half_height = 0.72

        top = np.array([
            plane_x,
            0.55,
            0.0,
        ])

        bottom = np.array([
            plane_x,
            -0.85,
            0.0,
        ])

        core_outer = Circle(
            radius=0.20,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        ).move_to(center)

        core = Dot(
            center,
            radius=0.055,
            color=color,
        )

        edges = VGroup(
            Line(
                center,
                top,
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.30,
            ),
            Line(
                center,
                bottom,
                color=color,
                stroke_width=1.0,
                stroke_opacity=0.30,
            ),
        )

        plane = Line(
            top,
            bottom,
            color=color,
            stroke_width=1.3,
            stroke_opacity=0.70,
        )

        plane_glow = Line(
            top,
            bottom,
            color=color,
            stroke_width=5,
            stroke_opacity=0.025,
        )

        return VGroup(
            core_outer,
            edges,
            plane_glow,
            plane,
            core,
        )

    def make_pixel(
        self,
        point,
        color,
    ):
        halo = Square(
            side_length=0.28,
            stroke_color=color,
            stroke_width=1.0,
            stroke_opacity=0.12,
        )

        core = Square(
            side_length=0.13,
            stroke_color=WHITE,
            stroke_width=0.8,
            fill_color=color,
            fill_opacity=1.0,
        )

        group = VGroup(
            halo,
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
            radius=radius * 3.0,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        )

        mid = Circle(
            radius=radius * 1.8,
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

    def make_glow_line(
        self,
        start,
        end,
        color,
    ):
        return VGroup(
            Line(
                start,
                end,
                color=color,
                stroke_width=10,
                stroke_opacity=0.025,
            ),
            Line(
                start,
                end,
                color=color,
                stroke_width=5,
                stroke_opacity=0.07,
            ),
            Line(
                start,
                end,
                color=color,
                stroke_width=1.8,
                stroke_opacity=0.92,
            ),
        )

    def extend_ray(
        self,
        start,
        through,
        length,
    ):
        direction = (
            through - start
        )

        direction /= np.linalg.norm(
            direction
        )

        return (
            start
            + direction * length
        )

    def intersect_with_vertical_plane(
        self,
        start,
        target,
        plane_x,
    ):
        direction = target - start

        t = (
            plane_x - start[0]
        ) / direction[0]

        return (
            start
            + direction * t
        )