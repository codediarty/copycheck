/* 아임웹 바로 결제 상품(185~244)을 크레딧 표시로 고치는 도우미. 상품 수정 화면(/admin/shopping/product/detail?idx=N)에서
   new Function("IDX","IMG","SUBMIT", 이 글) 로 실행. 2026.11.28 대표 '40만원 보다 40 크레딧', '총 상품금액에만 1번만'
   상품명 · 대표 그림 · 요약 설명 · 상세 설명 · SEO 제목과 설명에서 원 금액을 빼고 크레딧으로(판매가 · 결제 금액은 그대로) */
const RAW = 'https://raw.githubusercontent.com/codediarty/copycheck/4ee9e0a661aab0d4c209c07d734300a3cf0b2a11/_src/skkc/shop/';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const deep = (root, pred, out = []) => { for (const e of root.querySelectorAll('*')) { if (pred(e)) out.push(e); if (e.shadowRoot) deep(e.shadowRoot, pred, out); } return out; };
const vis = e => e && e.getBoundingClientRect().width > 0;
if (!(IDX >= 185 && IDX <= 244)) return { IDX, err: 'range' };
if (!new RegExp('[?&]idx=' + IDX + '(&|$)').test(location.search)) return { IDX, err: 'wrong page ' + location.search };
const kind = IDX >= 205 ? 'tc' : 'hm';
const N = kind === 'tc' ? (IDX - 204) * 5 : (IDX - 184) * 5;
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
const OLD = kind === 'tc' ? '[성균관컨설팅] 논문 컨설팅 결제 (' + won + '원)' : '[카피클린] AI 유사도 개선 결제 (' + won + '원)';
const NAME = kind === 'tc' ? '[성균관컨설팅] 논문 컨설팅 ' + N + ' 크레딧' : '[카피클린] AI 유사도 개선 ' + N + ' 크레딧';
if (nameEl.value !== OLD && nameEl.value !== NAME) return { IDX, err: 'unexpected name', name: nameEl.value };
const priceEl = deep(sr, e => e.tagName === 'INPUT' && e.placeholder === '0' && vis(e))[0];
const price = priceEl ? priceEl.value.replace(/[^0-9]/g, '') : '';
if (price !== String(A)) return { IDX, err: 'price mismatch', price };

function setVal(el, v) {
  const proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  el.focus();
  Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v);
  ['input', 'change'].forEach(t => el.dispatchEvent(new Event(t, { bubbles: true, composed: true })));
  el.dispatchEvent(new FocusEvent('blur', { bubbles: true, composed: true }));
}
function setFroala(ins, html) {
  ins.html.set(html); ins.undo && ins.undo.saveStep(); ins.events.trigger('contentChanged');
  ['input', 'keyup'].forEach(t => ins.el.dispatchEvent(new Event(t, { bubbles: true })));
}

