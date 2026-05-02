"""build123d 共通ヘルパー関数。

各部品（card / body / base）から再利用される汎用形状ユーティリティを集約。
"""

from build123d import BuildPart, BuildSketch, Part, Rectangle, RectangleRounded, extrude


def make_rounded_plate(
    width: float,
    height: float,
    thickness: float,
    corner_radius: float,
) -> Part:
    """角丸矩形を厚み extrude した板状パーツを返す。

    原点はパーツ中心 (X=0, Y=0)、底面は Z=0、上面は Z=thickness。
    corner_radius=0 では Rectangle にフォールバックする
    （RectangleRounded は OCC で半径0を許容しないため）。
    """
    with BuildPart() as part:
        with BuildSketch():
            if corner_radius > 0:
                RectangleRounded(width, height, corner_radius)
            else:
                Rectangle(width, height)
        extrude(amount=thickness)
    return part.part
