"""フルスケール本体パネル(200×200×3 + 6棚 + 5ホゾ)の STL/STEP 出力。

Usage:
    mise exec -- uv run python parts/body_full.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.body import make_body


def main() -> None:
    body = make_body()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(body, str(out_dir / "body_full.stl"))
    export_step(body, str(out_dir / "body_full.step"))
    print(f"Wrote: {out_dir}/body_full.stl")
    print(f"Wrote: {out_dir}/body_full.step")


if __name__ == "__main__":
    main()