let SUM, DETAIL, SEO_T, SEO_D;
if (kind === 'tc') {
  SUM = '<p>성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 논문 컨설팅 상품입니다.</p>';
  const TD = 'width:46px;padding:14px 0;vertical-align:top;font-size:15px;font-weight:800;color:#175df6;';
  const row = (no, t, d, last) => '<tr><td style="' + TD + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '">' + no + '</td><td style="padding:14px 0;' + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '"><strong style="font-size:16px;color:#0f172a;">' + t + '</strong><br><span style="font-size:15px;color:#475569;">' + d + '</span></td></tr>';
  DETAIL = '<div style="max-width:760px;margin:0 auto;font-family:\'Pretendard Variable\',Pretendard,-apple-system,BlinkMacSystemFont,sans-serif;color:#0f172a;line-height:1.7;word-break:keep-all;">'
   + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:#175df6;">SKKC · 논문 컨설팅</p>'
   + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">논문 컨설팅 결제 · ' + N + ' 크레딧</h2>'
   + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 논문 컨설팅 상품입니다. 결제와 영수증은 성균관컨설팅 이름으로 처리됩니다.</p>'
   + '<div style="margin:26px 0 0;padding:22px 24px;border-radius:18px;background:#f5f8fd;border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 1:1 상담에서 작업 범위 · 납기일과 함께 안내받은 크레딧<br>✓ 진행 중 범위가 늘어 추가로 안내받은 크레딧</p></div>'
   + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
   + row('01', '크레딧 안내', '1:1 상담에서 작업 범위 · 납기일 · 크레딧을 함께 정해요.')
   + row('02', '같은 크레딧 결제', '안내받은 크레딧과 같은 상품(' + N + ' 크레딧)으로 결제해요.')
   + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
   + row('04', '진행 · 전달', '전문가가 진행하고, 약속한 날짜까지 결과물을 이메일로 보내요.', true)
   + '</tbody></table>'
   + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:#ebf2ff;border:1px solid #d6e4ff;"><p style="margin:0;font-size:15px;color:#0b2a6e;"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:#175df6;font-weight:700;" target="_blank">채팅 상담</a>으로 연락해 크레딧을 안내받아 주세요.</p></div>'
   + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">결제금은 결과물 전달이 끝날 때까지 플랫폼이 보관하는 에스크로 방식입니다. 크레딧은 작업 범위 · 분량 · 일정에 따라 상담에서 정해지며, 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
  SEO_T = '논문 컨설팅 ' + N + ' 크레딧 | 성균관컨설팅';
  SEO_D = '성균관컨설팅 1:1 상담에서 안내받은 논문 컨설팅 크레딧을 결제하는 상품입니다. 결제금은 결과물 전달까지 플랫폼이 보관합니다.';
} else {
  SUM = '<p>카피클린 채팅 상담에서 안내받은 크레딧을 결제하는 AI 유사도 개선 상품입니다.</p>';
  const TD = 'width:46px;padding:14px 0;vertical-align:top;font-size:15px;font-weight:800;color:#0b7a4b;';
  const row = (no, t, d, last) => '<tr><td style="' + TD + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '">' + no + '</td><td style="padding:14px 0;' + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '"><strong style="font-size:16px;color:#0f172a;">' + t + '</strong><br><span style="font-size:15px;color:#475569;">' + d + '</span></td></tr>';
  DETAIL = '<div style="max-width:760px;margin:0 auto;font-family:\'Pretendard Variable\',Pretendard,-apple-system,BlinkMacSystemFont,sans-serif;color:#0f172a;line-height:1.7;word-break:keep-all;">'
   + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:#0e9a62;">COPYCLEAN · AI 유사도 개선</p>'
   + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">AI 유사도 개선 결제 · ' + N + ' 크레딧</h2>'
   + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">카피클린 채팅 상담에서 안내받은 크레딧을 결제하는 AI 유사도 개선 상품입니다. 결제와 영수증은 카피클린을 운영하는 성균관컨설팅 이름으로 처리됩니다.</p>'
   + '<div style="margin:26px 0 0;padding:22px 24px;border-radius:18px;background:#f5f7fa;border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 채팅 상담에서 문서를 확인하고 안내받은 AI 유사도 개선 크레딧<br>✓ 진행 중 개선 범위가 늘어 추가로 안내받은 크레딧</p></div>'
   + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
   + row('01', '크레딧 안내', '채팅 상담에서 문서를 확인하고 개선 크레딧을 안내받아요.')
   + row('02', '같은 크레딧 결제', '안내받은 크레딧과 같은 상품(' + N + ' 크레딧)으로 결제해요.')
   + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
   + row('04', '개선 진행', '전담 에디터가 개선하고, AI 유사도를 다시 확인한 뒤 전달해요.', true)
   + '</tbody></table>'
   + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:#ecf8f2;border:1px solid #cdebdc;"><p style="margin:0;font-size:15px;color:#14532d;"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:#0b7a4b;font-weight:700;" target="_blank">채팅 상담</a>으로 문서를 보내 크레딧을 안내받아 주세요.</p></div>'
   + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">크레딧은 문서 분량, 개선 구간, 희망 일정에 따라 상담에서 정해집니다. 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
  SEO_T = 'AI 유사도 개선 ' + N + ' 크레딧 | 카피클린';
  SEO_D = '카피클린 채팅 상담에서 안내받은 AI 유사도 개선 크레딧을 결제하는 상품입니다. 결제와 영수증은 성균관컨설팅 이름으로 처리됩니다.';
}
const log = [];
// 1. 대표 그림(IMG 가 참일 때만): 있던 그림을 빼고 크레딧 그림 하나로
if (IMG) {
  for (const d of deep(sr, e => e.tagName === 'BUTTON' && e.classList.contains('delete-button') && e.closest('.image-item'))) { d.click(); await sleep(500); }
  const fin = deep(sr, e => e.tagName === 'INPUT' && e.type === 'file' && /\.jpg/.test(e.accept || ''))[0];
  const file = kind + '-c' + N + '.jpg';
  const b = await fetch(RAW + file, { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error('fetch ' + file + ' ' + r.status); return r.blob(); });
  const dt = new DataTransfer(); dt.items.add(new File([b], file, { type: 'image/jpeg' }));
  fin.files = dt.files; fin.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
  for (let i = 0; i < 40; i++) { await sleep(500); const im = deep(sr, e => e.tagName === 'IMG' && e.closest('.image-item')); if (im.length === 1 && /cdn/.test(im[0].getAttribute('src') || '')) break; }
  log.push('img ' + b.size);
}
// 2. 상품명 · 3. 요약 · 4. 상세
setVal(nameEl, NAME);
let ins = live();
setFroala(ins[0], SUM);
setFroala(ins[ins.length - 1], DETAIL);
// 5. SEO
const seoHd = deep(sr, e => e.getAttribute && e.getAttribute('role') === 'button' && /^SEO\(검색엔진 최적화\)/.test((e.textContent || '').trim()))[0];
if (seoHd && seoHd.getAttribute('aria-expanded') !== 'true') { seoHd.click(); await sleep(800); }
const st = deep(sr, e => e.tagName === 'INPUT' && /상품명과 동일하게/.test(e.placeholder || ''))[0];
const sd = deep(sr, e => e.tagName === 'TEXTAREA' && /상품 상세에 입력한/.test(e.placeholder || ''))[0];
if (st) setVal(st, SEO_T); if (sd) setVal(sd, SEO_D);
await sleep(300);
// 확인
ins = live();
const imgs = deep(sr, e => e.tagName === 'IMG' && e.closest('.image-item'));
const ok = {
  name: nameEl.value === NAME,
  img: imgs.length === 1 && /cdn/.test(imgs[0].getAttribute('src') || ''),
  sum: ins[0].html.get().indexOf('크레딧을 결제하는') > 0 && ins[0].html.get().indexOf('원') < 0,
  det: ins[ins.length - 1].html.get().indexOf(N + ' 크레딧') > 0 && ins[ins.length - 1].html.get().indexOf(won) < 0,
  seo: !!(st && sd && st.value === SEO_T && sd.value === SEO_D),
  price: priceEl.value.replace(/[^0-9]/g, '') === String(A)
};
const all = Object.values(ok).every(Boolean);
if (!SUBMIT || !all) return { IDX, N, log, ok, submitted: false };
const save = deep(sr, e => e.tagName === 'BUTTON' && (e.textContent || '').trim() === '저장' && vis(e))[0];
if (!save) return { IDX, N, log, ok, err: 'no save button' };
save.click();
let toast = '';
for (let i = 0; i < 30 && !toast; i++) {
  await sleep(400);
  const t = deep(document, e => e.children.length === 0 && /저장되었|저장했|수정되었|완료/.test((e.textContent || '').trim()) && vis(e))[0];
  if (t) toast = t.textContent.trim();
}
return { IDX, N, log, ok, submitted: true, toast, url: location.pathname + location.search };
