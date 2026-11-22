# Ready-to-enable parts of ivelro.com

These files are **not published yet**. They are switched on with one command once we have the IVELRO email (planned for 29 November).

| File | What it becomes |
|---|---|
| `contact-en.html`, `contact-el.html` | Contact section with a working form, added to the English and Greek homepages |
| `contact.js` | Sends the form to Web3Forms (copied to `assets/js/contact.js`) |
| `contact.css` | Styles for the contact section and privacy pages (added to `assets/css/style.css`) |
| `privacy-en.html`, `privacy-el.html` | `privacy.html` and `el/privacy.html` |
| `enable.py` | Fills in the details and switches everything on |

## Switch on the contact section (29 November)

1. Create the IVELRO inbox in OpenInbox, e.g. `info@ivelro.com`.
2. Go to <https://web3forms.com>, enter that email and copy the **access key** it sends you. Messages from the form will arrive in that inbox.
3. From the repository root:

```bash
python3 staging/enable.py --email info@ivelro.com --phone "+30 69X XXX XXXX" --key YOUR_WEB3FORMS_KEY
```

4. Check the homepage locally (`python3 -m http.server 8000`), send a test message, then commit and push to `main`.

## Switch on visitor statistics (any time)

1. Cloudflare dashboard → **Analytics & Logs → Web Analytics → Add a site** → `ivelro.com`.
2. Choose the JavaScript snippet option and copy the **token** from it.
3. Run:

```bash
python3 staging/enable.py --analytics-token YOUR_TOKEN
```

The script is safe to run more than once: it skips anything already added.
