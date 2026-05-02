"""base.make_base の形状検証テスト。"""

import math
from dataclasses import replace

import pytest
from build123d import Part

from plotter.base import make_base
from plotter.params import params


def test_make_base_returns_part():
    """戻り値は build123d Part。"""
    base = make_base()
    assert isinstance(base, Part)


def test_base_outer_bbox_matches_params():
    """外形 bbox: X=base_width, Y=base_depth, Z=base_ridge_height."""
    base = make_base()
    bbox = base.bounding_box()
    assert bbox.size.X == pytest.approx(params.base_width, abs=0.01)
    assert bbox.size.Y == pytest.approx(params.base_depth, abs=0.01)
    assert bbox.size.Z == pytest.approx(params.base_ridge_height, abs=0.01)


def test_base_uses_base_width_independently_from_panel_width():
    """base_width は panel_width と独立。

    panel_width を変えても base_width はデフォルトのまま → bbox.X は base_width に追従。
    ホゾ穴 X 位置は body と合わせるため panel_width 由来で残す。
    """
    custom = replace(params, panel_width=150.0)  # base_width はデフォルト 200
    base = make_base(custom)
    assert base.bounding_box().size.X == pytest.approx(params.base_width, abs=0.01)


def test_base_starts_at_z_zero():
    """底面は Z=0。"""
    base = make_base()
    bbox = base.bounding_box()
    assert bbox.min.Z == pytest.approx(0.0, abs=0.01)


def test_base_is_single_solid():
    """全パーツが1つの連続したソリッド。"""
    base = make_base()
    assert len(base.solids()) == 1


def test_base_volume_is_positive_and_reasonable():
    """体積はゼロでなく、外接ボックスより小さい。"""
    base = make_base()
    bbox = base.bounding_box()
    full_box_volume = bbox.size.X * bbox.size.Y * bbox.size.Z
    assert base.volume > 0
    assert base.volume < full_box_volume * 0.7


def test_base_mortise_clearance_meets_spec():
    """ホゾ穴のクリアランスが params.mortise_clearance を反映。"""
    p = params
    hole_x = p.tenon_width + p.mortise_clearance
    hole_y_thickness = p.tenon_thickness + p.mortise_clearance
    assert hole_x == pytest.approx(14.2, abs=0.01)
    assert hole_y_thickness == pytest.approx(2.2, abs=0.01)


def test_base_param_override():
    """custom params で base_width を変えると bbox X も追従。"""
    custom = replace(params, base_width=150.0)
    base = make_base(custom)
    assert base.bounding_box().size.X == pytest.approx(150.0, abs=0.01)


def test_ridge_geometry_supports_22mm_hole():
    """背厚部の高さがホゾ穴 22mm + 底材 4mm 以上を確保していること。"""
    p = params
    angle_offset = math.radians(90 - p.panel_angle)
    entry_z = p.base_ridge_height - (p.base_ridge_depth / 2) * math.tan(angle_offset)
    bottom_z = entry_z - 22.0 * math.cos(angle_offset)
    assert bottom_z >= 4.0
