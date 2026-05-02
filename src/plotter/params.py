"""PLOTTER 全部品の寸法・公差・パラメータの集中管理。

他モジュール（card.py / wedge.py）は必ず

    from plotter.params import params

でこのシングルトン経由で値を参照すること。値のハードコードは禁止。

frozen=True により実行時にミューテーションを禁止する。値を変える場合は
このファイルのデフォルト値を編集するか、別インスタンスを作って渡す。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    # === Card ===
    card_width_std: float = 30.0
    card_width_wide: float = 60.0
    card_height: float = 30.0
    card_thickness: float = 2.0
    card_corner_radius: float = 3.0

    # === Wedge body ===
    wedge_width: float = 200.0  # X 方向（左右）
    wedge_depth: float = 200.0  # Y 方向（前後）
    wedge_front_thickness: float = 20.0  # 前縁の厚さ（ドロワー収容のため 5→20）
    wedge_back_thickness: float = 50.0  # 後縁の厚さ（傾斜角維持のため 35→50）
    wedge_fillet_radius: float = 4.0  # 全エッジ R

    # === Drawer ===
    drawer_width: float = 180.0  # X 方向（ウェッジ内幅 - 余裕）
    drawer_depth: float = 150.0  # Y 方向（前縁から後縁手前まで）
    drawer_height: float = 12.0  # Z 方向（厚み）
    drawer_clearance: float = 0.4  # ウェッジキャビティとのスライド隙間
    drawer_wall_thickness: float = 2.0  # ドロワー外壁の厚み
    drawer_floor_offset_z: float = 4.0  # ウェッジ底からドロワー底面までの Z オフセット
    drawer_handle_width: float = 60.0  # 取っ手バーの横幅
    drawer_handle_height: float = 4.0  # 取っ手バーの縦幅
    drawer_handle_protrusion: float = 5.0  # 前面からの突出量（指がかかる空間）
    drawer_handle_fillet: float = 1.5  # 取っ手のエッジ R

    # === Card slots (cut into top tilted surface, 6 rows of long slits) ===
    # 列の仕切りはなし。各行 1 本の長スロット。標準カード(30mm)とワイド(60mm)
    # を任意の組み合わせで並べられる。カードはスロット内を自由スライド可。
    card_slot_rows: int = 6
    card_slot_length: float = 180.0  # 各スロットの長さ（X 方向、左右 10mm マージン）
    card_slot_pocket_depth: float = 8.0  # 上面に対する垂直深さ（カード保持力）
    card_slot_clearance: float = 0.5  # 厚み方向のクリアランス（カード厚2 + 0.5）
    card_slot_face_pitch: float = 33.0  # 上面に沿った行間隔


params = Params()
