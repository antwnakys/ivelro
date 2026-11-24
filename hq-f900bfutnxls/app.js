/* IVELRO team dashboard. Data lives in a private Google Sheet; the Apps Script back end
   (tools/dashboard/Code.gs) checks the password and only then returns or saves clients. */
(function () {
  'use strict';

  // Web app URL of the deployed Apps Script (Deploy → Manage deployments → Web app URL).
  var API = 'https://script.google.com/macros/s/AKfycbz6s7DbCldaH93dElqWtV_l0lEV4F0O_jINbutfI7bgc9JDbDJ6YHsj0ep6V-xR4sez/exec';

  var STAGES = ['Signed', 'Discovery', 'Build', 'Testing', 'Live', 'Paused'];
  var STAGE_PCT = { Signed: 10, Discovery: 30, Build: 60, Testing: 85, Live: 100, Paused: 0 };
  var IN_PROGRESS = ['Signed', 'Discovery', 'Build', 'Testing'];
  var SERVICES = ['AI Search Presence', 'Automation & AI Integration', 'Local AI', 'Several services'];
  var PACKAGES = ['None', 'Basic', 'Plus'];
  var ROLES = ['', 'Sales & Partnerships', 'AI Search & Content Lead', 'Brand & Communication Designer', 'Developer', 'AI Solutions Specialist'];
  var TOKEN_KEY = 'ivelro_hq_session';

  var $ = function (id) { return document.getElementById(id); };
  var state = { clients: [], loadedAt: 0 };

  /* ---------- Small helpers ---------- */

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = String(text);
    return n;
  }
  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function parseDate(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(s || ''));
    return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
  }
  function daysFromToday(s) { var d = parseDate(s); return d ? Math.round((d - today()) / 864e5) : null; }
  function fmtDate(s) {
    var d = parseDate(s);
    return d ? d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }) : '';
  }
  function money(n) { return (Math.round(Number(n) || 0)).toLocaleString('en-GB') + ' €'; }
  function plural(n, word) { return n + ' ' + word + (n === 1 ? '' : 's'); }

  function getSession() {
    try {
      var s = JSON.parse(sessionStorage.getItem(TOKEN_KEY) || 'null');
      if (s && s.token && s.exp > Date.now()) return s.token;
    } catch (e) { /* storage blocked */ }
    return null;
  }
  function setSession(token, hours) {
    try { sessionStorage.setItem(TOKEN_KEY, JSON.stringify({ token: token, exp: Date.now() + hours * 36e5 - 6e4 })); } catch (e) { /* ignore */ }
    state.token = token;
  }
  function clearSession() {
    try { sessionStorage.removeItem(TOKEN_KEY); } catch (e) { /* ignore */ }
    state.token = null;
  }

  function api(action, data) {
    if (!API) return Promise.reject(new Error('not_connected'));
    var body = Object.assign({ action: action, token: state.token }, data || {});
    // text/plain keeps this a "simple" request, which Apps Script accepts from another site
    return fetch(API, { method: 'POST', body: JSON.stringify(body), redirect: 'follow', credentials: 'omit' })
      .then(function (r) { if (!r.ok) throw new Error('network'); return r.json(); })
      .catch(function () { throw new Error('network'); })
      .then(function (res) {
        if (!res || !res.ok) {
          var err = new Error((res && res.error) || 'server_error');
          if (err.message === 'signed_out') { clearSession(); showLogin('You were signed out. Sign in again.'); }
          throw err;
        }
        return res;
      });
  }

  var MESSAGES = {
    wrong_password: 'Wrong password.',
    locked: 'Too many wrong tries. Logins are paused for 15 minutes.',
    no_password_set: 'The team password has not been set yet. See “Client dashboard: setup and use” in Drive.',
    not_connected: 'The dashboard is not connected yet. See “Client dashboard: setup and use” in Drive.',
    network: 'Cannot reach the server. Check your connection and try again.',
    not_found: 'That client no longer exists. Press Refresh.',
    bad_request: 'Something in the form is not valid.',
    signed_out: 'You were signed out. Sign in again.',
    server_error: 'The server had a problem. Try again in a minute.'
  };
  function msg(e) { return MESSAGES[e && e.message] || MESSAGES.server_error; }

  /* ---------- Sign in ---------- */

  function showLogin(text) {
    $('app').hidden = true;
    $('login').hidden = false;
    $('login-msg').textContent = text || '';
    if ($('dlg').open) $('dlg').close();
    $('pw').value = '';
    $('pw').focus();
  }

  $('login-form').addEventListener('submit', function (ev) {
    ev.preventDefault();
    var pw = $('pw').value;
    if (!pw) { $('login-msg').textContent = 'Type the team password.'; return; }
    var btn = $('login-btn');
    btn.disabled = true; btn.textContent = 'Signing in…';
    $('login-msg').textContent = '';
    api('login', { password: pw })
      .then(function (res) { setSession(res.token, res.hours || 6); $('pw').value = ''; return start(); })
      .catch(function (e) { $('login-msg').textContent = msg(e); $('pw').select(); })
      .then(function () { btn.disabled = false; btn.textContent = 'Sign in'; });
  });

  $('logout').addEventListener('click', function () {
    api('logout').catch(function () {});
    clearSession();
    state.clients = [];
    showLogin('Signed out.');
  });

  /* ---------- Load and render ---------- */

  function start() {
    $('login').hidden = true;
    $('app').hidden = false;
    return load();
  }

  function load() {
    $('sync').textContent = 'Loading…';
    $('refresh').disabled = true;
    return api('list')
      .then(function (res) {
        state.clients = res.clients || [];
        state.loadedAt = Date.now();
        render();
        $('sync').textContent = 'Updated ' + new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
      })
      .catch(function (e) { if (e.message !== 'signed_out') $('sync').textContent = msg(e); })
      .then(function () { $('refresh').disabled = false; });
  }
  $('refresh').addEventListener('click', load);
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden && state.token && !$('app').hidden && Date.now() - state.loadedAt > 5 * 6e4 && !$('dlg').open) load();
  });

  function render() {
    renderStats();
    renderPipeline();
    renderAttention();
    renderClients();
  }

  function renderStats() {
    var c = state.clients;
    var live = c.filter(function (x) { return x.stage === 'Live'; });
    var supported = live.filter(function (x) { return x['package'] && x['package'] !== 'None'; });
    var basic = supported.filter(function (x) { return x['package'] === 'Basic'; }).length;
    var mrr = supported.reduce(function (s, x) { return s + (Number(x.monthly) || 0); }, 0);
    var value = c.reduce(function (s, x) { return s + (Number(x.projectPrice) || 0); }, 0);
    var paused = c.filter(function (x) { return x.stage === 'Paused'; }).length;
    $('s-total').textContent = c.length;
    $('s-total-sub').textContent = paused ? paused + ' paused' : ' ';
    $('s-progress').textContent = c.filter(function (x) { return IN_PROGRESS.indexOf(x.stage) !== -1; }).length;
    $('s-live').textContent = live.length;
    $('s-live-sub').textContent = supported.length + ' on a support package';
    $('s-mrr').textContent = money(mrr);
    $('s-mrr-sub').textContent = supported.length ? 'Basic ' + basic + ' · Plus ' + (supported.length - basic) : 'per month';
    $('s-value').textContent = money(value);
  }

  function renderPipeline() {
    var pipe = $('pipe'), legend = $('pipe-legend');
    pipe.textContent = ''; legend.textContent = '';
    var counts = {};
    STAGES.forEach(function (s) { counts[s] = 0; });
    state.clients.forEach(function (x) { if (counts[x.stage] !== undefined) counts[x.stage]++; });
    var total = state.clients.length;
    var parts = [];
    STAGES.forEach(function (s) {
      if (counts[s]) {
        var seg = el('span', 'c-' + s);
        seg.style.flexGrow = counts[s];
        seg.title = s + ': ' + counts[s];
        pipe.appendChild(seg);
        parts.push(s + ' ' + counts[s]);
      }
      var li = el('li');
      li.appendChild(el('i', 'c-' + s));
      li.appendChild(document.createTextNode(s + ' '));
      li.appendChild(el('b', '', counts[s]));
      legend.appendChild(li);
    });
    if (!total) pipe.appendChild(el('span', 'none'));
    pipe.setAttribute('aria-label', total ? 'Clients by stage: ' + parts.join(', ') : 'No clients yet');
    $('pipe-sum').textContent = total ? plural(total, 'client') : '';
  }

  // Everything that needs someone to act, most urgent first
  function issues() {
    var out = [];
    state.clients.forEach(function (x) {
      var name = x.business || '(no name)';
      var d = daysFromToday(x.renewal);
      if (x.stage !== 'Paused' && d !== null && d <= 60) {
        var what = x.renewalOf || 'A subscription';
        if (d < 0) out.push({ sev: 0, c: x, title: name + ': renewal overdue', detail: what + ' expired ' + plural(-d, 'day') + ' ago. Check with the client now.', badge: ['b-crit', 'Expired'] });
        else if (d <= 30) out.push({ sev: 1, c: x, title: name + ': renewal due', detail: what + ' renews on ' + fmtDate(x.renewal) + '.', badge: ['b-crit', d === 0 ? 'Today' : 'In ' + plural(d, 'day')] });
        else out.push({ sev: 3, c: x, title: name + ': renewal coming up', detail: what + ' renews on ' + fmtDate(x.renewal) + '.', badge: ['b-warn', 'In ' + plural(d, 'day')] });
      }
      if (x.stage === 'Live') {
        if (x['package'] && x['package'] !== 'None') {
          var since = x.lastCheck ? -daysFromToday(x.lastCheck) : null;
          if (since === null || since > 35) out.push({ sev: 2, c: x, title: name + ': monthly check due', detail: since === null ? 'No monthly check recorded yet.' : 'Last check was ' + plural(since, 'day') + ' ago.', badge: ['b-warn', 'Check due'] });
        }
        if (!x.renewal && x.renewalOf) out.push({ sev: 4, c: x, title: name + ': add the renewal date', detail: 'So the dashboard can warn you before ' + x.renewalOf + ' expires.', badge: ['b-info', 'Missing'] });
      }
      if (IN_PROGRESS.indexOf(x.stage) !== -1) {
        var upd = x.updated ? -daysFromToday(String(x.updated).slice(0, 10)) : null;
        if (upd !== null && upd > 14) out.push({ sev: 3, c: x, title: name + ': no update for ' + plural(upd, 'day'), detail: 'Stage: ' + x.stage + (x.nextStep ? '. Next step: ' + x.nextStep : '.'), badge: ['b-warn', 'Stalled'] });
        else if (!x.nextStep) out.push({ sev: 4, c: x, title: name + ': add a next step', detail: 'Stage: ' + x.stage + '. Write what happens next and who does it.', badge: ['b-info', 'No next step'] });
      }
    });
    return out.sort(function (a, b) { return a.sev - b.sev; });
  }

  function renderAttention() {
    var list = $('attention');
    list.textContent = '';
    var items = issues();
    $('att-count').textContent = items.length ? plural(items.length, 'item') : '';
    if (!items.length) {
      var li = el('li');
      li.appendChild(el('span', 'ok-line', state.clients.length ? 'All good. Nothing needs attention right now.' : 'Nothing yet. Warnings about subscription renewals, monthly checks and stalled projects appear here.'));
      list.appendChild(li);
      return;
    }
    items.forEach(function (it) {
      var li = el('li');
      li.appendChild(el('span', 'badge ' + it.badge[0], it.badge[1]));
      var what = el('div', 'what');
      what.appendChild(el('b', '', it.title));
      what.appendChild(el('span', '', it.detail));
      li.appendChild(what);
      var open = el('button', 'open', 'Open');
      open.type = 'button';
      open.setAttribute('aria-label', 'Open ' + (it.c.business || 'client'));
      open.addEventListener('click', function () { openDialog(it.c); });
      li.appendChild(open);
      list.appendChild(li);
    });
  }

  function renewalBadge(x) {
    var d = daysFromToday(x.renewal);
    if (d === null) return null;
    if (d < 0) return ['b-crit', 'Expired'];
    if (d <= 30) return ['b-crit', 'Renew in ' + plural(d, 'day')];
    if (d <= 60) return ['b-warn', 'Renew in ' + plural(d, 'day')];
    return ['b-good', 'Renews ' + fmtDate(x.renewal)];
  }

  function renderClients() {
    var box = $('clients');
    box.textContent = '';
    var q = $('q').value.trim().toLowerCase();
    var fs = $('f-stage').value;
    var sort = $('sort').value;
    var rows = state.clients.filter(function (x) {
      if (fs && x.stage !== fs) return false;
      if (!q) return true;
      return [x.business, x.industry, x.service, x.tools, x.contact, x.owner, x.email, x.phone, x.nextStep, x.notes]
        .join(' ').toLowerCase().indexOf(q) !== -1;
    });
    rows.sort(function (a, b) {
      if (sort === 'business') return String(a.business).localeCompare(String(b.business));
      if (sort === 'updated') return String(b.updated).localeCompare(String(a.updated));
      if (sort === 'renewal') return (a.renewal ? String(a.renewal) : '9999').localeCompare(b.renewal ? String(b.renewal) : '9999');
      return STAGES.indexOf(a.stage) - STAGES.indexOf(b.stage) || String(a.business).localeCompare(String(b.business));
    });
    $('empty').hidden = state.clients.length > 0;
    if (state.clients.length && !rows.length) box.appendChild(el('p', 'empty', 'No clients match the search.'));

    rows.forEach(function (x) {
      var card = el('button', 'client');
      card.type = 'button';
      card.setAttribute('aria-label', 'Edit ' + (x.business || 'client'));
      card.addEventListener('click', function () { openDialog(x); });

      var a = el('span');
      a.appendChild(el('span', 'name', x.business || '(no name)'));
      a.appendChild(el('span', 'sub', [x.industry, x.contact].filter(Boolean).join(' · ') || ' '));
      card.appendChild(a);

      var b = el('span');
      b.appendChild(el('span', 'k', x.stage || 'Signed'));
      var prog = el('span', 'progress');
      var bar = el('span', 'bar' + (x.stage === 'Paused' ? ' paused' : ''));
      var fill = el('span');
      fill.style.width = (STAGE_PCT[x.stage] || 0) + '%';
      bar.appendChild(fill);
      prog.appendChild(bar);
      prog.appendChild(el('span', 'pct', x.stage === 'Paused' ? 'paused' : (STAGE_PCT[x.stage] || 0) + '%'));
      b.appendChild(prog);
      if (x.nextStep && x.stage !== 'Live') b.appendChild(el('span', 'next', 'Next: ' + x.nextStep));
      card.appendChild(b);

      var c = el('span');
      c.appendChild(el('span', 'k', 'Service'));
      c.appendChild(el('span', 'v', x.service || '—'));
      if (x.runsOn) c.appendChild(el('span', 'sub', 'Runs on: ' + x.runsOn));
      var rb = renewalBadge(x);
      if (rb) c.appendChild(el('span', 'badge ' + rb[0], rb[1]));
      card.appendChild(c);

      var d = el('span');
      d.appendChild(el('span', 'k', 'Support'));
      var pk = x['package'] && x['package'] !== 'None' ? x['package'] + (x.monthly ? ' · ' + money(x.monthly) + '/mo' : '') : 'No package';
      d.appendChild(el('span', 'v', pk));
      d.appendChild(el('span', 'sub', x.owner || 'No one responsible yet'));
      card.appendChild(d);

      box.appendChild(card);
    });
  }
  ['q', 'f-stage', 'sort'].forEach(function (id) { $(id).addEventListener('input', renderClients); });

  /* ---------- Add / edit dialog ---------- */

  var form = $('client-form');
  function fillSelect(sel, values, labels) {
    values.forEach(function (v, i) { var o = el('option', '', labels ? labels[i] : v); o.value = v; sel.appendChild(o); });
  }
  fillSelect(form.elements.stage, STAGES);
  fillSelect(form.elements.service, [''].concat(SERVICES), ['Not set'].concat(SERVICES));
  fillSelect(form.elements['package'], PACKAGES, ['None', 'Basic', 'Plus']);
  fillSelect(form.elements.owner, ROLES, ['Not set'].concat(ROLES.slice(1)));
  fillSelect($('f-stage'), STAGES);

  function openDialog(x) {
    form.reset();
    $('dlg-msg').textContent = '';
    var c = x || { stage: 'Signed', 'package': 'None', startDate: new Date().toISOString().slice(0, 10) };
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!f.name) return;
      var v = c[f.name];
      if (f.name === 'owner' && v && ROLES.indexOf(v) === -1) fillSelect(f, [v]);
      f.value = v === undefined || v === null ? '' : String(v);
      f.removeAttribute('aria-invalid');
    });
    $('dlg-h').textContent = x ? (x.business || 'Client') : 'New client';
    $('del').hidden = !x;
    $('dlg').showModal();
    form.elements.business.focus();
  }
  $('add').addEventListener('click', function () { openDialog(null); });
  $('dlg-close').addEventListener('click', function () { $('dlg').close(); });
  $('dlg-cancel').addEventListener('click', function () { $('dlg').close(); });

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var biz = form.elements.business;
    var email = form.elements.email;
    biz.setAttribute('aria-invalid', String(!biz.value.trim()));
    email.setAttribute('aria-invalid', String(!email.validity.valid));
    if (!biz.value.trim()) { $('dlg-msg').textContent = 'Write the business name.'; biz.focus(); return; }
    if (!email.validity.valid) { $('dlg-msg').textContent = 'The email address does not look right.'; email.focus(); return; }
    var client = {};
    Array.prototype.forEach.call(form.elements, function (f) { if (f.name) client[f.name] = f.value.trim(); });
    var btn = $('save');
    btn.disabled = true; btn.textContent = 'Saving…';
    api('save', { client: client })
      .then(function (res) {
        var saved = res.client;
        var i = state.clients.findIndex(function (x) { return String(x.id) === String(saved.id); });
        if (i === -1) state.clients.push(saved); else state.clients[i] = saved;
        render();
        $('dlg').close();
        $('sync').textContent = 'Saved';
      })
      .catch(function (e) { if (e.message !== 'signed_out') $('dlg-msg').textContent = msg(e); })
      .then(function () { btn.disabled = false; btn.textContent = 'Save'; });
  });

  $('del').addEventListener('click', function () {
    var id = form.elements.id.value;
    var name = form.elements.business.value || 'this client';
    if (!id || !window.confirm('Delete ' + name + '? This removes the row from the Google Sheet too.')) return;
    var btn = $('del');
    btn.disabled = true;
    api('delete', { id: id })
      .then(function () {
        state.clients = state.clients.filter(function (x) { return String(x.id) !== String(id); });
        render();
        $('dlg').close();
        $('sync').textContent = 'Deleted';
      })
      .catch(function (e) { if (e.message !== 'signed_out') $('dlg-msg').textContent = msg(e); })
      .then(function () { btn.disabled = false; });
  });

  /* ---------- Go ---------- */

  state.token = getSession();
  if (state.token) start(); else showLogin(API ? '' : MESSAGES.not_connected);
})();
