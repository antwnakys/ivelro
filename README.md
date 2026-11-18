# IVELRO

Company website for IVELRO — *Intelligence, Simplified.*

A static site (plain HTML and CSS, no build step), published to GitHub Pages by
`.github/workflows/pages.yml` on every push to `main`.

## Structure

```
index.html            Single-page site
404.html              Not-found page
assets/js/main.js     Interactions (header, reveals, scroll-spy, card spotlight)
assets/css/style.css  Styles (colour tokens at the top of the file)
assets/img/           Logo, favicon and social-preview image
```

## Local preview

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Domain

The site is served at https://ivelro.com (set by the `CNAME` file).
DNS records at the domain registrar:

| Type  | Name  | Value                 |
|-------|-------|-----------------------|
| A     | @     | 185.199.108.153       |
| A     | @     | 185.199.109.153       |
| A     | @     | 185.199.110.153       |
| A     | @     | 185.199.111.153       |
| CNAME | www   | antwnakys.github.io   |

Then in **Settings → Pages**: custom domain `ivelro.com`, and tick **Enforce HTTPS** once it is available.
