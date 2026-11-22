/* IVELRO starter: mobile menu, scroll reveal, sticky header, live opening hours, contact form (Web3Forms). */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile menu */
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) {
    var nav = document.getElementById(menuBtn.getAttribute('aria-controls'));
    var setMenu = function (open) { menuBtn.setAttribute('aria-expanded', String(open)); nav.classList.toggle('open', open); };
    menuBtn.addEventListener('click', function () { setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') { setMenu(false); menuBtn.focus(); }
    });
  }

  /* Reveal on scroll */
  var rv = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    rv.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (e) { io.observe(e); });
  }

  /* Header shadow once the page scrolls */
  var hdr = document.querySelector('.site-header');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Opening hours in Athens time.
     data-hours='{"1":[["09:00","14:00"],["17:00","21:00"]]}'  (0 = Sunday; "24:30" runs past midnight) */
  var o = {};
  new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Athens', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
    .formatToParts(new Date()).forEach(function (p) { o[p.type] = p.value; });
  var now = { day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(o.weekday), min: Number(o.hour) * 60 + Number(o.minute) };
  var toMin = function (t) { var a = t.split(':'); return Number(a[0]) * 60 + Number(a[1]); };
  var fmt = function (t) { var m = toMin(t) % 1440; return String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'); };
  document.querySelectorAll('[data-hours]').forEach(function (el) {
    var hours;
    try { hours = JSON.parse(el.getAttribute('data-hours')); } catch (e) { return; }
    var until = null;
    var check = function (day, shift) {
      (hours[day] || []).forEach(function (r) { if (now.min >= toMin(r[0]) + shift && now.min < toMin(r[1]) + shift) until = r[1]; });
    };
    check(now.day, 0);
    check((now.day + 6) % 7, -1440);
    el.textContent = until ? el.getAttribute('data-open').replace('{t}', fmt(until)) : el.getAttribute('data-closed');
    el.classList.add(until ? 'is-open' : 'is-closed');
    el.hidden = false;
  });
  document.querySelectorAll('[data-day]').forEach(function (row) {
    if (row.getAttribute('data-day').split(' ').indexOf(String(now.day)) > -1) { row.classList.add('today'); row.setAttribute('aria-current', 'date'); }
  });

  /* Contact form: inline errors, then send to Web3Forms */
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = form.querySelector('.form-status');
  var btn = form.querySelector('button[type="submit"]');
  var fields = Array.prototype.slice.call(form.querySelectorAll('input[required], textarea[required], input[type="email"], input[pattern]'));
  var clear = function (f) {
    f.removeAttribute('aria-invalid'); f.removeAttribute('aria-describedby');
    var e = document.getElementById(f.id + '-err'); if (e) e.remove();
  };
  var fail = function (f) {
    clear(f);
    f.setAttribute('aria-invalid', 'true');
    var e = document.createElement('span');
    e.className = 'field-err'; e.id = f.id + '-err';
    e.textContent = f.getAttribute('data-msg') || f.validationMessage;
    (f.closest('.field') || f.closest('label') || f.parentNode).appendChild(e);
    f.setAttribute('aria-describedby', e.id);
  };
  form.addEventListener('input', function (e) { if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) clear(e.target); });
  form.addEventListener('change', function (e) { if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) clear(e.target); });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.textContent = ''; status.className = 'form-status';
    fields.forEach(clear);
    var bad = fields.filter(function (f) { return !f.checkValidity(); });
    bad.forEach(fail);
    if (bad.length) { bad[0].focus(); return; }
    if (form.botcheck && form.botcheck.checked) return;

    var key = form.access_key && form.access_key.value;
    if (!key || key.indexOf('{{') === 0) {
      status.textContent = 'Demo: the form works, but it is not connected yet. Add the Web3Forms access key.';
      status.className = 'form-status is-error';
      return;
    }
    var label = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = form.getAttribute('data-sending');
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });
    fetch('https://api.web3forms.com/submit', {
      method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (!res.success) throw new Error(res.message || 'Failed');
      status.textContent = form.getAttribute('data-ok'); status.className = 'form-status is-ok';
      form.reset();
    }).catch(function () {
      status.textContent = form.getAttribute('data-error'); status.className = 'form-status is-error';
    }).then(function () { btn.disabled = false; btn.innerHTML = label; });
  });
})();
