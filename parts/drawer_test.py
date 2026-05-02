"""Drawer の試作版（半分スケール）STL/STEP 出力エントリ。

wedge_test.py と同じ寸法（半分スケール）でドロワーを生成する。
ウェッジ内部キャビティに適合するサイズ。

Usage:
    mise exec -- uv run python parts/drawer_test.py
"""

from dataclasses import replace
from pathlib import Path

from build123d import export_step, export_stl

from plotter.drawer import make_drawer
from plotter.params import params

TEST_PARAMS = replace(
    params,
    wedge_width=100.0,
    wedge_depth=100.0,
    wedge_front_thickness=15.0,
    wedge_back_thickness=28.0,
    card_slot_rows=3,
    card_slot_length=80.0,
    card_slot_face_pitch=30.0,
    drawer_width=76.0,
    drawer_depth=70.0,
    drawer_height=10.0,
    drawer_floor_offset_z=3.0,
)


def main() -> None:
    drawer = make_drawer(TEST_PARAMS)
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(drawer, str(out_dir / "drawer_test.stl"))
    export_step(drawer, str(out_dir / "drawer_test.step"))
    print(f"Wrote: {out_dir}/drawer_test.stl")
    print(f"Wrote: {out_dir}/drawer_test.step")


if __name__ == "__main__":
    main()
