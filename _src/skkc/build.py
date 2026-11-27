# -*- coding: utf-8 -*-
"""성균관컨설팅(skkc.co.kr) 카피클린 두 쪽 새 디자인 코드 만들기
  python3 build.py
  -> dist/ai-detector_widget.html (아임웹 코드 위젯 w20260708a3f8e71b2ea81 에 넣을 전체 코드: 새 첫 화면 + 예전 차별점 그대로)
  -> dist/ai-humanizer_widget.html (아임웹 /ai-humanizer 새 코드 위젯 전체 코드)
  -> dist/preview_*.html (로컬 확인용, 아임웹 머리글 흉내 + 로컬 글꼴)
CSS 는 src/*.css 에 보통으로 쓰고, 아임웹 기본 CSS 에 지지 않게 모든 선언에 !important 를 붙임(@keyframes 안은 빼고)."""
import os
import json
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
DIST = os.path.join(HERE, "dist")
os.makedirs(DIST, exist_ok=True)
FONT_LINK = '<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" rel="stylesheet">'
LOCAL_FONT = "file:///home/claude/ccwork/node_modules/pretendard/dist/web/variable/woff2/PretendardVariable.woff2"


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def split_decls(body):
    out, cur, depth, q = [], "", 0, None
    for ch in body:
        if q:
            cur += ch
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == ";" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def importantize(css):
    """선언마다 !important. @media 안쪽도, @keyframes 안쪽은 그대로"""
    css = strip_comments(css)
    res, i, n = [], 0, len(css)
    stack = []   # 'kf' | 'at' | 'rule'
    buf = ""
    while i < n:
        ch = css[i]
        if ch == "{":
            sel = buf.strip()
            if sel.startswith("@keyframes") or sel.startswith("@-webkit-keyframes"):
                stack.append("kf")
            elif sel.startswith("@"):
                stack.append("at")
            else:
                stack.append("rule")
            res.append(buf + "{")
            buf = ""
        elif ch == "}":
            kind = stack.pop() if stack else "rule"
            in_kf = "kf" in stack or kind == "kf"
            if kind == "rule" and not in_kf:
                decls = []
                for d in split_decls(buf):
                    d = d.strip()
                    if not d:
                        continue
                    if "!important" not in d and ":" in d:
                        d = d + " !important"
                    decls.append(d)
                res.append(" " + "; ".join(decls) + (" " if decls else "") + "}")
            else:
                res.append(buf + "}")
            buf = ""
        else:
            buf += ch
        i += 1
    res.append(buf)
    out = "".join(res)
    out = re.sub(r"\n\s*\n+", "\n", out)
    return out.strip()


DET_ONLY = ("ccd-offer", "ccd-gauge", "ccd-scale", "ccd-mini", "ccd-lines", "ccd-verdict", "ccd-card__top", "ccd-judge")


def drop_rules(css, names):
    """선택자 전부가 names 가운데 하나를 품은 규칙은 뺌(빈 @media 도 뺌)"""
    out, i, n = [], 0, len(css)
    def block_end(j):
        d = 0
        while j < n:
            if css[j] == "{":
                d += 1
            elif css[j] == "}":
                d -= 1
                if d == 0:
                    return j
            j += 1
        return n - 1
    while i < n:
        j = css.find("{", i)
        if j < 0:
            out.append(css[i:])
            break
        sel = css[i:j]
        k = block_end(j)
        body = css[j + 1:k]
        s2 = sel.strip()
        if s2.startswith("@media"):
            inner = drop_rules(body, names)
            if inner.strip():
                out.append(sel + "{" + inner + "}")
        elif s2.startswith("@"):
            out.append(css[i:k + 1])
        else:
            parts = [x.strip() for x in s2.split(",")]
            if not all(any(nm in x for nm in names) for x in parts):
                out.append(css[i:k + 1])
        i = k + 1
    return "".join(out)


def minify(css):
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};])\s*", r"\1", css)
    css = css.replace(";}", "}")
    return css.strip()


def compact_html(h):
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = re.sub(r">\s+<", "><", h)
    return h.strip()


