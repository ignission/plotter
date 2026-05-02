"""土台（base）の形状生成。

座標系:
- X: 幅方向
- Y: 奥行方向 (Y=0 が前端)
- Z: 高さ方向 (Z=0 が底面)

構造:
- 前部平板 + 背部厳部（傾斜上面）+ 前リップ + 角度付きホゾ穴×N
"""

import math

from build123d import Box, Compound, Part, Pos, Rot

from plotter.params import Params
from plotter.params import params as default_params


def make_base(p: Params = default_params) -> Part:
    """土台を単一の Part として返す。

    前部平板（Y=0..flat_depth）と背部厳部（Y=flat_depth..base_depth）を fuse し、
    傾斜カットで ridge 上面を 15° 傾ける。前リップと角度付きホゾ穴を追加する。
    """
    angle_offset_deg = 90 - p.panel_angle  # = 15°
    angle_offset_rad = math.radians(angle_offset_deg)
    flat_depth = p.base_depth - p.base_ridge_depth  # = 30mm

    # === flat front: Y=0..flat_depth, Z=0..base_thickness ===
    # 土台自体の幅は base_width。本体パネルの panel_width とは独立に変えられる。
    base = Pos(0, flat_depth / 2, p.base_thickness / 2) * Box(
        p.base_width, flat_depth, p.base_thickness
    )

    # === ridge block: Y=flat_depth..base_depth, Z=0..base_ridge_height ===
    ridge_block = Pos(
        0,
        flat_depth + p.base_ridge_depth / 2,
        p.base_ridge_height / 2,
    ) * Box(p.base_width, p.base_ridge_depth, p.base_ridge_height)
    base = base.fuse(ridge_block)

    # === 傾斜カット: ridge 上面を 15° 前下がりに切り落とす ===
    # ridge 前端 (Y=flat_depth, Z=base_ridge_height) を通る平面を基準に
    # X 軸まわり -angle_offset_deg 回転した大きな直方体で上面を cut する。
    # cutter の中心は回転軸から +Y, +Z 方向に大きく離す。
    cutter_size = max(p.base_width, p.base_depth, p.base_ridge_height) * 4
    # 回転前の cutter: Y>0, Z>0 の大きな箱（回転軸の前端上角から始まる）
    # 回転後に ridge 前端上角 (Y=flat_depth, Z=base_ridge_height) 付近から
    # 斜め後ろに伸びて上面を切り落とす
    cutter = (
        Pos(0, flat_depth, p.base_ridge_height)
        * Rot(-angle_offset_deg, 0, 0)
        * Pos(0, cutter_size / 2, cutter_size / 2)
        * Box(cutter_size, cutter_size, cutter_size)
    )
    base = base.cut(cutter)

    # === front lip: Y=0..base_front_lip_thickness, Z=base_thickness..(+base_front_lip_height) ===
    lip = Pos(
        0,
        p.base_front_lip_thickness / 2,
        p.base_thickness + p.base_front_lip_height / 2,
    ) * Box(p.base_width, p.base_front_lip_thickness, p.base_front_lip_height)
    base = base.fuse(lip)

    # === mortise holes × tenon_count ===
    # ホゾ穴は傾斜面に垂直な方向 (0, -sin(15°), -cos(15°)) に深さ hole_l で掘る。
    # Box の長手方向（Z 軸）を (0, -sin, -cos) に揃えるため X 軸まわり (180 - 15°) = 165° 回転する。
    hole_w = p.tenon_width + p.mortise_clearance  # 14.2mm
    hole_t = p.tenon_thickness + p.mortise_clearance  # 2.2mm
    hole_l = p.tenon_height + 2.0  # 22.0mm

    # entry 点: ridge 中央高さの傾斜面上
    entry_y = p.base_depth - p.base_ridge_depth / 2
    entry_z = p.base_ridge_height - (p.base_ridge_depth / 2) * math.tan(angle_offset_rad)
    # 穴底: entry 点から穴の方向に hole_l 進んだ点
    bottom_y = entry_y - hole_l * math.sin(angle_offset_rad)
    bottom_z = entry_z - hole_l * math.cos(angle_offset_rad)
    # 穴の中心（mid 点）
    mid_y = (entry_y + bottom_y) / 2
    mid_z = (entry_z + bottom_z) / 2

    # X 方向の配置（body のホゾと同じ計算）
    if p.tenon_count == 1:
        x_centers = [0.0]
    else:
        pitch = (p.panel_width - p.tenon_width) / (p.tenon_count - 1)
        x_centers = [
            -p.panel_width / 2 + p.tenon_width / 2 + j * pitch for j in range(p.tenon_count)
        ]

    rotation_x_deg = 180 - angle_offset_deg  # = 165°
    for x_c in x_centers:
        hole = Pos(x_c, mid_y, mid_z) * Rot(rotation_x_deg, 0, 0) * Box(hole_w, hole_t, hole_l)
        base = base.cut(hole)

    # Solid を Part 型に変換して返す（body.py と同じパターン）
    return Part(Compound([base]).wrapped)
