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


def prune_unused(css, used, js_text=""):
    """2026.11.28 카피클린 새 판: 쪽에 없는 class 만 쓰는 선택자를 뺌(위젯 크기 줄이기).
    선택자 안 class 가 모두 쪽 HTML 에 있거나 · 스크립트 글에 나오거나 · is- 로 시작하면 남김. :not() · :is() · :where() · :has() 안은 따지지 않음"""
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
    def ok(sel):
        s = re.sub(r":(?:not|is|where|has)\([^()]*\)", "", sel)
        for c in re.findall(r"\.([A-Za-z_][\w-]*)", s):
            if c in used or c.startswith("is-") or ("'" + c in js_text or " " + c in js_text or '"' + c in js_text):
                continue
            return False
        return True
    while i < n:
        j = css.find("{", i)
        if j < 0:
            out.append(css[i:])
            break
        sel = css[i:j]
        k = block_end(j)
        body = css[j + 1:k]
        s2 = sel.strip()
        if s2.startswith("@media") or s2.startswith("@supports"):
            inner = prune_unused(body, used, js_text)
            if inner.strip():
                out.append(sel + "{" + inner + "}")
        elif s2.startswith("@"):
            out.append(css[i:k + 1])
        else:
            parts = [x.strip() for x in s2.split(",")]
            keep = [x for x in parts if ok(x)]
            if keep:
                out.append(",".join(keep) + "{" + body + "}")
        i = k + 1
    return "".join(out)


def html_classes(h):
    used = set()
    for m in re.findall(r'class="([^"]*)"', h):
        used.update(m.split())
    return used


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
    code = old.replace(btn, btn + '\n    <a href="#ccpPay" class="ccp-jump">상담 후 안내받은 크레딧 결제하기 ↓</a>', 1)
    mark = '<!-- ===== 상세내역서 구성 ===== -->'
    assert code.count(mark) == 1
    code = code.replace(mark, "%s\n<style>\n%s\n</style>\n%s\n\n  %s" % (FONT_LINK, css, block, mark), 1)
    open(os.path.join(DIST, "copyclean-pricing_widget.html"), "w", encoding="utf-8").write(code)
    open(os.path.join(DIST, "preview_pricing.html"), "w", encoding="utf-8").write(page_preview("pricing preview", code))
    return len(code)



def build_hero():
    """2026.11.28 11:36 /pricing · /copyclean-pricing 새 첫 화면(코드 위젯). 예전 텍스트 위젯은 CSS 로 숨김(지우지 않음)"""
    css = open(os.path.join(SRC, "hero", "hero.css"), encoding="utf-8").read()
    out = {}
    for name, old_id in (("pricing", "w20260708447dc6617897e"), ("copyclean", "w202607089821035f1b604")):
        html = compact_html(open(os.path.join(SRC, "hero", name + ".html"), encoding="utf-8").read())
        hide = "\n#" + old_id + " { display: none; }\n"
        snippet = "<style>" + minify(importantize(css + hide)) + "</style>\n" + html + "\n"
        open(os.path.join(DIST, "hero_" + name + "_widget.html"), "w", encoding="utf-8", newline="").write(snippet)
        out[name] = len(snippet)
    return out

