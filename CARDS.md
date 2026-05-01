# PLOTTER カード一覧（Core 111）

このリストは Shoma さんの dotfiles（[shomatan/dotfiles](https://github.com/shomatan/dotfiles)）から
抽出した実使用キーバインドに基づく **Shoma さん専用 MVP** の構成です。

## カード総数：111枚

| 種類 | 枚数 | 配色 |
|---|---|---|
| 動詞・機能 | 60 | 黄（クリーム + 濃茶） |
| 修飾キー（ワイド） | 5 | 紫（ラベンダー + 濃紫） |
| アルファベット | 26 | 緑（ミント + 濃緑） |
| 数字 | 10 | 緑（ミント + 濃緑） |
| 特殊キー | 10 | 赤（ピンク + 濃赤） |

---

## 動詞・機能カード（60枚）

### A. ファイル・検索（10）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 1 | 検索 | `<leader><leader>` / `Space p` | 汎用検索 |
| 2 | ファイル検索 | `<leader>ff` / `Space f` | Telescope find_files |
| 3 | grep | `<leader>sg` | 文字列検索（live grep） |
| 4 | 最近 | `<leader>fr` / `Space b` | 最近のファイル |
| 5 | バッファ | `<leader>fb` / `<leader>,` | バッファ検索/一覧 |
| 6 | コマンド検索 | `Space c` | コマンドパレット |
| 7 | 全体検索 | `Space f` | プロジェクト全体検索 |
| 8 | 文字列検索 | `<leader>sw` | カーソル下の単語 |
| 9 | ファイル構造 | `Space o` | アウトライン |
| 10 | ハイライト解除 | `Esc Esc` | 検索ハイライトをクリア |

### B. 編集・保存（5）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 11 | 保存 | `Space w` / `Cmd s` | autosave 補助 |
| 12 | 再読込 | `<leader>r` | バッファリロード |
| 13 | オートセーブ | `:AutoSaveToggle` | トグル |
| 14 | 閉じる | `Space q` / `<leader>bd` | バッファ/ファイル閉じる |
| 15 | 復元 | `<leader>qr` | セッション復元 |

### C. ジャンプ・ナビ（10）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 16 | 定義へ | `gd` | LSP definition |
| 17 | 参照 | `gr` | LSP references |
| 18 | 型定義 | `gy` | LSP type definition |
| 19 | 実装 | `gi` | LSP implementation |
| 20 | 戻る | `Ctrl+o` | jump back |
| 21 | 進む | `Ctrl+i` | jump forward |
| 22 | 行頭 | `1` | Shoma 独自バインド |
| 23 | 行末 | `2` | Shoma 独自バインド |
| 24 | 親ディレクトリ | `-` | Oil.nvim |
| 25 | ジャンプリスト | `:jumps` | 履歴表示 |

### D. ウィンドウ・タブ（10）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 26 | 水平分割 | `<leader>-` | |
| 27 | 垂直分割 | `<leader>\|` | |
| 28 | ウィンドウ移動 | `<S-h/j/k/l>` | WezTerm 統一 |
| 29 | ウィンドウ閉じる | `<leader>wd` | |
| 30 | ウィンドウ最大化 | `<leader>wm` | トグル |
| 31 | サイズ変更 | `<C-Up/Down/Left/Right>` | |
| 32 | 新規タブ | `<leader><tab><tab>` | |
| 33 | タブ閉じる | `<leader><tab>d` | |
| 34 | 次タブ | `gt` / `<leader><tab>]` | |
| 35 | 前タブ | `gT` / `<leader><tab>[` | |

### E. コード操作（6）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 36 | リネーム | `<leader>cr` / `Space rn` | LSP rename |
| 37 | ホバー | `<leader>k` / `K` | ドキュメント表示 |
| 38 | コードアクション | `<leader>ca` | LSP code action |
| 39 | 診断 | `<leader>xx` | Trouble |
| 40 | 実装ジャンプ | `gi` | LSP implementation |
| 41 | GitHubで開く | `go` | IdeaVim |

### F. Git（4）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 42 | Lazygit | `<leader>gg` | Lazygit launcher |
| 43 | blame | `<leader>gb` | Git blame |
| 44 | 差分 | （TBD） | gitsigns hunks |
| 45 | ステータス | （TBD） | git status |

### G. ターミナル・パネル（4）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 46 | ターミナル | `<C-/>` / `Space t` | トグル |
| 47 | フローティング | `<leader>ft` | フローティング端末 |
| 48 | 問題パネル | `Space d` | 問題一覧 |
| 49 | ファイラー | `<leader>e` / `-` | Oil.nvim |

### H. Claude Code（9）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 50 | Claude切替 | `<leader>ac` | claudecode.nvim |
| 51 | Claudeフォーカス | `<leader>af` | フォーカス移動 |
| 52 | 再開 | `<leader>ar` | resume session |
| 53 | 継続 | `<leader>aC` | continue |
| 54 | モデル選択 | `<leader>am` | model picker |
| 55 | バッファ追加 | `<leader>ab` | add buffer to context |
| 56 | 選択範囲送信 | `<leader>as` | visual mode で送信 |
| 57 | 差分受入 | `<leader>aa` | accept diff |
| 58 | 差分拒否 | `<leader>ad` | reject diff |

### I. その他（2）

| # | カード文字 | 関連キー | 補足 |
|---|---|---|---|
| 59 | セッション保存 | `<leader>qs` | session save |
| 60 | セッション復元 | `<leader>qr` | session restore |

---

## 修飾キーカード（ワイド、5枚）

サイズ：60×30×2mm（標準カード2枚分）

| # | カード文字 | 配色 |
|---|---|---|
| 61 | Leader | 紫 |
| 62 | Cmd | 紫 |
| 63 | Ctrl | 紫 |
| 64 | Shift | 紫 |
| 65 | Alt | 紫 |

---

## アルファベットカード（26枚）

サイズ：30×30×2mm、配色：緑

| 文字 | 文字 | 文字 | 文字 | 文字 | 文字 |
|---|---|---|---|---|---|
| a | b | c | d | e | f |
| g | h | i | j | k | l |
| m | n | o | p | q | r |
| s | t | u | v | w | x |
| y | z | | | | |

フォントは **JetBrains Mono Bold** で小文字統一。
（大文字版は将来 Verb Pack で追加検討）

---

## 数字カード（10枚）

サイズ：30×30×2mm、配色：緑

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|

特別カード：
- **`1〜9`**（範囲指示）: AeroSpace の `Alt 1〜9` で使用するため1枚追加
  → 計11枚？ → MVP では `1` と `9` を別途用意で代用、Verb Pack で対応

---

## 特殊キーカード（10枚）

サイズ：30×30×2mm、配色：赤

| # | カード文字 | フォント |
|---|---|---|
| 1 | Tab | JetBrains Mono |
| 2 | Space | JetBrains Mono |
| 3 | Esc | JetBrains Mono |
| 4 | Enter | JetBrains Mono |
| 5 | `,` | JetBrains Mono |
| 6 | `:` | JetBrains Mono |
| 7 | `/` | JetBrains Mono |
| 8 | `-` | JetBrains Mono |
| 9 | `\|` | JetBrains Mono |
| 10 | `=` | JetBrains Mono |

---

## カード使用例

### 例1: ファイル検索（LazyVim）

```
[ ファイル検索 ] [ Leader ] [ f ] [ f ]
```

### 例2: Lazygit

```
[ Lazygit ] [ Leader ] [ g ] [ g ]
```

### 例3: AeroSpace ワークスペース移動

```
[ ウィンドウ移動 ] [ Alt ] [ 1 ]   ← 数字部分は差替えで再利用
```

※ 範囲指示 `1〜9` のカード需要あり、Verb Pack で追加

### 例4: Claude Code 切替

```
[ Claude切替 ] [ Leader ] [ a ] [ c ]
```

### 例5: macOS 標準ショートカット

```
[ 保存 ] [ Cmd ] [ s ]
```

---

## カード制作の優先順位

1. **修飾キー5枚**（最頻出、商品価値の中核）
2. **アルファベット26枚**（大量だが単純、X2D で1〜2バッチ）
3. **動詞 A〜D（35枚）**（Shoma さんの最頻出ジャンル）
4. **動詞 E〜G（14枚）**（コード・Git・ターミナル）
5. **動詞 H（Claude 9枚）**（Shoma さん固有、商品差別化要素）
6. **動詞 I（2枚）**（残り）
7. **特殊キー10枚 + 数字10枚**（最後でOK）

---

## 将来の Verb Pack 候補

商品化フェーズで追加検討するカード：

- **数字範囲**: `1〜9`、`0〜9` のレンジカード
- **大文字版アルファベット**: 26枚
- **追加動詞**: コピー、貼付、切取、削除、置換、整形、選択、コメント、折畳、展開
- **環境固有**: Telescope、Mason、Oil、Lazygit、Trouble などの**ツール名カード**
- **記号拡張**: `+`、`<`、`>`、`(`、`)`、`{`、`}`、`[`、`]`
- **Function キー**: F1〜F12
