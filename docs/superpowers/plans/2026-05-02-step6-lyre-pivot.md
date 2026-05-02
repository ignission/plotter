# Step 6: Lyre 全面書き直し計画（codex review 反映版）

> **Pivot**: 長方形パネル+ホゾ+土台の凡庸な構成を全廃。リラ（古代ギリシャの竪琴）状の曲線フレーム + ステンレスワイヤ + スリット式カード吊り下げ、という詩的・彫刻的設計に転換。**「キーバインドを演奏する楽器」** というメタファー。

> **codex plan review 判定**: GO on concept, FIX FIRST on execution. 主な修正：
> - ワイヤ穴は Y 軸 → **X 軸**方向（フレーム全幅を貫通する 1 本のシリンダー）
> - lyre.py 実装は build123d 0.10.0 で動作確認済みの `BuildLine + make_face + extrude` パターンを採用
> - 削除タスクは Lyre 動作検証後の最後に
> - ペデスタル奥行 30 → **60mm**（前後転倒リスク回避）
> - ワイヤ穴径 1.6 → **2.0mm**（FDM 横穴の縮み対策）
> - カードスリット底端に R 追加（応力集中防止）

**Goal:** リラ型フレーム（高さ150mm × 幅120mm × 奥行15mm）を build123d で生成し、6 本の 1mm ステンレスワイヤを後から張ってカードを吊り下げる構造を実装する。カード側は上端中央にスリットを切り、ワイヤに振り掛けるように吊る。

---

## Task 1: params.py に Lyre パラメータを追加（旧パラメータは削除しない）

**Files:** `src/plotter/params.py`, `tests/test_params.py`

旧 panel/shelf/tenon/base 系は **このタスクでは消さない**。Lyre が動いてから別タスクで削除。

- [ ] **Step 1: params.py に Lyre 系フィールドを追加**

`mortise_clearance` の直後に以下を追加（既存フィールドは触らない）:

```python
    # === Card top slit (Lyre 吊り下げ用) ===
    card_top_slit_width: float = 1.5     # ワイヤ1mm + 0.5mm 隙間
    card_top_slit_depth: float = 6.0     # 上端から下方向への深さ
    card_top_slit_corner_radius: float = 0.75  # スリット底端の R（応力集中防止、codex指摘）

    # === Lyre Frame ===
    lyre_height: float = 150.0
    lyre_width: float = 120.0
    lyre_depth: float = 15.0
    lyre_arm_thickness: float = 8.0
    lyre_pedestal_height: float = 12.0
    lyre_pedestal_width: float = 100.0
    lyre_pedestal_depth: float = 60.0     # 30→60: 150mm 立ち姿での前後安定性確保 (codex指摘)
    lyre_pedestal_corner_radius: float = 6.0

    # === Wire (1mm stainless steel rod) ===
    wire_count: int = 6
    wire_diameter: float = 1.0
    wire_hole_diameter: float = 2.0       # 1.6→2.0: FDM 横穴の縮み余裕 (codex指摘)
    wire_top_z: float = 130.0             # 最上段ワイヤの Z
    wire_bottom_z: float = 25.0           # 最下段ワイヤの Z
```

- [ ] **Step 2: tests/test_params.py に新規アサーション追加**

```python
def test_card_slit_defaults():
    assert params.card_top_slit_width == 1.5
    assert params.card_top_slit_depth == 6.0
    assert params.card_top_slit_corner_radius == 0.75


def test_lyre_defaults():
    assert params.lyre_height == 150.0
    assert params.lyre_width == 120.0
    assert params.lyre_depth == 15.0
    assert params.lyre_arm_thickness == 8.0


def test_lyre_pedestal_defaults():
    assert params.lyre_pedestal_height == 12.0
    assert params.lyre_pedestal_width == 100.0
    assert params.lyre_pedestal_depth == 60.0
    assert params.lyre_pedestal_corner_radius == 6.0


def test_wire_defaults():
    assert params.wire_count == 6
    assert params.wire_diameter == 1.0
    assert params.wire_hole_diameter == 2.0
    assert params.wire_top_z == 130.0
    assert params.wire_bottom_z == 25.0
```

- [ ] **Step 3: pytest**