def build_pricing_tc():
    """2026.11.28 /pricing 코드 위젯(w202607083d4e39e7b756e) '의뢰자 후기' 바로 앞에 끼워 넣는 '바로 결제' 금액 칸(표시 줄 사이만 지우면 원래 위젯)"""
    html = open(os.path.join(SRC, "pricing_tc.html"), encoding="utf-8").read().strip()
    css = open(os.path.join(SRC, "pricing_tc.css"), encoding="utf-8").read()
    js = re.sub(r"/\*.*?\*/", "", open(os.path.join(SRC, "pricing_tc.js"), encoding="utf-8").read(), flags=re.S).strip()
    assert "//" not in js
    snippet = ("<!-- 2026.11.28 바로 결제 금액 칸 시작(지우면 원래 위젯, 원래 SHA-256 앞 16자 e672a3d450b6c31e) -->\r\n"
               "<style>" + minify(importantize(css)) + "</style>\r\n" + html + "\r\n" + ("<script>" + js + "</script>\r\n" if js else "") +
               "<!-- 2026.11.28 바로 결제 금액 칸 끝 -->\r\n\r\n  ")
    open(os.path.join(DIST, "pricing_tc_snippet.html"), "w", encoding="utf-8", newline="").write(snippet)
    return len(snippet)


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
    # 2026.11.27 22:45 '여기도 좀 잘 바꿔봐'. 둘째 칸(s2026070870b8543218885)은 지우지 않고 thesis-consulting.css 에서 폼 · 자주 묻는 질문만 남겨 모양을 바꿈
    "thesis-consulting": {"first": "s20260708a3c65e18cbed6", "first_w": ["w2026070830cf2f3f95856", "w202607086a8723a2ab49e", "w2026070864246139d0abc"],
                          "hide_s": []},
    # 2026.11.28 08:49 '여기도 개선'. 둘째 칸은 지우지 않고 예전 글 · 여백 위젯만 숨김, 쪽 CSS 코드 위젯 두 개는 그대로, 상담 신청 폼은 모양만(consult_form.css)
    "gov-rnd": {"first": "s20260708b570b07a8b534", "first_w": ["w202607080dd5b7573d901", "w20260708630992ef50338", "w202607081bbec5dfdef5c"],
                "hide_s": [], "extra": ["consult"],
                "sec2": {"id": "s20260708a17ff96bf1fde", "form": "w202607083ca2b609b5032",
                         "hide_w": ["w202607085e289b551bacc", "w202607086e15707e2a42a", "w20260708b6facb4556487", "w202607084f0813f75e38c",
                                    "w20260708b9212987e64c7", "w202607087dca341b2daff", "w202607081dab6d09535b6"]}},
    "industry-cooperation": {"first": "s2026070852a296be74d6e", "first_w": ["w202607082bad1e2ca90a4", "w20260708bdfaeb9587159", "w202607085a01229af5684"],
                             "hide_s": [], "extra": ["consult"],
                             "sec2": {"id": "s20260708ca695d0dfc5be", "form": "w20260708cc269b2b182d6",
                                      "hide_w": ["w202607084b824e852afb6", "w20260708d5ee1e689b087", "w20260708a95bbfbcc7556", "w20260708463afa4f94d74",
                                                 "w20260708bec2e94a8b964", "w202607089823e6019838f", "w20260708536b8c6361ac9"]}},
}


def skp_sec2_css(sec):
    """둘째 아임웹 칸: 예전 위젯 숨김 + 상담 신청 폼 모양(consult_form.css 의 #SEC2 · #FORM 을 실제 ID 로)"""
    css = open(os.path.join(SRC, "skp", "consult_form.css"), encoding="utf-8").read()
    css = css.replace("#SEC2", "#" + sec["id"]).replace("#FORM", "#" + sec["form"])
    return css + "%s { display: none; }\n" % ", ".join("#" + w for w in sec["hide_w"])


def skp_faq_ld(html):
    """쪽 안의 자주 묻는 질문(details.skp-faq__q)을 그대로 FAQPage 구조화 데이터로. 화면 글과 같게 유지"""
    import html as _h
    items = []
    for m in re.finditer(r'<details class="skp-faq__q"[^>]*>\s*<summary><span>Q</span>(.*?)</summary>\s*<div class="skp-faq__a">(.*?)</div>\s*</details>', html, re.S):
        q = _h.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
        a = _h.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(2)))).strip()
        items.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    assert items, "자주 묻는 질문이 없음"
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}
    return '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False, separators=(",", ":"))


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
        for ex in cfg.get("extra", []):
            css += "\n" + open(os.path.join(d, ex + ".css"), encoding="utf-8").read()
        if cfg.get("sec2"):
            css += "\n" + skp_sec2_css(cfg["sec2"])
        pc = os.path.join(d, page + ".css")
        if os.path.exists(pc):
            css += "\n" + open(pc, encoding="utf-8").read()
        css = minify(importantize(css))
        raw = open(os.path.join(d, page + ".html"), encoding="utf-8").read()
        if "{{faqld}}" in raw:
            raw = raw.replace("{{faqld}}", skp_faq_ld(raw))
        html = compact_html(skp_icons(raw))
        js = bjs
        for ex in cfg.get("extra", []):
            pe = os.path.join(d, ex + ".js")
            if os.path.exists(pe):
                js += "\n" + open(pe, encoding="utf-8").read()
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


