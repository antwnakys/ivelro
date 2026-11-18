(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO = 'IntersectionObserver' in window;
  var root = document.documentElement;

  // Footer year
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Header: solid background once the page scrolls
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 24); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Hero title: word-by-word reveal
  var title = document.querySelector('[data-split]');
  if (title && !reduce) {
    var words = title.textContent.trim().split(/\s+/);
    title.setAttribute('aria-label', title.textContent.trim());
    title.innerHTML = words.map(function (w, i) {
      return '<span class="w" aria-hidden="true"><span style="--i:' + i + '">' + w + '</span></span>';
    }).join(' ');
    title.classList.add('split');
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  var steps = document.querySelector('.steps');
  if (!hasIO || reduce) {
    items.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    root.classList.add('js-reveal');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });

    if (steps) {
      var so = new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting) { steps.classList.add('is-drawn'); so.disconnect(); }
      }, { rootMargin: '0px 0px -20% 0px' });
      so.observe(steps);
    }
  }

  // Scroll-spy: highlight the nav link of the section in view
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (hasIO && links.length) {
    var map = {};
    links.forEach(function (a) {
      var t = document.querySelector(a.getAttribute('href'));
      if (t) map[t.id] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('is-active'); });
          if (map[e.target.id]) map[e.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { spy.observe(document.getElementById(id)); });
    // Clear when back at the top
    window.addEventListener('scroll', function () {
      if (window.scrollY < window.innerHeight * 0.4) links.forEach(function (a) { a.classList.remove('is-active'); });
    }, { passive: true });
  }

  // Service cards: cursor-following spotlight
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }
})();
