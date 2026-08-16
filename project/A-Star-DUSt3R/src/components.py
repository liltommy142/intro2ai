from manim import *
import numpy as np

from theme import *


# ============================================================
# Helpers
# ============================================================

def glow_dot(
    point=ORIGIN,
    color=CYAN,
    radius=0.07,
    glow_radius=0.28,
):
    """
    Fake glow bằng nhiều circle opacity thấp.
    Dùng được với Cairo renderer, không cần shader riêng.
    """

    glow = VGroup()

    for r, opacity in [
        (glow_radius, 0.035),
        (glow_radius * 0.72, 0.06),
        (glow_radius * 0.48, 0.10),
    ]:
        glow.add(
            Circle(
                radius=r,
                stroke_width=0,
                fill_color=color,
                fill_opacity=opacity,
            ).move_to(point)
        )

    core = Dot(
        point,
        radius=radius,
        color=color,
    )

    glow.add(core)

    return glow


def glow_line(
    start,
    end,
    color=CYAN,
    width=2.4,
):
    """
    Line chính + 2 line mờ phía dưới để tạo cảm giác phát sáng.
    """

    return VGroup(
        Line(
            start,
            end,
            color=color,
            stroke_width=9,
            stroke_opacity=0.035,
        ),
        Line(
            start,
            end,
            color=color,
            stroke_width=5,
            stroke_opacity=0.08,
        ),
        Line(
            start,
            end,
            color=color,
            stroke_width=width,
            stroke_opacity=0.95,
        ),
    )


# ============================================================
# Modern photo card
# ============================================================

def room_photo_card(
    width=4.5,
    height=2.9,
    variant=0,
):
    """
    Một 'ảnh căn phòng' stylized.
    Không phụ thuộc asset bên ngoài.
    """

    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.12,
        stroke_color="#31394A",
        stroke_width=1.2,
        fill_color=SURFACE,
        fill_opacity=1,
    )

    # clipping thật khá phiền trong Manim,
    # nên toàn bộ geometry giữ trong bounds frame.

    left = -width / 2
    right = width / 2
    top = height / 2
    bottom = -height / 2

    vanishing = np.array([
        0.55 if variant == 0 else -0.45,
        0.20,
        0,
    ])

    floor_horizon = 0.30

    # Back wall
    wall = Polygon(
        [left + 0.18, bottom + 0.18, 0],
        [right - 0.18, bottom + 0.18, 0],
        [right - 0.18, top - 0.18, 0],
        [left + 0.18, top - 0.18, 0],
        fill_color="#141925",
        fill_opacity=1,
        stroke_width=0,
    )

    # Perspective floor
    floor = Polygon(
        [left + 0.18, bottom + 0.18, 0],
        [right - 0.18, bottom + 0.18, 0],
        [1.25 + vanishing[0], floor_horizon, 0],
        [-1.20 + vanishing[0], floor_horizon, 0],
        fill_color="#1B2130",
        fill_opacity=1,
        stroke_width=0,
    )

    horizon = Line(
        [left + 0.2, floor_horizon, 0],
        [right - 0.2, floor_horizon, 0],
        color="#30384A",
        stroke_width=1,
    )

    perspective_lines = VGroup()

    for x in np.linspace(left + 0.25, right - 0.25, 7):
        perspective_lines.add(
            Line(
                [x, bottom + 0.2, 0],
                vanishing,
                stroke_color="#293143",
                stroke_width=0.8,
                stroke_opacity=0.65,
            )
        )

    # Furniture shapes
    sofa = RoundedRectangle(
        width=1.45,
        height=0.55,
        corner_radius=0.08,
        stroke_width=0,
        fill_color="#526079",
        fill_opacity=0.62,
    )

    sofa.move_to(
        np.array([
            -0.75 if variant == 0 else -0.35,
            -0.35,
            0,
        ])
    )

    sofa_back = RoundedRectangle(
        width=1.35,
        height=0.45,
        corner_radius=0.07,
        stroke_width=0,
        fill_color="#65728C",
        fill_opacity=0.38,
    ).next_to(sofa, UP, buff=-0.06)

    table = Rectangle(
        width=0.8,
        height=0.28,
        fill_color="#8B7697",
        fill_opacity=0.6,
        stroke_width=0,
    )

    table.move_to(
        np.array([
            0.75 if variant == 0 else 0.95,
            -0.57,
            0,
        ])
    )

    window = Rectangle(
        width=0.95,
        height=0.72,
        stroke_color=CYAN,
        stroke_width=1,
        stroke_opacity=0.45,
        fill_color=CYAN,
        fill_opacity=0.035,
    ).move_to(
        np.array([
            1.15 if variant == 0 else 0.85,
            0.75,
            0,
        ])
    )

    content = VGroup(
        wall,
        floor,
        horizon,
        perspective_lines,
        sofa,
        sofa_back,
        table,
        window,
    )

    content.move_to(frame)

    return VGroup(frame, content)


