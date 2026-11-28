/* 아임웹 바로 결제 상품 205~244 이름을 '전문가 컨설팅'으로 고치는 도우미(2026.11.28 10:42 대표 '논문 컨설팅만 하는 게 아니니 전문가 컨설팅으로').
   상품 수정 화면(/admin/shopping/product/detail?idx=N&product-type=digital)에서 new Function("IDX","IMG","FILE","SUBMIT", 이 글) 로 실행.
   이름 · 대표 그림 · 요약 · 상세 · SEO 제목과 설명 · 내려받는 안내 파일을 바꿈(판매가 · 할인 · 카테고리 · 검색 제외는 그대로).
   10:44 대표 '결과물 받기 전에는 전문가에게 금액이 가지 않고 성균관컨설팅이 안전하게 보관'도 요약 · 상세 · SEO 설명에 넣음
   10:59 대표 '모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달됩니다'도 요약 · 상세에 */
const RAW = 'https://raw.githubusercontent.com/codediarty/copycheck/__COMMIT__/_src/skkc/shop/';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const deep = (root, pred, out = []) => { for (const e of root.querySelectorAll('*')) { if (pred(e)) out.push(e); if (e.shadowRoot) deep(e.shadowRoot, pred, out); } return out; };
const vis = e => e && e.getBoundingClientRect().width > 0;
if (!(IDX >= 205 && IDX <= 244)) return { IDX, err: 'range' };
if (!new RegExp('[?&]idx=' + IDX + '(&|$)').test(location.search)) return { IDX, err: 'wrong page ' + location.search };
const N = (IDX - 204) * 5;
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
const OK_OLD = ['[성균관컨설팅] 논문 컨설팅 결제 (' + won + '원)', '[성균관컨설팅] 논문 컨설팅 ' + N + ' 크레딧'];
const NAME = '[성균관컨설팅] 전문가 컨설팅 ' + N + ' 크레딧';
if (OK_OLD.indexOf(nameEl.value) < 0 && nameEl.value !== NAME) return { IDX, err: 'unexpected name', name: nameEl.value };
const priceEl = deep(sr, e => e.tagName === 'INPUT' && e.placeholder === '0' && vis(e))[0];
if (!priceEl || priceEl.value.replace(/[^0-9]/g, '') !== String(A)) return { IDX, err: 'price mismatch', price: priceEl && priceEl.value };

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
async function fileOf(name, saveAs, type) {
  const b = await fetch(RAW + name, { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error('fetch ' + name + ' ' + r.status); return r.blob(); });
  return new File([b], saveAs, { type });
}

