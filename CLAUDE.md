# Claude Code 向け作業指示

このプロジェクトは PLOTTER という3Dプリント製品の設計・実装プロジェクトです。
Claude Code は build123d でのモデリング、Python パッケージ構成、テスト・ビルド設定を担当します。

## プロジェクトの本質

PLOTTER は「キーバインド学習装置」です。覚えにくいキーバインドを物理カードで机に並べる。
**「単なる物理チートシート」ではなく「カードを部品として組み合わせて自分のキーバインドを構成する」**
という発想が中核です。自分の dotfiles からカードを刷り、机の上で並び替えながら学ぶ。この本質を見失わないこと。

## 技術スタック

- **CAD**: [build123d](https://github.com/gumyr/build123d) 0.10+（OpenCascade ベースの Python CAD）
- **Python**: 3.13+
- **依存管理**: uv（rye/poetry ではなく uv を採用）
- **バージョン管理**: mise
- **テスト**: pytest
- **ビルド**: Makefile + Python スクリプト
- **3Dプリンタ**: Bambu Lab X2D（デュアルノズル）
- **素材**: PLA（Wedge・Drawer・カード）
- **ツール実行**: `mise exec -- uv run` 経由

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

`parts/*.py` は 1 ファイル 1 パーツ。
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
# tests/test_card.py
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
    card_width_std: float = 30.0        # 標準カード幅
    card_width_wide: float = 60.0       # ワイドカード幅（修飾キー用）
    card_height: float = 30.0           # カード高さ
    card_thickness: float = 2.0         # カード厚（試作で 2.5/3.0 も検討）
    card_corner_radius: float = 3.0     # カード角 R

    # === Wedge body ===
    wedge_width: float = 200.0          # X 方向（左右）
    wedge_depth: float = 200.0          # Y 方向（前後）
    wedge_front_thickness: float = 20.0 # 前縁の厚さ（ドロワー収容のため）
    wedge_back_thickness: float = 50.0  # 後縁の厚さ（傾斜角維持のため）
    wedge_fillet_radius: float = 4.0    # 全エッジ R

    # === Drawer ===
    drawer_width: float = 180.0         # X 方向（ウェッジ内幅 - 余裕）
    drawer_depth: float = 150.0         # Y 方向（前縁から後縁手前まで）
    drawer_height: float = 12.0         # Z 方向（厚み）
    drawer_clearance: float = 0.4       # ウェッジキャビティとのスライド隙間 ★試作で調整
    drawer_wall_thickness: float = 2.0  # ドロワー外壁の厚み
    drawer_floor_offset_z: float = 4.0  # ウェッジ底からドロワー底面までの Z オフセット
    drawer_handle_width: float = 60.0   # 取っ手バーの横幅
    drawer_handle_height: float = 4.0   # 取っ手バーの縦幅
    drawer_handle_protrusion: float = 5.0 # 前面からの突出量
    drawer_handle_fillet: float = 1.5   # 取っ手エッジ R

    # === Card slots（上面傾斜面に切るスロット） ===
    # 列の仕切りはなし。各行 1 本の長スロット。
    card_slot_rows: int = 6
    card_slot_length: float = 180.0     # 各スロットの長さ（X 方向）
    card_slot_pocket_depth: float = 8.0 # 上面に対する垂直深さ
    card_slot_clearance: float = 0.5    # 厚み方向のクリアランス ★試作で調整
    card_slot_face_pitch: float = 33.0  # 上面に沿った行間隔

params = Params()
```

## 試作の進め方

### Step 1: 試作セット印刷（半日）

最小ダメージの半スケール版から始める。

```bash
make test-set
```

- `build/wedge_test.stl` — 半スケール Wedge
- `build/drawer_test.stl` — 半スケール Drawer
- `build/card_thickness_test.stl` — 厚み検証（1.5/2/2.5/3mm）

Bambu Studio でツリーサポートを設定して印刷。確認ポイント：
- カードスロットへの差し込み感
- Drawer のスライド感
- 全体の安定性

### Step 2: 公差確認 & パラメータ調整（半日）

実測結果を `params.py` に反映：

- `card_slot_clearance`: カードがきつい → 増やす、緩い → 減らす
- `drawer_clearance`: Drawer が固い → 増やす、ぐらつく → 減らす

調整後は `make test` でテストが通ることを確認してから次へ進む。

### Step 3: フル版印刷（1 日）

```bash
make wedge
make drawer
```

フル版（200×200mm）を印刷し、カード 36 枚を並べて安定性を最終確認。

### Step 4: カード一式印刷（複数日）

```bash
make card
```

X2D ベッドに 36 枚同時印刷。111 枚を複数バッチで印刷。
カードの内容は `docs/CARDS.md` を参照。

## build123d でハマりやすい点

### a. プレビューには ocp-vscode を使う

build123d はビューワーが標準同梱されない。VSCode 拡張 [ocp-vscode](https://github.com/bernhard-42/vscode-ocp-cad-viewer) で表示するのが標準的。

```python
from ocp_vscode import show

with BuildPart() as wedge:
    # ...
    pass

show(wedge)
```

### b. 単位はミリメートル前提

build123d はデフォルトで mm。インチ系の関数を呼ばないように注意。

### c. fillet の対象選択

エッジ選択は `Selector` 構文を使う：

```python
# Z 方向に伸びるエッジ全部にフィレット
fillet(part.edges().filter_by(Axis.Z), radius=3)

# 特定の面のエッジ
fillet(part.faces().sort_by(Axis.Z)[-1].edges(), radius=1)
```

### d. STEP 出力でアセンブリ表現

複数部品を STEP に出す時、`Compound` でラップする：

```python
from build123d import Compound
asm = Compound(label="plotter", children=[wedge, drawer])
asm.export_step("build/assembly.step")
```

### e. extrude(both=True) の解釈

`extrude(amount=X, both=True)` は両方向に X ずつ（合計 2X）伸ばす。
スロットの切り込みなど、スケッチ面を中心に対称に切りたい場合に使う。

```python
# スロット切り込み（both=True で上面スケッチを中心に上下 4mm ずつ切る）
extrude(amount=4, mode=Mode.SUBTRACT, both=True)
```

### f. インスタンス化のコスト

build123d のオブジェクト生成は OpenCascade 呼び出しが入るので、ループ内で大量生成すると遅い。
カード 111 枚を 1 スクリプトで生成しようとすると重い。
**カード生成は別プロセスで並列化** or **個別ファイルに分ける**。

## Makefile

```makefile
.PHONY: all clean test card wedge drawer wedge-test drawer-test test-set format lint help

PYTHON := uv run python
BUILD_DIR := build

all: card wedge drawer

card: $(BUILD_DIR)
    $(PYTHON) parts/card_standard.py
    $(PYTHON) parts/card_wide.py
    $(PYTHON) parts/card_thickness_test.py

wedge: $(BUILD_DIR)
    $(PYTHON) parts/wedge.py

drawer: $(BUILD_DIR)
    $(PYTHON) parts/drawer.py

wedge-test: $(BUILD_DIR)
    $(PYTHON) parts/wedge_test.py

drawer-test: $(BUILD_DIR)
    $(PYTHON) parts/drawer_test.py

test-set: wedge-test drawer-test card

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

## pyproject.toml

```toml
[project]
name = "plotter"
version = "0.1.0"
description = "PLOTTER - Physical key-binding learning device"
requires-python = ">=3.13"
dependencies = [
    "build123d>=0.10.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0",
    "ruff>=0.5",
    "ocp-vscode>=2.0",
]

[tool.ruff]
line-length = 100
target-version = "py313"

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
│   ├── wedge.py         # Wedge 本体生成関数
│   ├── drawer.py        # Drawer 生成関数
│   └── utils.py         # 共通関数
├── parts/               # エントリポイント（実行可能）
│   ├── card_standard.py
│   ├── card_wide.py
│   ├── card_thickness_test.py
│   ├── wedge.py
│   ├── wedge_test.py    # 半スケール試作
│   ├── drawer.py
│   └── drawer_test.py   # 半スケール試作
├── assemblies/
│   └── full_assembly.py
├── tests/
│   ├── test_card.py
│   ├── test_wedge.py
│   ├── test_drawer.py
│   ├── test_params.py
│   └── test_utils.py
└── build/               # gitignore
```

## 実装順序（推奨）

1. **`src/plotter/params.py`**: パラメータ dataclass を定義
2. **`src/plotter/utils.py`**: 角丸矩形などの共通関数
3. **`src/plotter/card.py`**: カード生成関数
4. **`tests/test_card.py`**: カードの寸法テスト
5. **`parts/card_standard.py`**, **`parts/card_wide.py`**: STL 出力エントリ
6. **`src/plotter/wedge.py`**: Wedge 本体生成関数
7. **`tests/test_wedge.py`**: Wedge の寸法テスト
8. **`src/plotter/drawer.py`**: Drawer 生成関数
9. **`tests/test_drawer.py`**: Drawer の寸法テスト
10. **`assemblies/full_assembly.py`**: 全体組立図

各ステップで `mise exec -- uv run pytest` を通してから次に進む。

## やってはいけないこと

### パラメータをハードコードしない

`src/plotter/wedge.py` の中で `wedge_width = 200` と書いてはいけない。
必ず `params` から参照する。

```python
# NG
def make_wedge():
    return Box(200, 200, 50)

# OK
def make_wedge(p: Params):
    return Box(p.wedge_width, p.wedge_depth, p.wedge_back_thickness)
```

### STL/STEP を Git にコミットしない

`build/*.stl`, `build/*.step` は `.gitignore` に追加。再現可能なビルドが原則。

### カードスロット・Drawer の公差を仮定で決め打ちしない

`card_slot_clearance = 0.5` と `drawer_clearance = 0.4` は**初期値**。実印刷の結果で必ず調整する。
第 1 試作（試作セット）の前に公差調整を前提とした設計にしておくこと。

### カードの内容を勝手に変えない

カード 111 枚の内容は `docs/CARDS.md` に確定済み。
Shoma さんの dotfiles から抽出した結果なので、変更は確認を取ること。

### ブランド名を変えない

PLOTTER で確定。商標調査は別途進行中。

### build123d ではなく cadquery や OpenSCAD を使わない

このプロジェクトは build123d で統一。同類の CadQuery のコードを混入させない。

## 参照すべきドキュメント

- [`README.md`](./README.md) — プロジェクト概要
- [`SPEC.md`](./SPEC.md) — 物理仕様の詳細・公差設計
- [`CARDS.md`](./CARDS.md) — カード 111 枚の完全リスト
- [`ROADMAP.md`](./ROADMAP.md) — フェーズ別の作業内容

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
