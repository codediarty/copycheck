# -*- coding: utf-8 -*-
"""카피클린 AI 유사도 개선 결제 상품(5만 원 ~ 100만 원, 5만 원 단위) 그림 만들기
  python3 render.py  ->  hm-50000.jpg ... hm-1000000.jpg (750x750 대표 그림), hm-guide.png (1200x800 디지털 파일 '결제 안내')"""
import asyncio, os
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "file:///home/claude/ccwork/node_modules/pretendard/dist/web/variable/woff2/PretendardVariable.woff2"
AMOUNTS = list(range(50000, 1000001, 50000))

def man(a):
    m = a // 10000
    return ("%d" % m)

CSS = """
@font-face{font-family:'P';font-weight:45 920;src:url('%s') format('woff2-variations');}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'P',sans-serif;-webkit-font-smoothing:antialiased;letter-spacing:-0.02em;color:#0f172a;word-break:keep-all}
""" % FONT

LOGO = ('<span class="lg"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>'
        '<path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/></svg></span>')
CHECK = '<i><svg viewBox="0 0 24 24"><path d="m5 12 5 5L20 7"/></svg></i>'

def thumb_html(a):
    return """<!doctype html><html><head><meta charset="utf-8"><style>%s
.c{width:750px;height:750px;background:#fff;padding:46px 48px 44px;display:flex;flex-direction:column}
.hd{display:flex;align-items:center;gap:12px}
.lg{width:46px;height:46px;border-radius:13px;background:linear-gradient(135deg,#12a86a,#0b7a4b);display:flex;align-items:center;justify-content:center;box-shadow:0 8px 18px rgba(16,163,102,.3)}
.lg svg{width:25px;height:25px;stroke:#fff;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round}
.br b{display:block;font-size:27px;font-weight:800;line-height:1}
.br small{display:block;margin-top:4px;font-size:11.5px;font-weight:800;letter-spacing:.22em;color:#64748b}
.dm{margin-left:auto;font-size:17px;font-weight:700;color:#0b7a4b}
.pn{position:relative;overflow:hidden;margin-top:30px;height:330px;border-radius:30px;padding:30px 34px;color:#fff;
 background:radial-gradient(420px 260px at 100%% 0%%,rgba(110,231,183,.28),rgba(110,231,183,0) 70%%),linear-gradient(140deg,#0e6b45 0%%,#0a4d33 55%%,#083a27 100%%);
 box-shadow:0 30px 60px -30px rgba(8,58,39,.7)}
.pn:after{content:"";position:absolute;right:-90px;bottom:-120px;width:330px;height:330px;border-radius:50%%;border:1px solid rgba(255,255,255,.14)}
.t1{display:flex;align-items:center;gap:10px;font-size:20px;font-weight:800}
.t1 i{display:flex;width:30px;height:30px;border-radius:9px;background:rgba(255,255,255,.16);align-items:center;justify-content:center}
.t1 svg{width:17px;height:17px;stroke:#fff;stroke-width:2.4;fill:none;stroke-linecap:round;stroke-linejoin:round}
.pl{display:flex;gap:8px;margin-top:14px}
.pl span{padding:6px 12px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);font-size:14.5px;font-weight:700;color:#ecfdf5}
.big{margin-top:22px;display:flex;align-items:baseline;gap:8px}
.big b{font-size:112px;font-weight:850;letter-spacing:-0.05em;line-height:.95}
.big span{font-size:38px;font-weight:800}
.ft{position:absolute;left:34px;right:34px;bottom:28px;display:flex;align-items:flex-end;justify-content:space-between}
.ft small{font-size:15px;font-weight:700;color:rgba(236,253,245,.75)}
.ft strong{font-size:38px;font-weight:850;letter-spacing:-0.03em}
.ti{margin-top:34px;font-size:35px;font-weight:850;letter-spacing:-0.035em}
.ck{margin-top:16px;display:flex;flex-direction:column;gap:10px}
.ck p{display:flex;align-items:center;gap:10px;font-size:19px;font-weight:600;color:#334155}
.ck i{display:flex;width:24px;height:24px;border-radius:50%%;background:#10a366;align-items:center;justify-content:center;flex-shrink:0}
.ck svg{width:14px;height:14px;stroke:#fff;stroke-width:3.2;fill:none;stroke-linecap:round;stroke-linejoin:round}
</style></head><body><div class="c">
<div class="hd">%s<div class="br"><b>카피클린</b><small>AI DETECTOR</small></div><span class="dm">skkc.co.kr</span></div>
<div class="pn">
 <div class="t1"><i><svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg></i>AI 유사도 개선 결제</div>
 <div class="pl"><span>안내받은 금액 결제</span><span>전담 에디터 개선</span></div>
 <div class="big"><b>%s</b><span>만 원</span></div>
 <div class="ft"><small>카피클린 상담 안내 금액</small><strong>%s원</strong></div>
</div>
<p class="ti">AI 유사도 개선 결제 (%s원)</p>
<div class="ck"><p>%s채팅 상담에서 안내받은 금액을 결제해요</p><p>%s결제가 확인되면 개선 작업을 이어서 진행해요</p></div>
</div></body></html>""" % (CSS, LOGO, man(a), "{:,}".format(a), "{:,}".format(a), CHECK, CHECK)

