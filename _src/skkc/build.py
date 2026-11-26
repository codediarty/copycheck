# -*- coding: utf-8 -*-
"""성균관컨설팅(skkc.co.kr) 카피클린 두 쪽 새 디자인 코드 만들기
  python3 build.py
  -> dist/ai-detector_widget.html (아임웹 코드 위젯 w20260708a3f8e71b2ea81 에 넣을 전체 코드: 새 첫 화면 + 예전 차별점 그대로)
  -> dist/ai-humanizer_widget.html (아임웹 /ai-humanizer 새 코드 위젯 전체 코드)
  -> dist/preview_*.html (로컬 확인용, 아임웹 머리글 흉내 + 로컬 글꼴)
CSS 는 src/*.css 에 보통으로 쓰고, 아임웹 기본 CSS 에 지지 않게 모든 선언에 !important 를 붙임(@keyframes 안은 빼고)."""
import os
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
    print("detector", build_detector(), "humanizer", build_humanizer())
