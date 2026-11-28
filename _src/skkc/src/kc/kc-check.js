/* 카피클린 AI 작성률 무료 검사(kc-check.js) 2026.11.28
   대표: 'aimarker 엔진을 동일하게 탑재 · 무료 검사 → 블라인드 → 결제 전환 · 여기서는 상담해서 견적(9,900원 같은 고정가 말고)'
   - 엔진: AIMarker 서버 am.style(mode check, tone auto, pass 없음) 그대로. 글을 6,000자씩 나누는 규칙 · 합치는 규칙 · 판정 숫자는 형제 사이트(humanize.js 13.45)와 같음
   - 무료 결과: AI 작성률 · 판정 · AI 패턴 문장 수 · 판정 근거는 보여 주고, 문장은 가장 뚜렷한 2개만 열고 나머지는 블라인드
   - 다음 단계: 결제 대신 채널톡 상담(검사 결과 · 문서 종류 · 마감 · 목표가 첫 메시지에 자동으로 들어감) → 크레딧 견적 → /copyclean-pricing
   - 파일은 이 브라우저 안에서 글만 꺼냄(AMTextIn, 카피체크와 같은 textin.js). 서버에는 검사할 글만 가고 저장하지 않음
   설정: window.KC_CFG = { api, demo, chatUrl, pricing, report, humanizer } 또는 쪽 안의 <div hidden data-kc-cfg="{…}">(아임웹: 글 칸 스크립트를 쪽 끝으로 옮기므로 설정은 속성으로)
         root · textin 이 있으면 body data-root 를 넣고 textin.js 를 그 주소에서 불러옴(카피체크 쪽 글 꺼내기 도구를 그대로 씀) */