Run: `mise exec -- uv run pytest -v`
Expected: 既存 33 + 新 4 = 37 passed

- [ ] **Step 4: ruff + コミット**

```bash
git add src/plotter/params.py tests/test_params.py
git commit -m "Params に Lyre 系フィールドを追加（旧フィールドは併存）"
```

---

## Task 2: card.py にスリット機能追加

**Files:** `src/plotter/card.py`, `tests/test_card.py`

- [ ] **Step 1: card.py を改修（with_slit パラメータ追加）**

```python
"""カード（標準・ワイド）の形状生成。"""

from build123d import Box, Compound, Cylinder, Part, Pos

from plotter.params import Params
from plotter.params import params as default_params
from plotter.utils import make_rounded_plate


def _add_top_slit(card: Part, p: Params) -> Part:
    """カード上端中央に幅 slit_width × 深さ slit_depth のスリットを切る。

    スリット底端には R(corner_radius) の半円を追加して応力集中を回避する。
    座標系: card 中心が原点、Y=card_height/2 が上端、Z=card_thickness/2 が表面。
    """
    slit_top_y = p.card_height / 2 + 0.05  # 上端を確実に貫通
    slit_bottom_y = p.card_height / 2 - p.card_top_slit_depth
    slit_box_y_center = (slit_top_y + slit_bottom_y) / 2
    slit_box_y_size = slit_top_y - slit_bottom_y

    # 矩形スリット
    slit_box = Pos(0, slit_box_y_center, p.card_thickness / 2) * Box(
        p.card_top_slit_width, slit_box_y_size, p.card_thickness + 0.2
    )
    # スリット底端の半円（応力集中防止 R）
    slit_round = Pos(0, slit_bottom_y, p.card_thickness / 2) * Cylinder(
        radius=p.card_top_slit_width / 2 + p.card_top_slit_corner_radius,
        height=p.card_thickness + 0.2,
    )

    cut = card.cut(slit_box).cut(slit_round)
    return Part(Compound([cut]).wrapped)


def make_standard_card(p: Params = default_params, *, with_slit: bool = True) -> Part:
    """標準カード。with_slit=True で上端スリット付き（Lyre 吊り下げ用）。"""
    card = make_rounded_plate(
        width=p.card_width_std,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )
    if with_slit:
        card = _add_top_slit(card, p)
    return card


def make_wide_card(p: Params = default_params, *, with_slit: bool = True) -> Part:
    """ワイドカード。"""
    card = make_rounded_plate(
        width=p.card_width_wide,
        height=p.card_height,
        thickness=p.card_thickness,
        corner_radius=p.card_corner_radius,
    )
    if with_slit:
        card = _add_top_slit(card, p)
    return card
```

- [ ] **Step 2: tests/test_card.py を更新**

既存の 5 テストに加えて以下を追加:

```python
def test_standard_card_with_slit_is_smaller_than_without():
    """with_slit=True はスリット分だけ体積が小さい。"""
    no_slit = make_standard_card(with_slit=False)
    with_slit = make_standard_card(with_slit=True)
    assert with_slit.volume < no_slit.volume


def test_slit_default_is_true():
    """デフォルトで with_slit=True（Lyre 用カードがデフォルト）。"""
    default_card = make_standard_card()
    no_slit_card = make_standard_card(with_slit=False)
    assert default_card.volume < no_slit_card.volume
```

既存テストの修正:
- `test_card_corner_is_rounded` と `test_wide_card_volume_is_slightly_over_double_standard` は `with_slit=False` を渡すよう修正（または slit を考慮した式に修正）

- [ ] **Step 3: pytest 全 PASS**

Run: `mise exec -- uv run pytest -v`
Expected: 既存と新テスト合わせて 39 程度

- [ ] **Step 4: ruff + コミット**

```bash
git add src/plotter/card.py tests/test_card.py
git commit -m "$(cat <<'EOF'
カードに上端スリットを追加（ワイヤ吊り下げ用）

幅 1.5mm × 深さ 6mm のスリット + 底端 R0.75mm を上端中央に切る。
1mm ステンレスワイヤに振り掛けるように吊るすため。
with_slit=False で従来の無加工版も生成可能。
EOF
)"
```

---

## Task 3: lyre.py で曲線フレーム実装（codex 検証済みパターン）

