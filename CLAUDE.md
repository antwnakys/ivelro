# IVELRO website: notes for Claude

## Keep the website status document up to date (always)

After **any** change to the website, templates, staging package or website docs, update the Google Doc
**"Website status: done and to do"** in the Drive folder **IVELRO → Website (Web Developer)**
(document ID `12dls_aQCtEbYbGbyeq5kC8hy16TP_z4uOputEskD-4E`):

- Move finished items from **To do** to **Done**, add new open items to **To do**.
- Update the **Last updated** date.
- Write only what has been done and what remains. No other content.

## Project rules

- The ivelro.com design (round 2) is final. Do not redesign `index.html`, `el/index.html` or `assets/css/style.css`; small additions only.
- English and Greek are separate pages (`/` and `/el/`). Any text change on one goes on the other too.
- `staging/` is not published. `staging/enable.py` switches on the contact section, privacy pages and analytics.
- `templates/` and `docs/` are internal (not published). Client sites are made with `templates/new-site.py`.
- Deploy: push to `main`; `.github/workflows/pages.yml` publishes only the folders listed in its `cp` line.
- Test with Playwright at 360, 390, 768, 1024 and 1440 px: no sideways scrolling, no console errors.
