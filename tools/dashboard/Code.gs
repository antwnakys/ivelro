/**
 * IVELRO client dashboard: back end.
 *
 * Paste this whole file into the Google Sheet "Client websites tracker"
 * (Extensions → Apps Script) and deploy it as a web app. The dashboard page on
 * ivelro.com talks to it. Client data stays in the private Google Sheet and is
 * only returned after the team password is checked here, on Google's side.
 *
 * Setup steps: Drive → IVELRO → Website (Web Developer) → "Client dashboard: setup and use".
 */

var SHEET_NAME = 'Clients';
var SESSION_HOURS = 6;          // a login lasts this long
var MAX_FAILS = 10;             // wrong passwords allowed ...
var FAIL_WINDOW_MIN = 15;       // ... within this many minutes, then logins pause for that long
var MIN_PASSWORD_LENGTH = 12;

// key, column title in the sheet
var COLUMNS = [
  ['id', 'ID'],
  ['business', 'Business'],
  ['industry', 'Industry'],
  ['contact', 'Contact person'],
  ['phone', 'Phone'],
  ['email', 'Email'],
  ['stage', 'Stage'],
  ['nextStep', 'Next step'],
  ['owner', 'Responsible'],
  ['startDate', 'Start date'],
  ['launchDate', 'Launch date'],
  ['website', 'Website'],
  ['domain', 'Domain'],
  ['registrar', 'Registrar'],
  ['renewal', 'Domain renewal'],
  ['hosting', 'Hosting'],
  ['projectPrice', 'Project price (€)'],
  ['package', 'Support package'],
  ['monthly', 'Monthly fee (€)'],
  ['lastCheck', 'Last monthly check'],
  ['notes', 'Notes'],
  ['updated', 'Last updated']
];
var STAGES = ['Signed', 'Design', 'Build', 'Review', 'Live', 'Paused'];
var PACKAGES = ['None', 'Basic', 'Plus'];
var DATE_KEYS = ['startDate', 'launchDate', 'renewal', 'lastCheck'];
var NUMBER_KEYS = ['projectPrice', 'monthly'];

/* ---------- Menu inside the Google Sheet ---------- */

function onOpen() {
  SpreadsheetApp.getUi().createMenu('IVELRO dashboard')
    .addItem('Set or change the password', 'setPassword')
    .addItem('Sign everyone out', 'signEveryoneOut')
    .addItem('Repair the sheet layout', 'setupSheet')
    .addToUi();
}

function setPassword() {
  var ui = SpreadsheetApp.getUi();
  var r = ui.prompt('Dashboard password',
    'Type the new team password (at least ' + MIN_PASSWORD_LENGTH + ' characters). ' +
    'Save it in the IVELRO group in Apple Passwords. Everyone is signed out.',
    ui.ButtonSet.OK_CANCEL);
  if (r.getSelectedButton() !== ui.Button.OK) return;
  var pw = r.getResponseText();
  if (!pw || pw.length < MIN_PASSWORD_LENGTH) {
    ui.alert('Too short. Use at least ' + MIN_PASSWORD_LENGTH + ' characters. Nothing was changed.');
    return;
  }
  var props = PropertiesService.getScriptProperties();
  var salt = Utilities.getUuid();
  props.setProperties({ PW_SALT: salt, PW_HASH: hash_(salt, pw) });
  bumpSessions_();
  setupSheet();
  ui.alert('Password saved. Everyone has been signed out of the dashboard.');
}

function signEveryoneOut() {
  bumpSessions_();
  SpreadsheetApp.getUi().alert('Everyone has been signed out of the dashboard.');
}

/** Creates the Clients tab with the right columns, dropdowns and frozen header. Safe to run again. */
function setupSheet() {
  var ss = SpreadsheetApp.getActive();
  var sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME, 0);
  var titles = COLUMNS.map(function (c) { return c[1]; });
  var have = sh.getLastColumn() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
  titles.forEach(function (t) {
    if (have.indexOf(t) === -1) { have.push(t); sh.getRange(1, have.length).setValue(t); }
  });
  sh.setFrozenRows(1);
  sh.getRange(1, 1, 1, have.length).setFontWeight('bold');
  var head = headerMap_(sh);
  var rows = Math.max(sh.getMaxRows() - 1, 1);
  sh.getRange(2, head.stage + 1, rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STAGES, true).setAllowInvalid(false).build());
  sh.getRange(2, head['package'] + 1, rows, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(PACKAGES, true).setAllowInvalid(false).build());
}

/* ---------- Web app ---------- */

function doGet() {
  return json_({ ok: true, service: 'ivelro-dashboard' });
}

function doPost(e) {
  var req;
  try { req = JSON.parse(e.postData.contents); } catch (err) { return json_({ ok: false, error: 'bad_request' }); }
  try {
    switch (req.action) {
      case 'login': return json_(login_(String(req.password || '')));
      case 'logout': endSession_(req.token); return json_({ ok: true });
      case 'list': requireSession_(req.token); return json_({ ok: true, clients: listClients_() });
      case 'save': requireSession_(req.token); return json_({ ok: true, client: saveClient_(req.client || {}) });
      case 'delete': requireSession_(req.token); deleteClient_(String(req.id || '')); return json_({ ok: true });
      default: return json_({ ok: false, error: 'bad_request' });
    }
  } catch (err) {
    var code = String(err && err.message || err);
    if (['signed_out', 'not_found', 'locked', 'bad_request'].indexOf(code) === -1) code = 'server_error';
    return json_({ ok: false, error: code });
  }
}

/* ---------- Login and sessions ---------- */

