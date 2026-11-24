<p align="center">
  <a href="https://ivelro.com"><img src=".github/readme/banner.png" alt="IVELRO: AI search presence, business automation and local AI" width="100%"></a>
</p>

<p align="center">
  <a href="https://ivelro.com"><img src="https://img.shields.io/badge/website-ivelro.com-f2f2f2?style=flat-square&labelColor=0a0a0a" alt="Website: ivelro.com"></a>
  <a href="https://github.com/antwnakys/ivelro/actions/workflows/pages.yml"><img src="https://img.shields.io/github/actions/workflow/status/antwnakys/ivelro/pages.yml?branch=main&style=flat-square&label=deploy&labelColor=0a0a0a" alt="Deploy status"></a>
  <img src="https://img.shields.io/badge/stack-HTML%20%C2%B7%20CSS%20%C2%B7%20JS-3a3a3a?style=flat-square&labelColor=0a0a0a" alt="Stack: HTML, CSS, JavaScript">
  <img src="https://img.shields.io/badge/build%20step-none-3a3a3a?style=flat-square&labelColor=0a0a0a" alt="No build step">
</p>

<p align="center">
  <a href="https://ivelro.com"><b>Website</b></a>
  &nbsp;·&nbsp;
  <a href="https://ivelro.com/use-cases/"><b>Use cases</b></a>
  &nbsp;·&nbsp;
  <a href="#run-it-locally"><b>Run locally</b></a>
</p>

<br>

<p align="center">
  <img src=".github/readme/showcase.jpg" alt="The IVELRO website on desktop and phone" width="100%">
</p>

## About

**IVELRO** helps businesses be found in the AI answers their customers trust. We make companies understandable, credible and easy to recommend in AI-powered search, automate everyday work, and build private AI systems around the knowledge a company already has. Based in Athens, working with companies of every size, anywhere.

> *Intelligence, Simplified.*

| | What we do |
|---|---|
| **01 · AI Search Presence** | Make a business easier for AI search and answer tools to understand, trust and recommend: clear company information, structured data and regular checks of what AI tools say. No guaranteed rankings, no traditional SEO. |
| **02 · Business Automation & AI Integration** | Automate repetitive work, connect the tools a business already uses, and bring AI into everyday workflows. |
| **03 · Local AI for Companies** | Private AI systems that run on hardware the company controls, tailored to its size, workflows, tools and privacy needs, from small teams to large organisations. |

This repository holds the company website, [ivelro.com](https://ivelro.com), in English and Greek.

## How it's built

- **Plain HTML, CSS and JavaScript.** No framework and no build step, so pages load fast and are easy to maintain.
- **Mobile first.** Every page is tested from 360 px phones to 1440 px desktops.
- **Accessible.** Keyboard navigation, visible focus, readable contrast, reduced-motion support.
- **Private.** No cookies, no tracking, and fonts served from the site itself.
- **Machine-readable.** Structured company information (schema.org) on every page, so AI tools and search engines read IVELRO's details reliably.
- **Automatic deploys.** Every push to `main` is published to GitHub Pages.

## Project structure

```
.
├── index.html               Homepage (English)
├── el/                      Greek homepage, use cases and legal pages
├── use-cases/               Use cases and how we work (English)
├── legal/                   Policies (English)
├── 404.html                 Not-found page
├── assets/
│   ├── css/                 Site styles (colour tokens at the top of style.css)
│   ├── fonts/               Self-hosted fonts (SIL Open Font License)
│   ├── js/main.js           Header, reveal animations, scroll-spy
│   └── img/                 Logo, favicons, social image, email signature images
├── portfolio/, websites/    Redirects from retired pages to the use cases
├── tools/
│   ├── build_pages.py       Builds the use-cases pages, redirects and sitemap
│   ├── build_legal.py       Builds the policies from tools/legal/
│   └── dashboard/           Back end of the private team dashboard (Apps Script)
├── signatures/              Email signatures and signature maker (not published)
├── staging/                 Contact section, ready to switch on (not published)
├── docs/                    Delivery process, go-live checklist, support package (not published)
├── sitemap.xml · robots.txt · llms.txt · CNAME
└── .github/workflows/pages.yml   Deploy to GitHub Pages
```

## Run it locally

No installation needed. From the project folder:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. After editing texts in `tools/`, rebuild the generated pages:

```bash
python3 tools/build_pages.py && python3 tools/build_legal.py
```

## Deployment

The workflow in [`.github/workflows/pages.yml`](.github/workflows/pages.yml) publishes the site to GitHub Pages on every push to `main`. The site is served at **[ivelro.com](https://ivelro.com)** over HTTPS.

<details>
<summary><b>Domain and DNS settings</b></summary>
<br>

The custom domain is set by the `CNAME` file. DNS records (Cloudflare, DNS only):

| Type  | Name  | Value               |
|-------|-------|---------------------|
| A     | @     | 185.199.108.153     |
| A     | @     | 185.199.109.153     |
| A     | @     | 185.199.110.153     |
| A     | @     | 185.199.111.153     |
| CNAME | www   | antwnakys.github.io |

In **Settings → Pages**, the custom domain is `ivelro.com` with **Enforce HTTPS** turned on.

</details>

---

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/img/mark.png">
    <img src="assets/img/mark-dark.png" alt="" width="28">
  </picture>
  <br>
  <sub>© 2026 IVELRO. All rights reserved.</sub>
</p>
