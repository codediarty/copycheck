# 성균관컨설팅(skkc.co.kr) 카피클린 쪽 코드

아임웹 코드 위젯에 넣는 코드의 원본입니다. 사이트(copycheck.skkc.co.kr) 빌드와는 따로 움직입니다.

- `src/detector.css`, `src/detector_hero.html`: /ai-detector 첫 화면(코드 위젯 w20260708a3f8e71b2ea81)
- `src/detector_more.css`, `src/detector_more.html`: /ai-detector 아래 칸(2026.11.27, 그림 9장 대신 글자. 바탕 규칙은 humanizer.css 의 .cch 를 빌드 때 가져옴, 새 코드 위젯은 섹션 s202607082cb706dd1f142 맨 아래)
- `src/inquiry.css`, `src/inquiry.html`: /copyclean-inquiry 첫 칸(코드 위젯 w20260708800e3d6a4bfc5, 2026.11.27) + 아래 입력폼(w202607085502e59ce09ef) 모양. 입력폼 단추 글('도입 문의 보내기') · 완료 글 · 개인정보 동의 글은 아임웹 입력폼 설정에서 바꿈(예전 동의 글은 backup/copyclean-inquiry_form_privacy_before_20261127.txt)
- `src/pricing_pay.css`, `src/pricing_pay.html`: /copyclean-pricing(바로 결제) 코드 위젯 w20260708b6614391e575a 에 더한 'AI 유사도 개선 결제' 금액 고르기(2026.11.27). 예전 코드(backup/copyclean-pricing_w20260708b6614391e575a_before_20261127.html)는 그대로 두고 카드 단추 아래 길잡이 한 줄 + 상세내역서 칸 앞에 금액 칸을 끼워 넣음. 금액 칸 링크 = /shop_view?idx=(184 + 금액/50,000), 상품 185(5만 원) ~ 204(100만 원)
- `src/academic.css`, `src/academic.js`: /academic-info 학술정보 게시판(위젯 w20260818cbad0e3273d77) 글 보기 · 목록 모양(2026.11.27). 저장된 글은 그대로 두고, 같은 페이지 코드 위젯 하나(스타일 + 스크립트)로 보이는 모양만 바꿈. 예전 글(■ 제목, 빈 줄 문단, '- ' 줄, '1. ' 줄, '… → 주소' 줄, #태그 줄)은 스크립트가 보일 때만 ac-* 이름표를 붙여 제목 · 목록 · 단추 모양으로. 되돌리기: 그 코드 위젯을 숨기거나 지우면 예전 모양 그대로
- `src/skp/`: 성균관컨설팅 소개 페이지 7곳 새 디자인(2026.11.27). base.css · parts.css · base.js 는 함께 쓰고, 페이지마다 <이름>.html(+ reviews.css · reviews.js). 빌드하면 dist/skp_<이름>_widget.html. 각 페이지 첫 칸(배너 칸) 맨 아래 새 코드 위젯에 넣고 가로 영역 확장을 켬. 예전 배너 글 · 칸은 지우지 않고 숨김(build.py SKP_PAGES 의 first_w · hide_s). /reviews 는 숫자 칸 · 후기 47건 위젯을 그대로 두고 모양만 바꿈. 되돌리기: 새 코드 위젯을 숨기거나 지우면 예전 화면
- `src/skp/thesis-consulting.*`(2026.11.27 22:45 추가): /thesis-consulting 논문 컨설팅. 새 위젯은 첫 칸(s20260708a3c65e18cbed6) 맨 아래. 둘째 칸(s2026070870b8543218885)은 thesis-consulting.css 에서 예전 글 · 가치 카드 · 여백을 숨기고(지우지 않음) 상담 신청 폼(w2026070842b4c10d80377)과 11.25 검색 글 위젯(w20261125afb1d408ed1d1)의 자주 묻는 질문만 새 모양으로. 쪽 CSS 코드 위젯 w2026070841fa96fb35489 · w20260708b2095be7d97f2 는 그대로. FAQPage 구조화 데이터는 11.25 위젯 안에 그대로
- `src/humanizer.css`, `src/humanizer.html`: /ai-humanizer 전체 쪽
- `python3 build.py` → `dist/ai-detector_widget.html`, `dist/ai-detector_more_widget.html`, `dist/copyclean-inquiry_widget.html`, `dist/copyclean-pricing_widget.html`, `dist/academic-info_widget.html`, `dist/ai-humanizer_widget.html` (아임웹 디자인 모드 → 코드 설정에 그대로 넣음)
- `backup/`: 바꾸기 전 /ai-detector 코드 위젯 원본(되돌릴 때 그대로 붙여 넣기)
- CSS 는 보통으로 쓰고, 빌드할 때 아임웹 기본 CSS 에 지지 않게 `!important` 를 붙임