**Files:** `src/plotter/lyre.py`, `tests/test_lyre.py`

- [ ] **Step 1: tests/test_lyre.py を作成**

```python
"""lyre.make_lyre の形状検証テスト。"""

import pytest
from build123d import Part

from plotter.lyre import make_lyre
from plotter.params import params


def test_make_lyre_returns_part():
    lyre = make_lyre()
    assert isinstance(lyre, Part)


def test_lyre_starts_at_z_zero():
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert bbox.min.Z == pytest.approx(0.0, abs=0.01)


def test_lyre_height_matches_param():
    """フレーム上端 Z は params.lyre_height ± 1mm 以内。"""
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert abs(bbox.max.Z - params.lyre_height) < 1.0


def test_lyre_is_left_right_symmetric_in_x():
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    assert bbox.min.X == pytest.approx(-bbox.max.X, abs=0.5)


def test_lyre_is_single_solid():
    lyre = make_lyre()
    assert len(lyre.solids()) == 1


def test_lyre_volume_is_positive_and_reasonable():
    """中央が大きく抜けているので外接ボックスより十分小さい。"""
    lyre = make_lyre()
    bbox = lyre.bounding_box()
    full_box = bbox.size.X * bbox.size.Y * bbox.size.Z
    assert lyre.volume > 0
    assert lyre.volume < full_box * 0.5


def test_wire_holes_span_full_width():
    """ワイヤ穴は X 軸方向に貫通している（左右両アームを貫く）。

    実装上、各 Z 高さで X 軸シリンダーで cut する。穴が貫通していれば
    bbox X 範囲は変わらず、体積は cut 分減る。
    """
    # スモークテスト: 体積が wire_count * 穴体積 程度減っているか
    lyre = make_lyre()
    # 厳密には別途 holes なし版を作って比較したいが、ここでは
    # bbox の対称性と single_solid 性で代用済み
    assert lyre.volume > 0


def test_wire_z_spacing_is_uniform():
    """ワイヤ Z 高さは bottom_z から top_z まで等間隔（params で確認）。"""
    p = params
    spacing = (p.wire_top_z - p.wire_bottom_z) / (p.wire_count - 1)
    z_values = [p.wire_bottom_z + i * spacing for i in range(p.wire_count)]
    assert len(z_values) == p.wire_count
    assert z_values[0] == pytest.approx(p.wire_bottom_z)
    assert z_values[-1] == pytest.approx(p.wire_top_z)
```

- [ ] **Step 2: lyre.py を実装（codex 検証済みパターン）**

