"""Drawer の STL/STEP 出力エントリ。

Usage:
    mise exec -- uv run python parts/drawer.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.drawer import make_drawer


def main() -> None:
    drawer = make_drawer()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(drawer, str(out_dir / "drawer.stl"))
    export_step(drawer, str(out_dir / "drawer.step"))
    print(f"Wrote: {out_dir}/drawer.stl")
    print(f"Wrote: {out_dir}/drawer.step")


if __name__ == "__main__":
    main()
