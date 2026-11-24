#!/usr/bin/env python3
"""Builds the legal pages of ivelro.com (policies, in English and Greek) from tools/legal/.

Run from the repository root:  python3 tools/build_legal.py [--docs OUTDIR]

The texts live in tools/legal/en/*.html and tools/legal/el/*.html (body only, no title).
Edit them there and run again; do not edit the generated pages by hand.
With --docs, it also writes one HTML file per policy to OUTDIR, ready to upload to Google Docs.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pages import ROOT, SITE, e, page  # noqa: E402

UPDATED = {'en': '24 November 2026', 'el': '24 Νοεμβρίου 2026', 'iso': '2026-11-24'}
HUB = {
    'en': dict(dir='legal', label='Legal', title='Legal information',
               desc='IVELRO policies: privacy, cookies, terms of use, terms of service, payments and refunds, support and accessibility.',
               lead='The policies that apply to our website and to the work we do for our clients. Written to be clear, not just legal.',
               updated='Last updated', other='Other policies', all='All policies'),
    'el': dict(dir='el/nomika', label='Νομικά', title='Νομικές πληροφορίες',
               desc='Οι πολιτικές της IVELRO: απόρρητο, cookies, όροι χρήσης, όροι παροχής υπηρεσιών, πληρωμές και επιστροφές, υποστήριξη και προσβασιμότητα.',
               lead='Οι πολιτικές που ισχύουν για την ιστοσελίδα μας και για τη δουλειά που κάνουμε για τους πελάτες μας. Γραμμένες για να είναι κατανοητές.',
               updated='Τελευταία ενημέρωση', other='Άλλες πολιτικές', all='Όλες οι πολιτικές'),
}
POLICIES = [
    dict(en=('privacy', 'Privacy Policy', 'How IVELRO collects, uses and protects personal data, and your rights under the GDPR.',
             'What data we collect, why, who we share it with and your rights.'),
         el=('aporrito', 'Πολιτική Απορρήτου', 'Πώς η IVELRO συλλέγει, χρησιμοποιεί και προστατεύει τα προσωπικά δεδομένα και ποια δικαιώματα έχετε σύμφωνα με τον ΓΚΠΔ.',
             'Ποια δεδομένα συλλέγουμε, γιατί, με ποιους τα μοιραζόμαστε και τα δικαιώματά σας.')),
    dict(en=('cookies', 'Cookie Policy', 'ivelro.com does not use cookies or tracking. What the services we use do, and how to control cookies.',
             'Why our website has no cookies or tracking, and how to control cookies.'),
         el=('cookies', 'Πολιτική Cookies', 'Το ivelro.com δεν χρησιμοποιεί cookies ή παρακολούθηση. Τι κάνουν οι υπηρεσίες που χρησιμοποιούμε και πώς ελέγχετε τα cookies.',
             'Γιατί η ιστοσελίδα μας δεν έχει cookies ή παρακολούθηση, και πώς τα ελέγχετε.')),
    dict(en=('terms-of-use', 'Website Terms of Use', 'The rules for using ivelro.com.',
             'The rules for using our website.'),
         el=('oroi-xrisis', 'Όροι Χρήσης Ιστοσελίδας', 'Οι κανόνες για τη χρήση του ivelro.com.',
             'Οι κανόνες για τη χρήση της ιστοσελίδας μας.')),
    dict(en=('terms-of-service', 'Terms of Service', 'The terms for IVELRO AI search presence, business automation and AI integration, local AI systems, support and maintenance.',
             'How projects work: proposals, ownership, data protection, warranty and liability.'),
         el=('oroi-ypiresion', 'Όροι Παροχής Υπηρεσιών', 'Οι όροι για την παρουσία στην αναζήτηση με AI, τους αυτοματισμούς και την ενσωμάτωση AI, τα συστήματα τοπικής AI, την υποστήριξη και τη συντήρηση της IVELRO.',
             'Πώς λειτουργούν τα έργα: προτάσεις, ιδιοκτησία, δεδομένα, εγγύηση και ευθύνη.')),
    dict(en=('payments-and-refunds', 'Payments and Refunds Policy', 'How pricing, payments, cancellations and refunds work for IVELRO projects and support.',
             'Prices, payment schedule, cancellations, refunds and the right of withdrawal.'),
         el=('pliromes-kai-epistrofes', 'Πολιτική Πληρωμών και Επιστροφών', 'Πώς λειτουργούν οι τιμές, οι πληρωμές, οι ακυρώσεις και οι επιστροφές για τα έργα και την υποστήριξη της IVELRO.',
             'Τιμές, πρόγραμμα πληρωμών, ακυρώσεις, επιστροφές και δικαίωμα υπαναχώρησης.')),
    dict(en=('support-and-maintenance', 'Support and Maintenance Policy', 'What IVELRO support packages include, how to request support and our response times.',
             'Support packages, how to ask for help and how fast we respond.'),
         el=('ypostirixi-kai-syntirisi', 'Πολιτική Υποστήριξης και Συντήρησης', 'Τι περιλαμβάνουν τα πακέτα υποστήριξης της IVELRO, πώς ζητάτε υποστήριξη και οι χρόνοι απάντησης.',
             'Πακέτα υποστήριξης, πώς ζητάτε βοήθεια και πόσο γρήγορα απαντάμε.')),
    dict(en=('accessibility', 'Accessibility Statement', 'How IVELRO makes ivelro.com accessible, our WCAG 2.1 AA status and how to report a problem.',
             'Our accessibility goal, status and how to report a barrier.'),
         el=('prosvasimotita', 'Δήλωση Προσβασιμότητας', 'Πώς η IVELRO κάνει το ivelro.com προσβάσιμο, η κατάσταση συμμόρφωσης με τις WCAG 2.1 AA και πώς αναφέρετε πρόβλημα.',
             'Ο στόχος μας για την προσβασιμότητα, η κατάστασή της και πώς αναφέρετε ένα εμπόδιο.')),
]


def body_of(lang, slug):
    with open(os.path.join(ROOT, 'tools', 'legal', lang, slug + '.html'), encoding='utf-8') as f:
        return f.read().strip()


def path_of(lang, slug=None):
    return f'{HUB[lang]["dir"]}/' + (f'{slug}/' if slug else '')


def policy_page(p, lang):
    other = 'el' if lang == 'en' else 'en'
    slug, title, desc, _ = p[lang]
    path = path_of(lang, slug)
    h = HUB[lang]
    others = '\n'.join(f'          <li><a href="../{q[lang][0]}/">{e(q[lang][1])}</a></li>' for q in POLICIES if q is not p)
    content = body_of(lang, slug).replace('\n', '\n      ')
    body = f'''    <article class="container article legal">
      <p class="label"><a href="../" style="border:0">{h["label"]}</a></p>
      <h1>{e(title)}</h1>
      <p class="meta">{h["updated"]}: <time datetime="{UPDATED["iso"]}">{UPDATED[lang]}</time></p>
      {content}
      <nav class="box" aria-label="{h["other"]}">
        <p>{h["other"]}</p>
        <ul class="legal-links">
{others}
        </ul>
      </nav>
    </article>'''
    alternates = {lang: path, other: path_of(other, p[other][0])}
    jsonld = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'description': desc, 'inLanguage': lang,
              'dateModified': UPDATED['iso'], 'url': SITE + path,
              'publisher': {'@type': 'Organization', 'name': 'IVELRO', 'url': SITE}}
    return path, page(lang, path, title, desc, alternates, body, jsonld)


def hub_page(lang):
    other = 'el' if lang == 'en' else 'en'
    h = HUB[lang]
    path = path_of(lang)
    items = '\n'.join(f'        <li><a href="{p[lang][0]}/"><b>{e(p[lang][1])}</b><span>{e(p[lang][3])}</span></a></li>' for p in POLICIES)
    body = f'''    <div class="container page-hero">
      <p class="label">{h["label"]}</p>
      <h1>{e(h["title"])}</h1>
      <p class="lead">{e(h["lead"])}</p>
      <p class="meta legal-meta">{h["updated"]}: <time datetime="{UPDATED["iso"]}">{UPDATED[lang]}</time></p>
    </div>
    <div class="container">
      <ul class="guides">
{items}
      </ul>
    </div>'''
    return path, page(lang, path, h['title'], h['desc'], {lang: path, other: path_of(other)}, body)


def doc_html(p, lang):
    """A standalone HTML version for Google Docs: absolute links, bordered tables."""
    slug, title, _, _ = p[lang]
    h = HUB[lang]
    body = body_of(lang, slug)
    body = re.sub(r'href="\.\./([a-z-]+)/"', lambda m: f'href="{SITE}{path_of(lang, m.group(1))}"', body)
    body = body.replace('<table>', '<table border="1" cellpadding="6" style="border-collapse:collapse">')
    return (f'<html><head><meta charset="utf-8"></head><body>\n<h1>{e(title)}</h1>\n'
            f'<p><i>{h["updated"]}: {UPDATED[lang]} · {SITE}{path_of(lang, slug)}</i></p>\n{body}\n</body></html>\n')


def main():
    pages = [hub_page('en'), hub_page('el')]
    for p in POLICIES:
        pages += [policy_page(p, 'en'), policy_page(p, 'el')]
    for path, content in pages:
        full = os.path.join(ROOT, path, 'index.html')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
    print('\n'.join(p for p, _ in pages))
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    for p, _ in pages:
        loc = f'<loc>{SITE}{p}</loc>'
        if loc not in sm:
            sm = sm.replace('</urlset>', f'  <url>\n    {loc}\n    <lastmod>{UPDATED["iso"]}</lastmod>\n  </url>\n</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)
    if '--docs' in sys.argv:
        out = sys.argv[sys.argv.index('--docs') + 1]
        for lang in ('en', 'el'):
            os.makedirs(os.path.join(out, lang), exist_ok=True)
            for p in POLICIES:
                with open(os.path.join(out, lang, p[lang][0] + '.html'), 'w', encoding='utf-8') as f:
                    f.write(doc_html(p, lang))
        print('Google Docs versions written to', out)


if __name__ == '__main__':
    main()
