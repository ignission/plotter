"""75°版土台のSTL/STEP出力エントリ。

panel_angle=75 (= 鉛直から 15° 後傾) の本体に対応する土台。

Usage:
    mise exec -- uv run python parts/base_75.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.base import make_base


def main() -> None:
    base = make_base()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(base, str(out_dir / "base_75.stl"))
    export_step(base, str(out_dir / "base_75.step"))
    print(f"Wrote: {out_dir}/base_75.stl")
    print(f"Wrote: {out_dir}/base_75.step")


if __name__ == "__main__":
    main()
