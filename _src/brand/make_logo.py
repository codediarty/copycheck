# -*- coding: utf-8 -*-
"""카피체크 새 로고(2026.11.26 대표가 준 그림 두 장 가운데 흰 바탕용) → 사이트 로고 · 표지 · 아이콘
python3 _src/brand/make_logo.py
  cc-logo-source-light.png(흰 바탕: 초록 리본 C 표지 + 검정 Copy · 초록 Check)에서 흰 바탕만 투명으로 바꿔(색 그대로) 잘라 냄
  -> _src/brand/cc-logo-full.png(원본 크기, render.py 가 상품 그림 · 공유 그림에 씀) · docs/assets/img/cc-logo.png(표지 + 글자, 높이 114px = 38px 화면의 3배) · cc-mark.png(표지만, 256px 정사각)
  -> docs/assets/img/apple-touch-icon.png(180) · logo-192.png · logo-512.png(흰 바탕 가운데 표지) · favicon.svg(표지 그림을 담은 SVG) · docs/favicon.ico(16 · 32 · 48)
cc-logo-source-dark.png(어두운 바탕용)는 원본으로만 보관(사이트가 밝은 바탕이라 흰 바탕용을 씀)"""
import base64, io, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, "docs", "assets", "img")

src = np.array(Image.open(os.path.join(HERE, "cc-logo-source-light.png")).convert("RGB")).astype(np.float64)
a = ((255.0 - src) / 255.0).max(axis=2)           # 흰색을 투명으로(color to alpha)
a[a < 0.035] = 0.0                                 # 바탕 잡티(253~254) 없앰
rgb = np.clip(255.0 - (255.0 - src) / np.clip(a, 1e-6, 1)[..., None], 0, 255)
rgba = np.dstack([rgb, a * 255.0]).round().astype(np.uint8)
rgba[a == 0] = 0
full = Image.fromarray(rgba, "RGBA")

# 원본 그림 속 자리(2172x724): 표지 x334~697 · y186~568, 글자 x744~1890 · y281~487
LOCK = (334 - 6, 186 - 6, 1890 + 7, 568 + 7)
MARK = (334, 186, 697 + 1, 568 + 1)


def down(im, size):
    """투명 가장자리가 검게 번지지 않게(곱한 알파로 줄임)"""
    return im.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


lock = full.crop(LOCK)
lock.save(os.path.join(HERE, "cc-logo-full.png"), optimize=True)   # 원본 크기(상품 그림 · 공유 그림을 그릴 때 씀, 사이트에는 올리지 않음)
H = 114
lk = down(lock, (round(lock.width * H / lock.height), H))
lk.save(os.path.join(IMG, "cc-logo.png"), optimize=True)

mark = full.crop(MARK)
side = max(mark.size)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
down(sq, (256, 256)).save(os.path.join(IMG, "cc-mark.png"), optimize=True)


def icon(sz, bg, k):
    c = Image.new("RGBA", (sz, sz), bg)
    m = down(sq, (round(sz * k), round(sz * k)))
    c.alpha_composite(m, ((sz - m.width) // 2, (sz - m.height) // 2))
    return c


icon(180, (255, 255, 255, 255), .78).convert("RGB").save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)
icon(192, (255, 255, 255, 255), .74).convert("RGB").save(os.path.join(IMG, "logo-192.png"), optimize=True)
icon(512, (255, 255, 255, 255), .74).convert("RGB").save(os.path.join(IMG, "logo-512.png"), optimize=True)
ims = [icon(z, (0, 0, 0, 0), 1.0) for z in (16, 32, 48)]
ims[2].save(os.path.join(ROOT, "docs", "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)], append_images=ims[:2])
b = io.BytesIO(); down(sq, (64, 64)).save(b, "PNG", optimize=True)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64"><image width="64" height="64" '
       'href="data:image/png;base64,%s" xlink:href="data:image/png;base64,%s"/></svg>') % ((base64.b64encode(b.getvalue()).decode(),) * 2)
open(os.path.join(IMG, "favicon.svg"), "w").write(svg)
print("logo", lk.size, "mark", sq.size, "svg", len(svg))
