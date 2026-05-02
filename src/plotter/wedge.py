"""Wedge body の形状生成。

Apple Magic Keyboard 型の薄いウェッジスラブ。上面が緩く傾斜し、6 本の
長スロット（列の仕切り無し）が上面に切られている。カードを上から差し込んで
使う。標準カード(30mm)とワイドカード(60mm)を任意に混在可能、スロット内を
スライドして自由に並び替え。

座標系:
- 原点: 底面前縁中央 (X=0 中心、Y=0 前縁、Z=0 底)
- X: 幅方向 (-wedge_width/2 .. +wedge_width/2)
- Y: 奥行 (0 .. wedge_depth、Y=0 が前縁、Y=depth が後縁)
- Z: 高さ (0 が底、上面は前低後高の傾斜)
"""

import math

from build123d import (
    Axis,
    Box,
    BuildLine,
    BuildSketch,
    Plane,
    Polyline,
    Pos,
    Rotation,
    extrude,
    fillet,
    make_face,
)
from build123d.topology import Compound, Part

from plotter.params import Params
from plotter.params import params as default_params


def make_wedge(p: Params = default_params) -> Part:
    """Wedge body を単一の Part として返す。

    座標系:
    - X: 幅方向 (-wedge_width/2 .. +wedge_width/2)
    - Y: 奥行 (0 .. wedge_depth)
    - Z: 高さ (0 .. wedge_back_thickness)
    """
    # === ウェッジ本体: 側面プロファイル (XZ 平面) を Y 方向に extrude ===
    # XZ 平面上: X = 奥行方向 (0..wedge_depth), Z = 高さ (front..back)
    # extrude 後に Z 軸 90° 回転して X=奥行 → Y=奥行 に変換
    with BuildLine(Plane.XZ) as profile:
        Polyline(
            (0, 0),
            (p.wedge_depth, 0),
            (p.wedge_depth, p.wedge_back_thickness),
            (0, p.wedge_front_thickness),
            close=True,
        )
    with BuildSketch(Plane.XZ) as sk:
        make_face(profile.line)
    body = extrude(sk.sketch, amount=p.wedge_width / 2, both=True)
    # X=奥行、Y=幅 → Z 軸 90° 回転で X=幅、Y=奥行 に入れ替え
    body = Rotation(0, 0, 90) * body

    # === 底面の稜線にフィレット ===
    # ポケット切り込み後は OCC が fillet を受け付けなくなるため先に適用する
    try:
        bottom_face = body.faces().sort_by(Axis.Z)[0]
        body = fillet(bottom_face.edges(), radius=p.wedge_fillet_radius)
    except Exception:  # noqa: BLE001
        pass  # フィレット失敗時はスキップしてフラットエッジのまま続行

    # === 傾斜上面の幾何 ===
    tilt_rad = math.atan2(p.wedge_back_thickness - p.wedge_front_thickness, p.wedge_depth)
    cos_t = math.cos(tilt_rad)
    sin_t = math.sin(tilt_rad)
    # body 内部向き法線（上面から Z 下方向）
    inward_dir = (0, sin_t, -cos_t)

    # === 6 本の長スロット（列仕切り無し、カードはスロット内をスライド可）===
    slot_length = p.card_slot_length  # X 方向のスロット長
    slot_thickness = p.card_thickness + p.card_slot_clearance  # 厚み方向 (face_vertical)
    slot_d = p.card_slot_pocket_depth  # 上面に対する垂直深さ

    for row in range(p.card_slot_rows):
        # 上面に沿った行方向距離（face_t）
        face_t = (row + 0.5) * p.card_slot_face_pitch
        # 上面座標 → world (Y, Z)
        y_world = face_t * cos_t
        z_world = p.wedge_front_thickness + face_t * sin_t

        # 傾斜面に沿った平面を定義し、長スロット Box を配置
        slot_plane = Plane(
            origin=(0, y_world, z_world),
            x_dir=(1, 0, 0),
            z_dir=inward_dir,
        )
        # Box(W, H, D): W=長さ(X), H=厚み(face_vertical), D=深さ(inward)
        slot = slot_plane * Pos(0, 0, slot_d / 2) * Box(slot_length, slot_thickness, slot_d)
        body = body - slot

    # === ドロワーキャビティ（前面開口、底面から drawer_floor_offset_z 上） ===
    # キャビティ幅: drawer_width + clearance, 奥行: drawer_depth + clearance
    # Z: drawer_floor_offset_z .. drawer_floor_offset_z + drawer_height + clearance
    cav_w = p.drawer_width + p.drawer_clearance
    cav_d = p.drawer_depth + p.drawer_clearance
    cav_h = p.drawer_height + p.drawer_clearance
    cav_z_center = p.drawer_floor_offset_z + cav_h / 2
    # Y 中心: キャビティは前面 (Y=0) から cav_d まで → 中心 = cav_d/2
    cav_y_center = cav_d / 2
    cavity = Pos(0, cav_y_center, cav_z_center) * Box(cav_w, cav_d, cav_h)
    body = body - cavity

    # Boolean 演算後は Compound になるため Part に変換して返す
    if isinstance(body, Compound):
        return Part(body.wrapped)
    return body
