"""Shared visual language for the DUSt3R explainer.

The video deliberately uses generated vector geometry instead of screenshots from
the paper.  A colour is attached to each view and survives the whole journey
from pixel, through token, to 3D point.
"""

from __future__ import annotations

from math import cos, sin
from typing import Iterable, Sequence

import numpy as np
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Dot,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Square,
    Text,
    Triangle,
    VGroup,
)


PALETTE = {
    "background": "#0B0F14",
    "surface": "#111923",
    "surface_2": "#182431",
    "ink": "#E8E3D8",
    "muted": "#8393A7",
    "view_1": "#42C6FF",
    "view_2": "#FFB84D",
    "pose": "#FF5CA8",
    "confidence": "#8BE35B",
    "low_confidence": "#C85C5C",
    "pair_frame": "#9B7BFF",
    "world": "#FFD166",
}


def mix_hex(first: str, second: str, amount: float) -> str:
    """Return a deterministic RGB interpolation accepted by Manim."""
    amount = max(0.0, min(1.0, amount))
    rgb_a = tuple(int(first[index : index + 2], 16) for index in (1, 3, 5))
    rgb_b = tuple(int(second[index : index + 2], 16) for index in (1, 3, 5))
    mixed = tuple(round(a + (b - a) * amount) for a, b in zip(rgb_a, rgb_b))
    return "#" + "".join(f"{value:02X}" for value in mixed)


