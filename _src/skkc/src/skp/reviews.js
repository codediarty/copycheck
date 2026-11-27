/* /reviews 후기 칸 머리말 · 거르기 · 더 보기, 마지막 권유 칸 옮기기(2026.11.27). 후기 글은 건드리지 않음 */
(function () {
  var W = document.getElementById('w202607080062baf8dd14f');
  var SEC = document.getElementById('s20260708d8aba9e23d417');
  var cta = document.getElementById('skpRvCta');
  if (cta && SEC && SEC.parentNode) SEC.parentNode.insertBefore(cta, SEC.nextSibling);
  if (!W) return;
  var list = W.querySelector('.skk-reviews');
  if (!list || list.getAttribute('data-skp')) return;
  list.setAttribute('data-skp', '1');
  var cards = [].slice.call(list.querySelectorAll('.skk-review-card'));
  var n = cards.length;
  var counts = document.querySelectorAll('.skp-rvcount');
  for (var c = 0; c < counts.length; c++) counts[c].textContent = n;
  function txt(card, sel) { var e = card.querySelector(sel); return e ? (e.textContent || '').replace(/\s+/g, ' ') : ''; }
  var BIZ = /기업|기관|스타트업|연구원|담당|기획자|대리|사업|정책|로드맵|평가 대응|카피클린|피드백/;
  var THESIS = /논문|학위|학술|SCI|KCI|통계|설문|입시/;
  var groups = { all: [], thesis: [], biz: [], verified: [] };
  for (var i = 0; i < n; i++) {
    var meta = txt(cards[i], '.skk-review-meta'), tag = txt(cards[i], '.skk-review-tag'), res = txt(cards[i], '.skk-review-result');
    groups.all.push(cards[i]);
    if (/거래 인증/.test(meta)) groups.verified.push(cards[i]);
    if (BIZ.test(meta + ' ' + tag + ' ' + res) && !/논문/.test(tag)) groups.biz.push(cards[i]);
    else if (THESIS.test(meta + ' ' + tag + ' ' + res)) groups.thesis.push(cards[i]);
  }
  var head = document.createElement('div');
  head.className = 'skp-rvhead';
  head.innerHTML = '<div><span class="skp-rvhead__eb">REAL REVIEWS</span><h2>고객이 직접 남긴 후기 <b>' + n + '</b>건</h2><p>개인정보 보호를 위해 이름은 가려서 표기했습니다.</p></div>' +
    '<div class="skp-rvf" role="group" aria-label="후기 거르기">' +
    '<button type="button" class="is-on" data-f="all" aria-pressed="true">전체 <i>' + groups.all.length + '</i></button>' +
    '<button type="button" data-f="thesis" aria-pressed="false">학위 · 학술 논문 <i>' + groups.thesis.length + '</i></button>' +
    '<button type="button" data-f="biz" aria-pressed="false">기업 · 기관 <i>' + groups.biz.length + '</i></button>' +
    '<button type="button" data-f="verified" aria-pressed="false">거래 인증 <i>' + groups.verified.length + '</i></button></div>';
  list.parentNode.insertBefore(head, list);
  var more = document.createElement('div');
  more.className = 'skp-rvmore';
  more.innerHTML = '<button type="button">후기 더 보기 <span></span></button>';
  list.parentNode.insertBefore(more, list.nextSibling);
  var STEP = 12, cur = 'all', shown = STEP;
  function render(animateFrom) {
    var g = groups[cur];
    for (var k = 0; k < n; k++) { cards[k].className = cards[k].className.replace(/\s*skp-rv-(off|new)/g, ''); }
    for (var k2 = 0; k2 < n; k2++) {
      var idx = g.indexOf(cards[k2]);
      if (idx < 0 || idx >= shown) cards[k2].className += ' skp-rv-off';
      else if (animateFrom !== undefined && idx >= animateFrom) cards[k2].className += ' skp-rv-new';
    }
    var left = g.length - Math.min(shown, g.length);
    more.className = 'skp-rvmore' + (left <= 0 ? ' is-done' : '');
    more.querySelector('span').textContent = '(' + Math.min(shown, g.length) + ' / ' + g.length + ')';
  }
  var btns = head.querySelectorAll('button');
  for (var b = 0; b < btns.length; b++) {
    btns[b].addEventListener('click', function () {
      for (var q = 0; q < btns.length; q++) { btns[q].className = ''; btns[q].setAttribute('aria-pressed', 'false'); }
      this.className = 'is-on'; this.setAttribute('aria-pressed', 'true');
      cur = this.getAttribute('data-f'); shown = STEP; render(0);
    });
  }
  more.querySelector('button').addEventListener('click', function () { var from = shown; shown += STEP; render(from); });
  render();
})();
