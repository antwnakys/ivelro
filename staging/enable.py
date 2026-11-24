#!/usr/bin/env python3
"""Switch on the ivelro.com contact section and (optionally) visitor statistics.

The policies (privacy, cookies, terms...) are already published at /legal/ and /el/nomika/ (tools/build_legal.py).

Usage, from the repository root:
  python3 staging/enable.py --email info@ivelro.com --phone "+30 69X XXX XXXX" --key WEB3FORMS_ACCESS_KEY
  python3 staging/enable.py --analytics-token CLOUDFLARE_BEACON_TOKEN

Each part can run on its own and is safe to run twice (it skips what is already there).
"""
import argparse
import datetime
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGING = os.path.join(ROOT, 'staging')
MONTHS_EL = ['Ιανουαρίου', 'Φεβρουαρίου', 'Μαρτίου', 'Απριλίου', 'Μαΐου', 'Ιουνίου', 'Ιουλίου',
             'Αυγούστου', 'Σεπτεμβρίου', 'Οκτωβρίου', 'Νοεμβρίου', 'Δεκεμβρίου']


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f:
        f.write(s)


def fill(text, a):
    today = datetime.date.today()
    tel = re.sub(r'[^0-9+]', '', a.phone)
    return (text.replace('{{EMAIL}}', a.email).replace('{{PHONE}}', a.phone).replace('{{TEL}}', tel)
            .replace('{{WEB3FORMS_KEY}}', a.key)
            .replace('{{DATE_EN}}', today.strftime('%-d %B %Y'))
            .replace('{{DATE_EL}}', f'{today.day} {MONTHS_EL[today.month - 1]} {today.year}'))


def enable_contact(a):
    for page, section, prefix, footer_old, footer_new in [
        ('index.html', 'contact-en.html', '',
         '          <a href="portfolio/">Work</a>\n',
         '          <a href="portfolio/">Work</a>\n          <a href="#contact">Contact</a>\n'),
        ('el/index.html', 'contact-el.html', '../',
         '          <a href="portfolio/">Έργα</a>\n',
         '          <a href="portfolio/">Έργα</a>\n          <a href="#contact">Επικοινωνία</a>\n'),
    ]:
        s = read(page)
        if 'id="contact"' in s:
            print(f'{page}: contact section already there, skipped')
            continue
        block = fill(open(os.path.join(STAGING, section), encoding='utf-8').read(), a)
        anchor = '    <section class="closing">'
        assert anchor in s, f'{page}: could not find where to insert the contact section'
        s = s.replace(anchor, block + anchor, 1)
        main_js = f'<script src="{prefix}assets/js/main.js" defer></script>'
        assert main_js in s
        s = s.replace(main_js, main_js + f'\n  <script src="{prefix}assets/js/contact.js" defer></script>', 1)
        assert footer_old in s, f'{page}: footer links not found'
        s = s.replace(footer_old, footer_new, 1)
        write(page, s)
        print(f'{page}: contact section added')

    shutil.copy(os.path.join(STAGING, 'contact.js'), os.path.join(ROOT, 'assets/js/contact.js'))
    css = read('assets/css/style.css')
    if '/* ---------- Contact ---------- */' not in css:
        write('assets/css/style.css', css.rstrip('\n') + '\n' + open(os.path.join(STAGING, 'contact.css'), encoding='utf-8').read())
    print('Styles and form script installed.')

    # Show the "Contact us" buttons on the industry pages and guides
    for base in ('websites', 'el/istoselides', 'el/odigoi'):
        for root, _, files in os.walk(os.path.join(ROOT, base)):
            for name in files:
                if name.endswith('.html'):
                    p = os.path.relpath(os.path.join(root, name), ROOT)
                    s = read(p)
                    if ' data-contact-cta hidden' in s:
                        write(p, s.replace(' data-contact-cta hidden', ' data-contact-cta'))
    print('Contact buttons switched on in the industry pages and guides.')


def enable_analytics(token):
    tag = ("<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
           "data-cf-beacon='{\"token\": \"%s\"}'></script>" % token)
    pages = ['index.html', 'el/index.html', 'portfolio/index.html', 'el/portfolio/index.html', '404.html']
    for p in pages:
        if not os.path.exists(os.path.join(ROOT, p)):
            continue
        s = read(p)
        if 'cloudflareinsights' in s:
            print(f'{p}: analytics already there, skipped')
            continue
        s = s.replace('</body>', '  ' + tag + '\n</body>', 1)
        write(p, s)
        print(f'{p}: analytics added')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--email')
    ap.add_argument('--phone')
    ap.add_argument('--key', help='Web3Forms access key')
    ap.add_argument('--analytics-token', help='Cloudflare Web Analytics token')
    a = ap.parse_args()
    contact_args = [a.email, a.phone, a.key]
    if any(contact_args) and not all(contact_args):
        sys.exit('For the contact section, give all three: --email, --phone and --key.')
    if not any(contact_args) and not a.analytics_token:
        ap.print_help()
        sys.exit(1)
    if all(contact_args):
        enable_contact(a)
    if a.analytics_token:
        enable_analytics(a.analytics_token)


if __name__ == '__main__':
    main()
