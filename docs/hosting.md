# Hosting client websites

## Recommended: Cloudflare Pages (free)

Why: free, very fast in Greece, free HTTPS, custom domains, and we already use Cloudflare for ivelro.com.

1. Put the client site in its own GitHub repository (e.g. `ivelro-client-name`).
2. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git** → choose the repository.
3. Build settings: framework **None**, build command empty, output directory `/`.
4. **Custom domains → Set up a domain** → the client's domain. If the domain's DNS is on Cloudflare it connects in one click;
   otherwise add the CNAME record Cloudflare shows at the client's registrar.
5. Every push to the repository updates the live site automatically.

GitHub Pages also works (that is how ivelro.com runs), but Cloudflare Pages is better for client sites:
preview links for each change, easier domains, and redirects.

## Domains

- **.gr domains:** register through a Greek registrar, e.g. papaki.gr or top.host.
- Register the domain **in the client's name**, so they own it. We manage it with their login or as a technical contact.
- Note the renewal date in the client's folder, and remind them a month before.

## Email for clients

If the client needs `info@theirdomain.gr`, the simplest options are Zoho Mail (free plan for small teams) or Google Workspace (paid).
Add the MX records the provider gives you in the domain's DNS.

## Forms

All our sites use **Web3Forms** (free up to 250 messages a month): sign up at web3forms.com with the client's email,
copy the access key into the form's `access_key` field. Messages go straight to the client's inbox.
For forms that must also save to a Google Sheet or send an automatic reply, the Automation & AI developer builds a Google Apps Script instead.