def old_detector_parts():
    """예전 코드에서 차별점(.ccx .cc-diff …)에 쓰이는 CSS · HTML 만 그대로 남김"""
    s = open(os.path.join(HERE, "backup", "ai-detector_w20260708a3f8e71b2ea81_before_20261126.html"), encoding="utf-8").read()
    css = s[s.index("<style>") + 7:s.index("</style>")]
    keep = []
    # 리셋 · 뿌리 · 링크 · svg
    a = css.index("/* 네임스페이스 리셋 */")
    b = css.index("/* ═══════════ 1. HERO")
    keep.append(css[a:b])
    c = css.index("/* ═══════════ 2. 차별점")
    d = css.index("/* ═══════════ 반응형")
    keep.append(css[c:d])
    keep.append("@media (max-width: 1100px) {\n  .ccx .cc-diff__grid { grid-template-columns: repeat(2, 1fr) !important; }\n}\n"
                "@media (max-width: 768px) {\n  .ccx .cc-diff { padding: 56px 18px 72px !important; }\n  .ccx .cc-diff__title { font-size: 26px !important; margin-bottom: 32px !important; }\n  .ccx .cc-diff__grid { grid-template-columns: 1fr !important; }\n}\n")
    html = s[s.index('<section class="cc-diff">'):s.rindex("</section>") + len("</section>")]
    # 2026.11.26 사용자 요청: 'AI 의심' 대신 'AI 패턴'
    html = html.replace("직관적인 리포트로 AI 사용 의심<br>현황을 쉽게 확인", "직관적인 리포트로 AI 패턴<br>현황을 쉽게 확인")
    return "".join(keep), '<div class="ccx">' + html + "</div>"


def page_preview(title, widget_code, after=""):
    code = widget_code.replace(FONT_LINK, "")
    return ("<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>%s</title>"
            "<style>@font-face{font-family:'Pretendard Variable';font-weight:45 920;src:url('%s') format('woff2-variations');}"
            "body{margin:0;font-family:'Malgun Gothic',sans-serif;color:#363636;background:#fff}"
            ".imw-hd{position:sticky;top:0;z-index:50;height:108px;background:#fff;border-bottom:1px solid #eee;display:flex;align-items:center;justify-content:space-between;padding:0 260px 0 265px;font:600 16px 'Pretendard Variable',sans-serif}"
            ".imw-hd b{font-size:26px;color:#1d3b8b}.imw-hd nav{display:flex;gap:38px}.imw-hd i{font-style:normal;background:#1a5cf5;color:#fff;padding:12px 20px;border-radius:99px;font-size:14px}"
            "h1,h2,h3,p{margin:0 0 10px}a{color:#363636}ul{padding-left:30px}"
            "@media(max-width:900px){.imw-hd{padding:0 18px;height:64px}.imw-hd nav{display:none}}</style></head><body>"
            "<div class='imw-hd'><b>성균관컨설팅</b><nav><span>산학연 연구소</span><span>컨설팅 분야</span><span>컨설팅 의뢰</span><span>카피 클린</span><span>커뮤니티</span></nav><i>마이페이지</i></div>"
            "<div class='widget-code'>%s</div>%s</body></html>") % (title, LOCAL_FONT, code, after)


def build_detector():
    new_css = minify(importantize(open(os.path.join(SRC, "detector.css"), encoding="utf-8").read()))
    hero = compact_html(open(os.path.join(SRC, "detector_hero.html"), encoding="utf-8").read())
    old_css, old_html = old_detector_parts()
    old_css = strip_comments(old_css).strip()
    code = "%s\n<style>\n%s\n%s\n</style>\n%s\n%s" % (FONT_LINK, new_css, old_css, hero, compact_html(old_html))
    open(os.path.join(DIST, "ai-detector_widget.html"), "w", encoding="utf-8").write(code)
    after = ("<div style='background:#fff;padding:60px 0;text-align:center;font:700 30px Pretendard Variable'>실제 분석 결과 기반 정밀 진단(예전 쪽 그대로)</div>")
    open(os.path.join(DIST, "preview_detector.html"), "w", encoding="utf-8").write(page_preview("ai-detector preview", code, after))
    return len(code)


# /ai-humanizer 아래 칸 바탕(.cch) 가운데 /ai-detector 아래 칸에서 쓰지 않는 것(첫 화면 .ccd, 그 쪽에만 있는 위젯 숨김 · 머리글 틈 · 카피체크 줄 등)
CCH_UNUSED = (".ccd", "#inline_header", "#w2026", ".cch-rel", ".cch-case", ".cch-compare", ".cch-cmp", ".cch-bar", ".cch-proof",
              ".cch-why", ".cch-stats", ".cch-stat", ".cch-src", ".cch-est__card", ".cch-est__lead", ".cch-crit", ".cch-notice",
              ".cch-promise", ".cch-pr", ".cch-faq", ".cch-qa", ".cch-more", ".cch-quote--ans", ".cch-final__sub")


