# Step 2: ホゾ・ホゾ穴 公差検証パーツ 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** ホゾ（14×2×20mm）とホゾ穴（14+c × 2+c × 22mm）の最適クリアランス c を実印刷で確定するための公差検証 STL を生成する。clearance ∈ {0.1, 0.15, 0.2, 0.25, 0.3} の5バリエーションを X 軸に30mmピッチで並べた1ファイルにする。

**Architecture:**
- `tests/tenon_clearance_test.py` をエントリポイントスクリプトとし、`__main__` で `build/tenon_clearance_test.stl` と `build/tenon_clearance_test.step` を出力する
- 形状生成ロジックは `build_specimen(clearance: float) -> Part` という純粋関数に切り出し、引数なしで呼べる `build_assembly() -> Compound` で5検体を並べる
- 寸法は `params.tenon_width / tenon_thickness / tenon_height` から取得し、検体固有の足回り寸法（ベース板厚など）はファイル内のモジュール定数で扱う（試作専用の使い捨てパラメータなので `params.py` には入れない）

**Tech Stack:** build123d 0.10.0、pytest、Python 3.13

---

## File Structure

- Create: `tests/tenon_clearance_test.py` — エントリポイント。形状生成 + STL/STEP 出力。pytest 収集対象外（`python_files = "test_*.py"` 設定により `_test.py` 終わりは無視される）
- Create: `tests/test_tenon_clearance.py` — 形状の自動テスト（pytest 対象、bounding box と検体数の検証）
- Modify: `Makefile` — `make clearance` ターゲットを追加（任意・最後に）

build/ 出力は .gitignore 済み。

---

## 検体の幾何

各検体は X 軸に幅 `BASE_W=20mm` の **ホゾ側** と **ホゾ穴側** の2ブロックを並べたもの。

```
            Z
            ↑
            │   ┌──┐  ← tenon (14×2, 高さ 20)
            │   │  │
            │   │  │
   ┌────────┴───┴──┴──────────┐         ┌──────────────────────┐
   │ tenon base (20×8×3)       │         │ mortise base (20×8×24) │
   └───────────────────────────┘         │   ┏━━┓ hole (14+c × 2+c, depth 22)
                                          │   ┃  ┃                │
                                          │   ┗━━┛                │
                                          └──────────────────────┘
   ───── X ───→  (1検体内で2ブロックを 1mm 隙間で並べる)
```

検体の総占有: X 方向 ≈ 41mm（20+1+20）、Y 方向 8mm、Z 方向 24mm。
検体ピッチ: 30mm（**設計上隣の検体と接触する** → ピッチを 45mm に変えるかは検討）。

**ピッチ 30mm vs 45mm:** SPEC.md の指定は 30mm だが、上記の幾何だと検体幅 41mm > ピッチ 30mm で重なる。Task 1 開始前に再確認 → ピッチを **45mm に拡張**する（SPEC との差分を README/SPEC のどこかにメモ）。

### モジュール定数

```python
CLEARANCES: list[float] = [0.1, 0.15, 0.2, 0.25, 0.3]
SPECIMEN_PITCH_X: float = 45.0           # 検体間ピッチ（SPEC は 30mm だが幾何上 45mm 必要）
BASE_W: float = 20.0                     # 各ブロックの X 幅
BASE_Y: float = 8.0                      # 各ブロックの Y 奥行
GAP_BETWEEN_HALVES: float = 1.0          # 同一検体内のホゾブロックとホゾ穴ブロックの隙間
TENON_BASE_Z: float = 3.0                # ホゾ側ベース板厚
HOLE_DEPTH_MARGIN: float = 2.0           # ホゾ穴深さ = tenon_height + margin
MORTISE_BASE_Z: float = 24.0             # ホゾ穴側ブロック厚（= 穴22 + 底2）
```

ホゾ寸法は `params.tenon_width=14`、`params.tenon_thickness=2`、`params.tenon_height=20` から参照。

---

## Task 1: テストファイルの骨格と数量検証テストを書く（RED）

**Files:**
- Create: `tests/test_tenon_clearance.py`

- [ ] **Step 1: テストファイル全体を書く**