(function () {
  'use strict';
  var CFG = window.KC_CFG || {};
  var API = CFG.api || '';
  function readCfg() {   /* 2026.11.28 배포판: 아임웹 쪽은 설정을 속성에서 읽음 */
    if (!window.KC_CFG) {
      var el = document.querySelector('[data-kc-cfg]');
      if (el) { try { CFG = JSON.parse(el.getAttribute('data-kc-cfg')) || {}; } catch (e) { CFG = {}; } }
    }
    API = CFG.api || '';
    var b = document.body;
    if (CFG.root && b && !b.getAttribute('data-root')) b.setAttribute('data-root', CFG.root);
    if (CFG.textin && !window.AMTextIn && !document.querySelector('script[src*="textin.js"]')) {
      var s = document.createElement('script'); s.src = CFG.textin; s.async = true; document.head.appendChild(s);
    }
  }
  var CHUNK = 6000, PAR = 4, MAXC = 200000, SHOW = 2;
  var J = { HI: 85, MID: 65, SHORT: 60, UNFIT_RATE: 40, RISK_RATE: 20, UNFIT_SEG: 50,
    B: { unfit: ['부적합', '부적합 · 개선 필요'], risk: ['고위험', '고위험 · 수정 권고'], safe: ['안전', '안전 · AI 패턴 적음'], short: ['판단 보류', '판단 보류 · 글이 짧음'] } };
  var SAMPLE = '본 연구는 생성형 인공지능의 확산이 대학 교육 현장에 미치는 영향을 분석하는 것을 목적으로 한다. 이를 위해 국내 대학생 312명을 대상으로 설문조사를 실시하였으며, 수집된 자료는 구조방정식 모형을 활용하여 분석하였다. 분석 결과, 생성형 인공지능의 활용 빈도는 학업 효능감에 유의미한 정적 영향을 미치는 것으로 나타났다. 또한 학업 효능감은 학습 몰입을 매개하여 학업 성취에 긍정적인 영향을 미치는 것으로 확인되었다. 이러한 결과는 대학 교육 현장에서 생성형 인공지능을 체계적으로 활용하기 위한 교육적 시사점을 제공한다는 점에서 의의가 있다.\n\n지난 학기에 나는 조별 과제를 하면서 처음으로 챗봇을 써 봤다. 솔직히 처음엔 신기했는데, 막상 답을 받아 보니 우리 조 주제랑 안 맞는 얘기가 많아서 결국 도서관에서 책을 다시 찾았다. 그래도 목차를 잡을 때는 꽤 도움이 됐다.';
  var Q = {
    doc: ['학위논문', '학술지 · 학회 논문', '과제 · 레포트', '자기소개서', '보고서 · 사업계획서', '기타'],
    due: ['24시간 안', '3일 안', '1주 안', '여유 있음'],
    goal: ['제출처 기준 맞추기', '최대한 낮게', '상담 후 결정']
  };
  var ICO = {
    file: '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 13H8"/><path d="M16 17H8"/>',
    up: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    x: '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    lock: '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    check: '<path d="m5 12 5 5L20 7"/>',
    arrow: '<path d="M5 12h14"/><path d="m13 6 6 6-6 6"/>',
    down: '<path d="M12 5v14"/><path d="m6 13 6 6 6-6"/>',
    chat: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8"/><path d="M8 13h5"/>',
    redo: '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    clip: '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    trash: '<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14H6L5 6"/>',
    scan: '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><path d="M7 12h10"/>',
    card: '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>',
    rpt: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 2 2 4-4"/>'
  };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var n2 = function (n) { return Number(n || 0).toLocaleString('ko-KR'); };
  function ico(n) { return '<svg class="kc-ico" viewBox="0 0 24 24" aria-hidden="true">' + (ICO[n] || '') + '</svg>'; }
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  function cid() {
    var c = '';
    try { c = localStorage.getItem('am_cid') || ''; if (!c) { c = 'w' + Math.random().toString(36).slice(2, 12); localStorage.setItem('am_cid', c); } }
    catch (e) { c = c || 'w' + Math.random().toString(36).slice(2, 12); }
    return c;
  }
  function canon(t) {
    if (window.AMTextIn && typeof window.AMTextIn.canon === 'function') return window.AMTextIn.canon(t);
    return String(t == null ? '' : t).replace(/\r\n?/g, '\n').replace(/[​-‍⁠﻿­]/g, '').replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  /* 글 나누기: 형제 사이트 humanize.js chunk 와 같은 규칙(같은 글은 언제나 같게) */
  function chunk(text) {
    var t = String(text).replace(/\r\n?/g, '\n'), parts = [];
    if (t.length <= CHUNK) return [t];
    var ps = t.split(/\n{2,}/), cur = '';
    var push = function (s) { if (!s.trim()) return; parts.push(s); };
    ps.forEach(function (p) {
      if (p.length > CHUNK) {
        if (cur) { push(cur); cur = ''; }
        var bits = p.match(/[^.!?。！？…\n]+[.!?。！？…]+["'”’)\]]*\s*|[^.!?。！？…\n]*\n|[^.!?。！？…\n]+$/g) || [p], c = '';
        bits.forEach(function (b) {
          if ((c + b).length > CHUNK && c) { push(c); c = ''; }
          if (b.length > CHUNK) { for (var i = 0; i < b.length; i += CHUNK) push(b.slice(i, i + CHUNK)); } else c += b;
        });
        if (c) push(c);
        return;
      }
      var add = cur ? cur + '\n\n' + p : p;
      if (add.length > CHUNK && cur) { push(cur); cur = p; } else cur = add;
    });
    if (cur) push(cur);
    return parts;
  }

  function post(body, ms) {
    var ctl = 'AbortController' in window ? new AbortController() : null;
    var t = ctl ? setTimeout(function () { ctl.abort(); }, ms || 120000) : 0;
    return fetch(API, { method: 'POST', body: JSON.stringify(body), redirect: 'follow', signal: ctl ? ctl.signal : undefined })
      .then(function (r) { return r.json(); })
      .finally(function () { if (t) clearTimeout(t); });
  }
  function checkPart(part, i) {
    var body = { action: 'am.style', _o: location.hostname, cid: cid(), ci: i, text: part, mode: 'check', tone: 'auto', pass: '' };
    var once = function () { return post(body, 120000).then(function (r) { if (!r || !r.ok) throw r || { message: '응답이 없어요. 잠시 뒤 다시 시도해 주세요.' }; return r; }); };
    return once().catch(function (e) { if (e && e.code) throw e; return new Promise(function (ok) { setTimeout(ok, 1200); }).then(once); });   /* 연결이 끊긴 경우만 한 번 더 */
  }
  function par(list, fn, step) {
    var res = new Array(list.length), next = 0, err = null, done = 0;
    function one() {
      if (err || next >= list.length) return Promise.resolve();
      var i = next++;
      return fn(list[i], i).then(function (r) { res[i] = r; done++; if (step) step(done, list.length); return one(); }, function (e) { err = err || e; });
    }
    var w = [];
    for (var k = 0; k < Math.min(PAR, list.length); k++) w.push(one());
    return Promise.all(w).then(function () { if (err) throw err; return res; });
  }

  /* 여러 조각 합치기(형제 사이트 merge · judge 와 같은 숫자) */
  function judge(s) {
    var why = [], mk = function (k, w) { return { key: k, ko: J.B[k][0], label: J.B[k][1], why: w }; };
    if (s.chars < J.SHORT) return mk('short', ['글자 수 ' + s.chars + '자(' + J.SHORT + '자 미만은 판단하지 않음)']);
    if (s.rate >= J.UNFIT_RATE) why.push('AI 작성률 ' + s.rate + '%(부적합 기준 ' + J.UNFIT_RATE + '% 이상)');
    if (s.segN >= 2 && s.segAi * 100 >= s.segN * J.UNFIT_SEG) why.push('AI 검출 구간 ' + s.segAi + '/' + s.segN + '구간(부적합 기준 전체 구간의 절반 이상)');
    if (s.chat >= 1) why.push('AI 대화창 흔적 ' + s.chat + '곳(부적합 기준 1곳 이상)');
    if (why.length) return mk('unfit', why);
    if (s.rate >= J.RISK_RATE) why.push('AI 작성률 ' + s.rate + '%(고위험 기준 ' + J.RISK_RATE + '% 이상)');
    if (s.segAi >= 1) why.push('AI 검출 구간 ' + s.segAi + '/' + s.segN + '구간(고위험 기준 1구간 이상)');
    if (s.hi + s.mid >= 1) why.push('AI 점수 ' + J.MID + ' 이상 문장 ' + (s.hi + s.mid) + '개(고위험 기준 1개 이상)');
    if (why.length) return mk('risk', why);
    return mk('safe', ['AI 작성률 ' + s.rate + '%(안전 기준 ' + J.RISK_RATE + '% 미만)', 'AI 검출 구간 없음', 'AI 점수 ' + J.MID + ' 이상 문장 없음']);
  }
  function whyFix(w) { return String(w || '').replace(/AI 가능성 중간 이상 문장/g, 'AI 점수 ' + J.MID + ' 이상 문장').replace(/^(AI 작성률 \d+%)\((\d+)% 미만\)$/, '$1(안전 기준 $2% 미만)'); }
  function merge(rs) {
    var M = { sentences: [], chars: 0, aiChars: 0, aiN: 0, n: 0, lv: { hi: 0, mid: 0, low: 0 }, segN: 0, segAi: 0, chat: 0, feat: {}, crit: '', critName: '' }, one = null;
    rs.forEach(function (r) {
      var d = r.ai || {};
      if (rs.length === 1) one = d;
      (d.sentences || []).forEach(function (s) { M.sentences.push({ t: s.t, p: s.p, g: s.g, ai: s.ai, lock: s.lock }); });
      M.chars += d.chars || 0; M.aiChars += d.aiChars || 0; M.aiN += d.aiN || 0; M.n += d.n || 0;
      if (d.lv) { M.lv.hi += d.lv.hi || 0; M.lv.mid += d.lv.mid || 0; M.lv.low += d.lv.low || 0; }
      M.segN += d.segN || 0; M.segAi += d.segAi || 0; M.chat += d.chat || 0;
      (d.feat || []).forEach(function (f) { var o = M.feat[f.cat] = M.feat[f.cat] || { cat: f.cat, name: f.name, lock: 1 }; if (!f.lock) o.lock = 0; });
      M.crit = d.crit || M.crit; M.critName = d.critName || M.critName;
    });
    M.rate = M.chars ? Math.round(M.aiChars / M.chars * 100) : 0;
    if (one && one.band) M.band = { key: one.band.key, ko: one.band.ko, label: one.band.label, why: (one.band.why || []).map(whyFix) };
    else M.band = judge({ chars: M.chars, rate: M.rate, segN: M.segN, segAi: M.segAi, chat: M.chat, hi: M.lv.hi, mid: M.lv.mid });
    var open = [];   /* 무료: 글 전체에서 가장 뚜렷한 2개만 열고 나머지는 블라인드 */
    M.sentences.forEach(function (s, i) { if (!s.lock && (s.g || s.ai)) open.push(i); });
    open.sort(function (a, b) { return (M.sentences[b].p || 0) - (M.sentences[a].p || 0) || a - b; });
    open.slice(SHOW).forEach(function (i) { M.sentences[i].lock = true; });
    M.open = open.slice(0, SHOW).sort(function (a, b) { return a - b; });
    M.feats = Object.keys(M.feat).map(function (k) { return M.feat[k]; });
    M.critName = String(M.critName || '').replace(/AIMarker/g, '카피클린');
    return M;
  }

  /* ---------- 화면 ---------- */
  var ST = { res: null, q: { doc: '', due: '', goal: '' }, name: '' };
  function bk(k) { return { unfit: 'u', risk: 'r', safe: 's' }[k] || 'n'; }
  function head(M) {
    var r = M.rate, k = M.band.key;
    if (k === 'unfit') return { h: 'AI 작성률 <em>' + r + '%</em>, 제출 전에 개선을 권해요', p: 'AI 작성 패턴이 많이 보여 제출처의 AI 검사에서도 높게 나올 수 있어요. 블라인드된 문장까지 전문 에디터가 짚어서 뜻은 그대로 두고 다듬어 드려요.' };
    if (k === 'risk') return { h: 'AI 작성률 <em>' + r + '%</em>, AI 패턴 문장부터 다듬어 보세요', p: '일부 구간에 AI 작성 패턴이 몰려 있어요. 표시된 문장을 중심으로 전문 에디터가 직접 다듬어 드려요.' };
    if (k === 'safe') return { h: 'AI 작성률 <em>' + r + '%</em>, 지금은 안전 구간이에요', p: '제출처 기준이 더 엄격하다면 남은 AI 패턴 문장까지 다듬어 둘 수 있어요. 필요한 만큼만 상담에서 정해요.' };
    return { h: '글이 짧아 판정하지 않았어요', p: J.SHORT + '자 이상, 가능하면 세 문장 이상 넣어 다시 검사해 주세요. 바로 상담으로 물어보셔도 돼요.' };
  }
  function judgeLine(M) {
    var k = M.band.key;
    if (k === 'unfit') return 'AI 작성 패턴이 많은 편이에요. 제출 전에 개선을 권해요.';
    if (k === 'risk') return '일부 구간에 AI 작성 패턴이 몰려 있어요. 표시된 문장을 중심으로 다듬는 것이 좋아요.';
    if (k === 'safe') return 'AI 작성 패턴이 적은 편이에요.';
    return '글이 짧으면 판정하지 않아요.';
  }
  function optsHtml(key) {
    return Q[key].map(function (v) { return '<button type="button" class="kc-opt" data-kc-q="' + key + '" data-v="' + esc(v) + '" aria-pressed="' + (ST.q[key] === v ? 'true' : 'false') + '">' + esc(v) + '</button>'; }).join('');
  }
  function render(M, box) {
    var c = bk(M.band.key), hd = head(M), locked = [], shown = [];
    M.sentences.forEach(function (s, i) { if (M.open.indexOf(i) >= 0) shown.push(i); });
    var aiHidden = Math.max(0, M.aiN - shown.length);
    M.sentences.forEach(function (s, i) { if (shown.indexOf(i) < 0 && locked.length < 5 && s.t) locked.push(s); });
    var sHtml = shown.map(function (i, k) { var s = M.sentences[i]; return '<li class="kc-s is-open"><span class="kc-s__n">' + (k + 1) + '</span><p><mark>' + esc(s.t) + '</mark></p><em>AI 점수 ' + (s.p || 0) + '</em></li>'; }).join('');
    var lHtml = locked.map(function (s, k) { return '<li class="kc-s"><span class="kc-s__n">' + (shown.length + k + 1) + '</span><p>' + esc(s.t) + '</p></li>'; }).join('');
    var openF = M.feats.filter(function (f) { return !f.lock; }), lockF = M.feats.length - openF.length;
    var why = (M.band.why || []).slice(0, 3).map(function (w) { return '<li>' + esc(w) + '</li>'; }).join('');
    var date = new Date();
    var dstr = date.getFullYear() + '.' + (date.getMonth() + 1) + '.' + date.getDate();
    box.innerHTML =
      '<div class="kc-res">' +
        '<div class="kc-res__hd"><div><span class="kc-eb">FREE REPORT</span><h2>AI 작성률 진단 결과</h2></div>' +
        '<button type="button" class="kc-res__again" data-kc-again>' + ico('redo') + '다른 글 검사</button></div>' +
        '<div class="kc-res__grid">' +
          '<article class="kc-rep kc-rise ' + 'is-' + c + '">' +
            '<div class="kc-rep__top"><span class="kc-rep__logo">' + ico('rpt') + '</span><div class="kc-rep__nm"><b>' + esc(ST.name || '붙여 넣은 글') + '</b><small>' + n2(M.chars) + '자 · 문장 ' + n2(M.n) + '개 · ' + dstr + '</small></div>' +
            (M.critName ? '<span class="kc-crit">' + esc(M.critName) + '</span>' : '') + '</div>' +
            '<div class="kc-rep__body">' +
              '<div class="kc-sum"><div class="kc-g" role="img" aria-label="AI 작성률 ' + M.rate + '퍼센트"><svg viewBox="0 0 188 188"><circle class="trk" cx="94" cy="94" r="80"/><circle class="val" cx="94" cy="94" r="80" data-kc-arc/></svg>' +
              '<div class="kc-g__c"><b><span data-kc-num>0</span><small>%</small></b><span>AI 작성률</span></div></div>' +
              '<div class="kc-judge"><span class="kc-pill">' + esc(M.band.ko) + '</span><h3>' + esc(M.band.label) + '</h3><p>' + esc(judgeLine(M)) + '</p>' +
              '<div class="kc-scale" aria-hidden="true"><i></i><i></i><i></i><em data-kc-mark style="left:0%"></em></div>' +
              '<div class="kc-scale__lb"><span>안전 0~19%</span><span>고위험 20~39%</span><span>부적합 40~100%</span></div></div></div>' +
              '<div class="kc-stats"><div class="kc-stat"><small>AI 패턴 문장</small><b>' + n2(M.aiN) + '<i>/ ' + n2(M.n) + '문장</i></b></div>' +
              '<div class="kc-stat"><small>AI 검출 구간</small><b>' + n2(M.segAi) + '<i>/ ' + n2(M.segN) + '구간</i></b></div>' +
              '<div class="kc-stat"><small>AI 패턴 유형</small><b>' + n2(M.feats.length) + '<i>가지</i></b></div></div>' +
              (why ? '<div class="kc-why"><b>판정 근거</b><ul>' + why + '</ul></div>' : '') +
              (M.n ? '<div class="kc-sents"><div class="kc-sents__hd"><b>AI 패턴 문장</b><span>' + shown.length + '개 공개 · ' + n2(aiHidden) + '개 블라인드</span></div>' +
                (sHtml ? '<ol class="kc-sl">' + sHtml + '</ol>' : '') +
                (lHtml ? '<div class="kc-lockwrap"><ol class="kc-sl" aria-hidden="true">' + lHtml + '</ol>' +
                  '<div class="kc-blind"><span class="kc-blind__ic">' + ico('lock') + '</span><b>AI 패턴 문장 ' + n2(aiHidden) + '개는 블라인드 처리됐어요</b>' +
                  '<p>어떤 문장을 어떻게 고칠지는 전문가 상담에서 개선 범위와 함께 안내해 드려요.</p>' +
                  '<button type="button" data-kc-chat="blind">' + ico('chat') + '전문가에게 개선 상담받기</button></div></div>' : '') +
              '</div>' : '') +
              (M.feats.length ? '<div class="kc-feat"><b>이 글에서 보인 AI 패턴</b>' + openF.map(function (f) { return '<span class="kc-chip">' + esc(f.name) + '</span>'; }).join('') +
                (lockF ? '<span class="kc-chip is-lock">' + ico('lock') + lockF + '가지 더</span>' : '') + '</div>' : '') +
              '<p class="kc-rep__note">AI 작성률은 문장마다 판별 모델이 매긴 AI 점수를 그 문장의 글자 수만큼 반영한 추정값이에요(가장 높아도 92%, 가장 낮아도 7%). 놓치는 AI 글을 줄이도록 엄격하게 재기 때문에 사람이 쓴 글도 높게 나올 수 있어, 결과만으로 글쓴이를 단정하지 마세요. 같은 글은 언제나 같은 값이 나오고, 검사기마다 기준이 달라 다른 검사기의 수치와는 다를 수 있어요.</p>' +
            '</div>' +
          '</article>' +
          '<aside class="kc-cta kc-rise" aria-label="전문가 개선 견적 상담">' +
            '<span class="kc-cta__eb">' + ico('chat') + '다음 단계 · 전문가 개선</span>' +
            '<h3>' + hd.h + '</h3><p>' + esc(hd.p) + '</p>' +
            '<ul class="kc-inc"><li>' + ico('check') + '블라인드된 AI 패턴 문장까지 전문 에디터가 직접 개선</li><li>' + ico('check') + '원문의 뜻 · 인용 · 전문 용어는 그대로</li><li>' + ico('check') + '개선 뒤 AI 작성률을 다시 검사해 함께 전달</li></ul>' +
            '<div class="kc-q"><div class="kc-q__t">견적 요청 메모<span>고르면 상담 창에 함께 들어가요</span></div>' +
              '<div class="kc-q__g"><b>문서 종류</b><div class="kc-q__opts">' + optsHtml('doc') + '</div></div>' +
              '<div class="kc-q__g"><b>희망 마감</b><div class="kc-q__opts">' + optsHtml('due') + '</div></div>' +
              '<div class="kc-q__g"><b>목표</b><div class="kc-q__opts">' + optsHtml('goal') + '</div></div></div>' +
            '<button type="button" class="kc-cta__go" data-kc-chat="cta">' + ico('chat') + '무료 견적 받기 · 채널톡 상담</button>' +
            '<p class="kc-cta__fine">검사 결과가 상담 창에 자동으로 들어가요. 분량 · 마감 · 목표를 보고 크레딧(1 크레딧 = 1만 원)으로 견적을 안내해요.</p>' +
            '<div class="kc-cta__as"><span>' + ico('shield') + '에스크로<br>안전결제</span><span>' + ico('clip') + '품질 검수<br>후 전달</span><span>' + ico('trash') + '작업 후<br>문서 폐기</span></div>' +
            '<div class="kc-cta__links">' +
              (CFG.pricing ? '<a href="' + esc(CFG.pricing) + '">견적을 이미 받았다면 크레딧 결제' + ico('arrow') + '</a>' : '') +
              (CFG.report ? '<a href="' + esc(CFG.report) + '">상세 결과서만 받기 · 5,500원' + ico('arrow') + '</a>' : '') +
            '</div>' +
          '</aside>' +
        '</div>' +
      '</div>' +
      '<div class="kc-dock" data-kc-dock><div class="kc-dock__v is-' + c + '"><b>' + M.rate + '%</b><small>' + esc(M.band.ko) + '</small></div><button type="button" data-kc-chat="dock">무료 견적 받기 · 상담</button></div>';
    box.hidden = false;
    var arc = $('[data-kc-arc]', box), num = $('[data-kc-num]', box), mark = $('[data-kc-mark]', box), L = 2 * Math.PI * 80;
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        if (arc) arc.style.setProperty('--kcd', (L * M.rate / 100).toFixed(1) + ' ' + L.toFixed(1));
        if (mark) mark.style.left = Math.max(1.5, Math.min(98.5, M.rate)) + '%';
        var t0 = performance.now(), D = 1100;
        (function tick(now) { var k = Math.min(1, (now - t0) / D), e = 1 - Math.pow(1 - k, 3); if (num) num.textContent = Math.round(M.rate * e); if (k < 1) requestAnimationFrame(tick); })(t0);
      });
    });
    setTimeout(function () {   /* 탭이 뒤에 있어 그림 갱신이 멈춘 경우에도 마지막 값은 꼭 보이게 */
      if (num) num.textContent = M.rate;
      if (arc) arc.style.setProperty('--kcd', (L * M.rate / 100).toFixed(1) + ' ' + L.toFixed(1));
      if (mark) mark.style.left = Math.max(1.5, Math.min(98.5, M.rate)) + '%';
    }, 1600);
    var dock = $('[data-kc-dock]', box), cta = $('.kc-cta__go', box), raf = 0;   /* 휴대폰: 결과를 보는 동안 상담 단추가 화면에 없으면 아래 고정 줄 */
    function dockPaint() {
      raf = 0; if (!dock || box.hidden) return;
      var vh = window.innerHeight, r = box.getBoundingClientRect(), c = cta ? cta.getBoundingClientRect() : null;
      var ctaIn = c && c.top < vh && c.bottom > 0;
      dock.classList.toggle('is-on', r.top < vh * 0.5 && r.bottom > vh * 0.4 && !ctaIn);
    }
    if (dock) { window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(dockPaint); }, { passive: true }); setTimeout(dockPaint, 700); }
  }

  /* ---------- 상담(채널톡) ---------- */
  function chatMsg() {
    var M = ST.res, L = [];
    if (CFG.demo) L.push('[데모 테스트]');
    if (M) {
      L.push('[카피클린 무료 검사 결과]');
      L.push('AI 작성률 ' + M.rate + '% · ' + M.band.ko);
      L.push('글자 수 ' + n2(M.chars) + '자 · AI 패턴 문장 ' + n2(M.aiN) + '/' + n2(M.n) + '개');
    }
    var q = [];
    if (ST.q.doc) q.push('문서 종류: ' + ST.q.doc);
    if (ST.q.due) q.push('희망 마감: ' + ST.q.due);
    if (ST.q.goal) q.push('목표: ' + ST.q.goal);
    if (q.length) L.push(q.join(' / '));
    L.push(M ? 'AI 작성률 개선 견적을 받고 싶어요.' : 'AI 작성률 개선 상담을 받고 싶어요.');
    return L.join('\n');
  }
  function toast(m) {
    var host = $('.kc') || document.body, t = document.createElement('div');
    t.className = 'kc-toast'; t.setAttribute('role', 'status'); t.textContent = m;
    host.appendChild(t); setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 3600);
  }
  function copyText(s) {
    try { if (navigator.clipboard) return navigator.clipboard.writeText(s); } catch (e) { /* 아래로 */ }
    var ta = document.createElement('textarea'); ta.value = s; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e2) { /* 그대로 */ }
    document.body.removeChild(ta);
  }
  function openChat(from) {
    var msg = chatMsg(), ok = false;
    try {
      if (typeof window.ChannelIO === 'function') {
        window.ChannelIO('openChat', undefined, msg); ok = true;
        try { window.ChannelIO('track', 'KcConsult', { from: from || '', rate: ST.res ? ST.res.rate : -1, band: ST.res ? ST.res.band.key : '' }); } catch (e1) { /* 그대로 */ }
      }
    } catch (e) { ok = false; }
    if (!ok) { copyText(msg); window.open(CFG.chatUrl || 'https://skcdesk.channel.io/home', '_blank', 'noopener'); toast('검사 결과를 복사했어요. 상담 창에 붙여 넣어 주세요.'); }
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-kc-chat]');
    if (b) { e.preventDefault(); openChat(b.getAttribute('data-kc-chat')); return; }
    var o = e.target.closest && e.target.closest('[data-kc-q]');
    if (o) {
      var key = o.getAttribute('data-kc-q'), v = o.getAttribute('data-v');
      ST.q[key] = ST.q[key] === v ? '' : v;
      $$('[data-kc-q="' + key + '"]').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-v') === ST.q[key] ? 'true' : 'false'); });
      return;
    }
    var top = e.target.closest && e.target.closest('a[href="#kcCheck"]');   /* 검사 칸으로 부드럽게 올라가 글 칸에 바로 입력 */
    if (top) { var tl = document.getElementById('kcCheck'); if (tl) { e.preventDefault(); var y = tl.getBoundingClientRect().top + window.pageYOffset - 110; window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' }); setTimeout(function () { var x = $('[data-kc-ta]', tl); if (x && !x.closest('[hidden]')) { try { x.focus({ preventScroll: true }); } catch (er) { x.focus(); } } }, 650); } return; }
    var a = e.target.closest && e.target.closest('a[href*="channel.io"]');   /* 쪽 안의 다른 상담 단추도 같은 상담 창으로(검사 결과가 있으면 함께) */
    if (a && typeof window.ChannelIO === 'function' && !e.ctrlKey && !e.metaKey && !e.shiftKey) { e.preventDefault(); openChat('link'); }
  });

  /* 글 꺼내기 도구(textin.js)가 늦게 올 수 있어 잠깐 기다림(배포판은 kc-check.js 가 불러옴) */
  function textIn() {
    return new Promise(function (ok, no) {
      var t0 = Date.now();
      (function wait() {
        if (window.AMTextIn && typeof window.AMTextIn.read === 'function') ok(window.AMTextIn);
        else if (Date.now() - t0 > 9000) no(new Error('파일을 여는 도구를 불러오지 못했어요. 글을 복사해 붙여 넣어 주세요.'));
        else setTimeout(wait, 150);
      })();
    });
  }

  /* ---------- 검사 칸 ---------- */
  function init(tool) {
    var ta = $('[data-kc-ta]', tool), go = $('[data-kc-go]', tool), cnt = $('[data-kc-count]', tool), inp = $('[data-kc-in]', tool), pick = $('[data-kc-pick]', tool);
    var fileEl = $('[data-kc-file]', tool), busyEl = $('[data-kc-busy]', tool), errEl = $('[data-kc-err]', tool), runEl = $('[data-kc-run]', tool), doneEl = $('[data-kc-done]', tool), body = $('[data-kc-body]', tool);
    var resBox = document.getElementById(tool.getAttribute('data-kc-res') || 'kcRes');
    var busy = false, src = null;
    function err(m) { if (!errEl) return; errEl.textContent = m || ''; errEl.hidden = !m; }
    function count() {
      var n = canon(ta.value).length;
      cnt.textContent = n2(n) + '자' + (n && n < J.SHORT ? ' · ' + J.SHORT + '자부터 검사' : '');
      cnt.classList.toggle('is-ok', n >= J.SHORT);
      go.disabled = busy || n < J.SHORT;
    }
    function chip() {
      if (!fileEl) return;
      if (!src) { fileEl.hidden = true; fileEl.innerHTML = ''; return; }
      fileEl.hidden = false;
      fileEl.innerHTML = '<span class="kc-file__ic">' + ico('file') + '</span><span class="kc-file__nm"><b>' + esc(src.name) + '</b><small>' + esc(src.kindKo || '파일') + ' · ' + n2(src.chars) + '자 꺼냄' + (src.cut ? '(앞 20만 자까지)' : '') + '</small></span><button type="button" class="kc-file__x" data-kc-unfile aria-label="올린 파일 빼기">' + ico('x') + '</button>';
    }
    function takeFile(f) {
      if (!f || busy) return;
      err('');
      busyEl.hidden = false; $('span', busyEl).textContent = '“' + String(f.name || '파일').slice(0, 30) + '”에서 글을 꺼내는 중';
      textIn().then(function (T) { return T.read(f); }).then(function (r) {
        busyEl.hidden = true;
        var t = r.text || '', cut = 0;
        if (t.length > MAXC) { var k = t.lastIndexOf('\n\n', MAXC); cut = k > MAXC * 0.6 ? k : MAXC; }
        ta.value = cut ? t.slice(0, cut) : t;
        src = { name: String(f.name || '파일').slice(0, 80), kindKo: r.kindKo, chars: t.length, cut: !!cut };
        ST.name = src.name; chip(); count();
      }).catch(function (e) { busyEl.hidden = true; err((e && e.message) || '파일에서 글을 꺼내지 못했어요. 글을 복사해 붙여 넣어 주세요.'); });
    }
    ta.addEventListener('input', function () { if (src && !ta.value) { src = null; ST.name = ''; chip(); } count(); });
    if (pick) pick.addEventListener('change', function () { takeFile(pick.files && pick.files[0]); pick.value = ''; });
    tool.addEventListener('click', function (e) {
      if (e.target.closest('[data-kc-unfile]')) { src = null; ST.name = ''; ta.value = ''; chip(); count(); ta.focus(); }
      if (e.target.closest('[data-kc-sample]')) { src = null; ST.name = '예시 글(논문 서론 · 일기)'; chip(); ta.value = SAMPLE; count(); }
      if (e.target.closest('[data-kc-new]')) { reset(); }
      if (e.target.closest('[data-kc-view]') && resBox) { scrollTo(resBox); }
    });
    ['dragenter', 'dragover'].forEach(function (ev) { inp.addEventListener(ev, function (e) { e.preventDefault(); if (!busy) inp.classList.add('is-drag'); }); });
    ['dragleave', 'dragend'].forEach(function (ev) { inp.addEventListener(ev, function (e) { if (e.target === inp || !inp.contains(e.relatedTarget)) inp.classList.remove('is-drag'); }); });
    inp.addEventListener('drop', function (e) { e.preventDefault(); inp.classList.remove('is-drag'); var f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]; if (f) takeFile(f); });
    if (resBox) resBox.addEventListener('click', function (e) { if (e.target.closest('[data-kc-again]')) { reset(); scrollTo(tool, true); } });

    function reset() {
      ST.res = null; src = null; ST.name = ''; ta.value = ''; chip(); err('');
      if (doneEl) doneEl.hidden = true; if (body) body.hidden = false;
      if (resBox) { resBox.hidden = true; resBox.innerHTML = ''; }
      count(); setTimeout(function () { try { ta.focus(); } catch (e) { /* 그대로 */ } }, 60);
    }
    function scrollTo(el, center) {
      var y = el.getBoundingClientRect().top + window.pageYOffset - (center ? 120 : 76);
      window.scrollTo({ top: Math.max(0, y), behavior: 'smooth' });
    }

    /* 진행 화면 */
    var R = { shown: 0, target: 0, timer: 0 };
    function runSet(stepNo, partTxt) {
      $$('[data-s]', runEl).forEach(function (li) { var s = +li.getAttribute('data-s'); li.className = s < stepNo ? 'is-done' : s === stepNo ? 'is-on' : ''; });
      var sm = $('[data-kc-part]', runEl); if (sm) sm.textContent = partTxt || '';
    }
    function runPaint() {
      var c = $('.val', runEl), b = $('[data-kc-pct]', runEl);
      if (c) c.style.setProperty('--kcr', (3.02 * R.shown).toFixed(1) + ' 302');
      if (b) b.innerHTML = Math.round(R.shown) + '<small>%</small>';
    }
    function runStart(total) {
      runEl.hidden = false; R.shown = 0; R.target = 12; runSet(1, ''); runPaint();
      clearInterval(R.timer);
      R.timer = setInterval(function () { if (R.shown < R.target) R.shown = Math.min(R.target, R.shown + Math.max(0.4, (R.target - R.shown) * 0.08)); else if (R.target < 92) R.target += 0.25; runPaint(); }, 60);
      setTimeout(function () { if (!runEl.hidden) { runSet(2, total > 1 ? '0/' + total + ' 구간' : ''); R.target = Math.max(R.target, 22); } }, 650);
    }
    function runStep(done, total) { R.target = Math.max(R.target, 22 + 62 * done / total); runSet(2, total > 1 ? done + '/' + total + ' 구간' : ''); }
    function runEnd(ok) {
      return new Promise(function (res) {
        if (!ok) { clearInterval(R.timer); runEl.hidden = true; res(); return; }
        runSet(3, ''); R.target = 100;
        setTimeout(function () { R.shown = 100; runPaint(); runSet(4, ''); setTimeout(function () { clearInterval(R.timer); runEl.hidden = true; res(); }, 420); }, 520);
      });
    }

    go.addEventListener('click', function () {
      var t = canon(ta.value);
      if (busy || t.length < J.SHORT) return;
      if (!API) { err('검사 서버 주소가 없어요.'); return; }
      if (t.length > MAXC) { var k = t.lastIndexOf('\n\n', MAXC); t = t.slice(0, k > MAXC * 0.6 ? k : MAXC); }
      busy = true; err(''); go.disabled = true;
      var parts = chunk(t);
      runStart(parts.length);
      par(parts, checkPart, function (d, n) { runStep(d, n); }).then(function (rs) {
        var M = merge(rs);
        ST.res = M;
        return runEnd(true).then(function () {
          busy = false;
          if (body) body.hidden = true;
          if (doneEl) {
            doneEl.hidden = false;
            doneEl.innerHTML = '<span class="kc-pill is-' + bk(M.band.key) + '">' + esc(M.band.ko) + '</span><span class="kc-done__v is-' + bk(M.band.key) + '" style="color:var(--kcb)">' + M.rate + '<small>%</small></span>' +
              '<p>AI 작성률 검사를 마쳤어요. 결과와 다음 단계를 아래에서 확인하세요.</p>' +
              '<div class="kc-done__row"><button type="button" class="kc-btn2 kc-btn2--g" data-kc-view>' + ico('down') + '결과 보기</button><button type="button" class="kc-btn2 kc-btn2--w" data-kc-new>' + ico('redo') + '다른 글 검사</button></div>';
          }
          if (resBox) { render(M, resBox); setTimeout(function () { scrollTo(resBox); }, 80); }
          try { if (typeof window.ChannelIO === 'function') window.ChannelIO('track', 'KcFreeCheck', { rate: M.rate, band: M.band.key, chars: M.chars }); } catch (e) { /* 그대로 */ }
        });
      }).catch(function (e) {
        runEnd(false).then(function () {
          busy = false; count();
          var m = (e && e.message) || '';
          if (e && e.name === 'AbortError') m = '응답이 늦어 멈췄어요. 잠시 뒤 다시 시도해 주세요.';
          err(m || '검사하지 못했어요. 잠시 뒤 다시 시도해 주세요.');
        });
      });
    });
    count();
  }
  function boot() { readCfg(); $$('[data-kc-tool]').forEach(init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
