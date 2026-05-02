"""Wedge body の STL/STEP 出力エントリ。

Usage:
    mise exec -- uv run python parts/wedge.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.wedge import make_wedge


def main() -> None:
    wedge = make_wedge()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(wedge, str(out_dir / "wedge.stl"))
    export_step(wedge, str(out_dir / "wedge.step"))
    print(f"Wrote: {out_dir}/wedge.stl")
    print(f"Wrote: {out_dir}/wedge.step")


if __name__ == "__main__":
    main()
