(function () {
  'use strict';

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Highlight the nav link for the section currently on screen
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  if (!('IntersectionObserver' in window) || !links.length) return;
  var byId = {};
  links.forEach(function (a) {
    var el = document.querySelector(a.getAttribute('href'));
    if (el) byId[el.id] = a;
  });
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      links.forEach(function (a) { a.classList.remove('is-active'); });
      if (byId[e.target.id]) byId[e.target.id].classList.add('is-active');
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  Object.keys(byId).forEach(function (id) { spy.observe(document.getElementById(id)); });
})();
