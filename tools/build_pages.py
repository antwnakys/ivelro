#!/usr/bin/env python3
"""Builds the industry pages, overview pages and guides of ivelro.com from the content below.

Run from the repository root:  python3 tools/build_pages.py
Edit the texts here and run again; it rewrites the generated pages.
"""
import html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ivelro.com/'

UI = {
    'en': dict(home='IVELRO home', nav='Primary', services='Services', work='Work', solutions='Industries',
               footer='Footer', tagline='Intelligent Automation. Digital Innovation.', rights='All rights reserved.',
               see='See the sample website', contact='Contact us', included='What your website includes',
               autos='Automation that saves you time', how='How we work', faq='Frequently asked questions',
               cta_t='Want a website like this for your business?', cta_p='Tell us about your business. The first conversation is free.',
               steps=[('Free conversation', 'We learn how your business works and what you need.'),
                      ('Design and offer', 'A clear plan and a fixed price before we start.'),
                      ('Build', 'We build, connect the automations and test everything on phones.'),
                      ('Launch and support', 'We put it live, get it on Google and keep it running.')],
               other='Other industries', sample='Sample website', open='Open →', lang_short='ΕΛ', lang_label='Ελληνικά'),
    'el': dict(home='IVELRO, αρχική', nav='Κύριο μενού', services='Υπηρεσίες', work='Έργα', solutions='Κλάδοι',
               footer='Υποσέλιδο', tagline='Ευφυής Αυτοματοποίηση. Ψηφιακή Καινοτομία.', rights='Με την επιφύλαξη παντός δικαιώματος.',
               see='Δείτε το δείγμα ιστοσελίδας', contact='Επικοινωνήστε μαζί μας', included='Τι περιλαμβάνει η ιστοσελίδα σας',
               autos='Αυτοματισμοί που σας γλιτώνουν χρόνο', how='Πώς δουλεύουμε', faq='Συχνές ερωτήσεις',
               cta_t='Θέλετε μια τέτοια ιστοσελίδα για την επιχείρησή σας;', cta_p='Πείτε μας για την επιχείρησή σας. Η πρώτη συζήτηση είναι δωρεάν.',
               steps=[('Δωρεάν συζήτηση', 'Μαθαίνουμε πώς δουλεύει η επιχείρησή σας και τι χρειάζεστε.'),
                      ('Σχέδιο και προσφορά', 'Ξεκάθαρο πλάνο και σταθερή τιμή πριν ξεκινήσουμε.'),
                      ('Κατασκευή', 'Φτιάχνουμε, συνδέουμε τους αυτοματισμούς και ελέγχουμε τα πάντα στο κινητό.'),
                      ('Παράδοση και υποστήριξη', 'Τη βάζουμε online, στη Google, και τη φροντίζουμε.')],
               other='Άλλοι κλάδοι', sample='Δείγμα ιστοσελίδας', open='Άνοιγμα →', lang_short='EN', lang_label='English'),
}

