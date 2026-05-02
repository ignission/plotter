"""Drawer body の形状生成。

ウェッジ内部にスライドインする収納ドロワー。前面に指掛け recess、
内部にカード収納空間を持つ。

座標系（部品ローカル）:
- X: 幅方向（中心 0）
- Y: 前後方向（Y=0 が前面開口、Y=drawer_depth が後面）
- Z: 高さ方向（Z=0 が底面）
"""

from build123d import Box, Cylinder, Pos, Rotation
from build123d.topology import Compound, Part

from plotter.params import Params
from plotter.params import params as default_params


def make_drawer(p: Params = default_params) -> Part:
    """ドロワーを単一の Part として返す。

    外形寸法: drawer_width × drawer_depth × drawer_height
    内部空洞: 前面開口（Y=0 側は壁なし）、後面・左右・上下に drawer_wall_thickness の壁
    前面指掛け recess: 前面中央に drawer_pull_diameter の円形くり抜き
    """
    w = p.drawer_width
    d = p.drawer_depth
    h = p.drawer_height
    wt = p.drawer_wall_thickness

    # === 外殻 ===
    # Box の中心は原点に来る → Pos でオフセット
    body = Pos(0, d / 2, h / 2) * Box(w, d, h)

    # === 内部空洞（前面開口） ===
    # 前面 (Y=0) は開口するため内部空洞は Y=0..d-wt の範囲
    # 左右・上下は wt の壁を残す
    inner_w = w - 2 * wt
    inner_d = d - wt  # 前面は開口（壁なし）、後面のみ wt の壁
    inner_h = h - 2 * wt
    # inner の Y 中心: Y=0 から Y=(d-wt) なので中心は (d-wt)/2
    inner_y_center = (d - wt) / 2
    inner_z_center = h / 2
    inner = Pos(0, inner_y_center, inner_z_center) * Box(inner_w, inner_d, inner_h)
    body = body - inner

    # === 前面の指掛け recess（円形くり抜き） ===
    # Cylinder のデフォルトは Z 方向、Rotation(90,0,0) で Y 方向に向く
    # 前面 (Y=0) の中央から内側 pull_depth 分掘る
    # 円柱の中心を Y=0 に置くと Y=-pull_depth/2..+pull_depth/2 の範囲に切り込む
    # → 前面から pull_depth 分内部方向に掘るには中心を Y=-pull_depth/2 に配置
    # （body は Y=0..d なので Y=0 から +Y 方向に掘る）
    pull_z_center = h / 2  # 高さ方向中央
    pull = (
        Pos(0, p.drawer_pull_depth / 2, pull_z_center)
        * Rotation(90, 0, 0)
        * Cylinder(radius=p.drawer_pull_diameter / 2, height=p.drawer_pull_depth)
    )
    body = body - pull

    # Boolean 演算後は Compound になるため Part に変換して返す
    if isinstance(body, Compound):
        return Part(body.wrapped)
    return body
