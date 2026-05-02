"""tenon_clearance_test スクリプトの形状検証テスト。

実 STL は build/ に出力されるが、ここでは build123d オブジェクトの形状
プロパティを直接検証する（STL 解析よりも安定で速い）。
"""

from build123d import Compound

from tests.tenon_clearance_test import (
    BASE_W,
    BASE_Y,
    CLEARANCES,
    GAP_BETWEEN_HALVES,
    MORTISE_BASE_Z,
    SPECIMEN_PITCH_X,
    build_assembly,
    build_specimen,
)


def test_clearances_are_five_variants():
    """5 段階の clearance バリエーションが定義されていること。"""
    assert CLEARANCES == [0.1, 0.15, 0.2, 0.25, 0.3]


def test_specimen_returns_compound():
    """build_specimen は build123d Compound を返すこと。"""
    spec = build_specimen(0.2)
    assert isinstance(spec, Compound)


def test_specimen_bounding_box_dimensions():
    """1検体の bounding box が想定範囲内であること。

    X = 2*BASE_W + GAP, Y = BASE_Y, Z = MORTISE_BASE_Z (24)
    """
    spec = build_specimen(0.2)
    bbox = spec.bounding_box()
    assert bbox.size.X == 2 * BASE_W + GAP_BETWEEN_HALVES
    assert bbox.size.Y == BASE_Y
    # ホゾ側はベース3mm + ホゾ20mm = 23mm、ホゾ穴側は 24mm。max は 24mm。
    assert bbox.size.Z == MORTISE_BASE_Z


def test_assembly_has_five_specimens():
    """build_assembly は 5 検体を含む Compound を返すこと。"""
    asm = build_assembly()
    assert isinstance(asm, Compound)
    # 1検体あたり 2 solid（ホゾ側 + ホゾ穴側）→ 計 10 solid
    solids = asm.solids()
    assert len(solids) == 10


def test_assembly_x_extent():
    """5検体を SPECIMEN_PITCH_X で並べた合計 X 幅。"""
    asm = build_assembly()
    bbox = asm.bounding_box()
    expected_x = (len(CLEARANCES) - 1) * SPECIMEN_PITCH_X + (2 * BASE_W + GAP_BETWEEN_HALVES)
    assert bbox.size.X == expected_x


def test_specimen_volume_decreases_with_clearance():
    """clearance を増やすと検体体積は単調減少すること。"""
    volumes = [build_specimen(c).volume for c in CLEARANCES]
    assert volumes == sorted(volumes, reverse=True)
