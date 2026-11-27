/* 성균관컨설팅 소개 페이지 공통 움직임(2026.11.27): 화면에 들어올 때 살짝 떠오르기, 숫자 올라가기.
   움직임을 줄이도록 설정한 기기에서는 모두 끔. 스크립트가 없으면 처음부터 다 보임. */
(function () {
  var roots = document.querySelectorAll('.skp');
  if (!roots.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canIO = 'IntersectionObserver' in window;
  function fmt(n, dec) {
    var s = dec ? n.toFixed(dec) : String(Math.round(n));
    var p = s.split('.');
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return p.join('.');
  }
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count'));
    var dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    var num = el.querySelector('.skp-num') || el;
    if (isNaN(to) || reduce) { return; }
    var start = null, dur = 1600;
    function step(ts) {
      if (start === null) start = ts;
      var t = Math.min(1, (ts - start) / dur);
      var e = 1 - Math.pow(1 - t, 3);
      num.textContent = fmt(to * e, dec);
      if (t < 1) window.requestAnimationFrame(step); else num.textContent = fmt(to, dec);
    }
    num.textContent = fmt(0, dec);
    window.requestAnimationFrame(step);
  }
  for (var r = 0; r < roots.length; r++) {
    var root = roots[r];
    if (root.getAttribute('data-skp-on')) continue;
    root.setAttribute('data-skp-on', '1');
    var items = root.querySelectorAll('[data-rv]');
    var counts = root.querySelectorAll('[data-count]');
    if (reduce || !canIO) continue;
    root.className += ' skp-js';
    var io = new IntersectionObserver(function (ents) {
      for (var i = 0; i < ents.length; i++) {
        if (ents[i].isIntersecting) { ents[i].target.className += ' rv-in'; io.unobserve(ents[i].target); }
      }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    for (var k = 0; k < items.length; k++) io.observe(items[k]);
    var co = new IntersectionObserver(function (ents) {
      for (var i = 0; i < ents.length; i++) {
        if (ents[i].isIntersecting) { countUp(ents[i].target); co.unobserve(ents[i].target); }
      }
    }, { threshold: 0.5 });
    for (var c = 0; c < counts.length; c++) co.observe(counts[c]);
  }
})();