def build_detector_more():
    """2026.11.27 /ai-detector 아래 그림 9장 대신 글자로 만든 칸(새 코드 위젯, 섹션 s202607082cb706dd1f142 맨 아래)"""
    hcss = open(os.path.join(SRC, "humanizer.css"), encoding="utf-8").read()
    base = hcss[hcss.index("/* ── 아래 칸(.cch) ── */"):]
    base = drop_rules(importantize(base), CCH_UNUSED)
    more = importantize(open(os.path.join(SRC, "detector_more.css"), encoding="utf-8").read())
    css = minify(base + "\n" + more)
    html = compact_html(open(os.path.join(SRC, "detector_more.html"), encoding="utf-8").read())
    code = "%s\n<style>\n%s\n</style>\n%s" % (FONT_LINK, css, html)
    open(os.path.join(DIST, "ai-detector_more_widget.html"), "w", encoding="utf-8").write(code)
    # 로컬 확인용: 첫 화면 + (가운데 예전 칸 자리) + 새 아래 칸 + (자주 묻는 질문 자리)
    hero = open(os.path.join(DIST, "ai-detector_widget.html"), encoding="utf-8").read().replace(FONT_LINK, "")
    mid = ("<div style='background:#f7f9fc;padding:70px 0;text-align:center;font:700 26px Pretendard Variable;color:#94a3b8'>"
           "(가운데 예전 칸 세 개: 실제 분석 결과 기반 정밀 진단 · 제출 전 점검 · 4단계 프로세스, 그대로)</div>")
    faq = ("<div style='background:#fff;padding:70px 0;text-align:center;font:700 26px Pretendard Variable;color:#94a3b8'>(자주 묻는 질문, 그대로)</div>")
    open(os.path.join(DIST, "preview_detector_full.html"), "w", encoding="utf-8").write(
        page_preview("ai-detector full preview", hero, mid + "<div class='widget-code'>" + code.replace(FONT_LINK, "") + "</div>" + faq))
    return len(code)


# /copyclean-inquiry 첫 칸에서 쓰지 않는 바탕 규칙(.cch) 더하기
INQ_UNUSED = CCH_UNUSED + (".cch-who", ".cch-quotes", ".cch-quote", ".cch-docs", ".cch-doclist", ".cch-doc", ".cch-band", ".cch-est",
                           ".cch-checks", ".cch-how", ".cch-flow", ".cch-final", ".cch-fn", ".cch-glow", ".cch-center")


def build_inquiry():
    """2026.11.27 /copyclean-inquiry 첫 칸(코드 위젯 w20260708800e3d6a4bfc5) + 아래 입력폼 모양"""
    hcss = open(os.path.join(SRC, "humanizer.css"), encoding="utf-8").read()
    base = hcss[hcss.index("/* ── 아래 칸(.cch) ── */"):]
    base = drop_rules(importantize(base), INQ_UNUSED)
    own = importantize(open(os.path.join(SRC, "inquiry.css"), encoding="utf-8").read())
    css = minify(base + "\n" + own)
    html = compact_html(open(os.path.join(SRC, "inquiry.html"), encoding="utf-8").read())
    code = "%s\n<style>\n%s\n</style>\n%s" % (FONT_LINK, css, html)
    open(os.path.join(DIST, "copyclean-inquiry_widget.html"), "w", encoding="utf-8").write(code)
    return len(code)


def build_pricing():
    """2026.11.27 /copyclean-pricing 코드 위젯(w20260708b6614391e575a): 예전 코드 그대로 + 'AI유사도 개선' 카드 단추 아래 길잡이 + 금액 고르기 칸(.ccp)"""
    old = open(os.path.join(HERE, "backup", "copyclean-pricing_w20260708b6614391e575a_before_20261127.html"), encoding="utf-8").read()
    css = minify(importantize(open(os.path.join(SRC, "pricing_pay.css"), encoding="utf-8").read()))
    block = compact_html(open(os.path.join(SRC, "pricing_pay.html"), encoding="utf-8").read())
    btn = '      개선 요청하기\n    </a>'
    assert old.count(btn) == 1
    code = old.replace(btn, btn + '\n    <a href="#ccpPay" class="ccp-jump">상담 후 안내받은 금액 결제하기 ↓</a>', 1)
    mark = '<!-- ===== 상세내역서 구성 ===== -->'
    assert code.count(mark) == 1
    code = code.replace(mark, "%s\n<style>\n%s\n</style>\n%s\n\n  %s" % (FONT_LINK, css, block, mark), 1)
    open(os.path.join(DIST, "copyclean-pricing_widget.html"), "w", encoding="utf-8").write(code)
    open(os.path.join(DIST, "preview_pricing.html"), "w", encoding="utf-8").write(page_preview("pricing preview", code))
    return len(code)


