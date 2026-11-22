# Client website starter

A ready base for every new client site: header with mobile menu, hero, services, about, reviews, FAQ,
contact with live opening hours, map and a working form, footer, privacy page, 404, sitemap and Google business data.

## Make a new client site

1. Copy `example-client.json` to `clients/<client>.json` and fill in the client's details, colours and opening hours.
2. Run:

   ```bash
   python3 templates/new-site.py clients/<client>.json ../<client>-site
   ```

   It copies the starter, fills in every placeholder and lists anything still missing.
3. **Designer:** set the colours in `assets/css/style.css` (`:root`), add the logo and real photos
   (`assets/img/`, 1200×900, under 250 KB each), and the share image `assets/img/og-image.jpg` (1200×630).
4. **Web developer:** check every text, add the Google Maps embed link and the Web3Forms key, then follow
   [`docs/launch-checklist.md`](../docs/launch-checklist.md).

## What is where

| File | Purpose |
|---|---|
| `starter/index.html` | The page. Sections can be removed or duplicated freely. |
| `starter/assets/css/style.css` | All styles. Change the look in `:root` only. |
| `starter/assets/js/site.js` | Mobile menu, scroll reveal, "open now" status, form sending. |
| `starter/privacy.html` | Privacy policy with the client as the responsible business. |
| `new-site.py` | Creates a client site from a JSON file. |
