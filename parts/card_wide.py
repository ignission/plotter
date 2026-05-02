"""ワイドカード(60×30×2mm)のSTL/STEP出力エントリ。

Usage:
    mise exec -- uv run python parts/card_wide.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.card import make_wide_card


def main() -> None:
    card = make_wide_card()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(card, str(out_dir / "card_wide.stl"))
    export_step(card, str(out_dir / "card_wide.step"))
    print(f"Wrote: {out_dir}/card_wide.stl")
    print(f"Wrote: {out_dir}/card_wide.step")


if __name__ == "__main__":
    main()
