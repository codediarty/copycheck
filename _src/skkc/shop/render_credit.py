# -*- coding: utf-8 -*-
"""2026.11.28 대표 '40만원 보다 40 크레딧', '총 상품금액에만 1번만'
바로 결제 상품 대표 그림을 크레딧으로(1 크레딧 = 1만 원, 그림에는 원 금액을 넣지 않음)
  python3 render_credit.py  ->  tc-c5.jpg ~ tc-c200.jpg(논문 컨설팅, 상품 205~244) · hm-c5.jpg ~ hm-c100.jpg(카피클린 AI 유사도 개선, 상품 185~204)
  10:42 대표 '논문 컨설팅만 하는 게 아니니 전문가 컨설팅으로' -> ex-c5.jpg ~ ex-c200.jpg · ex-guide.png(상품 205~244 새 그림 · 내려받는 안내)
render.py · render_tc.py 의 그림 틀을 그대로 쓰고, 금액 글자만 크레딧 글자로 바꿈"""
import asyncio, os
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    src = open(os.path.join(HERE, name), encoding="utf-8").read()
    src = src[:src.index("async def main")]
    ns = {"__file__": os.path.join(HERE, name)}
    exec(src, ns)
    return ns

def to_credit(html, n, kind):
    won = "{:,}".format(n * 10000)
    rep = [
        ('<div class="big"><b>%d</b><span>만 원</span></div>' % n, '<div class="big"><b>%d</b><span>크레딧</span></div>' % n),
        ('<strong>%s원</strong>' % won, ''),
    ]
    if kind == "ex":
        rep += [
            ('</svg></i>논문 컨설팅 결제</div>', '</svg></i>전문가 컨설팅 결제</div>'),
            ('<span>상담 후 안내받은 금액</span>', '<span>상담 후 안내받은 크레딧</span>'),
            ('<small>성균관컨설팅 상담 안내 금액</small>', '<small>성균관컨설팅 1:1 상담에서 정한 크레딧</small>'),
            ('<p class="ti">논문 컨설팅 결제 (%s원)</p>' % won, '<p class="ti">전문가 컨설팅 %d 크레딧</p>' % n),
            ('상담에서 안내받은 금액을 결제해요', '상담에서 안내받은 크레딧을 결제해요'),
            ('결과물 전달까지 결제금은 플랫폼이 보관해요', '결과물을 받기 전까지 결제금은 성균관컨설팅이 보관해요'),
        ]
    elif kind == "tc":
        rep += [
            ('<span>상담 후 안내받은 금액</span>', '<span>상담 후 안내받은 크레딧</span>'),
            ('<small>성균관컨설팅 상담 안내 금액</small>', '<small>성균관컨설팅 1:1 상담에서 정한 크레딧</small>'),
            ('<p class="ti">논문 컨설팅 결제 (%s원)</p>' % won, '<p class="ti">논문 컨설팅 %d 크레딧</p>' % n),
            ('상담에서 안내받은 금액을 결제해요', '상담에서 안내받은 크레딧을 결제해요'),
        ]
    else:
        rep += [
            ('<span>안내받은 금액 결제</span>', '<span>안내받은 크레딧 결제</span>'),
            ('<small>카피클린 상담 안내 금액</small>', '<small>카피클린 채팅 상담에서 정한 크레딧</small>'),
            ('<p class="ti">AI 유사도 개선 결제 (%s원)</p>' % won, '<p class="ti">AI 유사도 개선 %d 크레딧</p>' % n),
            ('채팅 상담에서 안내받은 금액을 결제해요', '채팅 상담에서 안내받은 크레딧을 결제해요'),
        ]
    for a, b in rep:
        assert html.count(a) == 1, (kind, n, a)
        html = html.replace(a, b)
    assert '원</' not in html and won not in html and '금액' not in html, (kind, n)
    assert kind != "ex" or '논문' not in html, (kind, n)
    return html

def guide_ex(g):
    rep = [
        ('<h1>논문 컨설팅 <em>결제 안내</em></h1>', '<h1>전문가 컨설팅 <em>결제 안내</em></h1>'),
        ('<p class="sub">상담에서 안내받은 금액을 결제하셨다면, 아래 순서로 이어서 진행돼요.</p>',
         '<p class="sub">상담에서 안내받은 크레딧을 결제하셨다면, 아래 순서로 이어서 진행돼요.<br>결과물을 받기 전까지 결제금은 전문가에게 가지 않고 성균관컨설팅이 안전하게 보관해요.</p>'),
        ('<b>금액 안내</b><p>1:1 상담에서 작업 범위 · 납기일 · 금액을 함께 정해요.</p>', '<b>크레딧 안내</b><p>1:1 상담에서 작업 범위 · 납기일 · 크레딧을 함께 정해요.</p>'),
        ('<b>같은 금액 결제</b><p>안내받은 금액과 같은 상품으로 결제해요.</p>', '<b>같은 크레딧 결제</b><p>안내받은 크레딧과 같은 상품으로 결제해요.</p>'),
    ]
    for a, b in rep:
        assert g.count(a) == 1, a
        g = g.replace(a, b)
    assert '논문' not in g and '금액' not in g
    return g

async def main():
    import sys
    jobs = [("render_tc.py", "tc", range(5, 201, 5)), ("render.py", "hm", range(5, 101, 5))]
    if "ex" in sys.argv[1:]:
        jobs = [("render_tc.py", "ex", range(5, 201, 5))]
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 750, "height": 750}, device_scale_factor=1)
        for src, kind, ns_ in jobs:
            ns = load(src)
            for n in ns_:
                html = to_credit(ns["thumb_html"](n * 10000), n, kind)
                await pg.set_content(html)
                await pg.wait_for_timeout(120)
                await pg.screenshot(path=os.path.join(HERE, "%s-c%d.jpg" % (kind, n)), type="jpeg", quality=90)
        if jobs[0][1] == "ex":
            pg2 = await b.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=1)
            await pg2.set_content(guide_ex(load("render_tc.py")["GUIDE"]))
            await pg2.wait_for_timeout(300)
            await pg2.screenshot(path=os.path.join(HERE, "ex-guide.png"))
        await b.close()

asyncio.run(main())
print("ok")
