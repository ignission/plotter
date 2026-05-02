"""Params dataclass の不変性とデフォルト値テスト。"""

import dataclasses

import pytest

from plotter.params import Params, params


def test_params_is_frozen_dataclass():
    """Params は frozen=True の dataclass であること。"""
    assert dataclasses.is_dataclass(Params)
    assert Params.__dataclass_params__.frozen is True


def test_params_singleton_is_instance():
    """モジュールレベルで params シングルトンが Params のインスタンスとして
    エクスポートされていること。"""
    assert isinstance(params, Params)


def test_params_cannot_be_mutated():
    """frozen=True により属性代入が FrozenInstanceError になること。"""
    with pytest.raises(dataclasses.FrozenInstanceError):
        params.card_thickness = 99.0  # type: ignore[misc]


def test_card_defaults():
    """Card パラメータのデフォルト値が SPEC.md と一致すること。"""
    assert params.card_width_std == 30.0
    assert params.card_width_wide == 60.0
    assert params.card_height == 30.0
    assert params.card_thickness == 2.0
    assert params.card_corner_radius == 3.0


def test_body_panel_defaults():
    """本体パネルのデフォルト値。"""
    assert params.panel_width == 200.0
    assert params.panel_height == 200.0
    assert params.panel_thickness == 3.0
    assert params.panel_angle == 75.0
    assert params.shelf_count == 6
    assert params.shelf_lip_height == 5.0
    assert params.shelf_lip_thickness == 2.0
    assert params.shelf_divider_thickness == 2.0


def test_tenon_defaults():
    """ホゾ（本体下端の凸）のデフォルト値。"""
    assert params.tenon_count == 5
    assert params.tenon_width == 14.0
    assert params.tenon_thickness == 2.0
    assert params.tenon_height == 20.0


def test_mortise_clearance_default():
    """ホゾ穴クリアランスは試作で実測調整される初期値。"""
    assert params.mortise_clearance == 0.2


def test_base_defaults():
    """土台のデフォルト値。"""
    assert params.base_width == 200.0
    assert params.base_depth == 50.0
    assert params.base_thickness == 4.0
    assert params.base_front_lip_height == 3.0
    assert params.base_front_lip_thickness == 2.0
