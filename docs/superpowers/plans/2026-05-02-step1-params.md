# Step 1: Params dataclass 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** PLOTTER 全部品の寸法・公差を1箇所に集約した `frozen` dataclass `Params` と、モジュールレベルのシングルトン `params` を `src/plotter/params.py` に定義する。

**Architecture:** `dataclasses.dataclass(frozen=True)` で不変な値オブジェクトを定義する。全モジュール（card.py / body.py / base.py）は `from plotter.params import params` でこのシングルトンを参照する。`frozen=True` によりタイポや意図しない上書きを実行時に検出する。

**Tech Stack:** Python 3.13 標準ライブラリ（`dataclasses`）、pytest

---

## File Structure

- Create: `src/plotter/__init__.py` — パッケージマーカー（空）
- Create: `src/plotter/params.py` — `Params` dataclass と `params` シングルトン
- Create: `tests/__init__.py` — テストパッケージマーカー（空）
- Create: `tests/test_params.py` — Params の不変性とデフォルト値テスト

各ファイルの責務は1つだけ。`params.py` は他モジュールに **依存しない** 葉ノード。

---

## Task 1: パッケージスケルトンを作る

**Files:**
- Create: `src/plotter/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: 空の `src/plotter/__init__.py` を作成**

```python
```

(完全に空のファイル)

- [ ] **Step 2: 空の `tests/__init__.py` を作成**

```python
```

(完全に空のファイル)

- [ ] **Step 3: pyproject.toml の hatch 設定が src/plotter を認識するか確認**

Run: `mise exec -- uv run python -c "import plotter; print(plotter.__file__)"`
Expected: `/Users/shoma/dev/github.com/ignission/plotter/src/plotter/__init__.py`

- [ ] **Step 4: コミット**

```bash
git add src/plotter/__init__.py tests/__init__.py
git commit -m "plotter パッケージとテストの骨格を追加"
```

---

## Task 2: Params dataclass のテストを先に書く（RED）

**Files:**
- Create: `tests/test_params.py`

- [ ] **Step 1: テストファイル全体を一気に書く**

```python
"""Params dataclass の不変性とデフォルト値テスト。"""

import dataclasses

import pytest

from plotter.params import Params, params


def test_params_is_frozen_dataclass():
    """Params は frozen=True の dataclass であること。"""
    assert dataclasses.is_dataclass(Params)
    assert Params.__dataclass_params__.frozen is True


def test_params_singleton_is_instance():
    """モジュールレベルで params シングルトンが Params のインスタンスとして
    エクスポートされていること。"""
    assert isinstance(params, Params)


def test_params_cannot_be_mutated():
    """frozen=True により属性代入が FrozenInstanceError になること。"""
    with pytest.raises(dataclasses.FrozenInstanceError):
        params.card_thickness = 99.0  # type: ignore[misc]


def test_card_defaults():
    """Card パラメータのデフォルト値が SPEC.md と一致すること。"""
    assert params.card_width_std == 30.0
    assert params.card_width_wide == 60.0
    assert params.card_height == 30.0
    assert params.card_thickness == 2.0
    assert params.card_corner_radius == 3.0


def test_body_panel_defaults():
    """本体パネルのデフォルト値。"""
    assert params.panel_width == 200.0
    assert params.panel_height == 200.0
    assert params.panel_thickness == 3.0
    assert params.panel_angle == 75.0
    assert params.shelf_count == 6
    assert params.shelf_lip_height == 5.0
    assert params.shelf_lip_thickness == 2.0
    assert params.shelf_divider_thickness == 2.0


def test_tenon_defaults():
    """ホゾ（本体下端の凸）のデフォルト値。"""
    assert params.tenon_count == 5
    assert params.tenon_width == 14.0
    assert params.tenon_thickness == 2.0
    assert params.tenon_height == 20.0


def test_mortise_clearance_default():
    """ホゾ穴クリアランスは試作で実測調整される初期値。"""
    assert params.mortise_clearance == 0.2


def test_base_defaults():
    """土台のデフォルト値。"""
    assert params.base_width == 200.0
    assert params.base_depth == 50.0
    assert params.base_thickness == 4.0
    assert params.base_front_lip_height == 3.0
    assert params.base_front_lip_thickness == 2.0
```

- [ ] **Step 2: テストを実行して FAIL することを確認（RED）**

Run: `mise exec -- uv run pytest tests/test_params.py -v`
Expected: `ModuleNotFoundError: No module named 'plotter.params'`（または `ImportError`）

---

## Task 3: Params dataclass の実装（GREEN）

**Files:**
- Create: `src/plotter/params.py`

- [ ] **Step 1: `src/plotter/params.py` を実装**

```python
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
```

- [ ] **Step 2: テスト実行 → 全 PASS（GREEN）**

Run: `mise exec -- uv run pytest tests/test_params.py -v`
Expected: 8 passed

- [ ] **Step 3: ruff で format & lint**

Run: `mise exec -- uv run ruff format src/ tests/ && mise exec -- uv run ruff check src/ tests/`
Expected: format で変更なし or 自動整形のみ、check で 0 エラー

- [ ] **Step 4: コミット**

```bash
git add src/plotter/params.py tests/test_params.py
git commit -m "Params dataclass を実装

全部品の寸法・公差を frozen dataclass に集約。
他モジュールは plotter.params.params シングルトンを参照する。"
```

---

## 完了の定義

- `mise exec -- uv run pytest tests/test_params.py -v` が 8 PASS
- `mise exec -- uv run ruff check src/ tests/` が 0 エラー
- `from plotter.params import params` が他モジュールから可能
- 3コミットが main にある（パッケージ骨格、テスト追加は不要 — Task 2/3 はTDD で1コミットにまとめる）

## 次フェーズへの引き継ぎ

- Step 2（公差検証パーツ）と Step 3（カード生成）は params をインポートして使う
- params の値変更は **このファイルのみ** で完結する（変更時は全テスト再実行）
- `mortise_clearance` は試作前に `tenon_clearance_test.py` で実測調整される前提

---

## Self-Review

**Spec coverage（CLAUDE.md と照合）:**
- ✅ Card パラメータ 5項目
- ✅ Body Panel パラメータ 8項目
- ✅ Tenon パラメータ 4項目
- ✅ Mortise パラメータ 1項目
- ✅ Base パラメータ 5項目
- ✅ `frozen=True` 指定
- ✅ `params = Params()` シングルトン

**Placeholder scan:** TODO/TBD/「適切な〜」「テストを書く」のような曖昧表現なし。

**Type consistency:** `Params` クラス名・`params` インスタンス名・属性名すべて統一。
