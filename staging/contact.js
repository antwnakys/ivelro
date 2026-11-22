/* IVELRO contact form: sends to Web3Forms, shows inline errors and a status message.
   Settings come from data attributes on the <form>, so the same file works in English and Greek. */
(function () {
  'use strict';
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = form.querySelector('.form-status');
  var btn = form.querySelector('button[type="submit"]');
  var fields = Array.prototype.slice.call(form.querySelectorAll('input[required], textarea[required]'));

  function clear(f) {
    f.removeAttribute('aria-invalid');
    f.removeAttribute('aria-describedby');
    var e = document.getElementById(f.id + '-err');
    if (e) e.remove();
  }
  function fail(f) {
    clear(f);
    f.setAttribute('aria-invalid', 'true');
    var e = document.createElement('span');
    e.className = 'field-err';
    e.id = f.id + '-err';
    e.textContent = f.getAttribute('data-msg') || f.validationMessage;
    (f.closest('.field') || f.parentNode).appendChild(e);
    f.setAttribute('aria-describedby', e.id);
  }
  form.addEventListener('input', function (e) {
    if (e.target.getAttribute('aria-invalid') === 'true' && e.target.checkValidity()) clear(e.target);
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    status.textContent = '';
    status.className = 'form-status';
    fields.forEach(clear);
    var bad = fields.filter(function (f) { return !f.checkValidity(); });
    bad.forEach(fail);
    if (bad.length) { bad[0].focus(); return; }
    if (form.botcheck && form.botcheck.checked) return; // spam bot filled the hidden box

    var label = btn.innerHTML;
    btn.disabled = true;
    btn.textContent = form.getAttribute('data-sending');
    var data = {};
    new FormData(form).forEach(function (v, k) { data[k] = v; });

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); }).then(function (res) {
      if (!res.success) throw new Error(res.message || 'Failed');
      status.textContent = form.getAttribute('data-ok');
      status.className = 'form-status is-ok';
      form.reset();
    }).catch(function () {
      status.textContent = form.getAttribute('data-error');
      status.className = 'form-status is-error';
    }).then(function () {
      btn.disabled = false;
      btn.innerHTML = label;
    });
  });
})();
