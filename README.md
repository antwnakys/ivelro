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

## Moving to a custom domain

1. Add a file named `CNAME` at the repo root containing only the domain, e.g. `ivelro.com`.
2. At your DNS provider, point the domain to GitHub Pages:
   - apex domain: `A` records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www`: a `CNAME` record to `antwnakys.github.io`
3. In the repo go to **Settings → Pages**, enter the domain under *Custom domain* and enable **Enforce HTTPS**.

Paths in `index.html` are relative, so it needs no changes. In `404.html`, change
`<base href="/ivelro/">` to `<base href="/">`.
