from manim import *
import numpy as np

from theme import *


class Scene04ClassicalPipeline(Scene):
    """
    00:00-00:07
    "Nhưng để triangulate, trước tiên phải biết pixel nào ở ảnh này
    tương ứng với pixel nào ở ảnh kia."

    00:08-00:10
    "Rồi phải ước lượng mối quan hệ giữa các camera."

    00:11-00:22
    "Với nhiều ảnh, ta có một chuỗi khá dài:
    tìm keypoints, matching, camera geometry, triangulation,
    sparse reconstruction, rồi dense reconstruction."

    00:22-00:29
    "Những pipeline như SfM và MVS rất mạnh, nhưng chúng có một
    nhược điểm tự nhiên: lỗi ở bước trước có thể truyền xuống bước sau."

    00:29-00:30
    "DUSt3R bắt đầu bằng cách đặt lại câu hỏi."
    """

    def construct(self):
        self.camera.background_color = BG
        self.t = 0.0

        self.setup_views()

        self.sentence_1()
        self.wait_until(8.0)

        self.sentence_2()
        self.wait_until(11.0)

        self.sentence_3()
        self.wait_until(22.0)

        self.sentence_4()
        self.wait_until(29.0)

        self.sentence_5()
        self.wait_until(30.0)

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
    # INITIAL VIEWS
    # =========================================================

    def setup_views(self):
        self.left_image = self.make_image_card(
            variant=0,
            accent=CYAN,
        )

        self.right_image = self.make_image_card(
            variant=1,
            accent=VIOLET,
        )

        self.left_image.scale(0.88)
        self.right_image.scale(0.88)

        self.left_image.move_to(LEFT * 3.25)
        self.right_image.move_to(RIGHT * 3.25)

    # =========================================================
    # 00:00 -> 00:07
    #
    # Correspondence
    # =========================================================

    def sentence_1(self):

        self.play_timed(
            FadeIn(
                self.left_image,
                shift=UP * 0.10,
                scale=0.97,
            ),
            FadeIn(
                self.right_image,
                shift=UP * 0.10,
                scale=0.97,
            ),
            run_time=0.70,
        )

        # Feature locations in each image.
        left_positions = [
            self.left_image.get_center()
            + np.array([-0.75, 0.55, 0]),
            self.left_image.get_center()
            + np.array([0.10, 0.28, 0]),
            self.left_image.get_center()
            + np.array([-0.35, -0.42, 0]),
            self.left_image.get_center()
            + np.array([0.82, -0.18, 0]),
        ]

        right_positions = [
            self.right_image.get_center()
            + np.array([-0.48, 0.50, 0]),
            self.right_image.get_center()
            + np.array([0.34, 0.25, 0]),
            self.right_image.get_center()
            + np.array([-0.06, -0.40, 0]),
            self.right_image.get_center()
            + np.array([1.02, -0.15, 0]),
        ]

        self.left_features = VGroup()
        self.right_features = VGroup()

        colors = [
            CYAN,
            CYAN_SOFT,
            BLUE,
            VIOLET,
        ]

        for p, color in zip(left_positions, colors):
            self.left_features.add(
                self.make_feature(p, color)
            )

        for p, color in zip(right_positions, colors):
            self.right_features.add(
                self.make_feature(p, color)
            )

        # "pixel nào..."
        self.play_timed(
            LaggedStart(
                *[
                    GrowFromCenter(p)
                    for p in self.left_features
                ],
                lag_ratio=0.12,
            ),
            run_time=0.80,
        )

        # "...tương ứng với pixel nào..."
        self.play_timed(
            LaggedStart(
                *[
                    GrowFromCenter(p)
                    for p in self.right_features
                ],
                lag_ratio=0.12,
            ),
            run_time=0.80,
        )

        # Matching lines.
        self.matches = VGroup()

        for left, right, color in zip(
            self.left_features,
            self.right_features,
            colors,
        ):
            line = Line(
                left[-1].get_center(),
                right[-1].get_center(),
                color=color,
                stroke_width=1.2,
                stroke_opacity=0.38,
            )

            self.matches.add(line)

        self.play_timed(
            LaggedStart(
                *[
                    Create(line)
                    for line in self.matches
                ],
                lag_ratio=0.18,
            ),
            run_time=1.25,
        )

        # One correspondence gets emphasized.
        self.play_timed(
            Indicate(
                self.left_features[1][-1],
                color=CYAN_SOFT,
                scale_factor=1.45,
            ),
            Indicate(
                self.right_features[1][-1],
                color=CYAN_SOFT,
                scale_factor=1.45,
            ),
            run_time=0.70,
        )

        # Passing signal along correspondence.
        pulse = self.matches[1].copy()
        pulse.set_stroke(
            CYAN_SOFT,
            width=3,
            opacity=0.8,
        )

        self.play_timed(
            ShowPassingFlash(
                pulse,
                time_width=0.25,
            ),
            run_time=0.70,
        )

        self.wait_timed(1.35)

    # =========================================================
    # 00:08 -> 00:10
    #
    # Camera relation
    # =========================================================

    def sentence_2(self):

        self.play_timed(
            self.matches.animate.set_opacity(0.12),
            self.left_features.animate.set_opacity(0.35),
            self.right_features.animate.set_opacity(0.35),
            self.left_image.animate.scale(0.78).shift(UP * 0.65),
            self.right_image.animate.scale(0.78).shift(UP * 0.65),
            run_time=0.45,
        )

        cam1 = self.make_camera_pose(
            LEFT * 2.5 + DOWN * 1.55,
            CYAN,
            angle=-12 * DEGREES,
        )

        cam2 = self.make_camera_pose(
            RIGHT * 2.5 + DOWN * 1.55,
            VIOLET,
            angle=15 * DEGREES,
        )

        baseline = Line(
            cam1.get_center(),
            cam2.get_center(),
            color=MUTED,
            stroke_width=1,
            stroke_opacity=0.35,
        )

        self.play_timed(
            FadeIn(cam1, scale=0.8),
            FadeIn(cam2, scale=0.8),
            Create(baseline),
            run_time=0.65,
        )

        # Show relative pose as spatial relationship.
        relative_arc = ArcBetweenPoints(
            cam1.get_center() + UP * 0.05,
            cam2.get_center() + UP * 0.05,
            angle=-0.18,
            color=VIOLET,
            stroke_width=1.3,
        )

        self.play_timed(
            Create(relative_arc),
            run_time=0.40,
        )

        self.play_timed(
            cam2.animate.rotate(
                -8 * DEGREES
            ),
            run_time=0.35,
        )

        self.cam1 = cam1
        self.cam2 = cam2
        self.baseline = baseline
        self.relative_arc = relative_arc

    # =========================================================
    # 00:11 -> 00:22
    #
    # Full classical pipeline
    # =========================================================

    def sentence_3(self):

        # Clear geometry into a clean processing layout.
        self.play_timed(
            FadeOut(self.matches),
            FadeOut(self.left_features),
            FadeOut(self.right_features),
            FadeOut(self.cam1),
            FadeOut(self.cam2),
            FadeOut(self.baseline),
            FadeOut(self.relative_arc),
            self.left_image.animate
            .scale(0.76)
            .move_to(LEFT * 5.2),
            self.right_image.animate
            .scale(0.76)
            .move_to(LEFT * 4.0 + DOWN * 0.10),
            run_time=0.65,
        )

        input_stack = VGroup(
            self.left_image,
            self.right_image,
        )

        # -----------------------------------------------------
        # STEP 1 — KEYPOINTS
        # -----------------------------------------------------

        keypoints = self.make_pipeline_node(
            "KEYPOINTS",
            CYAN,
        )
        keypoints.move_to(LEFT * 2.45)

        arrow_1 = self.make_arrow(
            input_stack.get_right(),
            keypoints.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_1),
            FadeIn(
                keypoints,
                shift=RIGHT * 0.10,
            ),
            run_time=0.75,
        )

        # Tiny points appear inside.
        kp_dots = VGroup()

        rng = np.random.default_rng(10)

        for _ in range(9):
            p = Dot(
                radius=0.022,
                color=CYAN,
            )

            p.move_to(
                keypoints.get_center()
                + np.array([
                    rng.uniform(-0.48, 0.48),
                    rng.uniform(-0.18, 0.18),
                    0,
                ])
            )

            kp_dots.add(p)

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(p, scale=0.4)
                    for p in kp_dots
                ],
                lag_ratio=0.05,
            ),
            run_time=0.50,
        )

        # -----------------------------------------------------
        # STEP 2 — MATCHING
        # -----------------------------------------------------

        matching = self.make_pipeline_node(
            "MATCHING",
            BLUE,
        )
        matching.move_to(LEFT * 0.55)

        arrow_2 = self.make_arrow(
            keypoints.get_right(),
            matching.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_2),
            FadeIn(
                matching,
                shift=RIGHT * 0.10,
            ),
            run_time=0.65,
        )

        # -----------------------------------------------------
        # STEP 3 — CAMERA GEOMETRY
        # -----------------------------------------------------

        geometry = self.make_pipeline_node(
            "CAMERA\nGEOMETRY",
            VIOLET,
            width=1.55,
        )
        geometry.move_to(RIGHT * 1.45)

        arrow_3 = self.make_arrow(
            matching.get_right(),
            geometry.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_3),
            FadeIn(
                geometry,
                shift=RIGHT * 0.10,
            ),
            run_time=0.70,
        )

        # -----------------------------------------------------
        # Screen scrolls left to reveal next part.
        # -----------------------------------------------------

        first_half = VGroup(
            input_stack,
            arrow_1,
            keypoints,
            kp_dots,
            arrow_2,
            matching,
            arrow_3,
            geometry,
        )

        self.play_timed(
            first_half.animate.shift(
                LEFT * 3.5
            ),
            run_time=0.60,
        )

        # -----------------------------------------------------
        # STEP 4 — TRIANGULATION
        # -----------------------------------------------------

        triangulation = self.make_pipeline_node(
            "TRIANGULATION",
            CYAN_SOFT,
            width=1.75,
        )

        triangulation.move_to(
            LEFT * 0.4
        )

        arrow_4 = self.make_arrow(
            geometry.get_right(),
            triangulation.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_4),
            FadeIn(
                triangulation,
                shift=RIGHT * 0.10,
            ),
            run_time=0.70,
        )

        # -----------------------------------------------------
        # STEP 5 — SPARSE
        # -----------------------------------------------------

        sparse = self.make_pipeline_node(
            "SPARSE 3D",
            BLUE,
        )

        sparse.move_to(
            RIGHT * 1.7
        )

        arrow_5 = self.make_arrow(
            triangulation.get_right(),
            sparse.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_5),
            FadeIn(
                sparse,
                shift=RIGHT * 0.10,
            ),
            run_time=0.65,
        )

        sparse_points = VGroup()

        for p in [
            [-0.45, 0.12],
            [-0.15, -0.08],
            [0.05, 0.15],
            [0.35, -0.10],
        ]:
            dot = Dot(
                radius=0.026,
                color=CYAN_SOFT,
            )

            dot.move_to(
                sparse.get_center()
                + np.array([
                    p[0],
                    p[1],
                    0,
                ])
            )

            sparse_points.add(dot)

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(p)
                    for p in sparse_points
                ],
                lag_ratio=0.08,
            ),
            run_time=0.35,
        )

        # -----------------------------------------------------
        # STEP 6 — DENSE
        # -----------------------------------------------------

        dense = self.make_pipeline_node(
            "DENSE 3D",
            VIOLET,
        )

        dense.move_to(
            RIGHT * 3.9
        )

        arrow_6 = self.make_arrow(
            sparse.get_right(),
            dense.get_left(),
        )

        self.play_timed(
            GrowArrow(arrow_6),
            FadeIn(
                dense,
                shift=RIGHT * 0.10,
            ),
            run_time=0.65,
        )

        dense_points = VGroup()

        rng = np.random.default_rng(4)

        for _ in range(28):
            dot = Dot(
                radius=0.016,
                color=interpolate_color(
                    ManimColor(CYAN),
                    ManimColor(VIOLET),
                    rng.uniform(),
                ),
            )

            dot.move_to(
                dense.get_center()
                + np.array([
                    rng.uniform(-0.50, 0.50),
                    rng.uniform(-0.20, 0.20),
                    0,
                ])
            )

            dense_points.add(dot)

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        p,
                        scale=0.3,
                    )
                    for p in dense_points
                ],
                lag_ratio=0.02,
            ),
            run_time=0.55,
        )

        self.pipeline = VGroup(
            first_half,
            arrow_4,
            triangulation,
            arrow_5,
            sparse,
            sparse_points,
            arrow_6,
            dense,
            dense_points,
        )

        self.pipeline_nodes = [
            keypoints,
            matching,
            geometry,
            triangulation,
            sparse,
            dense,
        ]

    # =========================================================
    # 00:22 -> 00:29
    #
    # Error propagation
    # =========================================================

    def sentence_4(self):

        # -----------------------------------------------------
        # First: acknowledge pipeline is powerful.
        # Everything looks healthy.
        # -----------------------------------------------------

        self.play_timed(
            self.pipeline.animate.set_opacity(
                0.92
            ),
            run_time=0.40,
        )

        # -----------------------------------------------------
        # Introduce ONE bad match near the beginning.
        # -----------------------------------------------------

        matching = self.pipeline_nodes[1]

        error = Dot(
            radius=0.055,
            color=RED,
        )

        error.move_to(
            matching.get_center()
        )

        error_halo = Circle(
            radius=0.18,
            stroke_width=0,
            fill_color=RED,
            fill_opacity=0.08,
        ).move_to(error)

        self.play_timed(
            GrowFromCenter(
                error_halo
            ),
            GrowFromCenter(
                error
            ),
            run_time=0.45,
        )

        self.play_timed(
            Flash(
                error,
                color=RED,
                line_length=0.12,
                num_lines=8,
            ),
            run_time=0.50,
        )

        # -----------------------------------------------------
        # Error propagates downstream.
        # -----------------------------------------------------

        downstream = self.pipeline_nodes[2:]

        for node in downstream:

            connector = Line(
                error.get_center(),
                node.get_center(),
                color=RED,
                stroke_width=1.4,
                stroke_opacity=0.25,
            )

            pulse = connector.copy()

            pulse.set_stroke(
                RED,
                width=3,
                opacity=0.85,
            )

            self.play_timed(
                Create(
                    connector
                ),
                ShowPassingFlash(
                    pulse,
                    time_width=0.25,
                ),
                run_time=0.45,
            )

            self.play_timed(
                node.animate.set_stroke(
                    RED,
                    opacity=0.55,
                ),
                run_time=0.25,
            )

            error.move_to(
                node.get_center()
            )

        # Dense reconstruction visibly degrades.
        dense = self.pipeline_nodes[-1]

        corrupted = VGroup()

        rng = np.random.default_rng(31)

        for _ in range(14):
            dot = Dot(
                radius=0.021,
                color=RED,
            )

            dot.move_to(
                dense.get_center()
                + np.array([
                    rng.uniform(-0.75, 0.75),
                    rng.uniform(-0.55, 0.55),
                    0,
                ])
            )

            corrupted.add(dot)

        self.play_timed(
            LaggedStart(
                *[
                    FadeIn(
                        p,
                        shift=np.array([
                            rng.uniform(-0.15, 0.15),
                            rng.uniform(-0.15, 0.15),
                            0,
                        ]),
                    )
                    for p in corrupted
                ],
                lag_ratio=0.035,
            ),
            run_time=0.85,
        )

        # Whole pipeline subtly destabilizes.
        self.play_timed(
            self.pipeline.animate.shift(
                DOWN * 0.05
            ),
            corrupted.animate.set_opacity(
                0.8
            ),
            run_time=0.40,
            rate_func=there_and_back,
        )

        self.error_visuals = VGroup(
            error_halo,
            error,
            corrupted,
        )

    # =========================================================
    # 00:29 -> 00:30
    #
    # "DUSt3R bắt đầu bằng cách đặt lại câu hỏi."
    # =========================================================

    def sentence_5(self):

        # Classical pipeline recedes into the background.
        self.play_timed(
            self.pipeline.animate
            .scale(0.92)
            .set_opacity(0.10),

            FadeOut(
                self.error_visuals
            ),

            run_time=0.45,
        )

        # No giant logo yet.
        # Just a deliberate visual reset.
        question = Text(
            "What if we predict 3D directly?",
            font_size=34,
            color=WHITE,
        )

        question.move_to(
            ORIGIN
        )

        accent = Line(
            question.get_left()
            + DOWN * 0.28,
            question.get_right()
            + DOWN * 0.28,
            color=CYAN,
            stroke_width=1.5,
            stroke_opacity=0.65,
        )

        self.play_timed(
            FadeIn(
                question,
                shift=UP * 0.10,
            ),
            Create(
                accent
            ),
            run_time=0.55,
        )

    # =========================================================
    # HELPERS
    # =========================================================

    def make_image_card(
        self,
        variant=0,
        accent=CYAN,
    ):

        frame = RoundedRectangle(
            width=4.0,
            height=2.45,
            corner_radius=0.10,
            stroke_color="#303747",
            stroke_width=1.0,
            fill_color="#10141D",
            fill_opacity=1,
        )

        floor = Polygon(
            [-1.90, -1.05, 0],
            [1.90, -1.05, 0],
            [0.65 + variant * 0.22, 0.12, 0],
            [-0.72 + variant * 0.22, 0.12, 0],
            fill_color="#1A202C",
            fill_opacity=1,
            stroke_width=0,
        )

        sofa = RoundedRectangle(
            width=1.10,
            height=0.40,
            corner_radius=0.07,
            stroke_width=0,
            fill_color="#5D6980",
            fill_opacity=0.7,
        )

        sofa.move_to(
            LEFT * (0.45 - variant * 0.18)
            + DOWN * 0.33
        )

        window = Rectangle(
            width=0.72,
            height=0.62,
            stroke_color=accent,
            stroke_width=0.8,
            stroke_opacity=0.40,
            fill_color=accent,
            fill_opacity=0.025,
        )

        window.move_to(
            RIGHT * (1.02 - variant * 0.15)
            + UP * 0.55
        )

        content = VGroup(
            floor,
            sofa,
            window,
        )

        return VGroup(
            frame,
            content,
        )

    def make_feature(
        self,
        point,
        color,
    ):

        halo = Circle(
            radius=0.11,
            stroke_color=color,
            stroke_width=1,
            stroke_opacity=0.15,
        )

        core = Dot(
            radius=0.035,
            color=color,
        )

        group = VGroup(
            halo,
            core,
        )

        group.move_to(
            point
        )

        return group

    def make_camera_pose(
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
            LEFT * 0.32,
            RIGHT * 0.32,
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
            ),
            Line(
                core.get_center(),
                plane.get_right(),
                color=color,
                stroke_width=1,
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

    def make_pipeline_node(
        self,
        label,
        color,
        width=1.45,
    ):

        box = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.10,
            stroke_color=color,
            stroke_width=1.1,
            stroke_opacity=0.55,
            fill_color=color,
            fill_opacity=0.025,
        )

        text = Text(
            label,
            font_size=15,
            color=WHITE,
            line_spacing=0.8,
        )

        text.set_opacity(
            0.80
        )

        text.move_to(
            box
        )

        return VGroup(
            box,
            text,
        )

    def make_arrow(
        self,
        start,
        end,
    ):

        return Arrow(
            start,
            end,
            buff=0.12,
            color=MUTED,
            stroke_width=1.2,
            stroke_opacity=0.45,
            max_tip_length_to_length_ratio=0.12,
        )