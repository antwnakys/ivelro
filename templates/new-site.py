#!/usr/bin/env python3
"""Create a new client website from the IVELRO starter template.

Usage:
  python3 templates/new-site.py templates/example-client.json ../client-sites/my-client

1. Copy templates/example-client.json, fill in the client's details.
2. Run the command above. It copies the starter, fills in every {{PLACEHOLDER}} it can,
   builds the opening hours (table, live "open now" status, Google data) and lists anything left to fill.
3. Replace assets/img/placeholder.svg with real photos, check the texts, then follow docs/launch-checklist.md.
"""
import datetime
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STARTER = os.path.join(HERE, 'starter')
TEXT_EXT = {'.html', '.css', '.js', '.txt', '.xml', '.svg'}
SCHEMA_DAYS = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
MONTHS_EL = ['Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου', 'Ιουλίου',
             'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου']


def hours_values(hours):
    """hours: list of {"label": "Δευτέρα–Παρασκευή", "days": [1,2,3,4,5], "times": [["09:00","17:00"]]}"""
    by_day, rows, schema = {}, [], []
    for h in hours:
        times = h.get('times', [])
        for d in h['days']:
            by_day[str(d)] = times
        text = ', '.join(f'{a}–{b}' for a, b in times) or 'Κλειστά'
        rows.append(f'<tr data-day="{" ".join(str(d) for d in h["days"])}"><th scope="row">{h["label"]}</th><td>{text}</td></tr>')
        days = ','.join(SCHEMA_DAYS[d] for d in h['days'])
        schema += [f'{days} {a}-{b}' for a, b in times]
    return (json.dumps(by_day, ensure_ascii=False),
            '\n            '.join(rows),
            json.dumps(schema, ensure_ascii=False))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    cfg_path, out = sys.argv[1], sys.argv[2]
    with open(cfg_path, encoding='utf-8') as f:
        cfg = json.load(f)
    if os.path.exists(out):
        sys.exit(f'{out} already exists. Choose a new folder.')

    values = {k.upper(): str(v) for k, v in cfg.items() if not isinstance(v, (list, dict))}
    phone = cfg.get('phone', '')
    digits = re.sub(r'[^0-9+]', '', phone)
    values.setdefault('PHONE_INTL', digits if digits.startswith('+') else '+30' + digits)
    values.setdefault('INITIAL', cfg.get('business_name', '?')[:1].upper())
    today = datetime.date.today()
    values['YEAR'] = str(today.year)
    values['TODAY'] = f'{today.day} {MONTHS_EL[today.month - 1]} {today.year}'
    if 'hours' in cfg:
        values['HOURS_JSON'], values['HOURS_ROWS'], values['OPENING_HOURS_SCHEMA'] = hours_values(cfg['hours'])

    shutil.copytree(STARTER, out)
    left = set()
    for root, _, files in os.walk(out):
        for name in files:
            path = os.path.join(root, name)
            if os.path.splitext(name)[1] not in TEXT_EXT:
                continue
            with open(path, encoding='utf-8') as f:
                s = f.read()
            s = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: values.get(m.group(1), m.group(0)), s)
            left.update(re.findall(r'\{\{([A-Z0-9_]+)\}\}', s))
            with open(path, 'w', encoding='utf-8') as f:
                f.write(s)

    print(f'Created {out}')
    if left:
        print('Still to fill in (search the files for these):')
        for k in sorted(left):
            print('  {{' + k + '}}')
    else:
        print('All placeholders filled.')


if __name__ == '__main__':
    main()
