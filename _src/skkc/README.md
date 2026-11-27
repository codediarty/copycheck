# 성균관컨설팅(skkc.co.kr) 카피클린 쪽 코드

아임웹 코드 위젯에 넣는 코드의 원본입니다. 사이트(copycheck.skkc.co.kr) 빌드와는 따로 움직입니다.

- `src/detector.css`, `src/detector_hero.html`: /ai-detector 첫 화면(코드 위젯 w20260708a3f8e71b2ea81)
- `src/detector_more.css`, `src/detector_more.html`: /ai-detector 아래 칸(2026.11.27, 그림 9장 대신 글자. 바탕 규칙은 humanizer.css 의 .cch 를 빌드 때 가져옴, 새 코드 위젯은 섹션 s202607082cb706dd1f142 맨 아래)
- `src/inquiry.css`, `src/inquiry.html`: /copyclean-inquiry 첫 칸(코드 위젯 w20260708800e3d6a4bfc5, 2026.11.27) + 아래 입력폼(w202607085502e59ce09ef) 모양. 입력폼 단추 글('도입 문의 보내기') · 완료 글 · 개인정보 동의 글은 아임웹 입력폼 설정에서 바꿈(예전 동의 글은 backup/copyclean-inquiry_form_privacy_before_20261127.txt)
- `src/humanizer.css`, `src/humanizer.html`: /ai-humanizer 전체 쪽
- `python3 build.py` → `dist/ai-detector_widget.html`, `dist/ai-detector_more_widget.html`, `dist/copyclean-inquiry_widget.html`, `dist/ai-humanizer_widget.html` (아임웹 디자인 모드 → 코드 설정에 그대로 넣음)
- `backup/`: 바꾸기 전 /ai-detector 코드 위젯 원본(되돌릴 때 그대로 붙여 넣기)
- CSS 는 보통으로 쓰고, 빌드할 때 아임웹 기본 CSS 에 지지 않게 `!important` 를 붙임