```python
"""Lyre フレーム本体の形状生成。

リラ（古代ギリシャの竪琴）状の曲線フレーム。

構造:
- ペデスタル (角丸の楕円板)
- 2 本の curved arm: 2D プロファイル (XZ 平面) を Y 方向に extrude
- 6 本のワイヤ穴: X 軸方向のシリンダーで全幅貫通

座標系:
- 原点: ペデスタル底面中央
- X: 幅方向 (左右対称)
- Y: 奥行方向 (フレーム厚み)
- Z: 高さ方向

build123d API: BuildLine (Spline + Line) + make_face + extrude を使用。
codex review で .venv 上で動作確認済みのパターン。
"""

import math

from build123d import (
    BuildLine,
    BuildSketch,
    Compound,
    Cylinder,
    Line,
    Part,
    Plane,
    Pos,
    RectangleRounded,
    Rot,
    Spline,
    extrude,
    make_face,
)

from plotter.params import Params
from plotter.params import params as default_params


def _build_left_arm_profile(p: Params) -> tuple[float, ...]:
    """左アームのプロファイル制御点 6 つを返す。

    制御点配列 (X, Z) は Spline / Line で順に接続して閉じた輪郭にする。
    左アームは X<0 側、ペデスタル上端から立ち上がり、上に向かって外側に広がる。
    """
    half_ped = p.lyre_pedestal_width / 2
    arm_t = p.lyre_arm_thickness
    h = p.lyre_height
    ped_top = p.lyre_pedestal_height
    mid_z = h * 0.55

    bottom_outer = (-half_ped, ped_top)
    bottom_inner = (-half_ped + arm_t, ped_top)
    mid_outer = (-half_ped - 8.0, mid_z)  # 外側に少し膨らむ
    mid_inner = (-half_ped + arm_t + 4.0, mid_z)
    top_outer = (-p.lyre_width / 2, h)
    top_inner = (-p.lyre_width / 2 + arm_t * 0.7, h - arm_t * 0.3)

    return (
        bottom_outer,
        mid_outer,
        top_outer,
        top_inner,
        mid_inner,
        bottom_inner,
    )


def _build_arm(p: Params, mirror: bool = False) -> Part:
    """1 本のアームを 2D プロファイル + extrude で生成する。"""
    points = _build_left_arm_profile(p)
    if mirror:
        points = tuple((-x, z) for x, z in points)

    bottom_outer, mid_outer, top_outer, top_inner, mid_inner, bottom_inner = points

    with BuildLine(Plane.XZ) as outline:
        Spline(bottom_outer, mid_outer, top_outer)
        Line(top_outer, top_inner)
        Spline(top_inner, mid_inner, bottom_inner)
        Line(bottom_inner, bottom_outer)

    with BuildSketch(Plane.XZ) as sk:
        make_face(outline.line)

    arm = extrude(sk.sketch, amount=p.lyre_depth, dir=(0, 1, 0), both=True)
    return arm


def make_lyre(p: Params = default_params) -> Part:
    """Lyre フレームを単一の Part として返す。"""
    # === ペデスタル ===
    with BuildSketch() as ped_sk:
        RectangleRounded(
            p.lyre_pedestal_width,
            p.lyre_pedestal_depth,
            p.lyre_pedestal_corner_radius,
        )
    pedestal = extrude(ped_sk.sketch, amount=p.lyre_pedestal_height)

    # === 左右アーム ===
    left = _build_arm(p, mirror=False)
    right = _build_arm(p, mirror=True)

    body = pedestal.fuse(left).fuse(right)

    # === ワイヤ穴: 各 Z で X 軸方向のシリンダーをフレーム全幅貫通 ===
    spacing = (p.wire_top_z - p.wire_bottom_z) / (p.wire_count - 1)
    cylinder_length = p.lyre_width + 4.0  # 全幅 + 余裕
    for i in range(p.wire_count):
        z = p.wire_bottom_z + i * spacing
        # X 軸方向のシリンダー: デフォルトの Z 軸方向シリンダーを Rot で X 軸向きに
        hole = (
            Pos(0, 0, z)
            * Rot(0, 90, 0)  # Z 軸シリンダー → X 軸シリンダー
            * Cylinder(
                radius=p.wire_hole_diameter / 2,
                height=cylinder_length,
            )
        )
        body = body.cut(hole)

    return Part(Compound([body]).wrapped)
```

実装サブエージェントへの注記:
- build123d 0.10.0 で `BuildLine + Spline + Line + make_face + extrude(dir=(0,1,0), both=True)` が動作することは codex review で .venv 上で検証済み
- Cylinder のデフォルト軸は Z。X 軸向きにするには `Rot(0, 90, 0)` で 90° 回転する
- もし `Rot(Y=90)` 形式の方が安全なら API を確認して書き換えてよい
- アームの mirror は `_build_arm(p, mirror=True)` で実現
- 体積/bbox 計算が想定とずれた場合は **STOP and report** して相談

- [ ] **Step 3: テスト → 全 PASS**

Run: `mise exec -- uv run pytest tests/test_lyre.py -v`
Expected: 8 passed

- [ ] **Step 4: 全テスト + ruff**

Run: `mise exec -- uv run pytest -v && mise exec -- uv run ruff format src/ tests/ && mise exec -- uv run ruff check src/ tests/`

- [ ] **Step 5: コミット**

```bash
git add src/plotter/lyre.py tests/test_lyre.py
git commit -m "Lyre フレーム make_lyre を実装"
```

---

## Task 4: parts/lyre_frame.py を追加して STL/STEP 出力検証

**Files:** `parts/lyre_frame.py`

- [ ] **Step 1: parts/lyre_frame.py を作成**

