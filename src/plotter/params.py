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
    wedge_front_thickness: float = 5.0  # 前縁の薄さ
    wedge_back_thickness: float = 35.0  # 後縁の厚さ
    wedge_fillet_radius: float = 4.0  # 全エッジ R

    # === Card slots (cut into top tilted surface) ===
    card_slot_rows: int = 6
    card_slot_cols: int = 6
    card_slot_pocket_depth: float = 3.0  # ポケット深さ（カード厚2+1mm余裕）
    card_slot_clearance: float = 0.5  # ポケット幅と長さの余裕
    card_slot_x_pitch: float = 33.0  # X 方向のスロット中心間隔
    card_slot_face_pitch: float = 33.0  # 上面に沿った行間隔


params = Params()
