"""plotter.utils の汎用ヘルパー関数テスト。"""

import pytest
from build123d import Part

from plotter.utils import make_rounded_plate


def test_make_rounded_plate_returns_part():
    """戻り値は build123d の Part（BuildPart().part の型）。"""
    plate = make_rounded_plate(30.0, 30.0, 2.0, 3.0)
    assert isinstance(plate, Part)


def test_make_rounded_plate_bbox_matches_dimensions():
    """bounding box が指定寸法と一致すること。"""
    plate = make_rounded_plate(30.0, 30.0, 2.0, 3.0)
    bbox = plate.bounding_box()
    assert bbox.size.X == pytest.approx(30.0, abs=0.01)
    assert bbox.size.Y == pytest.approx(30.0, abs=0.01)
    assert bbox.size.Z == pytest.approx(2.0, abs=0.01)


def test_make_rounded_plate_corner_is_rounded():
    """角R が効いている = 矩形より体積が小さく、削れすぎてもいないこと。"""
    plate = make_rounded_plate(30.0, 30.0, 2.0, 3.0)
    rect_volume = 30.0 * 30.0 * 2.0
    # 角R による削れ: (4 - π) * r² * thickness ≈ 0.86 * 9 * 2 ≈ 15.5mm³
    assert plate.volume < rect_volume
    assert plate.volume > rect_volume * 0.95  # 5%以上は残る


def test_make_rounded_plate_zero_radius_equals_box():
    """corner_radius=0 なら矩形ボックスと同体積（許容誤差内）。

    RectangleRounded は radius=0 で OCC 例外を出すため、関数内で
    Rectangle に分岐する必要がある（codex review で検証済み）。
    """
    plate = make_rounded_plate(30.0, 30.0, 2.0, 0.0)
    rect_volume = 30.0 * 30.0 * 2.0
    assert plate.volume == pytest.approx(rect_volume, rel=1e-6)


def test_make_rounded_plate_wide_dimensions():
    """ワイドカード相当 60×30×2 でも bbox が一致。"""
    plate = make_rounded_plate(60.0, 30.0, 2.0, 3.0)
    bbox = plate.bounding_box()
    assert bbox.size.X == pytest.approx(60.0, abs=0.01)
    assert bbox.size.Y == pytest.approx(30.0, abs=0.01)
    assert bbox.size.Z == pytest.approx(2.0, abs=0.01)