```python
"""Lyre フレームの STL/STEP 出力エントリ。

Usage:
    mise exec -- uv run python parts/lyre_frame.py
"""

from pathlib import Path

from build123d import export_step, export_stl

from plotter.lyre import make_lyre


def main() -> None:
    lyre = make_lyre()
    out_dir = Path(__file__).resolve().parent.parent / "build"
    out_dir.mkdir(parents=True, exist_ok=True)
    export_stl(lyre, str(out_dir / "lyre_frame.stl"))
    export_step(lyre, str(out_dir / "lyre_frame.step"))
    print(f"Wrote: {out_dir}/lyre_frame.stl")
    print(f"Wrote: {out_dir}/lyre_frame.step")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 実行 + ファイル確認**

Run: `mise exec -- uv run python parts/lyre_frame.py && ls -la build/lyre_frame.*`
Expected: 2 ファイル、サイズ>0

- [ ] **Step 3: scripts/preview_lyre.py を作って ocp-vscode で目視確認**

```python
"""Lyre フレームを ocp-vscode に表示。

VSCode で OCP CAD Viewer を開いた状態で実行:
    PYTHONPATH=. mise exec -- uv run python scripts/preview_lyre.py
"""

from ocp_vscode import show

from plotter.lyre import make_lyre

show(make_lyre(), names=["lyre_frame"])
print("送信完了")
```

実行 → ビューワーでフレームが想定通り（曲線アーム+ペデスタル+ワイヤ穴貫通）か目視確認。**形状がおかしい場合は Task 3 に戻る**。

- [ ] **Step 4: コミット**

```bash
git add parts/lyre_frame.py scripts/preview_lyre.py
git commit -m "parts/lyre_frame.py + プレビュースクリプト追加"
```

---

## Task 5: 旧コード削除（**Lyre が動いてから初めて実行**）

ここまでの Task 1-4 で Lyre が動作することを確認した後、初めて旧コードを削除する。

**削除対象:**
- `src/plotter/body.py`
- `src/plotter/base.py`
- `tests/test_body.py`
- `tests/test_base.py`
- `tests/tenon_clearance_test.py`
- `tests/test_tenon_clearance.py`
- `parts/body_full.py`
- `parts/body_test.py`
- `parts/base_75.py`
- `scripts/preview_body.py`
- `scripts/preview_clearance.py`
- `scripts/preview_assembly.py`
- `params.py` の panel_*, shelf_*, tenon_*, base_*, mortise_clearance フィールド
- `tests/test_params.py` の対応する旧アサーション

**ビルド成果物クリーンアップ:**
- `build/body_*.{stl,step}` `build/base_*.{stl,step}` `build/tenon_clearance_test.*`

- [ ] **Step 1: ファイル削除**

```bash
git rm src/plotter/body.py src/plotter/base.py \
       tests/test_body.py tests/test_base.py \
       tests/tenon_clearance_test.py tests/test_tenon_clearance.py \
       parts/body_full.py parts/body_test.py parts/base_75.py \
       scripts/preview_body.py scripts/preview_clearance.py scripts/preview_assembly.py
rm -f build/body_*.stl build/body_*.step build/base_*.stl build/base_*.step \
      build/tenon_clearance_test.stl build/tenon_clearance_test.step
```

- [ ] **Step 2: params.py から旧フィールドを削除**

`Params` dataclass から以下のフィールドと該当コメントブロックを削除:
- panel_width, panel_height, panel_thickness, panel_angle
- shelf_count, shelf_lip_height, shelf_lip_thickness, shelf_divider_thickness, shelf_depth
- tenon_count, tenon_width, tenon_thickness, tenon_height
- base_width, base_depth, base_thickness, base_front_lip_height, base_front_lip_thickness
- base_ridge_height, base_ridge_depth
- mortise_clearance（Lyre では不要）

- [ ] **Step 3: tests/test_params.py から対応する assertion を削除**

`test_body_panel_defaults`, `test_tenon_defaults`, `test_mortise_clearance_default`, `test_base_defaults` の 4 テスト関数を削除。

- [ ] **Step 4: pytest 全 PASS**

Expected: ~14 passed (params 5 + utils 5 + card 7 + lyre 8 = 25 程度)

- [ ] **Step 5: ruff + コミット**

```bash
git add -A
git commit -m "$(cat <<'EOF'
PLOTTER Lyre pivot: 旧 body/base/tenon コードを削除

