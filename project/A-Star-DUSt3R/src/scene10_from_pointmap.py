from manim import *
import numpy as np

from theme import *


class Scene10FromPointmap(Scene):
    """
    Audio: Đoạn 10.wav
    Duration: 52.71s

    00:00.00-00:03.72
    "Bây giờ ta thấy sức mạnh của representation này."

    00:04.56-00:12.04
    "Nếu hai pixel ở hai ảnh được dự đoán tới gần cùng một vị trí 3D,
    chúng rất có khả năng là cùng một điểm ngoài đời."

    00:12.82-00:15.12
    "Vậy correspondence có thể suy ra từ pointmap."

    00:16.08-00:21.84
    "Nếu biết pixel và 3D point tương ứng,
    camera parameters cũng có thể được recover."

    00:21.84-00:32.38
    "Và nếu cùng một scene được biểu diễn trong hai coordinate frames
    khác nhau, ta có thể tìm phép xoay, dịch chuyển và scale
    làm hai point clouds khớp nhau."

    00:33.14-00:35.98
    "Phép biến đổi đó cho ta mối quan hệ giữa hai camera."

    00:36.58-00:42.30
    "Từ một representation duy nhất, ta có thể suy ra
    depth, matching, camera pose và reconstruction."

    00:42.66-00:47.32
    "Không phải vì network có một output riêng cho từng task."

    00:48.26-00:52.71
    "Mà vì tất cả chúng đều là những góc nhìn khác nhau
    của cùng một geometry."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_scene()

        self.sentence_1()
        self.wait_until(4.56)

        self.sentence_2()
        self.wait_until(12.82)

        self.sentence_3()
        self.wait_until(16.08)

        self.sentence_4()
        self.wait_until(21.84)

        self.sentence_5()
        self.wait_until(33.14)

        self.sentence_6()
        self.wait_until(36.58)

        self.sentence_7()
        self.wait_until(42.66)

        self.sentence_8()
        self.wait_until(48.26)

        self.sentence_9()
        self.wait_until(52.71)

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
        self.rows = 5
        self.cols = 8

        self.pointmap = self.make_pointmap(
            center=ORIGIN,
            color_a=CYAN,
            color_b=VIOLET,
            seed=12,
        )

    # =========================================================
    # 00:00 -> 00:03.72
    #
    # "Bây giờ ta thấy sức mạnh của representation này."
    # =========================================================

    def sentence_1(self):

        self.pointmap.scale(
            1.15
        )

        self.play_timed(
            FadeIn(
                self.pointmap,
                scale=0.94,
            ),
            run_time=0.75,
        )

        halo = SurroundingRectangle(
            self.pointmap,
            buff=0.30,
            corner_radius=0.16,
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.16,
        )

        self.play_timed(
            FadeIn(
                halo
            ),
            run_time=0.40,
        )

        pulse = halo.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.5,
            opacity=0.60,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.60,
        )

        label = Text(
            "POINTMAP",
            font_size=24,
            color=WHITE,
        )

        label.next_to(
            self.pointmap,
            UP,
            buff=0.34,
        )

        self.play_timed(
            FadeIn(
                label,
                shift=UP * 0.06,
            ),
            run_time=0.40,
        )

        self.wait_timed(0.55)

        self.pointmap_halo = halo
        self.pointmap_label = label

    # =========================================================
    # 00:04.56 -> 00:12.04
    #
    # "Nếu hai pixel ở hai ảnh được dự đoán tới gần
    # cùng một vị trí 3D..."
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            self.pointmap.animate
            .scale(0.72)
            .move_to(DOWN * 1.25),

            self.pointmap_halo.animate
            .scale(0.72)
            .move_to(DOWN * 1.25),

            self.pointmap_label.animate
            .shift(DOWN * 1.35)
            .set_opacity(0.30),

            run_time=0.55,
        )

        image_a = self.make_image_grid(
            center=LEFT * 3.45 + UP * 1.65,
            accent=CYAN,
            variant=0,
        )

        image_b = self.make_image_grid(
            center=RIGHT * 3.45 + UP * 1.65,
            accent=VIOLET,
            variant=1,
        )

        self.play_timed(
            FadeIn(
                image_a,
                shift=DOWN * 0.06,
            ),
            FadeIn(
                image_b,
                shift=DOWN * 0.06,
            ),
            run_time=0.55,
        )

        pixel_a = self.make_pixel(
            image_a.get_center()
            + RIGHT * 0.30
            + UP * 0.15,
            CYAN,
        )

        pixel_b = self.make_pixel(
            image_b.get_center()
            + LEFT * 0.38
            + UP * 0.04,
            VIOLET,
        )

        self.play_timed(
            GrowFromCenter(pixel_a),
            GrowFromCenter(pixel_b),
            run_time=0.45,
        )

        # Same 3D location.
        world_pos = np.array([
            0.15,
            -0.55,
            0,
        ])

        point_a = self.make_glow_point(
            world_pos + LEFT * 0.28,
            CYAN,
        )

        point_b = self.make_glow_point(
            world_pos + RIGHT * 0.28,
            VIOLET,
        )

        path_a = CubicBezier(
            pixel_a.get_center(),
            pixel_a.get_center() + DOWN * 0.9,
            point_a.get_center() + LEFT * 0.7 + UP * 0.3,
            point_a.get_center(),
        )

        path_b = CubicBezier(
            pixel_b.get_center(),
            pixel_b.get_center() + DOWN * 0.9,
            point_b.get_center() + RIGHT * 0.7 + UP * 0.3,
            point_b.get_center(),
        )

        self.add(
            point_a,
            point_b,
        )

        self.play_timed(
            MoveAlongPath(
                point_a,
                path_a,
            ),
            MoveAlongPath(
                point_b,
                path_b,
            ),
            run_time=1.05,
        )

        # They converge in 3D.
        self.play_timed(
            point_a.animate.move_to(
                world_pos + LEFT * 0.055
            ),
            point_b.animate.move_to(
                world_pos + RIGHT * 0.055
            ),
            run_time=0.85,
        )

        proximity_ring = Circle(
            radius=0.22,
            stroke_color=WHITE,
            stroke_width=1.3,
            stroke_opacity=0.65,
        ).move_to(
            world_pos
        )

        self.play_timed(
            GrowFromCenter(
                proximity_ring
            ),
            run_time=0.40,
        )

        self.play_timed(
            proximity_ring.animate
            .scale(1.75)
            .set_opacity(0),
            run_time=0.45,
        )

        # Trace back to the source pixels.
        line_a = Line(
            pixel_a.get_center(),
            world_pos,
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.22,
        )

        line_b = Line(
            pixel_b.get_center(),
            world_pos,
            color=VIOLET,
            stroke_width=1.0,
            stroke_opacity=0.22,
        )

        self.play_timed(
            Create(line_a),
            Create(line_b),
            run_time=0.55,
        )

        self.play_timed(
            Indicate(
                pixel_a[-1],
                color=CYAN,
                scale_factor=1.35,
            ),
            Indicate(
                pixel_b[-1],
                color=VIOLET,
                scale_factor=1.35,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.55)

        self.image_a = image_a
        self.image_b = image_b
        self.pixel_a = pixel_a
        self.pixel_b = pixel_b

        self.match_point_a = point_a
        self.match_point_b = point_b

        self.match_line_a = line_a
        self.match_line_b = line_b

    # =========================================================
    # 00:12.82 -> 00:15.12
    #
    # "Vậy correspondence có thể suy ra từ pointmap."
    # =========================================================

    def sentence_3(self):

        # Direct pixel correspondence appears only AFTER
        # geometry has established the relationship.
        correspondence = CubicBezier(
            self.pixel_a.get_right(),
            self.pixel_a.get_right()
            + RIGHT * 1.2
            + DOWN * 0.25,

            self.pixel_b.get_left()
            + LEFT * 1.2
            + DOWN * 0.25,

            self.pixel_b.get_left(),
        )

        correspondence.set_stroke(
            CYAN_SOFT,
            width=1.5,
            opacity=0.58,
        )

        self.play_timed(
            Create(
                correspondence
            ),
            run_time=0.65,
        )

        pulse = correspondence.copy()

        pulse.set_stroke(
            WHITE,
            width=3,
            opacity=0.85,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.20,
            ),
            run_time=0.55,
        )

        inferred = Text(
            "correspondence",
            font_size=18,
            color=CYAN_SOFT,
        )

        inferred.next_to(
            correspondence,
            UP,
            buff=0.10,
        )

        self.play_timed(
            FadeIn(
                inferred,
                shift=UP * 0.04,
            ),
            run_time=0.35,
        )

        self.wait_timed(0.30)

        self.correspondence = correspondence
        self.correspondence_label = inferred

    # =========================================================
    # 00:16.08 -> 00:21.84
    #
    # "pixel và 3D point tương ứng...
    # camera parameters recover."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            FadeOut(
                self.correspondence
            ),
            FadeOut(
                self.correspondence_label
            ),
            FadeOut(
                self.match_point_a
            ),
            FadeOut(
                self.match_point_b
            ),
            FadeOut(
                self.match_line_a
            ),
            FadeOut(
                self.match_line_b
            ),
            self.image_b.animate.set_opacity(
                0.10
            ),
            self.pixel_b.animate.set_opacity(
                0.10
            ),
            run_time=0.45,
        )

        # Multiple pixel <-> 3D pairs.
        pairs = VGroup()

        pixel_positions = [
            self.image_a.get_center()
            + np.array([-0.60, 0.32, 0]),

            self.image_a.get_center()
            + np.array([0.16, 0.14, 0]),

            self.image_a.get_center()
            + np.array([0.55, -0.32, 0]),
        ]

        world_positions = [
            LEFT * 1.0 + DOWN * 0.55,
            RIGHT * 0.05 + DOWN * 0.82,
            RIGHT * 1.20 + DOWN * 0.35,
        ]

        for source, target in zip(
            pixel_positions,
            world_positions,
        ):
            p = Dot(
                source,
                radius=0.032,
                color=CYAN,
            )

            q = Dot(
                target,
                radius=0.045,
                color=VIOLET,
            )

            line = Line(
                source,
                target,
                color=CYAN_SOFT,
                stroke_width=0.8,
                stroke_opacity=0.20,
            )

            pairs.add(
                VGroup(
                    line,
                    p,
                    q,
                )
            )

        self.play_timed(
            LaggedStart(
                *[
                    AnimationGroup(
                        Create(pair[0]),
                        GrowFromCenter(pair[1]),
                        GrowFromCenter(pair[2]),
                    )
                    for pair in pairs
                ],
                lag_ratio=0.13,
            ),
            run_time=0.85,
        )

        # Camera initially absent / unknown.
        camera_pos = (
            LEFT * 3.45
            + DOWN * 1.55
        )

        inferred_camera = self.make_camera(
            camera_pos,
            CYAN,
            angle=-9 * DEGREES,
        )

        inferred_camera.set_opacity(
            0
        )

        rays = VGroup()

        for pair in pairs:
            rays.add(
                Line(
                    camera_pos,
                    pair[2].get_center(),
                    color=CYAN,
                    stroke_width=0.8,
                    stroke_opacity=0.20,
                )
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(r)
                    for r in rays
                ],
                lag_ratio=0.10,
            ),
            run_time=0.65,
        )

        # Camera emerges as the geometry becomes sufficient.
        self.play_timed(
            inferred_camera.animate.set_opacity(
                0.92
            ),
            run_time=0.55,
        )

        pose = MathTex(
            r"\hat{R},\hat{t}",
            font_size=29,
            color=CYAN,
        )

        pose.next_to(
            inferred_camera,
            DOWN,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(
                pose,
                shift=UP * 0.05,
            ),
            run_time=0.45,
        )

        self.play_timed(
            Indicate(
                inferred_camera[-1],
                color=CYAN_SOFT,
                scale_factor=1.35,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.45)

        self.pixel_3d_pairs = pairs
        self.recovered_camera = inferred_camera
        self.recovered_pose = pose
        self.recovered_rays = rays

    # =========================================================
    # 00:21.84 -> 00:32.38
    #
    # Different coordinate frames -> rotate/translate/scale
    # until point clouds align.
    # =========================================================

    def sentence_5(self):

        self.play_timed(
            FadeOut(self.image_a),
            FadeOut(self.image_b),
            FadeOut(self.pixel_a),
            FadeOut(self.pixel_b),
            FadeOut(self.pointmap),
            FadeOut(self.pointmap_halo),
            FadeOut(self.pointmap_label),
            FadeOut(self.pixel_3d_pairs),
            FadeOut(self.recovered_camera),
            FadeOut(self.recovered_pose),
            FadeOut(self.recovered_rays),
            run_time=0.50,
        )

        cloud_a = self.make_cloud(
            center=LEFT * 2.4,
            color=CYAN,
            seed=3,
        )

        cloud_b = cloud_a.copy()

        cloud_b.set_color(
            VIOLET
        )

        # Deliberately put B in another frame.
        cloud_b.scale(
            1.35
        )

        cloud_b.rotate(
            23 * DEGREES
        )

        cloud_b.shift(
            RIGHT * 5.0
            + UP * 0.60
        )

        self.play_timed(
            FadeIn(
                cloud_a,
                scale=0.90,
            ),
            FadeIn(
                cloud_b,
                scale=1.10,
            ),
            run_time=0.65,
        )

        frame_a = self.make_coordinate_frame(
            LEFT * 4.6 + DOWN * 1.7,
            CYAN,
        )

        frame_b = self.make_coordinate_frame(
            RIGHT * 4.7 + UP * 1.5,
            VIOLET,
        )

        self.play_timed(
            FadeIn(frame_a),
            FadeIn(frame_b),
            run_time=0.45,
        )

        # ---------------------------------------------
        # ROTATION
        # ---------------------------------------------

        rotate_symbol = MathTex(
            r"R",
            font_size=30,
            color=VIOLET,
        )

        rotate_symbol.move_to(
            UP * 2.55
        )

        self.play_timed(
            FadeIn(
                rotate_symbol
            ),
            run_time=0.30,
        )

        self.play_timed(
            cloud_b.animate.rotate(
                -23 * DEGREES
            ),
            frame_b.animate.rotate(
                -23 * DEGREES
            ),
            run_time=1.10,
            rate_func=smooth,
        )

        # ---------------------------------------------
        # SCALE
        # ---------------------------------------------

        scale_symbol = MathTex(
            r"s",
            font_size=30,
            color=CYAN_SOFT,
        )

        scale_symbol.move_to(
            rotate_symbol
        )

        self.play_timed(
            Transform(
                rotate_symbol,
                scale_symbol,
            ),
            run_time=0.30,
        )

        self.play_timed(
            cloud_b.animate.scale(
                1 / 1.35
            ),
            frame_b.animate.scale(
                1 / 1.35
            ),
            run_time=1.00,
            rate_func=smooth,
        )

        # ---------------------------------------------
        # TRANSLATION
        # ---------------------------------------------

        translate_symbol = MathTex(
            r"t",
            font_size=30,
            color=MAGENTA,
        )

        translate_symbol.move_to(
            rotate_symbol
        )

        self.play_timed(
            Transform(
                rotate_symbol,
                translate_symbol,
            ),
            run_time=0.30,
        )

        target_center = cloud_a.get_center()

        offset = (
            target_center
            - cloud_b.get_center()
        )

        self.play_timed(
            cloud_b.animate.shift(
                offset
            ),
            frame_b.animate.shift(
                offset
            ),
            run_time=1.25,
            rate_func=smooth,
        )

        # Clouds now overlap.
        self.play_timed(
            cloud_a.animate.set_opacity(
                0.68
            ),
            cloud_b.animate.set_opacity(
                0.68
            ),
            run_time=0.35,
        )

        overlap = Circle(
            radius=1.35,
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.18,
        ).move_to(
            cloud_a
        )

        self.play_timed(
            FadeIn(
                overlap,
                scale=0.75,
            ),
            run_time=0.35,
        )

        self.play_timed(
            overlap.animate
            .scale(1.30)
            .set_opacity(0),
            FadeOut(
                rotate_symbol
            ),
            run_time=0.45,
        )

        self.wait_timed(0.70)

        self.cloud_a = cloud_a
        self.cloud_b = cloud_b

        self.frame_a = frame_a
        self.frame_b = frame_b

    # =========================================================
    # 00:33.14 -> 00:35.98
    #
    # "Phép biến đổi đó cho ta mối quan hệ giữa hai camera."
    # =========================================================

    def sentence_6(self):

        self.play_timed(
            self.cloud_a.animate.set_opacity(
                0.18
            ),
            self.cloud_b.animate.set_opacity(
                0.18
            ),
            FadeOut(self.frame_a),
            FadeOut(self.frame_b),
            run_time=0.35,
        )

        cam1 = self.make_camera(
            LEFT * 3.0 + DOWN * 1.2,
            CYAN,
            angle=-8 * DEGREES,
        )

        cam2 = self.make_camera(
            RIGHT * 3.0 + DOWN * 1.2,
            VIOLET,
            angle=12 * DEGREES,
        )

        self.play_timed(
            FadeIn(
                cam1,
                scale=0.85,
            ),
            FadeIn(
                cam2,
                scale=0.85,
            ),
            run_time=0.45,
        )

        relation = CurvedArrow(
            cam1.get_top(),
            cam2.get_top(),
            angle=-0.30,
            color=WHITE,
            stroke_width=1.4,
            stroke_opacity=0.55,
        )

        # Create, not GrowArrow: safer with CurvedArrow on Manim 0.21.
        self.play_timed(
            Create(
                relation
            ),
            run_time=0.50,
        )

        relative_pose = MathTex(
            r"(R,t,s)",
            font_size=28,
            color=WHITE,
        )

        relative_pose.next_to(
            relation,
            UP,
            buff=0.12,
        )

        self.play_timed(
            FadeIn(
                relative_pose
            ),
            run_time=0.35,
        )

        self.play_timed(
            ShowPassingFlash(
                relation.copy().set_stroke(
                    CYAN_SOFT,
                    width=3,
                    opacity=0.8,
                ),
                time_width=0.22,
            ),
            run_time=0.45,
        )

        self.wait_timed(0.45)

        self.cam1 = cam1
        self.cam2 = cam2
        self.camera_relation = relation
        self.relative_pose = relative_pose

    # =========================================================
    # 00:36.58 -> 00:42.30
    #
    # "Từ một representation duy nhất..."
    # =========================================================

    def sentence_7(self):

        self.play_timed(
            FadeOut(self.cloud_a),
            FadeOut(self.cloud_b),
            FadeOut(self.cam1),
            FadeOut(self.cam2),
            FadeOut(self.camera_relation),
            FadeOut(self.relative_pose),
            run_time=0.40,
        )

        central = self.make_pointmap(
            center=ORIGIN,
            color_a=CYAN,
            color_b=VIOLET,
            seed=12,
        )

        central.scale(
            0.78
        )

        self.play_timed(
            FadeIn(
                central,
                scale=0.92,
            ),
            run_time=0.55,
        )

        tasks = [
            ("DEPTH", UP * 2.55, CYAN),
            ("MATCHING", LEFT * 4.3, CYAN_SOFT),
            ("CAMERA POSE", RIGHT * 4.3, VIOLET),
            ("RECONSTRUCTION", DOWN * 2.55, MAGENTA),
        ]

        task_mobjects = VGroup()
        links = VGroup()

        for name, pos, color in tasks:

            task = Text(
                name,
                font_size=18,
                color=color,
            )

            task.move_to(
                pos
            )

            line = Line(
                central.get_center(),
                task.get_center(),
                color=color,
                stroke_width=1,
                stroke_opacity=0.18,
            )

            task_mobjects.add(
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
                        task_mobjects,
                    )
                ],
                lag_ratio=0.13,
            ),
            run_time=1.20,
        )

        # Four pulses derive outward from the SAME geometry.
        self.play_timed(
            *[
                ShowPassingFlash(
                    line.copy().set_stroke(
                        task.get_color(),
                        width=2.8,
                        opacity=0.80,
                    ),
                    time_width=0.22,
                )
                for line, task in zip(
                    links,
                    task_mobjects,
                )
            ],
            run_time=0.75,
        )

        self.play_timed(
            central.animate.scale(
                1.06
            ),
            run_time=0.40,
        )

        self.wait_timed(0.55)

        self.central_pointmap = central
        self.task_labels = task_mobjects
        self.task_links = links

    # =========================================================
    # 00:42.66 -> 00:47.32
    #
    # "Không phải vì network có một output riêng cho từng task."
    # =========================================================

    def sentence_8(self):

        # Briefly show the WRONG mental model:
        # one output head per task.
        head_boxes = VGroup()

        for task in self.task_labels:

            box = RoundedRectangle(
                width=task.width + 0.45,
                height=0.55,
                corner_radius=0.08,
                stroke_color=task.get_color(),
                stroke_width=1.0,
                stroke_opacity=0.35,
                fill_color=SURFACE,
                fill_opacity=0.25,
            )

            box.move_to(
                task
            )

            head_boxes.add(
                box
            )

        self.play_timed(
            FadeIn(
                head_boxes
            ),
            run_time=0.45,
        )

        strikes = VGroup()

        for box in head_boxes:

            strike = Line(
                box.get_corner(DL),
                box.get_corner(UR),
                color=RED,
                stroke_width=1.7,
                stroke_opacity=0.60,
            )

            strikes.add(
                strike
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(s)
                    for s in strikes
                ],
                lag_ratio=0.09,
            ),
            run_time=0.65,
        )

        self.play_timed(
            head_boxes.animate.set_opacity(
                0.10
            ),
            strikes.animate.set_opacity(
                0.16
            ),
            self.task_labels.animate.set_opacity(
                0.30
            ),
            self.task_links.animate.set_opacity(
                0.10
            ),
            self.central_pointmap.animate.set_opacity(
                1.0
            ),
            run_time=0.60,
        )

        # Central representation remains.
        self.play_timed(
            Indicate(
                self.central_pointmap[1][18],
                color=WHITE,
                scale_factor=1.55,
            ),
            run_time=0.45,
        )

        self.play_timed(
            FadeOut(
                head_boxes
            ),
            FadeOut(
                strikes
            ),
            run_time=0.40,
        )

        self.wait_timed(0.50)

    # =========================================================
    # 00:48.26 -> 00:52.71
    #
    # "...góc nhìn khác nhau của cùng một geometry."
    # =========================================================

    def sentence_9(self):

        # Tasks stop looking like independent destinations.
        self.play_timed(
            self.task_labels.animate.set_opacity(
                0.78
            ),
            self.task_links.animate.set_opacity(
                0.28
            ),
            run_time=0.40,
        )

        geometry_ring = Circle(
            radius=2.05,
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.16,
        )

        geometry_ring.move_to(
            self.central_pointmap
        )

        self.play_timed(
            Create(
                geometry_ring
            ),
            run_time=0.55,
        )

        # Fold all semantic views inward toward the same geometry.
        self.play_timed(
            self.task_labels[0].animate.move_to(
                UP * 1.45
            ),
            self.task_labels[1].animate.move_to(
                LEFT * 2.25
            ),
            self.task_labels[2].animate.move_to(
                RIGHT * 2.25
            ),
            self.task_labels[3].animate.move_to(
                DOWN * 1.45
            ),
            run_time=0.65,
        )

        geometry = Text(
            "SAME GEOMETRY",
            font_size=22,
            color=WHITE,
        )

        geometry.next_to(
            self.central_pointmap,
            DOWN,
            buff=0.30,
        )

        self.play_timed(
            FadeIn(
                geometry,
                shift=UP * 0.06,
            ),
            run_time=0.45,
        )

        # One final pulse from center to every interpretation.
        for line in self.task_links:

            pulse = line.copy()

            pulse.set_stroke(
                WHITE,
                width=2.3,
                opacity=0.65,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.18,
                ),
                run_time=0.25,
            )

        self.play_timed(
            self.central_pointmap.animate.scale(
                1.05
            ),
            geometry_ring.animate.set_opacity(
                0.26
            ),
            run_time=0.35,
        )

        self.wait_timed(0.40)

    # =========================================================
    # COMPONENTS
    # =========================================================

    def make_pixel(self, point, color):

        halo = Square(
            side_length=0.25,
            stroke_color=color,
            stroke_width=1,
            stroke_opacity=0.14,
        )

        core = Square(
            side_length=0.12,
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
        radius=0.065,
    ):

        outer = Circle(
            radius=radius * 3.2,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.025,
        )

        middle = Circle(
            radius=radius * 1.9,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.07,
        )

        core = Dot(
            radius=radius,
            color=color,
        )

        result = VGroup(
            outer,
            middle,
            core,
        )

        result.move_to(
            point
        )

        return result

    def make_image_grid(
        self,
        center,
        accent,
        variant=0,
    ):

        width = 3.3
        height = 2.05

        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1,
            stroke_opacity=0.30,
            fill_color=SURFACE,
            fill_opacity=0.92,
        )

        frame.move_to(
            center
        )

        pixels = VGroup()

        rows = 4
        cols = 7

        cw = width / cols
        ch = height / rows

        left = center[0] - width / 2
        bottom = center[1] - height / 2

        for row in range(rows):
            for col in range(cols):

                x = (
                    left
                    + (col + 0.5) * cw
                )

                y = (
                    bottom
                    + (
                        rows - row - 0.5
                    ) * ch
                )

                t = (
                    0.55 * col / (cols - 1)
                    + 0.25 * row / (rows - 1)
                )

                base = interpolate_color(
                    ManimColor("#263141"),
                    ManimColor("#56647A"),
                    t,
                )

                if variant == 1:
                    base = interpolate_color(
                        base,
                        ManimColor(VIOLET),
                        0.10,
                    )

                pixel = Square(
                    side_length=min(
                        cw,
                        ch,
                    ) * 0.90,
                    stroke_color="#5B6373",
                    stroke_width=0.35,
                    stroke_opacity=0.14,
                    fill_color=base,
                    fill_opacity=0.92,
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

        camera = VGroup(
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

        camera.rotate(
            angle
        )

        camera.move_to(
            center
        )

        return camera

    def make_coordinate_frame(
        self,
        origin,
        color,
    ):

        x = Arrow(
            origin,
            origin + RIGHT * 0.60,
            buff=0,
            color=CYAN,
            stroke_width=1.1,
            max_tip_length_to_length_ratio=0.17,
        )

        y = Arrow(
            origin,
            origin + UP * 0.60,
            buff=0,
            color=VIOLET,
            stroke_width=1.1,
            max_tip_length_to_length_ratio=0.17,
        )

        z = Arrow(
            origin,
            origin
            + LEFT * 0.28
            + DOWN * 0.27,
            buff=0,
            color=MAGENTA,
            stroke_width=1.1,
            max_tip_length_to_length_ratio=0.17,
        )

        o = Dot(
            origin,
            radius=0.035,
            color=color,
        )

        return VGroup(
            x,
            y,
            z,
            o,
        )

    def make_cloud(
        self,
        center,
        color,
        seed=0,
    ):

        rng = np.random.default_rng(
            seed
        )

        points = VGroup()
        edges = VGroup()

        positions = []

        for i in range(20):

            theta = (
                i / 20
                * TAU
            )

            radius = (
                0.65
                + 0.18
                * np.sin(
                    3 * theta
                )
            )

            x = (
                radius
                * np.cos(theta)
            )

            y = (
                0.65
                * radius
                * np.sin(theta)
            )

            x += rng.uniform(
                -0.08,
                0.08,
            )

            y += rng.uniform(
                -0.08,
                0.08,
            )

            p = (
                np.array([
                    x,
                    y,
                    0,
                ])
                + center
            )

            positions.append(
                p
            )

            points.add(
                Dot(
                    p,
                    radius=0.037,
                    color=color,
                )
            )

        for i in range(len(positions)):

            edges.add(
                Line(
                    positions[i],
                    positions[
                        (i + 1)
                        % len(positions)
                    ],
                    color=color,
                    stroke_width=0.65,
                    stroke_opacity=0.16,
                )
            )

        return VGroup(
            edges,
            points,
        )

    def make_pointmap(
        self,
        center,
        color_a,
        color_b,
        seed=1,
    ):

        rng = np.random.default_rng(
            seed
        )

        points = VGroup()
        mesh = VGroup()

        positions = []

        for row in range(self.rows):

            current = []

            for col in range(self.cols):

                u = col / (
                    self.cols - 1
                )

                v = row / (
                    self.rows - 1
                )

                x = (
                    u - 0.5
                ) * 3.8

                y = (
                    0.5 - v
                ) * 2.2

                depth = (
                    0.38
                    + 0.48
                    * np.sin(
                        np.pi * u
                    )
                    * np.cos(
                        np.pi * v
                    )
                    + rng.uniform(
                        -0.018,
                        0.018,
                    )
                )

                p = np.array([
                    center[0]
                    + x
                    + depth * 0.52,

                    center[1]
                    + y
                    + depth * 0.27,

                    0,
                ])

                current.append(
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
                        radius=0.028,
                        color=color,
                    )
                )

            positions.append(
                current
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
                        stroke_opacity=0.22,
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
                        stroke_opacity=0.18,
                    )
                )

        return VGroup(
            mesh,
            points,
        )