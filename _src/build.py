# -*- coding: utf-8 -*-
"""카피체크(copycheck.skkc.co.kr) 정적 사이트 만들기

    python3 _src/build.py

docs/ 에 페이지 · sitemap.xml · robots.txt · llms.txt · llms-full.txt · rss.xml 을 씁니다(GitHub Pages 가 docs/ 를 그대로 서빙).
검사 · 휴머나이징 엔진은 AIMarker 서버(Apps Script 'AIMarker 서버' 프로젝트)의 같은 엔진, 카피체크 배포(버전 55, CC서버.gs 층)를 씁니다.
대표(2026.11.25 22:18): 'https://copycheck.skkc.co.kr/ 이것도 형제사이트로 추가해줘. aimarker 휴머나이징 엔진 그대로 넣어주고 결제도 아임웹
연결해주고 사이트 디자인도 대폭 개선해줘' · 'seo geo aeo 키워드도 대폭 추가하고'. 교차검증(AIMarker ↔ 카피체크 8/8 · AIHuman ↔ 카피체크 8/8 일치)
생성기 틀은 형제 사이트(AIHuman)와 같고, 글 · 디자인 · 검색어 쪽은 카피체크만을 위해 새로 씀
"""
import datetime
import difflib
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs")
sys.path.insert(0, HERE)
from icons import ICONS  # noqa: E402
import pages as P  # noqa: E402
import board as BD  # noqa: E402
import more_kw as MK  # noqa: E402
import new_pages as NP  # noqa: E402
P.GUIDES.extend(NP.GUIDES_NEW)   # 2026.11.24 새 가이드 네 편(검색어 주소 맨 위)
import kw1125 as KW  # noqa: E402
P.GUIDES.extend(KW.GUIDES)   # 2026.11.25 대표 '기존 쪽과 겹치지 않으면서 노출될 만한 키워드'(턴잇인 AI 검사 · GPTZero 한국어)

# ---------------- 설정 ----------------
SITE = "https://copycheck.skkc.co.kr"
HOST = "copycheck.skkc.co.kr"
BRAND = "카피체크"
BRAND_KO = "CopyCheck"
VER = "20261125c"
TODAY = "2026-11-25"
# 카피체크 배포(AIMarker 서버 프로젝트 버전 55, 엔진은 AIMarker 와 같음 · 2026.11.25 22:48, CC서버.gs 1.0.0)
API = "https://script.google.com/macros/s/AKfycbz3qUbNNd_21wHvi6EGHAz1_lrRJ7LAzzIYlIeg4U0bm8m-ioqHLPJV1UzatPmpOfkOFg/exec"
SHOP = "https://skkc.co.kr/shop_view?idx=%s&kaiec_buy=1"
# 성균관컨설팅(아임웹) 카피체크 전용 상품 번호. 서버는 스크립트 속성 CC_IDX 로 같은 번호를 cc1~cc4 로 봄
SHOP_IDX = {"lt": "170", "pl": "171", "pr": "172", "mx": "173"}   # 2026.11.25 등록(170 라이트 · 171 플러스 · 172 프로 · 173 맥스)
NAVER_VERIFY = ""   # 네이버 서치어드바이저 HTML 태그(등록하면 채움)
NAVER_VERIFY2 = ""
GOOGLE_VERIFY = ""
BING_VERIFY = "6CFE39150A28BBBB4694B507E2E689C0"   # Bing 웹마스터 도구(형제 사이트와 같은 계정의 메타 태그)
BING_VERIFY2 = "B673011129D1A8E10FC5977377C8BBBC"   # 2026.11.25 Bing 웹마스터 도구에 copycheck.skkc.co.kr 추가할 때 받은 메타 태그(위 것은 그대로 둠)
INDEXNOW_KEY = "0e96c841cd5c8ab919a5b65f1e2d453f"
GOOGLE_FILES = ["google67694027f26c117c.html"]   # 구글 서치 콘솔 URL 접두어 확인용(moistener22 계정 파일, 형제 사이트와 같음). 지우지 말 것
BIZ = {"name": "성균관컨설팅", "ceo": "이채연", "no": "272-32-01885", "ecom": "제2026-경기송탄-0622",
       "addr": "경기도 수원시 장안구 서부로 2066 성균관대학교 브릿지팩토리(연구실)", "mail": "contact@skkc.co.kr"}
# 가격 · 토큰은 AIMarker 개인 토큰 · 형제 사이트와 같음(서버 ah1~ah4). 요금 카드는 정가 없이 간단하게(형제 사이트 방침과 같게)
PACKS = [
    {"id": "lt", "name": "라이트", "tok": 100, "price": 9900, "per": "99원", "who": "자기소개서 · 짧은 과제", "chars": "약 16,600자", "pg": "약 10페이지", "sub": "AI 작성률 낮추기, 미니멀하게", "doc": "레포트"},
    {"id": "pl", "name": "플러스", "tok": 350, "price": 19900, "per": "약 57원", "who": "레포트 · 과제 여러 편", "chars": "약 58,300자", "pg": "약 35페이지", "sub": "AI 작성률 낮추기, 합리적으로", "doc": "레포트"},
    {"id": "pr", "name": "프로", "tok": 1000, "price": 39900, "per": "약 40원", "who": "논문 · 학위논문", "chars": "약 166,600자", "pg": "약 100페이지", "best": "추천 요금제", "save": "플러스 대비 이용 단가 30% 절감", "sub": "AI 작성률 낮추기, 더 효과적으로", "doc": "논문"},
    {"id": "mx", "name": "맥스", "tok": 2000, "price": 69900, "per": "약 34원", "who": "논문 전체 · 여러 편", "chars": "약 333,300자", "pg": "약 250페이지", "top": "최대 할인 혜택", "save": "플러스 대비 이용 단가 39% 절감", "sub": "반복 변환으로 AI 작성률 극한까지 낮추기", "doc": "논문"},
]
COST = {"check": (0, 0), "hum": (6, 3)}   # 2026.11.23 대표 '1.5배는 앞으로 결제분부터': 휴머나이징 100자 0.6토큰(1,000자 6) · 최소 3(서버 AM서버.gs 1.4.0). 예전 메모 → 1,000자당 토큰 · 최소 토큰(서버와 같게: AI 작성률 검사 무료, 휴머나이징 1,000자 6토큰)


def esc(s):
    return html.escape(str(s), quote=True)


