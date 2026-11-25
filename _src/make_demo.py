# -*- coding: utf-8 -*-
"""엔진 실측(CC서버.gs ccDemoAll 의 CCB 줄, 카피체크 배포 버전 55, 2026.11.25)을 예시 화면 데이터(demo.json)로. python3 _src/make_demo.py
후보 6편을 잰 값 가운데 글 종류마다 하나씩(논문 · 사업계획서 · 대학 레포트 · 연구 보고서). 값은 엔진이 낸 그대로이며, 글마다 결과는 다릅니다"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
META = {"c_thesis": ("논문", "석사논문_결론.hwp"), "c_plan": ("사업계획서", "지원사업_계획서.hwpx"),
        "c_report": ("대학 레포트", "환경_교양레포트.docx"), "c_thesis2": ("연구 보고서", "직무스트레스_연구.pdf")}
ORDER = ["c_thesis", "c_plan", "c_report", "c_thesis2"]
raw = json.load(open(os.path.join(HERE, "demo_raw", "ccb_20261125.json"), encoding="utf-8"))
out = []
for k in ORDER:
    o = raw[k]
    out.append({"k": k, "label": META[k][0], "file": META[k][1], "src": o["src"], "dst": o["dst"],
                "ai": [i for i, s in enumerate(o["sc"]) if s[1]], "scores": {str(i): s[0] for i, s in enumerate(o["sc"]) if s[1]},
                "after_scores": {str(i): s[0] for i, s in enumerate(o.get("afterSc", []))},
                "before": {"rate": o["before"]["rate"], "band": o["before"]["band"], "n": o["before"]["n"]},
                "after": {"rate": o["after"]["rate"], "band": o["after"]["band"], "n": o["after"]["n"]}, "applied": o.get("ch", 0)})
json.dump({"samples": out, "measured": "2026.11.25 카피체크 엔진 실측값(판정 기준 1.6 · 인간화 엔진 HUM 2.5, 한 번의 휴머나이징). 글마다 결과는 다르며, 한 번에 덜 내려간 글은 다시 휴머나이징하면 더 낮아집니다."},
          open(os.path.join(HERE, "demo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("samples", [(s["k"], s["before"]["rate"], s["after"]["rate"]) for s in out])