# ── 2026.11.28 카피클린 무료 검사(AIMarker 엔진) 데모 두 쪽 ──
# 대표: '아직 배포해서 적용시키지는 말고 데모로 내가 먼저 테스트 · 지금의 사이트 상태는 유지한 채 개선된 버전의 사이트 2개 페이지를 만들어서 보여줘'
# 데모는 copycheck.skkc.co.kr/demo/skkc/ (검색 제외). 카피체크 주소는 서버가 이미 허용하는 곳이라 서버를 바꾸지 않고 실제 엔진으로 검사됨
KC_DEMO_API = "https://script.google.com/macros/s/AKfycbz3qUbNNd_21wHvi6EGHAz1_lrRJ7LAzzIYlIeg4U0bm8m-ioqHLPJV1UzatPmpOfkOFg/exec"
KC_CHAT_KEY = "c35b386f-d5db-4309-9a8b-18dd319b323d"   # skkc.co.kr 쪽에 이미 공개돼 있는 채널톡 플러그인 키
KC_FAQ = [
    ("무료 검사는 정말 무료인가요?", "네. 회원가입이나 결제 정보 없이 바로 검사해요. 결과에서 AI 작성률 · 판정 · AI 패턴 문장 수를 확인할 수 있어요."),
    ("올린 글이나 파일이 저장되나요?", "파일은 이 브라우저 안에서 글만 꺼내고, 검사할 글만 서버로 보내요. 검사에 쓴 글은 저장하지 않아요."),
    ("블라인드된 문장은 어떻게 확인하나요?", "어떤 문장을 어떻게 고칠지는 전문가 상담에서 개선 범위와 함께 안내해 드려요. 문장별 위치가 모두 담긴 상세 내역서(PDF)가 필요하면 상세 결과서(5,500원)로 받을 수 있어요."),
    ("카피킬러 · GPT킬러 같은 다른 검사기와 결과가 같나요?", "검사기마다 학습한 자료와 기준이 달라 수치가 다를 수 있어요. 카피클린 무료 검사는 놓치는 AI 글을 줄이도록 엄격한 기준으로 재므로, 제출처가 쓰는 검사기 기준으로도 함께 확인하는 것이 좋아요."),
    ("AI 작성률이 높게 나오면 어떻게 하나요?", "결과 아래 '무료 견적 받기'를 누르면 검사 결과가 채널톡 상담 창에 함께 들어가요. 분량 · 마감 · 목표를 보고 크레딧으로 견적을 안내해 드리고, 확인하신 뒤에 진행해요."),
    ("개선 비용은 어떻게 정해지나요?", "문서 분량, AI 작성률이 높게 나온 구간, 희망 마감일에 따라 달라져요. 상담에서 크레딧(1 크레딧 = 1만 원)으로 안내하고, 같은 크레딧을 바로 결제 쪽에서 결제해요."),
    ("결제는 안전한가요?", "에스크로 안전결제로, 결과물을 받기 전까지 결제금은 전문가가 아닌 성균관컨설팅이 안전하게 보관해요. 모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달돼요."),
    ("AI로 작성된 문서도 개선이 가능한가요?", "가능합니다. 생성형 언어모델 특유의 문장 구조와 표현 패턴을 분석한 뒤, 의미와 논리는 그대로 유지하면서 AI 사용 흔적이 드러나기 쉬운 구조를 자연스러운 문장 흐름으로 개선합니다."),
    ("AI 사용 규정이 있는 과제에도 맡겨도 되나요?", "카피클린은 이미 쓴 글의 표현을 다듬는 서비스이며 대필이나 AI 자동 생성은 하지 않아요. 제출처(학교 · 기관)의 생성형 AI 사용 규정을 먼저 확인해 주세요. 결과 수치는 문서와 검사 도구에 따라 달라 특정 수치를 보장하지 않아요."),
    ("의뢰 문서는 어떻게 관리되나요?", "모든 자료는 컨설팅 목적에 한해 제한적으로 접근되며, 작업 완료 후에는 내부 보안 규정에 따라 즉시 폐기됩니다."),
]
KC_CHAT_BOOT = ("(function(){var w=window;if(w.ChannelIO){return;}var ch=function(){ch.c(arguments);};ch.q=[];ch.c=function(args){ch.q.push(args);};w.ChannelIO=ch;"
                "function l(){if(w.ChannelIOInitialized){return;}w.ChannelIOInitialized=true;var s=document.createElement('script');s.type='text/javascript';s.async=true;"
                "s.src='https://cdn.channel.io/plugin/ch-plugin-web.js';var x=document.getElementsByTagName('script')[0];if(x.parentNode){x.parentNode.insertBefore(s,x);}}"
                "if(document.readyState==='complete'){l();}else{w.addEventListener('DOMContentLoaded',l);w.addEventListener('load',l);}})();"
                "ChannelIO('boot',{\"pluginKey\":\"%s\",\"language\":\"ko\"});") % KC_CHAT_KEY


