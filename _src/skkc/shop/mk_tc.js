/* 아임웹 새 디지털 상품 등록 도우미(논문 컨설팅 결제 N원). new Function("A","SUBMIT", 이 글) 로 실행. 2026.11.28 */
const RAW = 'https://raw.githubusercontent.com/codediarty/copycheck/c4fefee2d9a442af0c8a3f7496590a4ba24e4218/_src/skkc/shop/';
const fmt = n => n.toLocaleString('ko-KR');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const deep = (root, pred, out = []) => { for (const e of root.querySelectorAll('*')) { if (pred(e)) out.push(e); if (e.shadowRoot) deep(e.shadowRoot, pred, out); } return out; };
const vis = e => e && e.getBoundingClientRect().width > 0;
const log = [];
let sr = null;
for (let i = 0; i < 50; i++) { const h = document.querySelector('bo-shopping-product'); sr = h && h.shadowRoot; if (sr && deep(sr, e => e.tagName === 'INPUT' && e.type === 'file').length >= 2 && document.querySelectorAll('[contenteditable=true]').length >= 1) break; await sleep(400); }
if (!sr) throw new Error('no form');
if (/idx=/.test(location.search)) return { A, err: 'not a new product page' };
function setVal(el, v) {
  const proto = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
  el.focus();
  Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v);
  ['input', 'change'].forEach(t => el.dispatchEvent(new Event(t, { bubbles: true, composed: true })));
  el.dispatchEvent(new FocusEvent('blur', { bubbles: true, composed: true }));
}
async function setFile(input, url, name, type) {
  const b = await fetch(url, { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error('fetch ' + url + ' ' + r.status); return r.blob(); });
  const f = new File([b], name, { type });
  const dt = new DataTransfer(); dt.items.add(f);
  input.files = dt.files;
  input.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
  return b.size;
}
const NAME = '[성균관컨설팅] 논문 컨설팅 결제 (' + fmt(A) + '원)';
const SUM = '<p>성균관컨설팅 상담에서 안내받은 논문 컨설팅 금액을 결제하는 상품입니다. 결제 금액 ' + fmt(A) + '원.</p>';
const TD = 'width:46px;padding:14px 0;vertical-align:top;font-size:15px;font-weight:800;color:#175df6;';
const row = (no, t, d, last) => '<tr><td style="' + TD + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '">' + no + '</td><td style="padding:14px 0;' + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '"><strong style="font-size:16px;color:#0f172a;">' + t + '</strong><br><span style="font-size:15px;color:#475569;">' + d + '</span></td></tr>';
const DETAIL = '<div style="max-width:760px;margin:0 auto;font-family:\'Pretendard Variable\',Pretendard,-apple-system,BlinkMacSystemFont,sans-serif;color:#0f172a;line-height:1.7;word-break:keep-all;">'
 + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:#175df6;">SKKC · 논문 컨설팅</p>'
 + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">논문 컨설팅 결제 · ' + fmt(A) + '원</h2>'
 + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">성균관컨설팅 상담에서 안내받은 논문 컨설팅 금액을 결제하는 상품입니다. 결제와 영수증은 성균관컨설팅 이름으로 처리됩니다.</p>'
 + '<div style="margin:26px 0 0;padding:22px 24px;border-radius:18px;background:#f5f8fd;border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 1:1 상담에서 작업 범위 · 납기일과 함께 안내받은 금액<br>✓ 진행 중 범위가 늘어 추가로 안내받은 금액</p></div>'
 + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
 + row('01', '금액 안내', '1:1 상담에서 작업 범위 · 납기일 · 금액을 함께 정해요.')
 + row('02', '같은 금액 결제', '안내받은 금액과 같은 상품(' + fmt(A) + '원)으로 결제해요.')
 + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
 + row('04', '진행 · 전달', '전문가가 진행하고, 약속한 날짜까지 결과물을 이메일로 보내요.', true)
 + '</tbody></table>'
 + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:#ebf2ff;border:1px solid #d6e4ff;"><p style="margin:0;font-size:15px;color:#0b2a6e;"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:#175df6;font-weight:700;" target="_blank">채팅 상담</a>으로 연락해 금액을 안내받아 주세요.</p></div>'
 + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">결제금은 결과물 전달이 끝날 때까지 플랫폼이 보관하는 에스크로 방식입니다. 결제 금액은 작업 범위 · 분량 · 일정에 따라 상담에서 정해지며, 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
const SEO_T = '논문 컨설팅 결제 (' + fmt(A) + '원) | 성균관컨설팅';
const SEO_D = '성균관컨설팅 상담에서 안내받은 논문 컨설팅 금액 ' + fmt(A) + '원을 결제하는 상품입니다. 결제금은 결과물 전달까지 플랫폼이 보관합니다.';

