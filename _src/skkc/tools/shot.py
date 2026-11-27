# 사용: python3 tools/shot.py dist/preview_detector.html shots/det 1440,1280,1024,768,390 [full]
import sys, asyncio
from playwright.async_api import async_playwright

async def main():
    src, out, widths = sys.argv[1], sys.argv[2], [int(w) for w in sys.argv[3].split(',')]
    full = len(sys.argv) > 4 and sys.argv[4] == 'full'
    async with async_playwright() as p:
        try:
            b = await p.chromium.launch()
        except Exception:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w in widths:
            h = 900 if w > 800 else 844
            pg = await b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
            await pg.goto('file://' + __import__('os').path.abspath(src))
            await pg.wait_for_timeout(600)
            # 화면에 들어올 때 보이는 칸(.skp [data-rv])까지 다 보이게 끝까지 한 번 내려 봄
            await pg.evaluate('''async () => { const H = document.documentElement.scrollHeight; for (let y = 0; y < H; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); }''')
            await pg.wait_for_timeout(1400)
            sw = await pg.evaluate('document.documentElement.scrollWidth')
            hh = await pg.evaluate('document.documentElement.scrollHeight')
            await pg.screenshot(path='%s_%d.png' % (out, w), full_page=full)
            print(w, 'scrollWidth', sw, 'height', hh)
            await pg.close()
        await b.close()

asyncio.run(main())