def _kc_esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_kc_demo():
    """2026.11.28 데모 두 쪽: docs/demo/skkc/ai-detector/ · ai-humanizer/ + kc-check.js (실제 사이트 · 서버는 그대로)"""
    import hashlib
    rd = lambda *p: open(os.path.join(SRC, *p), encoding="utf-8").read()
    docs = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "demo", "skkc")
    os.makedirs(os.path.join(docs, "ai-detector"), exist_ok=True)
    os.makedirs(os.path.join(docs, "ai-humanizer"), exist_ok=True)
    js = rd("kc", "kc-check.js")
    open(os.path.join(docs, "kc-check.js"), "w", encoding="utf-8", newline="").write(js)
    ver = hashlib.sha256(js.encode("utf-8")).hexdigest()[:8]
    dcss = rd("detector.css")
    base = drop_rules(importantize(dcss[:dcss.index("/* 2026.11.26 아래 차별점 칸")] + "\n" + rd("humanizer.css")), DET_ONLY)
    page_css = minify(base + "\n" + importantize(rd("kc", "kc.css") + "\n" + rd("kc", "page.css")))
    shell_css = minify(rd("kc", "shell.css"))
    tool = compact_html(rd("kc", "tool.html"))
    report = "https://www.skkc.co.kr/shop_view/?idx=6"
    pricing = "https://www.skkc.co.kr/copyclean-pricing#ccpPay"
    cfg = json.dumps({"api": KC_DEMO_API, "demo": True, "chatUrl": "https://skcdesk.channel.io/home", "pricing": pricing, "report": report, "humanizer": "../ai-humanizer/"}, ensure_ascii=False)
    faq = "".join('<details class="kcp-q"%s><summary><i>Q</i>%s</summary><div class="kcp-a">%s</div></details>' % (" open" if i == 0 else "", _kc_esc(q), _kc_esc(a)) for i, (q, a) in enumerate(KC_FAQ))
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KC_FAQ]}, ensure_ascii=False)
    shell = rd("kc", "shell.html")

    def page(title, body, cur, tail=""):
        h = shell
        for k, v in (("{{TITLE}}", title), ("{{SHELL_CSS}}", shell_css), ("{{PAGE_CSS}}", page_css), ("{{BODY}}", body), ("{{CFG}}", cfg), ("{{V}}", ver),
                     ("{{CHAT}}", KC_CHAT_BOOT), ("{{TAIL}}", tail), ("{{CUR_DET}}", ' aria-current="page"' if cur == "det" else ""), ("{{CUR_HUM}}", ' aria-current="page"' if cur == "hum" else "")):
            h = h.replace(k, v)
        return h

    det = rd("kc", "detector.html").replace("{{TOOL}}", tool).replace("{{HUMANIZER}}", "../ai-humanizer/").replace("{{REPORT}}", report).replace("{{FAQ}}", faq)
    det_page = page("[데모] AI 작성률 무료 검사 · AI 사용 여부 확인 | 카피클린 · 성균관컨설팅", compact_html(det), "det",
                    '<script type="application/ld+json">%s</script>' % ld)
    open(os.path.join(docs, "ai-detector", "index.html"), "w", encoding="utf-8", newline="").write(det_page)

    hum = rd("humanizer.html")
    reps = [
        ('<span class="ccd-mflow__s"><b>1</b>문서 보내기</span>', '<span class="ccd-mflow__s"><b>1</b>무료 AI 작성률 검사</span>'),
        ('<a class="ccd-cta" href="https://skcdesk.channel.io/home" target="_blank" rel="noopener"><span class="ccd-cta__text">AI 작성률 개선 의뢰하기</span>',
         '<a class="ccd-cta" href="#kcCheck"><span class="ccd-cta__text">무료로 AI 작성률 검사하기</span>'),
        ('<a class="ccd-link" href="#cchCase">개선 사례 보기<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14"/><path d="m6 13 6 6 6-6"/></svg></a>',
         '<a class="ccd-link" href="https://skcdesk.channel.io/home" target="_blank" rel="noopener" data-kc-chat="hero">바로 견적 상담받기<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg></a>'),
        ('<section class="cch-sec cch-who">', rd("kc", "humanizer_check.html").replace("{{TOOL}}", tool) + '\n<section class="cch-sec cch-who">'),
        ('<section class="cch-sec cch-how">', rd("kc", "humanizer_pay.html").replace("{{PRICING}}", pricing) + '\n<section class="cch-sec cch-how">'),
    ]
    for a, b in reps:
        assert hum.count(a) == 1, a[:60]
        hum = hum.replace(a, b)
    n_det = hum.count('href="/ai-detector"')
    hum = hum.replace('href="/ai-detector"', 'href="../ai-detector/"')
    hum_page = page("[데모] AI 작성률 개선 · 전문 에디터 휴머나이징 | 카피클린 · 성균관컨설팅", compact_html(hum), "hum")
    open(os.path.join(docs, "ai-humanizer", "index.html"), "w", encoding="utf-8", newline="").write(hum_page)
    idx = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1">'
           '<title>카피클린 데모</title><meta http-equiv="refresh" content="0; url=ai-detector/"></head><body><a href="ai-detector/">/ai-detector 데모</a> · <a href="ai-humanizer/">/ai-humanizer 데모</a></body></html>')
    open(os.path.join(docs, "index.html"), "w", encoding="utf-8", newline="").write(idx)
    return {"det": len(det_page), "hum": len(hum_page), "js": len(js), "ver": ver, "det_links": n_det}


