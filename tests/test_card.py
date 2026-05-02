"""カード生成関数のテスト。"""

from dataclasses import replace

import pytest

from plotter.card import make_standard_card, make_wide_card
from plotter.params import params


def test_standard_card_bbox_matches_params():
    """標準カードの bbox が params 既定値と一致すること。"""
    card = make_standard_card()
    bbox = card.bounding_box()
    assert bbox.size.X == pytest.approx(params.card_width_std, abs=0.01)
    assert bbox.size.Y == pytest.approx(params.card_height, abs=0.01)
    assert bbox.size.Z == pytest.approx(params.card_thickness, abs=0.01)


def test_wide_card_bbox_matches_params():
    """ワイドカードの bbox が params 既定値と一致すること。"""
    card = make_wide_card()
    bbox = card.bounding_box()
    assert bbox.size.X == pytest.approx(params.card_width_wide, abs=0.01)
    assert bbox.size.Y == pytest.approx(params.card_height, abs=0.01)
    assert bbox.size.Z == pytest.approx(params.card_thickness, abs=0.01)


def test_card_thickness_override_via_custom_params():
    """custom Params(card_thickness=...) で厚みをオーバーライドできること。"""
    custom = replace(params, card_thickness=3.0)
    card = make_standard_card(custom)
    assert card.bounding_box().size.Z == pytest.approx(3.0, abs=0.01)


def test_card_corner_is_rounded():
    """角R が効いている = 矩形より体積が小さい。"""
    card = make_standard_card(with_slit=False)
    rect_volume = params.card_width_std * params.card_height * params.card_thickness
    assert card.volume < rect_volume
    assert card.volume > rect_volume * 0.95


def test_wide_card_volume_is_slightly_over_double_standard():
    """ワイド (60mm) は標準 (30mm) の2倍をわずかに超える体積。

    角Rの削れは標準・ワイドで同じ量（同じ4角）なので、
    std_volume = 1800 - cut, wide_volume = 3600 - cut
    → ratio = (3600 - cut) / (1800 - cut) > 2 になる（cut > 0 のため）。
    cut ≈ 15.5mm³ なので ratio ≈ 3584.5 / 1784.5 ≈ 2.009。
    """
    std = make_standard_card(with_slit=False)
    wide = make_wide_card(with_slit=False)
    ratio = wide.volume / std.volume
    assert 2.0 < ratio < 2.02


def test_standard_card_with_slit_is_smaller_than_without():
    """with_slit=True はスリット分だけ体積が小さい。"""
    no_slit = make_standard_card(with_slit=False)
    with_slit = make_standard_card(with_slit=True)
    assert with_slit.volume < no_slit.volume


def test_slit_default_is_true():
    """デフォルトで with_slit=True（Lyre 用カードがデフォルト）。"""
    default_card = make_standard_card()
    no_slit_card = make_standard_card(with_slit=False)
    assert default_card.volume < no_slit_card.volume