# ============================================================
# Image plane
# ============================================================

def image_plane_3d(
    width=4.8,
    height=3.0,
    color=CYAN,
):
    """
    Image plane tối giản để dùng trong ThreeDScene.
    """

    border = Rectangle(
        width=width,
        height=height,
        stroke_color=color,
        stroke_width=1.4,
        stroke_opacity=0.65,
        fill_color=color,
        fill_opacity=0.018,
    )

    grid = VGroup()

    cols = 12
    rows = 8

    for i in range(1, cols):
        x = -width / 2 + width * i / cols

        grid.add(
            Line(
                [x, -height / 2, 0],
                [x, height / 2, 0],
                stroke_color=GRID,
                stroke_width=0.6,
                stroke_opacity=0.32,
            )
        )

    for j in range(1, rows):
        y = -height / 2 + height * j / rows

        grid.add(
            Line(
                [-width / 2, y, 0],
                [width / 2, y, 0],
                stroke_color=GRID,
                stroke_width=0.6,
                stroke_opacity=0.32,
            )
        )

    return VGroup(border, grid)


# ============================================================
# Camera frustum
# ============================================================

def camera_frustum(
    center=np.array([-4.0, 0.0, 0.0]),
    image_x=-2.2,
    half_width=1.15,
    half_height=0.75,
    color=CYAN,
):
    """
    Camera theo kiểu computer vision:
    optical center + image plane + frustum.
    """

    c = np.array(center, dtype=float)

    p1 = np.array([image_x, half_height, half_width])
    p2 = np.array([image_x, half_height, -half_width])
    p3 = np.array([image_x, -half_height, half_width])
    p4 = np.array([image_x, -half_height, -half_width])

    center_dot = glow_dot(
        c,
        color=color,
        radius=0.055,
        glow_radius=0.20,
    )

    edges = VGroup(
        Line(c, p1),
        Line(c, p2),
        Line(c, p3),
        Line(c, p4),
    )

    edges.set_stroke(
        color=color,
        width=1.3,
        opacity=0.55,
    )

    plane_edges = VGroup(
        Line(p1, p2),
        Line(p2, p4),
        Line(p4, p3),
        Line(p3, p1),
    )

    plane_edges.set_stroke(
        color=color,
        width=1,
        opacity=0.35,
    )

    return VGroup(
        edges,
        plane_edges,
        center_dot,
    )


# ============================================================
# Pixel
# ============================================================

def luminous_pixel(
    point,
    color=CYAN,
):
    square = Square(
        side_length=0.16,
        stroke_color=color,
        stroke_width=1.2,
        fill_color=color,
        fill_opacity=0.95,
    )

    square.move_to(point)

    halo1 = Square(
        side_length=0.27,
        stroke_color=color,
        stroke_width=1,
        stroke_opacity=0.16,
    ).move_to(point)

    halo2 = Square(
        side_length=0.42,
        stroke_color=color,
        stroke_width=1,
        stroke_opacity=0.06,
    ).move_to(point)

    return VGroup(
        halo2,
        halo1,
        square,
    )   