INDUSTRIES = [
    dict(key='tutoring', sample='frontistirio', en_slug='tutoring-centres', el_slug='frontistiria',
         en=dict(name='Tutoring centres', title='Websites for tutoring centres',
                 desc='Websites for tutoring centres: classes and timetables, online signup with automatic confirmation and a progress page for parents.',
                 h1='Websites for tutoring centres that fill your classes',
                 lead='Parents compare tutoring centres online before they call. We build a clear, fast website that shows your classes, your results and your teachers, and lets parents sign up in a minute.',
                 features=[('Classes by school year', 'Gymnasio, Lykeio and Panhellenic exams, with example weekly timetables.'),
                           ('Online signup', 'Parents fill in a short form instead of calling during class hours.'),
                           ('Progress page for parents', 'Grades, absences and the next test, always up to date.'),
                           ('Results and announcements', 'Successful students, exam papers and news in one place.'),
                           ('Perfect on a phone', 'Most parents search on their phone. Every page is built for it first.'),
                           ('Found on Google', 'Set up on Google Search and Maps, so local parents find you.')],
                 autos=[('Automatic signup confirmation', 'Every signup goes into one list and the parent gets an email straight away.'),
                        ('SMS to parents', 'Absences and upcoming tests sent automatically, no phone calls.'),
                        ('Diagnostic test bookings', 'Parents choose a time for the free diagnostic test online.')],
                 faq=[('How long does it take?', 'Usually two to four weeks, depending on how quickly we receive texts and photos.'),
                      ('Can I update announcements myself?', 'Yes. We show you how, or we do it for you with a monthly support plan.'),
                      ('What do you need from us?', 'Your logo, a few photos and the basic information. We help with the texts.')]),
         el=dict(name='Φροντιστήρια', title='Ιστοσελίδες για φροντιστήρια',
                 desc='Κατασκευή ιστοσελίδας για φροντιστήριο: τμήματα και πρόγραμμα, ηλεκτρονική εγγραφή με αυτόματη επιβεβαίωση και καρτέλα προόδου για γονείς.',
                 h1='Ιστοσελίδες για φροντιστήρια που γεμίζουν τα τμήματα',
                 lead='Οι γονείς συγκρίνουν φροντιστήρια στο internet πριν τηλεφωνήσουν. Φτιάχνουμε μια καθαρή, γρήγορη ιστοσελίδα που δείχνει τα τμήματα, τους επιτυχόντες και τους καθηγητές σας, και επιτρέπει εγγραφή σε ένα λεπτό.',
                 features=[('Τμήματα ανά τάξη', 'Γυμνάσιο, Λύκειο και Πανελλαδικές, με ενδεικτικό εβδομαδιαίο πρόγραμμα.'),
                           ('Ηλεκτρονική εγγραφή', 'Οι γονείς συμπληρώνουν μια σύντομη φόρμα αντί να τηλεφωνούν την ώρα του μαθήματος.'),
                           ('Καρτέλα προόδου για γονείς', 'Βαθμοί, απουσίες και επόμενο διαγώνισμα, πάντα ενημερωμένα.'),
                           ('Επιτυχόντες και ανακοινώσεις', 'Επιτυχόντες, θέματα εξετάσεων και νέα σε ένα σημείο.'),
                           ('Τέλεια στο κινητό', 'Οι περισσότεροι γονείς ψάχνουν από το κινητό. Κάθε σελίδα φτιάχνεται πρώτα για αυτό.'),
                           ('Εμφάνιση στη Google', 'Ρύθμιση στην αναζήτηση και στους χάρτες της Google, για να σας βρίσκουν οι γονείς της περιοχής.')],
                 autos=[('Αυτόματη επιβεβαίωση εγγραφής', 'Κάθε εγγραφή μπαίνει σε μία λίστα και ο γονέας λαμβάνει αμέσως email.'),
                        ('SMS στους γονείς', 'Απουσίες και επόμενα διαγωνίσματα στέλνονται αυτόματα, χωρίς τηλέφωνα.'),
                        ('Κλείσιμο διαγνωστικού τεστ', 'Οι γονείς διαλέγουν ώρα για το δωρεάν διαγνωστικό online.')],
                 faq=[('Πόσο χρόνο χρειάζεται;', 'Συνήθως δύο έως τέσσερις εβδομάδες, ανάλογα με το πόσο γρήγορα έχουμε κείμενα και φωτογραφίες.'),
                      ('Μπορώ να αλλάζω μόνος μου τις ανακοινώσεις;', 'Ναι. Σας δείχνουμε πώς, ή το κάνουμε εμείς με μηνιαία υποστήριξη.'),
                      ('Τι χρειάζεστε από εμάς;', 'Το λογότυπο, μερικές φωτογραφίες και τα βασικά στοιχεία. Στα κείμενα βοηθάμε εμείς.')])),
    dict(key='clinics', sample='dental', en_slug='clinics', el_slug='iatreia',
         en=dict(name='Clinics and practices', title='Websites for clinics and dental practices',
                 desc='Websites for clinics, dental practices and physiotherapists: services and prices, live opening hours and online appointment requests with SMS confirmation.',
                 h1='Websites for clinics that make booking easy',
                 lead='Patients want three things: what you treat, when you are open and how to book. We build a calm, trustworthy website that answers all three and takes appointment requests day and night.',
                 features=[('Services and prices', 'Clear treatments with indicative prices, so patients arrive informed.'),
                           ('Live opening hours', 'Shows "open now" and highlights today, always correct.'),
                           ('Your team', 'Doctors and therapists with their background, to build trust before the first visit.'),
                           ('Appointment requests', 'Patients choose a reason and a time in under a minute.'),
                           ('Directions and map', 'Address, nearest metro and parking, on every phone.'),
                           ('Found on Google', 'Set up on Google Search and Maps for searches in your area.')],
                 autos=[('Instant booking notification', 'Each request reaches you at once and the patient gets an SMS confirmation.'),
                        ('Reminder the day before', 'An automatic reminder means fewer missed appointments.'),
                        ('Review requests', 'After the visit, patients get a polite request to leave a Google review.')],
                 faq=[('Is patient data safe?', 'The form collects only what is needed to call the patient back, with a clear privacy policy.'),
                      ('Can it connect to my calendar?', 'Yes. Requests can go straight into a Google Calendar or a shared sheet.'),
                      ('How long does it take?', 'Usually two to four weeks.')]),
         el=dict(name='Ιατρεία', title='Ιστοσελίδες για ιατρεία και οδοντιατρεία',
                 desc='Κατασκευή ιστοσελίδας για ιατρείο, οδοντιατρείο ή φυσικοθεραπευτήριο: υπηρεσίες και τιμές, ωράριο σε πραγματικό χρόνο και αίτημα ραντεβού με επιβεβαίωση SMS.',
                 h1='Ιστοσελίδες για ιατρεία που κάνουν το ραντεβού εύκολο',
                 lead='Οι ασθενείς θέλουν τρία πράγματα: τι θεραπεύετε, πότε είστε ανοιχτά και πώς κλείνουν ραντεβού. Φτιάχνουμε μια ήρεμη, αξιόπιστη ιστοσελίδα που απαντά και στα τρία και δέχεται αιτήματα μέρα και νύχτα.',
                 features=[('Υπηρεσίες και τιμές', 'Σαφείς θεραπείες με ενδεικτικές τιμές, για να έρχονται οι ασθενείς ενημερωμένοι.'),
                           ('Ωράριο σε πραγματικό χρόνο', 'Δείχνει «ανοιχτά τώρα» και τη σημερινή μέρα, πάντα σωστά.'),
                           ('Η ομάδα σας', 'Γιατροί και θεραπευτές με τις σπουδές τους, για εμπιστοσύνη πριν την πρώτη επίσκεψη.'),
                           ('Αίτημα ραντεβού', 'Ο ασθενής διαλέγει λόγο και ώρα σε λιγότερο από ένα λεπτό.'),
                           ('Οδηγίες και χάρτης', 'Διεύθυνση, κοντινότερο μετρό και στάθμευση, σε κάθε κινητό.'),
                           ('Εμφάνιση στη Google', 'Ρύθμιση στην αναζήτηση και στους χάρτες της Google για την περιοχή σας.')],
                 autos=[('Άμεση ειδοποίηση για κάθε ραντεβού', 'Κάθε αίτημα σας φτάνει αμέσως και ο ασθενής λαμβάνει SMS επιβεβαίωσης.'),
                        ('Υπενθύμιση την προηγούμενη μέρα', 'Η αυτόματη υπενθύμιση σημαίνει λιγότερα χαμένα ραντεβού.'),
                        ('Αίτημα κριτικής', 'Μετά την επίσκεψη, ο ασθενής λαμβάνει ευγενικό αίτημα για κριτική στη Google.')],
                 faq=[('Είναι ασφαλή τα στοιχεία των ασθενών;', 'Η φόρμα ζητά μόνο ό,τι χρειάζεται για να καλέσετε τον ασθενή, με σαφή πολιτική απορρήτου.'),
                      ('Συνδέεται με το ημερολόγιό μου;', 'Ναι. Τα αιτήματα μπορούν να πηγαίνουν κατευθείαν σε Google Calendar ή σε κοινό φύλλο.'),
                      ('Πόσο χρόνο χρειάζεται;', 'Συνήθως δύο έως τέσσερις εβδομάδες.')])),
    dict(key='restaurants', sample='taverna', en_slug='restaurants', el_slug='estiatoria',
         en=dict(name='Restaurants and tavernas', title='Websites for restaurants and tavernas',
                 desc='Websites for restaurants, tavernas and cafés: a bilingual menu with prices, today\'s specials and online table reservations with an SMS reminder.',
                 h1='Websites for restaurants that fill your tables',
                 lead='Locals and tourists decide where to eat on their phone, in seconds. We build a website with your menu, your story and online reservations, in Greek and English.',
                 features=[('Menu with prices', 'Greek and English, with vegetarian and allergen markers.'),
                           ("Today's specials", 'Change the daily dishes in seconds, no technical knowledge needed.'),
                           ('Online reservations', 'Guests choose day, time and number of people in under a minute.'),
                           ('Open now', 'Opening hours that always show whether you are open right now.'),
                           ('Your story and photos', 'What makes your place special, told well.'),
                           ('Found on Google Maps', 'Set up so hungry people nearby find you first.')],
                 autos=[('Reservations straight into your book', 'Each booking appears at once and the guest gets an SMS confirmation.'),
                        ('Reminder on the day', 'Fewer no-shows with an automatic reminder.'),
                        ('Menu from a simple sheet', 'Update prices and dishes in a Google Sheet; the website follows.')],
                 faq=[('Do I pay commission on reservations?', 'No. Reservations come straight to you, with no platform fees.'),
                      ('Can tourists read it?', 'Yes. Menu and booking work in Greek and English.'),
                      ('How long does it take?', 'Usually two to three weeks.')]),
         el=dict(name='Εστιατόρια και ταβέρνες', title='Ιστοσελίδες για εστιατόρια και ταβέρνες',
                 desc='Κατασκευή ιστοσελίδας για εστιατόριο, ταβέρνα ή καφέ: δίγλωσσο μενού με τιμές, πιάτα ημέρας και online κρατήσεις με υπενθύμιση SMS.',
                 h1='Ιστοσελίδες για εστιατόρια που γεμίζουν τα τραπέζια',
                 lead='Ντόπιοι και τουρίστες αποφασίζουν πού θα φάνε από το κινητό, σε δευτερόλεπτα. Φτιάχνουμε ιστοσελίδα με το μενού, την ιστορία σας και online κρατήσεις, στα ελληνικά και στα αγγλικά.',
                 features=[('Μενού με τιμές', 'Ελληνικά και αγγλικά, με σήμανση για χορτοφαγικά και αλλεργιογόνα.'),
                           ('Πιάτα ημέρας', 'Αλλάζετε τα μαγειρευτά της ημέρας σε δευτερόλεπτα, χωρίς τεχνικές γνώσεις.'),
                           ('Online κρατήσεις', 'Ο πελάτης διαλέγει μέρα, ώρα και άτομα σε λιγότερο από ένα λεπτό.'),
                           ('Ανοιχτά τώρα', 'Ωράριο που δείχνει πάντα αν είστε ανοιχτά αυτή τη στιγμή.'),
                           ('Η ιστορία και οι φωτογραφίες σας', 'Τι κάνει το μαγαζί σας ξεχωριστό, ειπωμένο σωστά.'),
                           ('Εμφάνιση στους χάρτες της Google', 'Ρύθμιση ώστε να σας βρίσκουν πρώτους όσοι ψάχνουν φαγητό κοντά.')],
                 autos=[('Κρατήσεις κατευθείαν στο βιβλίο σας', 'Κάθε κράτηση εμφανίζεται αμέσως και ο πελάτης λαμβάνει SMS επιβεβαίωσης.'),
                        ('Υπενθύμιση την ημέρα της κράτησης', 'Λιγότερα «άδεια» τραπέζια με αυτόματη υπενθύμιση.'),
                        ('Μενού από ένα απλό φύλλο', 'Αλλάζετε τιμές και πιάτα σε ένα Google Sheet και η ιστοσελίδα ενημερώνεται.')],
                 faq=[('Πληρώνω προμήθεια για τις κρατήσεις;', 'Όχι. Οι κρατήσεις έρχονται απευθείας σε εσάς, χωρίς χρεώσεις πλατφόρμας.'),
                      ('Μπορούν να το διαβάσουν οι τουρίστες;', 'Ναι. Μενού και κρατήσεις λειτουργούν στα ελληνικά και στα αγγλικά.'),
                      ('Πόσο χρόνο χρειάζεται;', 'Συνήθως δύο έως τρεις εβδομάδες.')])),
    dict(key='guesthouses', sample='guesthouse', en_slug='guesthouses', el_slug='katalymata',
         en=dict(name='Guesthouses and rentals', title='Websites for guesthouses and holiday rentals in Greece',
                 desc='Websites for guesthouses, small hotels and holiday rentals: rooms and prices, direct booking requests without platform commission, in Greek and English.',
                 h1='Websites for guesthouses that bring direct bookings',
                 lead='Every booking through a platform costs you 15–20% in commission. A good website of your own turns returning guests and Google searches into direct bookings.',
                 features=[('Rooms and prices', 'Each room with its size, view, beds and price.'),
                           ('Direct booking requests', 'Guests check dates and send a request without platform fees.'),
                           ('Greek and English', 'Built for international guests from day one.'),
                           ('Getting here', 'Directions by car, bus and from the airport, with a map.'),
                           ('Guest reviews', 'Show what guests say, and link to your Google reviews.'),
                           ('Found on Google', 'Set up on Google Search and Maps for your area.')],
                 autos=[('Instant reply to every request', 'Guests get an automatic reply and you get the details at once.'),
                        ('Arrival information', 'An email with directions and check-in details before arrival.'),
                        ('Review request after the stay', 'A friendly message asking happy guests for a review.')],
                 faq=[('Will it replace Booking.com?', 'It works alongside it. The goal is more direct bookings, especially from returning guests.'),
                      ('Can it show availability?', 'Yes. We can connect a simple calendar or your channel manager.'),
                      ('How long does it take?', 'Usually two to four weeks.')]),
         el=dict(name='Καταλύματα', title='Ιστοσελίδες για καταλύματα και ενοικιαζόμενα δωμάτια',
                 desc='Κατασκευή ιστοσελίδας για ξενώνα, μικρό ξενοδοχείο ή ενοικιαζόμενα: δωμάτια και τιμές, απευθείας κρατήσεις χωρίς προμήθεια πλατφόρμας, στα ελληνικά και στα αγγλικά.',
                 h1='Ιστοσελίδες για καταλύματα που φέρνουν απευθείας κρατήσεις',
                 lead='Κάθε κράτηση μέσω πλατφόρμας σας κοστίζει 15–20% προμήθεια. Μια καλή δική σας ιστοσελίδα μετατρέπει τους επαναλαμβανόμενους επισκέπτες και τις αναζητήσεις στη Google σε απευθείας κρατήσεις.',
                 features=[('Δωμάτια και τιμές', 'Κάθε δωμάτιο με τετραγωνικά, θέα, κρεβάτια και τιμή.'),
                           ('Απευθείας κρατήσεις', 'Ο επισκέπτης ελέγχει ημερομηνίες και στέλνει αίτημα χωρίς χρεώσεις πλατφόρμας.'),
                           ('Ελληνικά και αγγλικά', 'Φτιαγμένη για ξένους επισκέπτες από την πρώτη μέρα.'),
                           ('Πώς θα έρθετε', 'Οδηγίες με αυτοκίνητο, λεωφορείο και από το αεροδρόμιο, με χάρτη.'),
                           ('Κριτικές επισκεπτών', 'Δείξτε τι λένε οι επισκέπτες σας, με σύνδεση στις κριτικές Google.'),
                           ('Εμφάνιση στη Google', 'Ρύθμιση στην αναζήτηση και στους χάρτες της Google για την περιοχή σας.')],
                 autos=[('Άμεση απάντηση σε κάθε αίτημα', 'Ο επισκέπτης λαμβάνει αυτόματη απάντηση και εσείς τα στοιχεία αμέσως.'),
                        ('Πληροφορίες άφιξης', 'Email με οδηγίες και στοιχεία check-in πριν την άφιξη.'),
                        ('Αίτημα κριτικής μετά τη διαμονή', 'Ένα φιλικό μήνυμα που ζητά από ικανοποιημένους επισκέπτες μια κριτική.')],
                 faq=[('Θα αντικαταστήσει το Booking.com;', 'Δουλεύει δίπλα του. Ο στόχος είναι περισσότερες απευθείας κρατήσεις, ειδικά από επισκέπτες που επιστρέφουν.'),
                      ('Μπορεί να δείχνει διαθεσιμότητα;', 'Ναι. Συνδέουμε ένα απλό ημερολόγιο ή το channel manager σας.'),
                      ('Πόσο χρόνο χρειάζεται;', 'Συνήθως δύο έως τέσσερις εβδομάδες.')])),
]

