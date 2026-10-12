# Website jstnmultidiensten.nl

Statische website van JSTN Multidiensten (Groningen). Netlify publiceert de map `site/` automatisch bij elke push naar `main`.

## Werken aan de site (nieuw ontwerp v2, oktober 2026)
Alle HTML-pagina's staan als vaste bestanden in `site/` (ontwerp van Compound Media). Pas teksten direct in die HTML aan.

- `site/assets/v2.css` en `site/assets/img/` – opmaak en foto's van het nieuwe ontwerp
- `site/contact.js` – contactformulier (Netlify Forms)
- `site/_headers` – beveiligingsheaders (CSP) en cacheregels; **de enige bron van headers**. Nieuwe externe tool (chat, reviewwidget)? Voeg het domein toe aan de Content-Security-Policy.
- Elke pagina bevat al GTM (`GTM-P7LMDWQF`) en de cookiemelding. Voeg GTM nergens extra toe.

`python3 build.py` maakt alleen nog `sitemap.xml`, `robots.txt`, `_redirects` en kopieert `portfolio_img/` naar `site/portfolio/img/`. Het schrijft geen pagina's, `404.html` of `_headers` meer.

**Nieuw blogartikel** (tot er een v2-blogsjabloon is):
1. Kopieer een bestaand artikel in `site/post/` naar een nieuwe map en vervang titel, meta-description, canonical/OG-url, JSON-LD (BlogPosting, kruimelpad, FAQ), datum, categorie en de tekst in `<article>`.
2. Voeg bovenaan in `site/blog/index.html` een kaart toe (kopieer een bestaande `<a class="post">`).
3. Zet het artikel ook als item in `posts.py` (voor de sitemap) en draai `python3 build.py`.

Commit en push naar `main`: Netlify publiceert dan automatisch.

HEIC-foto's van een iPhone omzetten: `python3 heic2jpg.py foto.HEIC uit.jpg` (heeft ffmpeg nodig).
