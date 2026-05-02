"""カード3種（標準・ワイド・厚み試作4枚）を ocp-vscode に並べて表示する。

VSCode で OCP CAD Viewer を開いた状態で実行する:
    PYTHONPATH=. mise exec -- uv run python scripts/preview_cards.py
"""

from dataclasses import replace

from build123d import Compound, Pos
from ocp_vscode import show

from parts.card_thickness_test import THICKNESSES
from plotter.card import make_standard_card, make_wide_card
from plotter.params import params

# 標準カード（左）
std = Pos(0, 0, 0) * make_standard_card()

# ワイドカード（右）
wide = Pos(50, 0, 0) * make_wide_card()

# 厚み試作（手前に並べる）
thickness_pitch_x = params.card_width_std + 5.0
thickness_row_y = -50.0
thickness_cards = [
    Pos(i * thickness_pitch_x, thickness_row_y, 0)
    * make_standard_card(replace(params, card_thickness=t))
    for i, t in enumerate(THICKNESSES)
]

asm = Compound(
    label="cards_preview",
    children=[std, wide, *thickness_cards],
)

show(asm, names=["cards_preview"])
print("送信完了。VSCode のビューワーに以下が表示されているはず:")
print("  上段: 標準(30×30) + ワイド(60×30)")
print(f"  下段: 厚み試作 {THICKNESSES} mm の4枚")
