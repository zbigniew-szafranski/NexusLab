// nexuslab.pl homepage: mobile menu, portfolio filter, "show all" buttons, lazy demo videos.
(function () {
  'use strict';

  var burger = document.getElementById('nav-burger');
  var drawer = document.getElementById('nav-drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    drawer.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        drawer.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // "Show all" buttons remove the phone-only limit on the list right before them
  document.querySelectorAll('[data-show-all]').forEach(function (btn) {
    var list = document.getElementById(btn.getAttribute('data-show-all'));
    if (!list) return;
    btn.addEventListener('click', function () { list.classList.remove('limit'); });
  });

  var grid = document.getElementById('work-grid');
  if (grid) {
    var filters = document.querySelectorAll('.m-filters button');
    var cards = grid.querySelectorAll('.m-card');
    filters.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-f');
        grid.classList.remove('limit');
        filters.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        cards.forEach(function (c) { c.hidden = !(f === 'all' || c.getAttribute('data-cat') === f); });
      });
    });
  }

  // Load demo videos only when they scroll into view; no autoplay for reduced motion
  var videos = document.querySelectorAll('video[data-lazy-src]');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!videos.length || reduceMotion || !('IntersectionObserver' in window)) return;
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      var video = entry.target;
      if (entry.isIntersecting) {
        if (!video.src) video.src = video.dataset.lazySrc;
        video.play().catch(function () {});
      } else if (video.src) {
        video.pause();
      }
    });
  }, { threshold: 0.25 });
  videos.forEach(function (v) { observer.observe(v); });
})();
