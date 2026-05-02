"""wedge.make_wedge の形状検証テスト。"""

import pytest
from build123d.topology import Part

from plotter.params import params
from plotter.wedge import make_wedge


def test_make_wedge_returns_part():
    wedge = make_wedge()
    assert isinstance(wedge, Part)


def test_wedge_starts_at_z_zero():
    wedge = make_wedge()
    bbox = wedge.bounding_box()
    assert bbox.min.Z == pytest.approx(0.0, abs=0.01)


def test_wedge_width_matches_params():
    wedge = make_wedge()
    bbox = wedge.bounding_box()
    assert bbox.size.X == pytest.approx(params.wedge_width, abs=0.5)


def test_wedge_depth_matches_params():
    wedge = make_wedge()
    bbox = wedge.bounding_box()
    assert bbox.size.Y == pytest.approx(params.wedge_depth, abs=0.5)


def test_wedge_back_is_taller_than_front():
    """ウェッジは前縁が薄く、後縁が厚い（傾斜上面）。"""
    wedge = make_wedge()
    bbox = wedge.bounding_box()
    # 高さは back_thickness 程度になる（ドロワーキャビティ後も外形は変わらない）
    assert bbox.size.Z == pytest.approx(params.wedge_back_thickness, abs=5.0)


def test_wedge_is_single_solid():
    wedge = make_wedge()
    assert len(wedge.solids()) == 1


def test_wedge_volume_is_reduced_by_pockets():
    """ポケットで体積が削れているはず（36 ポケット × 30×30×3 ≈ 97000mm³）。"""
    wedge = make_wedge()
    # 完全な wedge の体積（台形断面 × 幅）
    profile_area = (
        (params.wedge_front_thickness + params.wedge_back_thickness) / 2 * params.wedge_depth
    )
    full_volume = profile_area * params.wedge_width
    assert wedge.volume > 0
    assert wedge.volume < full_volume


def test_wedge_has_drawer_cavity():
    """ウェッジ内部にドロワーキャビティがあるので体積が減る。"""
    wedge = make_wedge()
    # ドロワーキャビティ + ポケット分の削減を確認
    avg_thickness = (params.wedge_front_thickness + params.wedge_back_thickness) / 2
    profile_area = avg_thickness * params.wedge_depth
    full_volume = profile_area * params.wedge_width
    assert wedge.volume < full_volume * 0.85  # キャビティ + ポケットで 15%以上削れる
