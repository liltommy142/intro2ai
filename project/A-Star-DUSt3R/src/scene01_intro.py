from manim import *
import numpy as np

from theme import *


# ============================================================
# Scene 01
# Actual narration duration: 00:00 -> 00:28
# ============================================================


class Scene01Intro(Scene):
    """
    00:00-00:03
    Đây là hai bức ảnh của cùng một căn phòng.

    00:04-00:14
    Chúng chỉ là những lưới pixel hai chiều...
    ...

    00:15-00:20
    Vậy mà khi nhìn vào chúng...

    00:21-00:23
    Vậy một máy tính sẽ làm điều đó như thế nào?

    00:25-00:28
    Hay nói chính xác hơn...
    """

    def construct(self):
        self.camera.background_color = BG

        # Timeline clock.
        # Dùng để scene không bị lệch khỏi recording.
        self.t = 0.0

        self.sentence_1()
        self.wait_until(4.0)

        self.sentence_2()
        self.wait_until(15.0)

        self.sentence_3()
        self.wait_until(21.0)

        self.sentence_4()
        self.wait_until(25.0)

        self.sentence_5()

        # Chính xác hết 28 giây.
        self.wait_until(28.0)

    # ========================================================
    # Timeline helper
    # ========================================================

    def play_timed(self, *animations, run_time=1.0, **kwargs):
        self.play(
            *animations,
            run_time=run_time,
            **kwargs,
        )
        self.t += run_time

    def wait_timed(self, duration):
        if duration <= 0:
            return

        self.wait(duration)
        self.t += duration

    def wait_until(self, timestamp):
        remaining = timestamp - self.t

        if remaining > 0:
            self.wait_timed(remaining)

    # ========================================================
    # CÂU 1
    # 00:00 -> 00:03
    #
    # “Đây là hai bức ảnh của cùng một căn phòng.”
    # ========================================================

    def sentence_1(self):

        # Hai góc nhìn cùng một scene.
        left_view = self.make_room_view(
            perspective=-1,
        )

        right_view = self.make_room_view(
            perspective=1,
        )

        left_view.scale(0.88)
        right_view.scale(0.88)

        left_view.move_to(
            LEFT * 3.0
        )

        right_view.move_to(
            RIGHT * 3.0
        )

        # Một line rất nhỏ phía trên tạo visual hierarchy.
        tag = Text(
            "SAME SCENE",
            font_size=14,
            color=MUTED,
        )

        tag.set_opacity(0.65)
        tag.to_edge(UP, buff=0.45)

        self.play_timed(
            AnimationGroup(
                FadeIn(
                    left_view,
                    shift=UP * 0.12,
                    scale=0.96,
                ),
                FadeIn(
                    right_view,
                    shift=UP * 0.12,
                    scale=0.96,
                ),
                lag_ratio=0.12,
            ),
            run_time=1.15,
        )

        self.play_timed(
            FadeIn(
                tag,
                shift=DOWN * 0.05,
            ),
            run_time=0.35,
        )

        # Subtle floating motion.
        self.play_timed(
            left_view.animate.shift(
                RIGHT * 0.06
            ),
            right_view.animate.shift(
                LEFT * 0.06
            ),
            run_time=0.8,
            rate_func=smooth,
        )

        self.wait_timed(0.7)

        self.left_view = left_view
        self.right_view = right_view
        self.same_scene_tag = tag

    # ========================================================
    # CÂU 2
    # 00:04 -> 00:14
    #
    # “Chúng chỉ là những lưới pixel hai chiều.
    # Không có dòng chữ nào nói cho ta cái ghế cách camera
    # bao xa, bức tường nằm ở đâu, hay camera thứ hai đã
    # di chuyển như thế nào.”
    # ========================================================

    def sentence_2(self):

        left = self.left_view
        right = self.right_view

        # ----------------------------------------------------
        # 04.0 -> 06.2
        # “Chúng chỉ là những lưới pixel hai chiều.”
        # ----------------------------------------------------

        pixel_grid = self.make_pixel_grid()

        pixel_grid.move_to(
            ORIGIN
        )

        focus = RoundedRectangle(
            width=0.62,
            height=0.48,
            corner_radius=0.04,
            color=CYAN,
            stroke_width=1.5,
        )

        focus.move_to(
            left.get_center()
            + RIGHT * 0.35
            + DOWN * 0.12
        )

        self.play_timed(
            FadeOut(
                self.same_scene_tag
            ),
            Create(focus),
            run_time=0.35,
        )

        # Push image A forward.
        self.play_timed(
            right.animate
            .scale(0.82)
            .set_opacity(0.22)
            .shift(RIGHT * 0.5),

            left.animate
            .scale(1.32)
            .move_to(ORIGIN),

            focus.animate
            .scale(2.6)
            .move_to(ORIGIN),

            run_time=0.85,
        )

        # Entire image resolves into pixels.
        self.play_timed(
            FadeOut(
                left,
                run_time=0.1,
            ),
            FadeOut(
                focus,
                run_time=0.1,
            ),
            FadeIn(
                pixel_grid,
                scale=1.04,
            ),
            run_time=0.65,
        )

        # A few pixels pulse.
        selected_pixels = VGroup(
            pixel_grid[27],
            pixel_grid[43],
            pixel_grid[58],
        )

        self.play_timed(
            LaggedStart(
                *[
                    Indicate(
                        px,
                        color=CYAN,
                        scale_factor=1.5,
                    )
                    for px in selected_pixels
                ],
                lag_ratio=0.15,
            ),
            run_time=0.35,
        )

        # ----------------------------------------------------
        # 06.2 -> 09.0
        # “…cái ghế cách camera bao xa…”
        #
        # Không reveal 3D room.
        # Ta chỉ cho thấy GHẾ tồn tại ở ảnh nhưng depth
        # không có trong dữ liệu.
        # ----------------------------------------------------

        self.play_timed(
            FadeOut(
                pixel_grid,
                scale=0.97,
            ),
            FadeIn(
                left,
            ),
            right.animate.set_opacity(
                0.5
            ),
            run_time=0.45,
        )

        left.move_to(
            LEFT * 2.65
        )

        left.scale(
            1 / 1.32
        )

        # Locate chair within stylized room.
        chair_pos = (
            left.get_center()
            + LEFT * 0.38
            + DOWN * 0.30
        )

        chair_marker = self.make_focus_marker(
            chair_pos,
            CYAN,
        )

        self.play_timed(
            Create(
                chair_marker
            ),
            run_time=0.30,
        )

        # Depth axis begins at image,
        # but immediately disappears.
        depth_line = Line(
            chair_pos,
            chair_pos + RIGHT * 2.2,
            color=CYAN,
            stroke_width=1.2,
        )

        depth_line.set_opacity(
            0.65
        )

        unknown_depth = VGroup(
            Dot(
                chair_pos + RIGHT * 0.75,
                radius=0.045,
                color=CYAN,
            ),
            Dot(
                chair_pos + RIGHT * 1.35,
                radius=0.045,
                color=CYAN,
            ),
            Dot(
                chair_pos + RIGHT * 1.95,
                radius=0.045,
                color=CYAN,
            ),
        )

        unknown_depth.set_opacity(
            0.35
        )

        self.play_timed(
            Create(
                depth_line
            ),
            LaggedStart(
                *[
                    FadeIn(x)
                    for x in unknown_depth
                ],
                lag_ratio=0.15,
            ),
            run_time=0.55,
        )

        self.play_timed(
            depth_line.animate
            .set_opacity(0.08),

            unknown_depth.animate
            .set_opacity(0.08),

            run_time=0.35,
        )

        # ----------------------------------------------------
        # 09.0 -> 11.1
        # “…bức tường nằm ở đâu…”
        # ----------------------------------------------------

        wall_marker = self.make_focus_marker(
            left.get_center()
            + RIGHT * 0.82
            + UP * 0.42,
            VIOLET,
            width=1.25,
            height=0.82,
        )

        self.play_timed(
            FadeOut(
                chair_marker
            ),
            FadeOut(
                depth_line
            ),
            FadeOut(
                unknown_depth
            ),
            Create(
                wall_marker
            ),
            run_time=0.35,
        )

        # Several possible wall locations as ghost planes.
        ghost_walls = VGroup()

        for dx, opacity in [
            (0.45, 0.18),
            (0.90, 0.11),
            (1.35, 0.06),
        ]:
            wall = Rectangle(
                width=1.0,
                height=0.70,
                stroke_color=VIOLET,
                stroke_width=1,
                stroke_opacity=opacity,
                fill_color=VIOLET,
                fill_opacity=opacity * 0.12,
            )

            wall.move_to(
                wall_marker.get_center()
                + RIGHT * dx
            )

            ghost_walls.add(
                wall
            )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        wall,
                        shift=RIGHT * 0.08,
                    )
                    for wall in ghost_walls
                ],
                lag_ratio=0.12,
            ),
            run_time=0.55,
        )

        self.play_timed(
            ghost_walls.animate
            .set_opacity(0.05),
            run_time=0.25,
        )

        # ----------------------------------------------------
        # 11.1 -> 14.0
        # “…hay camera thứ hai đã di chuyển như thế nào.”
        # ----------------------------------------------------

        self.play_timed(
            FadeOut(
                wall_marker
            ),
            FadeOut(
                ghost_walls
            ),
            run_time=0.25,
        )

        # Second image gets emphasized.
        self.play_timed(
            right.animate
            .set_opacity(1)
            .scale(1.07),

            left.animate
            .set_opacity(0.45),

            run_time=0.35,
        )

        # Camera pose hypotheses.
        cam_center = (
            right.get_center()
            + DOWN * 1.75
        )

        cam_main = self.make_camera_pose(
            cam_center,
            angle=0,
            color=VIOLET,
            opacity=0.9,
        )

        cam_ghost_1 = self.make_camera_pose(
            cam_center
            + LEFT * 0.55
            + UP * 0.15,
            angle=18 * DEGREES,
            color=VIOLET,
            opacity=0.16,
        )

        cam_ghost_2 = self.make_camera_pose(
            cam_center
            + RIGHT * 0.55
            + UP * 0.05,
            angle=-18 * DEGREES,
            color=VIOLET,
            opacity=0.10,
        )

        self.play_timed(
            FadeIn(
                cam_main,
                scale=0.85,
            ),
            run_time=0.35,
        )

        self.play_timed(
            FadeIn(
                cam_ghost_1
            ),
            FadeIn(
                cam_ghost_2
            ),
            cam_main.animate.set_opacity(
                0.35
            ),
            run_time=0.45,
        )

        # End of sentence:
        # leave three unknown poses visible.
        self.play_timed(
            AnimationGroup(
                cam_ghost_1.animate.shift(
                    LEFT * 0.16
                ),
                cam_ghost_2.animate.shift(
                    RIGHT * 0.16
                ),
                lag_ratio=0,
            ),
            run_time=0.45,
        )

    # ========================================================
    # CÂU 3
    # 00:15 -> 00:20
    #
    # “Vậy mà khi nhìn vào chúng, chúng ta gần như ngay lập
    # tức cảm nhận được chiều sâu.”
    # ========================================================

    def sentence_3(self):

        # Clean uncertainty visualization.
        self.play_timed(
            FadeOut(
                *[
                    mob
                    for mob in self.mobjects
                    if mob not in [
                        self.left_view,
                        self.right_view,
                    ]
                ]
            ),
            self.left_view.animate
            .set_opacity(1)
            .move_to(LEFT * 2.75),

            self.right_view.animate
            .set_opacity(1)
            .move_to(RIGHT * 2.75),

            run_time=0.45,
        )

        # Make both photos slightly smaller,
        # revealing a central empty space.
        self.play_timed(
            self.left_view.animate
            .scale(0.84)
            .shift(LEFT * 0.2),

            self.right_view.animate
            .scale(0.84)
            .shift(RIGHT * 0.2),

            run_time=0.45,
        )

        # Central reconstruction:
        # points start as a flat layer...
        points = self.make_room_point_cloud()

        points.set_opacity(
            0
        )

        self.add(
            points
        )

        # ...then appear with simulated depth.
        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        dot,
                        scale=0.5,
                    )
                    for dot in points
                ],
                lag_ratio=0.012,
            ),
            run_time=1.35,
        )

        # Separate layers to visually suggest depth.
        near = VGroup(
            *points[:30]
        )

        middle = VGroup(
            *points[30:70]
        )

        far = VGroup(
            *points[70:]
        )

        self.play_timed(
            near.animate
            .scale(1.12)
            .set_opacity(0.95),

            middle.animate
            .scale(1.02)
            .set_opacity(0.72),

            far.animate
            .scale(0.92)
            .set_opacity(0.42),

            run_time=1.05,
        )

        # Thin connecting geometry.
        structure = self.make_room_wireframe()

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in structure
                ],
                lag_ratio=0.05,
            ),
            run_time=0.85,
        )

        self.play_timed(
            points.animate.shift(
                UP * 0.05
            ),
            structure.animate.shift(
                UP * 0.05
            ),
            run_time=0.55,
            rate_func=there_and_back,
        )

        self.wait_timed(0.3)

        self.reconstruction = VGroup(
            points,
            structure,
        )

    # ========================================================
    # CÂU 4
    # 00:21 -> 00:23
    #
    # “Vậy một máy tính sẽ làm điều đó như thế nào?”
    # ========================================================

    def sentence_4(self):

        # Human inferred 3D disappears.
        # Machine only receives arrays of pixels.
        self.play_timed(
            FadeOut(
                self.reconstruction,
                scale=0.92,
            ),
            self.left_view.animate
            .set_opacity(0.35),

            self.right_view.animate
            .set_opacity(0.35),

            run_time=0.40,
        )

        # Abstract machine cursor / processing indicator.
        machine = VGroup(
            Circle(
                radius=0.32,
                stroke_color=CYAN,
                stroke_width=1.3,
                stroke_opacity=0.75,
            ),
            Dot(
                radius=0.045,
                color=CYAN,
            ),
        )

        machine.move_to(
            ORIGIN
        )

        ring = Circle(
            radius=0.55,
            stroke_color=VIOLET,
            stroke_width=0.8,
            stroke_opacity=0.25,
        )

        ring.move_to(
            ORIGIN
        )

        self.play_timed(
            GrowFromCenter(
                machine
            ),
            FadeIn(
                ring,
                scale=0.7,
            ),
            run_time=0.45,
        )

        # machine "looks" at both images
        left_ray = Line(
            machine.get_left(),
            self.left_view.get_right(),
            color=CYAN,
            stroke_width=1,
            stroke_opacity=0.22,
        )

        right_ray = Line(
            machine.get_right(),
            self.right_view.get_left(),
            color=VIOLET,
            stroke_width=1,
            stroke_opacity=0.22,
        )

        self.play_timed(
            Create(
                left_ray
            ),
            Create(
                right_ray
            ),
            run_time=0.40,
        )

        self.play_timed(
            Rotate(
                ring,
                angle=PI / 2,
            ),
            run_time=0.45,
            rate_func=linear,
        )

        self.wait_timed(0.30)

        self.machine_group = VGroup(
            machine,
            ring,
            left_ray,
            right_ray,
        )

    # ========================================================
    # CÂU 5
    # 00:25 -> 00:28
    #
    # “Hay nói chính xác hơn:
    # Làm thế nào để biến những bức ảnh 2D
    # thành một thế giới 3D?”
    # ========================================================

    def sentence_5(self):

        self.play_timed(
            FadeOut(
                self.machine_group
            ),
            self.left_view.animate
            .set_opacity(1)
            .scale(0.80)
            .move_to(LEFT * 3.7),

            self.right_view.animate
            .set_opacity(1)
            .scale(0.80)
            .move_to(LEFT * 2.0),

            run_time=0.45,
        )

        # Both inputs grouped as a single "2D side".
        images = VGroup(
            self.left_view,
            self.right_view,
        )

        arrow = Arrow(
            start=LEFT * 0.50,
            end=RIGHT * 1.05,
            buff=0,
            stroke_width=1.8,
            color=CYAN,
            max_tip_length_to_length_ratio=0.12,
        )

        arrow.set_opacity(
            0.65
        )

        self.play_timed(
            GrowArrow(
                arrow
            ),
            run_time=0.45,
        )

        # Build 3D-looking world from points.
        world = self.make_room_point_cloud(
            scale=0.86
        )

        world.move_to(
            RIGHT * 3.0
        )

        wire = self.make_room_wireframe(
            scale=0.86
        )

        wire.move_to(
            RIGHT * 3.0
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        dot,
                        shift=RIGHT * 0.10,
                        scale=0.4,
                    )
                    for dot in world
                ],
                lag_ratio=0.008,
            ),
            run_time=0.75,
        )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in wire
                ],
                lag_ratio=0.04,
            ),
            run_time=0.45,
        )

        # Last 0.9 sec:
        # one tiny semantic label, not a PowerPoint title.
        label_2d = Text(
            "2D",
            font_size=16,
            color=MUTED,
        )

        label_3d = Text(
            "3D",
            font_size=16,
            color=VIOLET,
        )

        label_2d.next_to(
            images,
            DOWN,
            buff=0.20,
        )

        label_3d.next_to(
            world,
            DOWN,
            buff=0.20,
        )

        self.play_timed(
            FadeIn(
                label_2d
            ),
            FadeIn(
                label_3d
            ),
            world.animate.scale(
                1.04
            ),
            wire.animate.scale(
                1.04
            ),
            run_time=0.50,
        )

        self.wait_timed(0.40)

    # ========================================================
    # COMPONENTS LOCAL TO SCENE
    # Sau khi style ổn có thể move sang components.py
    # ========================================================

    def make_room_view(self, perspective=1):

        frame = RoundedRectangle(
            width=4.55,
            height=2.65,
            corner_radius=0.10,
            stroke_color="#313848",
            stroke_width=1.0,
            fill_color="#10141C",
            fill_opacity=1,
        )

        # Same room, slightly different vanishing point.
        vp_x = 0.45 * perspective

        floor = Polygon(
            [-2.15, -1.15, 0],
            [2.15, -1.15, 0],
            [0.80 + vp_x, 0.15, 0],
            [-0.85 + vp_x, 0.15, 0],
            fill_color="#1A202C",
            fill_opacity=1,
            stroke_width=0,
        )

        horizon = Line(
            [-2.1, 0.15, 0],
            [2.1, 0.15, 0],
            color="#303746",
            stroke_width=0.8,
        )

        perspective_lines = VGroup()

        for x in np.linspace(
            -2.0,
            2.0,
            8,
        ):
            perspective_lines.add(
                Line(
                    [x, -1.10, 0],
                    [vp_x, 0.15, 0],
                    color="#282F3D",
                    stroke_width=0.6,
                    stroke_opacity=0.65,
                )
            )

        sofa = RoundedRectangle(
            width=1.35,
            height=0.46,
            corner_radius=0.08,
            stroke_width=0,
            fill_color="#58647C",
            fill_opacity=0.72,
        )

        sofa.move_to(
            [
                -0.60
                + 0.20 * perspective,
                -0.34,
                0,
            ]
        )

        sofa_back = RoundedRectangle(
            width=1.25,
            height=0.38,
            corner_radius=0.06,
            stroke_width=0,
            fill_color="#69768E",
            fill_opacity=0.48,
        )

        sofa_back.next_to(
            sofa,
            UP,
            buff=-0.05,
        )

        table = Polygon(
            [-0.25, -0.15, 0],
            [0.60, -0.15, 0],
            [0.72, -0.43, 0],
            [-0.34, -0.43, 0],
            fill_color="#736D83",
            fill_opacity=0.66,
            stroke_width=0,
        )

        table.shift(
            RIGHT * (
                0.65
                + 0.1 * perspective
            )
            + DOWN * 0.38
        )

        window = Rectangle(
            width=0.82,
            height=0.70,
            stroke_color=CYAN,
            stroke_width=0.8,
            stroke_opacity=0.38,
            fill_color=CYAN,
            fill_opacity=0.025,
        )

        window.move_to(
            [
                1.15
                - 0.15 * perspective,
                0.65,
                0,
            ]
        )

        content = VGroup(
            floor,
            horizon,
            perspective_lines,
            sofa,
            sofa_back,
            table,
            window,
        )

        return VGroup(
            frame,
            content,
        )

    def make_pixel_grid(self):

        grid = VGroup()

        rows = 9
        cols = 15

        size = 0.29

        rng = np.random.default_rng(
            21
        )

        for row in range(rows):
            for col in range(cols):

                t = (
                    col / max(
                        cols - 1,
                        1,
                    )
                )

                base = interpolate_color(
                    ManimColor(BLUE),
                    ManimColor(VIOLET),
                    t,
                )

                brightness = rng.uniform(
                    0.35,
                    0.85,
                )

                square = Square(
                    side_length=size,
                    stroke_color="#343A49",
                    stroke_width=0.35,
                    fill_color=base,
                    fill_opacity=brightness,
                )

                square.move_to(
                    [
                        (
                            col
                            - (cols - 1) / 2
                        ) * size,
                        (
                            (rows - 1) / 2
                            - row
                        ) * size,
                        0,
                    ]
                )

                grid.add(
                    square
                )

        return grid

    def make_focus_marker(
        self,
        point,
        color,
        width=0.75,
        height=0.55,
    ):

        marker = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.04,
            color=color,
            stroke_width=1.2,
        )

        marker.move_to(
            point
        )

        halo = marker.copy()

        halo.scale(
            1.10
        )

        halo.set_stroke(
            opacity=0.12,
            width=4,
        )

        return VGroup(
            halo,
            marker,
        )

    def make_camera_pose(
        self,
        center,
        angle=0,
        color=CYAN,
        opacity=1.0,
    ):

        optical_center = Dot(
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
                optical_center.get_center(),
                plane.get_left(),
                color=color,
                stroke_width=1,
            ),
            Line(
                optical_center.get_center(),
                plane.get_right(),
                color=color,
                stroke_width=1,
            ),
            plane,
            optical_center,
        )

        frustum.rotate(
            angle
        )

        frustum.move_to(
            center
        )

        frustum.set_opacity(
            opacity
        )

        return frustum

    def make_room_point_cloud(
        self,
        scale=1.0,
    ):

        rng = np.random.default_rng(
            4
        )

        cloud = VGroup()

        # Back wall
        for _ in range(45):
            x = rng.uniform(
                -1.35,
                1.35,
            )

            y = rng.uniform(
                -0.85,
                0.85,
            )

            cloud.add(
                Dot(
                    [
                        x,
                        y,
                        0,
                    ],
                    radius=0.018,
                    color=VIOLET,
                )
            )

        # Sofa/front geometry
        for _ in range(36):
            x = rng.uniform(
                -0.95,
                0.25,
            )

            y = rng.uniform(
                -0.62,
                -0.18,
            )

            cloud.add(
                Dot(
                    [
                        x * 1.07,
                        y * 1.12,
                        0,
                    ],
                    radius=0.023,
                    color=CYAN,
                )
            )

        # Floor
        for _ in range(42):
            x = rng.uniform(
                -1.35,
                1.35,
            )

            y = rng.uniform(
                -0.95,
                -0.60,
            )

            cloud.add(
                Dot(
                    [
                        x,
                        y,
                        0,
                    ],
                    radius=0.015,
                    color=BLUE,
                )
            )

        cloud.scale(
            scale
        )

        return cloud

    def make_room_wireframe(
        self,
        scale=1.0,
    ):

        lines = VGroup(
            Line(
                [-1.4, -0.9, 0],
                [1.4, -0.9, 0],
            ),
            Line(
                [1.4, -0.9, 0],
                [1.4, 0.9, 0],
            ),
            Line(
                [1.4, 0.9, 0],
                [-1.4, 0.9, 0],
            ),
            Line(
                [-1.4, 0.9, 0],
                [-1.4, -0.9, 0],
            ),
        )

        lines.set_stroke(
            color=VIOLET,
            width=0.8,
            opacity=0.28,
        )

        lines.scale(
            scale
        )

        return lines