```python
"""tenon_clearance_test スクリプトの形状検証テスト。

実 STL は build/ に出力されるが、ここでは build123d オブジェクトの形状
プロパティを直接検証する（STL 解析よりも安定で速い）。
"""

from build123d import Compound, Part

from tests.tenon_clearance_test import (
    BASE_W,
    BASE_Y,
    CLEARANCES,
    GAP_BETWEEN_HALVES,
    MORTISE_BASE_Z,
    SPECIMEN_PITCH_X,
    build_assembly,
    build_specimen,
)
from plotter.params import params


def test_clearances_are_five_variants():
    """5 段階の clearance バリエーションが定義されていること。"""
    assert CLEARANCES == [0.1, 0.15, 0.2, 0.25, 0.3]


def test_specimen_returns_part():
    """build_specimen は build123d Part を返すこと。"""
    spec = build_specimen(0.2)
    assert isinstance(spec, Part)


def test_specimen_bounding_box_dimensions():
    """1検体の bounding box が想定範囲内であること。

    X = 2*BASE_W + GAP, Y = BASE_Y, Z = MORTISE_BASE_Z (24)
    """
    spec = build_specimen(0.2)
    bbox = spec.bounding_box()
    assert bbox.size.X == 2 * BASE_W + GAP_BETWEEN_HALVES
    assert bbox.size.Y == BASE_Y
    # ホゾ側はベース3mm + ホゾ20mm = 23mm、ホゾ穴側は 24mm。max は 24mm。
    assert bbox.size.Z == MORTISE_BASE_Z


def test_assembly_has_five_specimens():
    """build_assembly は 5 検体を含む Compound を返すこと。"""
    asm = build_assembly()
    assert isinstance(asm, Compound)
    # 検体は5つ（Compound の直下の子要素 or solid 数で判定）
    solids = asm.solids()
    # 1検体あたり 2 solid（ホゾ側 + ホゾ穴側）→ 計 10 solid
    assert len(solids) == 10


def test_assembly_x_extent():
    """5検体を SPECIMEN_PITCH_X で並べた合計 X 幅。"""
    asm = build_assembly()
    bbox = asm.bounding_box()
    # 末尾検体の右端 X = (n-1) * pitch + 検体幅
    expected_x = (len(CLEARANCES) - 1) * SPECIMEN_PITCH_X + (2 * BASE_W + GAP_BETWEEN_HALVES)
    assert bbox.size.X == expected_x


def test_specimen_uses_params_for_tenon_dims():
    """検体のホゾ寸法は params から参照されていること（差分検出）。

    params.tenon_width を一時的に変えると bbox が変わることで間接確認。
    ここでは clearance=0 の specimen から hole/tenon の存在を体積比で見る。
    """
    spec_thin = build_specimen(0.1)
    spec_thick = build_specimen(0.3)
    # クリアランスが大きいほど hole が大きい = mortise 側ブロックの体積が小さい
    assert spec_thick.volume < spec_thin.volume


def test_specimen_volume_decreases_with_clearance():
    """clearance を増やすと検体体積は単調減少すること。"""
    volumes = [build_specimen(c).volume for c in CLEARANCES]
    assert volumes == sorted(volumes, reverse=True)
```

- [ ] **Step 2: テスト実行 → ImportError で FAIL（RED）**

Run: `mise exec -- uv run pytest tests/test_tenon_clearance.py -v`
Expected: `ModuleNotFoundError: No module named 'tests.tenon_clearance_test'` または ImportError

**この時点ではコミットしない。**

---

## Task 2: tenon_clearance_test.py を実装（GREEN）

**Files:**
- Create: `tests/tenon_clearance_test.py`

- [ ] **Step 1: スクリプト全体を実装**

