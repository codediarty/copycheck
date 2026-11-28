# -*- coding: utf-8 -*-
"""2026.11.28 대표 '40만원 보다 40 크레딧', '총 상품금액에만 1번만'
바로 결제 상품 대표 그림을 크레딧으로(1 크레딧 = 1만 원, 그림에는 원 금액을 넣지 않음)
  python3 render_credit.py  ->  tc-c5.jpg ~ tc-c200.jpg(논문 컨설팅, 상품 205~244) · hm-c5.jpg ~ hm-c100.jpg(카피클린 AI 유사도 개선, 상품 185~204)
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
    if kind == "tc":
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
    return html

async def main():
    jobs = [("render_tc.py", "tc", range(5, 201, 5)), ("render.py", "hm", range(5, 101, 5))]
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
        await b.close()

asyncio.run(main())
print("ok")
