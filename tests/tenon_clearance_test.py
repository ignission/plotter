"""ホゾ・ホゾ穴のクリアランス検証パーツ。

clearance ∈ {0.1, 0.15, 0.2, 0.25, 0.3} の5検体を並べた STL/STEP を生成する。
実印刷で最適なクリアランスを確定し、結果を params.mortise_clearance に反映すること。

Usage:
    mise exec -- uv run python tests/tenon_clearance_test.py
"""

from pathlib import Path

from build123d import Box, Compound, Pos, export_step, export_stl

from plotter.params import params

# === 試作専用パラメータ（params.py には入れない使い捨て値） ===
CLEARANCES: list[float] = [0.1, 0.15, 0.2, 0.25, 0.3]
SPECIMEN_PITCH_X: float = 45.0
BASE_W: float = 20.0
BASE_Y: float = 8.0
GAP_BETWEEN_HALVES: float = 1.0
TENON_BASE_Z: float = 3.0
HOLE_DEPTH_MARGIN: float = 2.0
MORTISE_BASE_Z: float = 24.0


def build_specimen(clearance: float) -> Compound:
    """1検体（ホゾブロック + ホゾ穴ブロック）を生成する。

    検体の原点は X=0 中央、Y=0 中央、Z=0 が底。
    """
    half_pitch = (BASE_W + GAP_BETWEEN_HALVES) / 2

    # --- ホゾ側 (x < 0) ---
    tenon_base = Pos(-half_pitch, 0, TENON_BASE_Z / 2) * Box(BASE_W, BASE_Y, TENON_BASE_Z)
    tenon_post = Pos(-half_pitch, 0, TENON_BASE_Z + params.tenon_height / 2) * Box(
        params.tenon_width, params.tenon_thickness, params.tenon_height
    )
    tenon_block = tenon_base + tenon_post  # Solid

    # --- ホゾ穴側 (x > 0) ---
    hole_depth = params.tenon_height + HOLE_DEPTH_MARGIN  # 22mm
    mortise_base = Pos(half_pitch, 0, MORTISE_BASE_Z / 2) * Box(BASE_W, BASE_Y, MORTISE_BASE_Z)
    hole = Pos(half_pitch, 0, MORTISE_BASE_Z - hole_depth / 2) * Box(
        params.tenon_width + clearance,
        params.tenon_thickness + clearance,
        hole_depth,
    )
    mortise_block = mortise_base - hole  # Compound（Boolean差分）

    return Compound(children=[tenon_block, mortise_block])


def build_assembly() -> Compound:
    """5検体を X 軸に並べた Compound を返す。"""
    children = [
        Pos(i * SPECIMEN_PITCH_X, 0, 0) * build_specimen(c) for i, c in enumerate(CLEARANCES)
    ]
    return Compound(label="tenon_clearance_test", children=children)


def main() -> None:
    asm = build_assembly()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(asm, str(out_dir / "tenon_clearance_test.stl"))
    export_step(asm, str(out_dir / "tenon_clearance_test.step"))
    print(f"Wrote: {out_dir}/tenon_clearance_test.stl")
    print(f"Wrote: {out_dir}/tenon_clearance_test.step")


if __name__ == "__main__":
    main()
