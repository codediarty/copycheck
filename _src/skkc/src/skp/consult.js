/* 컨설팅 소개 쪽 공통(2026.11.28): '맞춤 상담 요청하기' 단추는 아래 상담 신청 칸으로 부드럽게 이동(위 고정 머리글 높이만큼 덜 내려감),
   자주 묻는 질문 첫 칸은 펼쳐 둠. 아임웹 폼은 건드리지 않음 */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function headH() {
    var h = document.getElementById('sgkHeader');
    if (!h) return 0;
    var r = h.getBoundingClientRect();
    return r.bottom > 0 ? r.height : 0;
  }
  var go = document.querySelectorAll('.skp [data-skp-go]');
  for (var i = 0; i < go.length; i++) {
    if (go[i].getAttribute('data-skp-on')) continue;
    go[i].setAttribute('data-skp-on', '1');
    go[i].addEventListener('click', function (e) {
      var id = (this.getAttribute('href') || '').replace('#', '');
      var t = id ? document.getElementById(id) : null;
      if (!t) return;
      e.preventDefault();
      var y = t.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop) - headH() + 30;
      if (reduce || !('scrollBehavior' in document.documentElement.style)) window.scrollTo(0, y);
      else window.scrollTo({ top: y, behavior: 'smooth' });
    });
  }
  var lists = document.querySelectorAll('.skp .skp-faq');
  for (var k = 0; k < lists.length; k++) {
    var q = lists[k].querySelector('.skp-faq__q');
    if (q && !lists[k].getAttribute('data-skp-on')) { lists[k].setAttribute('data-skp-on', '1'); q.open = true; }
  }
})();
