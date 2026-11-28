/* 아임웹 바로 결제 상품(185~244) 요약 · 상세에 '에스크로 안전결제 · 품질 검수 후 전달' 안내를 깔끔한 두 칸 카드로 넣는 도우미.
   2026.11.28 11:17 대표 '못생기게 넣지 말고 둘 다 잘 어울리게, 너무 조잡해'. 상품 수정 화면에서 new Function("IDX","SUBMIT", 이 글) 로 실행.
   이름 · 그림 · 안내 파일 · SEO · 판매가는 그대로 두고 요약 · 상세만 바꿈 */
const sleep = ms => new Promise(r => setTimeout(r, ms));
const deep = (root, pred, out = []) => { for (const e of root.querySelectorAll('*')) { if (pred(e)) out.push(e); if (e.shadowRoot) deep(e.shadowRoot, pred, out); } return out; };
const vis = e => e && e.getBoundingClientRect().width > 0;
if (!(IDX >= 185 && IDX <= 244)) return { IDX, err: 'range' };
if (!new RegExp('[?&]idx=' + IDX + '(&|$)').test(location.search)) return { IDX, err: 'wrong page ' + location.search };
const kind = IDX >= 205 ? 'ex' : 'hm';
const N = kind === 'ex' ? (IDX - 204) * 5 : (IDX - 184) * 5;
const A = N * 10000;
const won = A.toLocaleString('ko-KR');
const live = () => (window.FroalaEditor && FroalaEditor.INSTANCES || []).filter(i => i.el && i.el.isConnected);
let sr = null;
for (let i = 0; i < 60; i++) {
  const h = document.querySelector('bo-shopping-product'); sr = h && h.shadowRoot;
  const nm = sr && deep(sr, e => e.placeholder === '상품명을 입력해 주세요.')[0];
  if (nm && nm.value && live().length >= 2) break;
  await sleep(400);
}
const nameEl = sr && deep(sr, e => e.placeholder === '상품명을 입력해 주세요.')[0];
if (!nameEl) return { IDX, err: 'no form' };
const NAME = kind === 'ex' ? '[성균관컨설팅] 전문가 컨설팅 ' + N + ' 크레딧' : '[카피클린] AI 유사도 개선 ' + N + ' 크레딧';
if (nameEl.value !== NAME) return { IDX, err: 'unexpected name', name: nameEl.value };
const priceEl = deep(sr, e => e.tagName === 'INPUT' && e.placeholder === '0' && vis(e))[0];
if (!priceEl || priceEl.value.replace(/[^0-9]/g, '') !== String(A)) return { IDX, err: 'price mismatch', price: priceEl && priceEl.value };
function setFroala(ins, html) {
  ins.html.set(html); ins.undo && ins.undo.saveStep(); ins.events.trigger('contentChanged');
  ['input', 'keyup'].forEach(t => ins.el.dispatchEvent(new Event(t, { bubbles: true })));
}

const C = kind === 'ex'
  ? { main: '#175df6', soft: '#eef4ff', eyebrow: '#175df6', box: '#f5f8fd', note: '#ebf2ff', noteB: '#d6e4ff', noteT: '#0b2a6e' }
  : { main: '#0b7a4b', soft: '#ecf8f2', eyebrow: '#0e9a62', box: '#f5f7fa', note: '#ecf8f2', noteB: '#cdebdc', noteT: '#14532d' };
const SAFE = ['에스크로 안전결제', '결과물을 받기 전까지 결제금은 전문가가 아닌 성균관컨설팅이 안전하게 보관해요.'];
const QA = ['품질 검수 후 전달', '모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달돼요.'];
const card = t => '<div style="flex:1 1 260px;display:flex;align-items:flex-start;gap:12px;padding:16px 18px;border-radius:14px;background:#ffffff;border:1px solid #e2e8f0;box-shadow:0 10px 24px -20px rgba(15,23,42,0.35);">'
  + '<span style="flex:0 0 32px;width:32px;height:32px;border-radius:10px;background:' + C.soft + ';color:' + C.main + ';font-size:16px;font-weight:800;line-height:32px;text-align:center;">✓</span>'
  + '<div style="flex:1 1 auto;min-width:0;"><p style="margin:0;font-size:15px;font-weight:800;color:#0f172a;">' + t[0] + '</p><p style="margin:3px 0 0;font-size:14px;line-height:1.6;color:#64748b;">' + t[1] + '</p></div></div>';
