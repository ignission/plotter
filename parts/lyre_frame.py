"""Lyre フレームの STL/STEP 出力エントリ。

Usage:
    mise exec -- uv run python parts/lyre_frame.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.lyre import make_lyre


def main() -> None:
    lyre = make_lyre()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(lyre, str(out_dir / "lyre_frame.stl"))
    export_step(lyre, str(out_dir / "lyre_frame.step"))
    print(f"Wrote: {out_dir}/lyre_frame.stl")
    print(f"Wrote: {out_dir}/lyre_frame.step")


if __name__ == "__main__":
    main()
