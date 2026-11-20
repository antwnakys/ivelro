/* IVELRO email signature template. One source for the maker page and the ready-made role files.
   Email-safe: tables, inline styles, hosted images with fixed sizes and alt text. */
(function (root) {
  'use strict';

  var IMG = 'https://ivelro.com/assets/img/email/';
  var FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif";
  var TEXT = {
    en: { tagline: 'INTELLIGENT AUTOMATION &middot; DIGITAL INNOVATION', cta: 'SEE OUR WORK', site: 'https://ivelro.com/' },
    el: { tagline: '&Epsilon;&Upsilon;&Phi;&Upsilon;&Eta;&Sigma; &Alpha;&Upsilon;&Tau;&Omicron;&Mu;&Alpha;&Tau;&Omicron;&Pi;&Omicron;&Iota;&Eta;&Sigma;&Eta; &middot; &Psi;&Eta;&Phi;&Iota;&Alpha;&Kappa;&Eta; &Kappa;&Alpha;&Iota;&Nu;&Omicron;&Tau;&Omicron;&Mu;&Iota;&Alpha;',
          cta: '&Delta;&Epsilon;&Iota;&Tau;&Epsilon; &Tau;&Eta; &Delta;&Omicron;&Upsilon;&Lambda;&Epsilon;&Iota;&Alpha; &Mu;&Alpha;&Sigma;', site: 'https://ivelro.com/el/' }
  };
  var WORK = 'https://ivelro.com/portfolio/';

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function clean(o) {
    var phone = (o.phone || '').trim() || '+30 69X XXX XXXX';
    var linkedin = (o.linkedin || '').trim();
    if (linkedin && !/^https?:\/\//i.test(linkedin)) linkedin = 'https://' + linkedin;
    return {
      name: esc((o.name || '').trim() || 'Name Surname'),
      role: esc((o.role || 'Project Manager').trim()),
      roleCaps: esc((o.role || 'Project Manager').trim().toUpperCase()),
      phone: esc(phone),
      tel: esc(phone.replace(/[^0-9+]/g, '')),
      email: esc((o.email || '').trim() || 'name@ivelro.com'),
      linkedin: esc(linkedin),
      t: TEXT[o.lang === 'el' ? 'el' : 'en']
    };
  }
  function row(icon, inner) {
    return '<tr>' +
      '<td style="padding:0 10px 5px 0;vertical-align:middle;width:14px;"><img src="' + IMG + icon + '.png" width="14" height="14" alt="" style="display:block;border:0;width:14px;height:14px;"></td>' +
      '<td style="padding:0 0 5px 0;vertical-align:middle;font-family:' + FONT + ';font-size:13px;line-height:18px;color:#3d3d3d;">' + inner + '</td>' +
      '</tr>';
  }

  function full(o) {
    var d = clean(o);
    var link = 'color:#3d3d3d;text-decoration:none;';
    var rows = row('phone', '<a href="tel:' + d.tel + '" style="' + link + '">' + d.phone + '</a>') +
      row('mail', '<a href="mailto:' + d.email + '" style="' + link + '">' + d.email + '</a>') +
      row('web', '<a href="' + d.t.site + '" style="color:#0a0a0a;text-decoration:none;font-weight:bold;">ivelro.com</a>') +
      (d.linkedin ? row('linkedin', '<a href="' + d.linkedin + '" style="' + link + '">LinkedIn</a>') : '');
    return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:' + FONT + ';color:#0a0a0a;">' +
      '<tr>' +
        '<td style="vertical-align:top;padding:2px 20px 0 0;width:104px;">' +
          '<a href="' + d.t.site + '" style="text-decoration:none;"><img src="' + IMG + 'tile.png" width="104" height="104" alt="IVELRO" style="display:block;border:0;width:104px;height:104px;border-radius:14px;"></a>' +
        '</td>' +
        '<td style="vertical-align:top;">' +
          '<div style="font-family:' + FONT + ';font-size:18px;line-height:22px;font-weight:bold;letter-spacing:-0.2px;color:#0a0a0a;">' + d.name + '</div>' +
          '<div style="font-family:' + FONT + ';font-size:10px;line-height:16px;letter-spacing:2px;color:#8c8c8c;padding:3px 0 0 0;">' + d.roleCaps + '&nbsp;&nbsp;&middot;&nbsp;&nbsp;IVELRO</div>' +
          '<div style="width:28px;height:2px;background-color:#0a0a0a;font-size:0;line-height:2px;margin:11px 0 12px 0;">&nbsp;</div>' +
          '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">' + rows + '</table>' +
          '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:separate;margin:9px 0 0 0;"><tr>' +
            '<td style="background-color:#0a0a0a;border-radius:4px;">' +
              '<a href="' + WORK + '" style="display:inline-block;padding:7px 14px;font-family:' + FONT + ';font-size:10px;line-height:14px;letter-spacing:1.6px;font-weight:bold;color:#ffffff;text-decoration:none;">' + d.t.cta + '&nbsp;&nbsp;&rarr;</a>' +
            '</td>' +
          '</tr></table>' +
        '</td>' +
      '</tr>' +
      '<tr><td colspan="2" style="padding:16px 0 0 0;">' +
        '<div style="border-top:1px solid #e6e6e6;padding:10px 0 0 0;font-family:' + FONT + ';font-size:9px;line-height:13px;letter-spacing:2px;color:#a0a0a0;">' + d.t.tagline + '</div>' +
      '</td></tr>' +
    '</table>';
  }

  function reply(o) {
    var d = clean(o);
    return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:' + FONT + ';">' +
      '<tr>' +
        '<td style="vertical-align:middle;padding:0 12px 0 0;width:40px;">' +
          '<a href="' + d.t.site + '" style="text-decoration:none;"><img src="' + IMG + 'tile-small.png" width="40" height="40" alt="IVELRO" style="display:block;border:0;width:40px;height:40px;border-radius:8px;"></a>' +
        '</td>' +
        '<td style="vertical-align:middle;font-family:' + FONT + ';font-size:12.5px;line-height:18px;color:#5a5a5a;">' +
          '<b style="font-size:13.5px;color:#0a0a0a;">' + d.name + '</b>&nbsp;&nbsp;&middot;&nbsp;&nbsp;' + d.role + ', IVELRO<br>' +
          '<a href="tel:' + d.tel + '" style="color:#5a5a5a;text-decoration:none;">' + d.phone + '</a>&nbsp;&nbsp;&middot;&nbsp;&nbsp;' +
          '<a href="' + d.t.site + '" style="color:#0a0a0a;text-decoration:none;font-weight:bold;">ivelro.com</a>' +
        '</td>' +
      '</tr>' +
    '</table>';
  }

  function ivelroSignature(o) { return (o && o.style === 'reply') ? reply(o || {}) : full(o || {}); }
  root.ivelroSignature = ivelroSignature;
  if (typeof module !== 'undefined' && module.exports) module.exports = ivelroSignature;
})(typeof window !== 'undefined' ? window : globalThis);
