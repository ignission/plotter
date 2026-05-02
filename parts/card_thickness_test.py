"""カードの厚み試作（1.5/2/2.5/3mm）を4ファイルに分割出力する試作専用エントリ。

CLAUDE.md の指示通り、各厚みごとに独立した STL/STEP を生成する。
スライサで4ファイルをまとめて読み込めば1回の印刷で比較できる。
ファイル名は card_standard_t{thickness}.stl の形式。

Usage:
    mise exec -- uv run python parts/card_thickness_test.py
"""

from dataclasses import replace
from pathlib import Path

from build123d import export_step, export_stl

from plotter.card import make_standard_card
from plotter.params import params

THICKNESSES: list[float] = [1.5, 2.0, 2.5, 3.0]


def main() -> None:
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    for t in THICKNESSES:
        card = make_standard_card(replace(params, card_thickness=t))
        stem = f"card_standard_t{t}"
        export_stl(card, str(out_dir / f"{stem}.stl"))
        export_step(card, str(out_dir / f"{stem}.step"))
        print(f"Wrote: {out_dir}/{stem}.stl ({t}mm)")
        print(f"Wrote: {out_dir}/{stem}.step ({t}mm)")


if __name__ == "__main__":
    main()