function login_(pw) {
  var props = PropertiesService.getScriptProperties();
  var cache = CacheService.getScriptCache();
  var salt = props.getProperty('PW_SALT'), stored = props.getProperty('PW_HASH');
  if (!salt || !stored) return { ok: false, error: 'no_password_set' };
  if (cache.get('locked')) return { ok: false, error: 'locked' };
  if (!pw || !safeEqual_(hash_(salt, pw), stored)) {
    var fails = Number(cache.get('fails') || 0) + 1;
    cache.put('fails', String(fails), FAIL_WINDOW_MIN * 60);
    if (fails >= MAX_FAILS) { cache.put('locked', '1', FAIL_WINDOW_MIN * 60); cache.remove('fails'); }
    Utilities.sleep(800);
    return { ok: false, error: fails >= MAX_FAILS ? 'locked' : 'wrong_password' };
  }
  cache.remove('fails');
  var token = Utilities.getUuid() + Utilities.getUuid().replace(/-/g, '');
  cache.put(sessionKey_(token), '1', SESSION_HOURS * 3600);
  return { ok: true, token: token, hours: SESSION_HOURS };
}

function requireSession_(token) {
  if (!token || !CacheService.getScriptCache().get(sessionKey_(String(token)))) throw new Error('signed_out');
}

function endSession_(token) {
  if (token) CacheService.getScriptCache().remove(sessionKey_(String(token)));
}

function sessionKey_(token) {
  var v = PropertiesService.getScriptProperties().getProperty('SESSION_VERSION') || '1';
  return 's' + v + '_' + hash_('session', token).slice(0, 40);
}

function bumpSessions_() {
  var props = PropertiesService.getScriptProperties();
  props.setProperty('SESSION_VERSION', String(Number(props.getProperty('SESSION_VERSION') || '1') + 1));
}

function hash_(salt, text) {
  var bytes = Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt + '|' + text, Utilities.Charset.UTF_8);
  return bytes.map(function (b) { return ('0' + (b & 255).toString(16)).slice(-2); }).join('');
}

function safeEqual_(a, b) {
  if (a.length !== b.length) return false;
  var diff = 0;
  for (var i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

/* ---------- Clients ---------- */

function sheet_() {
  var sh = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  if (!sh) { setupSheet(); sh = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME); }
  return sh;
}

function headerMap_(sh) {
  var titles = sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0];
  var map = {};
  COLUMNS.forEach(function (c) { map[c[0]] = titles.indexOf(c[1]); });
  return map;
}

function listClients_() {
  var sh = sheet_();
  var head = headerMap_(sh);
  var last = sh.getLastRow();
  if (last < 2) return [];
  var tz = Session.getScriptTimeZone();
  var values = sh.getRange(2, 1, last - 1, sh.getLastColumn()).getValues();
  var out = [];
  values.forEach(function (row) {
    var c = {};
    COLUMNS.forEach(function (col) {
      var i = head[col[0]];
      var v = i === -1 ? '' : row[i];
      if (Object.prototype.toString.call(v) === '[object Date]') v = Utilities.formatDate(v, tz, col[0] === 'updated' ? "yyyy-MM-dd'T'HH:mm" : 'yyyy-MM-dd');
      c[col[0]] = v === null || v === undefined ? '' : v;
    });
    if (String(c.id) || String(c.business)) out.push(c);
  });
  return out;
}

function clean_(key, v) {
  if (v === null || v === undefined) return '';
  if (NUMBER_KEYS.indexOf(key) !== -1) {
    if (v === '') return '';
    var n = Number(String(v).replace(',', '.'));
    return isFinite(n) ? Math.round(n * 100) / 100 : '';
  }
  var s = String(v).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, '').trim().slice(0, key === 'notes' ? 2000 : 300);
  if (DATE_KEYS.indexOf(key) !== -1) return /^\d{4}-\d{2}-\d{2}$/.test(s) ? s : '';
  if (key === 'stage') return STAGES.indexOf(s) !== -1 ? s : 'Signed';
  if (key === 'package') return PACKAGES.indexOf(s) !== -1 ? s : 'None';
  if (key === 'website' && s && !/^https?:\/\//i.test(s)) s = 'https://' + s;
  if (/^[=+\-@]/.test(s)) s = "'" + s;   // never let a value become a spreadsheet formula
  return s;
}

function saveClient_(input) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = sheet_();
    var head = headerMap_(sh);
    var c = {};
    COLUMNS.forEach(function (col) { c[col[0]] = clean_(col[0], input[col[0]]); });
    if (!c.business) throw new Error('bad_request');
    c.updated = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm");
    var rowIndex = c.id ? findRow_(sh, head, c.id) : -1;
    if (c.id && rowIndex === -1) throw new Error('not_found');
    if (!c.id) c.id = Utilities.getUuid().slice(0, 8);
    var width = sh.getLastColumn();
    var row = rowIndex === -1 ? new Array(width).fill('') : sh.getRange(rowIndex, 1, 1, width).getValues()[0];
    COLUMNS.forEach(function (col) { if (head[col[0]] !== -1) row[head[col[0]]] = c[col[0]]; });
    if (rowIndex === -1) sh.appendRow(row); else sh.getRange(rowIndex, 1, 1, width).setValues([row]);
    return c;
  } finally {
    lock.releaseLock();
  }
}

function deleteClient_(id) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var sh = sheet_();
    var r = findRow_(sh, headerMap_(sh), id);
    if (r === -1) throw new Error('not_found');
    sh.deleteRow(r);
  } finally {
    lock.releaseLock();
  }
}

function findRow_(sh, head, id) {
  var last = sh.getLastRow();
  if (!id || last < 2) return -1;
  var ids = sh.getRange(2, head.id + 1, last - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) if (String(ids[i][0]) === String(id)) return i + 2;
  return -1;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
