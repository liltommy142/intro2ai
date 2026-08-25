"""Chapter 1 — begin with an ambiguous image, then reveal a 3D world."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Scene,
    Square,
    Text,
    Transform,
    VGroup,
)

from scenes.visuals import (
    PALETTE,
    label_pill,
    make_camera,
    make_image_panel,
    make_point_cloud,
    make_pointmap_positions,
    toy_world,
)


class IntroScene(Scene):
    """Turn two flat observations into the film's persistent 3D hero object."""

    def construct(self) -> None:
        self.camera.background_color = PALETTE["background"]

        world = toy_world().scale(0.94).shift(UP * 0.05)
        world_tag = label_pill("một thế giới 3D", accent=PALETTE["world"], font_size=19)
        world_tag.next_to(world, DOWN, buff=0.18)

        camera_1 = make_camera(PALETTE["view_1"], scale=0.72)
        camera_1.move_to(LEFT * 5.25 + DOWN * 2.35)
        camera_2 = make_camera(PALETTE["view_2"], mirrored=True, scale=0.72)
        camera_2.move_to(RIGHT * 5.25 + DOWN * 2.35)

        image_1 = make_image_panel(
            "VIEW 1",
            accent=PALETTE["view_1"],
            variant=0,
            width=2.55,
            height=1.72,
        ).move_to(LEFT * 4.45 + UP * 1.65)
        image_2 = make_image_panel(
            "VIEW 2",
            accent=PALETTE["view_2"],
            variant=1,
            width=2.55,
            height=1.72,
        ).move_to(RIGHT * 4.45 + UP * 1.65)
        camera_2.set_opacity(0.2)
        image_2.set_opacity(0.2)

        framing_1 = VGroup(
            Line(
                camera_1.get_center(),
                image_1[0].get_corner(DOWN + LEFT),
                color=PALETTE["view_1"],
                stroke_width=1.2,
                stroke_opacity=0.24,
            ),
            Line(
                camera_1.get_center(),
                image_1[0].get_corner(DOWN + RIGHT),
                color=PALETTE["view_1"],
                stroke_width=1.2,
                stroke_opacity=0.24,
            ),
        )
        framing_2 = VGroup(
            Line(
                camera_2.get_center(),
                image_2[0].get_corner(DOWN + LEFT),
                color=PALETTE["view_2"],
                stroke_width=1.2,
                stroke_opacity=0.24,
            ),
            Line(
                camera_2.get_center(),
                image_2[0].get_corner(DOWN + RIGHT),
                color=PALETTE["view_2"],
                stroke_width=1.2,
                stroke_opacity=0.24,
            ),
        ).set_opacity(0.2)

        self.play(FadeIn(world, scale=0.92), FadeIn(world_tag), run_time=1.6)
        self.play(
            FadeIn(camera_1, shift=RIGHT * 0.18),
            Create(framing_1),
            FadeIn(image_1, shift=UP * 0.15),
            run_time=1.5,
        )
        self.play(FadeIn(camera_2), FadeIn(image_2), FadeIn(framing_2), run_time=0.7)

        question = Text(
            "Một pixel nằm ở đâu trong không gian?",
            font_size=31,
            color=PALETTE["ink"],
            weight="BOLD",
        ).to_edge(UP, buff=0.34)
        self.play(FadeIn(question, shift=DOWN * 0.12))

        pixel_centers_1 = [
            image_1[3].get_center() + LEFT * 0.12 + UP * 0.05,
            image_1[4].get_center() + DOWN * 0.04,
            image_1[2].get_center() + LEFT * 0.42 + DOWN * 0.08,
        ]
        target_centers = [
            world[1].get_center() + UP * 0.16,
            world[3].get_center() + UP * 0.18,
            world[0].get_center() + LEFT * 0.95 + DOWN * 0.1,
        ]
        pixels_1 = VGroup(
            *[
                Square(
                    side_length=0.15,
                    stroke_color=PALETTE["ink"],
                    stroke_width=1.0,
                    fill_color=PALETTE["view_1"],
                    fill_opacity=1,
                ).move_to(center)
                for center in pixel_centers_1
            ]
        )
        rays_1 = VGroup()
        sliders = VGroup()
        ghosts = VGroup()
        for pixel, target in zip(pixels_1, target_centers):
            start = pixel.get_center()
            end = target + 0.52 * (target - start)
            ray = Line(
                start,
                end,
                color=PALETTE["view_1"],
                stroke_width=1.5,
                stroke_opacity=0.5,
            )
            rays_1.add(ray)
            sliders.add(Dot(ray.point_from_proportion(0.28), radius=0.065, color=PALETTE["view_1"]))
            for amount in (0.46, 0.68, 0.86):
                ghosts.add(
                    Dot(
                        ray.point_from_proportion(amount),
                        radius=0.045,
                        color=PALETTE["view_1"],
                        fill_opacity=0.22,
                    )
                )

        self.play(FadeIn(pixels_1), LaggedStart(*[Create(ray) for ray in rays_1], lag_ratio=0.13))
        self.play(FadeIn(ghosts), FadeIn(sliders), run_time=0.8)
        self.play(
            *[
                MoveAlongPath(
                    slider,
                    Line(ray.point_from_proportion(0.28), ray.point_from_proportion(0.84)),
                )
                for slider, ray in zip(sliders, rays_1)
            ],
            run_time=2.1,
        )
        ambiguity = Text(
            "một hướng nhìn · nhiều độ sâu khả dĩ",
            font_size=23,
            color=PALETTE["muted"],
        ).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(ambiguity, shift=UP * 0.12))
        self.play(LaggedStart(*[Indicate(pixel, color=PALETTE["view_1"]) for pixel in pixels_1], lag_ratio=0.18))

        pixel_centers_2 = [
            image_2[3].get_center() + RIGHT * 0.1 + UP * 0.04,
            image_2[4].get_center() + DOWN * 0.04,
            image_2[2].get_center() + RIGHT * 0.42 + DOWN * 0.08,
        ]
        pixels_2 = VGroup(
            *[
                Square(
                    side_length=0.15,
                    stroke_color=PALETTE["ink"],
                    stroke_width=1.0,
                    fill_color=PALETTE["view_2"],
                    fill_opacity=1,
                ).move_to(center)
                for center in pixel_centers_2
            ]
        )
        rays_2 = VGroup()
        resolved = VGroup()
        for pixel, target in zip(pixels_2, target_centers):
            start = pixel.get_center()
            end = target + 0.52 * (target - start)
            rays_2.add(
                Line(
                    start,
                    end,
                    color=PALETTE["view_2"],
                    stroke_width=1.7,
                    stroke_opacity=0.62,
                )
            )
            resolved.add(Dot(target, radius=0.075, color=PALETTE["world"]))

        second_view = Text(
            "view thứ hai thu hẹp câu trả lời",
            font_size=24,
            color=PALETTE["view_2"],
        ).move_to(ambiguity)
        self.play(
            camera_2.animate.set_opacity(1),
            image_2.animate.set_opacity(1),
            framing_2.animate.set_opacity(1),
            Transform(ambiguity, second_view),
            run_time=1.2,
        )
        self.play(
            FadeIn(pixels_2),
            LaggedStart(*[Create(ray) for ray in rays_2], lag_ratio=0.14),
            run_time=1.4,
        )
        self.play(
            *[Transform(slider, point) for slider, point in zip(sliders, resolved)],
            FadeOut(ghosts),
            run_time=1.5,
        )
        self.play(LaggedStart(*[GrowFromCenter(point) for point in resolved], lag_ratio=0.14))

        positions = make_pointmap_positions(rows=6, cols=9)
        cloud_1 = make_point_cloud(
            positions,
            color=PALETTE["view_1"],
            radius=0.042,
            scale=0.82,
            opacity=0.88,
        ).move_to(world)
        cloud_2 = make_point_cloud(
            positions,
            color=PALETTE["view_2"],
            radius=0.034,
            scale=0.82,
            opacity=0.62,
        ).move_to(world).shift(RIGHT * 0.045 + UP * 0.025)
        self.play(
            world.animate.set_opacity(0.14),
            LaggedStart(*[FadeIn(dot, scale=0.35) for dot in cloud_1], lag_ratio=0.014),
            LaggedStart(*[FadeIn(dot, scale=0.35) for dot in cloud_2], lag_ratio=0.014),
            run_time=2.3,
        )
        self.play(
            FadeOut(
                VGroup(
                    camera_1,
                    camera_2,
                    image_1,
                    image_2,
                    framing_1,
                    framing_2,
                    pixels_1,
                    pixels_2,
                    rays_1,
                    rays_2,
                    sliders,
                    resolved,
                    world_tag,
                    question,
                    ambiguity,
                    world,
                )
            ),
            VGroup(cloud_1, cloud_2).animate.shift(RIGHT * 2.05).scale(1.18).rotate(0.12),
            run_time=1.5,
        )

        title = Text(
            "DUSt3R",
            font_size=73,
            color=PALETTE["ink"],
            weight="BOLD",
        ).move_to(LEFT * 3.35 + UP * 0.35)
        thesis = Text(
            "dự đoán geometry trước",
            font_size=28,
            color=PALETTE["world"],
        ).next_to(title, DOWN, aligned_edge=LEFT, buff=0.18)
        underline = Line(
            title.get_corner(DOWN + LEFT),
            title.get_corner(DOWN + RIGHT),
            color=PALETTE["view_1"],
            stroke_width=4,
        ).next_to(title, DOWN, buff=0.08)
        self.play(
            FadeIn(title, shift=UP * 0.18),
            Create(underline),
            FadeIn(thesis, shift=UP * 0.12),
            VGroup(cloud_1, cloud_2).animate.rotate(-0.22),
            run_time=1.6,
        )
        self.wait(1.3)
        self.play(FadeOut(VGroup(title, thesis, underline, cloud_1, cloud_2)), run_time=0.8)