def build_academic():
    """2026.11.27 /academic-info 학술정보 게시판 글 보기 · 목록 모양(코드 위젯 하나: 스타일 + 예전 글 정리 스크립트). 저장된 글은 그대로."""
    css = minify(importantize(open(os.path.join(SRC, "academic.css"), encoding="utf-8").read()))
    js = open(os.path.join(SRC, "academic.js"), encoding="utf-8").read()
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    js = "\n".join(l.strip() for l in js.split("\n") if l.strip())
    assert "//" not in js, "아임웹이 주석으로 볼 수 있는 // 이 스크립트에 있음"
    code = "%s\n<style>\n%s\n</style>\n<script>\n%s\n</script>" % (FONT_LINK, css, js)
    open(os.path.join(DIST, "academic-info_widget.html"), "w", encoding="utf-8").write(code)
    open(os.path.join(DIST, "academic-info_test.js"), "w", encoding="utf-8").write(
        "(function(){var s=document.getElementById('acTestStyle')||document.createElement('style');s.id='acTestStyle';s.textContent=%s;document.head.appendChild(s);})();\n%s" % (json.dumps(css, ensure_ascii=False), js))
    return len(code)


# ── 2026.11.27 성균관컨설팅 소개 페이지 7곳 새 디자인(.skp) ──
SKP_ICONS = {
    "arrow": '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    "down": '<path d="M12 5v14"/><path d="m6 13 6 6 6-6"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "info": '<circle cx="12" cy="12" r="9.5"/><path d="M12 16v-4.5"/><path d="M12 8h.01"/>',
    "alert": '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "badge": '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76z"/><path d="m9 12 2 2 4-4"/>',
    "aioff": '<rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 7V4"/><circle cx="12" cy="3" r="1"/><path d="M9 12h.01"/><path d="M15 12h.01"/><path d="M9.5 15.5h5"/><path d="M2 2l20 20"/>',
    "cap": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/><path d="M22 10v6"/>',
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "usercheck": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
    "manager": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/><path d="m10 14 2 3 2-3"/>',
    "network": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="18" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M12 7.5v4"/><path d="m12 11.5-5.2 4.6"/><path d="m12 11.5 5.2 4.6"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><path d="M12 15v2"/>',
    "flask": '<path d="M9 3h6"/><path d="M10 3v6.5L4.6 18.6A2 2 0 0 0 6.3 21.6h11.4a2 2 0 0 0 1.7-3L14 9.5V3"/><path d="M7.5 15h9"/>',
    "building": '<rect x="4" y="2.5" width="16" height="19" rx="2"/><path d="M9 21.5v-4h6v4"/><path d="M8.5 7h.01"/><path d="M12 7h.01"/><path d="M15.5 7h.01"/><path d="M8.5 11h.01"/><path d="M12 11h.01"/><path d="M15.5 11h.01"/><path d="M8.5 15h.01"/><path d="M15.5 15h.01"/>',
    "landmark": '<path d="M3 21h18"/><path d="M5 18v-7"/><path d="M9.5 18v-7"/><path d="M14.5 18v-7"/><path d="M19 18v-7"/><path d="M12 3 3.5 8h17z"/>',
    "route": '<circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H17a3.5 3.5 0 0 0 0-7H7a3.5 3.5 0 0 1 0-7h8.5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/><path d="M10 9H8"/>',
    "list": '<path d="M9 6h11"/><path d="M9 12h11"/><path d="M9 18h11"/><path d="m3 6 1 1 2-2"/><path d="m3 12 1 1 2-2"/><path d="m3 18 1 1 2-2"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/><path d="m16 16-1.9-1.9"/>',
    "target": '<circle cx="12" cy="12" r="9.5"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="1.5"/>',
    "briefcase": '<rect x="2.5" y="7" width="19" height="13.5" rx="2"/><path d="M16 20.5V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v15.5"/>',
    "layers": '<path d="m12 2.5 9.5 4.8-9.5 4.8-9.5-4.8z"/><path d="m2.5 12 9.5 4.8 9.5-4.8"/><path d="m2.5 16.7 9.5 4.8 9.5-4.8"/>',
    "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "cpu": '<rect x="4.5" y="4.5" width="15" height="15" rx="2"/><rect x="9" y="9" width="6" height="6" rx="1"/><path d="M9 2v2.5"/><path d="M15 2v2.5"/><path d="M9 19.5V22"/><path d="M15 19.5V22"/><path d="M2 9h2.5"/><path d="M2 15h2.5"/><path d="M19.5 9H22"/><path d="M19.5 15H22"/>',
    "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/><path d="M3.5 12h3.5l1.5-3 3 6 1.5-3h3.5"/>',
    "palette": '<circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/><circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.9 0 1.7-.8 1.7-1.7 0-.4-.2-.8-.4-1.1-.3-.3-.4-.7-.4-1.1a1.6 1.6 0 0 1 1.6-1.7h2c3.1 0 5.6-2.5 5.6-5.6C22 6 17.5 2 12 2z"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.9-3.9a3 3 0 0 0-4.2 0l-.9.9a1 1 0 1 1-3-3l2.8-2.8a5.8 5.8 0 0 1 7.1-.9l.5.3a2 2 0 0 0 1.4.3L21 4"/><path d="m21 3 1 11h-2"/><path d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path d="M3 4h8"/>',
    "ban": '<circle cx="12" cy="12" r="9.5"/><path d="m5.3 5.3 13.4 13.4"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="M4 7h16"/><path d="m4 7-2.5 6a3 3 0 0 0 5 0z"/><path d="m20 7-2.5 6a3 3 0 0 0 5 0z"/>',
    "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4"/><path d="M12 16h4"/><path d="M8 11h.01"/><path d="M8 16h.01"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "puzzle": '<path d="M15.4 2.6a2.2 2.2 0 0 0-3.1 0L10 4.9a2 2 0 0 1-2.8 0 1.9 1.9 0 0 0-2.7 2.7 2 2 0 0 1 0 2.8l-2.3 2.3a2.2 2.2 0 0 0 0 3.1l1.6 1.6c.5.5 1.2.5 1.6 0a2.4 2.4 0 1 1 3.4 3.4c-.5.5-.5 1.2 0 1.6l1.6 1.6a2.2 2.2 0 0 0 3.1 0l2.3-2.3a2 2 0 0 1 2.8 0 1.9 1.9 0 0 0 2.7-2.7 2 2 0 0 1 0-2.8l2.3-2.3a2.2 2.2 0 0 0 0-3.1z"/>',
    "star": '<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-.9z"/>',
    "starf": '<path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5-4.8-4.6 6.6-.9z"/>',
    "sparkle": '<path d="M12 3 10.1 8.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4L21 8"/><path d="M21 3v5h-5"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
    "quote": '<path d="M7 7h4v5c0 3-1.5 5-4 6"/><path d="M15 7h4v5c0 3-1.5 5-4 6"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}

SKP_PAGES = {
    "researchers": {"first": "s2026070819b61feb68722", "first_w": ["w20260708ca4f0043e3107", "w20260708f4d32e90d2468", "w202607087bbf6a47b1f56"],
                    "hide_s": ["s202607087e57ed0eed9c3", "s20260708bad59358abc39", "s202607088385a9813368e"]},
    "degree-thesis": {"first": "s202607083b0dbae25f133", "first_w": ["w20260708efd61b803918f", "w202607082ebfe82a8ceed", "w202607086c82891adafde"],
                      "hide_s": ["s20260708fa3d43741f542", "s202607084d70224dd28fc"]},
    "ai-ethics": {"first": "s20260818c29a26fc77c9b", "first_w": ["w2026081813261b3d30bb8", "w202608187a110627e5119", "w202608183a72e94dffb9a"],
                  "hide_s": ["s20260814f59dc7c5538ce", "s202608144eab46cd01117"]},
    "thesis-writing": {"first": "s20260708baa0d98ffec2a", "first_w": ["w20260708a5e50a5b7e38b", "w202607086c048d01a5437", "w2026070895fd7813ec71c"],
                       "hide_s": ["s20260708c0a53c2ae5376"]},
    "ai-similarity": {"first": "s2026070809d37e8cfc690", "first_w": ["w20260708d683f7b6fed01", "w20260708d4791da4cc260", "w20260708c0478e9877c50"],
                      "hide_s": ["s20260708c246e5bc3f3d3"]},
    "rnd-consulting": {"first": "s2026070854bf5bd61fafc", "first_w": ["w20260708dcf3206a6e160", "w20260708198c41d9c804a", "w202607083a6913e46963d"],
                       "hide_s": ["s20260708dfc1adf52dd17"]},
    "reviews": {"first": "s20260708e6feeafa329f2", "first_w": ["w2026070832172f8bcf689", "w202607084e558c1212915", "w2026070890ee26f19e70b"],
                "hide_s": ["s20260708e9085b48fecef"]},
}


def skp_icons(html):
    def rep(m):
        name = m.group(1)
        assert name in SKP_ICONS, name
        return '<svg class="skp-ico" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % SKP_ICONS[name]
    return re.sub(r"\{\{i:([a-z0-9-]+)\}\}", rep, html)


def skp_host_css(cfg):
    f = cfg["first"]
    out = ["/* 이 페이지 예전 칸: 지우지 않고 숨김. 첫 칸은 새 코드 위젯을 담는 자리로만 씀 */",
           "#%s { padding: 0; background: transparent; min-height: 0; }" % f,
           "#%s > .section_bg, #%s > .section_bg_color { display: none; }" % (f, f),
           "%s { display: none; }" % ", ".join("#" + w for w in cfg["first_w"])]
    if cfg.get("hide_s"):
        out.append("%s { display: none; }" % ", ".join("#" + s for s in cfg["hide_s"]))
    return "\n".join(out) + "\n"


def skp_js(text):
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = "\n".join(l.strip() for l in text.split("\n") if l.strip())
    assert "//" not in text, "아임웹이 주석으로 볼 수 있는 // 이 스크립트에 있음"
    return text


def build_skp():
    d = os.path.join(SRC, "skp")
    base = open(os.path.join(d, "base.css"), encoding="utf-8").read() + "\n" + open(os.path.join(d, "parts.css"), encoding="utf-8").read()
    bjs = open(os.path.join(d, "base.js"), encoding="utf-8").read()
    sizes = {}
    for page, cfg in SKP_PAGES.items():
        css = base + "\n" + skp_host_css(cfg)
        pc = os.path.join(d, page + ".css")
        if os.path.exists(pc):
            css += "\n" + open(pc, encoding="utf-8").read()
        css = minify(importantize(css))
        html = compact_html(skp_icons(open(os.path.join(d, page + ".html"), encoding="utf-8").read()))
        js = bjs
        pj = os.path.join(d, page + ".js")
        if os.path.exists(pj):
            js += "\n" + open(pj, encoding="utf-8").read()
        js = skp_js(js)
        code = "%s\n<style>\n%s\n</style>\n%s\n<script>\n%s\n</script>" % (FONT_LINK, css, html, js)
        open(os.path.join(DIST, "skp_%s_widget.html" % page), "w", encoding="utf-8").write(code)
        open(os.path.join(DIST, "preview_skp_%s.html" % page), "w", encoding="utf-8").write(page_preview("%s preview" % page, code))
        sizes[page] = len(code)
    return sizes


def build_humanizer():
    p = os.path.join(SRC, "humanizer.css")
    if not os.path.exists(p):
        return 0
    base = open(os.path.join(SRC, "detector.css"), encoding="utf-8").read()
    base = base[:base.index("/* 2026.11.26 아래 차별점 칸")]  # 첫 화면 판(.ccd)만 함께 씀
    css = minify(drop_rules(importantize(base + "\n" + open(p, encoding="utf-8").read()), DET_ONLY))
    html = compact_html(open(os.path.join(SRC, "humanizer.html"), encoding="utf-8").read())
    code = "%s\n<style>\n%s\n</style>\n%s" % (FONT_LINK, css, html)
    open(os.path.join(DIST, "ai-humanizer_widget.html"), "w", encoding="utf-8").write(code)
    open(os.path.join(DIST, "preview_humanizer.html"), "w", encoding="utf-8").write(page_preview("ai-humanizer preview", code))
    return len(code)


if __name__ == "__main__":
    print("detector", build_detector(), "detector_more", build_detector_more(), "inquiry", build_inquiry(), "pricing", build_pricing(), "academic", build_academic(), "humanizer", build_humanizer())
    print("skp", build_skp())
