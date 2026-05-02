"""Params dataclass の不変性とデフォルト値テスト。"""

import dataclasses

import pytest

from plotter.params import Params, params


def test_params_singleton_is_instance():
    assert isinstance(params, Params)


def test_params_cannot_be_mutated():
    with pytest.raises(dataclasses.FrozenInstanceError):
        params.card_thickness = 99.0  # type: ignore[misc]


def test_card_defaults():
    assert params.card_width_std == 30.0
    assert params.card_width_wide == 60.0
    assert params.card_height == 30.0
    assert params.card_thickness == 2.0
    assert params.card_corner_radius == 3.0


def test_wedge_defaults():
    assert params.wedge_width == 200.0
    assert params.wedge_depth == 200.0
    assert params.wedge_front_thickness == 20.0
    assert params.wedge_back_thickness == 50.0
    assert params.wedge_fillet_radius == 4.0


def test_drawer_defaults():
    assert params.drawer_width == 180.0
    assert params.drawer_depth == 150.0
    assert params.drawer_height == 12.0
    assert params.drawer_clearance == 0.4
    assert params.drawer_wall_thickness == 2.0
    assert params.drawer_floor_offset_z == 4.0
    assert params.drawer_handle_width == 60.0
    assert params.drawer_handle_height == 4.0
    assert params.drawer_handle_protrusion == 5.0
    assert params.drawer_handle_fillet == 1.5


def test_card_slot_defaults():
    assert params.card_slot_rows == 6
    assert params.card_slot_length == 180.0
    assert params.card_slot_pocket_depth == 8.0
    assert params.card_slot_clearance == 0.5
    assert params.card_slot_face_pitch == 33.0
