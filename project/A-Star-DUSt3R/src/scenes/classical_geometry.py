"""Chapter 2 — classical geometry is precise, but sequentially dependent."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    Scene,
    Square,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    chapter_title,
    label_pill,
    make_camera,
    make_image_panel,
    make_point_cloud,
    make_pointmap_positions,
    toy_world,
)


class ClassicalGeometryScene(Scene):
    """Show triangulation sensitivity, then follow evidence through SfM and MVS."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]

        heading = chapter_title(
            "02 · Hình học cổ điển",
            "Hai tia nhìn, một điểm 3D",
            accent=PALETTE["pose"],
        ).to_corner(UP + LEFT, buff=0.42)
        self.play(FadeIn(heading, shift=RIGHT * 0.18))

        world = toy_world().scale(0.5).move_to(UP * 0.35)
        true_point = world[1].get_corner(UP + RIGHT)
        true_marker = Dot(true_point, radius=0.085, color=PALETTE["world"])

        center_1 = np.array([-5.1, -2.35, 0.0])
        center_2 = np.array([5.1, -2.35, 0.0])
        camera_1 = make_camera(PALETTE["view_1"], scale=0.72).move_to(center_1)
        camera_2 = make_camera(PALETTE["view_2"], mirrored=True, scale=0.72).move_to(center_2)
        view_1 = label_pill("view 1", accent=PALETTE["view_1"], font_size=18).next_to(camera_1, DOWN)
        view_2 = label_pill("view 2", accent=PALETTE["view_2"], font_size=18).next_to(camera_2, DOWN)

        direction_1 = true_point - center_1
        direction_2 = true_point - center_2
        pixel_center_1 = center_1 + 0.31 * direction_1
        pixel_center_2 = center_2 + 0.31 * direction_2
        normal_1 = np.array([-direction_1[1], direction_1[0], 0.0])
        normal_1 /= np.linalg.norm(normal_1)
        normal_2 = np.array([-direction_2[1], direction_2[0], 0.0])
        normal_2 /= np.linalg.norm(normal_2)

        plane_1 = Line(
            pixel_center_1 - 0.58 * normal_1,
            pixel_center_1 + 0.58 * normal_1,
            color=PALETTE["view_1"],
            stroke_width=3,
        )
        plane_2 = Line(
            pixel_center_2 - 0.58 * normal_2,
            pixel_center_2 + 0.58 * normal_2,
            color=PALETTE["view_2"],
            stroke_width=3,
        )
        pixel_1 = Square(
            side_length=0.17,
            stroke_color=PALETTE["ink"],
            stroke_width=1,
            fill_color=PALETTE["view_1"],
            fill_opacity=1,
        ).move_to(pixel_center_1)
        pixel_2 = Square(
            side_length=0.17,
            stroke_color=PALETTE["ink"],
            stroke_width=1,
            fill_color=PALETTE["view_2"],
            fill_opacity=1,
        ).move_to(pixel_center_2)

        ray_1_end = true_point + 0.42 * direction_1
        ray_2_end = true_point + 0.42 * direction_2
        ray_1 = Line(
            center_1,
            ray_1_end,
            color=PALETTE["view_1"],
            stroke_width=1.8,
            stroke_opacity=0.62,
        )
        ray_2 = Line(
            center_2,
            ray_2_end,
            color=PALETTE["view_2"],
            stroke_width=1.8,
            stroke_opacity=0.62,
        )
        correspondence = Line(
            pixel_1.get_center(),
            pixel_2.get_center(),
            color=PALETTE["ink"],
            stroke_width=1.1,
            stroke_opacity=0.28,
        )

        self.play(
            FadeIn(world),
            FadeIn(camera_1, shift=RIGHT * 0.15),
            FadeIn(camera_2, shift=LEFT * 0.15),
            FadeIn(view_1),
            FadeIn(view_2),
            run_time=1.3,
        )
        self.play(Create(plane_1), Create(plane_2), FadeIn(pixel_1), FadeIn(pixel_2))
        self.play(Create(correspondence), run_time=0.7)
        self.play(Create(ray_1), Create(ray_2), run_time=1.4)
        self.play(GrowFromCenter(true_marker), Indicate(world[1], color=PALETTE["world"]), run_time=0.9)

        triangulation = Text(
            "camera + correspondence → triangulation",
            font_size=25,
            color=PALETTE["ink"],
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(triangulation, shift=UP * 0.12))
        self.wait(0.6)

        bad_camera_center = center_2 + LEFT * 0.13 + UP * 0.24
        outlier_point = true_point + 0.39 * direction_1
        bad_direction = outlier_point - bad_camera_center
        bad_pixel_center = bad_camera_center + 0.31 * bad_direction
        bad_normal = np.array([-bad_direction[1], bad_direction[0], 0.0])
        bad_normal /= np.linalg.norm(bad_normal)
        bad_plane_2 = Line(
            bad_pixel_center - 0.58 * bad_normal,
            bad_pixel_center + 0.58 * bad_normal,
            color=PALETTE["pose"],
            stroke_width=3,
        )
        bad_pixel_2 = pixel_2.copy().move_to(bad_pixel_center).set_fill(PALETTE["pose"])
        bad_ray_2 = Line(
            bad_camera_center,
            outlier_point + 0.13 * bad_direction,
            color=PALETTE["pose"],
            stroke_width=2.3,
            stroke_opacity=0.78,
        )
        outlier = Dot(outlier_point, radius=0.095, color=PALETTE["low_confidence"])
        displacement = Line(
            true_point,
            outlier_point,
            color=PALETTE["low_confidence"],
            stroke_width=4,
        )
        perturbation = label_pill(
            "pose / focal hơi lệch",
            accent=PALETTE["pose"],
            font_size=19,
        ).next_to(camera_2, UP, buff=0.35)
        sensitivity = Text(
            "giao điểm trượt xa",
            font_size=25,
            color=PALETTE["low_confidence"],
            weight="BOLD",
        ).move_to(triangulation)

        self.play(
            camera_2.animate.shift(LEFT * 0.13 + UP * 0.24).rotate(0.07),
            Transform(plane_2, bad_plane_2),
            Transform(pixel_2, bad_pixel_2),
            Transform(ray_2, bad_ray_2),
            Transform(triangulation, sensitivity),
            FadeIn(perturbation, shift=UP * 0.1),
            run_time=1.6,
        )
        self.play(
            Transform(true_marker, outlier),
            Create(displacement),
            run_time=1.0,
        )
        self.play(Indicate(true_marker, color=PALETTE["low_confidence"], scale_factor=1.3))
        self.wait(0.5)

        geometry = VGroup(
            world,
            camera_1,
            camera_2,
            view_1,
            view_2,
            plane_1,
            plane_2,
            pixel_1,
            pixel_2,
            ray_1,
            ray_2,
            correspondence,
            true_marker,
            displacement,
            perturbation,
            triangulation,
        )
        pipeline_heading = chapter_title(
            "Từ sparse đến dense",
            "Bằng chứng đi qua một chuỗi hình học",
            accent=PALETTE["view_1"],
        ).to_corner(UP + LEFT, buff=0.42)
        self.play(FadeOut(geometry), Transform(heading, pipeline_heading), run_time=1.0)

        image_a = make_image_panel(
            "VIEW 1",
            accent=PALETTE["view_1"],
            variant=0,
            width=3.05,
            height=2.02,
        ).move_to(LEFT * 3.35 + UP * 0.1)
        image_b = make_image_panel(
            "VIEW 2",
            accent=PALETTE["view_2"],
            variant=1,
            width=3.05,
            height=2.02,
        ).move_to(RIGHT * 3.35 + UP * 0.1)
        phase = label_pill("1 · keypoints", accent=PALETTE["view_1"], font_size=21)
        phase.to_edge(DOWN, buff=0.38)
        self.play(FadeIn(image_a, shift=RIGHT * 0.12), FadeIn(image_b, shift=LEFT * 0.12), FadeIn(phase))

        offsets_a = [
            np.array([-0.72, 0.46, 0.0]),
            np.array([-0.18, -0.18, 0.0]),
            np.array([0.44, 0.34, 0.0]),
            np.array([0.72, -0.42, 0.0]),
            np.array([-0.58, -0.56, 0.0]),
            np.array([0.1, 0.58, 0.0]),
        ]
        offsets_b = [
            np.array([-0.56, 0.44, 0.0]),
            np.array([0.05, -0.2, 0.0]),
            np.array([0.58, 0.31, 0.0]),
            np.array([0.72, -0.38, 0.0]),
            np.array([-0.4, -0.55, 0.0]),
            np.array([0.29, 0.57, 0.0]),
        ]
        keypoints_a = VGroup(
            *[
                Dot(image_a[0].get_center() + offset, radius=0.052, color=PALETTE["view_1"])
                for offset in offsets_a
            ]
        )
        keypoints_b = VGroup(
            *[
                Dot(image_b[0].get_center() + offset, radius=0.052, color=PALETTE["view_2"])
                for offset in offsets_b
            ]
        )
        self.play(
            LaggedStart(*[GrowFromCenter(point) for point in VGroup(keypoints_a, keypoints_b)], lag_ratio=0.05),
            run_time=1.3,
        )

        good_matches = VGroup(
            *[
                Line(
                    keypoints_a[index].get_center(),
                    keypoints_b[index].get_center(),
                    color=PALETTE["ink"],
                    stroke_width=1.4,
                    stroke_opacity=0.42,
                )
                for index in (0, 1, 2, 4, 5)
            ]
        )
        wrong_matches = VGroup(
            Line(
                keypoints_a[3].get_center(),
                keypoints_b[0].get_center(),
                color=PALETTE["low_confidence"],
                stroke_width=2.1,
                stroke_opacity=0.86,
            ),
            Line(
                keypoints_a[1].get_center(),
                keypoints_b[4].get_center(),
                color=PALETTE["low_confidence"],
                stroke_width=2.1,
                stroke_opacity=0.72,
            ),
        )
        matching_phase = label_pill("2 · matching", accent=PALETTE["view_2"], font_size=21)
        matching_phase.move_to(phase)
        self.play(
            Transform(phase, matching_phase),
            LaggedStart(*[Create(match) for match in good_matches], lag_ratio=0.1),
            run_time=1.3,
        )
        self.play(Create(wrong_matches), run_time=0.7)

        robust_ring = Circle(
            radius=0.55,
            stroke_color=PALETTE["pose"],
            stroke_width=3,
            stroke_opacity=0.85,
        ).move_to(wrong_matches[0].get_center())
        reject_a = VGroup(
            Line(LEFT * 0.12 + UP * 0.12, RIGHT * 0.12 + DOWN * 0.12, color=PALETTE["pose"], stroke_width=4),
            Line(LEFT * 0.12 + DOWN * 0.12, RIGHT * 0.12 + UP * 0.12, color=PALETTE["pose"], stroke_width=4),
        ).move_to(wrong_matches[0].get_center())
        robust_phase = label_pill("3 · robust estimation", accent=PALETTE["pose"], font_size=21)
        robust_phase.move_to(phase)
        self.play(Transform(phase, robust_phase), Create(robust_ring), FadeIn(reject_a), run_time=0.8)
        self.play(
            FadeOut(wrong_matches[0]),
            FadeOut(robust_ring),
            FadeOut(reject_a),
            wrong_matches[1].animate.set_opacity(0.28),
            run_time=0.8,
        )

        positions = make_pointmap_positions(rows=4, cols=7)
        target_sparse = make_point_cloud(
            positions,
            color=PALETTE["ink"],
            radius=0.058,
            scale=0.88,
        ).move_to(UP * 0.05)
        sparse = target_sparse.copy()
        perturbations = {
            2: LEFT * 0.16 + UP * 0.08,
            8: RIGHT * 0.13 + DOWN * 0.09,
            15: RIGHT * 0.18 + UP * 0.06,
            23: LEFT * 0.14 + DOWN * 0.1,
        }
        for index, shift in perturbations.items():
            sparse[index].shift(shift)
        residuals = VGroup(
            *[
                Line(
                    sparse[index].get_center(),
                    target_sparse[index].get_center(),
                    color=PALETTE["pose"],
                    stroke_width=2.2,
                    stroke_opacity=0.72,
                )
                for index in perturbations
            ]
        )
        sfm_camera_1 = make_camera(PALETTE["view_1"], scale=0.46).move_to(LEFT * 3.1 + DOWN * 1.45)
        sfm_camera_2 = make_camera(PALETTE["view_2"], mirrored=True, scale=0.46).move_to(RIGHT * 3.1 + DOWN * 1.45)
        sfm_phase = label_pill("4 · SfM + bundle adjustment", accent=PALETTE["pose"], font_size=21)
        sfm_phase.move_to(phase)
        self.play(
            Transform(phase, sfm_phase),
            FadeOut(VGroup(image_a, image_b, keypoints_a, keypoints_b, wrong_matches)),
            ReplacementTransform(good_matches, sparse),
            FadeIn(sfm_camera_1, shift=RIGHT * 0.16),
            FadeIn(sfm_camera_2, shift=LEFT * 0.16),
            run_time=1.6,
        )
        self.play(Create(residuals), run_time=0.7)
        collapsed_residuals = VGroup(
            *[
                Dot(target_sparse[index].get_center(), radius=0.012, color=PALETTE["confidence"])
                for index in perturbations
            ]
        )
        self.play(
            Transform(sparse, target_sparse),
            Transform(residuals, collapsed_residuals),
            sfm_camera_1.animate.shift(RIGHT * 0.16 + UP * 0.06),
            sfm_camera_2.animate.shift(LEFT * 0.16 + UP * 0.06),
            run_time=1.35,
        )

        surviving_error = Dot(
            target_sparse.get_corner(UP + RIGHT) + RIGHT * 0.54 + UP * 0.26,
            radius=0.07,
            color=PALETTE["low_confidence"],
        )
        self.play(TransformFromCopy(wrong_matches[1], surviving_error), run_time=0.7)

        dense_positions = make_pointmap_positions(rows=7, cols=11)
        dense = make_point_cloud(
            dense_positions,
            color=PALETTE["view_1"],
            radius=0.033,
            scale=0.72,
        ).move_to(UP * 0.05)
        dense_phase = label_pill("5 · dense MVS", accent=PALETTE["confidence"], font_size=21)
        dense_phase.move_to(phase)
        error_cluster = VGroup(
            surviving_error.copy(),
            surviving_error.copy().shift(RIGHT * 0.18 + DOWN * 0.08),
            surviving_error.copy().shift(LEFT * 0.11 + UP * 0.13),
            surviving_error.copy().shift(RIGHT * 0.06 + UP * 0.2),
        )
        self.play(
            Transform(phase, dense_phase),
            ReplacementTransform(sparse, dense),
            FadeOut(residuals),
            FadeIn(error_cluster, scale=0.35),
            FadeOut(surviving_error),
            run_time=1.7,
        )
        self.play(LaggedStart(*[Indicate(dot, color=PALETTE["low_confidence"]) for dot in error_cluster], lag_ratio=0.14))

        summary = Text(
            "Hình học mạnh mẽ · các bước phụ thuộc tuần tự",
            font_size=29,
            color=PALETTE["ink"],
            weight="BOLD",
        ).to_edge(DOWN, buff=0.36)
        nuance = Text(
            "robust estimation và BA sửa nhiều lỗi — nhưng đầu vào vẫn quyết định các bước sau",
            font_size=20,
            color=PALETTE["muted"],
        ).next_to(summary, DOWN, buff=0.12)
        self.play(FadeOut(phase), FadeIn(summary, shift=UP * 0.12), FadeIn(nuance), run_time=0.9)
        self.play(
            dense.animate.scale(1.08),
            sfm_camera_1.animate.shift(LEFT * 0.2),
            sfm_camera_2.animate.shift(RIGHT * 0.2),
            run_time=1.0,
        )
        self.wait(1.0)
        self.play(
            FadeOut(
                VGroup(
                    heading,
                    dense,
                    sfm_camera_1,
                    sfm_camera_2,
                    error_cluster,
                    summary,
                    nuance,
                )
            ),
            run_time=0.8,
        )