const ASSURE = '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:24px 0 0;">' + card(SAFE) + card(QA) + '</div>';
const TD = 'width:46px;padding:14px 0;vertical-align:top;font-size:15px;font-weight:800;color:' + C.main + ';';
const row = (no, t, d, last) => '<tr><td style="' + TD + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '">' + no + '</td><td style="padding:14px 0;' + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '"><strong style="font-size:16px;color:#0f172a;">' + t + '</strong><br><span style="font-size:15px;color:#475569;">' + d + '</span></td></tr>';
const WRAP = '<div style="max-width:760px;margin:0 auto;font-family:\'Pretendard Variable\',Pretendard,-apple-system,BlinkMacSystemFont,sans-serif;color:#0f172a;line-height:1.7;word-break:keep-all;">';
let SUM, DETAIL;
if (kind === 'ex') {
  SUM = '<p>성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 전문가 컨설팅 상품입니다. 결과물을 받기 전까지 결제금은 성균관컨설팅이 안전하게 보관하고, 모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달됩니다.</p>';
  DETAIL = WRAP
   + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:' + C.eyebrow + ';">SKKC · 전문가 컨설팅</p>'
   + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">전문가 컨설팅 결제 · ' + N + ' 크레딧</h2>'
   + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 전문가 컨설팅 상품입니다. 결제와 영수증은 성균관컨설팅 이름으로 처리됩니다.</p>'
   + ASSURE
   + '<div style="margin:16px 0 0;padding:22px 24px;border-radius:18px;background:' + C.box + ';border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 1:1 상담에서 작업 범위 · 납기일과 함께 안내받은 크레딧<br>✓ 진행 중 범위가 늘어 추가로 안내받은 크레딧</p></div>'
   + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
   + row('01', '크레딧 안내', '1:1 상담에서 작업 범위 · 납기일 · 크레딧을 함께 정해요.')
   + row('02', '같은 크레딧 결제', '안내받은 크레딧과 같은 상품(' + N + ' 크레딧)으로 결제해요.')
   + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
   + row('04', '진행 · 전달', '전문가가 진행하고, 내부 품질 검수를 거쳐 약속한 날짜까지 결과물을 이메일로 보내요.', true)
   + '</tbody></table>'
   + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:' + C.note + ';border:1px solid ' + C.noteB + ';"><p style="margin:0;font-size:15px;color:' + C.noteT + ';"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:' + C.main + ';font-weight:700;" target="_blank">채팅 상담</a>으로 연락해 크레딧을 안내받아 주세요.</p></div>'
   + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">결제금은 결과물 전달이 끝날 때까지 성균관컨설팅이 보관하는 에스크로 방식입니다. 크레딧은 작업 범위 · 분량 · 일정에 따라 상담에서 정해지며, 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
} else {
  SUM = '<p>카피클린 채팅 상담에서 안내받은 크레딧을 결제하는 AI 유사도 개선 상품입니다. 결과물을 받기 전까지 결제금은 성균관컨설팅이 안전하게 보관하고, 모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달됩니다.</p>';
  DETAIL = WRAP
   + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:' + C.eyebrow + ';">COPYCLEAN · AI 유사도 개선</p>'
   + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">AI 유사도 개선 결제 · ' + N + ' 크레딧</h2>'
   + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">카피클린 채팅 상담에서 안내받은 크레딧을 결제하는 AI 유사도 개선 상품입니다. 결제와 영수증은 카피클린을 운영하는 성균관컨설팅 이름으로 처리됩니다.</p>'
   + ASSURE
   + '<div style="margin:16px 0 0;padding:22px 24px;border-radius:18px;background:' + C.box + ';border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 채팅 상담에서 문서를 확인하고 안내받은 AI 유사도 개선 크레딧<br>✓ 진행 중 개선 범위가 늘어 추가로 안내받은 크레딧</p></div>'
   + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
   + row('01', '크레딧 안내', '채팅 상담에서 문서를 확인하고 개선 크레딧을 안내받아요.')
   + row('02', '같은 크레딧 결제', '안내받은 크레딧과 같은 상품(' + N + ' 크레딧)으로 결제해요.')
   + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
   + row('04', '개선 · 전달', '전담 에디터가 개선하고, 내부 품질 검수를 거쳐 AI 유사도를 다시 확인한 뒤 전달해요.', true)
   + '</tbody></table>'
   + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:' + C.note + ';border:1px solid ' + C.noteB + ';"><p style="margin:0;font-size:15px;color:' + C.noteT + ';"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:' + C.main + ';font-weight:700;" target="_blank">채팅 상담</a>으로 문서를 보내 크레딧을 안내받아 주세요.</p></div>'
   + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">결제금은 결과물 전달이 끝날 때까지 성균관컨설팅이 보관하는 에스크로 방식입니다. 크레딧은 문서 분량, 개선 구간, 희망 일정에 따라 상담에서 정해지며, 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
}
let ins = live();
setFroala(ins[0], SUM);
setFroala(ins[ins.length - 1], DETAIL);
await sleep(400);
ins = live();
const txt = h => { const d = document.createElement('div'); d.innerHTML = h; return d.textContent; };
const det = txt(ins[ins.length - 1].html.get());
const ok = {
  sum: txt(ins[0].html.get()).indexOf('내부 품질 검수 기준을 충족한 후 최종 전달됩니다') >= 0,
  det: det.indexOf('에스크로 안전결제') >= 0 && det.indexOf('품질 검수 후 전달') >= 0 && det.indexOf(N + ' 크레딧') >= 0 && det.indexOf(won) < 0 && det.indexOf('논문') < 0,
  flex: ins[ins.length - 1].html.get().indexOf('flex:1 1 260px') >= 0,
  name: nameEl.value === NAME,
  price: priceEl.value.replace(/[^0-9]/g, '') === String(A)
};
const all = Object.values(ok).every(Boolean);
if (!SUBMIT || !all) return { IDX, N, ok, submitted: false };
const save = deep(sr, e => e.tagName === 'BUTTON' && (e.textContent || '').trim() === '저장' && vis(e))[0];
if (!save) return { IDX, N, ok, err: 'no save button' };
save.click();
let toast = '';
for (let i = 0; i < 30 && !toast; i++) {
  await sleep(400);
  const t = deep(document, e => e.children.length === 0 && /저장되었|저장했|수정되었|완료/.test((e.textContent || '').trim()) && vis(e))[0];
  if (t) toast = t.textContent.trim();
}
return { IDX, N, ok, submitted: true, toast };