const SAFE = '결과물을 받기 전까지 결제금은 전문가에게 가지 않고 성균관컨설팅이 안전하게 보관해요.';
const SUM = '<p>성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 전문가 컨설팅 상품입니다. 결과물을 받기 전까지 결제금은 성균관컨설팅이 안전하게 보관하고, 모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달됩니다.</p>';
const QA = '모든 작업물은 내부 품질 검수 기준을 충족한 후 최종 전달돼요.';
const TD = 'width:46px;padding:14px 0;vertical-align:top;font-size:15px;font-weight:800;color:#175df6;';
const row = (no, t, d, last) => '<tr><td style="' + TD + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '">' + no + '</td><td style="padding:14px 0;' + (last ? '' : 'border-bottom:1px solid #eef2f6;') + '"><strong style="font-size:16px;color:#0f172a;">' + t + '</strong><br><span style="font-size:15px;color:#475569;">' + d + '</span></td></tr>';
const DETAIL = '<div style="max-width:760px;margin:0 auto;font-family:\'Pretendard Variable\',Pretendard,-apple-system,BlinkMacSystemFont,sans-serif;color:#0f172a;line-height:1.7;word-break:keep-all;">'
 + '<p style="margin:0 0 6px;font-size:13px;font-weight:800;letter-spacing:0.14em;color:#175df6;">SKKC · 전문가 컨설팅</p>'
 + '<h2 style="margin:0;font-size:28px;font-weight:800;letter-spacing:-0.03em;color:#0f172a;">전문가 컨설팅 결제 · ' + N + ' 크레딧</h2>'
 + '<p style="margin:12px 0 0;font-size:16px;color:#475569;">성균관컨설팅 1:1 상담에서 안내받은 크레딧을 결제하는 전문가 컨설팅 상품입니다. 결제와 영수증은 성균관컨설팅 이름으로 처리됩니다.</p>'
 + '<div style="margin:22px 0 0;padding:16px 20px;border-radius:16px;background:#eef4ff;border:1px solid #d6e3fb;"><p style="margin:0;font-size:16px;font-weight:800;color:#0f2a6b;">에스크로 안전결제</p><p style="margin:4px 0 0;font-size:15px;color:#334155;">' + SAFE + '</p><p style="margin:12px 0 0;font-size:16px;font-weight:800;color:#0f2a6b;">품질 검수 후 전달</p><p style="margin:4px 0 0;font-size:15px;color:#334155;">' + QA + '</p></div>'
 + '<div style="margin:16px 0 0;padding:22px 24px;border-radius:18px;background:#f5f8fd;border:1px solid #e2e8f0;"><p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#0f172a;">이럴 때 결제해요</p><p style="margin:0;font-size:15px;color:#334155;">✓ 1:1 상담에서 작업 범위 · 납기일과 함께 안내받은 크레딧<br>✓ 진행 중 범위가 늘어 추가로 안내받은 크레딧</p></div>'
 + '<p style="margin:30px 0 4px;font-size:17px;font-weight:800;color:#0f172a;">결제하는 법</p><table style="width:100%;border-collapse:collapse;"><tbody>'
 + row('01', '크레딧 안내', '1:1 상담에서 작업 범위 · 납기일 · 크레딧을 함께 정해요.')
 + row('02', '같은 크레딧 결제', '안내받은 크레딧과 같은 상품(' + N + ' 크레딧)으로 결제해요.')
 + row('03', '결제 확인', '상담 채팅에 결제하신 분 성함을 남겨 주시면 확인이 빨라요.')
 + row('04', '진행 · 전달', '전문가가 진행하고, 약속한 날짜까지 결과물을 이메일로 보내요.', true)
 + '</tbody></table>'
 + '<div style="margin:28px 0 0;padding:18px 20px;border-radius:14px;background:#ebf2ff;border:1px solid #d6e4ff;"><p style="margin:0;font-size:15px;color:#0b2a6e;"><strong>아직 상담 전이라면</strong> 먼저 <a href="https://skcdesk.channel.io/home" rel="noopener" style="color:#175df6;font-weight:700;" target="_blank">채팅 상담</a>으로 연락해 크레딧을 안내받아 주세요.</p></div>'
 + '<p style="margin:24px 0 0;font-size:13px;color:#94a3b8;">결제금은 결과물 전달이 끝날 때까지 성균관컨설팅이 보관하는 에스크로 방식입니다. 크레딧은 작업 범위 · 분량 · 일정에 따라 상담에서 정해지며, 취소와 환불은 성균관컨설팅 이용약관을 따릅니다. 성균관대학교 RISE 사업단 지원 · 한국AI윤리위원회 인증</p></div>';
const SEO_T = '전문가 컨설팅 ' + N + ' 크레딧 | 성균관컨설팅';
const SEO_D = '성균관컨설팅 1:1 상담에서 안내받은 전문가 컨설팅 크레딧을 결제하는 상품입니다. 결과물을 받기 전까지 결제금은 성균관컨설팅이 안전하게 보관합니다.';
const GUIDE_NAME = '성균관컨설팅-전문가컨설팅-결제-안내.png';
const log = [];

