/* 학술정보 예전 글 모양 정리(2026.11.27). 저장된 글은 바꾸지 않고, 화면에 보일 때만 이름표(ac-*)를 붙임.
   - 빈 줄 문단(<p><br></p>)은 숨기고, 빈 줄 없이 이어진 줄은 한 덩어리로 붙여 보이게(ac-tight)
   - '■ 제목' 줄은 소제목(ac-h), '하나. ' · '1단계. ' 같은 줄은 작은 제목(ac-h3)
   - '- ' 줄은 점 목록(ac-li), '1. ' 줄은 번호 목록(ac-num), 따옴표로만 된 줄은 인용(ac-q)
   - '… → 주소' 줄은 단추 모양(ac-cta), '#태그' 줄은 칩(ac-tags) */
(function () {
  var WID = 'w20260818cbad0e3273d77';
  function clean(s) { return (s || '').replace(/ /g, ' ').replace(/\s+/g, ' ').trim(); }
  function firstText(p) {
    var n = p.firstChild;
    while (n && n.nodeType === 3 && !n.nodeValue.replace(/ /g, ' ').trim()) n = n.nextSibling;
    return n && n.nodeType === 3 ? n : null;
  }
  function cut(p, re) { var n = firstText(p); if (n) n.nodeValue = n.nodeValue.replace(re, ''); }
  function boldLabel(p) {
    var n = firstText(p); if (!n) return;
    var m = n.nodeValue.match(/^\s*([^:：—]{2,26}?)\s+(:|：|—)\s+/);
    if (!m) return;
    var s = document.createElement('strong'); s.textContent = m[1];
    n.nodeValue = ' ' + n.nodeValue.slice(m[0].length);
    p.insertBefore(s, n);
  }
  function isGap(p) { return p.tagName === 'P' && !clean(p.textContent) && !p.querySelector('img,iframe,video,table'); }
  function run() {
    var w = document.getElementById(WID); if (!w) return;
    var box = w.querySelector('.board_view .board_txt_area > div');
    if (!box || box.getAttribute('data-ac')) return;
    box.setAttribute('data-ac', '1');
    var kids = [], i, p, t;
    for (i = 0; i < box.children.length; i++) kids.push(box.children[i]);
    var gaps = 0, squares = 0;
    for (i = 0; i < kids.length; i++) {
      if (isGap(kids[i])) gaps++;
      else if (/^■/.test(clean(kids[i].textContent))) squares++;
    }
    var semantic = !!box.querySelector('h1,h2,h3,h4,ul,ol,blockquote,table');
    var lineMode = gaps >= 3;
    for (i = 0; i < kids.length; i++) {
      p = kids[i];
      if (p.tagName !== 'P') continue;
      if (isGap(p)) { p.className += ' ac-gap'; continue; }
      if (p.children.length && p.querySelector('img,iframe,video,table')) continue;
      t = clean(p.textContent);
      var next = kids[i + 1];
      if (lineMode && next && next.tagName === 'P' && !isGap(next)) p.className += ' ac-tight';
      if (/^■/.test(t)) { cut(p, /^\s*■\s*/); p.className += ' ac-h'; continue; }
      if (!squares && !semantic && t.length <= 32 && /^\d{1,2}\.\s/.test(t) && !/[.!?다요]$/.test(t)) { p.className += ' ac-h'; continue; }
      if (/^\d{1,2}단계\.\s/.test(t) && t.length <= 40) { p.className += ' ac-h3'; continue; }
      if (/^(하나|둘|셋|넷|다섯)\.\s/.test(t) && t.length <= 60) { p.className += ' ac-h3'; continue; }
      if (!semantic && /^(첫째|둘째|셋째|넷째|다섯째),\s/.test(t) && t.length <= 26 && !/[.!?다요]$/.test(t)) { p.className += ' ac-h3'; continue; }
      if (/^#\S/.test(t) && (t.match(/#[^\s#]+/g) || []).length >= 2 && !p.querySelector('a')) {
        var tags = t.match(/#[^\s#]+/g); p.textContent = '';
        for (var k = 0; k < tags.length; k++) { var sp = document.createElement('span'); sp.textContent = tags[k]; p.appendChild(sp); p.appendChild(document.createTextNode(' ')); }
        p.className += ' ac-tags'; continue;
      }
      var as = p.querySelectorAll('a');
      if (as.length === 1 && /→/.test(t) && /^https?:/.test(clean(as[0].textContent))) {
        var label = clean(t.split('→')[0]);
        if (label && label.length <= 40) { var a = as[0]; a.textContent = label; p.textContent = ''; p.appendChild(a); p.className += ' ac-cta'; continue; }
      }
      if (/^[-–•·]\s/.test(t)) { cut(p, /^\s*[-–•·]\s*/); boldLabel(p); p.className += ' ac-li'; continue; }
      var mn = t.match(/^(\d{1,2})\.\s/);
      if (mn) { cut(p, /^\s*\d{1,2}\.\s*/); p.setAttribute('data-n', mn[1]); boldLabel(p); p.className += ' ac-num'; continue; }
      if (/^["“].{2,}["”]$/.test(t) && t.length <= 90) { p.className += ' ac-q'; continue; }
      p.setAttribute('data-acp', '1');
    }
    /* 빈 줄 없이 이어진 짧은 줄 3개 이상(끝맺음 · '이름: 값' · 주소 없음)은 점 목록으로 */
    if (!lineMode) return;
    var run = [];
    function flush() {
      var ok = run.length >= 3;
      for (var r = 0; ok && r < run.length; r++) {
        var s = clean(run[r].textContent);
        if (s.length > 30 || /[.!?다요:]$/.test(s) || /:\s|：|https?:|@|www\./.test(s)) ok = false;
      }
      for (r = 0; ok && r < run.length; r++) run[r].className += ' ac-li';
      run = [];
    }
    for (i = 0; i < kids.length; i++) {
      p = kids[i];
      if (p.tagName === 'P' && p.getAttribute('data-acp')) { run.push(p); p.removeAttribute('data-acp'); }
      else flush();
    }
    flush();
  }
  run();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
})();
