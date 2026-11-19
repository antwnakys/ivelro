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

  /* ---------- Reveal on scroll (.rv -> .rv.in) ---------- */
  var rv = document.querySelectorAll('.rv');
  if (reduce || !('IntersectionObserver' in window)) {
    rv.forEach(function (e) { e.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (e) { io.observe(e); });
  }

  /* ---------- Sticky header shadow ---------- */
  var hdr = document.querySelector('header');
  if (hdr) {
    var onScroll = function () { hdr.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Tabs: [role=tablist] > [role=tab][aria-controls] ---------- */
  document.querySelectorAll('[role="tablist"]').forEach(function (list) {
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    var select = function (t, focus) {
      tabs.forEach(function (x) {
        var on = x === t;
        x.setAttribute('aria-selected', String(on));
        x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) t.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var j = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : null;
        if (j === null) return;
        e.preventDefault();
        select(tabs[(j + tabs.length) % tabs.length], true);
      });
    });
  });

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

    var first = function (f) { return f.type === 'radio' ? form.querySelector('input[name="' + f.name + '"]') : f; };
    function clear(field) {
      field = first(field);
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
      (field.type === 'radio' ? field.closest('fieldset') : (field.closest('label') || field.parentNode)).appendChild(err);
      field.setAttribute('aria-describedby', err.id);
    }
    function onEdit(e) {
      var f = e.target;
      if (!f.willValidate || first(f).getAttribute('aria-invalid') !== 'true') return;
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

      var seen = {};
      var bad = fields.filter(function (f) {
        if (f.type === 'radio') { if (seen[f.name]) return false; seen[f.name] = 1; f = first(f); }
        return !f.checkValidity();
      }).map(first);
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