// 1. 대표 그림
if (IMG) {
  for (const d of deep(sr, e => e.tagName === 'BUTTON' && e.classList.contains('delete-button') && e.closest('.image-item'))) { d.click(); await sleep(500); }
  const fin = deep(sr, e => e.tagName === 'INPUT' && e.type === 'file' && /\.jpg/.test(e.accept || ''))[0];
  const f = await fileOf('ex-c' + N + '.jpg', 'ex-c' + N + '.jpg', 'image/jpeg');
  const dt = new DataTransfer(); dt.items.add(f); fin.files = dt.files; fin.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
  for (let i = 0; i < 40; i++) { await sleep(500); const im = deep(sr, e => e.tagName === 'IMG' && e.closest('.image-item')); if (im.length === 1 && /cdn/.test(im[0].getAttribute('src') || '')) break; }
  log.push('img ' + f.size);
}
// 2. 내려받는 안내 파일
const fileItem = () => deep(sr, e => e.getAttribute && e.getAttribute('role') === 'listitem' && /결제-안내/.test(e.textContent || ''));
if (FILE) {
  const items = fileItem();
  if (!(items.length === 1 && /전문가컨설팅-결제-안내/.test(items[0].textContent))) {
    for (const d of deep(sr, e => e.tagName === 'BUTTON' && e.getAttribute('aria-label') === '파일 삭제')) { d.click(); await sleep(700); }
    let din = null;
    for (let i = 0; i < 20 && !din; i++) { din = deep(sr, e => e.tagName === 'INPUT' && e.type === 'file' && !/\.jpg/.test(e.accept || ''))[0]; if (!din) await sleep(300); }
    if (!din) return { IDX, N, log, err: 'no digital file input' };
    const g = await fileOf('ex-guide.png', GUIDE_NAME, 'image/png');
    const dt = new DataTransfer(); dt.items.add(g); din.files = dt.files; din.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
    for (let i = 0; i < 60; i++) { await sleep(500); const it = fileItem(); if (it.length === 1 && /전문가컨설팅-결제-안내/.test(it[0].textContent)) break; }
    log.push('file ' + g.size);
  }
}
// 3. 상품명 · 4. 요약 · 5. 상세
setVal(nameEl, NAME);
let ins = live();
setFroala(ins[0], SUM);
setFroala(ins[ins.length - 1], DETAIL);
// 6. SEO
const seoHd = deep(sr, e => e.getAttribute && e.getAttribute('role') === 'button' && /^SEO\(검색엔진 최적화\)/.test((e.textContent || '').trim()))[0];
if (seoHd && seoHd.getAttribute('aria-expanded') !== 'true') { seoHd.click(); await sleep(800); }
const st = deep(sr, e => e.tagName === 'INPUT' && /상품명과 동일하게/.test(e.placeholder || ''))[0];
const sd = deep(sr, e => e.tagName === 'TEXTAREA' && /상품 상세에 입력한/.test(e.placeholder || ''))[0];
if (st) setVal(st, SEO_T); if (sd) setVal(sd, SEO_D);
await sleep(400);
// 확인
ins = live();
const imgs = deep(sr, e => e.tagName === 'IMG' && e.closest('.image-item'));
const fi = fileItem();
const txt = h => { const d = document.createElement('div'); d.innerHTML = h; return d.textContent; };
const ok = {
  name: nameEl.value === NAME,
  img: imgs.length === 1 && /cdn/.test(imgs[0].getAttribute('src') || ''),
  file: fi.length === 1 && (!FILE || /전문가컨설팅-결제-안내/.test(fi[0].textContent)),
  sum: ins[0].html.get().indexOf('전문가 컨설팅 상품') > 0 && ins[0].html.get().indexOf('내부 품질 검수') > 0 && ins[0].html.get().indexOf('논문') < 0,
  det: txt(ins[ins.length - 1].html.get()).indexOf('전문가 컨설팅 결제 · ' + N + ' 크레딧') >= 0 && txt(ins[ins.length - 1].html.get()).indexOf('에스크로 안전결제') >= 0 && txt(ins[ins.length - 1].html.get()).indexOf('품질 검수 후 전달') >= 0 && ins[ins.length - 1].html.get().indexOf('논문') < 0 && ins[ins.length - 1].html.get().indexOf(won) < 0,
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
