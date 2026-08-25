from manim import *
import numpy as np

from theme import *


class Scene11GlobalAlignment(Scene):
    """
    Audio: Đoạn 11.wav
    Duration: 43.42s

    00:00.00-00:05.07
    "Với hai ảnh, mọi thứ khá gọn."

    00:06.11-00:08.54
    "Nhưng một scene thực tế có thể có hàng chục ảnh."

    00:09.05-00:16.78
    "DUSt3R vẫn xử lý các cặp ảnh, nên mỗi pair ban đầu
    có một reconstruction cục bộ."

    00:17.83-00:23.53
    "Để dựng cả scene, các reconstruction đó phải được đưa
    vào một world coordinate frame chung."

    00:24.45-00:32.19
    "DUSt3R xây một graph: mỗi image là một node,
    các pair liên quan tạo thành edge."

    00:33.24-00:38.12
    "Sau đó global alignment tìm pose và scale cho các pair
    sao cho tất cả pointmaps cùng đồng ý về một geometry toàn cục."

    00:38.79-00:43.42
    "Thay vì chỉ nhìn lỗi sau khi project lại về ảnh 2D như
    Bundle Adjustment truyền thống, pointmaps cho phép alignment
    được thực hiện trực tiếp trong 3D."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.sentence_1()
        self.wait_until(6.11)

        self.sentence_2()
        self.wait_until(9.05)

        self.sentence_3()
        self.wait_until(17.83)

        self.sentence_4()
        self.wait_until(24.45)

        self.sentence_5()
        self.wait_until(33.24)

        self.sentence_6()
        self.wait_until(38.79)

        self.sentence_7()
        self.wait_until(43.42)

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
    # 00:00 - 00:05.07
    #
    # "Với hai ảnh, mọi thứ khá gọn."
    # =========================================================

    def sentence_1(self):

        image_1 = self.make_image(
            LEFT * 2.8 + UP * 1.45,
            CYAN,
            0,
        )

        image_2 = self.make_image(
            RIGHT * 2.8 + UP * 1.45,
            VIOLET,
            1,
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
            run_time=0.65,
        )

        pair_line = Line(
            image_1.get_right(),
            image_2.get_left(),
            color=WHITE,
            stroke_width=1,
            stroke_opacity=0.22,
        )

        self.play_timed(
            Create(
                pair_line
            ),
            run_time=0.45,
        )

        cloud = self.make_cloud(
            center=DOWN * 1.15,
            color_a=CYAN,
            color_b=VIOLET,
            seed=1,
        )

        arrow_1 = Line(
            image_1.get_bottom(),
            cloud.get_top(),
            color=CYAN,
            stroke_width=1,
            stroke_opacity=0.20,
        )

        arrow_2 = Line(
            image_2.get_bottom(),
            cloud.get_top(),
            color=VIOLET,
            stroke_width=1,
            stroke_opacity=0.20,
        )

        self.play_timed(
            Create(arrow_1),
            Create(arrow_2),
            FadeIn(
                cloud,
                shift=DOWN * 0.10,
            ),
            run_time=0.85,
        )

        pulse = pair_line.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=2.8,
            opacity=0.80,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.22,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.65)

        self.image_1 = image_1
        self.image_2 = image_2

        self.pair_line = pair_line
        self.pair_cloud = cloud

        self.pair_arrows = VGroup(
            arrow_1,
            arrow_2,
        )

    # =========================================================
    # 00:06.11 - 00:08.54
    #
    # "scene thực tế có thể có hàng chục ảnh."
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            FadeOut(
                self.pair_cloud
            ),
            FadeOut(
                self.pair_arrows
            ),
            FadeOut(
                self.pair_line
            ),

            self.image_1.animate
            .scale(0.65)
            .move_to(LEFT * 5.25 + UP * 0.5),

            self.image_2.animate
            .scale(0.65)
            .move_to(LEFT * 3.7 + UP * 0.5),

            run_time=0.45,
        )

        images = VGroup(
            self.image_1,
            self.image_2,
        )

        positions = [
            LEFT * 2.15 + UP * 0.5,
            LEFT * 0.6 + UP * 0.5,
            RIGHT * 0.95 + UP * 0.5,
            RIGHT * 2.5 + UP * 0.5,
            RIGHT * 4.05 + UP * 0.5,
            RIGHT * 5.6 + UP * 0.5,
        ]

        colors = [
            CYAN,
            CYAN_SOFT,
            BLUE,
            VIOLET,
            MAGENTA,
            VIOLET,
        ]

        for i, (pos, color) in enumerate(
            zip(
                positions,
                colors,
            )
        ):

            image = self.make_image(
                pos,
                color,
                i + 2,
            )

            image.scale(
                0.65
            )

            images.add(
                image
            )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        im,
                        shift=RIGHT * 0.08,
                    )
                    for im in images[2:]
                ],
                lag_ratio=0.08,
            ),
            run_time=0.75,
        )

        self.play_timed(
            images.animate.set_opacity(
                0.80
            ),
            run_time=0.30,
        )

        self.wait_timed(0.40)

        self.images = images

    # =========================================================
    # 00:09.05 - 00:16.78
    #
    # "DUSt3R vẫn xử lý các cặp ảnh..."
    # =========================================================

    def sentence_3(self):

        self.play_timed(
            self.images.animate
            .scale(0.82)
            .shift(UP * 1.25),
            run_time=0.50,
        )

        # Highlight pairs:
        #
        # I1-I2
        # I2-I3
        # I3-I4
        pair_indices = [
            (0, 1),
            (1, 2),
            (2, 3),
        ]

        pair_lines = VGroup()

        for a, b in pair_indices:

            line = Line(
                self.images[a].get_center(),
                self.images[b].get_center(),
                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.28,
            )

            pair_lines.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(
                        line
                    )
                    for line in pair_lines
                ],
                lag_ratio=0.15,
            ),
            run_time=0.75,
        )

        # Local reconstructions.
        cloud_12 = self.make_cloud(
            LEFT * 3.6 + DOWN * 1.05,
            CYAN,
            BLUE,
            seed=4,
        )

        cloud_23 = self.make_cloud(
            DOWN * 1.15,
            BLUE,
            VIOLET,
            seed=4,
        )

        cloud_34 = self.make_cloud(
            RIGHT * 3.6 + DOWN * 1.05,
            VIOLET,
            MAGENTA,
            seed=4,
        )

        # Deliberately make local frames inconsistent.
        cloud_12.rotate(
            -14 * DEGREES
        )

        cloud_12.scale(
            0.85
        )

        cloud_23.rotate(
            9 * DEGREES
        )

        cloud_23.scale(
            1.05
        )

        cloud_34.rotate(
            24 * DEGREES
        )

        cloud_34.scale(
            1.22
        )

        clouds = VGroup(
            cloud_12,
            cloud_23,
            cloud_34,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        cloud,
                        scale=0.85,
                    )
                    for cloud in clouds
                ],
                lag_ratio=0.16,
            ),
            run_time=1.00,
        )

        # Local coordinate frames.
        frame_12 = self.make_coordinate_frame(
            cloud_12.get_center()
            + LEFT * 1.05
            + DOWN * 0.8,

            CYAN,
            scale=0.65,
        )

        frame_23 = self.make_coordinate_frame(
            cloud_23.get_center()
            + LEFT * 1.05
            + DOWN * 0.8,

            BLUE,
            scale=0.65,
        )

        frame_34 = self.make_coordinate_frame(
            cloud_34.get_center()
            + LEFT * 1.05
            + DOWN * 0.8,

            VIOLET,
            scale=0.65,
        )

        frames = VGroup(
            frame_12,
            frame_23,
            frame_34,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(frame)
                    for frame in frames
                ],
                lag_ratio=0.12,
            ),
            run_time=0.65,
        )

        # Pulse each local reconstruction.
        for cloud in clouds:

            pulse = cloud[0].copy()

            pulse.set_stroke(
                WHITE,
                width=2,
                opacity=0.45,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.20,
                ),
                run_time=0.35,
            )

        self.wait_timed(0.55)

        self.pair_lines = pair_lines

        self.cloud_12 = cloud_12
        self.cloud_23 = cloud_23
        self.cloud_34 = cloud_34

        self.local_clouds = clouds
        self.local_frames = frames

    # =========================================================
    # 00:17.83 - 00:23.53
    #
    # "đưa vào một world coordinate frame chung."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            self.images.animate.set_opacity(
                0.15
            ),
            self.pair_lines.animate.set_opacity(
                0.08
            ),
            run_time=0.35,
        )

        world_origin = (
            LEFT * 5.3
            + DOWN * 2.15
        )

        world_frame = self.make_coordinate_frame(
            world_origin,
            WHITE,
            scale=1.20,
        )

        self.play_timed(
            FadeIn(
                world_frame,
                scale=0.85,
            ),
            run_time=0.50,
        )

        # Shared spatial field.
        field = RoundedRectangle(
            width=10.0,
            height=3.5,
            corner_radius=0.18,
            stroke_color=WHITE,
            stroke_width=1,
            stroke_opacity=0.10,
            fill_color=WHITE,
            fill_opacity=0.008,
        )

        field.move_to(
            DOWN * 0.70
        )

        self.play_timed(
            FadeIn(
                field
            ),
            run_time=0.40,
        )

        # Links from local clouds toward one common origin.
        global_links = VGroup()

        for cloud in self.local_clouds:

            line = Line(
                world_origin,
                cloud.get_center(),
                color=MUTED,
                stroke_width=1,
                stroke_opacity=0.18,
            )

            global_links.add(
                line
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in global_links
                ],
                lag_ratio=0.12,
            ),
            run_time=0.70,
        )

        # Local frames become secondary.
        self.play_timed(
            self.local_frames.animate.set_opacity(
                0.16
            ),
            world_frame.animate.scale(
                1.06
            ),
            run_time=0.45,
        )

        # Signal flows from global frame to all reconstructions.
        for line in global_links:

            pulse = line.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.4,
                opacity=0.70,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.22,
                ),
                run_time=0.35,
            )

        self.wait_timed(0.45)

        self.world_frame = world_frame
        self.world_field = field
        self.global_links = global_links

    # =========================================================
    # 00:24.45 - 00:32.19
    #
    # "DUSt3R xây một graph..."
    # =========================================================

    def sentence_5(self):

        self.play_timed(
            FadeOut(
                self.local_clouds
            ),
            FadeOut(
                self.local_frames
            ),
            FadeOut(
                self.world_frame
            ),
            FadeOut(
                self.world_field
            ),
            FadeOut(
                self.global_links
            ),
            FadeOut(
                self.pair_lines
            ),
            run_time=0.45,
        )

        # Bring images to graph layout.
        graph_positions = [
            LEFT * 4.8,
            LEFT * 3.2 + UP * 1.4,
            LEFT * 1.2 + UP * 0.3,
            RIGHT * 0.8 + UP * 1.45,
            RIGHT * 2.8,
            RIGHT * 4.6 + UP * 1.1,
            LEFT * 0.2 + DOWN * 1.45,
            RIGHT * 2.0 + DOWN * 1.65,
        ]

        nodes = VGroup()

        for i, image in enumerate(
            self.images
        ):

            image.generate_target()

            image.target.scale(
                0.56
            )

            image.target.move_to(
                graph_positions[i]
            )

            image.target.set_opacity(
                0.80
            )

        self.play_timed(
            *[
                MoveToTarget(
                    im
                )
                for im in self.images
            ],
            run_time=0.85,
        )

        for image in self.images:

            node = Circle(
                radius=0.16,
                stroke_color=CYAN,
                stroke_width=1.2,
                stroke_opacity=0.45,
                fill_color=BG,
                fill_opacity=0.7,
            )

            node.move_to(
                image.get_center()
            )

            nodes.add(
                node
            )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        node,
                        scale=0.75,
                    )
                    for node in nodes
                ],
                lag_ratio=0.05,
            ),
            run_time=0.55,
        )

        # Graph edges.
        graph_pairs = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (2, 6),
            (6, 7),
            (7, 4),
            (1, 6),
        ]

        edges = VGroup()

        for a, b in graph_pairs:

            edge = Line(
                nodes[a].get_center(),
                nodes[b].get_center(),
                color=MUTED,
                stroke_width=1,
                stroke_opacity=0.24,
            )

            edge.set_z_index(
                -1
            )

            edges.add(
                edge
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(edge)
                    for edge in edges
                ],
                lag_ratio=0.08,
            ),
            run_time=1.10,
        )

        # Graph information propagates.
        for edge in edges[:5]:

            pulse = edge.copy()

            pulse.set_stroke(
                CYAN_SOFT,
                width=2.7,
                opacity=0.80,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.20,
                ),
                run_time=0.30,
            )

        self.play_timed(
            nodes.animate.set_stroke(
                color=VIOLET,
                opacity=0.65,
            ),
            run_time=0.40,
        )

        self.wait_timed(0.45)

        self.graph_nodes = nodes
        self.graph_edges = edges

    # =========================================================
    # 00:33.24 - 00:38.12
    #
    # "global alignment tìm pose và scale..."
    # =========================================================

    def sentence_6(self):

        self.play_timed(
            FadeOut(
                self.images
            ),
            FadeOut(
                self.graph_nodes
            ),
            FadeOut(
                self.graph_edges
            ),
            run_time=0.40,
        )

        # Three copies of same latent scene.
        cloud_a = self.make_cloud(
            LEFT * 3.5,
            CYAN,
            BLUE,
            seed=9,
        )

        cloud_b = self.make_cloud(
            ORIGIN + UP * 1.0,
            BLUE,
            VIOLET,
            seed=9,
        )

        cloud_c = self.make_cloud(
            RIGHT * 3.5 + DOWN * 0.5,
            VIOLET,
            MAGENTA,
            seed=9,
        )

        cloud_a.rotate(
            -18 * DEGREES
        )
        cloud_a.scale(
            0.78
        )

        cloud_b.rotate(
            12 * DEGREES
        )
        cloud_b.scale(
            1.12
        )

        cloud_c.rotate(
            27 * DEGREES
        )
        cloud_c.scale(
            1.32
        )

        clouds = VGroup(
            cloud_a,
            cloud_b,
            cloud_c,
        )

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        cloud,
                        scale=0.9,
                    )
                    for cloud in clouds
                ],
                lag_ratio=0.12,
            ),
            run_time=0.70,
        )

        # All converge into one global geometry.
        target = DOWN * 0.15

        self.play_timed(
            cloud_a.animate
            .rotate(18 * DEGREES)
            .scale(1 / 0.78)
            .move_to(target),

            cloud_b.animate
            .rotate(-12 * DEGREES)
            .scale(1 / 1.12)
            .move_to(target),

            cloud_c.animate
            .rotate(-27 * DEGREES)
            .scale(1 / 1.32)
            .move_to(target),

            run_time=1.55,
            rate_func=smooth,
        )

        self.play_timed(
            cloud_a.animate.set_opacity(
                0.55
            ),
            cloud_b.animate.set_opacity(
                0.55
            ),
            cloud_c.animate.set_opacity(
                0.55
            ),
            run_time=0.35,
        )

        global_ring = Circle(
            radius=1.65,
            color=WHITE,
            stroke_width=1,
            stroke_opacity=0.18,
        )

        global_ring.move_to(
            target
        )

        self.play_timed(
            FadeIn(
                global_ring,
                scale=0.75,
            ),
            run_time=0.35,
        )

        self.play_timed(
            global_ring.animate
            .scale(1.22)
            .set_opacity(0),
            run_time=0.40,
        )

        self.wait_timed(0.35)

        self.aligned_clouds = clouds

    # =========================================================
    # 00:38.79 - 00:43.42
    #
    # "...alignment được thực hiện trực tiếp trong 3D."
    # =========================================================

    def sentence_7(self):

        # Briefly show image plane / reprojection idea.
        image_plane = Rectangle(
            width=3.5,
            height=2.15,
            stroke_color=MUTED,
            stroke_width=1,
            stroke_opacity=0.28,
            fill_color=SURFACE,
            fill_opacity=0.10,
        )

        image_plane.move_to(
            LEFT * 3.7
        )

        self.play_timed(
            self.aligned_clouds.animate
            .scale(0.72)
            .move_to(RIGHT * 2.8),

            FadeIn(
                image_plane
            ),

            run_time=0.50,
        )

        # Projection rays from 3D back to 2D.
        rays = VGroup()

        points = self.aligned_clouds[0][1]

        for point in points[::5]:

            target = (
                image_plane.get_center()
                + LEFT * 0.6
                + UP * (
                    0.15
                    * np.sin(
                        point.get_center()[1]
                    )
                )
            )

            ray = Line(
                point.get_center(),
                target,
                color=MUTED,
                stroke_width=0.7,
                stroke_opacity=0.14,
            )

            rays.add(
                ray
            )

        self.play_timed(
            LaggedStart(
                *[
                    Create(ray)
                    for ray in rays
                ],
                lag_ratio=0.08,
            ),
            run_time=0.65,
        )

        # 2D reprojection fades out.
        self.play_timed(
            image_plane.animate.set_opacity(
                0.08
            ),
            rays.animate.set_opacity(
                0.04
            ),
            self.aligned_clouds.animate
            .scale(1.18)
            .move_to(ORIGIN),
            run_time=0.65,
        )

        # Explicit 3D-space alignment signal.
        frame = self.make_coordinate_frame(
            LEFT * 4.5 + DOWN * 2.0,
            WHITE,
            scale=1.15,
        )

        self.play_timed(
            FadeIn(
                frame
            ),
            run_time=0.35,
        )

        direct_links = VGroup()

        clouds = list(
            self.aligned_clouds
        )

        for i in range(
            len(clouds) - 1
        ):

            link = Line(
                clouds[i].get_center()
                + UP * 0.2
                + LEFT * 0.15 * i,

                clouds[i + 1].get_center()
                + DOWN * 0.2
                + RIGHT * 0.15 * i,

                color=WHITE,
                stroke_width=1,
                stroke_opacity=0.18,
            )

            direct_links.add(
                link
            )

        self.play_timed(
            Create(
                direct_links
            ),
            run_time=0.40,
        )

        pulse = Circle(
            radius=1.2,
            color=CYAN_SOFT,
            stroke_width=2,
            stroke_opacity=0.35,
        )

        pulse.move_to(
            ORIGIN
        )

        self.play_timed(
            FadeIn(
                pulse,
                scale=0.75,
            ),
            run_time=0.30,
        )

        self.play_timed(
            pulse.animate
            .scale(1.45)
            .set_opacity(0),
            run_time=0.40,
        )

        self.wait_timed(0.40)

    # =========================================================
    # HELPERS
    # =========================================================

    def make_image(
        self,
        center,
        accent,
        variant=0,
    ):

        frame = RoundedRectangle(
            width=2.35,
            height=1.48,
            corner_radius=0.08,
            stroke_color=accent,
            stroke_width=1,
            stroke_opacity=0.35,
            fill_color=SURFACE,
            fill_opacity=0.95,
        )

        floor = Polygon(
            [-1.05, -0.58, 0],
            [1.05, -0.58, 0],
            [0.42, 0.04, 0],
            [-0.42, 0.04, 0],
            fill_color="#1A202C",
            fill_opacity=1,
            stroke_width=0,
        )

        sofa = RoundedRectangle(
            width=0.70,
            height=0.28,
            corner_radius=0.04,
            stroke_width=0,
            fill_color="#566177",
            fill_opacity=0.72,
        )

        sofa.move_to(
            LEFT * (
                0.25
                - 0.03 * variant
            )
            + DOWN * 0.20
        )

        window = Rectangle(
            width=0.40,
            height=0.38,
            stroke_color=accent,
            stroke_width=0.7,
            stroke_opacity=0.35,
            fill_color=accent,
            fill_opacity=0.025,
        )

        window.move_to(
            RIGHT * 0.58
            + UP * 0.30
        )

        group = VGroup(
            frame,
            floor,
            sofa,
            window,
        )

        group.move_to(
            center
        )

        return group

    def make_cloud(
        self,
        center,
        color_a,
        color_b,
        seed=1,
    ):

        rng = np.random.default_rng(
            seed
        )

        rows = 4
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
                ) * 2.2

                y = (
                    0.5 - v
                ) * 1.30

                depth = (
                    0.28
                    + 0.35
                    * np.sin(
                        np.pi * u
                    )
                    * np.cos(
                        np.pi * v
                    )
                    + rng.uniform(
                        -0.015,
                        0.015,
                    )
                )

                p = np.array([
                    center[0]
                    + x
                    + depth * 0.42,

                    center[1]
                    + y
                    + depth * 0.22,

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
                        radius=0.027,
                        color=color,
                    )
                )

            positions.append(
                current
            )

        # Horizontal
        for row in range(rows):

            for col in range(
                cols - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row][col + 1],
                        color=color_a,
                        stroke_width=0.6,
                        stroke_opacity=0.20,
                    )
                )

        # Vertical
        for col in range(cols):

            for row in range(
                rows - 1
            ):

                mesh.add(
                    Line(
                        positions[row][col],
                        positions[row + 1][col],
                        color=color_b,
                        stroke_width=0.6,
                        stroke_opacity=0.18,
                    )
                )

        return VGroup(
            mesh,
            points,
        )

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
            stroke_width=1.2,
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
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )

        z_axis = Arrow(
            origin,
            origin
            + LEFT
            * 0.32
            * scale
            + DOWN
            * 0.28
            * scale,
            buff=0,
            color=MAGENTA,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )

        origin_dot = Dot(
            origin,
            radius=0.035,
            color=color,
        )

        return VGroup(
            x_axis,
            y_axis,
            z_axis,
            origin_dot,
        )