HUB = {
    'en': dict(dir='websites', title='Websites by industry', label='Industries',
               desc='Websites and automation by IVELRO for tutoring centres, clinics, restaurants, guesthouses and businesses of every other kind.',
               h1='Websites built for your type of business',
               lead='Every industry has different visitors and different needs. Here are a few examples, with what we build, the automations that save time and a sample website. We build websites for businesses of every kind and size, so if yours is not listed, just ask.'),
    'el': dict(dir='el/istoselides', title='Ιστοσελίδες ανά κλάδο', label='Κλάδοι',
               desc='Κατασκευή ιστοσελίδων και αυτοματισμών από την IVELRO για φροντιστήρια, ιατρεία, εστιατόρια, καταλύματα και επιχειρήσεις κάθε άλλου είδους.',
               h1='Ιστοσελίδες φτιαγμένες για τον δικό σας τύπο επιχείρησης',
               lead='Κάθε κλάδος έχει διαφορετικούς επισκέπτες και διαφορετικές ανάγκες. Εδώ θα βρείτε μερικά παραδείγματα, με το τι φτιάχνουμε, τους αυτοματισμούς που γλιτώνουν χρόνο και ένα δείγμα ιστοσελίδας. Φτιάχνουμε ιστοσελίδες για επιχειρήσεις κάθε είδους και μεγέθους, οπότε αν δεν βλέπετε τη δική σας, απλώς ρωτήστε μας.'),
}

