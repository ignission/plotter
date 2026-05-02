"""Wedge body の試作版（半分スケール）STL/STEP 出力エントリ。

カードは 30mm のまま、wedge と drawer の外寸を半分に縮小した試作。
印刷時間とフィラメントを節約しつつ、スロット・ドロワー・取っ手の
動作確認ができる。

Usage:
    mise exec -- uv run python parts/wedge_test.py
"""

from dataclasses import replace
from pathlib import Path

from build123d import export_step, export_stl

from plotter.params import params
from plotter.wedge import make_wedge

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
    wedge = make_wedge(TEST_PARAMS)
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(wedge, str(out_dir / "wedge_test.stl"))
    export_step(wedge, str(out_dir / "wedge_test.step"))
    print(f"Wrote: {out_dir}/wedge_test.stl")
    print(f"Wrote: {out_dir}/wedge_test.step")


if __name__ == "__main__":
    main()
