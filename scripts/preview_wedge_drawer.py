"""Wedge + Drawer のアセンブリを ocp-vscode に表示。

Usage:
    PYTHONPATH=. mise exec -- uv run python scripts/preview_wedge_drawer.py
"""

from build123d import Compound, Pos
from ocp_vscode import show

from plotter.drawer import make_drawer
from plotter.params import params
from plotter.wedge import make_wedge

wedge = make_wedge()
# ドロワーをキャビティ位置に配置（半分突き出した状態で見やすく）
drawer = Pos(0, -50, params.drawer_floor_offset_z) * make_drawer()

asm = Compound(label="plotter_assembly", children=[wedge, drawer])
show(asm, names=["plotter_assembly"])
print("送信完了")
