# Gacha Flask Lite – Webガチャアプリ（Flask / デプロイ済み）
デモ: https://gacha-flask-lite.onrender.com/

## 概要
ブラウザで動くガチャアプリです。
画像・効果音・演出つきで、誰でも迷わず1クリックで回せます。

- ワンクリックで抽選 → 結果を画像と名前で表示
- ローディング演出（回転 → 開封）と効果音
- Render でデプロイ済み（URLを共有するだけで動作）

## できること（現状）
- ランダム抽選（`/api/gacha` が JSON を返す）
- 画像・効果音の表示（`/static/images`, `/static/sounds`）
- 画面遷移と音の演出（スタート / 回転 / 開封 / 結果）
- モバイル対応のレイアウト（レスポンシブ）

※レア度・重み・在庫・期間限定は今後の拡張予定（未実装）。

## 技術スタック
- Python 3.x / Flask
- HTML + CSS + JavaScript（`render_template_string` 内で実装）
- デプロイ：Render（Flask単体動作）

## エンドポイント
- `GET /` … 画面本体（HTML / JS / CSS）
- `GET /api/gacha` … 抽選結果を JSON で返す（`{"name": "...", "img": "images/..."}`）

## ディレクトリ構成（例）
``` 
.
├─ app.py # 本体（Flaskアプリ & HTML）
├─ static/
│ ├─ images/ # 結果表示に使う画像
│ └─ sounds/ # BGM/SE（mp3, wav）
└─ README.md

shell
コードをコピーする

## ローカル実行
### Windows (PowerShell)
```
powershell
git clone https://github.com/inafukuparadise/gacha-flask-lite
cd gacha-flask-lite
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install flask
$env:FLASK_APP="app.py"; flask run

こだわった点
初めて触る人でも迷わないUI（3画面の遷移と演出）

画像と音声を static/ にまとめ、差し替え運用しやすい構成

ローカル環境がなくても動くよう、Render にデプロイ

今後の拡張
重み付き抽選（レア度・在庫の設定）
ログ出力（CSV / JSON）
API化（FastAPI版 / 認証追加）
Docker / Cloud Run での運用
