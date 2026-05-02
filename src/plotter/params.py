"""PLOTTER 全部品の寸法・公差・パラメータの集中管理。

他モジュール（card.py / body.py / base.py）は必ず

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

    # === Body Panel ===
    panel_width: float = 200.0
    panel_height: float = 200.0
    panel_thickness: float = 3.0
    panel_angle: float = 75.0

    shelf_count: int = 6
    shelf_lip_height: float = 5.0
    shelf_lip_thickness: float = 2.0
    shelf_divider_thickness: float = 2.0

    # === Tenon (本体下端の凸) ===
    tenon_count: int = 5
    tenon_width: float = 14.0
    tenon_thickness: float = 2.0
    tenon_height: float = 20.0

    # === Mortise (土台側の穴) ===
    # 試作で実測調整必須。第1試作前に tenon_clearance_test で確定する。
    mortise_clearance: float = 0.2

    # === Base ===
    base_width: float = 200.0
    base_depth: float = 50.0
    base_thickness: float = 4.0
    base_front_lip_height: float = 3.0
    base_front_lip_thickness: float = 2.0


params = Params()
