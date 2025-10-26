from flask import Flask, jsonify, render_template_string
import random
import os  # ← Renderで必要

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ===== 抽選データ（最新版） =====
RESULTS = [
    {"name": "🐱 ねこ", "img": "images/catRelax.jpg"},
    {"name": "お医者さん", "img": "images/DoctorDuo.jpg"},
    {"name": "出っ歯いちくん", "img": "images/DeppaIchi.jpg"},
    {"name": "出っ歯くんくん", "img": "images/DeppaKun.jpg"},
    {"name": "ゴリラたち", "img": "images/Gorilladup.jpg"},
    {"name": "蛇拳いちくん", "img": "images/Jakenichi.jpg"},
    {"name": "マッチョいちくん", "img": "images/Macchoichi.png"},
    {"name": "マッチョくんくん", "img": "images/Macchokun.png"},
    {"name": "ポリスいちくん", "img": "images/Policeichi.jpg"},
    {"name": "ポリスくんくん", "img": "images/Policekun.jpg"},
    {"name": "たそがれ", "img": "images/Souryoduo.png"},
    {"name": "僧侶くんくん", "img": "images/SouryoKun.jpg"},
    {"name": "スパイダーいちくん", "img": "images/Spiderichi.jpg"},
    {"name": "スパイダーくんくん", "img": "images/SpiderKun.jpg"},
    {"name": "滝行くんくん", "img": "images/Takigyokun.jpg"},
    {"name": "ゾンビデュオ", "img": "images/Zombiduo.jpg"},
]

# ===== HTMLテンプレート（Renderテスト用） =====
HTML = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>ガチャのすけ・ガチャどう</title>
</head>
<body style="text-align:center; font-family:sans-serif; background:#9eb6ff;">
  <h1>ガチャのすけ・ガチャどう 🎡</h1>
  <p>FlaskアプリはRender上で動作中です！</p>
  <p><a href="/api/gacha">🎲 試しにガチャ結果APIを開く</a></p>
</body>
</html>"""

# ===== ページルート =====
@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/gacha")
def api_gacha():
    return jsonify(random.choice(RESULTS))

# ===== Flask起動設定（Render対応） =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが自動割り当てするポートを使用
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
