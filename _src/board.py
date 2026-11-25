# -*- coding: utf-8 -*-
"""예전 카피체크 커뮤니티 글 8편(2026.08, /board/*.html)을 새 디자인으로 다시 냄. 주소는 그대로(검색 노출 유지).
글 내용은 예전 그대로 두고, 줄표(—)만 쉼표 · 쌍점으로 바꾸고(대표 지시), 예전 외부 의뢰 링크 대신 새 검사 도구로 연결"""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "old_board")


PART = r"(?=(?:이|가|을|를|은|는|의|과|와|로|으로|에|에서)\s)"


def _dash(s, title=False):
    """줄표 바꾸기: 제목은 쌍점, 본문의 끼움 말(— … —)은 괄호, 강조 뒤는 쌍점, 나머지는 쉼표 · 문장 나누기"""
    if title:
        return re.sub(r"\s*—\s*", ": ", s)
    s = re.sub(r"\s—\s([^—<]{1,60}?)\s—\s" + PART, r"(\1)", s)
    s = re.sub(r"\s—\s([^—<]{1,60}?)\s—\s", r"(\1) ", s)
    s = re.sub(r"(</strong>|</b>)\s*—\s*", r"\1: ", s)
    s = re.sub(r"(다)\s+—\s+", r"\1. ", s)
    s = re.sub(r"(\")\s+—\s+", r"\1. ", s)
    s = re.sub(r"\s*—\s*", ", ", s)
    return s.replace(", ,", ",")


def _text(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def load():
    out = []
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith(".html"):
            continue
        s = open(os.path.join(SRC, fn), encoding="utf-8").read()
        art = re.search(r"<article[\s\S]*?</article>", s).group(0)
        h1 = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", art).group(1)
        lede = re.search(r'<p class="lede"[^>]*>([\s\S]*?)</p>', art)
        body = re.search(r'<div itemprop="articleBody">([\s\S]*?)</div>\s*<div class="cta-box">', art)
        date = re.search(r'datetime="(\d{4}-\d{2}-\d{2})"', art).group(1)
        cat = re.search(r'<span class="cat[^"]*">([^<]*)</span>', art)
        desc = re.search(r'<meta name="description" content="([^"]*)"', s)
        title = re.search(r"<title>([^<]*)</title>", s).group(1).split(" | ")[0]
        b = body.group(1).strip() if body else ""
        b = re.sub(r'<a [^>]*href="https?://(www\.)?skkc\.co\.kr/[^"]*"[^>]*>([\s\S]*?)</a>', r'<a href="/#tool">\2</a>', b)
        b = re.sub(r"\n\s*", "\n", b)
        out.append({"slug": fn[:-5], "path": "board/" + fn, "date": date, "cat": _text(cat.group(1)) if cat else "커뮤니티",
                    "h1": _dash(_text(h1), True), "title": _dash(_text(title), True), "desc": _dash(html.unescape(desc.group(1))) if desc else "",
                    "lede": _dash(_text(lede.group(1))) if lede else "", "body": _dash(b)})
    out.sort(key=lambda x: x["date"])
    return out


POSTS = load()