GUIDE = """<!doctype html><html><head><meta charset="utf-8"><style>%s
.g{width:1200px;height:800px;padding:64px 72px 56px;display:flex;flex-direction:column;background:radial-gradient(700px 420px at 90%% 0%%,rgba(16,163,102,.10),rgba(16,163,102,0) 70%%),linear-gradient(180deg,#f5f7fa,#ffffff)}
.hd{display:flex;align-items:center;gap:14px}
.lg{width:52px;height:52px;border-radius:15px;background:linear-gradient(135deg,#12a86a,#0b7a4b);display:flex;align-items:center;justify-content:center}
.lg svg{width:28px;height:28px;stroke:#fff;stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round}
.br b{display:block;font-size:30px;font-weight:800;line-height:1}
.br small{display:block;margin-top:5px;font-size:12px;font-weight:800;letter-spacing:.22em;color:#64748b}
.op{margin-left:auto;font-size:18px;font-weight:700;color:#64748b}
h1{margin-top:70px;font-size:54px;font-weight:850;letter-spacing:-0.04em}
h1 em{font-style:normal;color:#0b7a4b}
.sub{margin-top:14px;font-size:22px;color:#475569}
.st{margin-top:56px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.s{padding:30px 26px 32px;border-radius:22px;background:#fff;border:1px solid #e2e8f0;box-shadow:0 18px 40px -30px rgba(15,23,42,.35)}
.s em{display:block;font-style:normal;font-size:14px;font-weight:800;letter-spacing:.08em;color:#10a366}
.s b{display:block;margin-top:14px;font-size:25px;font-weight:800;letter-spacing:-0.03em}
.s p{margin-top:10px;font-size:17px;line-height:1.6;color:#475569}
.ft{margin-top:auto;padding-top:22px;border-top:1px solid #e2e8f0;display:flex;justify-content:space-between;font-size:16px;color:#64748b;font-weight:600}
</style></head><body><div class="g">
<div class="hd">%s<div class="br"><b>카피클린</b><small>AI DETECTOR</small></div><span class="op">운영 성균관컨설팅</span></div>
<h1>AI 유사도 개선 <em>결제 안내</em></h1>
<p class="sub">채팅 상담에서 안내받은 금액을 결제하셨다면, 아래 순서로 이어서 진행돼요.</p>
<div class="st">
 <div class="s"><em>STEP 01</em><b>금액 안내</b><p>채팅 상담에서 문서를 확인하고 개선 금액을 안내받아요.</p></div>
 <div class="s"><em>STEP 02</em><b>같은 금액 결제</b><p>안내받은 금액과 같은 상품으로 결제해요.</p></div>
 <div class="s"><em>STEP 03</em><b>결제 확인</b><p>상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.</p></div>
 <div class="s"><em>STEP 04</em><b>개선 진행</b><p>전담 에디터가 개선하고, 다시 확인한 뒤 전달해요.</p></div>
</div>
<div class="ft"><span>상담 skcdesk.channel.io</span><span>성균관컨설팅 · skkc.co.kr</span></div>
</div></body></html>""" % (CSS, LOGO)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 750, "height": 750}, device_scale_factor=1)
        for a in AMOUNTS:
            await pg.set_content(thumb_html(a))
            await pg.wait_for_timeout(250)
            await pg.screenshot(path=os.path.join(HERE, "hm-%d.jpg" % a), type="jpeg", quality=90)
        pg2 = await b.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=1)
        await pg2.set_content(GUIDE)
        await pg2.wait_for_timeout(300)
        await pg2.screenshot(path=os.path.join(HERE, "hm-guide.png"))
        await b.close()

asyncio.run(main())
print("ok", len(AMOUNTS))