def make_pixel_grid(
    rows: int = 5,
    cols: int = 7,
    cell_size: float = 0.32,
    *,
    view_color: str = PALETTE["view_1"],
    variant: int = 0,
) -> VGroup:
    """Create a small synthetic image whose cells can morph into 3D points."""
    cells = VGroup()
    for row in range(rows):
        for col in range(cols):
            wave = 0.5 + 0.25 * sin((col + variant) * 0.9) + 0.2 * cos(row * 1.2)
            color = mix_hex(PALETTE["surface_2"], view_color, wave)
            if row >= rows - 2:
                color = mix_hex("#243223", view_color, 0.24 + 0.08 * col)
            if 1 <= row <= rows - 2 and col in {cols // 2, cols // 2 + 1}:
                color = mix_hex("#C95A4D", view_color, 0.13)
            cell = Square(
                side_length=cell_size,
                stroke_color=PALETTE["background"],
                stroke_width=0.7,
                fill_color=color,
                fill_opacity=1,
            )
            cell.move_to(
                np.array(
                    [
                        (col - (cols - 1) / 2) * cell_size,
                        ((rows - 1) / 2 - row) * cell_size,
                        0,
                    ]
                )
            )
            cell.pixel_index = (row, col)  # type: ignore[attr-defined]
            cells.add(cell)
    return cells


def make_pointmap_positions(rows: int = 5, cols: int = 7) -> list[np.ndarray]:
    """Synthetic W×H×3 surface with a visible depth variation."""
    points: list[np.ndarray] = []
    for row in range(rows):
        for col in range(cols):
            x = (col - (cols - 1) / 2) * 0.52
            y = ((rows - 1) / 2 - row) * 0.42
            z = 0.36 * sin(col * 0.72) + 0.22 * cos(row * 1.03)
            if 1 <= row <= rows - 2 and col in {cols // 2, cols // 2 + 1}:
                z += 0.72
            points.append(np.array([x, y, z]))
    return points


def project_iso(point: Sequence[float], scale: float = 1.0) -> np.ndarray:
    """Project a synthetic 3D coordinate into the 2D Manim frame."""
    x, y, z = point
    return np.array([(x + 0.48 * z) * scale, (y + 0.27 * z) * scale, 0.0])


def make_point_cloud(
    positions: Iterable[Sequence[float]],
    *,
    color: str = PALETTE["view_1"],
    radius: float = 0.045,
    scale: float = 1.0,
    opacity: float = 1.0,
) -> VGroup:
    dots = VGroup()
    for index, point in enumerate(positions):
        shade = mix_hex(color, PALETTE["ink"], 0.18 * ((index % 5) / 4))
        dots.add(
            Dot(
                project_iso(point, scale=scale),
                radius=radius,
                color=shade,
                fill_opacity=opacity,
            )
        )
    return dots


def make_image_panel(
    label: str,
    *,
    accent: str,
    variant: int = 0,
    width: float = 3.3,
    height: float = 2.25,
) -> VGroup:
    """A self-contained, generated toy image with a persistent view colour."""
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.15,
        stroke_color=accent,
        stroke_width=2.2,
        fill_color=PALETTE["surface"],
        fill_opacity=1,
    )
    sky = Rectangle(
        width=width - 0.18,
        height=(height - 0.18) * 0.58,
        stroke_width=0,
        fill_color=mix_hex(PALETTE["surface_2"], accent, 0.18),
        fill_opacity=1,
    ).align_to(frame, UP).shift(DOWN * 0.09)
    ground = Polygon(
        frame.get_corner(DOWN + LEFT) + np.array([0.09, 0.09, 0]),
        frame.get_corner(DOWN + RIGHT) + np.array([-0.09, 0.09, 0]),
        frame.get_center() + DOWN * 0.05,
        stroke_width=0,
        fill_color="#263226",
        fill_opacity=1,
    )
    cube_shift = LEFT * (0.35 - 0.3 * variant)
    cube = Square(
        side_length=0.62,
        stroke_color="#F4A59A",
        stroke_width=1.3,
        fill_color="#B94E48",
        fill_opacity=0.95,
    ).move_to(frame.get_center() + DOWN * 0.28 + cube_shift)
    column = Rectangle(
        width=0.34,
        height=0.95,
        stroke_color=PALETTE["world"],
        stroke_width=1.2,
        fill_color="#9A7728",
        fill_opacity=0.95,
    ).move_to(frame.get_center() + RIGHT * (0.75 - 0.2 * variant) + DOWN * 0.08)
    tag = label_pill(label, accent=accent, font_size=21)
    tag.next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
    return VGroup(frame, sky, ground, cube, column, tag)


def make_camera(accent: str, *, mirrored: bool = False, scale: float = 1.0) -> VGroup:
    """Small side-view camera and translucent field of view."""
    direction = -1 if mirrored else 1
    body = RoundedRectangle(
        width=0.66,
        height=0.46,
        corner_radius=0.08,
        stroke_color=accent,
        stroke_width=2,
        fill_color=PALETTE["surface_2"],
        fill_opacity=1,
    )
    lens = Polygon(
        np.array([0.33 * direction, 0.17, 0]),
        np.array([0.61 * direction, 0.28, 0]),
        np.array([0.61 * direction, -0.28, 0]),
        np.array([0.33 * direction, -0.17, 0]),
        stroke_color=accent,
        stroke_width=1.7,
        fill_color=accent,
        fill_opacity=0.18,
    )
    sensor = Line(UP * 0.13, DOWN * 0.13, color=accent, stroke_width=3).shift(
        RIGHT * 0.18 * direction
    )
    return VGroup(body, lens, sensor).scale(scale)


def make_axes(accent: str, *, length: float = 0.9, labels: bool = False) -> VGroup:
    origin = Dot(radius=0.035, color=accent)
    x_axis = Line(ORIGIN, RIGHT * length, color=accent, stroke_width=2.2)
    y_axis = Line(ORIGIN, UP * length * 0.75, color=accent, stroke_width=2.2)
    z_axis = Line(ORIGIN, (RIGHT + UP) * length * 0.5, color=accent, stroke_width=2.2)
    axes = VGroup(origin, x_axis, y_axis, z_axis)
    if labels:
        axes.add(
            Text("x", font_size=18, color=accent).next_to(x_axis.get_end(), RIGHT, buff=0.05),
            Text("y", font_size=18, color=accent).next_to(y_axis.get_end(), UP, buff=0.05),
            Text("z", font_size=18, color=accent).next_to(z_axis.get_end(), UP, buff=0.05),
        )
    return axes


def make_token_grid(accent: str, rows: int = 3, cols: int = 5) -> VGroup:
    tokens = VGroup()
    for row in range(rows):
        for col in range(cols):
            token = RoundedRectangle(
                width=0.26,
                height=0.26,
                corner_radius=0.05,
                stroke_color=accent,
                stroke_width=1,
                fill_color=mix_hex(PALETTE["surface_2"], accent, 0.25 + 0.08 * ((row + col) % 3)),
                fill_opacity=1,
            )
            token.move_to(np.array([(col - 2) * 0.3, (1 - row) * 0.3, 0]))
            tokens.add(token)
    return tokens


def label_pill(
    text: str,
    *,
    accent: str = PALETTE["ink"],
    font_size: int = 24,
) -> VGroup:
    label = Text(text, font_size=font_size, color=accent)
    shell = RoundedRectangle(
        width=label.width + 0.34,
        height=label.height + 0.18,
        corner_radius=0.12,
        stroke_color=accent,
        stroke_width=1.2,
        fill_color=PALETTE["surface"],
        fill_opacity=0.94,
    )
    label.move_to(shell)
    return VGroup(shell, label)


def chapter_title(kicker: str, title: str, *, accent: str) -> VGroup:
    small = Text(kicker.upper(), font_size=18, color=accent, weight="BOLD")
    headline = Text(title, font_size=38, color=PALETTE["ink"], weight="BOLD")
    group = VGroup(small, headline).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    rule = Line(LEFT * 0.4, RIGHT * 0.4, color=accent, stroke_width=4)
    rule.next_to(group, LEFT, buff=0.2)
    return VGroup(rule, group)


def confidence_halo(point: Dot, level: float) -> Circle:
    color = mix_hex(PALETTE["low_confidence"], PALETTE["confidence"], level)
    return Circle(
        radius=point.radius * (2.2 + level),
        stroke_color=color,
        stroke_width=1.3,
        stroke_opacity=0.45 + 0.4 * level,
        fill_opacity=0,
    ).move_to(point)


def make_benchmark_glyph(label: str, value: str, caption: str, *, accent: str) -> VGroup:
    ring = Circle(
        radius=0.78,
        stroke_color=PALETTE["surface_2"],
        stroke_width=11,
    )
    arc_hint = Circle(
        radius=0.78,
        stroke_color=accent,
        stroke_width=5,
        stroke_opacity=0.95,
    )
    number = Text(value, font_size=31, color=PALETTE["ink"], weight="BOLD").move_to(ring)
    name = Text(label, font_size=22, color=accent, weight="BOLD").next_to(ring, UP, buff=0.24)
    note = Text(caption, font_size=17, color=PALETTE["muted"]).next_to(ring, DOWN, buff=0.2)
    return VGroup(ring, arc_hint, number, name, note)


def toy_world() -> VGroup:
    """The hero object used throughout the film."""
    floor = Polygon(
        np.array([-2.2, -0.9, 0]),
        np.array([1.9, -0.9, 0]),
        np.array([2.55, 0.45, 0]),
        np.array([-1.55, 0.45, 0]),
        stroke_color=PALETTE["muted"],
        stroke_width=1.1,
        fill_color="#18211A",
        fill_opacity=0.65,
    )
    cube = Square(
        side_length=0.86,
        stroke_color="#F4A59A",
        stroke_width=2,
        fill_color="#B94E48",
        fill_opacity=0.85,
    ).move_to(LEFT * 0.55 + DOWN * 0.25)
    top = Polygon(
        cube.get_corner(UP + LEFT),
        cube.get_corner(UP + RIGHT),
        cube.get_corner(UP + RIGHT) + np.array([0.24, 0.18, 0]),
        cube.get_corner(UP + LEFT) + np.array([0.24, 0.18, 0]),
        stroke_color="#F4A59A",
        fill_color="#D66A60",
        fill_opacity=0.9,
    )
    pillar = Rectangle(
        width=0.43,
        height=1.35,
        stroke_color=PALETTE["world"],
        stroke_width=2,
        fill_color="#977324",
        fill_opacity=0.9,
    ).move_to(RIGHT * 0.75 + DOWN * 0.05)
    return VGroup(floor, cube, top, pillar)
