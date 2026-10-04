# Website jstnmultidiensten.nl

Statische website van JSTN Multidiensten (Groningen). Netlify publiceert de map `site/` automatisch bij elke push naar `main`.

## Werken aan de site
1. Pas de bronbestanden aan:
   - `build.py` – alle pagina's, menu, footer, sitemap, redirects
   - `diensten.py` – teksten van de dienstpagina's
   - `posts.py` – blogartikelen (nieuw artikel = nieuw item in `POSTS`)
   - `portfolio_img/` – foto's voor het portfolio (max ~900 px, zonder locatiegegevens)
   - `site/style.css`, `site/contact.js` – opmaak en scripts (handmatig bewerkt)
2. Draai `python3 build.py` (alleen standaard Python nodig). Dit schrijft alle HTML in `site/`.
3. Commit zowel de bronbestanden als `site/` en push naar `main`.

HEIC-foto's van een iPhone omzetten: `python3 heic2jpg.py foto.HEIC uit.jpg` (heeft ffmpeg nodig).
