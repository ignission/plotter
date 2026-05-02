"""標準カード(30×30×2mm)のSTL/STEP出力エントリ。

Usage:
    mise exec -- uv run python parts/card_standard.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.card import make_standard_card


def main() -> None:
    card = make_standard_card()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(card, str(out_dir / "card_standard.stl"))
    export_step(card, str(out_dir / "card_standard.step"))
    print(f"Wrote: {out_dir}/card_standard.stl")
    print(f"Wrote: {out_dir}/card_standard.step")


if __name__ == "__main__":
    main()
