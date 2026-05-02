"""Drawer body の形状生成。

ウェッジ内部にスライドインする収納ドロワー。前面に指掛け recess、
内部にカード収納空間を持つ。

座標系（部品ローカル）:
- X: 幅方向（中心 0）
- Y: 前後方向（Y=0 が前面開口、Y=drawer_depth が後面）
- Z: 高さ方向（Z=0 が底面）
"""

from build123d import Box, Pos, fillet
from build123d.topology import Compound, Part

from plotter.params import Params
from plotter.params import params as default_params


def make_drawer(p: Params = default_params) -> Part:
    """ドロワー（上面開口のトレイ）を単一の Part として返す。

    外形寸法: drawer_width × drawer_depth × drawer_height
    内部空洞: 上面開口（カードを上から取り出す）、前面・後面・左右・底に
    drawer_wall_thickness の壁。前面中央に指掛け recess（円形くり抜き）。

    押し込み時はウェッジ天井がドロワー上面の蓋になる。
    引き出し時は上が開いてカードが見える。
    """
    w = p.drawer_width
    d = p.drawer_depth
    h = p.drawer_height
    wt = p.drawer_wall_thickness

    # === 外殻 ===
    body = Pos(0, d / 2, h / 2) * Box(w, d, h)

    # === 内部空洞（上面開口） ===
    # 前後左右に wt の壁、底に wt の壁、上は開口（壁なし）
    inner_w = w - 2 * wt
    inner_d = d - 2 * wt
    # 上面開口: 内部 Box が上方向に飛び出すように、+1mm 余分に高くする
    inner_h = h - wt + 1.0
    inner_y_center = d / 2
    # 内部 Box の Z 中心: 底壁 wt の上から、上は body 上端を 1mm 突き抜ける
    # Z 範囲: wt から (h + 1.0) → 中心 = (wt + h + 1.0) / 2
    inner_z_center = (wt + h + 1.0) / 2
    inner = Pos(0, inner_y_center, inner_z_center) * Box(inner_w, inner_d, inner_h)
    body = body - inner

    # === 前面の取っ手バー（前方に突出） ===
    # 前面中央から外側 (Y<0) に protrusion 分突き出す。指がかかる立体的なバー。
    handle_y_center = -p.drawer_handle_protrusion / 2
    handle_z_center = h / 2
    handle = Pos(handle_y_center * 0 + 0, handle_y_center, handle_z_center) * Box(
        p.drawer_handle_width, p.drawer_handle_protrusion, p.drawer_handle_height
    )
    body = body + handle

    # === 取っ手のエッジに fillet（指あたりを柔らかく） ===
    # 突出した取っ手のエッジを丸める。fillet 失敗時はスキップ
    try:
        # 取っ手の Y<0 範囲のエッジを抽出（前方に突き出した部分のみ）
        handle_edges = [e for e in body.edges() if e.center().Y < 0]
        if handle_edges:
            body = fillet(handle_edges, radius=p.drawer_handle_fillet)
    except Exception:  # noqa: BLE001
        pass

    # Boolean 演算後は Compound になるため Part に変換して返す
    if isinstance(body, Compound):
        return Part(body.wrapped)
    return body