// 1. 대표 그림 · 2. 디지털 파일
const fins = deep(sr, e => e.tagName === 'INPUT' && e.type === 'file');
log.push('img ' + await setFile(fins[0], RAW + 'tc-' + A + '.jpg', 'tc-' + A + '.jpg', 'image/jpeg'));
await sleep(1800);
log.push('file ' + await setFile(fins[1], RAW + 'tc-guide.png', '성균관컨설팅-논문컨설팅-결제-안내.png', 'image/png'));
await sleep(1800);
// 3. 상품명
setVal(deep(sr, e => e.placeholder === '상품명을 입력해 주세요.')[0], NAME);
// 4. 카테고리 '컨설팅'
const cbtn = deep(sr, e => e.tagName === 'BUTTON' && (e.textContent || '').trim() === '카테고리 선택')[0];
cbtn.click(); await sleep(700);
const cs = deep(document, e => e.children.length === 0 && (e.textContent || '').trim() === '컨설팅' && vis(e))[0];
if (!cs) throw new Error('no category option');
(cs.closest('label') || cs.parentElement).click(); await sleep(500);
cbtn.click(); await sleep(400);
// 5. 요약 설명(첫 Froala)
let ins = (window.FroalaEditor && FroalaEditor.INSTANCES || []).filter(i => i.el && i.el.isConnected);
ins[0].html.set(SUM); ins[0].undo && ins[0].undo.saveStep(); ins[0].events.trigger('contentChanged');
['input', 'keyup'].forEach(t => ins[0].el.dispatchEvent(new Event(t, { bubbles: true })));
// 6. 브랜드
setVal(deep(sr, e => e.placeholder === '브랜드를 입력해 주세요.')[0], '성균관컨설팅');
// 7. 판매가
const p0 = deep(sr, e => e.tagName === 'INPUT' && e.placeholder === '0' && vis(e));
setVal(p0[0], String(A));
// 8. 할인 끔
for (const t of ['쇼핑 등급 할인', '쿠폰 할인']) {
  const cb = deep(sr, e => e.tagName === 'INPUT' && e.type === 'checkbox' && e.closest('label') && e.closest('label').textContent.trim() === t)[0];
  if (cb && cb.checked) cb.click();
}
// 9. 상세 설명(에디터로 등록)
const ed = deep(sr, e => e.tagName === 'LABEL' && (e.textContent || '').trim() === '에디터로 등록')[0];
if (ed) { ed.click(); await sleep(1200); }
ins = (window.FroalaEditor && FroalaEditor.INSTANCES || []).filter(i => i.el && i.el.isConnected);
const det = ins[ins.length - 1];
if (ins.length < 2) throw new Error('detail editor missing');
det.html.set(DETAIL); det.undo && det.undo.saveStep(); det.events.trigger('contentChanged');
['input', 'keyup'].forEach(t => det.el.dispatchEvent(new Event(t, { bubbles: true })));
// 10. SEO
const seoHd = deep(sr, e => e.getAttribute && e.getAttribute('role') === 'button' && /^SEO\(검색엔진 최적화\)/.test((e.textContent || '').trim()))[0];
if (seoHd && seoHd.getAttribute('aria-expanded') !== 'true') { seoHd.click(); await sleep(800); }
const st = deep(sr, e => e.tagName === 'INPUT' && /상품명과 동일하게/.test(e.placeholder || ''))[0];
const sd = deep(sr, e => e.tagName === 'TEXTAREA' && /상품 상세에 입력한/.test(e.placeholder || ''))[0];
if (st) setVal(st, SEO_T); if (sd) setVal(sd, SEO_D);
const lab = deep(sr, e => e.tagName === 'LABEL' && /검색엔진에서 제외/.test(e.textContent))[0];
const sw = lab && lab.parentElement.querySelector('[role=switch]');
if (sw && sw.getAttribute('aria-checked') !== 'true') { sw.click(); await sleep(300); }
// 확인
const okName = deep(sr, e => e.placeholder === '상품명을 입력해 주세요.')[0].value === NAME;
const okPrice = p0[0].value.replace(/,/g, '') === String(A);
const okCat = deep(sr, e => e.tagName === 'BUTTON' && (e.textContent || '').trim().startsWith('컨설팅')).length > 0;
const okDisc = ['쇼핑 등급 할인', '쿠폰 할인'].every(t => { const cb = deep(sr, e => e.tagName === 'INPUT' && e.type === 'checkbox' && e.closest('label') && e.closest('label').textContent.trim() === t)[0]; return cb && !cb.checked; });
const okFile = deep(sr, e => e.children.length === 0 && /결제-안내\.png/.test(e.textContent || '')).length + deep(sr, e => /결제-안내\.png\d/.test(e.textContent || '') && e.children.length < 3).length > 0;
const okImg = deep(sr, e => e.tagName === 'IMG' && vis(e) && /cdn/.test(e.getAttribute('src') || '')).length > 0;
const okSeo = sw && sw.getAttribute('aria-checked') === 'true' && st && st.value === SEO_T;
const okText = ins[0].html.get().length > 40 && det.html.get().length > 2000;
const ok = { okName, okPrice, okCat, okDisc, okFile, okImg, okSeo, okText };
const all = Object.values(ok).every(Boolean);
if (!SUBMIT || !all) return { A, log, ok, submitted: false };
const sub = deep(sr, e => e.tagName === 'BUTTON' && (e.textContent || '').trim() === '상품 등록 완료')[0];
sub.click();
for (let i = 0; i < 40 && !/\/admin\/shopping\/product\/?$/.test(location.pathname); i++) await sleep(500);
await sleep(1500);
let first = null;
for (let i = 0; i < 20 && !first; i++) {
  const h = document.querySelector('bo-shopping-product') || document.querySelector('bo-shopping-product-list');
  const txt = deep(document, e => e.children.length === 0 && /^\[성균관컨설팅\] 논문 컨설팅 결제/.test((e.textContent || '').trim())).map(e => e.textContent.trim());
  if (txt.length) first = txt[0];
  else await sleep(500);
}
const idxs = deep(document, e => e.children.length === 0 && /^\d{3}$/.test((e.textContent || '').trim()) && vis(e)).map(e => +e.textContent.trim());
return { A, log, ok, submitted: true, url: location.pathname, first, topIdx: idxs.length ? Math.max.apply(null, idxs) : null };
