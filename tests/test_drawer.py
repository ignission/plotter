"""drawer.make_drawer の形状検証テスト。"""

import pytest
from build123d.topology import Part

from plotter.drawer import make_drawer
from plotter.params import params


def test_make_drawer_returns_part():
    drawer = make_drawer()
    assert isinstance(drawer, Part)


def test_drawer_outer_dimensions():
    drawer = make_drawer()
    bbox = drawer.bounding_box()
    assert bbox.size.X == pytest.approx(params.drawer_width, abs=0.5)
    assert bbox.size.Y == pytest.approx(params.drawer_depth, abs=0.5)
    assert bbox.size.Z == pytest.approx(params.drawer_height, abs=0.5)


def test_drawer_is_single_solid():
    drawer = make_drawer()
    assert len(drawer.solids()) == 1


def test_drawer_has_internal_cavity():
    """内部空洞があるので体積はソリッドの外接箱より小さい。"""
    drawer = make_drawer()
    full_box = params.drawer_width * params.drawer_depth * params.drawer_height
    assert drawer.volume > 0
    assert drawer.volume < full_box * 0.6  # 内部空洞 + 前面開口 + プル recess で削れる
