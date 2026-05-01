# PLOTTER

> キーバインドを、プロットする。
> *Plot your bindings.*

覚えにくいキーバインドを物理カードで机に並べる学習装置。動詞・修飾キー・文字キーを部品として組み合わせ、自分の使うコマンドを物理的に構成する。覚えたら外す、新しく学ぶものが増えたら足す。

## なぜ作るのか

LazyVim、AeroSpace、Claude Code、Git…。エンジニアの机には覚えるべきキーバインドが多すぎる。デジタルなチートシートはアプリを開かないと見えない。紙のメモは机に散らかる。Anki などのフラッシュカードアプリは「覚えた/覚えてない」をボタンで操作するだけで身体感覚が伴わない。

PLOTTER は、**キーバインドを物理化して机の上に常駐させる**装置。視界に入るたびに無意識で覚える。覚えたカードは取り外し、空きセルには新しく学びたいキーバインドを差す。**学習の進捗が物理的に可視化される**。

## 商品構成

| 商品 | 内容 | 価格 |
|---|---|---|
| **PLOTTER Stand Set** | 本体 + 75°土台 + Core 60 カードセット | 9,800円 |
| **PLOTTER Stand** | 本体 + 75°土台のみ | 5,800円 |
| **PLOTTER Cards: Core 60** | カード111枚（動詞60 + 修飾5 + アルファベット26 + 数字10 + 特殊10） | 4,800円 |
| **PLOTTER Tilt 60° / 90°** | 角度切替用の追加土台 | 各1,800円 |
| **PLOTTER Cards: Verb Pack** | 拡張動詞カード（将来） | 2,800円 |

## 物理仕様

- **構造**：L字（底板 + 背板棚式）、2部品差込式（ホゾ・ホゾ穴接続）
- **寸法**：幅200mm × 高さ200mm × 奥行120mm
- **棚**：6行、横方向の仕切りなし
- **角度**：標準75°、土台SKU展開で60°/90°対応
- **素材**：本体 PLA + 底面 TPU
- **重量**：約170g
- **部品点数**：本体1 + 土台1

## カード仕様

- **標準カード**：30×30×2mm
- **ワイドカード**：60×30×2mm（修飾キー専用）
- **角R**：3mm
- **印刷**：X2D デュアルカラー、文字エンボス方式
- **フォント**：日本語 Noto Sans JP Bold、英字 JetBrains Mono Bold
- **配色**：動詞=黄、修飾キー=紫、文字キー=緑、特殊キー=赤

## ドキュメント

- [`CLAUDE.md`](./CLAUDE.md) — Claude Code 向けの作業前提・指示
- [`docs/SPEC.md`](./docs/SPEC.md) — 物理仕様の詳細（寸法・公差・素材）
- [`docs/CARDS.md`](./docs/CARDS.md) — カード111枚の完全リスト
- [`docs/ROADMAP.md`](./docs/ROADMAP.md) — 試作から販売までのフェーズ

## 技術スタック

- **CAD**: [build123d](https://github.com/gumyr/build123d)（Python 製の B-rep CAD）
- **基盤**: OpenCascade（業界標準の B-rep カーネル）
- **3Dプリンタ**: Bambu Lab X2D（デュアルノズル、65℃チャンバー、Auto Hole Compensation）
- **スライサー**: Bambu Studio
- **素材**: Bambu Lab Basic PLA（マット推奨）+ TPU 95A
- **依存管理**: uv（Python）
- **テスト**: pytest

## ディレクトリ構成（予定）

```
plotter/
├── README.md
├── CLAUDE.md
├── pyproject.toml          # uv 管理
├── docs/
│   ├── SPEC.md
│   ├── CARDS.md
│   └── ROADMAP.md
├── src/plotter/
│   ├── __init__.py
│   ├── params.py           # 全パラメータ定義
│   ├── card.py             # カードモジュール
│   ├── body.py             # 本体パネルモジュール
│   ├── base.py             # 土台モジュール
│   └── utils.py            # 共通ユーティリティ
├── parts/                  # エントリポイント（部品ごと1ファイル）
│   ├── card_standard.py
│   ├── card_wide.py
│   ├── body_6row.py
│   ├── base_75.py
│   ├── base_60.py
│   └── base_90.py
├── assemblies/
│   └── full_assembly.py    # プレビュー用組立図
├── tests/
│   ├── test_dimensions.py  # 寸法リグレッションテスト
│   ├── test_assembly.py    # 組立整合性テスト
│   └── tenon_clearance_test.py  # 公差検証パーツ生成
├── build/                  # STL/STEP 出力先（gitignore）
└── Makefile                # ビルド・テスト一括実行
```

## クイックスタート

```bash
# 1. 環境セットアップ
git clone https://github.com/shomatan/plotter
cd plotter
uv sync

# 2. ビルド（全部品の STL/STEP 生成）
make all

# 3. テスト
uv run pytest

# 4. 個別パーツの生成
uv run python parts/card_standard.py
```

## ライセンス（予定）

- **build123d コード**: MIT License（自由に派生可）
- **STL データ**: 非公開（販売物としての差別化を維持）
- **PLOTTER ブランド名**: 商標出願予定

## ステータス

🚧 **設計フェーズ**（build123d 着手前）

## 著者

Shoma Nishitateno ([@shomatan](https://github.com/shomatan)) / Ignission G.K.
