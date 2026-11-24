#!/usr/bin/env python3
"""Builds the use-cases pages of ivelro.com (English and Greek), the redirects from retired pages,
and the sitemap. tools/build_legal.py reuses page() and adds the legal pages to the sitemap.

Run from the repository root:  python3 tools/build_pages.py && python3 tools/build_legal.py
Edit the texts here and run again; it rewrites the generated pages.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ivelro.com/'

UI = {
    'en': dict(home='IVELRO home', nav='Primary', services='Services', cases='Use cases', process='Process', legal='Legal',
               footer='Footer', tagline='AI Search Presence · Automation · Local AI', rights='All rights reserved.',
               contact='Contact us', lang_short='ΕΛ', lang_label='Ελληνικά', cases_dir='use-cases', legal_dir='legal'),
    'el': dict(home='IVELRO, αρχική', nav='Κύριο μενού', services='Υπηρεσίες', cases='Παραδείγματα', process='Διαδικασία', legal='Νομικά',
               footer='Υποσέλιδο', tagline='Αναζήτηση με AI · Αυτοματισμοί · Τοπική AI', rights='Με την επιφύλαξη παντός δικαιώματος.',
               contact='Επικοινωνήστε μαζί μας', lang_short='EN', lang_label='English', cases_dir='el/paradeigmata', legal_dir='el/nomika'),
}

# ---------- Use cases page content ----------
CASES = {
    'en': dict(
        title='Use cases: AI search presence, automation and local AI',
        desc='Practical examples of what IVELRO does for companies: AI search presence, business automation and AI integration, and private local AI systems, plus how we work.',
        label='Use cases', h1='What working with IVELRO looks like.',
        lead='Practical examples of what our three services do for a business, and how we work with companies from the first conversation onwards. The scenarios below are typical examples, not client case studies.',
        services=[
            dict(label='01 · AI Search Presence', h2='Be described accurately when customers ask AI.',
                 intro='More and more customers ask AI assistants and AI-powered search for recommendations. We make sure the information those tools find about your business is clear, consistent and trustworthy. We do not promise rankings, because no one controls how AI tools choose their answers. We make your business easy to understand and easy to recommend.',
                 outcomes=[('Accurate answers', 'AI tools describe what you do, where you work and how to reach you correctly.'),
                           ('Consistent information', 'Services, opening hours, prices and contact details match wherever they appear.'),
                           ('Clear structure', 'Your company information is published in a structured form that machines read reliably.'),
                           ('Credibility', 'Facts, credentials and reviews about your business are easy to verify.'),
                           ('Regular checks', 'We check what AI tools say about you and correct what is wrong or missing.'),
                           ('Plain reporting', 'A short report on what changed, written in business language.')],
                 examples=[('A dental practice', 'AI assistants still mention old opening hours and a branch that has closed. We correct the sources, publish clear service and location details, and check the answers again a month later.'),
                           ('A software company', 'AI tools confuse it with a company with a similar name. We clarify its company facts, products and team across its own channels and trusted directories.'),
                           ('A guesthouse', 'Travellers asking AI for quiet places to stay by the sea get an outdated description. We rewrite its key facts and amenities in clear, consistent language.')]),
            dict(label='02 · Business Automation & AI Integration', h2='Less repetitive work, fewer manual steps.',
                 intro='Most businesses lose hours every week to copying data, sending the same messages and chasing reminders. We automate that work and connect the tools you already use, then bring AI into the steps where it genuinely helps, with your people staying in control.',
                 outcomes=[('Requests handled automatically', 'Enquiries, bookings and sign-ups are recorded, confirmed and passed to the right person.'),
                           ('Connected tools', 'Email, calendars, spreadsheets, accounting and CRM share the same information.'),
                           ('Reminders and follow-ups', 'Payments, appointments and renewals are followed up on time, automatically.'),
                           ('Reports without copy-paste', 'Weekly and monthly figures are collected and sent without manual work.'),
                           ('AI where it helps', 'Draft replies, summaries and sorted messages, always reviewed by your team.'),
                           ('Fewer errors', 'Less retyping means fewer mistakes and a clearer picture of the business.')],
                 examples=[('A tutoring centre', 'Parents sign up online; each sign-up goes straight into a spreadsheet, the family gets a confirmation and payment reminders go out on their own.'),
                           ('An accounting office', 'Clients receive automatic reminders to send their documents, and every file is named and stored in the right folder.'),
                           ('A sales team', 'AI drafts replies to common enquiries from the company’s own answers, and a salesperson checks and sends them.')]),
            dict(label='03 · Local AI for Companies', h2='Your company knowledge, available to your team, privately.',
                 intro='A local AI system runs on hardware you control, in your office or on a private server, so company information stays with you. We tailor every system to the company: how many people will use it, how they work, the tools you already have and your privacy requirements. It works for a team of five as well as for a company of hundreds.',
                 outcomes=[('Answers from your own documents', 'Staff ask questions in plain language and get answers with a link to the source.'),
                           ('Faster onboarding', 'New colleagues find procedures and past work without interrupting others.'),
                           ('Routine work automated', 'First drafts, summaries and standard documents prepared in seconds.'),
                           ('Private by design', 'Data stays on your systems, with access by role or department.'),
                           ('Sized to you', 'From one capable office computer for a small team to servers for a large company.'),
                           ('Connected to your tools', 'Works with the file storage, email and systems you already use.')],
                 examples=[('A 10-person office', 'Staff ask about procedures and past projects and get answers with links to the source documents, from a system running on one computer in the office.'),
                           ('A manufacturer with 300 employees', 'Technicians search manuals and maintenance records in plain language; the system runs on the company’s own servers with access by department.'),
                           ('A law or accounting firm', 'First drafts of routine documents are prepared from approved templates, without client files ever leaving the firm.')]),
        ],
        how_label='How we work with companies', how_h2='A clear process, from first conversation to continuous improvement.',
        steps=[('Discover', 'We learn how your business works, how customers find you and where time is lost.'),
               ('Design', 'We propose a practical solution with a fixed price, built around your workflows, tools and privacy needs.'),
               ('Build', 'We set up, connect and test everything carefully, keeping you informed throughout.'),
               ('Refine', 'We launch, train your team, measure what changed and keep improving.')],
        expect_h='What you can expect',
        expect=[('A fixed-price proposal', 'You know the scope, price and timeline before any work starts.'),
                ('Plain language', 'No jargon. You understand what we build and why.'),
                ('Your data stays yours', 'We only use your information for your project, and local AI keeps it on your systems.'),
                ('Training and support', 'Your team learns to use the system, and we stay available after launch.')],
        faq_h='Frequently asked questions',
        faq=[('Can you guarantee that AI tools will recommend us?', 'No. No one can guarantee how AI tools choose or rank their answers. We make sure your information is accurate, consistent and trustworthy, which gives AI tools what they need to describe and recommend you correctly.'),
             ('Is AI search presence the same as SEO?', 'No. We do not sell traditional search engine optimisation. Our work focuses on how AI assistants and answer tools understand your company: clear facts, consistent information and signs of trust.'),
             ('Do we need new hardware for local AI?', 'Not always. A small team can often start with one capable computer, and larger companies may use their own servers. We recommend a setup after looking at your needs.'),
             ('Which tools can you connect?', 'Most tools that offer an API or export: email, calendars, spreadsheets, CRM, accounting, forms and messaging.'),
             ('How long does a project take?', 'A focused automation usually takes days to a few weeks; a local AI system a few weeks, depending on its size. The timeline is in the proposal.')],
        cta_h='Tell us what slows your business down.', cta_p='The first conversation is free. We will tell you honestly what is worth doing.'),
    'el': dict(
        title='Παραδείγματα: αναζήτηση με AI, αυτοματισμοί και τοπική AI',
        desc='Πρακτικά παραδείγματα του τι κάνει η IVELRO για τις εταιρείες: παρουσία στην αναζήτηση με AI, αυτοματισμοί και ενσωμάτωση AI, ιδιωτικά συστήματα τοπικής AI, και πώς δουλεύουμε.',
        label='Παραδείγματα', h1='Πώς είναι η συνεργασία με την IVELRO.',
        lead='Πρακτικά παραδείγματα του τι προσφέρουν οι τρεις υπηρεσίες μας σε μια επιχείρηση, και πώς συνεργαζόμαστε με τις εταιρείες από την πρώτη συζήτηση. Τα σενάρια παρακάτω είναι τυπικά παραδείγματα, όχι μελέτες πελατών.',
        services=[
            dict(label='01 · Αναζήτηση με AI', h2='Να σας περιγράφουν σωστά όταν οι πελάτες ρωτούν την AI.',
                 intro='Όλο και περισσότεροι πελάτες ζητούν προτάσεις από βοηθούς AI και από την αναζήτηση με AI. Φροντίζουμε οι πληροφορίες που βρίσκουν αυτά τα εργαλεία για την επιχείρησή σας να είναι σαφείς, συνεπείς και αξιόπιστες. Δεν υποσχόμαστε θέσεις, γιατί κανείς δεν ελέγχει πώς επιλέγουν τις απαντήσεις τους τα εργαλεία AI. Κάνουμε την επιχείρησή σας εύκολη να γίνει κατανοητή και εύκολη να προταθεί.',
                 outcomes=[('Σωστές απαντήσεις', 'Τα εργαλεία AI περιγράφουν σωστά τι κάνετε, πού δραστηριοποιείστε και πώς σας βρίσκουν.'),
                           ('Συνεπή στοιχεία', 'Υπηρεσίες, ωράριο, τιμές και στοιχεία επικοινωνίας ταιριάζουν παντού.'),
                           ('Σαφής δομή', 'Τα στοιχεία της επιχείρησης δημοσιεύονται σε δομημένη μορφή που διαβάζεται αξιόπιστα.'),
                           ('Αξιοπιστία', 'Γεγονότα, πιστοποιήσεις και κριτικές για την επιχείρησή σας επιβεβαιώνονται εύκολα.'),
                           ('Τακτικοί έλεγχοι', 'Ελέγχουμε τι λένε για εσάς τα εργαλεία AI και διορθώνουμε ό,τι είναι λάθος ή λείπει.'),
                           ('Απλή αναφορά', 'Μια σύντομη αναφορά για το τι άλλαξε, σε γλώσσα επιχείρησης.')],
                 examples=[('Ένα οδοντιατρείο', 'Οι βοηθοί AI αναφέρουν ακόμη παλιό ωράριο και ένα κατάστημα που έκλεισε. Διορθώνουμε τις πηγές, δημοσιεύουμε σαφή στοιχεία υπηρεσιών και τοποθεσίας και ελέγχουμε ξανά τις απαντήσεις έναν μήνα μετά.'),
                           ('Μια εταιρεία λογισμικού', 'Τα εργαλεία AI τη μπερδεύουν με μια εταιρεία με παρόμοιο όνομα. Ξεκαθαρίζουμε τα στοιχεία, τα προϊόντα και την ομάδα της στα δικά της κανάλια και σε αξιόπιστους καταλόγους.'),
                           ('Ένας ξενώνας', 'Οι ταξιδιώτες που ζητούν από την AI ήσυχο κατάλυμα δίπλα στη θάλασσα βλέπουν μια παλιά περιγραφή. Ξαναγράφουμε τα βασικά στοιχεία και τις παροχές του με σαφή και συνεπή γλώσσα.')]),
            dict(label='02 · Αυτοματισμοί & ενσωμάτωση AI', h2='Λιγότερη επαναλαμβανόμενη δουλειά, λιγότερα χειροκίνητα βήματα.',
                 intro='Οι περισσότερες επιχειρήσεις χάνουν ώρες κάθε εβδομάδα αντιγράφοντας στοιχεία, στέλνοντας τα ίδια μηνύματα και κυνηγώντας υπενθυμίσεις. Αυτοματοποιούμε αυτή τη δουλειά, συνδέουμε τα εργαλεία που ήδη χρησιμοποιείτε και φέρνουμε την AI στα βήματα όπου πραγματικά βοηθά, με τους ανθρώπους σας να έχουν τον έλεγχο.',
                 outcomes=[('Αιτήματα που διεκπεραιώνονται μόνα τους', 'Ερωτήματα, κρατήσεις και εγγραφές καταγράφονται, επιβεβαιώνονται και πάνε στον σωστό άνθρωπο.'),
                           ('Συνδεδεμένα εργαλεία', 'Email, ημερολόγια, υπολογιστικά φύλλα, λογιστικό και CRM μοιράζονται τα ίδια στοιχεία.'),
                           ('Υπενθυμίσεις και follow-up', 'Πληρωμές, ραντεβού και ανανεώσεις παρακολουθούνται έγκαιρα, αυτόματα.'),
                           ('Αναφορές χωρίς αντιγραφή', 'Τα εβδομαδιαία και μηνιαία στοιχεία συγκεντρώνονται και στέλνονται χωρίς χειροκίνητη δουλειά.'),
                           ('AI όπου βοηθά', 'Προσχέδια απαντήσεων, περιλήψεις και ταξινόμηση μηνυμάτων, πάντα με έλεγχο από την ομάδα σας.'),
                           ('Λιγότερα λάθη', 'Λιγότερη πληκτρολόγηση σημαίνει λιγότερα λάθη και πιο καθαρή εικόνα της επιχείρησης.')],
                 examples=[('Ένα φροντιστήριο', 'Οι γονείς κάνουν εγγραφή online· κάθε εγγραφή μπαίνει κατευθείαν σε υπολογιστικό φύλλο, η οικογένεια λαμβάνει επιβεβαίωση και οι υπενθυμίσεις πληρωμής φεύγουν μόνες τους.'),
                           ('Ένα λογιστικό γραφείο', 'Οι πελάτες λαμβάνουν αυτόματες υπενθυμίσεις να στείλουν τα έγγραφά τους, και κάθε αρχείο ονομάζεται και αποθηκεύεται στον σωστό φάκελο.'),
                           ('Μια ομάδα πωλήσεων', 'Η AI ετοιμάζει προσχέδια απαντήσεων σε συνηθισμένα ερωτήματα με βάση τις απαντήσεις της εταιρείας, και ένας πωλητής τα ελέγχει και τα στέλνει.')]),
            dict(label='03 · Τοπική AI για εταιρείες', h2='Η γνώση της εταιρείας σας, διαθέσιμη στην ομάδα σας, ιδιωτικά.',
                 intro='Ένα σύστημα τοπικής AI λειτουργεί σε εξοπλισμό που ελέγχετε εσείς, στο γραφείο σας ή σε ιδιωτικό διακομιστή, οπότε οι πληροφορίες της εταιρείας μένουν σε εσάς. Προσαρμόζουμε κάθε σύστημα στην εταιρεία: πόσοι θα το χρησιμοποιούν, πώς δουλεύουν, τα εργαλεία που ήδη έχετε και τις απαιτήσεις ιδιωτικότητας. Λειτουργεί εξίσου για μια ομάδα πέντε ατόμων και για μια εταιρεία εκατοντάδων.',
                 outcomes=[('Απαντήσεις από τα δικά σας έγγραφα', 'Οι εργαζόμενοι ρωτούν σε απλή γλώσσα και παίρνουν απάντηση με σύνδεσμο στην πηγή.'),
                           ('Πιο γρήγορη ένταξη', 'Οι νέοι συνάδελφοι βρίσκουν διαδικασίες και προηγούμενη δουλειά χωρίς να διακόπτουν τους άλλους.'),
                           ('Αυτόματη ρουτίνα', 'Πρώτα προσχέδια, περιλήψεις και τυποποιημένα έγγραφα σε δευτερόλεπτα.'),
                           ('Ιδιωτικότητα από τον σχεδιασμό', 'Τα δεδομένα μένουν στα συστήματά σας, με πρόσβαση ανά ρόλο ή τμήμα.'),
                           ('Στα μέτρα σας', 'Από έναν ισχυρό υπολογιστή γραφείου για μια μικρή ομάδα έως διακομιστές για μια μεγάλη εταιρεία.'),
                           ('Συνδεδεμένη με τα εργαλεία σας', 'Δουλεύει με την αποθήκευση αρχείων, το email και τα συστήματα που ήδη χρησιμοποιείτε.')],
                 examples=[('Ένα γραφείο 10 ατόμων', 'Οι εργαζόμενοι ρωτούν για διαδικασίες και προηγούμενα έργα και παίρνουν απαντήσεις με συνδέσμους στα έγγραφα, από ένα σύστημα που τρέχει σε έναν υπολογιστή του γραφείου.'),
                           ('Μια βιομηχανία 300 ατόμων', 'Οι τεχνικοί αναζητούν εγχειρίδια και ιστορικό συντήρησης σε απλή γλώσσα· το σύστημα τρέχει στους διακομιστές της εταιρείας με πρόσβαση ανά τμήμα.'),
                           ('Ένα δικηγορικό ή λογιστικό γραφείο', 'Τα πρώτα προσχέδια τυποποιημένων εγγράφων ετοιμάζονται από εγκεκριμένα πρότυπα, χωρίς τα αρχεία των πελατών να φεύγουν ποτέ από το γραφείο.')]),
        ],
        how_label='Πώς συνεργαζόμαστε', how_h2='Μια ξεκάθαρη διαδικασία, από την πρώτη συζήτηση έως τη συνεχή βελτίωση.',
        steps=[('Ανάλυση', 'Μαθαίνουμε πώς δουλεύει η επιχείρησή σας, πώς σας βρίσκουν οι πελάτες και πού χάνεται χρόνος.'),
               ('Σχεδιασμός', 'Προτείνουμε μια πρακτική λύση με σταθερή τιμή, γύρω από τις διαδικασίες, τα εργαλεία και τις ανάγκες ιδιωτικότητάς σας.'),
               ('Υλοποίηση', 'Στήνουμε, συνδέουμε και ελέγχουμε τα πάντα προσεκτικά, κρατώντας σας ενήμερους σε κάθε βήμα.'),
               ('Βελτίωση', 'Παραδίδουμε, εκπαιδεύουμε την ομάδα σας, μετράμε τι άλλαξε και βελτιώνουμε συνεχώς.')],
        expect_h='Τι να περιμένετε',
        expect=[('Πρόταση με σταθερή τιμή', 'Ξέρετε το αντικείμενο, την τιμή και το χρονοδιάγραμμα πριν ξεκινήσει οποιαδήποτε δουλειά.'),
                ('Απλή γλώσσα', 'Χωρίς ορολογία. Καταλαβαίνετε τι φτιάχνουμε και γιατί.'),
                ('Τα δεδομένα σας μένουν δικά σας', 'Χρησιμοποιούμε τις πληροφορίες σας μόνο για το έργο σας, και η τοπική AI τις κρατά στα συστήματά σας.'),
                ('Εκπαίδευση και υποστήριξη', 'Η ομάδα σας μαθαίνει να χρησιμοποιεί το σύστημα, και είμαστε διαθέσιμοι και μετά την παράδοση.')],
        faq_h='Συχνές ερωτήσεις',
        faq=[('Εγγυάστε ότι τα εργαλεία AI θα μας προτείνουν;', 'Όχι. Κανείς δεν μπορεί να εγγυηθεί πώς επιλέγουν ή κατατάσσουν τις απαντήσεις τους τα εργαλεία AI. Φροντίζουμε τα στοιχεία σας να είναι ακριβή, συνεπή και αξιόπιστα, ώστε τα εργαλεία AI να έχουν ό,τι χρειάζονται για να σας περιγράψουν και να σας προτείνουν σωστά.'),
             ('Είναι το ίδιο με το SEO;', 'Όχι. Δεν προσφέρουμε κλασικό SEO για μηχανές αναζήτησης. Η δουλειά μας εστιάζει στο πώς οι βοηθοί και τα εργαλεία απαντήσεων AI καταλαβαίνουν την εταιρεία σας: σαφή στοιχεία, συνέπεια και σήματα αξιοπιστίας.'),
             ('Χρειαζόμαστε νέο εξοπλισμό για την τοπική AI;', 'Όχι πάντα. Μια μικρή ομάδα συχνά ξεκινά με έναν ισχυρό υπολογιστή, και οι μεγαλύτερες εταιρείες μπορεί να χρησιμοποιήσουν τους δικούς τους διακομιστές. Προτείνουμε τη λύση αφού δούμε τις ανάγκες σας.'),
             ('Ποια εργαλεία μπορείτε να συνδέσετε;', 'Τα περισσότερα εργαλεία που προσφέρουν API ή εξαγωγή: email, ημερολόγια, υπολογιστικά φύλλα, CRM, λογιστικό, φόρμες και μηνύματα.'),
             ('Πόσο διαρκεί ένα έργο;', 'Ένας στοχευμένος αυτοματισμός συνήθως θέλει από λίγες ημέρες έως λίγες εβδομάδες· ένα σύστημα τοπικής AI λίγες εβδομάδες, ανάλογα με το μέγεθος. Το χρονοδιάγραμμα είναι στην πρόταση.')],
        cta_h='Πείτε μας τι καθυστερεί την επιχείρησή σας.', cta_p='Η πρώτη συζήτηση είναι δωρεάν. Θα σας πούμε ειλικρινά τι αξίζει να γίνει.'),
}

# Pages that no longer exist, and where they now point
REDIRECTS = {
    'en': ['portfolio/', 'portfolio/dental/', 'portfolio/frontistirio/', 'portfolio/guesthouse/', 'portfolio/taverna/',
           'websites/', 'websites/tutoring-centres/', 'websites/clinics/', 'websites/restaurants/', 'websites/guesthouses/'],
    'el': ['el/portfolio/', 'el/istoselides/', 'el/istoselides/frontistiria/', 'el/istoselides/iatreia/',
           'el/istoselides/estiatoria/', 'el/istoselides/katalymata/', 'el/odigoi/', 'el/odigoi/istoselida-frontistiriou/'],
}


def e(s):
    return html.escape(s, quote=True)


def page(lang, path, title, desc, alternates, body, jsonld=None, extra_head=''):
    depth = path.count('/')
    up = '../' * depth
    home = up if lang == 'en' else up + 'el/'
    u = UI[lang]
    other_lang = 'el' if lang == 'en' else 'en'
    other = alternates.get(other_lang)
    alt_links = ''.join(f'\n  <link rel="alternate" hreflang="{k}" href="{SITE}{v}">' for k, v in alternates.items())
    if 'en' in alternates:
        alt_links += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{alternates["en"]}">'
    lang_link = (f'\n        <a class="lang" href="{up}{other}" lang="{other_lang}" hreflang="{other_lang}" aria-label="{u["lang_label"]}">{u["lang_short"]}</a>'
                 if other is not None else '')
    fonts = f'\n  <link rel="stylesheet" href="{up}assets/fonts/commissioner.css">' if lang == 'el' else ''
    ld = f'\n  <script type="application/ld+json">\n{json.dumps(jsonld, ensure_ascii=False, indent=2)}\n  </script>' if jsonld else ''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} | IVELRO</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#0a0a0a">
  <link rel="canonical" href="{SITE}{path}">{alt_links}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="IVELRO">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{SITE}{path}">
  <meta property="og:image" content="{SITE}assets/img/og-image.png">
  <link rel="icon" href="{up}assets/img/favicon.svg" type="image/svg+xml">
  <link rel="preload" href="{up}assets/fonts/jost-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="{up}assets/fonts/jost.css">{fonts}
  <link rel="stylesheet" href="{up}assets/css/style.css">
  <link rel="stylesheet" href="{up}assets/css/pages.css">{ld}{extra_head}
</head>
<body>
  <header class="site-header is-scrolled">
    <div class="container header-inner">
      <a class="brand" href="{home}" aria-label="{u["home"]}">
        <img class="brand-mark" src="{up}assets/img/mark.png" alt="" width="22" height="22">
        <img class="brand-word" src="{up}assets/img/wordmark.png" alt="IVELRO" width="118" height="13">
      </a>
      <nav class="nav" aria-label="{u["nav"]}">
        <a href="{home}#services">{u["services"]}</a>
        <a href="{up}{u["cases_dir"]}/">{u["cases"]}</a>{lang_link}
      </nav>
    </div>
  </header>

  <main>
{body}
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <img src="{up}assets/img/wordmark.png" alt="IVELRO" width="118" height="13">
          <p>{u["tagline"]}</p>
        </div>
        <nav class="footer-nav" aria-label="{u["footer"]}">
          <a href="{home}#services">{u["services"]}</a>
          <a href="{home}#process">{u["process"]}</a>
          <a href="{up}{u["cases_dir"]}/">{u["cases"]}</a>
          <a href="{up}{u["legal_dir"]}/">{u["legal"]}</a>
        </nav>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 IVELRO. {u["rights"]}</span>
        <a href="{home}" class="to-top">ivelro.com</a>
      </div>
    </div>
  </footer>
</body>
</html>
'''


def cases_page(lang):
    c = CASES[lang]
    u = UI[lang]
    path = u['cases_dir'] + '/'
    up = '../' * path.count('/')
    home = up if lang == 'en' else up + 'el/'
    blocks = []
    for s in c['services']:
        outs = '\n'.join(f'          <div><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in s['outcomes'])
        exs = '\n'.join(f'          <li><span>{i:02d}</span><div><b>{e(h)}</b><p>{e(p)}</p></div></li>' for i, (h, p) in enumerate(s['examples'], 1))
        blocks.append(f'''    <section class="block">
      <div class="container">
        <p class="label">{e(s["label"])}</p>
        <h2>{e(s["h2"])}</h2>
        <p class="intro">{e(s["intro"])}</p>
        <div class="features">
{outs}
        </div>
        <ul class="autos" aria-label="{'Example scenarios' if lang == 'en' else 'Ενδεικτικά σενάρια'}">
{exs}
        </ul>
      </div>
    </section>''')
    steps = '\n'.join(f'          <li><b>{e(h)}</b><p>{e(p)}</p></li>' for h, p in c['steps'])
    expect = '\n'.join(f'          <div><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in c['expect'])
    faq = '\n'.join(f'          <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    body = f'''    <div class="container page-hero">
      <p class="label">{e(c["label"])}</p>
      <h1>{e(c["h1"])}</h1>
      <p class="lead">{e(c["lead"])}</p>
    </div>
{chr(10).join(blocks)}
    <section class="block" id="how">
      <div class="container">
        <p class="label">{e(c["how_label"])}</p>
        <h2>{e(c["how_h2"])}</h2>
        <ol class="mini-steps">
{steps}
        </ol>
        <h2 class="sub-h">{e(c["expect_h"])}</h2>
        <div class="features features-4">
{expect}
        </div>
      </div>
    </section>
    <section class="block">
      <div class="container">
        <h2>{e(c["faq_h"])}</h2>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>
    <section class="cta-band">
      <div class="container">
        <h2>{e(c["cta_h"])}</h2>
        <p>{e(c["cta_p"])}</p>
        <div class="cta-row">
          <a class="btn btn-solid" href="{home}#services">{e(u["services"])} <span aria-hidden="true">→</span></a>
          <a class="btn" href="{home}#contact" data-contact-cta hidden>{e(u["contact"])}</a>
        </div>
      </div>
    </section>'''
    jsonld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang,
              'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]}
    alternates = {'en': UI['en']['cases_dir'] + '/', 'el': UI['el']['cases_dir'] + '/'}
    return path, page(lang, path, c['title'], c['desc'], alternates, body, jsonld)


def redirect_page(lang, path):
    target = UI[lang]['cases_dir'] + '/'
    up = '../' * path.count('/')
    text = 'This page has moved.' if lang == 'en' else 'Η σελίδα μεταφέρθηκε.'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="robots" content="noindex, follow">
  <title>IVELRO</title>
  <link rel="canonical" href="{SITE}{target}">
  <meta http-equiv="refresh" content="0; url={up}{target}">
</head>
<body>
  <p>{text} <a href="{up}{target}">{SITE}{target}</a></p>
</body>
</html>
'''


def main():
    pages = [cases_page('en'), cases_page('el')]
    for path, content in pages + [(p, redirect_page(lang, p)) for lang, ps in REDIRECTS.items() for p in ps]:
        full = os.path.join(ROOT, path, 'index.html')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
    print('\n'.join(p for p, _ in pages))
    # Sitemap: home pages and use cases; build_legal.py adds the legal pages
    urls = ['', 'el/'] + [p for p, _ in pages]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += ''.join(f'  <url>\n    <loc>{SITE}{u}</loc>\n  </url>\n' for u in urls) + '</urlset>\n'
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sm)


if __name__ == '__main__':
    main()
