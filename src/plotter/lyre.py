"""Lyre フレーム本体の形状生成。

リラ（古代ギリシャの竪琴）状の曲線フレーム。

構造:
- ペデスタル (角丸の長方形板)
- 2 本の curved arm: 2D プロファイル (XZ 平面) を Y 方向に extrude
- 6 本のワイヤ穴: X 軸方向のシリンダーで全幅貫通

座標系:
- 原点: ペデスタル底面中央
- X: 幅方向 (左右対称)
- Y: 奥行方向 (フレーム厚み)
- Z: 高さ方向
"""

from build123d import (
    BuildLine,
    BuildSketch,
    Compound,
    Cylinder,
    Line,
    Part,
    Plane,
    Pos,
    RectangleRounded,
    Rot,
    Spline,
    extrude,
    make_face,
)

from plotter.params import Params
from plotter.params import params as default_params


def _build_left_arm_profile(p: Params) -> tuple[tuple[float, float], ...]:
    """左アームのプロファイル制御点 6 つを返す。

    左アームは X<0 側、ペデスタル上端から立ち上がり、上に向かって外側に広がる。
    返り値は (X, Z) のタプル × 6。
    """
    half_ped = p.lyre_pedestal_width / 2
    arm_t = p.lyre_arm_thickness
    h = p.lyre_height
    ped_top = p.lyre_pedestal_height
    mid_z = h * 0.55

    return (
        (-half_ped, ped_top),  # bottom_outer
        (-half_ped - 8.0, mid_z),  # mid_outer
        (-p.lyre_width / 2, h),  # top_outer
        (-p.lyre_width / 2 + arm_t * 0.7, h - arm_t * 0.3),  # top_inner
        (-half_ped + arm_t + 4.0, mid_z),  # mid_inner
        (-half_ped + arm_t, ped_top),  # bottom_inner
    )


def _build_arm(p: Params, mirror: bool = False) -> Part:
    """1 本のアームを 2D プロファイル + extrude で生成する。

    BuildSketch を介さず BuildLine → make_face → extrude の順で処理する。
    BuildSketch(Plane.XZ) 経由だと面が Z 負方向に反転するため直接 make_face を使用。
    """
    points = _build_left_arm_profile(p)
    if mirror:
        points = tuple((-x, z) for x, z in points)

    bottom_outer, mid_outer, top_outer, top_inner, mid_inner, bottom_inner = points

    with BuildLine(Plane.XZ) as outline:
        Spline(bottom_outer, mid_outer, top_outer)
        Line(top_outer, top_inner)
        Spline(top_inner, mid_inner, bottom_inner)
        Line(bottom_inner, bottom_outer)

    # BuildSketch を介すと XZ 平面で面が Z 負方向に反転するため直接 make_face を使用
    face = make_face(outline.line)
    arm = extrude(face, amount=p.lyre_depth, dir=(0, 1, 0), both=True)
    return arm


def make_lyre(p: Params = default_params) -> Part:
    """Lyre フレームを単一の Part として返す。"""
    # === ペデスタル ===
    with BuildSketch() as ped_sk:
        RectangleRounded(
            p.lyre_pedestal_width,
            p.lyre_pedestal_depth,
            p.lyre_pedestal_corner_radius,
        )
    pedestal = extrude(ped_sk.sketch, amount=p.lyre_pedestal_height)

    # === 左右アーム ===
    left = _build_arm(p, mirror=False)
    right = _build_arm(p, mirror=True)

    body = pedestal.fuse(left).fuse(right)

    # === ワイヤ穴: 各 Z で X 軸方向のシリンダーをフレーム全幅貫通 ===
    spacing = (p.wire_top_z - p.wire_bottom_z) / (p.wire_count - 1)
    cylinder_length = p.lyre_width + 4.0
    for i in range(p.wire_count):
        z = p.wire_bottom_z + i * spacing
        # Z 軸 Cylinder を Y 軸まわり 90° 回転して X 軸シリンダーにする
        hole = (
            Pos(0, 0, z)
            * Rot(0, 90, 0)
            * Cylinder(
                radius=p.wire_hole_diameter / 2,
                height=cylinder_length,
            )
        )
        body = body - hole

    # Solid を Part 型に変換して返す
    # Part(solid.wrapped) では volume=0 になるため Compound 経由でラップする
    return Part(Compound([body]).wrapped)
