"""Lyre フレームを ocp-vscode に表示。

VSCode で OCP CAD Viewer を開いた状態で実行:
    PYTHONPATH=. mise exec -- uv run python scripts/preview_lyre.py
"""

from ocp_vscode import show

from plotter.lyre import make_lyre

show(make_lyre(), names=["lyre_frame"])
print("送信完了")
