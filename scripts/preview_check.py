"""ocp-vscode 動作確認用スクリプト。
VSCode で OCP CAD Viewer を開いた状態で実行する。
"""

from build123d import BuildPart, BuildSketch, RectangleRounded, extrude
from ocp_vscode import show

with BuildPart() as card:
    with BuildSketch():
        RectangleRounded(30, 30, 3)
    extrude(amount=2)

show(card.part, names=["card_preview_check"])
print("送信完了。VSCode のビューワーに角丸カードが表示されていればOK")
