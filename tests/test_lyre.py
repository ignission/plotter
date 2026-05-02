"""lyre.make_lyre の形状検証テスト。"""

import pytest
from build123d import Part

from plotter.lyre import make_lyre
from plotter.params import params


def test_make_lyre_returns_part():
    lyre = make_lyre()
    assert isinstance(lyre, Part)


def test_lyre_starts_at_z_zero():
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert bbox.min.Z == pytest.approx(0.0, abs=0.01)


def test_lyre_height_matches_param():
    """フレーム上端 Z は params.lyre_height ± 1mm 以内。"""
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert abs(bbox.max.Z - params.lyre_height) < 1.0


def test_lyre_is_left_right_symmetric_in_x():
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert bbox.min.X == pytest.approx(-bbox.max.X, abs=0.5)


def test_lyre_is_single_solid():
    lyre = make_lyre()
    assert len(lyre.solids()) == 1


def test_lyre_volume_is_positive_and_reasonable():
    """中央が大きく抜けているので外接ボックスより十分小さい。"""
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    full_box = bbox.size.X * bbox.size.Y * bbox.size.Z
    assert lyre.volume > 0
    assert lyre.volume < full_box * 0.5


def test_wire_z_spacing_is_uniform():
    """ワイヤ Z 高さは bottom_z から top_z まで等間隔（params で確認）。"""
    p = params
    spacing = (p.wire_top_z - p.wire_bottom_z) / (p.wire_count - 1)
    z_values = [p.wire_bottom_z + i * spacing for i in range(p.wire_count)]
    assert len(z_values) == p.wire_count
    assert z_values[0] == pytest.approx(p.wire_bottom_z)
    assert z_values[-1] == pytest.approx(p.wire_top_z)
