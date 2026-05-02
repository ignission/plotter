# PLOTTER

> キーバインドを、プロットする。
> *Plot your bindings.*

覚えにくいキーバインドを物理カードで机に並べる学習装置。動詞・修飾キー・文字キーをカードに印刷し、自分の使うコマンドを物理的に構成する。覚えたら外す、新しく学ぶものが増えたら足す。

## なぜ作るのか

LazyVim、AeroSpace、Claude Code、Git…。エンジニアの机には覚えるべきキーバインドが多すぎる。デジタルなチートシートはアプリを開かないと見えない。紙のメモは机に散らかる。Anki などのフラッシュカードアプリは「覚えた/覚えてない」をボタンで操作するだけで身体感覚が伴わない。

PLOTTER は、**キーバインドを物理化して机の上に常駐させる**装置。視界に入るたびに無意識で覚える。覚えたカードは取り外し、空いたスロットには新しく学びたいキーバインドを差す。**学習の進捗が物理的に可視化される**。

「単なる物理チートシート」ではなく、**「カードを部品として組み合わせて自分のキーバインドを構成する」** という発想が中核。自分の dotfiles からカードを刷り、机の上で並び替えながら学ぶ。

## 形状

```
             後縁 50mm
        ┌────────────────────┐  ← 上面（6本の長スロット）
       /  [検索][gd][Ctrl]   /
      /   [保存][gr][Leader] /   傾斜 8.5°
     /    ……6行 × 180mm……  /
    └────────────────────────┘  ← 前縁 20mm
    ←──── 200mm ────────────→

内部：Drawer（収納トレイ）が前面から引き出し式
```

Apple Magic Keyboard 系の薄いウェッジスラブ形状。机に置くとそのまま自立する。

## 現行設計の特徴

- **傾斜面ディスプレイ**: 上面が 8.5° 傾斜、カードが自然に見やすい角度で並ぶ
- **長スロット式**: 6 本の 180mm スロットに標準カード(30mm)とワイドカード(60mm)を任意に混在・並び替え可能。列の仕切りなし
- **内部ドロワー**: Wedge 内部に 180×150×12mm のキャビティ。前面から引き出すトレイに ~100 枚収納
- **シンプル 2 パーツ**: Wedge 本体 + Drawer のみ。接続部品なし

## カード仕様

| 種類 | サイズ | 用途 |
|---|---|---|
| 標準カード | 30×30×2mm、角 R3 | 動詞、文字キー、数字、特殊キー |
| ワイドカード | 60×30×2mm、角 R3 | 修飾キー（Leader、Cmd など） |

配色：cream（動詞）/ lavender（修飾キー）/ mint（文字キー）/ pink（特殊キー）

カードはウェッジ上面のスロットに差し込んで立てかけて使う。

## ドキュメント

- [`CLAUDE.md`](./CLAUDE.md) — Claude Code 向けの作業前提・指示
- [`SPEC.md`](./SPEC.md) — 物理仕様の詳細（寸法・公差・印刷パラメータ）
- [`CARDS.md`](./CARDS.md) — カード 111 枚の完全リスト
- [`ROADMAP.md`](./ROADMAP.md) — 試作から販売までのフェーズ

## 技術スタック

- **CAD**: [build123d](https://github.com/gumyr/build123d) 0.10+（Python 製 B-rep CAD）
- **基盤**: OpenCascade（業界標準の B-rep カーネル）
- **3Dプリンタ**: Bambu Lab X2D（デュアルノズル）
- **スライサー**: Bambu Studio（ツリーサポート推奨）
- **素材**: Bambu Lab Basic PLA（マット推奨）
- **依存管理**: uv / mise
- **テスト**: pytest

## クイックスタート

```bash
# 1. 環境セットアップ
git clone https://github.com/shomatan/plotter
cd plotter
mise install
uv sync

# 2. テスト
mise exec -- uv run pytest

# 3. 試作セット（半スケール Wedge + Drawer + カード）生成
make test-set

# 4. Bambu Studio に build/*.stl を読み込み、ツリーサポート設定で印刷
```

## ディレクトリ構成

```
plotter/
├── README.md
├── CLAUDE.md
├── pyproject.toml          # uv 管理
├── Makefile
├── SPEC.md
├── ROADMAP.md
├── CARDS.md
├── src/plotter/
│   ├── __init__.py
│   ├── params.py           # 全パラメータ定義
│   ├── card.py             # カードモジュール
│   ├── wedge.py            # Wedge 本体モジュール
│   ├── drawer.py           # Drawer モジュール
│   └── utils.py            # 共通ユーティリティ
├── parts/                  # エントリポイント（部品ごと1ファイル）
│   ├── card_standard.py
│   ├── card_wide.py
│   ├── card_thickness_test.py
│   ├── wedge.py
│   ├── wedge_test.py       # 半スケール試作
│   ├── drawer.py
│   └── drawer_test.py      # 半スケール試作
├── assemblies/             # プレビュー用組立図
├── tests/
│   ├── test_card.py
│   ├── test_wedge.py
│   ├── test_drawer.py
│   ├── test_params.py
│   └── test_utils.py
└── build/                  # STL/STEP 出力先（gitignore）
```

## ライセンス（予定）

- **build123d コード**: MIT License（自由に派生可）
- **STL データ**: 非公開（販売物としての差別化を維持）
- **PLOTTER ブランド名**: 商標出願予定

## ステータス

設計フェーズ（build123d コード実装中）

## 著者

Shoma Nishitateno ([@shomatan](https://github.com/shomatan)) / Ignission G.K.