def ico(name, cls="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS.get(name, ""))


def won(n):
    return "{:,}원".format(n)


def shop(pid):
    ix = SHOP_IDX.get(pid) or ""
    return SHOP % ix if ix else ""


# 로고: 예전 카피체크 'CC' 표지를 다듬은 표지(검은 사각 · 흰 C · 초록 확인 표시) + 글자 로고(Copy 검정 · Check 초록) + 카피체크
MARK = '<svg class="lg-m" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><rect width="40" height="40" rx="11" fill="#0b0f14"/><path d="M24.6 13.4a8.6 8.6 0 1 0 0 13.2" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/><path d="m21.2 20.3 3.6 3.6 7.4-8" fill="none" stroke="#22c38e" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
LOGO = '<a class="logo" href="/" aria-label="%s(%s) 홈">%s<span class="lg-t">Copy<b>Check</b></span><span class="lg-k">카피체크</span></a>' % (BRAND, BRAND_KO, MARK)
LOGO_W = '<a class="logo logo-w" href="/" aria-label="%s(%s) 홈">%s<span class="lg-t">Copy<b>Check</b></span><span class="lg-k">카피체크</span></a>' % (BRAND, BRAND_KO, MARK.replace('fill="#0b0f14"', 'fill="#fff"').replace('stroke="#fff"', 'stroke="#0b0f14"'))

# 메뉴: 형제 사이트에서 대표가 정한 대로 'AI 휴머나이저(AI 작성률 낮추기)' 하나가 첫 칸(헷갈리지 않고 결제로). 검사기 이름은 메뉴에 쓰지 않음
NAV = [("", "AI 작성률 낮추기"), ("ai-similarity-check/", "AI 유사도 검사"), ("ai-humanizer/", "AI 휴머나이저"), ("@menu", "상황별 안내"),
       ("pricing/", "요금"), ("guide/", "가이드"), ("board/", "커뮤니티"), ("faq/", "FAQ")]   # 2026.11.25 형제 사이트 방침대로 'AI 작성률 낮추기'가 첫 칸, 검사기 이름은 메뉴에 쓰지 않음


def menu_links(path, mobile=False):
    """'상황별 안내' 펼침 칸. 첫 화면(path == "")에는 검사기 이름 대신 일반 말(첫 화면 방침)"""
    out = []
    for h, items in NP.MENU_GROUPS:
        links = "".join('<a href="/%s"%s>%s</a>' % (u, ' aria-current="page"' if path == u else "", (t if (path == "" or not t2) else t2)) for u, t, t2 in items)
        out.append('<div class="dd-g"><b>%s</b>%s</div>' % (h, links))
    return "".join(out)


def header(path):
    in_menu = any(path == u for _, items in NP.MENU_GROUPS for u, _t, _t2 in items)
    parts = []
    for p, t in NAV:
        if p == "@menu":
            parts.append('<div class="dd%s" data-dd><button class="dd-b" type="button" aria-expanded="false" aria-controls="ddMenu"%s>%s%s</button>'
                         '<div class="dd-m" id="ddMenu"><div class="dd-in">%s</div></div></div>' % (" cur" if in_menu else "", ' aria-current="true"' if in_menu else "", t, ico("chev", "ico dd-i"), menu_links(path)))
        else:
            parts.append('<a href="/%s"%s>%s</a>' % (p, ' aria-current="page"' if path == p else "", t))
    nav = "".join(parts)
    mnav = "".join('<a href="/%s">%s</a>' % (p, t) for p, t in NAV if p != "@menu")
    mnav += '<details class="m-dd"><summary>상황별 안내%s</summary><div class="m-dd-in">%s</div></details>' % (ico("chev", "ico dd-i"), menu_links(path, True))
    top = ('<div class="topbar"><div class="wrap"><span class="dot" aria-hidden="true"></span><span><b>AI 작성률 검사 무료</b> · 가입 없이 20만 자<span class="hide-s"> · 한글 · 워드 · PDF 그대로</span></span>'
           '<a href="/#tool" data-tool>지금 검사하기 →</a></div></div>')
    return (top + '<header class="hd" id="hd"><div class="wrap hd-in">%s<nav class="nav" aria-label="주요 메뉴">%s</nav>'
            '<div class="hd-r"><a class="btn btn-g btn-s hd-tk" href="/pricing/">토큰 충전</a><a class="btn btn-p btn-s" href="/#tool" data-tool>%s<span class="hl">무료 AI 작성률 검사</span><span class="hs">무료 검사</span></a>'
            '<button class="menu-btn" id="menuBtn" type="button" aria-label="메뉴 열기" aria-expanded="false" aria-controls="mnav">%s</button></div></div></header>'
            '<nav class="mnav" id="mnav" aria-label="모바일 메뉴">%s<a href="/#tool" data-tool>무료 AI 작성률 검사</a><a href="/#example">실제 측정 결과</a><a href="/technology/">휴머나이징 기술</a><a href="/about/">서비스 소개</a></nav>') % (LOGO, nav, ico("search"), ico("menu"), mnav)


def guide_by(slug):
    return next(g for g in P.GUIDES if g["slug"] == slug)


GSLUG = {}


def gpath(g):
    return GSLUG.get(g["slug"], g["slug"]) + "/"


def guide_at(new):
    return next(g for g in P.GUIDES if gpath(g) == new.strip("/") + "/")


# 바닥글 검색어 링크(첫 화면은 검사기 이름 없이, 그 밖의 쪽은 검사기 이름 검색어도 더함)
FT_KW = [("/", "AI 작성률 낮추기"), ("/ai-similarity-check/", "AI 유사도 검사"), ("/ai-similarity-lower/", "AI 유사도 낮추기"), ("/ai-writing-check/", "AI 작성 여부 확인"),
         ("/ai-rate-check/", "AI 작성률 검사 무료"), ("/ai-humanizer/", "AI 휴머나이저"), ("/ai-rate-lower/", "AI 작성률 줄이기"), ("/ai-similarity-meaning/", "AI 유사도란"),
         ("/thesis-ai-check/", "학위논문 AI 검사"), ("/resume-ai-check/", "자기소개서 AI 판별"), ("/report-ai-check/", "레포트 AI 검사"), ("/chatgpt-detect-avoid/", "챗GPT 티 안 나게"),
         ("/ai-tone-remove/", "AI 말투 없애기"), ("/sentence-rewrite-natural/", "문장 자연스럽게"), ("/technology/", "휴머나이징 기술"), ("/pricing/", "카피체크 요금")]
FT_KW_HOME = [("/ai-detector-false-positive/", "AI 탐지기 오탐"), ("/ai-check-free-guide/", "AI 검사 무료"), ("/copykiller-ai-lower/", "표절 검사 AI 표시 풀기"), ("/gptkiller-report-read/", "AI 판정 결과 보는 법")]
FT_KW_SUB = [("/copykiller-ai-lower/", "카피킬러 AI 작성률 낮추기"), ("/gptkiller-report-read/", "GPT킬러 결과 보는 법"), ("/ai-detector-false-positive/", "AI 탐지기 오탐"),
             ("/ai-check-free-guide/", "AI 검사 무료"), ("/turnitin-ai-korean/", "턴잇인 AI 검사 대비"), ("/ai-use-policy-check/", "생성형 AI 사용 규정")]


def footer(home=False):
    gl = [("/guide/", "가이드 전체")] + [("/" + gpath(guide_by(x)), guide_by(x)["kw"].split(" · ")[0]) for x in ["ai-similarity-meaning", "thesis-ai-check", "resume-ai-check", "chatgpt-detect-avoid", "ai-check-free-guide"]]
    cols = [
        ("서비스", [("/#tool", "무료 AI 작성률 검사"), ("/ai-similarity-check/", "AI 유사도 검사"), ("/ai-similarity-lower/", "AI 유사도 낮추기"), ("/pricing/", "요금 · 토큰 충전"), ("/faq/", "자주 묻는 질문")]),
        ("가이드", gl),
        ("회사 · 정책", [("/about/", "서비스 소개"), ("/technology/", "휴머나이징 기술"), ("/board/", "커뮤니티"), ("/terms/", "이용약관"), ("/privacy/", "개인정보처리방침"), ("mailto:" + BIZ["mail"], "문의 " + BIZ["mail"])]),
    ]
    c = "".join('<div><h4>%s</h4><ul>%s</ul></div>' % (h, "".join('<li><a href="%s">%s</a></li>' % (u, t) for u, t in L)) for h, L in cols)
    kw = "".join('<a href="%s"><span>%s</span></a>' % (u, t) for u, t in FT_KW + (FT_KW_HOME if home else FT_KW_SUB))
    return ('<footer class="ft"><div class="wrap"><div class="ft-top"><div>%s<p>카피체크 | 제출 전 AI 작성률 검사 · AI 휴머나이징.<br>걸린 문장을 찾고, 그 문장만 사람 문장으로 바꾸고, 다시 잽니다.</p><div class="ft-kw">%s</div></div>%s</div>'
            '<div class="ft-biz"><b>운영</b> %s · 대표 %s · 사업자등록번호 %s · 통신판매업 신고 %s<br>%s · %s<br>성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증<br>'
            '다른 AI 탐지 서비스의 이름은 각 권리자의 상표이며, 카피체크는 해당 서비스와 제휴 관계가 없습니다. AI 작성률과 판정은 카피체크 판정 기준으로 계산한 추정값입니다.<br>© 2026 카피체크(CopyCheck). All rights reserved.</div></div></footer>'
            '<div class="mcta" id="mcta"><a class="btn btn-p" href="/#tool" data-tool>%s무료 검사</a><a class="btn btn-g" href="/pricing/">요금 보기</a></div>') % (
        LOGO_W, kw, c, BIZ["name"], BIZ["ceo"], BIZ["no"], BIZ["ecom"], BIZ["addr"], BIZ["mail"], ico("search"))


# ---------------- 구조화 데이터 ----------------
ALT = [BRAND_KO, "카피 체크", "Copy Check", "카피체크 AI 검사", HOST]
ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "alternateName": ALT, "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/logo-512.png", "width": 512, "height": 512},
       "slogan": "카피체크 | 제출 전 AI 작성률 검사 · AI 휴머나이징",
       "parentOrganization": {"@type": "Organization", "name": BIZ["name"], "taxID": BIZ["no"]},
       "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": BIZ["mail"], "availableLanguage": ["ko"]},
       "address": {"@type": "PostalAddress", "streetAddress": "서부로 2066 성균관대학교 브릿지팩토리", "addressLocality": "수원시 장안구", "addressRegion": "경기도", "postalCode": "16419", "addressCountry": "KR"}}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "name": BRAND, "alternateName": ALT, "url": SITE + "/", "inLanguage": "ko-KR", "publisher": {"@id": SITE + "/#org"}}
APP = {"@type": "WebApplication", "@id": SITE + "/#app", "name": BRAND + " AI 작성률 검사 · AI 휴머나이저", "alternateName": [BRAND_KO, "AI 유사도 검사", "AI 작성률 낮추기 도구"], "url": SITE + "/",
       "applicationCategory": "UtilitiesApplication", "operatingSystem": "Web", "inLanguage": "ko-KR",
       "description": "한국어 AI 작성률(AI 유사도) 검사와 AI 휴머나이징. 논문 · 레포트 · 자기소개서에서 AI 탐지기에 걸리는 문장을 문장 단위로 찾아 사람 문장으로 바꾸고, 같은 기준으로 다시 잽니다.",
       "featureList": ["AI 작성률 무료 검사(20만 자)", "문장 단위 AI 검출 표시", "AI 휴머나이징(한국어 전용 엔진, 생성 AI 사용 안 함)", "한글 HWP · HWPX · 워드 DOCX · PDF 파일 지원", "말투 자동 맞춤", "숫자 · 이름 · 인용 보존"],
       "offers": {"@type": "AggregateOffer", "priceCurrency": "KRW", "lowPrice": "0", "highPrice": "69900", "offerCount": "5"}, "publisher": {"@id": SITE + "/#org"}}


def ld_faq(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}


def ld_crumbs(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + "/" + u} for i, (n, u) in enumerate([("홈", "")] + trail)]}


def ld_howto(name, steps):
    return {"@type": "HowTo", "name": name, "inLanguage": "ko-KR", "totalTime": "PT2M", "step": [{"@type": "HowToStep", "position": i + 1, "name": a, "text": b} for i, (a, b) in enumerate(steps)]}


def ld_offers():
    return {"@type": "Product", "@id": SITE + "/pricing/#product", "name": BRAND + " AI 휴머나이징 토큰", "brand": {"@type": "Brand", "name": BRAND},
            "description": "AI 작성률 검사와 AI 휴머나이징에 쓰는 토큰. 월 구독 없이 한 번 충전하고, 남은 토큰은 기한 없이 쓸 수 있습니다.",
            "image": [SITE + "/assets/product/cc-pr-1x1.jpg", SITE + "/assets/img/og.png"], "category": "디지털콘텐츠 이용권",
            "offers": [{"@type": "Offer", "name": "%s %s토큰" % (p["name"], "{:,}".format(p["tok"])), "price": str(p["price"]), "priceCurrency": "KRW", "availability": "https://schema.org/InStock",
                        "url": (shop(p["id"]).replace("&kaiec_buy=1", "") if shop(p["id"]) else (SITE + "/pricing/")), "seller": {"@type": "Organization", "name": BIZ["name"]}} for p in PACKS]}