# ── 2026.11.28 12:54 대표 '응 그렇게 잘 배포해줘': 카피클린 /ai-detector · /ai-humanizer 실제 쪽(아임웹 코드 위젯) ──
# 서버: AIMarker 서버에 KC서버.gs 1.0.0(skkc.co.kr · www.skkc.co.kr 는 무료 검사만 허용)을 더하고 '카피클린 무료 검사' 배포를 따로 만듦(버전 63).
#       AIMarker · 형제 사이트 여섯 배포는 버전 56 그대로. KO-1126 묶음 25개가 지금 배포(56)와 새 배포(63)에서 한 글자도 같음(13:07~13:16)
# 쪽: 우리 코드 위젯 두 개의 내용을 새 판으로 바꿈(예전 코드는 backup/ 에 그대로). 아임웹 기본 칸은 지우지 않고 CSS 로 숨김
KC_API = "https://script.google.com/macros/s/AKfycbyxjGaM4T0uijCQtR6RHHfxTvkzdex1aYvqaq3pRy_Xlc2NvPojXdsgoAmrw-3GkURYnw/exec"
KC_CDN = "https://copycheck.skkc.co.kr/"   # kc-check.js · textin.js · 글 꺼내기 도구(pdf.js 등)를 두는 곳(GitHub Pages, CORS 허용)
# /ai-detector 에서 숨기는 아임웹 칸(지우지 않음): 첫 섹션의 여백 4 · 그림 지도 1, 아래 섹션 5(소개 · 그림 · 4단계 · 아래 칸 · 자주 묻는 질문)
KC_DET_HIDE = ("#w20260708e7e68f743ba69", "#w202607084db2c0069012f", "#w202607084bce09761819d", "#w20260708dfda217c71dd4", "#w20260708f65ac2c3bf849",
               "#s20260708fe0ddbaafbfaa", "#s20260708678cf93bb3858", "#s20260708f9953ca307aa5", "#s202607082cb706dd1f142", "#s20260708718612b8f8ed5")


