"""本体パネル（背板 + 棚 + リップ + ホゾ）の形状生成。

座標系:
- 原点: 背板下端中央、Z=0 が背板裏面
- X: 幅方向 (panel_width)
- Y: 高さ方向 (panel_height、Y=0 が背板下端、Y<0 にホゾが伸びる)
- Z: 奥行方向 (Z=0 が背板裏面、+Z 側に棚・リップが突き出る)
"""

from build123d import Box, Compound, Part, Pos

from plotter.params import Params
from plotter.params import params as default_params


def make_body(p: Params = default_params) -> Part:
    """本体パネルを単一の Part として返す。

    各形状を Pos でオフセット後に連続 fuse して単一ソリッドにし、
    Part(solid.wrapped) で build123d の Part 型に変換して返す。
    build123d 0.10.0 では Box + Box が Solid を返すため、
    BuildPart + add() パターンではなく fuse チェーンを採用している。
    """
    # === 背板 ===
    body = Pos(0, p.panel_height / 2, p.panel_thickness / 2) * Box(
        p.panel_width, p.panel_height, p.panel_thickness
    )

    # === 仕切り×shelf_count + リップ×shelf_count ===
    row_pitch = (p.panel_height - 2 * p.panel_thickness) / p.shelf_count
    shelf_front_z = p.panel_thickness + p.shelf_depth
    for i in range(p.shelf_count):
        y_div_bottom = p.panel_thickness + i * row_pitch
        # 仕切り
        divider = Pos(
            0,
            y_div_bottom + p.shelf_divider_thickness / 2,
            p.panel_thickness + p.shelf_depth / 2,
        ) * Box(p.panel_width, p.shelf_divider_thickness, p.shelf_depth)
        body = body.fuse(divider)
        # リップ（仕切り上面に立ち、棚前端に寄せる）
        lip = Pos(
            0,
            y_div_bottom + p.shelf_divider_thickness + p.shelf_lip_height / 2,
            shelf_front_z - p.shelf_lip_thickness / 2,
        ) * Box(p.panel_width, p.shelf_lip_height, p.shelf_lip_thickness)
        body = body.fuse(lip)

    # === ホゾ×tenon_count（X 等間隔、Y<0 に突出、Z 中心配置）===
    # tenon_count==1 はパネル中央に1本配置、>=2 は両端から等間隔で配置。
    for j in range(p.tenon_count):
        if p.tenon_count == 1:
            x_center = 0.0
        else:
            pitch = (p.panel_width - p.tenon_width) / (p.tenon_count - 1)
            x_center = -p.panel_width / 2 + p.tenon_width / 2 + j * pitch
        tenon = Pos(x_center, -p.tenon_height / 2, p.panel_thickness / 2) * Box(
            p.tenon_width, p.tenon_height, p.tenon_thickness
        )
        body = body.fuse(tenon)

    # Solid を Part 型に変換して返す
    # Part(solid.wrapped) では volume=0 になるため Compound 経由でラップする
    return Part(Compound([body]).wrapped)
