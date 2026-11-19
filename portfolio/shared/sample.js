/* Shared behaviour for the IVELRO sample sites:
   mobile menu, live opening-hours status and inline form validation. */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) {
    var nav = document.getElementById(menuBtn.getAttribute('aria-controls'));
    var setMenu = function (open) {
      menuBtn.setAttribute('aria-expanded', String(open));
      nav.classList.toggle('open', open);
    };
    menuBtn.addEventListener('click', function () {
      setMenu(menuBtn.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        menuBtn.focus();
      }
    });
    window.matchMedia('(min-width: 961px)').addEventListener('change', function (m) {
      if (m.matches) setMenu(false);
    });
  }

  /* ---------- Opening hours (Athens time) ---------- */
  function athensNow() {
    var o = {};
    new Intl.DateTimeFormat('en-GB', {
      timeZone: 'Europe/Athens', weekday: 'short', hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(new Date()).forEach(function (p) { o[p.type] = p.value; });
    return {
      day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(o.weekday),
      min: Number(o.hour) * 60 + Number(o.minute)
    };
  }
  function toMin(t) { var a = t.split(':'); return Number(a[0]) * 60 + Number(a[1]); }
  function fmt(t) { var m = toMin(t) % 1440; return String(Math.floor(m / 60)).padStart(2, '0') + ':' + String(m % 60).padStart(2, '0'); }

  var now = athensNow();

  // <span data-hours='{"1":[["09:00","14:00"]]}' data-open="Open until {t}" data-closed="Closed now" hidden>
  // Days: 0 = Sunday. An end time past 24:00 (e.g. 24:30) runs into the next day.
  document.querySelectorAll('[data-hours]').forEach(function (el) {
    var hours = JSON.parse(el.getAttribute('data-hours')), until = null;
    var check = function (day, shift) {
      (hours[day] || []).forEach(function (r) {
        if (now.min >= toMin(r[0]) + shift && now.min < toMin(r[1]) + shift) until = r[1];
      });
    };
    check(now.day, 0);
    check((now.day + 6) % 7, -1440);
    el.textContent = until ? el.getAttribute('data-open').replace('{t}', fmt(until)) : el.getAttribute('data-closed');
    el.classList.add(until ? 'is-open' : 'is-closed');
    el.hidden = false;
  });

  // Highlight today's row: <tr data-day="6 0">
  document.querySelectorAll('[data-day]').forEach(function (row) {
    if (row.getAttribute('data-day').split(' ').indexOf(String(now.day)) > -1) {
      row.classList.add('today');
      row.setAttribute('aria-current', 'date');
    }
  });

  /* ---------- Forms ---------- */
  // sampleForm(form, { busy: 'Sending…', success: fn(form) -> message, check: fn(form) -> [[field, message]], reset: bool })
  // Each field can carry data-msg with the error text to show when it is empty or invalid.
  window.sampleForm = function (form, opts) {
    var ok = form.querySelector('.ok') || document.getElementById(opts.ok);
    var btn = form.querySelector('[type="submit"]');
    var fields = Array.prototype.filter.call(form.elements, function (f) { return f.willValidate; });

    function clear(field) {
      field.removeAttribute('aria-invalid');
      field.removeAttribute('aria-describedby');
      var err = document.getElementById(field.id + '-err');
      if (err) err.remove();
    }
    function fail(field, msg) {
      clear(field);
      field.setAttribute('aria-invalid', 'true');
      var err = document.createElement('span');
      err.className = 'err';
      err.id = field.id + '-err';
      err.textContent = msg;
      (field.closest('label') || field.parentNode).appendChild(err);
      field.setAttribute('aria-describedby', err.id);
    }
    function onEdit(e) {
      var f = e.target;
      if (f.getAttribute('aria-invalid') !== 'true') return;
      f.setCustomValidity('');
      if (f.checkValidity()) clear(f);
    }
    form.addEventListener('input', onEdit);
    form.addEventListener('change', onEdit);

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      ok.textContent = '';
      fields.forEach(function (f) { f.setCustomValidity(''); clear(f); });
      (opts.check ? opts.check(form) : []).forEach(function (c) { c[0].setCustomValidity(c[1]); });

      var bad = fields.filter(function (f) { return !f.checkValidity(); });
      bad.forEach(function (f) {
        fail(f, f.validity.customError ? f.validationMessage : (f.getAttribute('data-msg') || f.validationMessage));
      });
      if (bad.length) { bad[0].focus(); return; }

      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = opts.busy;
      setTimeout(function () {
        btn.disabled = false;
        btn.textContent = label;
        ok.textContent = opts.success(form);
        if (opts.reset) form.reset();
        if (opts.after) opts.after(form);
        ok.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      }, 650);
    });
  };

  // Local date as yyyy-mm-dd
  window.isoDate = function (d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  };
})();
