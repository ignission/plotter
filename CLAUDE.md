# Claude Code 向け作業指示

このプロジェクトは PLOTTER という3Dプリント製品の設計・実装プロジェクトです。
Claude Code は build123d でのモデリング、Python パッケージ構成、テスト・ビルド設定を担当します。

## プロジェクトの本質

PLOTTER は「キーバインド学習装置」です。覚えにくいキーバインドを物理カードで机に並べる。
**「単なる物理チートシート」ではなく「カードを部品として組み合わせて自分のキーバインドを構成する」**
という発想が中核です。この本質を見失わないこと。

## 技術スタック

- **CAD**: [build123d](https://github.com/gumyr/build123d) 0.6+ （OpenCascade ベースの Python CAD）
- **Python**: 3.11+
- **依存管理**: uv（rye/poetry ではなく uv を採用）
- **テスト**: pytest
- **ビルド**: Makefile + Python スクリプト
- **3Dプリンタ**: Bambu Lab X2D（デュアルノズル、65℃チャンバー）
- **素材**: PLA（本体・カード）、TPU（底面滑り止め）

## build123d 設計原則

### 1. 全パラメータを `src/plotter/params.py` に集約

寸法・公差・色などすべての可変値を `params.py` の dataclass にまとめる。
他のモジュールからは `from plotter.params import params` で参照する。
パラメータ変更で全体が連動して変わるように設計する。

### 2. パーツ生成は `BuildPart` コンテキストマネージャで

build123d の慣用句に従う：

```python
from build123d import *

with BuildPart() as card:
    with BuildSketch() as sk:
        RectangleRounded(width=30, height=30, radius=3)
    extrude(amount=2)
```

### 3. パーツファイルは単一責務

`parts/*.py` は1ファイル1パーツ。
スクリプトとして実行すると、対応する STL/STEP を `build/` に出力する。

```python
# parts/card_standard.py
from plotter.card import make_standard_card
from plotter.params import params

if __name__ == "__main__":
    card = make_standard_card(params)
    card.export_stl("build/card_standard.stl")
    card.export_step("build/card_standard.step")
```

### 4. テスト駆動で公差を管理

寸法のリグレッションテストを必ず書く：

```python
# tests/test_dimensions.py
def test_card_standard_bbox():
    card = make_standard_card(params)
    bbox = card.bounding_box()
    assert bbox.size.X == pytest.approx(30, abs=0.01)
    assert bbox.size.Y == pytest.approx(30, abs=0.01)
    assert bbox.size.Z == pytest.approx(2, abs=0.01)
```

### 5. 共通モジュールを `src/plotter/utils.py` に

角丸スケッチ、フィレット適用などの汎用関数はここに集約。

## 重要な設計パラメータ

これらは**現時点での確定値**。変更する場合はユーザー（Shoma さん）に確認すること。

```python
# src/plotter/params.py
from dataclasses import dataclass

@dataclass(frozen=True)
class Params:
    # === Card ===
    card_width_std: float = 30.0      # 標準カード幅
    card_width_wide: float = 60.0     # ワイドカード幅（修飾キー用）
    card_height: float = 30.0         # カード高さ
    card_thickness: float = 2.0       # カード厚（試作で2.5/3.0も検討）
    card_corner_radius: float = 3.0   # カード角R

    # === Body Panel ===
    panel_width: float = 200.0
    panel_height: float = 200.0
    panel_thickness: float = 3.0
    panel_angle: float = 75.0         # 標準角度（土台で決定）

    shelf_count: int = 6              # 棚の数
    shelf_lip_height: float = 5.0
    shelf_lip_thickness: float = 2.0
    shelf_divider_thickness: float = 2.0

    # === Tenon (本体下端の凸) ===
    tenon_count: int = 5
    tenon_width: float = 14.0
    tenon_thickness: float = 2.0
    tenon_height: float = 20.0

    # === Mortise (土台側の穴) ===
    mortise_clearance: float = 0.2    # ★ 試作で実測調整必須

    # === Base ===
    base_width: float = 200.0
    base_depth: float = 50.0
    base_thickness: float = 4.0
    base_front_lip_height: float = 3.0
    base_front_lip_thickness: float = 2.0

params = Params()
```

## 試作の進め方

### Step 1: カード単体試作（半日）

最小単位から始める。失敗してもダメージが少ない。

- `src/plotter/card.py` を実装
- `parts/card_standard.py` でエントリポイント作成
- 厚み 1.5 / 2 / 2.5 / 3mm を一度に印刷（パラメータを変えて4ファイル生成）
- 反り・色合い・触り心地を実物確認
- → 厚みを確定する

### Step 2: 公差検証パーツ（半日）

ホゾ・ホゾ穴の公差を実測で決める。これが**最大のリスクポイント**。

- `tests/tenon_clearance_test.py` を実装
- 隙間 0.1 / 0.15 / 0.2 / 0.25 / 0.3mm の5バリエーションを一括生成
- 1回の印刷でベストフィットを発見
- 結果を `params.py` の `mortise_clearance` に反映

### Step 3: 本体パネル試作（1日）

- `src/plotter/body.py` を実装
- まず1/4スケール（panel_width=50）で動作確認
- 問題なければフルスケール（panel_width=200）

### Step 4: 土台試作（1日）

- `src/plotter/base.py` を実装
- 角度パラメータで75°/60°/90°を切替可能に
- 75°版を最初に出す

### Step 5: 組立試験

- `assemblies/full_assembly.py` で全部品を組み合わせ
- 36枚カードを置いて重心・安定性確認
- カードの抜き差し感、リップの効き、本体の倒れにくさ

## build123d でハマりやすい点

### a. プレビューには ocp-vscode を使う

build123d はビューワーが標準同梱されない。VSCode 拡張 [ocp-vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) で表示するのが標準的。

```python
from ocp_vscode import show

with BuildPart() as card:
    # ...
    pass

show(card)
```

### b. 単位はミリメートル前提

build123d はデフォルトで mm。インチ系の関数を呼ばないように注意。

### c. fillet の対象選択

エッジ選択は `Selector` 構文を使う：

```python
# Z 方向に伸びるエッジ全部にフィレット
fillet(card.edges().filter_by(Axis.Z), radius=3)

# 特定の面のエッジ
fillet(card.faces().sort_by(Axis.Z)[-1].edges(), radius=1)
```

### d. STEP 出力でアセンブリ表現

複数部品を STEP に出す時、`Compound` でラップする：

```python
from build123d import Compound
asm = Compound(label="plotter", children=[body, base])
asm.export_step("build/assembly.step")
```

### e. インスタンス化のコスト

build123d のオブジェクト生成は OpenCascade 呼び出しが入るので、ループ内で大量生成すると遅い。
ホゾ5本のような少量なら問題ないが、カード111枚を1スクリプトで生成しようとすると重い。
**カード生成は別プロセスで並列化** or **個別ファイルに分ける**。

## Makefile 例

```makefile
.PHONY: all clean test card body base

PYTHON := uv run python
BUILD_DIR := build

all: card body base

card:
	$(PYTHON) parts/card_standard.py
	$(PYTHON) parts/card_wide.py

body:
	$(PYTHON) parts/body_6row.py

base:
	$(PYTHON) parts/base_75.py
	$(PYTHON) parts/base_60.py
	$(PYTHON) parts/base_90.py

test:
	uv run pytest -v

clean:
	rm -rf $(BUILD_DIR)/*.stl $(BUILD_DIR)/*.step

format:
	uv run ruff format src/ parts/ tests/ assemblies/

lint:
	uv run ruff check src/ parts/ tests/ assemblies/
```

## pyproject.toml（推奨設定）

```toml
[project]
name = "plotter"
version = "0.1.0"
description = "PLOTTER - Physical key-binding learning device"
requires-python = ">=3.11"
dependencies = [
    "build123d>=0.6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.5",
    "ocp-vscode>=2.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "ruff>=0.5",
    "ocp-vscode>=2.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
```

## ディレクトリ構成

```
plotter/
├── pyproject.toml
├── Makefile
├── README.md
├── CLAUDE.md
├── .gitignore           # build/ を除外
├── docs/
│   ├── SPEC.md
│   ├── CARDS.md
│   └── ROADMAP.md
├── src/plotter/
│   ├── __init__.py
│   ├── params.py        # ★ 全パラメータ
│   ├── card.py          # カード生成関数
│   ├── body.py          # 本体パネル
│   ├── base.py          # 土台
│   └── utils.py         # 共通関数
├── parts/               # エントリポイント（実行可能）
│   ├── card_standard.py
│   ├── card_wide.py
│   ├── body_6row.py
│   ├── base_75.py
│   ├── base_60.py
│   └── base_90.py
├── assemblies/
│   └── full_assembly.py
├── tests/
│   ├── test_dimensions.py
│   ├── test_card.py
│   ├── test_body.py
│   ├── test_base.py
│   └── tenon_clearance_test.py
└── build/               # gitignore
```

## 実装順序（推奨）

1. **環境セットアップ**: `uv init`, `uv add build123d`, `pyproject.toml` 整備
2. **`src/plotter/params.py`**: パラメータ dataclass を定義
3. **`src/plotter/utils.py`**: 角丸矩形などの共通関数
4. **`src/plotter/card.py`**: カード生成関数
5. **`tests/test_card.py`**: カードの寸法テスト
6. **`parts/card_standard.py`**, **`parts/card_wide.py`**: STL 出力エントリ
7. **`tests/tenon_clearance_test.py`**: 公差検証パーツ
8. **`src/plotter/body.py`**: 本体パネル
9. **`src/plotter/base.py`**: 土台
10. **`assemblies/full_assembly.py`**: 全体組立図

各ステップで pytest を通してから次に進む。

## やってはいけないこと

### ❌ パラメータをハードコードしない

`src/plotter/body.py` の中で `panel_width = 200` と書いてはいけない。
必ず `params` から参照する。

```python
# ❌ Bad
def make_body():
    return Box(200, 200, 3)

# ✅ Good
def make_body(p: Params):
    return Box(p.panel_width, p.panel_height, p.panel_thickness)
```

### ❌ STL/STEP を Git にコミットしない

`build/*.stl`, `build/*.step` は `.gitignore` に追加。再現可能なビルドが原則。

### ❌ ホゾ・ホゾ穴の公差を仮定で決め打ちしない

`mortise_clearance = 0.2` は**初期値**。実印刷の結果で必ず調整する。
第1試作の前に公差検証パーツ（Step 2）を必ず実行する。

### ❌ カードの内容を勝手に変えない

カード111枚の内容は `docs/CARDS.md` に確定済み。
Shoma さんの dotfiles から抽出した結果なので、変更は確認を取ること。

### ❌ ブランド名を変えない

PLOTTER で確定。商標調査は別途進行中。

### ❌ build123d ではなく cadquery や OpenSCAD を使わない

このプロジェクトは build123d で統一。同類の CadQuery のコードを混入させない。

## 参照すべきドキュメント

- [`README.md`](./README.md) — プロジェクト概要
- [`docs/SPEC.md`](./docs/SPEC.md) — 物理仕様の詳細・公差設計
- [`docs/CARDS.md`](./docs/CARDS.md) — カード111枚の完全リスト
- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — フェーズ別の作業内容

## 外部リソース

- [build123d ドキュメント](https://build123d.readthedocs.io/)
- [build123d GitHub](https://github.com/gumyr/build123d)
- [build123d examples](https://github.com/gumyr/build123d/tree/dev/examples)
- [ocp-vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) — VSCode プレビュー

## 連絡

詰まった点・判断に迷う点があれば、コミットメッセージや Issue で記録し、
Shoma さんに確認を求めること。

---

**重要**: このプロジェクトは Shoma さん本人の dotfiles に基づく **Shoma さん専用 MVP** から始まる。
最初の試作は Shoma さんの机で動くことが最優先。商品化は試作完成後に検討する。
