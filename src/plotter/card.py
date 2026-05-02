"""カード（標準・ワイド）の形状生成関数。"""

from build123d import Part

from plotter.params import Params
from plotter.params import params as default_params
from plotter.utils import make_rounded_plate


def make_standard_card(p: Params = default_params) -> Part:
    """標準カード（card_width_std × card_height × card_thickness）を生成する。"""
    return make_rounded_plate(
        width=p.card_width_std,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )


def make_wide_card(p: Params = default_params) -> Part:
    """ワイドカード（card_width_wide × card_height × card_thickness）を生成する。"""
    return make_rounded_plate(
        width=p.card_width_wide,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )
