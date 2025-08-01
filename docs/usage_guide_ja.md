# data2slideimg 使用ガイド

このツールはJSONデータから見栄えの良いスライド画像を生成します。日本語にも対応しています。

## 基本的な使い方

### 1. CLI（コマンドライン）での利用
```bash
uv run python -m src.cli -i input.json -o output.png
```

### 2. APIサーバーでの利用
```bash
# サーバー起動
uv run python -m src.main

# 別のターミナルでリクエスト送信
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d @input.json \
  --output output.png
```

## JSON形式の仕様

### 基本構造
```json
{
  "title": "スライドタイトル（オプション）",
  "format": "horizontal",  // "horizontal"（デフォルト）または "vertical"
  "textBlocks": [
    {"text": "テキストブロック1"},
    {"text": "テキストブロック2"}
  ],
  "graph": {
    "type": "bar",
    "data": [10, 20, 30],
    "labels": ["ラベル1", "ラベル2", "ラベル3"]
  },
  "table": {
    "headers": ["列1", "列2", "列3"],
    "rows": [
      ["データ1-1", "データ1-2", "データ1-3"],
      ["データ2-1", "データ2-2", "データ2-3"]
    ]
  },
  "image": {
    "url": "https://example.com/image.jpg"
  }
}
```

### フィールドの説明
- **title**: スライドの上部に表示されるタイトル（省略可能）
- **format**: 出力フォーマット（省略可能）
  - `"horizontal"`: 1920×1080（デフォルト）
  - `"vertical"`: 1080×1920（スマホ向け、ストーリーズ形式）
- **textBlocks**: テキストの配列。各要素は`{"text": "内容"}`の形式
- **graph**: グラフデータ（省略可能）
  - **type**: `"bar"`（棒グラフ）、`"line"`（折れ線グラフ）、`"pie"`（円グラフ）
  - **data**: 数値データの配列
  - **labels**: ラベルの配列（data配列と同じ長さ）
- **table**: テーブルデータ（省略可能）
  - **headers**: ヘッダー行の配列
  - **rows**: データ行の2次元配列
- **image**: 画像データ（省略可能、グラフと排他的）
  - **url**: 画像のURL（HTTPSまたはHTTP）

## 日本語使用時の推奨事項

### テキストブロック
- **1ブロックあたりの文字数**: 40〜60文字程度
- グラフありの場合、右カラムに表示されるため、長すぎると改行が多くなります
- 2〜3ブロック程度が見やすいです

### グラフのラベル
- **ラベル文字数**: 2〜4文字程度を推奨
- 長いラベルは重なる可能性があります
- 例: ✓「東京」「大阪」 ✗「東京都千代田区」

### テーブル
- **列数**: 3〜5列を推奨（最大6列まで表示可能）
- **行数**: 3〜5行を推奨（多すぎると見切れる可能性）
- **セル内文字数**: 10文字以内を推奨
- 日本語の場合、半角英数字の約2倍の幅を使用します

## レイアウトの仕組み

### 横型フォーマット（horizontal: 1920×1080）

#### 画像またはグラフがある場合
```
+------------------+------------------+
|                  |  テキスト        |
|  画像/グラフ     |                  |
|                  |  テーブル        |
+------------------+------------------+
```
- 左側：画像またはグラフエリア（画面幅の約半分）
- 右側：テキスト＋テーブルエリア
- 注意：画像とグラフは同時に表示できません（画像が優先されます）

#### 画像もグラフもない場合
```
+-------------------------------------+
|           テキスト                  |
|                                     |
|           テーブル                  |
+-------------------------------------+
```
- 全幅を使用してテキストとテーブルを表示

### 縦型フォーマット（vertical: 1080×1920）

```
+-------------------------+
|       タイトル          |
+-------------------------+
|                         |
|     画像/グラフ         |
|      （カード型）       |
|                         |
+-------------------------+
|     テキスト1           |
|     （カード型）        |
+-------------------------+
|     テキスト2           |
|     （カード型）        |
+-------------------------+
|     テーブル            |
|     （カード型）        |
+-------------------------+
```
- 縦スクロール型のストーリーズ形式
- グラスモーフィズム効果のカード配置
- 鮮やかなグラデーション背景
- スマホ閲覧に最適化されたフォントサイズ

## 実用的なサンプル

### 1. シンプルなテキストスライド
```json
{
  "title": "プロジェクト進捗報告",
  "textBlocks": [
    {"text": "今月の主な成果：新機能の実装が完了しました。"},
    {"text": "来月の予定：テスト実施とドキュメント作成を行います。"}
  ]
}
```

### 2. グラフ付きレポート
```json
{
  "title": "売上推移",
  "textBlocks": [
    {"text": "第3四半期は前年比120%の成長を達成しました。"},
    {"text": "特に関東エリアでの売上が好調でした。"}
  ],
  "graph": {
    "type": "bar",
    "data": [150, 180, 220, 250, 300],
    "labels": ["4月", "5月", "6月", "7月", "8月"]
  }
}
```

### 3. 比較表
```json
{
  "title": "製品比較",
  "textBlocks": [
    {"text": "3つの製品プランを比較しています。"}
  ],
  "table": {
    "headers": ["機能", "Basic", "Pro", "Enterprise"],
    "rows": [
      ["容量", "10GB", "100GB", "無制限"],
      ["ユーザー数", "5名", "20名", "無制限"],
      ["サポート", "メール", "電話", "24時間"],
      ["価格", "¥1,000", "¥5,000", "お問合せ"]
    ]
  }
}
```

### 4. 画像付きスライド
```json
{
  "title": "新製品紹介",
  "textBlocks": [
    {"text": "新しい製品ラインナップをご紹介します。"},
    {"text": "左側の画像は実際の製品写真です。"}
  ],
  "image": {
    "url": "https://example.com/product-photo.jpg"
  }
}
```

### 5. 縦型フォーマット（ストーリーズ用）
```json
{
  "title": "SNSトレンド 📱",
  "format": "vertical",
  "textBlocks": [
    {"text": "Z世代の利用率が90%を超える"},
    {"text": "動画コンテンツが必須要素に"},
    {"text": "短時間投稿が主流"}
  ],
  "graph": {
    "type": "bar",
    "data": [85, 72, 45, 28],
    "labels": ["TikTok", "Instagram", "Twitter", "Facebook"]
  }
}
```

## トラブルシューティング

### 文字が切れる場合
- テキストブロックの文字数を減らす
- 改行位置を調整するため、句読点で区切る

### グラフラベルが重なる場合
- ラベルを短くする
- データ数を減らす（5〜7個程度が最適）

### テーブルが見切れる場合
- 列数または行数を減らす
- セル内のテキストを短くする

### 画像が表示されない場合
- URLが正しいか確認する
- 画像形式がサポートされているか確認（JPEG、PNG推奨）
- ネットワーク接続を確認する

## 高度な使い方

### プログラムからの利用（Python）
```python
import requests
import json

data = {
    "title": "自動生成レポート",
    "textBlocks": [{"text": "プログラムから生成したスライドです。"}],
    "graph": {
        "type": "line",
        "data": [10, 25, 30, 45, 60],
        "labels": ["月", "火", "水", "木", "金"]
    }
}

response = requests.post(
    "http://localhost:8000/generate",
    json=data
)

with open("output.png", "wb") as f:
    f.write(response.content)
```

### バッチ処理
```bash
# 複数のJSONファイルを一括処理
for file in data/*.json; do
    uv run python -m src.cli -i "$file" -o "output/$(basename "$file" .json).png"
done
```

## まとめ

このツールを使えば、データからプロフェッショナルなスライド画像を簡単に生成できます。日本語にも対応しているため、日本語のプレゼンテーション資料作成にも活用できます。推奨事項に従うことで、より見やすく効果的なスライドを作成できます。