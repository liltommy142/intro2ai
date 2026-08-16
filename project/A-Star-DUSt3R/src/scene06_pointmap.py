from manim import *
import numpy as np

from theme import *


class Scene06Pointmap(Scene):
    """
    00:00-00:05
    "DUSt3R dùng một representation gọi là pointmap."

    00:05-00:10
    "Ảnh có kích thước W × H.
    Một pointmap cũng có cùng lưới đó."

    00:11-00:17
    "Nhưng thay vì mỗi pixel chỉ mang thông tin màu,
    mỗi pixel được gắn với một tọa độ 3D: X, Y, Z."

    00:19-00:23
    "Nói cách khác:
    pixel này tương ứng với điểm này trong không gian."

    00:23-00:26
    "Pixel bên cạnh tương ứng với điểm bên cạnh."

    00:26-00:33
    "Và nếu làm điều đó cho toàn bộ ảnh,
    mặt phẳng 2D bắt đầu bung ra thành một bề mặt 3D."

    00:34-00:42
    "Điểm đẹp của pointmap là nó vẫn giữ quan hệ trực tiếp
    với pixel gốc, nhưng đồng thời đã sống trong không gian 3D."

    00:43-00:47
    "Nó nối image space và 3D space
    trong cùng một representation."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_scene()

        self.sentence_1()
        self.wait_until(5.0)

        self.sentence_2()
        self.wait_until(11.0)

        self.sentence_3()
        self.wait_until(19.0)

        self.sentence_4()
        self.wait_until(23.0)

        self.sentence_5()
        self.wait_until(26.0)

        self.sentence_6()
        self.wait_until(34.0)

        self.sentence_7()
        self.wait_until(43.0)

        self.sentence_8()
        self.wait_until(47.0)

    # =========================================================
    # TIMELINE
    # =========================================================

    def play_timed(
        self,
        *animations,
        run_time=1.0,
        **kwargs,
    ):
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
        self.cols = 10
        self.rows = 6

        self.grid_width = 6.2
        self.grid_height = 3.72

        self.cell_w = self.grid_width / self.cols
        self.cell_h = self.grid_height / self.rows

        self.grid_center = np.array([
            0.0,
            -0.20,
            0.0,
        ])

        self.image_pixels = self.make_image_grid(
            self.grid_center
        )

        self.grid_outline = RoundedRectangle(
            width=self.grid_width + 0.12,
            height=self.grid_height + 0.12,
            corner_radius=0.07,
            stroke_color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.32,
        )

        self.grid_outline.move_to(
            self.grid_center
        )

    # =========================================================
    # 00:00 -> 00:05
    #
    # "DUSt3R dùng một representation gọi là pointmap."
    # =========================================================

    def sentence_1(self):

        # Start from a clean image-like pixel grid.
        self.play_timed(
            FadeIn(
                self.image_pixels,
                scale=0.98,
            ),
            FadeIn(
                self.grid_outline,
            ),
            run_time=0.85,
        )

        # One wave passes through the grid.
        wave = self.grid_outline.copy()

        wave.set_stroke(
            CYAN_SOFT,
            width=2.5,
            opacity=0.65,
        )

        self.play_timed(
            ShowPassingFlash(
                wave,
                time_width=0.20,
            ),
            run_time=0.75,
        )

        pointmap_label = Text(
            "POINTMAP",
            font_size=28,
            color=WHITE,
        )

        pointmap_label.to_edge(
            UP,
            buff=0.48,
        )

        underline = Line(
            pointmap_label.get_left(),
            pointmap_label.get_right(),
            color=VIOLET,
            stroke_width=1.4,
            stroke_opacity=0.60,
        )

        underline.next_to(
            pointmap_label,
            DOWN,
            buff=0.12,
        )

        self.play_timed(
            FadeIn(
                pointmap_label,
                shift=UP * 0.08,
            ),
            Create(
                underline
            ),
            run_time=0.65,
        )

        # Grid remains the central object.
        self.play_timed(
            self.image_pixels.animate.set_opacity(
                0.92
            ),
            run_time=0.35,
        )

        self.wait_timed(0.55)

        self.pointmap_label = pointmap_label
        self.pointmap_underline = underline

    # =========================================================
    # 00:05 -> 00:10
    #
    # "Ảnh có kích thước W × H.
    # Một pointmap cũng có cùng lưới đó."
    # =========================================================

    def sentence_2(self):

        wh = MathTex(
            r"W \times H",
            font_size=34,
            color=WHITE,
        )

        wh.next_to(
            self.grid_outline,
            LEFT,
            buff=0.42,
        )

        self.play_timed(
            FadeIn(
                wh,
                shift=RIGHT * 0.08,
            ),
            run_time=0.45,
        )

        # Dimension guides.
        width_line = Line(
            self.grid_outline.get_corner(DL)
            + DOWN * 0.22,
            self.grid_outline.get_corner(DR)
            + DOWN * 0.22,
            color=MUTED,
            stroke_width=1.0,
            stroke_opacity=0.45,
        )

        height_line = Line(
            self.grid_outline.get_corner(DL)
            + LEFT * 0.22,
            self.grid_outline.get_corner(UL)
            + LEFT * 0.22,
            color=MUTED,
            stroke_width=1.0,
            stroke_opacity=0.45,
        )

        w_label = MathTex(
            r"W",
            font_size=24,
            color=MUTED,
        ).next_to(
            width_line,
            DOWN,
            buff=0.09,
        )

        h_label = MathTex(
            r"H",
            font_size=24,
            color=MUTED,
        ).next_to(
            height_line,
            LEFT,
            buff=0.09,
        )

        self.play_timed(
            Create(width_line),
            Create(height_line),
            FadeIn(w_label),
            FadeIn(h_label),
            run_time=0.65,
        )

        # Clone grid briefly:
        # image grid == pointmap grid topology.
        grid_copy = self.image_pixels.copy()

        self.add(
            grid_copy
        )

        self.play_timed(
            grid_copy.animate
            .scale(0.58)
            .move_to(RIGHT * 4.7 + DOWN * 0.15)
            .set_opacity(0.40),

            self.image_pixels.animate
            .scale(0.58)
            .move_to(LEFT * 4.7 + DOWN * 0.15)
            .set_opacity(0.40),

            self.grid_outline.animate.set_opacity(
                0.10
            ),

            run_time=0.85,
        )

        same_grid = VGroup(
            MathTex(
                r"W \times H",
                font_size=25,
                color=CYAN,
            ),
            Arrow(
                LEFT * 0.55,
                RIGHT * 0.55,
                buff=0,
                stroke_width=1.2,
                color=MUTED,
            ),
            MathTex(
                r"W \times H",
                font_size=25,
                color=VIOLET,
            ),
        ).arrange(
            RIGHT,
            buff=0.26,
        )

        same_grid.move_to(
            ORIGIN + DOWN * 0.15
        )

        self.play_timed(
            FadeIn(
                same_grid
            ),
            run_time=0.55,
        )

        # Return to one unified grid.
        self.play_timed(
            FadeOut(
                same_grid
            ),
            FadeOut(
                grid_copy
            ),
            FadeOut(
                wh
            ),
            FadeOut(
                width_line
            ),
            FadeOut(
                height_line
            ),
            FadeOut(
                w_label
            ),
            FadeOut(
                h_label
            ),

            self.image_pixels.animate
            .scale(1 / 0.58)
            .move_to(self.grid_center)
            .set_opacity(0.92),

            self.grid_outline.animate.set_opacity(
                0.32
            ),

            run_time=0.80,
        )

    # =========================================================
    # 00:11 -> 00:17
    #
    # "Nhưng thay vì mỗi pixel chỉ mang thông tin màu,
    # mỗi pixel được gắn với một tọa độ 3D: X, Y, Z."
    # =========================================================

    def sentence_3(self):

        row = 2
        col = 5

        index = (
            row * self.cols
            + col
        )

        selected = self.image_pixels[index]

        # Dim other pixels.
        others = VGroup(
            *[
                p
                for i, p
                in enumerate(self.image_pixels)
                if i != index
            ]
        )

        self.play_timed(
            others.animate.set_opacity(
                0.16
            ),
            selected.animate.scale(
                1.28
            ),
            run_time=0.55,
        )

        # Current pixel contains color.
        rgb = MathTex(
            r"(r,g,b)",
            font_size=28,
            color=CYAN_SOFT,
        )

        rgb.next_to(
            selected,
            RIGHT,
            buff=0.35,
        )

        connector = Line(
            selected.get_right(),
            rgb.get_left(),
            color=CYAN,
            stroke_width=1.0,
            stroke_opacity=0.35,
        )

        self.play_timed(
            Create(
                connector
            ),
            FadeIn(
                rgb,
                shift=RIGHT * 0.08,
            ),
            run_time=0.55,
        )

        # RGB transitions into XYZ.
        xyz = MathTex(
            r"(X,Y,Z)",
            font_size=31,
            color=VIOLET,
        )

        xyz.move_to(
            rgb
        )

        self.play_timed(
            Transform(
                rgb,
                xyz,
            ),
            connector.animate.set_color(
                VIOLET
            ),
            run_time=0.75,
        )

        # A tiny coordinate basis grows next to it.
        basis_origin = (
            xyz.get_right()
            + RIGHT * 0.42
        )

        x_axis = Arrow(
            basis_origin,
            basis_origin + RIGHT * 0.55,
            buff=0,
            color=CYAN,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )

        y_axis = Arrow(
            basis_origin,
            basis_origin + UP * 0.55,
            buff=0,
            color=VIOLET,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )

        z_axis = Arrow(
            basis_origin,
            basis_origin + LEFT * 0.30 + DOWN * 0.32,
            buff=0,
            color=MAGENTA,
            stroke_width=1.2,
            max_tip_length_to_length_ratio=0.18,
        )

        self.play_timed(
            GrowArrow(x_axis),
            GrowArrow(y_axis),
            GrowArrow(z_axis),
            run_time=0.65,
        )

        # Pulse pixel -> XYZ
        pulse = connector.copy()

        pulse.set_stroke(
            VIOLET,
            width=3,
            opacity=0.85,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.55,
        )

        self.wait_timed(0.60)

        self.selected_index = index
        self.selected_pixel = selected
        self.other_pixels = others

        self.xyz_label = rgb
        self.xyz_connector = connector

        self.xyz_basis = VGroup(
            x_axis,
            y_axis,
            z_axis,
        )

    # =========================================================
    # 00:19 -> 00:23
    #
    # "pixel này tương ứng với điểm này trong không gian."
    # =========================================================

    def sentence_4(self):

        self.play_timed(
            FadeOut(
                self.xyz_basis
            ),
            self.xyz_label.animate.set_opacity(
                0.45
            ),
            run_time=0.35,
        )

        source = self.selected_pixel.get_center()

        destination = self.project_pixel_to_3d(
            row=2,
            col=5,
        )

        path = CubicBezier(
            source,
            source + RIGHT * 1.0,
            destination + LEFT * 1.0 + DOWN * 0.25,
            destination,
        )

        point = self.make_world_point(
            source,
            VIOLET,
            radius=0.065,
        )

        self.add(
            point
        )

        self.play_timed(
            MoveAlongPath(
                point,
                path,
            ),
            self.selected_pixel.animate.set_opacity(
                0.32
            ),
            run_time=0.90,
        )

        mapping_line = Line(
            source,
            destination,
            color=VIOLET,
            stroke_width=1.2,
            stroke_opacity=0.32,
        )

        self.play_timed(
            Create(
                mapping_line
            ),
            run_time=0.45,
        )

        self.play_timed(
            Indicate(
                point[-1],
                color=VIOLET,
                scale_factor=1.55,
            ),
            run_time=0.50,
        )

        self.wait_timed(0.35)

        self.first_3d_point = point
        self.first_mapping_line = mapping_line

    # =========================================================
    # 00:23 -> 00:26
    #
    # "Pixel bên cạnh tương ứng với điểm bên cạnh."
    # =========================================================

    def sentence_5(self):

        row = 2
        col = 6

        index = (
            row * self.cols
            + col
        )

        neighbour_pixel = self.image_pixels[index]

        self.play_timed(
            neighbour_pixel.animate
            .set_opacity(1)
            .scale(1.18),
            run_time=0.40,
        )

        source = neighbour_pixel.get_center()

        destination = self.project_pixel_to_3d(
            row=row,
            col=col,
        )

        neighbour_point = self.make_world_point(
            source,
            CYAN_SOFT,
            radius=0.060,
        )

        self.add(
            neighbour_point
        )

        neighbour_path = CubicBezier(
            source,
            source + RIGHT * 0.9,
            destination + LEFT * 0.8 + DOWN * 0.15,
            destination,
        )

        self.play_timed(
            MoveAlongPath(
                neighbour_point,
                neighbour_path,
            ),
            neighbour_pixel.animate.set_opacity(
                0.32
            ),
            run_time=0.70,
        )

        mapping = Line(
            source,
            destination,
            color=CYAN_SOFT,
            stroke_width=1.0,
            stroke_opacity=0.26,
        )

        self.play_timed(
            Create(
                mapping
            ),
            run_time=0.40,
        )

        # Connection between neighboring 3D points.
        spatial_edge = Line(
            self.first_3d_point.get_center(),
            neighbour_point.get_center(),
            color=WHITE,
            stroke_width=1.0,
            stroke_opacity=0.28,
        )

        self.play_timed(
            Create(
                spatial_edge
            ),
            run_time=0.40,
        )

        self.wait_timed(0.40)

        self.neighbour_pixel = neighbour_pixel
        self.neighbour_point = neighbour_point

        self.neighbour_mapping = mapping
        self.spatial_edge = spatial_edge

    # =========================================================
    # 00:26 -> 00:33
    #
    # "toàn bộ ảnh...
    # mặt phẳng 2D bắt đầu bung ra thành một bề mặt 3D."
    # =========================================================

    def sentence_6(self):

        # Remove annotation, restore all pixels.
        self.play_timed(
            FadeOut(
                self.xyz_label
            ),
            FadeOut(
                self.xyz_connector
            ),
            self.other_pixels.animate.set_opacity(
                0.75
            ),
            run_time=0.45,
        )

        # -----------------------------------------------------
        # Build destination point map for ALL pixels.
        # -----------------------------------------------------

        destination_points = VGroup()

        for row in range(self.rows):
            for col in range(self.cols):

                destination = self.project_pixel_to_3d(
                    row,
                    col,
                )

                depth_t = col / (
                    self.cols - 1
                )

                color = interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    depth_t,
                )

                point = Dot(
                    destination,
                    radius=0.032,
                    color=color,
                )

                destination_points.add(
                    point
                )

        # Create a copy of every pixel that will lift into 3D.
        moving_pixels = self.image_pixels.copy()

        self.add(
            moving_pixels
        )

        animations = []

        for pixel, point in zip(
            moving_pixels,
            destination_points,
        ):
            animations.append(
                pixel.animate
                .move_to(
                    point.get_center()
                )
                .scale(0.35)
                .set_fill(
                    point.get_color(),
                    opacity=1,
                )
                .set_stroke(
                    width=0
                )
            )

        # "bung ra"
        self.play_timed(
            LaggedStart(
                *animations,
                lag_ratio=0.012,
            ),
            self.image_pixels.animate.set_opacity(
                0.10
            ),
            self.grid_outline.animate.set_opacity(
                0.08
            ),
            run_time=2.20,
            rate_func=smooth,
        )

        # -----------------------------------------------------
        # Connect topology -> surface mesh
        # -----------------------------------------------------

        mesh = self.make_surface_mesh()

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in mesh
                ],
                lag_ratio=0.008,
            ),
            run_time=1.40,
        )

        # Replace tiny squares visually with clean points.
        self.play_timed(
            FadeOut(
                moving_pixels
            ),
            FadeIn(
                destination_points
            ),
            run_time=0.55,
        )

        # Surface breath / depth emphasis.
        self.play_timed(
            destination_points.animate.scale(
                1.025
            ),
            mesh.animate.set_opacity(
                0.55
            ),
            run_time=0.45,
        )

        self.wait_timed(0.45)

        self.pointmap_points = destination_points
        self.pointmap_mesh = mesh

    # =========================================================
    # 00:34 -> 00:42
    #
    # "vẫn giữ quan hệ trực tiếp với pixel gốc,
    # nhưng đồng thời đã sống trong không gian 3D."
    # =========================================================

    def sentence_7(self):

        # -----------------------------------------------------
        # Split visual:
        # image space left, pointmap right.
        # Same indexing stays visible.
        # -----------------------------------------------------

        image_group = VGroup(
            self.image_pixels,
            self.grid_outline,
        )

        pointmap_group = VGroup(
            self.pointmap_points,
            self.pointmap_mesh,
        )

        self.play_timed(
            image_group.animate
            .scale(0.72)
            .move_to(LEFT * 3.7)
            .set_opacity(0.72),

            pointmap_group.animate
            .scale(0.72)
            .move_to(RIGHT * 3.4),

            run_time=0.85,
        )

        image_label = Text(
            "IMAGE SPACE",
            font_size=19,
            color=CYAN,
        )

        pointmap_label = Text(
            "3D SPACE",
            font_size=19,
            color=VIOLET,
        )

        image_label.next_to(
            image_group,
            UP,
            buff=0.28,
        )

        pointmap_label.next_to(
            pointmap_group,
            UP,
            buff=0.28,
        )

        self.play_timed(
            FadeIn(image_label),
            FadeIn(pointmap_label),
            run_time=0.45,
        )

        # -----------------------------------------------------
        # Pick several identical indices.
        # Pixel i <-> Point i
        # -----------------------------------------------------

        correspondence_indices = [
            (1, 2),
            (2, 5),
            (3, 6),
            (4, 8),
        ]

        mappings = VGroup()

        for row, col in correspondence_indices:

            index = (
                row * self.cols
                + col
            )

            pixel = self.image_pixels[index]
            point = self.pointmap_points[index]

            line = Line(
                pixel.get_center(),
                point.get_center(),
                color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    0.5,
                ),
                stroke_width=1.0,
                stroke_opacity=0.22,
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
                lag_ratio=0.15,
            ),
            run_time=1.00,
        )

        # Sequential index correspondence.
        for row, col in correspondence_indices[:3]:

            index = (
                row * self.cols
                + col
            )

            self.play_timed(
                Indicate(
                    self.image_pixels[index],
                    color=CYAN,
                    scale_factor=1.25,
                ),
                Indicate(
                    self.pointmap_points[index],
                    color=VIOLET,
                    scale_factor=1.6,
                ),
                run_time=0.55,
            )

        # Fade all except topology relationship.
        self.play_timed(
            mappings.animate.set_opacity(
                0.45
            ),
            self.pointmap_mesh.animate.set_opacity(
                0.35
            ),
            run_time=0.50,
        )

        # Signal travels from image to geometry.
        for line in mappings[:2]:

            pulse = line.copy()

            pulse.set_stroke(
                WHITE,
                width=2.5,
                opacity=0.75,
            )

            self.play_timed(
                ShowPassingFlash(
                    pulse,
                    time_width=0.25,
                ),
                run_time=0.45,
            )

        self.wait_timed(0.35)

        self.image_space_group = image_group
        self.pointmap_space_group = pointmap_group

        self.space_mappings = mappings
        self.image_space_label = image_label
        self.pointmap_space_label = pointmap_label

    # =========================================================
    # 00:43 -> 00:47
    #
    # "Nó nối image space và 3D space
    # trong cùng một representation."
    # =========================================================

    def sentence_8(self):

        # Make both spaces equally important.
        self.play_timed(
            self.image_space_group.animate.set_opacity(
                0.90
            ),
            self.pointmap_space_group.animate.set_opacity(
                0.95
            ),
            self.space_mappings.animate.set_opacity(
                0.55
            ),
            run_time=0.45,
        )

        # Central bridge.
        bridge = Arrow(
            self.image_space_group.get_right()
            + RIGHT * 0.20,
            self.pointmap_space_group.get_left()
            + LEFT * 0.20,
            buff=0.08,
            color=WHITE,
            stroke_width=1.5,
            stroke_opacity=0.65,
            max_tip_length_to_length_ratio=0.08,
        )

        reverse_bridge = Arrow(
            self.pointmap_space_group.get_left()
            + LEFT * 0.20
            + DOWN * 0.16,
            self.image_space_group.get_right()
            + RIGHT * 0.20
            + DOWN * 0.16,
            buff=0.08,
            color=MUTED,
            stroke_width=1.0,
            stroke_opacity=0.28,
            max_tip_length_to_length_ratio=0.08,
        )

        self.play_timed(
            GrowArrow(
                bridge
            ),
            GrowArrow(
                reverse_bridge
            ),
            run_time=0.65,
        )

        unified = Text(
            "POINTMAP",
            font_size=28,
            color=WHITE,
        )

        unified.move_to(
            ORIGIN + DOWN * 2.55
        )

        left_accent = Line(
            unified.get_left() + LEFT * 0.60,
            unified.get_left() - LEFT * 0.02,
            color=CYAN,
            stroke_width=1.4,
        )

        right_accent = Line(
            unified.get_right() + RIGHT * 0.02,
            unified.get_right() + RIGHT * 0.60,
            color=VIOLET,
            stroke_width=1.4,
        )

        self.play_timed(
            Create(
                left_accent
            ),
            FadeIn(
                unified,
                shift=UP * 0.07,
            ),
            Create(
                right_accent
            ),
            run_time=0.65,
        )

        # Final energy pulse:
        # image -> pointmap.
        pulse = bridge.copy()

        pulse.set_stroke(
            CYAN_SOFT,
            width=3.2,
            opacity=0.90,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.22,
            ),
            run_time=0.55,
        )

        self.play_timed(
            self.pointmap_points.animate.scale(
                1.035
            ),
            run_time=0.35,
        )

        self.wait_timed(0.35)

    # =========================================================
    # IMAGE GRID
    # =========================================================

    def make_image_grid(
        self,
        center,
    ):

        pixels = VGroup()

        left = (
            center[0]
            - self.grid_width / 2
        )

        bottom = (
            center[1]
            - self.grid_height / 2
        )

        for row in range(self.rows):
            for col in range(self.cols):

                x = (
                    left
                    + (col + 0.5)
                    * self.cell_w
                )

                y = (
                    bottom
                    + (
                        self.rows
                        - row
                        - 0.5
                    )
                    * self.cell_h
                )

                # Fake image content.
                u = col / (
                    self.cols - 1
                )

                v = row / (
                    self.rows - 1
                )

                color = interpolate_color(
                    ManimColor("#273444"),
                    ManimColor("#4D6179"),
                    0.55 * u + 0.20 * v,
                )

                # Add a brighter central region.
                dx = (
                    col
                    - self.cols * 0.52
                )

                dy = (
                    row
                    - self.rows * 0.52
                )

                distance = np.sqrt(
                    dx * dx
                    + dy * dy
                )

                if distance < 2.0:
                    color = interpolate_color(
                        color,
                        ManimColor(CYAN),
                        0.18,
                    )

                pixel = Square(
                    side_length=min(
                        self.cell_w,
                        self.cell_h,
                    )
                    * 0.93,
                    stroke_color="#5B6475",
                    stroke_width=0.45,
                    stroke_opacity=0.20,
                    fill_color=color,
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

        return pixels

    # =========================================================
    # PSEUDO-3D PROJECTION
    # =========================================================

    def project_pixel_to_3d(
        self,
        row,
        col,
    ):
        """
        Fake perspective projection.

        We deliberately keep row/column topology,
        but distort the grid according to a depth function.

        This gives the visual feeling of a pointmap surface
        without requiring ThreeDScene/OpenGL.
        """

        u = col / (
            self.cols - 1
        )

        v = row / (
            self.rows - 1
        )

        # Original normalized grid coordinates.
        x0 = (
            u - 0.5
        ) * 4.6

        y0 = (
            0.5 - v
        ) * 2.7

        # Synthetic depth surface.
        depth = (
            0.85
            + 0.65
            * np.sin(
                u * np.pi
            )
            * np.cos(
                v * np.pi * 0.85
            )
            + 0.28
            * u
        )

        # Isometric-like screen projection.
        screen_x = (
            x0
            + depth * 1.15
            + 0.45
        )

        screen_y = (
            y0
            + depth * 0.42
            - 0.28
        )

        return np.array([
            screen_x,
            screen_y,
            0.0,
        ])

    # =========================================================
    # SURFACE MESH
    # =========================================================

    def make_surface_mesh(self):

        mesh = VGroup()

        # Horizontal topology.
        for row in range(self.rows):

            for col in range(
                self.cols - 1
            ):

                p1 = self.project_pixel_to_3d(
                    row,
                    col,
                )

                p2 = self.project_pixel_to_3d(
                    row,
                    col + 1,
                )

                color = interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    col / (
                        self.cols - 1
                    ),
                )

                mesh.add(
                    Line(
                        p1,
                        p2,
                        color=color,
                        stroke_width=0.75,
                        stroke_opacity=0.40,
                    )
                )

        # Vertical topology.
        for col in range(self.cols):

            for row in range(
                self.rows - 1
            ):

                p1 = self.project_pixel_to_3d(
                    row,
                    col,
                )

                p2 = self.project_pixel_to_3d(
                    row + 1,
                    col,
                )

                color = interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    col / (
                        self.cols - 1
                    ),
                )

                mesh.add(
                    Line(
                        p1,
                        p2,
                        color=color,
                        stroke_width=0.75,
                        stroke_opacity=0.32,
                    )
                )

        return mesh

    # =========================================================
    # WORLD POINT
    # =========================================================

    def make_world_point(
        self,
        point,
        color,
        radius=0.06,
    ):

        halo_large = Circle(
            radius=radius * 3.4,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.022,
        )

        halo_small = Circle(
            radius=radius * 1.9,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.065,
        )

        core = Dot(
            radius=radius,
            color=color,
        )

        group = VGroup(
            halo_large,
            halo_small,
            core,
        )

        group.move_to(
            point
        )

        return group