def build_kc_prod():
    import hashlib
    import html as H
    rd = lambda *p: open(os.path.join(SRC, *p), encoding="utf-8").read()
    repo = os.path.dirname(os.path.dirname(HERE))
    js = rd("kc", "kc-check.js")
    open(os.path.join(repo, "docs", "assets", "kc-check.js"), "w", encoding="utf-8", newline="").write(js)
    open(os.path.join(repo, "docs", "demo", "skkc", "kc-check.js"), "w", encoding="utf-8", newline="").write(js)
    ver = hashlib.sha256(js.encode("utf-8")).hexdigest()[:8]
    tver = hashlib.sha256(open(os.path.join(repo, "docs", "assets", "textin.js"), "rb").read()).hexdigest()[:8]
    dcss = rd("detector.css")
    base = drop_rules(importantize(dcss[:dcss.index("/* 2026.11.26 아래 차별점 칸")] + "\n" + rd("humanizer.css")), DET_ONLY)
    raw_css = base + "\n" + importantize(rd("kc", "kc.css") + "\n" + rd("kc", "page.css"))
    tool = compact_html(rd("kc", "tool.html"))
    pricing, report = "/copyclean-pricing#ccpPay", "/shop_view/?idx=6"
    cfg = json.dumps({"api": KC_API, "demo": False, "chatUrl": "https://skcdesk.channel.io/home", "pricing": pricing, "report": report,
                      "humanizer": "/ai-humanizer", "root": KC_CDN, "textin": KC_CDN + "assets/textin.js?v=" + tver}, ensure_ascii=False)
    cfg_el = '<div hidden data-kc-cfg="%s"></div>' % H.escape(cfg, quote=True)
    script = '<script src="%sassets/kc-check.js?v=%s"></script>' % (KC_CDN, ver)
    faq = "".join('<details class="kcp-q"%s><summary><i>Q</i>%s</summary><div class="kcp-a">%s</div></details>' % (" open" if i == 0 else "", _kc_esc(q), _kc_esc(a)) for i, (q, a) in enumerate(KC_FAQ))
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in KC_FAQ]}, ensure_ascii=False)
    hide = ",".join(KC_DET_HIDE) + "{display:none !important}"

    det = rd("kc", "detector.html").replace("{{TOOL}}", tool).replace("{{HUMANIZER}}", "/ai-humanizer").replace("{{REPORT}}", report).replace("{{FAQ}}", faq)
    assert "{{" not in det
    det_html = compact_html(det)
    det_css = minify(prune_unused(raw_css, html_classes(det_html), js + det_html))   # 쪽에 없는 class 규칙은 뺌
    det_code = '%s\n<style>\n%s\n%s\n</style>\n%s%s<script type="application/ld+json">%s</script>%s' % (FONT_LINK, det_css, hide, cfg_el, det_html, ld, script)
    open(os.path.join(DIST, "kc_ai-detector_widget.html"), "w", encoding="utf-8").write(det_code)

    hum = rd("humanizer.html")
    reps = [
        ('<span class="ccd-mflow__s"><b>1</b>문서 보내기</span>', '<span class="ccd-mflow__s"><b>1</b>무료 AI 작성률 검사</span>'),
        ('<a class="ccd-cta" href="https://skcdesk.channel.io/home" target="_blank" rel="noopener"><span class="ccd-cta__text">AI 작성률 개선 의뢰하기</span>',
         '<a class="ccd-cta" href="#kcCheck"><span class="ccd-cta__text">무료로 AI 작성률 검사하기</span>'),
        ('<a class="ccd-link" href="#cchCase">개선 사례 보기<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14"/><path d="m6 13 6 6 6-6"/></svg></a>',
         '<a class="ccd-link" href="https://skcdesk.channel.io/home" target="_blank" rel="noopener" data-kc-chat="hero">바로 견적 상담받기<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14"/><path d="m13 6 6 6-6 6"/></svg></a>'),
        ('<section class="cch-sec cch-who">', rd("kc", "humanizer_check.html").replace("{{TOOL}}", tool) + '\n<section class="cch-sec cch-who">'),
        ('<section class="cch-sec cch-how">', rd("kc", "humanizer_pay.html").replace("{{PRICING}}", pricing) + '\n<section class="cch-sec cch-how">'),
    ]
    for a, b in reps:
        assert hum.count(a) == 1, a[:60]
        hum = hum.replace(a, b)
    assert "{{" not in hum
    hum_html = compact_html(hum)
    hum_css = minify(prune_unused(raw_css, html_classes(hum_html), js + hum_html))
    hum_code = "%s\n<style>\n%s\n</style>\n%s%s%s" % (FONT_LINK, hum_css, cfg_el, hum_html, script)
    open(os.path.join(DIST, "kc_ai-humanizer_widget.html"), "w", encoding="utf-8").write(hum_code)
    open(os.path.join(DIST, "preview_kc_detector.html"), "w", encoding="utf-8").write(page_preview("kc ai-detector preview", det_code))
    open(os.path.join(DIST, "preview_kc_humanizer.html"), "w", encoding="utf-8").write(page_preview("kc ai-humanizer preview", hum_code))
    sha = lambda s: hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
    return {"det": len(det_code), "det_sha": sha(det_code), "hum": len(hum_code), "hum_sha": sha(hum_code), "js_ver": ver, "textin_ver": tver}


if __name__ == "__main__":
    print("detector", build_detector(), "detector_more", build_detector_more(), "inquiry", build_inquiry(), "pricing", build_pricing(), "pricing_tc", build_pricing_tc(), "academic", build_academic(), "humanizer", build_humanizer())
    print("hero", build_hero())
    print("skp", build_skp())
    print("kc_demo", build_kc_demo())
    print("kc_prod", build_kc_prod())