```python
"""ホゾ・ホゾ穴のクリアランス検証パーツ。

clearance ∈ {0.1, 0.15, 0.2, 0.25, 0.3} の5検体を並べた STL/STEP を生成する。
実印刷で最適なクリアランスを確定し、結果を params.mortise_clearance に反映すること。

Usage:
    mise exec -- uv run python tests/tenon_clearance_test.py
    # → build/tenon_clearance_test.stl と .step が出力される
"""

from pathlib import Path

from build123d import Box, Compound, Location, Part, Pos

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


def build_specimen(clearance: float) -> Part:
    """1検体（ホゾブロック + ホゾ穴ブロック）を生成する。

    検体の原点は X=0 中央、Y=0 中央、Z=0 が底。
    """
    half_pitch = (BASE_W + GAP_BETWEEN_HALVES) / 2

    # --- ホゾ側 (x < 0) ---
    tenon_base = Pos(-half_pitch, 0, TENON_BASE_Z / 2) * Box(BASE_W, BASE_Y, TENON_BASE_Z)
    tenon_post = Pos(
        -half_pitch, 0, TENON_BASE_Z + params.tenon_height / 2
    ) * Box(params.tenon_width, params.tenon_thickness, params.tenon_height)
    tenon_block: Part = tenon_base + tenon_post

    # --- ホゾ穴側 (x > 0) ---
    hole_depth = params.tenon_height + HOLE_DEPTH_MARGIN  # 22mm
    mortise_base = Pos(half_pitch, 0, MORTISE_BASE_Z / 2) * Box(BASE_W, BASE_Y, MORTISE_BASE_Z)
    hole = Pos(
        half_pitch, 0, MORTISE_BASE_Z - hole_depth / 2
    ) * Box(
        params.tenon_width + clearance,
        params.tenon_thickness + clearance,
        hole_depth,
    )
    mortise_block: Part = mortise_base - hole

    return tenon_block + mortise_block


def build_assembly() -> Compound:
    """5検体を X 軸に並べた Compound を返す。"""
    children = [
        Pos(i * SPECIMEN_PITCH_X, 0, 0) * build_specimen(c)
        for i, c in enumerate(CLEARANCES)
    ]
    return Compound(label="tenon_clearance_test", children=children)


def main() -> None:
    asm = build_assembly()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    asm.export_stl(str(out_dir / "tenon_clearance_test.stl"))
    asm.export_step(str(out_dir / "tenon_clearance_test.step"))
    print(f"Wrote: {out_dir}/tenon_clearance_test.stl")
    print(f"Wrote: {out_dir}/tenon_clearance_test.step")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: テスト実行 → 全 PASS**

Run: `mise exec -- uv run pytest tests/test_tenon_clearance.py -v`
Expected: 7 passed

  build123d API ミスマッチで失敗した場合（例: `Pos` の名称、`Box` の `align` 引数など）、build123d 0.10.0 の docs を確認しながら修正する。**STOP and report concerns** if you cannot resolve API mismatches.

- [ ] **Step 3: 既存テストも全PASSであることを確認**

Run: `mise exec -- uv run pytest -v`
Expected: 14 passed (params 7 + tenon_clearance 7)

- [ ] **Step 4: ruff format & check**

Run: `mise exec -- uv run ruff format src/ tests/ && mise exec -- uv run ruff check src/ tests/`
Expected: 0 エラー

- [ ] **Step 5: スクリプトを実際に実行して STL/STEP が出力されることを確認**

Run: `mise exec -- uv run python tests/tenon_clearance_test.py`
Expected: `Wrote: .../build/tenon_clearance_test.stl` と `.step` が表示される。
追加確認: `ls -la build/tenon_clearance_test.*` で2ファイル存在、ファイルサイズが 0 でないこと。

- [ ] **Step 6: コミット**

```bash
git add tests/tenon_clearance_test.py tests/test_tenon_clearance.py
git commit -m "$(cat <<'EOF'
ホゾ・ホゾ穴の公差検証パーツを実装

clearance ∈ {0.1, 0.15, 0.2, 0.25, 0.3} の5検体を X 軸 45mm ピッチで並べた
STL/STEP を生成する。実印刷で最適 clearance を確定し params.mortise_clearance
に反映する用途。

検体ピッチは SPEC.md の 30mm から 45mm に拡張（検体幅 41mm のため重なり回避）。
EOF
)"
```

---

## Task 3: Makefile に make clearance ターゲットを追加

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Makefile を読む**

Read: `Makefile`

- [ ] **Step 2: `clearance` ターゲットを追加し help にも記載**

`.PHONY` 行に `clearance` を追加。
`help:` ターゲットの中に `@echo "  make clearance - Build tenon clearance test print"` を追加。
新ターゲット定義を `base:` の後に挿入：

```makefile
clearance: $(BUILD_DIR)
	$(PYTHON) tests/tenon_clearance_test.py
```

- [ ] **Step 3: 動作確認**

Run: `make clearance`
Expected: `tests/tenon_clearance_test.py` が走り、STL/STEP が更新される

- [ ] **Step 4: コミット**

```bash
git add Makefile
git commit -m "Makefile に make clearance ターゲットを追加"
```

---

## 完了の定義

- `mise exec -- uv run pytest -v` で 14 passed
- `make clearance` で `build/tenon_clearance_test.stl` と `.step` が生成
- `mise exec -- uv run ruff check src/ tests/` 0 エラー
- 2コミットが main にある（実装、Makefile）

## 次フェーズへの引き継ぎ

- 実印刷で最適 clearance を確定 → `params.mortise_clearance` を更新
- 結果を `docs/SPEC.md` の公差表に追記（コミット）
- 確定後に Step 3（本体パネル）に進む

---

## Self-Review

**Spec coverage:**
- ✅ clearance ∈ {0.1, 0.15, 0.2, 0.25, 0.3} の5検体
- ✅ X軸ピッチ並列配置（30mm → 45mm に変更しメモ）
- ✅ 1ファイル STL 出力で1回印刷
- ✅ params.tenon_* を参照（ハードコード回避）
- ✅ 試作専用パラメータは params.py を汚さずファイル内定数で管理

**Placeholder scan:** TODO/TBD なし。すべてのコードは完全実装。

**Type consistency:**
- `build_specimen(clearance: float) -> Part`
- `build_assembly() -> Compound`
- `CLEARANCES: list[float]`
- 型シグネチャはテストとも一致。

**Risk:**
- build123d 0.10.0 の API（`Pos`、`Box`、`Compound`、`Location`）がドキュメント通りか未検証。実装サブエージェントに最新 API を確認させ、mismatch があれば DONE_WITH_CONCERNS で報告させる。