GUIDES = [
    dict(slug='istoselida-frontistiriou', date='2026-11-22', date_el='22 Νοεμβρίου 2026',
         title='7 πράγματα που πρέπει να έχει η ιστοσελίδα ενός φροντιστηρίου',
         desc='Τι ψάχνουν οι γονείς όταν συγκρίνουν φροντιστήρια online, και τα 7 πράγματα που κάνουν μια ιστοσελίδα φροντιστηρίου να φέρνει εγγραφές.',
         summary='Τι ψάχνουν οι γονείς όταν συγκρίνουν φροντιστήρια και πώς η ιστοσελίδα σας φέρνει εγγραφές.',
         body='''<p>Όταν ένας γονέας ψάχνει φροντιστήριο, ανοίγει δύο ή τρεις ιστοσελίδες στο κινητό και αποφασίζει μέσα σε λίγα λεπτά ποιο θα πάρει τηλέφωνο. Αυτά είναι τα επτά πράγματα που κάνουν τη διαφορά.</p>
<h2>1. Τμήματα και πρόγραμμα ανά τάξη</h2>
<p>Ο γονέας θέλει να δει αμέσως αν καλύπτετε την τάξη του παιδιού του. Χωρίστε τα τμήματα σε Γυμνάσιο, Α΄–Β΄ Λυκείου και Γ΄ Λυκείου, με τα μαθήματα και ένα ενδεικτικό εβδομαδιαίο πρόγραμμα.</p>
<h2>2. Μέγεθος τμημάτων και μέθοδος</h2>
<p>«Τμήματα έως 6 μαθητών» και «διαγώνισμα κάθε 15 ημέρες» λένε περισσότερα από μια παράγραφο με γενικές υποσχέσεις. Γράψτε συγκεκριμένους αριθμούς.</p>
<h2>3. Οι καθηγητές</h2>
<p>Ονόματα, ειδικότητες και σπουδές χτίζουν εμπιστοσύνη. Ο γονέας θέλει να ξέρει ποιος θα διδάξει το παιδί του.</p>
<h2>4. Επιτυχόντες</h2>
<p>Τα αποτελέσματα των Πανελλαδικών είναι το πιο πειστικό στοιχείο. Δείξτε σχολές και ιδρύματα, με αρχικά ονομάτων και τη συγκατάθεση των μαθητών.</p>
<h2>5. Ηλεκτρονική εγγραφή</h2>
<p>Πολλοί γονείς ψάχνουν το βράδυ, όταν η γραμματεία είναι κλειστή. Μια σύντομη φόρμα εγγραφής με αυτόματο email επιβεβαίωσης κρατά τον γονέα πριν πάει στο επόμενο φροντιστήριο.</p>
<h2>6. Τέλεια εμφάνιση στο κινητό</h2>
<p>Η μεγάλη πλειονότητα των γονέων ψάχνει από το κινητό. Αν τα κουμπιά είναι μικρά ή το κείμενο βγαίνει εκτός οθόνης, ο γονέας φεύγει.</p>
<h2>7. Στοιχεία επικοινωνίας και χάρτης</h2>
<p>Διεύθυνση, τηλέφωνο που καλεί με ένα πάτημα, ωράριο γραμματείας και κοντινές στάσεις. Και φυσικά ένα ενημερωμένο προφίλ στη Google, για να εμφανίζεστε στον χάρτη όταν κάποιος ψάχνει «φροντιστήριο» στην περιοχή σας.</p>
<h2>Δείτε ένα παράδειγμα</h2>
<p>Φτιάξαμε ένα <a href="../../../portfolio/frontistirio/">δείγμα ιστοσελίδας φροντιστηρίου</a> με όλα τα παραπάνω, μαζί με καρτέλα προόδου για γονείς.</p>''',
         industry='frontistiria'),
]


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
        <a href="{home}portfolio/">{u["work"]}</a>{lang_link}
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
          <a href="{home}#process">{"Process" if lang == "en" else "Διαδικασία"}</a>
          <a href="{home}portfolio/">{u["work"]}</a>
          <a href="{up}{HUB[lang]["dir"]}/">{u["solutions"]}</a>
          <a href="{up}{"legal" if lang == "en" else "el/nomika"}/">{"Legal" if lang == "en" else "Νομικά"}</a>
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


