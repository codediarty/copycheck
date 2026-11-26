# 성균관컨설팅(skkc.co.kr) 카피클린 쪽 코드

아임웹 코드 위젯에 넣는 코드의 원본입니다. 사이트(copycheck.skkc.co.kr) 빌드와는 따로 움직입니다.

- `src/detector.css`, `src/detector_hero.html`: /ai-detector 첫 화면(코드 위젯 w20260708a3f8e71b2ea81)
- `src/humanizer.css`, `src/humanizer.html`: /ai-humanizer 전체 쪽
- `python3 build.py` → `dist/ai-detector_widget.html`, `dist/ai-humanizer_widget.html` (아임웹 디자인 모드 → 코드 설정에 그대로 넣음)
- `backup/`: 바꾸기 전 /ai-detector 코드 위젯 원본(되돌릴 때 그대로 붙여 넣기)
- CSS 는 보통으로 쓰고, 빌드할 때 아임웹 기본 CSS 에 지지 않게 `!important` 를 붙임