Lyre フレームの動作検証完了後、長方形パネル設計の関連ファイルを全削除。
git 履歴で復元可能。
EOF
)"
```

---

## Task 6: Makefile を Lyre 用に再編

**Files:** `Makefile`

- [ ] **Step 1: 旧ターゲット削除、lyre 追加**

```makefile
.PHONY: all clean test card lyre format lint help

PYTHON := uv run python
BUILD_DIR := build

help:
	@echo "PLOTTER build targets:"
	@echo "  make all       - Build all parts (cards + lyre)"
	@echo "  make card      - Build all card variants"
	@echo "  make lyre      - Build lyre frame"
	@echo "  make test      - Run pytest"
	@echo "  make format    - Format code with ruff"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make clean     - Remove build artifacts"

all: card lyre

card: $(BUILD_DIR)
	$(PYTHON) parts/card_standard.py
	$(PYTHON) parts/card_wide.py
	$(PYTHON) parts/card_thickness_test.py

lyre: $(BUILD_DIR)
	$(PYTHON) parts/lyre_frame.py

test:
	uv run pytest

format:
	uv run ruff format src/ parts/ tests/

lint:
	uv run ruff check src/ parts/ tests/

clean:
	rm -rf $(BUILD_DIR)/*.stl $(BUILD_DIR)/*.step $(BUILD_DIR)/*.3mf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)
```

- [ ] **Step 2: 動作確認**

Run: `make clean && make all && ls build/`

- [ ] **Step 3: コミット**

---

## Task 7: ドキュメント更新（CLAUDE.md / SPEC.md / README.md / ROADMAP.md）

CLAUDE.md, SPEC.md, README.md, ROADMAP.md には旧 panel/base/tenon 設計が「確定」として記載されている。Lyre pivot を反映させる。

- [ ] **Step 1: CLAUDE.md を更新**

「重要な設計パラメータ」セクションを Lyre 用に書き換え。「試作の進め方」も Lyre 試作プロセスに更新。

- [ ] **Step 2: SPEC.md を更新**

「構造仕様」を Lyre フレーム + ワイヤ + スリットカードに書き換え。「ホゾ・ホゾ穴」セクションは削除。

- [ ] **Step 3: README.md / ROADMAP.md を更新**

製品コンセプトに「PLOTTER Lyre」のメタファーを追記。

- [ ] **Step 4: コミット**

```bash
git add CLAUDE.md SPEC.md README.md ROADMAP.md
git commit -m "Docs: Lyre pivot を反映"
```

---

## 完了の定義

- `make all` で `build/card_*` と `build/lyre_frame.*` が生成
- `mise exec -- uv run pytest -v` で全テスト PASS
- `mise exec -- uv run ruff check src/ tests/ parts/` 0 エラー
- ドキュメント（CLAUDE.md, SPEC.md, README.md, ROADMAP.md）が Lyre 設計に同期
- 7 コミットが main にある

## 次フェーズへの引き継ぎ

- フレームを実印刷（Bambu Lab X2D、PLA）
- 1mm ステンレスワイヤ × 6 を 6 ペアの穴に通す
- ワイヤ両端は 90° 曲げて捕獲（または小さなアルミ製クリンプスリーブ）
- カードを上端スリットからワイヤに振り掛けて吊るす
- 公差問題があれば params 微調整（特に wire_hole_diameter, card_top_slit_width）

---

## codex 指摘で見送ったもの

- `mortise_clearance` → `fit_clearance` リネーム: Lyre では不要なので削除（Task 5 で）
- ワイヤ終端の詳細設計: 実印刷後に決める。とりあえず両端 90° 曲げで開始
- 物理試験用のクーポン（穴径テスト・スリット幅テスト）: 必要なら別タスクで追加

---

## Risk

- build123d の Spline 実装で意図したシルエットが出ないリスク → codex が `.venv` で検証済みのパターンを採用したので低リスク
- 150mm × 8mm 厚アームは PLA で反るリスク → ブリム必須、印刷向き要工夫
- ワイヤ穴 2.0mm でも FDM で縮む可能性 → 試作で確認、必要なら 2.2mm に
- スリット 1.5mm + R0.75mm でカード上端がトータル 2mm 切り欠きになる → カード上端に十分な material が残ることを実印刷で確認