def cta_buttons(lang, up, sample=None):
    u = UI[lang]
    home = up if lang == 'en' else up + 'el/'
    s = f'<a class="btn btn-solid" href="{up}portfolio/{sample}/">{u["see"]} <span aria-hidden="true">→</span></a>\n          ' if sample else ''
    return s + f'<a class="btn" href="{home}#contact" data-contact-cta hidden>{u["contact"]}</a>'


def industry_page(ind, lang):
    c = ind[lang]
    u = UI[lang]
    slug = ind['en_slug'] if lang == 'en' else ind['el_slug']
    path = f'websites/{slug}/' if lang == 'en' else f'el/istoselides/{slug}/'
    up = '../' * path.count('/')
    alternates = {'en': f'websites/{ind["en_slug"]}/', 'el': f'el/istoselides/{ind["el_slug"]}/'}
    features = '\n'.join(f'          <div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in c['features'])
    autos = '\n'.join(f'          <li><span>0{i + 1}</span><div><b>{e(t)}</b><p>{e(d)}</p></div></li>' for i, (t, d) in enumerate(c['autos']))
    steps = '\n'.join(f'          <li><b>{e(t)}</b><p>{e(d)}</p></li>' for t, d in u['steps'])
    faq = '\n'.join(f'          <details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in c['faq'])
    others = ' '.join(f'<a href="{up}{HUB[lang]["dir"]}/{(o["en_slug"] if lang == "en" else o["el_slug"])}/">{e(o[lang]["name"])}</a>'
                      for o in INDUSTRIES if o is not ind)
    body = f'''    <div class="container page-hero">
      <p class="label">{e(c["name"])}</p>
      <h1>{e(c["h1"])}</h1>
      <p class="lead">{e(c["lead"])}</p>
      <div class="cta-row">
          {cta_buttons(lang, up, ind["sample"])}
      </div>
    </div>

    <div class="container" style="padding-bottom:clamp(64px,9vw,112px)">
      <figure style="margin:0">
        <a class="preview" href="{up}portfolio/{ind["sample"]}/">
          <img src="{up}portfolio/img/{ind["sample"]}.jpg" alt="{e(u["sample"])}: {e(c["name"])}" width="960" height="600" loading="lazy">
          <span class="cap"><span>{e(u["sample"])}</span><span>{e(u["open"])}</span></span>
        </a>
      </figure>
    </div>

    <section class="block" aria-labelledby="inc">
      <div class="container">
        <p class="label">01</p>
        <h2 id="inc">{e(u["included"])}</h2>
        <div class="features">
{features}
        </div>
      </div>
    </section>

    <section class="block" aria-labelledby="aut">
      <div class="container">
        <p class="label">02</p>
        <h2 id="aut">{e(u["autos"])}</h2>
        <ul class="autos">
{autos}
        </ul>
      </div>
    </section>

    <section class="block" aria-labelledby="how">
      <div class="container">
        <p class="label">03</p>
        <h2 id="how">{e(u["how"])}</h2>
        <ol class="mini-steps">
{steps}
        </ol>
      </div>
    </section>

    <section class="block" aria-labelledby="faq">
      <div class="container">
        <p class="label">04</p>
        <h2 id="faq">{e(u["faq"])}</h2>
        <div class="faq">
{faq}
        </div>
      </div>
    </section>

    <section class="cta-band">
      <div class="container">
        <h2>{e(u["cta_t"])}</h2>
        <p>{e(u["cta_p"])}</p>
        <div class="cta-row">
          {cta_buttons(lang, up, ind["sample"])}
        </div>
        <p class="related" style="justify-content:center"><span style="color:var(--faint)">{e(u["other"])}:</span> {others}</p>
      </div>
    </section>'''
    jsonld = {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': c['title'],
        'description': c['desc'],
        'serviceType': 'Web design and business automation',
        'areaServed': [{'@type': 'City', 'name': 'Athens'}, {'@type': 'Country', 'name': 'Greece'}, {'@type': 'Place', 'name': 'Worldwide'}],
        'provider': {'@type': 'ProfessionalService', 'name': 'IVELRO', 'url': SITE, 'logo': SITE + 'assets/img/logo.png'},
        'url': SITE + path,
    }
    return path, page(lang, path, c['title'], c['desc'], alternates, body, jsonld)


def hub_page(lang):
    h = HUB[lang]
    u = UI[lang]
    path = h['dir'] + '/'
    up = '../' * path.count('/')
    alternates = {'en': HUB['en']['dir'] + '/', 'el': HUB['el']['dir'] + '/'}
    cards = '\n'.join(f'''      <a href="{(ind["en_slug"] if lang == "en" else ind["el_slug"])}/">
        <img src="{up}portfolio/img/{ind["sample"]}.jpg" alt="" width="960" height="600" loading="lazy">
        <div class="hub-body"><p class="label">{e(ind[lang]["name"])}</p><h2>{e(ind[lang]["title"])}</h2><p>{e(ind[lang]["desc"])}</p><span class="go">{e(u["open"])}</span></div>
      </a>''' for ind in INDUSTRIES)
    body = f'''    <div class="container page-hero">
      <p class="label">{e(h["label"])}</p>
      <h1>{e(h["h1"])}</h1>
      <p class="lead">{e(h["lead"])}</p>
    </div>
    <div class="container hub">
{cards}
    </div>'''
    return path, page(lang, path, h['title'], h['desc'], alternates, body)


def guides_pages():
    out = []
    path = 'el/odigoi/'
    items = '\n'.join(f'      <li><a href="{g["slug"]}/"><b>{e(g["title"])}</b><span>{e(g["summary"])}</span></a></li>' for g in GUIDES)
    body = f'''    <div class="container page-hero">
      <p class="label">Οδηγοί</p>
      <h1>Οδηγοί για επιχειρήσεις</h1>
      <p class="lead">Σύντομοι, πρακτικοί οδηγοί για το πώς μια επιχείρηση φέρνει περισσότερους πελάτες από το internet.</p>
    </div>
    <div class="container">
      <ul class="guides">
{items}
      </ul>
    </div>'''
    out.append((path, page('el', path, 'Οδηγοί για επιχειρήσεις', 'Πρακτικοί οδηγοί της IVELRO για ιστοσελίδες, Google και αυτοματισμούς για επιχειρήσεις.', {'el': path}, body)))
    for g in GUIDES:
        gp = f'el/odigoi/{g["slug"]}/'
        up = '../' * gp.count('/')
        more = (f'<p><a href="{up}el/istoselides/{g["industry"]}/">Δείτε τι περιλαμβάνει μια ιστοσελίδα για τον κλάδο σας →</a></p>'
                if g['industry'] else f'<p><a href="{up}el/istoselides/">Δείτε ιστοσελίδες ανά κλάδο →</a></p>')
        body = f'''    <article class="container article">
      <p class="label"><a href="../" style="border:0">Οδηγοί</a></p>
      <h1>{e(g["title"])}</h1>
      <p class="meta"><time datetime="{g["date"]}">{g["date_el"]}</time> · IVELRO</p>
{g["body"]}
      <div class="box">
        <p>Η IVELRO φτιάχνει ιστοσελίδες και αυτοματισμούς για επιχειρήσεις κάθε είδους και μεγέθους.</p>
        {more}
        <div class="cta-row" style="margin-top:20px"><a class="btn" href="{up}el/#contact" data-contact-cta hidden>Επικοινωνήστε μαζί μας</a></div>
      </div>
    </article>'''
        jsonld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': g['title'], 'description': g['desc'],
                  'datePublished': g['date'], 'inLanguage': 'el', 'author': {'@type': 'Organization', 'name': 'IVELRO', 'url': SITE},
                  'publisher': {'@type': 'Organization', 'name': 'IVELRO', 'logo': {'@type': 'ImageObject', 'url': SITE + 'assets/img/logo.png'}},
                  'mainEntityOfPage': SITE + gp}
        out.append((gp, page('el', gp, g['title'], g['desc'], {'el': gp}, body, jsonld)))
    return out


def main():
    pages = []
    for ind in INDUSTRIES:
        pages += [industry_page(ind, 'en'), industry_page(ind, 'el')]
    pages += [hub_page('en'), hub_page('el')]
    pages += guides_pages()
    for path, content in pages:
        full = os.path.join(ROOT, path, 'index.html')
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
    print('\n'.join(p for p, _ in pages))
    # sitemap: keep existing entries, add generated pages once
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sm_path, encoding='utf-8').read()
    for p, _ in pages:
        loc = f'<loc>{SITE}{p}</loc>'
        if loc not in sm:
            sm = sm.replace('</urlset>', f'  <url>\n    {loc}\n  </url>\n</urlset>')
    open(sm_path, 'w', encoding='utf-8').write(sm)


if __name__ == '__main__':
    main()
