# -*- coding: utf-8 -*-
"""카피체크 아임웹 상품 그림 · 토큰 이용 안내 그림 · 공유 그림(og.png) · 아이콘 만들기
python3 _src/shop/render.py
  -> _src/shop/out/cc-<id>-1x1.jpg (1200x1200), cc-tokens-guide.png (1080x1350)
  -> docs/assets/product/ 에도 복사(사이트 Product 구조화 데이터 · 아임웹 상세 그림에서 씀), docs/assets/img/og.png(1200x630)
형제 사이트 상품 그림의 짜임(로고 · 토큰 카드 · 장점 세 칸 · 실측 예시)을 바탕으로 카피체크 색(잉크 · 초록 · 민트)과 문서 검사 줄로.
정가 표시 없이(형제 사이트 방침, 정가 취소선은 아임웹 가격 칸이 보여 줌). 전후 AI 작성률은 _src/demo.json(카피체크 엔진 실측값) 논문 예시 그대로.
글꼴: _src/shop/pretendard.css(저장소에 올리지 않음, PretendardVariable.woff2 를 같은 폴더에)"""
import asyncio, json, os, shutil
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
ROOT = os.path.dirname(SRC)
OUT = os.path.join(HERE, "out")
PROD = os.path.join(ROOT, "docs", "assets", "product")
IMG = os.path.join(ROOT, "docs", "assets", "img")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PROD, exist_ok=True)
FONT = "file://" + os.path.join(HERE, "pretendard.css")
MARK_SVG = ('<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><rect width="40" height="40" rx="11" fill="#0b0f14"/>'
            '<path d="M24.6 13.4a8.6 8.6 0 1 0 0 13.2" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/>'
            '<path d="m21.2 20.3 3.6 3.6 7.4-8" fill="none" stroke="#22c38e" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
MARK_SVG_W = MARK_SVG.replace('fill="#0b0f14"', 'fill="#fff"').replace('stroke="#fff"', 'stroke="#0b0f14"')


def logo_html(h=96, white=False):
    m = MARK_SVG_W if white else MARK_SVG
    c1, c2, kb, kc = ("#fff", "#5ee6b4", "rgba(255,255,255,.10)", "#b9c9c1") if white else ("#0b0f14", "#0d9a6c", "#f1f4f2", "#6a7570")
    return ('<div class="lg" style="display:flex;align-items:center;gap:%dpx;height:%dpx"><span style="display:block;width:%dpx;height:%dpx">%s</span>'
            '<span style="font-size:%dpx;font-weight:880;letter-spacing:-.045em;color:%s;line-height:1">Copy<b style="font-weight:880;color:%s">Check</b></span>'
            '<span style="margin-left:4px;padding:%dpx %dpx;border-radius:999px;background:%s;font-size:%dpx;font-weight:780;color:%s;letter-spacing:-.01em">카피체크</span></div>') % (
        int(h * .26), h, h, h, m.replace('<svg ', '<svg width="%d" height="%d" ' % (h, h)), int(h * .62), c1, c2, int(h * .09), int(h * .2), kb, int(h * .25), kc)


DEMO = json.load(open(os.path.join(SRC, "demo.json"), encoding="utf-8"))
T = DEMO["samples"][0]
B_RATE, A_RATE, T_LABEL = T["before"]["rate"], T["after"]["rate"], T["label"]

PACKS = [
    {"id": "lt", "name": "라이트", "tok": "100", "price": "9,900원", "per": "토큰당 99원", "save": "", "badge": "", "fit": "자기소개서 · 짧은 과제", "pg": "레포트 약 10페이지"},
    {"id": "pl", "name": "플러스", "tok": "350", "price": "19,900원", "per": "토큰당 약 57원", "save": "", "badge": "", "fit": "레포트 · 과제 여러 편", "pg": "레포트 약 35페이지"},
    {"id": "pr", "name": "프로", "tok": "1,000", "price": "39,900원", "per": "토큰당 약 40원", "save": "플러스 대비 이용 단가 30% 절감", "badge": "추천 요금제", "fit": "논문 · 학위논문", "pg": "논문 약 100페이지"},
    {"id": "mx", "name": "맥스", "tok": "2,000", "price": "69,900원", "per": "토큰당 약 34원", "save": "플러스 대비 이용 단가 39% 절감", "badge": "최대 할인 혜택", "fit": "논문 전체 · 여러 편", "pg": "논문 약 250페이지"},
]

CHECK = ('<svg viewBox="0 0 24 24" width="30" height="30" fill="none"><circle cx="12" cy="12" r="11" fill="#e7f7f0"/>'
         '<path d="m7.5 12.3 3 3 6-6.3" stroke="#0d9a6c" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ORBIT = ('<svg class="orb" viewBox="0 0 1000 700" fill="none"><defs><linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="#22c38e" stop-opacity="0"/>'
         '<stop offset=".5" stop-color="#5ee6b4" stop-opacity=".95"/><stop offset="1" stop-color="#22c38e" stop-opacity="0"/></linearGradient>'
         '<radialGradient id="g3"><stop offset="0" stop-color="#5ee6b4" stop-opacity=".6"/><stop offset="1" stop-color="#5ee6b4" stop-opacity="0"/></radialGradient></defs>'
         '<g stroke="rgba(255,255,255,.12)" stroke-width="1.6"><rect x="560" y="90" width="330" height="430" rx="22"/><rect x="600" y="150" width="250" height="12" rx="6"/><rect x="600" y="186" width="210" height="12" rx="6"/>'
         '<rect x="600" y="222" width="236" height="12" rx="6"/><rect x="600" y="258" width="190" height="12" rx="6"/><rect x="600" y="306" width="244" height="12" rx="6"/><rect x="600" y="342" width="200" height="12" rx="6"/></g>'
         '<circle cx="740" cy="260" r="260" fill="url(#g3)" opacity=".5"/><rect x="540" y="236" width="380" height="4" rx="2" fill="url(#g1)"/></svg>')

BASE = ("<!doctype html><html><head><meta charset='utf-8'><link rel='stylesheet' href='%s'><style>"
        "*{box-sizing:border-box;margin:0;padding:0}html,body{font-family:'Pretendard Variable',Pretendard,sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-.02em;color:#0b0f14;word-break:keep-all}"
        "%%s</style></head><body>%%s</body></html>") % FONT

THUMB_CSS = """
body{width:1200px;height:1200px;position:relative;overflow:hidden;background:radial-gradient(700px 420px at 100% 0%,rgba(34,195,142,.10),transparent 70%),linear-gradient(180deg,#ffffff 0%,#f2f5f3 100%)}
.lg{position:absolute;left:92px;top:74px}
.card{position:absolute;left:92px;top:212px;width:1016px;height:600px;border-radius:48px;overflow:hidden;color:#fff;
 background:radial-gradient(560px 380px at 100% 0%,rgba(34,195,142,.55),transparent 70%),radial-gradient(520px 360px at 0% 110%,rgba(13,154,108,.55),transparent 64%),linear-gradient(155deg,#0b0f14 0%,#0f1d18 58%,#0b0f14 100%);
 box-shadow:0 44px 80px -34px rgba(11,15,20,.65)}
.card:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:56px 56px}
.orb{position:absolute;right:-170px;top:-60px;width:900px;opacity:.85}
.km{position:absolute;right:-30px;bottom:-40px;height:380px;opacity:.16;filter:brightness(1.6)}
.hdr{position:absolute;left:58px;top:54px;display:flex;align-items:center;gap:14px;font-size:30px;font-weight:720;color:#cfeee1;z-index:2}
.badge{position:absolute;right:56px;top:46px;height:56px;padding:0 26px;border-radius:28px;display:flex;align-items:center;font-size:27px;font-weight:860;z-index:2}
.badge.best{background:linear-gradient(135deg,#7cf0c4,#2fcf96);color:#0b0f14}
.badge.top{background:#fff;color:#0b0f14}
.pills{position:absolute;left:56px;top:128px;display:flex;gap:14px;z-index:2}
.pill{height:58px;padding:0 26px;border-radius:29px;display:flex;align-items:center;font-size:29px;font-weight:860}
.pill.n{background:linear-gradient(135deg,#087a55,#0d9a6c 50%,#22c38e);color:#fff;box-shadow:0 10px 24px -10px rgba(34,195,142,.9)}
.pill.o{border:2px solid rgba(255,255,255,.36);color:#fff;font-weight:720}
.big{position:absolute;left:48px;top:206px;display:flex;align-items:flex-end;z-index:2}
.big b{font-size:@BIG@px;font-weight:880;letter-spacing:-.06em;line-height:.8;background:linear-gradient(180deg,#ffffff 30%,#c9f5e3 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 18px 40px rgba(0,0,0,.35))}
.big span{font-size:60px;font-weight:860;margin:0 0 6px 16px}
.fit{position:absolute;left:58px;bottom:124px;font-size:27px;font-weight:650;color:rgba(255,255,255,.88);z-index:2}
.save{position:absolute;left:56px;bottom:50px;height:54px;padding:0 20px;border-radius:12px;border:2px solid rgba(124,240,196,.75);background:rgba(124,240,196,.12);color:#a7f3d0;font-size:25px;font-weight:820;display:flex;align-items:center;z-index:2}
.note{position:absolute;left:58px;bottom:58px;font-size:25px;font-weight:650;color:#9fe6c8;z-index:2}
.price{position:absolute;right:56px;bottom:44px;text-align:right;z-index:2}
.price b{display:block;font-size:78px;font-weight:880;letter-spacing:-.04em;line-height:1}
.price small{display:block;font-size:25px;font-weight:650;color:rgba(255,255,255,.78);margin-top:10px}
.feat{position:absolute;left:92px;right:92px;top:852px;display:grid;grid-template-columns:.82fr 1.36fr 1.12fr;gap:16px}
.feat div{display:flex;align-items:center;gap:10px;height:96px;padding:0 18px;border-radius:22px;background:#fff;border:1.5px solid #e3e8e5;font-size:24px;letter-spacing:-.03em;white-space:nowrap;font-weight:760;color:#0b0f14}
.proof{position:absolute;left:92px;right:92px;bottom:76px;height:120px;border-radius:24px;background:#fff;border:1.5px solid #e3e8e5;display:flex;align-items:center;gap:26px;padding:0 34px}
.proof .k{font-size:24px;font-weight:800;color:#6a7570;letter-spacing:-.01em}
.proof .v{display:flex;align-items:baseline;gap:14px;font-weight:880;letter-spacing:-.04em}
.proof .v s{font-size:50px;color:#e5154f;text-decoration-thickness:4px}
.proof .v i{font-style:normal;font-size:38px;color:#98a2b3}
.proof .v b{font-size:62px;color:#0b8f63}
.proof .t{margin-left:auto;text-align:right;font-size:23px;font-weight:650;color:#3a4540;line-height:1.45}
"""


def thumb_html(p):
    badge = ('<div class="badge best">%s</div>' % p["badge"]) if p["badge"] == "추천 요금제" else (('<div class="badge top">%s</div>' % p["badge"]) if p["badge"] else "")
    low = ('<div class="save">%s</div>' % p["save"]) if p["save"] else '<div class="note">AI 작성률 검사 · AI 휴머나이징 서비스</div>'
    big = 250 if len(p["tok"]) <= 3 else 205
    css = THUMB_CSS.replace("@BIG@", str(big))
    body = ('%s'
            '<div class="card">%s<div class="hdr">AI 작성률 검사 · AI 휴머나이징</div>%s'
            '<div class="pills"><span class="pill n">%s</span><span class="pill o">토큰 충전</span></div>'
            '<div class="big"><b>%s</b><span>토큰</span></div><div class="fit">%s · %s</div>%s'
            '<div class="price"><b>%s</b><small>%s · 부가세 포함</small></div></div>'
            '<div class="feat"><div>%s월 구독 없음</div><div>%s쓴 만큼 차감 · 기한 무제한</div><div>%s결제 즉시 코드 발송</div></div>'
            '<div class="proof"><span class="k">실측 예시</span><span class="v"><s>%d%%</s><i>→</i><b>%d%%</b></span><span class="t">%s · 한 번의 휴머나이징<br>실제 엔진으로 잰 값 · 글마다 다릅니다</span></div>') % (
        logo_html(98), ORBIT, badge, p["name"], p["tok"], p["fit"], p["pg"], low, p["price"], p["per"], CHECK, CHECK, CHECK, B_RATE, A_RATE, T_LABEL)
    return BASE % (css, body)


GUIDE_CSS = """
body{width:1080px;height:1350px;position:relative;overflow:hidden;background:radial-gradient(640px 380px at 100% 0%,rgba(34,195,142,.12),transparent 70%),linear-gradient(180deg,#ffffff,#f2f5f3)}
.lg{position:absolute;left:72px;top:62px}
h1{position:absolute;left:72px;top:184px;font-size:56px;line-height:1.22;font-weight:860;letter-spacing:-.045em;color:#0b0f14}
h1 em{font-style:normal;background:linear-gradient(135deg,#087a55,#0d9a6c 50%,#22c38e);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{position:absolute;left:74px;top:336px;font-size:26px;color:#3a4540;font-weight:560;line-height:1.6}
.steps{position:absolute;left:72px;right:72px;top:404px;display:grid;gap:16px}
.st{display:flex;gap:22px;align-items:flex-start;padding:24px 28px;border-radius:24px;background:#fff;border:1.5px solid #e3e8e5}
.st i{flex:none;width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#087a55,#0d9a6c 50%,#22c38e);color:#fff;font-style:normal;font-weight:860;font-size:28px;display:grid;place-items:center}
.st b{display:block;font-size:31px;font-weight:860;letter-spacing:-.03em;color:#0b0f14}
.st p{margin-top:4px;font-size:22.5px;line-height:1.5;color:#3a4540}
.cost{position:absolute;left:72px;right:72px;bottom:56px;padding:30px 34px;border-radius:26px;color:#fff;overflow:hidden;background:radial-gradient(420px 260px at 100% 0%,rgba(34,195,142,.6),transparent 70%),linear-gradient(150deg,#0b0f14,#0f1d18)}
.cost h2{font-size:30px;font-weight:860;letter-spacing:-.03em}
.cost ul{list-style:none;margin-top:14px;display:grid;grid-template-columns:1fr 1fr;gap:10px 26px;font-size:24px;color:#d3ebe0}
.cost b{color:#fff}
"""


def guide_html():
    steps = [("결제", "토큰을 고르고 성균관컨설팅 결제 페이지에서 결제합니다. 회원가입 없이 카드 · 간편결제로 끝납니다."),
             ("메일로 코드", "결제가 확인되면 보통 1분 안에 주문서의 이메일로 16자리 토큰 코드가 갑니다. 보내는 이름은 '카피체크'입니다."),
             ("바로 이어서", "메일의 '바로 이어서 하기'를 누르면 코드가 들어간 채로 copycheck.skkc.co.kr 이 열리고, 하던 글을 그대로 이어 갑니다."),
             ("쓴 만큼만", "글을 넣고 검사 · 휴머나이징을 누르면 글자 수만큼만 빠집니다. 남은 토큰은 기한 없이 그대로입니다.")]
    s = "".join('<div class="st"><i>%d</i><div><b>%s</b><p>%s</p></div></div>' % (i + 1, a, b) for i, (a, b) in enumerate(steps))
    body = ('%s<h1>결제하고 <em>1분</em>,<br>메일로 받은 코드로 바로</h1><p class="sub">AI 작성률 검사 · AI 휴머나이징 서비스에 쓰는 토큰 이용 안내</p><div class="steps">%s</div>'
            '<div class="cost"><h2>토큰은 이렇게 빠집니다</h2><ul><li>AI 작성률 검사 <b>무료</b></li><li>상세 진단 <b>1,000자 3토큰</b></li><li>휴머나이징 <b>1,000자 6토큰</b></li><li>1토큰 <b>100원</b> · 구독 없음</li></ul></div>') % (logo_html(84), s)
    return BASE % (GUIDE_CSS, body)


OG_CSS = """
body{width:1200px;height:630px;position:relative;overflow:hidden;color:#fff;
 background:radial-gradient(620px 420px at 92% 0%,rgba(34,195,142,.42),transparent 64%),radial-gradient(560px 420px at 0% 0%,rgba(13,154,108,.45),transparent 62%),linear-gradient(165deg,#0b0f14 0%,#0f1d18 58%,#0a120f 100%)}
body:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:48px 48px}
.orb{position:absolute;right:-260px;top:-150px;width:1000px;opacity:.9}
.lg{position:absolute;left:72px;top:58px}
.kw{position:absolute;left:76px;top:190px;font-size:26px;font-weight:760;color:#a6d9c4;letter-spacing:-.01em}
h1{position:absolute;left:72px;top:232px;font-size:66px;line-height:1.16;font-weight:860;letter-spacing:-.05em}
h1 em{font-style:normal;background:linear-gradient(92deg,#7cf0c4,#2fcf96 55%,#a7f3d0);-webkit-background-clip:text;background-clip:text;color:transparent}
.chips{position:absolute;left:76px;bottom:62px;display:flex;gap:12px}
.chips span{height:48px;padding:0 20px;border-radius:24px;display:flex;align-items:center;font-size:21px;font-weight:720;border:1.5px solid rgba(255,255,255,.26);color:#e0f2ea;background:rgba(255,255,255,.06)}
.chips span:first-child{background:linear-gradient(135deg,#087a55,#0d9a6c 50%,#22c38e);border-color:transparent;color:#fff}
.proof{position:absolute;right:72px;bottom:58px;width:330px;padding:22px 26px;border-radius:24px;background:#fff;color:#0b0f14;box-shadow:0 30px 60px -20px rgba(0,0,0,.55)}
.proof small{display:block;font-size:17px;font-weight:760;color:#6a7570}
.proof .v{display:flex;align-items:baseline;gap:12px;margin-top:6px;font-weight:880;letter-spacing:-.04em}
.proof .v s{font-size:40px;color:#e5154f;text-decoration-thickness:3px}
.proof .v i{font-style:normal;font-size:30px;color:#98a2b3}
.proof .v b{font-size:56px;color:#0b8f63}
.proof p{font-size:16px;color:#6a7570;margin-top:4px}
"""


def og_html():
    body = ('%s%s<p class="kw">AI 작성률 검사 · AI 유사도 낮추기 · AI 휴머나이징</p><h1>AI로 쓴 문장은<br><em>제출 전에 걸러 냅니다</em>.</h1>'
            '<div class="chips"><span>AI 작성률 무료 검사</span><span>한글 · 워드 · PDF</span><span>copycheck.skkc.co.kr</span></div>'
            '<div class="proof"><small>%s 예시 · 한 번의 휴머나이징</small><div class="v"><s>%d%%</s><i>→</i><b>%d%%</b></div><p>실제 엔진으로 잰 값 · 글마다 다릅니다</p></div>') % (ORBIT, logo_html(92, True), T_LABEL, B_RATE, A_RATE)
    return BASE % (OG_CSS, body)


async def shot(b, html, w, h, fp, jpeg=False):
    path = os.path.join(HERE, "_t_%d.html" % abs(hash(fp)))
    open(path, "w", encoding="utf-8").write(html)
    pg = await b.new_page(viewport={"width": w, "height": h})
    await pg.goto("file://" + path); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(300)
    if jpeg:
        await pg.screenshot(path=fp, type="jpeg", quality=90)
    else:
        await pg.screenshot(path=fp)
    await pg.close(); os.remove(path)


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        for p in PACKS:
            fp = os.path.join(OUT, "cc-%s-1x1.jpg" % p["id"])
            await shot(b, thumb_html(p), 1200, 1200, fp, jpeg=True)
            shutil.copy(fp, os.path.join(PROD, os.path.basename(fp)))
        fp = os.path.join(OUT, "cc-tokens-guide.png")
        await shot(b, guide_html(), 1080, 1350, fp)
        shutil.copy(fp, os.path.join(PROD, os.path.basename(fp)))
        await shot(b, og_html(), 1200, 630, os.path.join(IMG, "og.png"))
        for n, sz in [("apple-touch-icon.png", 180), ("logo-192.png", 192), ("logo-512.png", 512), ("_ico48.png", 48), ("_ico32.png", 32), ("_ico16.png", 16)]:
            pad = 0 if n.startswith("_ico") else int(sz * .1)
            html = "<!doctype html><html><body style='margin:0;width:%dpx;height:%dpx;display:grid;place-items:center;background:%s'>%s</body></html>" % (
                sz, sz, "transparent" if n.startswith("_ico") else "#ffffff", MARK_SVG.replace("<svg ", "<svg width='%d' height='%d' " % (sz - 2 * pad, sz - 2 * pad)))
            await shot(b, html, sz, sz, os.path.join(IMG, n))
        await b.close()
    from PIL import Image
    ims = [Image.open(os.path.join(IMG, "_ico%d.png" % z)).convert("RGBA") for z in (16, 32, 48)]
    ims[2].save(os.path.join(os.path.dirname(IMG), "..", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ims[:2])
    for z in (16, 32, 48):
        os.remove(os.path.join(IMG, "_ico%d.png" % z))
    open(os.path.join(IMG, "favicon.svg"), "w").write(MARK_SVG)
    print("ok", sorted(os.listdir(OUT)))

asyncio.run(main())
