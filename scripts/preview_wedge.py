"""Wedge body を ocp-vscode に表示。

VSCode で OCP CAD Viewer を開いた状態で実行:
    PYTHONPATH=. mise exec -- uv run python scripts/preview_wedge.py
"""

from ocp_vscode import show

from plotter.wedge import make_wedge

show(make_wedge(), names=["wedge"])
print("送信完了")
