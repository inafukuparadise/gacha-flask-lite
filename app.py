from flask import Flask, jsonify, render_template_string
import random

app = Flask(__name__, static_folder="static", static_url_path="/static")

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
    {"name": "スパイダーくんくん", "img": "images/Takigyokun.jpg"},
    {"name": "スパイダーくんくん", "img": "images/Zombiduo.jpg"},
]

HTML = r"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
<title>ガチャのすけ・ガチャどう</title>

<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700&display=swap" rel="stylesheet">

<style>
:root { --btn-w:340px; --accent:#ff6fa3; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow-x: hidden; }
body {
  font-family: "Zen Maru Gothic", "Rounded Mplus 1c", sans-serif;
  color:#444; text-align:center;
}

/* 背景 */
.app {
  min-height: 100dvh;
  display: grid;
  place-items: center;
  background: #9eb6ff url("/static/images/Background.png") center/cover no-repeat;
  padding: 24px 12px;
}

/* コンテナ */
.wrap {
  width: min(620px, 92vw);
  margin-inline: auto;
}

/* 各画面 */
.row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px;
  align-items: center;
  justify-items: center;
}
.hidden {
  display: none !important;  /* ← 優先度を上げて完全に非表示にする */
}

/* ボタン */
.btn {
  display:block;
  width:90%;
  max-width:340px;
  margin:1em auto;
  padding:1.2em 1em;
  border-radius:24px;
  background:#ffe599;
  color:#333;
  border:4px solid #fff;
  font-size:18px;
  font-weight:900;
  line-height:1.15;
  box-shadow:0 6px 10px rgba(0,0,0,.18), inset 0 2px 3px rgba(255,255,255,.5);
  transition:transform .15s, box-shadow .15s;
}
.btn:hover { transform:translateY(-1px) scale(1.03); }
.btn:active { transform:translateY(0) scale(.98); }

/* 画像 */
.media {
  display:block;
  width:100%;
  max-width:90%;
  height:auto;
  margin:.6em auto;
  border-radius:18px;
  box-shadow:0 4px 10px rgba(0,0,0,.15);
}

/* 見出し */
h1 {
  color: var(--accent);
  font-size: 2.4em;
  font-weight: 800;
  text-shadow: 0 2px 6px rgba(0,0,0,.15);
  -webkit-text-stroke: 0.6px #fff;
}
h2 {
  font-size: 1.5em;
  color: #333;
}

/* 結果名 */
#result-name {
  font-size: 2em;
  font-weight: 800;
  color: var(--accent);
  text-shadow:
    -2px -2px 0 #fff,  2px -2px 0 #fff,
    -2px  2px 0 #fff,  2px  2px 0 #fff,
     0    3px 6px rgba(0,0,0,.25);
  -webkit-text-stroke: 0.8px #fff;
}

/* 結果画面 */
#screen-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

/* スマホ最適化 */
@media (max-width: 600px) {
  html, body, .app { width: 100%; overflow-x: hidden; }
  h1 { font-size: 1.9em; }
  .btn {
    width: 85vw !important;
    font-size: 16px !important;
    padding: 1em .8em !important;
  }
  .media { max-width: 85vw !important; }
  #result-name { font-size: 1.8em; }
}
</style>
</head>

<body>
<div class="app">
  <div class="wrap">

    <!-- 🎵 BGM -->
    <audio id="bgm-home" loop preload="auto">
      <source src="/static/sounds/Gachahome.mp3" type="audio/mpeg">
    </audio>

    <!-- 効果音 -->
    <audio id="se-roll" preload="auto">
      <source src="/static/sounds/Gachamawashi.wav" type="audio/wav">
    </audio>
    <audio id="se-open" preload="auto">
      <source src="/static/sounds/GachaKekka.wav" type="audio/wav">
    </audio>

    <!-- 画面：開始 -->
    <div id="screen-start" class="row">
      <h1>ガチャのすけ・ガチャどう</h1>
      <button class="btn" id="btn-start">スタート ▶️</button>
    </div>

    <!-- 画面：ホーム -->
    <div id="screen-home" class="row hidden">
      <button class="btn" id="btn-spin">ガチャを回す 💖</button>
      <img class="media" src="/static/images/roll_1.png" alt="preview">
    </div>

    <!-- 画面：回転 -->
    <div id="screen-rolling" class="row hidden">
      <h2>🌀 ガチャを回しています…</h2>
      <img class="media" src="/static/images/roll.gif" alt="rolling">
    </div>

    <!-- 画面：開封 -->
    <div id="screen-open" class="row hidden">
      <h2>💥 カプセルが開きます！</h2>
      <img class="media" src="/static/images/open.gif" alt="opening">
    </div>

    <!-- 画面：結果 -->
    <div id="screen-result" class="row hidden">
      <h2 id="result-name"></h2>
      <img id="result-img" class="media" alt="result">
      <div style="display:flex; flex-direction:column; gap:12px;">
        <button class="btn" id="btn-again">もう一回！ 🔁</button>
        <button class="btn" id="btn-home">ホームへ戻る 🏠</button>
      </div>
    </div>

  </div>
</div>

<script>
const screens = {
  start: document.getElementById("screen-start"),
  home: document.getElementById("screen-home"),
  rolling: document.getElementById("screen-rolling"),
  open: document.getElementById("screen-open"),
  result: document.getElementById("screen-result"),
};

function show(id) {
  Object.values(screens).forEach(s => s.classList.add("hidden"));
  screens[id].classList.remove("hidden");
}

const bgm = document.getElementById("bgm-home");
const seRoll = document.getElementById("se-roll");
const seOpen = document.getElementById("se-open");
const resultImg = document.getElementById("result-img");
const resultName = document.getElementById("result-name");

async function fetchResult() {
  const r = await fetch("/api/gacha", { cache: "no-store" });
  return r.json();
}

async function runGacha() {
  show("rolling");
  try { seRoll.currentTime = 0; seRoll.play(); } catch (e) {}
  bgm.pause();
  await new Promise(r => setTimeout(r, 2600));
  show("open");
  try { seOpen.currentTime = 0; seOpen.play(); } catch (e) {}
  await new Promise(r => setTimeout(r, 1500));
  const r = await fetchResult();
  resultImg.src = "/static/" + r.img;
  resultName.textContent = r.name;
  show("result");
}

document.getElementById("btn-start").addEventListener("click", () => {
  try { bgm.volume = 0.5; bgm.currentTime = 0; bgm.play(); } catch (e) {}
  show("home");
});
document.getElementById("btn-spin").addEventListener("click", runGacha);
document.getElementById("btn-again").addEventListener("click", runGacha);
document.getElementById("btn-home").addEventListener("click", () => {
  show("home");
  try { bgm.currentTime = 0; bgm.play(); } catch (e) {}
});

show("start");
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/gacha")
def api_gacha():
    return jsonify(random.choice(RESULTS))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
