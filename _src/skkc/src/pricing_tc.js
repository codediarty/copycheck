(function () {
  var root = document.getElementById('spcPay');
  if (!root || root.getAttribute('data-on')) return;
  root.setAttribute('data-on', '1');
  root.classList.add('is-js');
  var tabs = root.querySelectorAll('.spc-pay__tab'), grids = root.querySelectorAll('.spc-pay__grid');
  for (var i = 0; i < tabs.length; i++) tabs[i].addEventListener('click', function () {
    var g = this.getAttribute('data-g');
    for (var j = 0; j < tabs.length; j++) { var on = tabs[j].getAttribute('data-g') === g; tabs[j].classList.toggle('is-on', on); tabs[j].setAttribute('aria-pressed', on ? 'true' : 'false'); }
    for (var k = 0; k < grids.length; k++) grids[k].classList.toggle('is-on', grids[k].getAttribute('data-g') === g);
  });
})();
