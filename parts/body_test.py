"""縮小試作版の本体パネル STL/STEP 出力。

panel_width=100, panel_height=80, shelf_count=2, tenon_count=3。
（CLAUDE.md は「1/4 scale」と書かれているが、実際は半幅×40%高さの
縮小版。tenon・card 寸法はフルスケールのままなので幾何検証用としては
有効。）

Usage:
    mise exec -- uv run python parts/body_test.py
"""

from dataclasses import replace
from pathlib import Path

from build123d import export_step, export_stl

from plotter.body import make_body
from plotter.params import params

TEST_PARAMS = replace(
    params,
    panel_width=100.0,
    panel_height=80.0,
    shelf_count=2,
    tenon_count=3,
)


def main() -> None:
    body = make_body(TEST_PARAMS)
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(body, str(out_dir / "body_test.stl"))
    export_step(body, str(out_dir / "body_test.step"))
    print(f"Wrote: {out_dir}/body_test.stl")
    print(f"Wrote: {out_dir}/body_test.step")


if __name__ == "__main__":
    main()