# ---------------- 페이지 틀 ----------------
PAGES = []   # (path, title, desc, lastmod, priority)


def page(path, title, desc, body, *, ld=None, tool=False, og=None, ptype="website", noindex=False, priority="0.7", lastmod=TODAY, extra_head="", keywords=""):
    url = SITE + "/" + path
    ogimg = og or (SITE + "/assets/img/og.png?v=" + VER)
    graph = [ORG, WEBSITE] + (ld or [])
    head = ['<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">',
            '<title>%s</title><meta name="description" content="%s">' % (esc(title), esc(desc)),
            ('<meta name="keywords" content="%s">' % esc(keywords)) if keywords else "",
            '<link rel="canonical" href="%s">' % url,
            '<link rel="alternate" hreflang="ko" href="%s"><link rel="alternate" hreflang="x-default" href="%s">' % (url, url),
            '<meta name="robots" content="%s">' % ("noindex,follow" if noindex else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"),
            '<meta property="og:type" content="%s"><meta property="og:site_name" content="%s(%s)"><meta property="og:locale" content="ko_KR">' % (ptype, BRAND, BRAND_KO),
            '<meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:url" content="%s">' % (esc(title), esc(desc), url),
            '<meta property="og:image" content="%s"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="%s">' % (ogimg, esc(BRAND + " · AI 작성률 검사와 AI 휴머나이징")),
            '<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="%s"><meta name="twitter:description" content="%s"><meta name="twitter:image" content="%s">' % (esc(title), esc(desc), ogimg),
            '<meta name="theme-color" content="#0b0f14"><meta name="format-detection" content="telephone=no"><meta name="author" content="%s"><meta name="application-name" content="%s">' % (BRAND, BRAND),
            ('<link rel="icon" href="/favicon.ico?v=%s" sizes="any"><link rel="icon" href="/assets/img/favicon.svg?v=%s" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png?v=%s"><link rel="manifest" href="/site.webmanifest?v=%s">' % (VER, VER, VER, VER)),
            '<link rel="alternate" type="application/rss+xml" title="%s 가이드" href="/rss.xml">' % BRAND]
    if NAVER_VERIFY:
        head.append('<meta name="naver-site-verification" content="%s">' % NAVER_VERIFY)
    if NAVER_VERIFY2:
        head.append('<meta name="naver-site-verification" content="%s">' % NAVER_VERIFY2)
    if GOOGLE_VERIFY:
        head.append('<meta name="google-site-verification" content="%s">' % GOOGLE_VERIFY)
    if BING_VERIFY:
        head.append('<meta name="msvalidate.01" content="%s">' % BING_VERIFY)
    if BING_VERIFY2:
        head.append('<meta name="msvalidate.01" content="%s">' % BING_VERIFY2)
    head.append('<script>document.documentElement.className+=" js";setTimeout(function(){if(!window.HZ_SITE){var a=document.querySelectorAll(".rv");for(var i=0;i<a.length;i++)a[i].className+=" in"}},3000)</script>')
    head.append('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin><link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">')
    if tool:
        head.append('<link rel="stylesheet" href="/assets/tool.css?v=%s">' % VER)
    head.append('<link rel="stylesheet" href="/assets/cc.css?v=%s">' % VER)
    head.append(extra_head)
    head.append('<script type="application/ld+json">%s</script>' % json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")))
    head.append("</head>")
    scripts = ['<script src="/assets/site.js?v=%s" defer></script>' % VER]
    if tool:
        scripts = ['<script>window.HZ_API=%s;</script>' % json.dumps(API),
                   '<script src="/assets/products.js?v=%s" defer></script>' % VER,
                   '<script src="/assets/am.js?v=%s" defer></script>' % VER,
                   '<script src="/assets/textin.js?v=%s" defer></script>' % VER,
                   '<script src="/assets/humanize.js?v=%s" defer></script>' % VER] + scripts
    doc = "".join(head) + '<body data-root="/">' + '<a class="sr" href="#main">본문 바로가기</a>' + header(path) + '<main id="main">' + body + "</main>" + footer(path == "") + "".join(scripts) + "</body></html>"
    fp = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    if path.endswith(".html"):   # 404.html · 예전 커뮤니티 글 주소(board/*.html)는 파일 이름 그대로
        fp = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(doc)
    if not noindex:
        PAGES.append((path, title, desc, lastmod, priority))


# ---------------- 검사 도구(엔진 화면, humanize.js 가 움직임) ----------------
def tool_html():
    packs = []
    for p in PACKS:
        cls = ' class="best"' if p.get("best") else (' class="top"' if p.get("top") else "")
        tag = '<i class="tg">%s</i>' % p["best"] if p.get("best") else ('<i class="tg top">%s</i>' % p["top"] if p.get("top") else "")
        sv = '<i class="hz17-sv">%s</i>' % p["save"] if p.get("save") else ""
        packs.append('<label%s><input type="radio" name="product" value="%s"%s><span>%s<b class="nm">%s</b><b class="tk">%s<small>토큰</small></b><b class="pr">%s<small>토큰당 %s</small></b>%s<small class="ds">%s · 검사와 휴머나이징 %s</small></span></label>' % (
            cls, p["id"], " checked" if p.get("best") else "", tag, p["name"], "{:,}".format(p["tok"]), won(p["price"]), p["per"], sv, p["who"], p["chars"]))
    return P.TOOL_TPL.format(ico_upload=ico("upload"), ico_search=ico("search"), ico_pen=ico("pen"), ico_lock=ico("lock"), ico_x=ico("x"), ico_spark=ico("sparkle"), ico_arrow=ico("arrow"),
                             packs="".join(packs), biz_no=BIZ["no"], mail=BIZ["mail"], brand=BRAND)


# ---------------- 예시 화면(실제 엔진 값) ----------------
DEMO = json.load(open(os.path.join(HERE, "demo.json"), encoding="utf-8"))


def tok(s):
    return re.findall(r"\S+\s*", s)


def sent_split(t):
    return [x for x in re.split(r"(?<=[.!?])\s+", t.strip()) if x]


def _chg(x, y, mode):
    """mode: anim(예시 화면, 바뀔 말에 새 말을 data-n 으로) · src(원문) · dst(다듬은 글)"""
    sx, sy = x.rstrip(), y.rstrip()
    tx, ty = x[len(sx):], y[len(sy):]
    if mode == "src":
        return ('<span class="x">%s</span>%s' % (esc(sx), esc(tx))) if sx else ""
    if mode == "dst":
        return ('<mark>%s</mark>%s' % (esc(sy), esc(ty))) if sy else ""
    return '<span class="x" data-n="%s">%s</span>%s' % (esc(sy + ty), esc(sx), esc(tx)) if (sx or sy) else ""


def _sent_ops(src, dst):
    """원문 문장마다 [(종류, 원래 말, 바뀐 말)] 목록. 휴머나이징이 문장을 잇거나 나눠도 원문 문장 경계로 자름"""
    A, B = tok(src), tok(dst)
    sid, k = [], 0
    for t in A:
        sid.append(k)
        if re.search(r"[.!?]\s*$", t):
            k += 1
    n = (sid[-1] + 1) if sid else 0
    per = [[] for _ in range(n)]
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        y = "".join(B[j1:j2])
        if i1 == i2:   # 넣기만 한 말: 앞 문장 끝에 붙임
            tgt = sid[i1 - 1] if i1 > 0 else 0
            per[tgt].append(("c", "", y))
            continue
        segs = []
        for i in range(i1, i2):
            if not segs or segs[-1][0] != sid[i]:
                segs.append([sid[i], []])
            segs[-1][1].append(A[i])
        for m, (si, toks) in enumerate(segs):
            x = "".join(toks)
            if op == "equal":
                per[si].append(("e", x, x))
            else:
                per[si].append(("c", x, y if m == 0 else ""))
    return per


BAND_LABEL = {"부적합": "AI 작성률 높음"}   # 2026.11.24 대표: '부적합'은 공식 제출 기준이 있는 것처럼 보일 수 있어 예시 화면에서는 'AI 작성률 높음'. 엔진 원값(demo.json)은 그대로
DEMO_MEASURED = "카피체크 엔진(HUM 2.5) 적용 결과입니다. 문서의 특성과 AI 작성 패턴에 따라 감소율은 달라질 수 있으며, 여러 번 변환해 더 낮출 수 있습니다."   # 2026.11.24 대표 전 → 후(예전 문구는 demo.json measured 에 그대로)


def _band(b):
    return BAND_LABEL.get(b, b)


def demo_samples():
    out = []
    for S in DEMO["samples"]:
        flags, scores = set(S.get("ai", [])), S.get("scores", {})
        bs, as_ = sent_split(S["src"]), sent_split(S["dst"])
        ascores = S.get("after_scores", {}) if len(bs) == len(as_) else {}
        per = _sent_ops(S["src"], S["dst"])
        anim, src, dst, nch = [], [], [], 0
        for i, ops in enumerate(per):
            n = sum(1 for o in ops if o[0] == "c")
            nch += n
            isai = i in flags
            p0, p1 = scores.get(str(i)), ascores.get(str(i))
            tag = ('<i class="demo-tag" data-p0="%s" data-p1="%s">AI 패턴</i>' % (p0, "" if p1 is None else p1)) if (isai and p0 is not None) else ""
            okt = '<i class="demo-tag ok">AI 미검출</i>' if (isai and p0 is not None and n and S["after"].get("n") == 0) else ""
            A_ = "".join(esc(o[1]) if o[0] == "e" else _chg(o[1], o[2], "anim") for o in ops)
            S_ = "".join(esc(o[1]) if o[0] == "e" else _chg(o[1], o[2], "src") for o in ops)
            D_ = "".join(esc(o[2]) if o[0] == "e" else _chg(o[1], o[2], "dst") for o in ops)
            anim.append('<span class="s%s">%s%s</span> ' % (" ai" if isai else "", A_.rstrip(), tag))
            src.append('<span class="s%s">%s%s</span> ' % (" ai" if isai else "", S_.rstrip(), tag.replace("demo-tag", "demo-tag st")))
            dst.append('<span class="s%s">%s%s</span> ' % (" hu" if n else "", D_.rstrip(), okt))
        bf, af = dict(S["before"], band=_band(S["before"]["band"])), dict(S["after"], band=_band(S["after"]["band"]))
        out.append({"k": S["k"], "label": S["label"], "file": S["file"], "before": bf, "after": af, "changes": nch,
                    "doc": '<p class="ai-blk">' + "".join(anim).strip() + "</p>",
                    "src": '<p class="ai-blk">' + "".join(src).strip() + "</p>", "dst": '<p class="hu-blk">' + "".join(dst).strip() + "</p>"})
    return out


SAMPLES = demo_samples()


def demo_json():
    return '<script type="application/json" id="hzDemoData">%s</script>' % json.dumps({"samples": SAMPLES, "measured": DEMO_MEASURED}, ensure_ascii=False).replace("</", "<\\/")


def demo_card():
    S = SAMPLES
    tabs = "".join('<button type="button" role="tab" aria-selected="%s">%s</button>' % ("true" if i == 0 else "false", s["label"]) for i, s in enumerate(S))
    first = S[0]
    return ('<div class="demo" id="demo" aria-label="AI 작성률 검사와 휴머나이징 예시(실제 엔진 값)">'
            '<div class="demo-bar"><i></i><i></i><i></i><span class="fn">%s<span>%s</span></span><div class="demo-tabs" role="tablist" aria-label="예시 글 종류">%s</div></div>'
            '<div class="demo-scan" aria-hidden="true"></div>'
            '<div class="demo-meter"><div class="dm from bad"><small>휴머나이징 전 AI 작성률</small><b>%s<small style="font-size:18px">%%</small> <em>%s</em></b><div class="dm-bar"><i style="width:%s%%"></i></div></div>'
            '<span class="dm-arr" aria-hidden="true">%s</span>'
            '<div class="dm to good wait"><small>휴머나이징 후 AI 작성률</small><b>– <em>대기</em></b><div class="dm-bar"><i style="width:0"></i></div></div></div>'
            '<div class="demo-legend"><span class="a"><i></i>AI 패턴 감지 문장</span><span class="h"><i></i>AI 패턴 개선 문장</span><span class="demo-state" aria-live="polite"></span></div>'
            '<div class="demo-doc">%s</div>'
            '<div class="demo-ft"><a class="btn btn-p btn-s demo-go" href="#tool" data-hum-go>%s<span>AI 작성률 낮추기</span></a>'
            '<a class="btn btn-g btn-s" href="#tool" data-tool>무료 AI 작성률 검사</a><p class="note">%s</p></div></div>') % (
        ico("file"), esc(first["file"]), tabs, first["before"]["rate"], first["before"]["band"], first["before"]["rate"], ico("arrow"),
        first["doc"], ico("trend_down"), esc(DEMO_MEASURED))


def compare_block():
    S = SAMPLES
    tabs = "".join('<button type="button" role="tab" aria-selected="%s">%s</button>' % ("true" if i == 0 else "false", s["label"]) for i, s in enumerate(S))
    return ('<div class="cmp-tabs" role="tablist" aria-label="예시 글 종류">%s</div><div class="cmp" id="cmp">'
            '<div class="cmp-col"><div class="cmp-h"><span>휴머나이징 전</span><span class="pill l bad"></span></div><div class="cmp-t l"></div></div>'
            '<div class="cmp-col"><div class="cmp-h"><span>휴머나이징 후</span><span class="pill r good"></span></div><div class="cmp-t r"></div></div></div>'
            '<div class="cmp-foot"></div><p class="center measured">%s</p>') % (tabs, esc(DEMO_MEASURED))


def faq_html(faq):
    return '<div class="faq">' + "".join('<details><summary>%s</summary><div class="a"><p>%s</p></div></details>' % (esc(q), a) for q, a in faq) + "</div>"


REP_LINE = "반복 변환할수록 AI 작성률은 계속 낮아집니다. 여러 번 변환하여 AI 작성 흔적을 극한까지 줄여보세요."   # 형제 사이트 요금 칸 아래 반복 변환 안내와 같게


PLUS_UNIT = 19900 / 350   # 2026.11.22 대표: 카피휴먼처럼 프로 · 맥스는 '플러스 단가로 샀을 때 금액'을 줄 그어 보여 줌(같은 토큰 × 플러스 토큰당 가격)
LIST_PRICE = {"pr": 60000, "mx": 120000}   # 2026.11.23 22:23 대표: 프로 · 맥스 정가 60,000원 · 120,000원(아임웹 정가와 같게, 줄 그어 보여 줌)
STRIKE = True   # 2026.11.24 23:09 대표 '취소선 가격 삭제'로 껐다가 23:38 대표 '프로랑 맥스는 취소선을 넣는게 좋을 것 같아 기존처럼 60,000 120,000'으로 다시 켬
PRICE_FN = "절감률은 플러스의 이용 단가(토큰당 약 57원)와 비교한 값이고, 줄 그은 금액은 정가입니다."   # 2026.11.24 23:09 대표(배지 · 혜택 문구, 취소선 가격 삭제). 예전: 절약률은 … 줄 그은 금액은 정가입니다.


def plus_strike(p):
    if not p.get("save") or not STRIKE:   # 2026.11.24 23:09 대표 '취소선 가격 삭제'
        return ""
    return '<s title="정가"><span class="sr">정가 </span>%s</s>' % won(LIST_PRICE.get(p["id"]) or int(round(p["tok"] * PLUS_UNIT)))


def save_badge(p, tag="p", cls="sv2"):
    if not p.get("save"):
        return ""
    m = re.search(r"\d+%", p["save"])
    return '<%s class="%s">플러스 대비 이용 단가 <b>%s 절감</b></%s>' % (tag, cls, m.group(0) if m else p["save"], tag)   # 2026.11.24 23:09 대표 문구(예전 '플러스 대비 토큰당 약 N% 절약')


def pricing_cards(cta_text="충전하기"):
    out = []
    for p in PACKS:
        cls = "pk" + (" best" if p.get("best") else (" top" if p.get("top") else ""))
        tag = '<span class="tg">%s</span>' % p["best"] if p.get("best") else ('<span class="tg top">%s</span>' % p["top"] if p.get("top") else "")
        link, bcls, label = shop(p["id"]), ("btn-p" if p.get("best") else "btn-g"), "%s %s" % (p["name"], cta_text)
        # 2026.11.25 18:21 대표 'AIMarker · 카피휴먼처럼 누르면 다시 고르는 충전 창(성균관컨설팅 운영 · 안전결제 안내)을 먼저': 충전 창으로.
        # 도구가 있는 쪽은 humanize.js [data-buy] 가 그 자리에서 창, 요금 쪽 등은 첫 화면 #buy-칸 으로 가서 창. 예전(바로 결제 페이지 새 창) 줄은 아래 주석
        # btn = ('<a class="btn %s" href="%s" target="_blank" rel="noopener" data-pack="%s">%s</a>' % (bcls, esc(link), p["id"], label)) if link else \
        # ('<a class="btn %s" href="/#buy-%s" data-buy-pack="%s">%s</a>' % (bcls, p["id"], p["id"], label))
        btn = '<a class="btn %s" href="/#buy-%s" data-buy="%s" data-pack="%s">%s</a>' % (bcls, p["id"], p["id"], p["id"], label)
        sv = save_badge(p)
        out.append('<div class="%s rv">%s<h3>%s</h3><p class="who">%s</p><p class="tk2"><b>%s</b>토큰</p><p class="pr2"><b>%s</b>%s<span>토큰당 %s · 부가세 포함</span></p>%s'
                   '<p class="use">%s 검사와 휴머나이징 서비스 <b>%s</b></p>%s</div>' % (
                       cls, tag, p["name"], p["sub"], "{:,}".format(p["tok"]), won(p["price"]), plus_strike(p), p["per"], sv, p["doc"], p["pg"], btn))
    return '<div class="price">' + "".join(out) + "</div>" + '<p class="price-rep">%s</p>' % REP_LINE + '<p class="price-fn">%s</p>' % PRICE_FN


def calc_block():
    docs = [("자소서 1문항", 1500), ("레포트", 5000), ("논문 한 장", 15000), ("학위논문 본문", 80000)]
    btns = "".join('<button type="button" data-chars="%d" aria-pressed="%s">%s</button>' % (n, "true" if i == 1 else "false", t) for i, (t, n) in enumerate(docs))
    data = json.dumps({"cost": COST, "packs": [{"id": p["id"], "name": p["name"], "tok": p["tok"], "price": p["price"], "link": shop(p["id"])} for p in PACKS]}, ensure_ascii=False)
    return ('<div class="calc rv" id="calc"><div class="calc-in"><h3>내 글에는 토큰이 얼마나 들까요?</h3><p>글 종류를 고르거나 글자 수를 맞춰 보세요. 서버가 실제로 빼는 값과 같은 셈입니다.</p>'
            '<div class="calc-docs" role="group" aria-label="글 종류">%s</div>'
            '<div class="calc-row"><label class="sr" for="calcN">글자 수</label><input type="range" id="calcN" min="500" max="200000" step="500" value="5000"><output id="calcO" for="calcN">5,000자</output></div>'
            '<div class="calc-opt"><label><input type="checkbox" id="calcC" checked>AI 작성률 검사</label><label><input type="checkbox" id="calcH" checked>AI 휴머나이징</label><label><input type="checkbox" id="calcT">한 번 더 다듬기</label></div></div>'
            '<div class="calc-out" aria-live="polite"><dl><div><dt>AI 작성률 검사</dt><dd id="calcCc">무료</dd></div><div><dt>AI 휴머나이징</dt><dd id="calcHc">30토큰</dd></div>'
            '<div class="sum"><dt>합계</dt><dd id="calcS">30토큰</dd></div></dl><p class="calc-rec" id="calcR"></p><a class="btn btn-p" id="calcB" href="/pricing/">충전하기</a></div>'
            '<script type="application/json" id="calcData">%s</script></div>') % (btns, data)


def cta_band(h="제출 전 30초, AI 작성률부터 확인하세요", p="가입도 카드 등록도 없이 무료로 검사합니다. 걸리는 문장이 있을 때만 휴머나이징하면 됩니다."):
    return ('<section class="sec-s cta-sec"><div class="wrap"><div class="cta rv"><h2>%s</h2><p>%s</p><div class="btns"><a class="btn btn-p btn-l" href="/#tool" data-tool>%s무료로 AI 작성률 검사</a>'
            '<a class="btn btn-g btn-l" href="/pricing/">요금 보기</a></div></div></div></section>') % (h, p, ico("search"))


def crumbs_html(trail):
    return '<nav class="crumb" aria-label="현재 위치"><a href="/">홈</a>' + "".join('<span>›</span>' + ('<a href="/%s">%s</a>' % (u, esc(n)) if i < len(trail) - 1 else '<span>%s</span>' % esc(n)) for i, (n, u) in enumerate(trail)) + "</nav>"


def proof_line():
    """2026.11.24 대표 전 → 후: 92% → 7% / 한 번의 휴머나이징으로 AI 작성률 85%p 감소 / 자체 엔진 측정 사례이며 문서에 따라 결과는 달라질 수 있습니다.
    (예전: '논문 예시, 한 번의 휴머나이징 · 실제 엔진으로 잰 값입니다. 글마다 결과는 다릅니다.') 숫자는 첫 예시(demo.json 논문) 그대로, 차이는 빼서 셈"""
    S = SAMPLES[0]
    a, b = S["before"]["rate"], S["after"]["rate"]
    return ('<p class="hero-proof"><span class="hp-n"><s>%d%%</s><i>→</i><em>%d%%</em></span><span class="hp-t"><b>한 번의 휴머나이징으로 AI 작성률 %d%%p 감소</b><small>자체 엔진 측정 사례이며 문서에 따라 결과는 달라질 수 있습니다.</small></span></p>' % (a, b, a - b))


ORBIT = ('<svg class="orbit scanfx" viewBox="0 0 980 760" aria-hidden="true" focusable="false"><defs>'
         '<linearGradient id="sg1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22c38e" stop-opacity="0"/><stop offset=".5" stop-color="#5ee6b4" stop-opacity=".9"/><stop offset="1" stop-color="#22c38e" stop-opacity="0"/></linearGradient>'
         '<radialGradient id="sg2"><stop offset="0" stop-color="#5ee6b4" stop-opacity=".55"/><stop offset="1" stop-color="#5ee6b4" stop-opacity="0"/></radialGradient></defs>'
         '<g class="doc" fill="none" stroke="rgba(255,255,255,.10)" stroke-width="1.2"><rect x="560" y="70" width="330" height="430" rx="18"/><rect x="600" y="120" width="250" height="10" rx="5"/>'
         '<rect x="600" y="150" width="210" height="10" rx="5"/><rect x="600" y="180" width="236" height="10" rx="5"/><rect x="600" y="210" width="190" height="10" rx="5"/>'
         '<rect x="600" y="250" width="244" height="10" rx="5"/><rect x="600" y="280" width="200" height="10" rx="5"/><rect x="600" y="310" width="228" height="10" rx="5"/></g>'
         '<circle cx="760" cy="230" r="220" fill="url(#sg2)" opacity=".35"/>'
         '<rect class="beam" x="540" y="0" width="370" height="3" rx="1.5" fill="url(#sg1)"/></svg>')


TECH_PAGE = True   # 2026.11.24 build_tech() 가 /technology/ 를 만듦(첫 화면 '저감 기술' 알약이 그 쪽 링크)


def eb2_html():
    if TECH_PAGE:
        return '<a class="eyebrow eb-2" href="/technology/"><b>%s</b>AI 작성률 저감 기술</a>' % ico("trend_down")
    return '<p class="eyebrow eb-2"><b>%s</b>AI 작성률 저감 기술</p>' % ico("trend_down")


def hero(eyebrow, h1, lead, pts=None):
    """첫 화면: 어두운 바탕(궤도선) 왼쪽 글(알약 · 제목 · 설명 · 파일 상자 · 장점 · 실측 한 줄) + 오른쪽 실제 엔진 예시.
    검사 도구는 바로 아래 떠 있는 흰 판(tool_section). 좁은 화면은 예시를 도구 아래로 옮김(site.js)"""
    pts = pts or ["문장 단위 AI 작성률 검사", "걸린 문장만 휴머나이징", "HWP · Word · PDF 지원"]   # 2026.11.24 대표 전 → 후(예전: 한국어 전용 엔진 · 문장 단위 AI 작성률 · 한글 · 워드 · PDF 그대로)
    return ('<section class="hero" id="top">%s<div class="wrap"><div class="hero-grid">'
            '<div class="hero-copy"><div class="eb-row"><p class="eyebrow eb-1"><b>%s</b>%s</p>%s</div><h1 class="h1">%s</h1><p class="lead">%s</p>'
            '<div class="hero-up" data-hero-drop><div class="hu-h"><span class="hu-ic">%s</span><p><b>파일 업로드 한 번으로 AI 작성률 확인</b><span>한글(HWP · HWPX) · 워드(DOCX) · PDF · 텍스트, 끌어다 놓아도 됩니다</span></p></div>'
            '<div class="hu-b"><button class="btn btn-p" type="button" data-hero-pick>%s파일 업로드</button><a class="btn btn-g" href="#tool" data-tool>%s텍스트 입력</a></div></div>'
            '<ul class="hero-pts">%s</ul>%s</div>'
            '<div class="hero-demo" id="heroDemo">%s</div>'
            '</div></div></section>') % (
        ORBIT, ico("check"), eyebrow, eb2_html(), h1, lead, ico("upload"), ico("upload"), ico("pen"), "".join("<li>%s%s</li>" % (ico("check"), t) for t in pts), proof_line(), demo_card())


def tool_section(flat=False):
    badges = [("lock", "가입 없이 무료"), ("file", "20만 자"), ("check", "한글 · 워드 · PDF"), ("shield", "글은 저장하지 않음")]
    return ('<section class="tool-sec%s" aria-labelledby="toolH"><div class="wrap"><div class="tool-panel">'
            '<div class="tool-head"><h2 id="toolH"><span class="ic">%s</span>AI 작성률 검사 · AI 휴머나이징</h2><div class="tool-badges">%s</div></div>'
            '<div id="tool" class="tool-w">%s</div></div><div class="demo-slot" id="demoSlot"></div></div></section>') % (
        " tool-flat" if flat else "", ico("sparkle"), "".join('<span>%s%s</span>' % (ico(i), t) for i, t in badges), tool_html())


def example_section(h2="AI 휴머나이징 전과 후,<br>실제 엔진으로 잰 결과", alt=False):
    return ('<section class="sec%s" id="example"><div class="wrap"><div class="center"><p class="kick">%s실제 측정 결과</p><h2 class="h2">%s</h2>'
            '<p class="sub">아래 예시는 %s 엔진에 그대로 넣어 잰 실제 값입니다. 보라색은 AI 패턴이 감지된 문장, 초록색은 AI 패턴을 개선한 문장입니다.</p></div>%s</div></section>') % (
        " alt" if alt else "", ico("eye"), h2, BRAND, compare_block())


def price_section(alt=True):
    return ('<section class="sec%s" id="price"><div class="wrap"><div class="center"><p class="kick">%s요금</p><h2 class="h2">AI 휴머나이징 가격,<br><em>쓴 만큼만</em> 냅니다</h2><p class="sub">월 구독 없이 한 번 충전하면 글자 수만큼만 빠지고, 남은 토큰은 기한 없이 쓸 수 있습니다. 검사는 언제나 무료로 먼저 해 보세요.</p></div>%s'
            '<p class="price-note">AI 작성률 검사 무료 · AI 휴머나이징 1,000자 6토큰 · 1토큰 100원 · 부가세 포함 · 결제는 운영사 성균관컨설팅 결제 페이지(가입 없이 카드 · 간편결제)</p>%s</div></section>') % (
        " alt" if alt else "", ico("card"), pricing_cards(), calc_block())


def guides_section():
    G = [guide_by(s) for s in P.HOME_GUIDES]
    cards = "".join('<a class="gcard rv" href="/%s"><small>%s · %s</small><h3>%s</h3><p>%s</p><span class="go">읽어 보기 →</span></a>' % (gpath(g), g["cat"], esc(g["kw"]), esc(g["h1"]), esc(g["desc"])) for g in G)
    return ('<section class="sec alt" id="guides"><div class="wrap"><div class="center"><p class="kick">%s가이드</p><h2 class="h2">AI 작성률 낮추기 가이드</h2>'
            '<p class="sub">AI 탐지기가 무엇을 보고 AI 작성률을 매기는지, 논문 · 자기소개서별로 어떻게 낮추는지 정리했습니다.</p></div><div class="gcards">%s</div>'
            '<p class="center" style="margin-top:26px"><a class="btn btn-g" href="/guide/">가이드 모두 보기</a></p></div></section>') % (ico("file"), cards)


# ---------------- 홈 ----------------
def build_home():
    H = P.HOME
    body = hero(H["eyebrow"], H["h1"], H["lead"])
    body += tool_section()
    body += demo_json()
    body += P.metrics_strip(ico)
    body += P.why_section(ico)
    body += example_section()
    body += P.scale_section(ico)
    body += P.how_section(ico)
    body += P.features_section(ico, BRAND)
    body += P.compare_table(ico, BRAND)
    body += P.usecases_section(ico)
    body += guides_section()
    body += price_section(alt=False)
    body += '<section class="sec alt" id="faq"><div class="wrap-n"><div class="center"><p class="kick">%s자주 묻는 질문</p><h2 class="h2">AI 휴머나이징, 궁금한 점부터</h2></div>%s<p class="center" style="margin-top:22px"><a class="btn btn-g" href="/faq/">질문 모두 보기</a></p></div></section>' % (ico("chat"), faq_html(H["faq"]))
    body += cta_band()
    ld = [APP, ld_faq(H["faq"]), ld_howto("AI 작성률 낮추기(%s)" % BRAND, P.HOW_STEPS)]
    page("", H["title"], H["desc"], body, ld=ld, tool=True, priority="1.0", keywords=H["keywords"])


def build_pricing():
    trail = [("요금", "pricing/")]
    body = ('<section class="ph"><div class="wrap">%s<h1 class="h1">카피체크 요금 · 토큰 충전</h1><p class="lead">월 구독 없이 한 번 충전하고 쓴 만큼만 씁니다. AI 작성률 검사는 무료, 휴머나이징 1,000자 6토큰. 남은 토큰은 기한 없이 쓸 수 있습니다.</p></div></section>'
            '<section class="sec-s"><div class="wrap">%s<p class="price-note">모든 가격은 부가세 포함입니다. 결제는 운영사 성균관컨설팅 결제 페이지에서 가입 없이 카드 · 간편결제로 합니다. 결제하면 보통 1분 안에, 적은 이메일로 16자리 토큰 코드가 갑니다.</p>%s</div></section>') % (
        crumbs_html(trail), pricing_cards(), calc_block())
    body += P.pricing_detail(ico)
    body += MK.PRICING_MORE   # 11.23: 요금 쪽만의 구역(사이트마다 다른 글)
    body += '<section class="sec alt"><div class="wrap-n"><h2 class="h2 center">결제 · 토큰 자주 묻는 질문</h2>%s</div></section>' % faq_html(P.PRICE_FAQ)
    body += cta_band("먼저 무료로 검사해 보세요", "AI 작성률이 높게 나온 문장만 휴머나이징하면 토큰을 아낄 수 있습니다.")
    page("pricing/", "카피체크 요금 · AI 휴머나이징 가격 · 토큰 충전 | 카피체크", "카피체크 AI 휴머나이징 가격. 라이트 100토큰 9,900원부터 맥스 2,000토큰 69,900원까지. 월 구독 없이 한 번 충전, AI 작성률 검사 무료 · 휴머나이징 1,000자 6토큰.",
         body, ld=[ld_offers(), ld_faq(P.PRICE_FAQ), ld_crumbs(trail)], priority="0.9", keywords="카피체크 요금, 카피체크 가격, AI 휴머나이징 가격, AI 유사도 낮추기 가격, AI 작성률 낮추기 비용")


def build_faq():
    trail = [("자주 묻는 질문", "faq/")]
    groups = [("서비스와 사용", P.HOME["faq"] + P.MORE_FAQ), ("결제와 토큰", P.PRICE_FAQ)]
    allq = [x for _, L in groups for x in L]
    gl = "".join('<a href="/%s">%s</a>' % (gpath(g), esc(g["kw"].split(" · ")[0])) for g in P.GUIDES)
    body = '<section class="ph"><div class="wrap">%s<h1 class="h1">자주 묻는 질문</h1><p class="lead">AI 작성률 · AI 유사도 검사, 휴머나이징, 결제와 토큰에 대해 자주 받는 질문을 모았습니다.</p></div></section>' % crumbs_html(trail)
    body += '<section class="sec-s"><div class="wrap-n">%s<h2 class="faq-h">검색어로 찾는 가이드</h2><div class="links">%s</div></div></section>' % ("".join('<h2 class="faq-h">%s</h2>%s' % (h, faq_html(L)) for h, L in groups), gl)
    body += cta_band()
    page("faq/", "자주 묻는 질문 · AI 작성률 · AI 유사도 FAQ | 카피체크", "AI 유사도와 AI 작성률의 차이, 무료 검사 범위, 휴머나이징으로 얼마나 내려가는지, 글이 저장되는지, 결제와 토큰은 어떻게 되는지 답해 드립니다.",
         body, ld=[ld_faq(allq), ld_crumbs(trail)], priority="0.8")


def build_guides():
    trail0 = [("가이드", "guide/")]
    cats = []
    for g in P.GUIDES:
        if g["cat"] not in cats:
            cats.append(g["cat"])
    cards = "".join('<a class="gcard rv" href="/%s"><small>%s · %s</small><h3>%s</h3><p>%s</p><span class="go">읽어 보기 →</span></a>' % (gpath(g), g["cat"], esc(g["kw"]), esc(g["h1"]), esc(g["desc"])) for g in P.GUIDES)
    body = ('<section class="ph"><div class="wrap">%s<h1 class="h1">카피체크 가이드</h1><p class="lead">AI 유사도의 뜻부터 검사기 결과 읽는 법, 글 종류별 대비, AI 말투 없애기까지 정리했습니다.</p></div></section>'
            '<section class="sec-s"><div class="wrap"><div class="gcards">%s</div></div></section>') % (crumbs_html(trail0), cards)
    body += MK.GUIDE_HUB   # 11.23 3차: 가이드 모음 쪽만의 읽는 순서 · 쓰는 방식
    body += cta_band()
    page("guide/", "가이드 · AI 유사도 · AI 작성률 낮추는 법 | 카피체크", "AI 유사도의 뜻, 카피킬러 · GPT킬러 · 턴잇인 결과 읽는 법, 학위논문 · 자기소개서 · 레포트 AI 검사 대비, AI 말투 없애기까지 정리한 카피체크 가이드.",
         body, ld=[ld_crumbs(trail0), {"@type": "CollectionPage", "name": BRAND + " 가이드", "url": SITE + "/guide/", "hasPart": [{"@type": "Article", "headline": g["h1"], "url": SITE + "/" + gpath(g)} for g in P.GUIDES]}], priority="0.8")
    for g in P.GUIDES:
        trail = [("가이드", "guide/"), (g["h1"], gpath(g))]
        toc = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', g["body"])
        toc_html = ('<nav class="toc" aria-label="목차"><b>목차</b><ol>%s</ol></nav>' % "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in toc)) if toc else ""
        idx = P.GUIDES.index(g)
        others = [P.GUIDES[(idx + k) % len(P.GUIDES)] for k in (1, 2, 3)]
        rel = "".join('<a class="gcard" href="/%s"><small>%s</small><h3>%s</h3><p>%s</p></a>' % (gpath(o), o["cat"], esc(o["h1"]), esc(o["desc"])) for o in others)
        faq = ('<h2 id="faq">자주 묻는 질문</h2>' + faq_html(g["faq"])) if g.get("faq") else ""
        body = ('<article><section class="ph"><div class="wrap-n">%s<p class="kick">%s</p><h1 class="h1">%s</h1><p class="meta"><span>%s 편집팀</span><span>%s</span><span>읽는 데 %d분</span></p></div></section>'
                '<section class="sec-s"><div class="wrap-n"><div class="answer">%s</div>%s<div class="prose">%s%s</div>'
                '<div class="gcta"><h2>내 글의 AI 작성률, 지금 바로 확인하세요</h2><p>가입 없이 무료 · 문장마다 AI 검출 여부를 보여 드립니다.</p><a class="btn btn-p btn-l" href="/#tool">%s무료로 AI 작성률 검사</a></div>'
                '</div></section></article><section class="sec-s alt"><div class="wrap"><h2 class="h2">함께 읽으면 좋은 글</h2><div class="gcards">%s</div></div></section>') % (
            crumbs_html(trail), esc(g["cat"] + " · " + g["kw"]), esc(g["h1"]), BRAND, g["date"].replace("-", "."), max(2, len(re.sub(r"<[^>]+>", "", g["body"])) // 650), g["answer"], toc_html, g["body"], faq, ico("search"), rel)
        art = {"@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": "ko-KR", "datePublished": g["date"], "dateModified": g["date"], "keywords": g["kw"].replace(" · ", ", "),
               "author": {"@type": "Organization", "name": BRAND + " 편집팀", "url": SITE + "/about/"}, "publisher": {"@id": SITE + "/#org"},
               "mainEntityOfPage": SITE + "/" + gpath(g), "image": [SITE + "/assets/img/og.png"], "articleSection": g["cat"]}
        ld = [art, ld_crumbs(trail)] + ([ld_faq(g["faq"])] if g.get("faq") else [])
        page(gpath(g), g["title"], g["desc"], body, ld=ld, ptype="article", priority="0.7", lastmod=g["date"],
             extra_head='<meta property="article:published_time" content="%sT09:00:00+09:00">' % g["date"], keywords=g["kw"].replace(" · ", ", "))


def build_landing():
    for L in P.LANDING:
        trail = [(L["crumb"], L["path"])]
        cards = "".join('<div class="card rv"><span class="ic">%s</span><h3>%s</h3><p>%s</p></div>' % (ico(i), esc(h), esc(t)) for i, h, t in L["cards"])
        rows = "".join('<tr><td>%s</td><td>%s</td><td class="me">%s</td></tr>' % (esc(a), esc(b), esc(c)) for a, b, c in L["table"])
        rel = "".join('<a class="gcard" href="/%s"><small>%s</small><h3>%s</h3><p>%s</p></a>' % (gpath(g), g["cat"], esc(g["h1"]), esc(g["desc"])) for g in [guide_at(x) for x in L["related"][:3]])
        body = ('<section class="ph"><div class="wrap">%s<p class="kick">%s</p><h1 class="h1">%s</h1><p class="lead">%s</p></div></section>') % (
            crumbs_html(trail), esc(L["kw"]), esc(L["h1"]), L["lead"])
        body += tool_section(flat=True)
        body += demo_json()
        body += ('<section class="sec"><div class="wrap-n"><div class="answer">%s</div></div>'
                 '<div class="wrap" style="margin-top:26px"><div class="grid4">%s</div></div></section>') % (L["answer"], cards)
        body += ('<section class="sec alt"><div class="wrap-n"><h2 class="h2 center">%s</h2><div class="tbl-w"><table class="tbl"><thead><tr><th scope="col">기준</th><th scope="col">왜 중요한가</th><th scope="col" class="me">%s</th></tr></thead><tbody>%s</tbody></table></div></div></section>') % (
            esc(L["table_h"]), BRAND, rows)
        if L.get("body"):   # 11.23 3차: 검색어 쪽마다 고유 글(more_kw.py)
            body += '<section class="sec"><div class="wrap-n prose">%s</div></section>' % L["body"]
        body += example_section(h2="실제 엔진으로 잰<br>AI 휴머나이징 전과 후")
        body += price_section(alt=True)
        body += '<section class="sec"><div class="wrap-n"><h2 class="h2 center">자주 묻는 질문</h2>%s</div></section>' % faq_html(L["faq"])
        body += '<section class="sec-s alt"><div class="wrap"><h2 class="h2">함께 읽으면 좋은 글</h2><div class="gcards">%s</div></div></section>' % rel
        body += cta_band()
        ld = [APP, ld_faq(L["faq"]), ld_crumbs(trail), {"@type": "WebPage", "@id": SITE + "/" + L["path"] + "#page", "url": SITE + "/" + L["path"], "name": L["title"].split(" | ")[0],
                                                       "description": L["desc"], "inLanguage": "ko-KR", "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#app"}}]
        page(L["path"], L["title"], L["desc"], body, ld=ld, tool=True, priority="0.9", keywords=L["keywords"])


def build_tech():
    """2026.11.24 /technology/ AI 작성률 저감 기술(첫 화면 '저감 기술' 알약 · 위 메뉴 '휴머나이징 기술')"""
    T = NP.TECH
    trail = [("휴머나이징 기술", T["path"])]
    steps = "".join('<li class="tk-st rv"><span class="tk-n">%d</span><span class="ic">%s</span><h3>%s</h3><p>%s</p></li>' % (i + 1, ico(ic), esc(h), esc(t)) for i, (ic, h, t) in enumerate(T["steps"]))
    rows = "".join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (esc(a), esc(b), esc(c)) for a, b, c in T["patterns"])
    cases = "".join('<tr><th scope="row">%s</th><td>%d%%</td><td>%d%%</td><td class="dn">%d%%p 감소</td></tr>' % (esc(S["label"]), S["before"]["rate"], S["after"]["rate"], S["before"]["rate"] - S["after"]["rate"]) for S in SAMPLES)
    body = ('<section class="ph tk-ph"><div class="wrap">%s<p class="kick">%s</p><h1 class="h1">%s</h1><p class="lead">%s</p>'
            '<p class="tk-cta"><a class="btn btn-p" href="/#tool" data-tool>%s무료로 AI 작성률 검사</a><a class="btn btn-g" href="/#example">휴머나이징 전후 보기</a></p></div></section>') % (
        crumbs_html(trail), esc(T["kick"]), T["h1"], esc(T["lead"]), ico("search"))
    body += ('<section class="sec-s"><div class="wrap"><h2 class="h2 center">한눈에 보는 4단계</h2><ol class="tk-flow">%s</ol></div></section>') % steps
    body += ('<section class="sec alt"><div class="wrap-n"><h2 class="h2 center">무엇을 지우나요: AI 문장 패턴 다섯 가지</h2><div class="tbl-w"><table class="tbl"><thead><tr><th scope="col">패턴</th><th scope="col">예</th><th scope="col" class="me">처리 방식</th></tr></thead><tbody>%s</tbody></table></div></div></section>') % rows
    body += ('<section class="sec"><div class="wrap-n prose"><h2 id="why">생성 AI로 다시 쓰지 않는 까닭</h2>%s<h2 id="keep">원문의 의미를 지키는 장치</h2><ul>%s</ul>'
             '<h2 id="case">자체 엔진 측정 사례</h2><div class="tbl-w"><table class="tbl tk-case"><thead><tr><th scope="col">글 종류</th><th scope="col">휴머나이징 전</th><th scope="col">휴머나이징 후</th><th scope="col">AI 작성률 변화</th></tr></thead><tbody>%s</tbody></table></div>'
             '<p class="meta">2026.11.25 카피체크 엔진(HUM 2.5), 한 번의 휴머나이징. 자체 엔진 측정 사례이며 문서에 따라 결과는 달라질 수 있습니다.</p>'
             '<h2 id="data">넣은 글은 저장하지 않습니다</h2>%s<h2 id="note">알아 둘 점</h2><ul>%s</ul></div></section>') % (
        T["why"], "".join("<li>%s</li>" % esc(x) for x in T["keep"]), cases, T["data"], "".join("<li>%s</li>" % esc(x) for x in T["note"]))
    body += '<section class="sec alt"><div class="wrap-n"><h2 class="h2 center">자주 묻는 질문</h2>%s</div></section>' % faq_html(T["faq"])
    body += cta_band("원리는 같고, 결과는 내 글로 확인하세요", "가입 없이 무료로 AI 작성률을 검사하고, 걸린 문장만 휴머나이징하면 됩니다.")
    art = {"@type": "TechArticle", "headline": "카피체크 휴머나이징 기술: 재고, 고치고, 다시 잽니다", "description": T["desc"], "inLanguage": "ko-KR", "datePublished": NP.DATE, "dateModified": NP.DATE,
           "keywords": T["keywords"], "author": {"@type": "Organization", "name": BRAND + " 편집팀", "url": SITE + "/about/"}, "publisher": {"@id": SITE + "/#org"},
           "about": {"@id": SITE + "/#app"}, "mainEntityOfPage": SITE + "/" + T["path"], "image": [SITE + "/assets/img/og.png"]}
    ld = [art, ld_howto("AI 작성률 검사와 휴머나이징 4단계(%s)" % BRAND, [(h, t) for _, h, t in T["steps"]]), ld_faq(T["faq"]), ld_crumbs(trail)]
    page(T["path"], T["title"], T["desc"], body, ld=ld, ptype="article", priority="0.9", keywords=T["keywords"])


def build_static():
    for S in P.STATIC:
        trail = [(S["crumb"], S["path"])]
        body = '<section class="ph"><div class="wrap-n">%s<h1 class="h1">%s</h1>%s</div></section><section class="sec-s"><div class="wrap-n prose">%s</div></section>' % (
            crumbs_html(trail), S["h1"], ('<p class="lead">%s</p>' % S["lead"]) if S.get("lead") else "", S["body"])
        page(S["path"], S["title"], S["desc"], body, ld=[ld_crumbs(trail)], priority=S.get("prio", "0.4"))
    body = '<section class="ph"><div class="wrap-n"><h1 class="h1">페이지를 찾을 수 없습니다</h1><p class="lead">주소가 바뀌었거나 없는 페이지입니다.</p><p><a class="btn btn-p" href="/">홈으로</a> <a class="btn btn-g" href="/#tool" data-tool>무료 AI 작성률 검사</a></p></div></section>'
    page("404.html", "페이지를 찾을 수 없습니다 | " + BRAND, "요청한 페이지를 찾을 수 없습니다.", body, noindex=True)


# ---------------- 커뮤니티(예전 카피체크 글 8편, 주소 /board/*.html 그대로) ----------------
def build_board():
    trail0 = [("커뮤니티", "board/")]
    cards = "".join('<a class="gcard rv" href="/%s"><small>%s · %s</small><h3>%s</h3><p>%s</p><span class="go">읽어 보기 →</span></a>' % (
        p["path"], esc(p["cat"]), p["date"].replace("-", "."), esc(p["h1"]), esc(p["desc"])) for p in reversed(BD.POSTS))
    body = ('<section class="ph"><div class="wrap">%s<h1 class="h1">카피체크 커뮤니티</h1><p class="lead">AI 검사에 걸린 사례와 대비법을 카피체크 편집팀이 정리합니다. 채용 서류, 대학 과제, 학위논문까지 실제로 일어나는 일을 다룹니다.</p></div></section>'
            '<section class="sec-s"><div class="wrap"><div class="gcards">%s</div></div></section>') % (crumbs_html(trail0), cards)
    body += cta_band()
    page("board/", "커뮤니티 · AI 검사 사례와 대비법 | 카피체크", "자기소개서 AI 판정, 대학 레포트 AI 적발, 학위논문 AI 유사도 반려, AI 워터마크까지. AI 검사에 걸린 사례와 대비법을 정리한 카피체크 커뮤니티입니다.",
         body, ld=[ld_crumbs(trail0), {"@type": "CollectionPage", "name": BRAND + " 커뮤니티", "url": SITE + "/board/", "hasPart": [{"@type": "BlogPosting", "headline": p["h1"], "url": SITE + "/" + p["path"]} for p in BD.POSTS]}], priority="0.7")
    for i, p in enumerate(BD.POSTS):
        trail = [("커뮤니티", "board/"), (p["h1"], p["path"])]
        others = [BD.POSTS[(i + k) % len(BD.POSTS)] for k in (1, 2, 3)]
        rel = "".join('<a class="gcard" href="/%s"><small>%s</small><h3>%s</h3><p>%s</p></a>' % (o["path"], esc(o["cat"]), esc(o["h1"]), esc(o["desc"])) for o in others)
        body = ('<article><section class="ph"><div class="wrap-n">%s<p class="kick">%s</p><h1 class="h1">%s</h1><p class="meta"><span>%s 편집팀</span><span>%s</span><span>읽는 데 %d분</span></p></div></section>'
                '<section class="sec-s"><div class="wrap-n">%s<div class="prose">%s</div>'
                '<div class="gcta"><h2>내 글은 어떻게 읽힐까요? 제출 전에 확인하세요</h2><p>가입 없이 무료 · 걸린 문장을 바로 보여 드리고, 그 문장만 사람 문장으로 바꿉니다.</p><a class="btn btn-p btn-l" href="/#tool">%s무료로 AI 작성률 검사</a></div>'
                '</div></section></article><section class="sec-s alt"><div class="wrap"><h2 class="h2">커뮤니티의 다른 글</h2><div class="gcards">%s</div></div></section>') % (
            crumbs_html(trail), esc(p["cat"]), esc(p["h1"]), BRAND, p["date"].replace("-", "."), max(2, len(re.sub(r"<[^>]+>", "", p["body"])) // 650),
            ('<div class="answer">%s</div>' % esc(p["lede"])) if p["lede"] else "", p["body"], ico("search"), rel)
        art = {"@type": "BlogPosting", "headline": p["h1"], "description": p["desc"], "inLanguage": "ko-KR", "datePublished": p["date"], "dateModified": TODAY,
               "author": {"@type": "Organization", "name": BRAND + " 편집팀", "url": SITE + "/about/"}, "publisher": {"@id": SITE + "/#org"},
               "mainEntityOfPage": SITE + "/" + p["path"], "image": [SITE + "/assets/img/og.png"], "articleSection": p["cat"]}
        page(p["path"], p["title"] + " | 카피체크", p["desc"], body, ld=[art, ld_crumbs(trail)], ptype="article", priority="0.6", lastmod=TODAY,
             extra_head='<meta property="article:published_time" content="%sT09:00:00+09:00">' % p["date"])


# ---------------- 넘기는 쪽: 토큰 메일의 /humanize/?pass= 단추 · 검색어 주소를 첫 화면으로 ----------------
# 11.22 오후: ai-humanizer/ 는 넘김 쪽에서 검색어 페이지(build_landing)로 바꿈. humanizing/ · free/ 는 같은 뜻의 새 검색어 주소로 넘김
MERGED = {"humanize/": "/#tool", "results/": "/#example", "check/": "/#tool", "ai-detector/": "/ai-writing-check/", "humanizer/": "/ai-humanizer/"}


def build_redirects():
    moved = dict(MERGED)
    for g in P.GUIDES:   # 예전 가이드 주소 → 새 검색어 주소
        moved["guide/%s/" % g["slug"]] = "/" + gpath(g)
    for path, to in moved.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        base, hsh = to.split("#")[0], (("#" + to.split("#")[1]) if "#" in to else "")
        doc = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>%s · AI 작성률 검사</title><link rel="canonical" href="%s%s">'
               '<meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=%s"><meta name="viewport" content="width=device-width,initial-scale=1">'
               '<script>location.replace(%s + (location.search || "") + (location.hash || %s));</script></head>'
               '<body><p><a href="%s">%s %s 이동합니다</a></p></body></html>') % (
            BRAND, SITE, base, to, json.dumps(base), json.dumps(hsh), to, BRAND, "첫 화면으로" if base == "/" else "새 주소로")
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)


# ---------------- 검색 · AI 검색용 파일 ----------------
def build_seo():
    urls = []
    for path, title, desc, lastmod, pr in PAGES:
        urls.append("<url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>" % (SITE, path, lastmod, "weekly" if pr >= "0.8" else "monthly", pr))
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    bots = ["Googlebot", "Yeti", "Daum", "Bingbot", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot", "Applebot-Extended", "CCBot", "Meta-ExternalAgent", "cohere-ai", "DuckAssistBot", "MistralAI-User"]
    rob = "# %s(%s) · 검색 엔진과 AI 검색이 모두 읽을 수 있게 엽니다\n" % (BRAND, BRAND_KO) + "".join("User-agent: %s\nAllow: /\n\n" % b for b in bots) + "User-agent: *\nAllow: /\nDisallow: /assets/vendor/\n\nSitemap: %s/sitemap.xml\n" % SITE
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(rob)
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(P.llms_txt(SITE, PAGES, PACKS, SAMPLES))
    open(os.path.join(OUT, "llms-full.txt"), "w", encoding="utf-8").write(P.llms_full(SITE, PACKS, SAMPLES))
    items = "".join("<item><title>%s</title><link>%s/%s</link><guid>%s/%s</guid><pubDate>%s</pubDate><description>%s</description></item>" % (
        esc(g["h1"]), SITE, gpath(g), SITE, gpath(g), datetime.datetime.strptime(g["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 09:00:00 +0900"), esc(g["desc"])) for g in P.GUIDES)
    open(os.path.join(OUT, "rss.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>%s 가이드</title><link>%s/guide/</link><description>AI 작성률 · AI 유사도 검사와 AI 휴머나이징 가이드</description><language>ko</language>%s</channel></rss>' % (BRAND, SITE, items))
    open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8").write(json.dumps({"name": BRAND + " AI 작성률 검사 · AI 휴머나이저", "short_name": BRAND, "start_url": "/", "display": "standalone", "background_color": "#ffffff", "theme_color": "#0b0f14", "lang": "ko",
                                                                                         "icons": [{"src": "/assets/img/logo-192.png?v=" + VER, "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/logo-512.png?v=" + VER, "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False))
    open(os.path.join(OUT, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
    for gf in GOOGLE_FILES:
        open(os.path.join(OUT, gf), "w").write("google-site-verification: %s" % gf)
    open(os.path.join(OUT, "CNAME"), "w").write(HOST + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("\n")
    prods = {"shop": SHOP, "idx": {k: v for k, v in SHOP_IDX.items()}, "items": {p["id"]: {"name": p["name"], "tok": p["tok"], "price": p["price"]} for p in PACKS}}
    open(os.path.join(OUT, "assets", "products.js"), "w", encoding="utf-8").write("/* %s 상품(빌드가 만듦: _src/build.py SHOP_IDX · PACKS) */\nwindow.AMP = %s;\n" % (BRAND, json.dumps(prods, ensure_ascii=False)))


BANNED = ["충분", "수강", "자격증", "선착순", "민간", "수료"]   # 프로젝트 지침: 사이트 문구에 쓰지 않는 말


def verify():
    bad = []
    for dp, dn, fn in os.walk(OUT):
        if "/assets" in dp:
            continue
        for f in fn:
            if not f.endswith((".html", ".txt", ".xml")):
                continue
            s = open(os.path.join(dp, f), encoding="utf-8").read()
            if "—" in s:
                bad.append("줄표(—) " + os.path.join(dp, f))
            if re.search(r">\s*None\s*<", s):
                bad.append("None 글자 " + os.path.join(dp, f))
            for w in ["한국휴머나이징", "한국휴머나이저", "humanizer.co.kr", "humanizing.ai.kr", "humanai.io.kr", "AIMarker", "aimarker", "Humani(", "휴머나이(Humani", "AIHuman", "aihuman", "AI휴먼", "YOUR-DOMAIN", "smartstore"]:
                if w in s:
                    bad.append("다른 브랜드 이름 %s %s" % (w, os.path.join(dp, f)))
            for w in BANNED:
                if w in re.sub(r"<[^>]+>", " ", s):
                    bad.append("쓰지 않는 말 %s %s" % (w, os.path.join(dp, f)))
            if f == "index.html" and dp == OUT and re.search(r"카피킬러|GPT킬러|지피티킬러", re.sub(r"<script[\s\S]*?</script>", "", s)):
                bad.append("첫 화면에 검사기 이름")
            for m in re.finditer(r'href="(/[^"#?]*)', s):
                u = m.group(1)
                if u.startswith("/assets/") or u.endswith((".png", ".svg", ".ico", ".xml", ".webmanifest", ".txt")):
                    continue
                t = os.path.join(OUT, u.lstrip("/"), "index.html") if u.endswith("/") else os.path.join(OUT, u.lstrip("/"))
                if not os.path.exists(t):
                    bad.append("링크 " + u + " in " + f)
            for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    bad.append("JSON-LD " + f + " " + str(e))
    return sorted(set(bad))


if __name__ == "__main__":
    build_home()
    build_pricing()
    build_faq()
    build_redirects()
    build_landing()
    build_guides()
    build_tech()
    build_static()
    build_board()
    build_seo()
    problems = verify()
    print("pages", len(PAGES), "problems", len(problems))
    for p in problems[:40]:
        print(" -", p)
