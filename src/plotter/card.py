"""カード（標準・ワイド）の形状生成。"""

from build123d import Box, Cylinder, Part, Pos

from plotter.params import Params
from plotter.params import params as default_params
from plotter.utils import make_rounded_plate


def _add_top_slit(card: Part, p: Params) -> Part:
    """カード上端中央に幅 slit_width × 深さ slit_depth のスリットを切る。

    スリット底端には半径 corner_radius の半円を追加して応力集中を回避する。
    座標系: card 中心が原点、Y=card_height/2 が上端、Z=card_thickness/2 が表面。
    """
    slit_top_y = p.card_height / 2 + 0.05  # 上端を確実に貫通
    slit_bottom_y = p.card_height / 2 - p.card_top_slit_depth
    slit_box_y_center = (slit_top_y + slit_bottom_y) / 2
    slit_box_y_size = slit_top_y - slit_bottom_y

    # 矩形スリット
    slit_box = Pos(0, slit_box_y_center, p.card_thickness / 2) * Box(
        p.card_top_slit_width, slit_box_y_size, p.card_thickness + 0.2
    )
    # スリット底端の半円（応力集中防止 R）
    slit_round = Pos(0, slit_bottom_y, p.card_thickness / 2) * Cylinder(
        radius=p.card_top_slit_width / 2 + p.card_top_slit_corner_radius,
        height=p.card_thickness + 0.2,
    )

    cut = card - slit_box - slit_round
    return cut


def make_standard_card(p: Params = default_params, *, with_slit: bool = True) -> Part:
    """標準カード。with_slit=True で上端スリット付き（Lyre 吊り下げ用）。"""
    card = make_rounded_plate(
        width=p.card_width_std,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )
    if with_slit:
        card = _add_top_slit(card, p)
    return card


def make_wide_card(p: Params = default_params, *, with_slit: bool = True) -> Part:
    """ワイドカード。with_slit=True で上端スリット付き（Lyre 吊り下げ用）。"""
    card = make_rounded_plate(
        width=p.card_width_wide,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )
    if with_slit:
        card = _add_top_slit(card, p)
    return card
