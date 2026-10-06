# -*- coding: utf-8 -*-
"""Bouwt de statische website van JSTN Multidiensten in ./site"""
import os, json, html
import diensten as D
from urllib.parse import quote

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
BASE = "https://www.jstnmultidiensten.nl"
TEL = "+31636179549"
TEL_TXT = "+31 6 36179549"
MAIL = "info@jstnmultidiensten.nl"
WA = "https://wa.me/31636179549"

WIX = "https://static.wixstatic.com/media/"
IMG_BUSSEN = "b719c9_e762ab247616427ab48ca0ee5403c98e~mv2.jpeg"
IMG_KANTOOR = "b719c9_b1a41a0f00494731addb3929defd1ae9~mv2.jpeg"

def wimg(mid, w, h, name):
    return f"{WIX}{mid}/v1/fill/w_{w},h_{h},al_c,q_80,enc_auto/{name}.jpg"

# ---------- iconen ----------
I = {
 "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "tel": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "wa": '<path d="M3 21l1.7-5A8.5 8.5 0 1 1 8 19.3z"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "office": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
 "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
 "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 "floor": '<path d="M3 20h18"/><path d="M6 20v-4h12v4"/><path d="M12 16V4"/><path d="M9 4h6"/>',
 "window": '<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M12 3v18M4 12h16"/>',
 "box": '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
 "truck": '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/>',
 "roller": '<rect x="4" y="3" width="14" height="6" rx="1"/><path d="M18 6h2v5h-8v3"/><rect x="10" y="14" width="4" height="7" rx="1"/>',
 "key": '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
 "drop": '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
 "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>',
 "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 "clip": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 10h6M9 14h6M9 18h3"/>',
 "chat": '<path d="M4 5h16v11H8l-4 4z"/>',
 "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "book": '<path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-4a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h5z"/>',
}
def ic(name, cls=""):
    return f'<svg{(" class=%s" % cls) if cls else ""} viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

STARS = '<div class="st" aria-label="5 sterren">' + "".join(ic("star") for _ in range(5)) + "</div>"

# ---------- structured data ----------
ORG = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": BASE + "/#bedrijf",
  "name": "JSTN Multidiensten",
  "url": BASE + "/",
  "logo": BASE + "/icon-512.png",
  "image": BASE + "/og-image.jpg",
  "telephone": TEL,
  "email": MAIL,
  "address": {"@type": "PostalAddress", "streetAddress": "Zernikepark 4", "postalCode": "9747 AN",
              "addressLocality": "Groningen", "addressCountry": "NL"},
  "areaServed": [{"@type": "City", "name": n} for n in D.PLAATSEN] + [{"@type": "AdministrativeArea", "name": "Provincie Groningen"}],
  "openingHours": "Mo-Sa 07:00-18:00",
  "slogan": "Schoonmaak, ontruiming en opleveringen. Wij regelen het.",
  "description": "Schoonmaak en desinfectie, vloerreiniging, glasbewassing, ontruimen, verhuizen, schilder- en behangwerk, opleveren van zorg-appartementen en hogedrukreiniging in Groningen en omgeving.",
}

NAV = [("/", "Home"), ("/zakelijk/", "Zakelijk"), ("/particulier/", "Particulier"),
       ("/over-ons/", "Over ons"), ("/portfolio/", "Portfolio"), ("/werken-bij/", "Vacatures"), ("/blog/", "Blog"), ("/contact/", "Contact")]

def header(active):
    links = "".join(f'<a href="{u}"{" class=on aria-current=page" if u == active else ""}>{t}</a>' for u, t in NAV)
    return f'''<a class="skip" href="#inhoud">Naar inhoud</a>
<header class="hd">
<div class="w">
<div class="top">
<a class="logo" href="/" aria-label="JSTN Multidiensten, naar home"><img src="/logo-donker.png" width="150" height="68" alt="JSTN Multidiensten"></a>
<div class="chips">
<a class="chip" href="https://maps.google.com/?q=Zernikepark+4,+9747+AN+Groningen" target="_blank" rel="noopener">{ic("pin")}<span><small>Ons adres</small>Zernikepark 4, Groningen</span></a>
<a class="chip" href="tel:{TEL}">{ic("tel")}<span><small>Bel ons</small>{TEL_TXT}</span></a>
<a class="btn hide-s" href="/contact/">Neem contact op</a>
</div>
</div>
<nav class="nav" aria-label="Hoofdmenu">{links}</nav>
</div>
</header>'''

FOOTER = f'''<footer class="ft">
<div class="w ftg">
<div>
<a class="logo" href="/" aria-label="JSTN Multidiensten, naar home"><img src="/logo-wit.png" width="150" height="68" alt="JSTN Multidiensten" loading="lazy"></a>
<p class="ftp">Schoonmaak, ontruiming en opleveringen. Wij regelen het.</p>
</div>
<div><h2 class="fth">Ga naar</h2><ul>{"".join(f'<li><a href="{u}">{t}</a></li>' for u, t in NAV)}</ul></div>
<div><h2 class="fth">Diensten</h2><ul>{"".join(f'<li><a href="/{d["slug"]}/">{d["kort"]}</a></li>' for d in D.DIENSTEN)}</ul></div>
<div><h2 class="fth">Contact</h2><ul><li>Zernikepark 4, 9747 AN Groningen</li><li><a href="tel:{TEL}">{TEL_TXT}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="/privacy/">Privacybeleid</a></li></ul></div>
<div><h2 class="fth">Maak een afspraak</h2><p class="ftp">Laat u adviseren door een van onze experts voor een oplossing die past bij uw situatie.</p><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp</a></div>
</div>
<div class="w"><div class="copy">© 2026 Jstnmultidiensten.nl · Alle rechten voorbehouden</div></div>
</footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Stuur ons een WhatsApp">{ic("wa")}</a>'''

CTA = f'''<section class="pb">
<div class="w">
<div class="dark cta">
<div style="max-width:560px">
<h2 style="color:#fff;margin-top:0">Klaar voor uw klus?</h2>
<p style="color:#E2E8EC;margin:0"><span class="acc" style="font-weight:800">Reactie binnen 12 uur.</span> Vraag vrijblijvend een offerte aan of stuur ons direct een WhatsApp.</p>
</div>
<div class="row">
<a class="btn btn-light" href="/contact/">Offerte aanvragen</a>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp</a>
</div>
</div>
</div>
</section>'''

def page(path, title, desc, active, body, extra_ld=None, og_type="website", og_img=None, head_extra=""):
    url = BASE + path
    lds = [ORG] + (extra_ld or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    doc = f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="JSTN Multidiensten">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img or BASE + '/og-image.jpg'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#3F3D3F">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&display=swap">
<link rel="stylesheet" href="/style.css">
{head_extra}{ld}
</head>
<body>
{header(active)}
<main id="inhoud">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    d = os.path.join(OUT, path.strip("/"))
    fn = os.path.join(d, "index.html") if not path.endswith(".html") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w", encoding="utf-8") as f:
        f.write(doc)
    return url

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
                                for i, (n, u) in enumerate(items)]}

def card(icon, title, text, tag="h3", bg=None):
    style = f' style="background:{bg}"' if bg else ""
    return f'<div class="card"{style}><div class="ic">{ic(icon)}</div><{tag}>{title}</{tag}><p class="muted">{text}</p></div>'

ANCHOR2SLUG = {"schoonmaak": "schoonmaak-groningen", "vloerreiniging": "vloerreiniging-groningen",
  "zorg-appartementen": "zorgappartementen-opleveren", "ontruimen": "woningontruiming-groningen",
  "leegruimen": "woningontruiming-groningen", "schilderwerk": "schilder-groningen",
  "hogedrukreiniging": "hogedrukreiniging-groningen", "glasbewassing": "glazenwasser-groningen",
  "verhuizingen": "verhuizen-groningen", "opleveringen": "woning-opleveren-groningen"}

def svc(icon, title, paras, anchor):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    lk = f'<a class="link" href="/{ANCHOR2SLUG[anchor]}/">Meer over {title.lower()}{ic("arrow")}</a>' if anchor in ANCHOR2SLUG else ""
    return f'<article class="card svc" id="{anchor}"><div class="ic">{ic(icon)}</div><div><h3>{title}</h3>{ps}{lk}</div></article>'

# ======================= HOME =======================
SERVICES = [
 ("sparkle", "Schoonmaak &amp; desinfectie", "Reguliere schoonmaak en grondige dieptereiniging met professionele apparatuur.", "/schoonmaak-groningen/"),
 ("floor", "Vloerreiniging", "Grote vloeren in scholen, kantoren en bedrijfspanden grondig schoon — ook in vakanties.", "/vloerreiniging-groningen/"),
 ("window", "Glasbewassing", "Streeploos schone ramen voor woningen en bedrijfspanden.", "/glazenwasser-groningen/"),
 ("box", "Ontruimen &amp; leegruimen", "Snel, zorgvuldig en duurzaam — ook spoedontruimingen.", "/woningontruiming-groningen/"),
 ("truck", "Verhuizen", "Inpakken, uitpakken en alles weer op zijn plek — met extra aandacht voor senioren.", "/verhuizen-groningen/"),
 ("roller", "Schilder- &amp; behangwerk", "Strak eindresultaat, netjes en vakkundig uitgevoerd.", "/schilder-groningen/"),
 ("key", "Zorg-appartementen", "Binnen maximaal 3 werkdagen weer beschikbaar voor een nieuwe cliënt.", "/zorgappartementen-opleveren/"),
 ("drop", "Hogedrukreiniging", "Daken, opritten, terreinen en gevels weer schoon en veilig.", "/hogedrukreiniging-groningen/"),
]
svc_cards = "".join(
    f'<a class="card svc-link" href="{u}"><div class="ic">{ic(i)}</div><h3>{t}</h3><p class="muted">{d}</p></a>'
    for i, t, d, u in SERVICES)

GREVIEWS = "https://www.google.com/maps/search/?api=1&query=JSTN+Multidiensten+Zernikepark+4+Groningen"
REVIEWS = [
 ("Matteo, Hoogezand", "Bij dit bedrijf kan je zeker terecht voor je reinigingsdiensten. Ze leveren grondig en goed werk. 5 sterren waard voor mij."),
 ("Luca, Groningen", "Service was top notch. My partner and I just moved to a new home and it was dirty! Sent a message to Justin and asked him if the day after he could come and do an urgency deep clean and he did it for less than i was expecting even if the work-load was more than he expected, excellent service overall will call again."),
 ("Milan, Froombosch", "Zeer tevreden over JSTN Multidiensten! Alles werd netjes en vakkundig uitgevoerd. De communicatie was duidelijk, afspraken werden goed nagekomen en het resultaat was precies zoals gehoopt. Zeker een aanrader als je op zoek bent naar een betrouwbare en professionele service!"),
]
rev_cards = "".join(f'<figure class="card rv">{STARS}<blockquote>“{q}”</blockquote><figcaption>{n}</figcaption></figure>' for n, q in REVIEWS)
REVIEWS_SEC = f'''<section class="sec" id="reviews">
<div class="w">
<div class="head"><span class="tag">Google Reviews</span><h2>Wat klanten over ons zeggen</h2><p class="lead"><b>5,0 ★</b> gemiddeld uit 15 reviews op Google · <a class="link" style="display:inline-flex" href="{GREVIEWS}" target="_blank" rel="noopener">Bekijk alle reviews{ic("arrow")}</a></p></div>
<div class="g3">{rev_cards}</div>
</div>
</section>'''

home = f'''<section class="sec">
<div class="w hero">
<div>
<span class="tag">Voor bedrijven en particulieren</span>
<h1>Schoonmaak, ontruiming en opleveringen. Wij regelen het.</h1>
<p class="lead">Van dieptereiniging tot een leeggeruimde, geschilderde woning. Eén team en één aanspreekpunt, voor bedrijven én particulieren.</p>
<div class="row" style="margin-top:22px">
<a class="btn" href="/contact/">{ic("mail")}Offerte aanvragen</a>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp ons</a>
</div>
<ul class="pts">
<li>{ic("check")}Reactie binnen 12 uur</li>
<li>{ic("check")}Flexibel inplanbaar, ook in (school)vakanties</li>
<li>{ic("check")}Ontruimen, schoonmaken en schilderen in één keer</li>
</ul>
</div>
<img class="photo" src="{wimg(IMG_BUSSEN, 900, 900, 'bussen-jstn-multidiensten')}" srcset="{wimg(IMG_BUSSEN, 600, 600, 'bussen-jstn-multidiensten')} 600w, {wimg(IMG_BUSSEN, 900, 900, 'bussen-jstn-multidiensten')} 900w" sizes="(max-width: 760px) 100vw, 540px" width="900" height="900" alt="Bedrijfsbussen van JSTN Multidiensten in Groningen" fetchpriority="high">
</div>
</section>

<section class="pb">
<div class="w g2">
<div class="card stack">
<div class="ic">{ic("office")}</div>
<h2 class="h3">Zakelijke dienstverlening</h2>
<p class="muted">Voor makelaars, woningcorporaties, zorginstellingen, scholen en bedrijven. Snel schakelen, vaste aanspreekpunten en zorg-appartementen binnen 3 werkdagen opgeleverd.</p>
<a class="link" href="/zakelijk/">Bekijk zakelijk{ic("arrow")}</a>
</div>
<div class="card stack">
<div class="ic">{ic("home")}</div>
<h2 class="h3">Particuliere dienstverlening</h2>
<p class="muted">Verhuizen, leegruimen, opleveren of uw nieuwe woning opknappen. Duidelijke afspraken en één vast contactpersoon van begin tot eind.</p>
<a class="link" href="/particulier/">Bekijk particulier{ic("arrow")}</a>
</div>
</div>
</section>

<section class="sec band">
<div class="w">
<div class="head">
<span class="tag">Onze diensten</span>
<h2>Alles onder één dak</h2>
<p class="lead">Van één klus tot het complete pakket: wij pakken het in één keer aan, zodat u maar één partij hoeft te bellen.</p>
</div>
<div class="g4">{svc_cards}</div>
</div>
</section>

{REVIEWS_SEC}

{CTA}'''
page("/", "Schoonmaak, ontruiming & verhuizen in Groningen | JSTN Multidiensten",
     "JSTN Multidiensten in Groningen: schoonmaak, vloerreiniging, ontruimen, verhuizen, schilderwerk en zorg-appartementen opleveren. Eén aanspreekpunt, reactie binnen 12 uur.",
     "/", home, extra_ld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "JSTN Multidiensten", "url": BASE + "/"}])

# ======================= ZAKELIJK =======================
zak_svcs = [
 ("sparkle", "Schoonmaak &amp; desinfectie", "schoonmaak", [
   "Reguliere schoonmaak of een grondige dieptereiniging van kantoren, woningen en zorgappartementen, met professionele apparatuur en desinfectiemiddelen."]),
 ("floor", "Vloerreiniging", "vloerreiniging", [
   "Grote vloeren in scholen, kantoren en bedrijfspanden grondig schoon. Eenmalig of periodiek, ook in (school)vakanties."]),
 ("key", "Zorg-appartementen", "zorg-appartementen", [
   "Bij vertrek van een bewoner is het appartement binnen maximaal 3 werkdagen weer beschikbaar: opknappen, schoonmaken en desgewenst de administratie."]),
 ("box", "Ontruimen", "ontruimen", [
   "Ontruiming bij (gedwongen) beëindiging van de huur: snel, zorgvuldig en duurzaam. Ook spoedontruimingen."]),
 ("roller", "Schilder- &amp; behangwerk", "schilderwerk", [
   "Wanden en plafonds bijwerken of volledig opnieuw schilderen en behangen, netjes en strak afgewerkt."]),
 ("drop", "Hogedrukreiniging", "hogedrukreiniging", [
   "Daken, terreinen, looppaden en gevels vrij van mos en aanslag: veilig, representatief en eenmalig of volgens schema."]),
 ("window", "Glasbewassing", "glasbewassing", [
   "Streeploos schone ramen voor kantoren en bedrijfspanden, eenmalig of periodiek."]),
]
zak = f'''<section class="sec">
<div class="w hero">
<div>
<span class="tag">Zakelijk · B2B</span>
<h1>Zakelijke dienstverlening in Groningen</h1>
<p class="lead">Voor makelaars, woningcorporaties, zorginstellingen, scholen en bedrijven. Vaste aanspreekpunten en korte lijnen.</p>
<div class="row" style="margin-top:22px">
<a class="btn" href="/contact/">{ic("mail")}Offerte aanvragen</a>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp ons</a>
</div>
</div>
<div class="g1">
<div class="card"><div class="ic">{ic("bolt")}</div><h2 class="h3">Snel &amp; flexibel</h2><p class="muted">Een onverwachte aanvraag of extra werk? Wij schakelen snel, zodat uw bedrijfsprocessen zo min mogelijk worden verstoord.</p></div>
<div class="card"><div class="ic">{ic("users")}</div><h2 class="h3">Persoonlijke betrokkenheid</h2><p class="muted">Vaste aanspreekpunten en waar mogelijk een vertrouwd team. Korte lijnen en duidelijke communicatie.</p></div>
</div>
</div>
</section>

<section class="sec band">
<div class="w">
<div class="head"><span class="tag">Onze diensten</span><h2>Wat wij voor uw organisatie doen</h2></div>
<div class="g2x">{"".join(svc(i, t, p, a) for i, t, a, p in zak_svcs)}</div>
</div>
</section>

{CTA}'''
page("/zakelijk/", "Zakelijke schoonmaak, vloerreiniging & ontruiming Groningen | JSTN",
     "Zakelijke dienstverlening in Groningen: schoonmaak en desinfectie, vloerreiniging voor scholen en kantoren, ontruimen, schilderwerk en zorg-appartementen binnen 3 werkdagen opgeleverd.",
     "/zakelijk/", zak, extra_ld=[crumbs([("Home", "/"), ("Zakelijk", "/zakelijk/")])])

# ======================= PARTICULIER =======================
par_svcs = [
 ("truck", "Verhuizingen", "verhuizingen", [
   "Inpakken, verhuizen en uitpakken, met extra aandacht voor senioren. We richten kasten in, hangen schilderijen op en sluiten apparatuur aan. Verhuisdozen zijn beschikbaar."]),
 ("box", "Leegruimen", "leegruimen", [
   "Woning, schuur, berging en tuin volledig leeg en netjes afgevoerd. Bruikbare spullen krijgen waar mogelijk een tweede leven."]),
 ("clip", "Opleveringen", "opleveringen", [
   "Uw huurwoning opgeleverd volgens de voorwaarden van corporatie of verhuurder. Vooraf duidelijke afspraken, een vaste prijs is mogelijk."]),
 ("roller", "Schilder- &amp; behangwerk", "schilderwerk", [
   "Uw nieuwe woning opgeknapt. Ook vloeren, gordijnen of aanpassingen in keuken of badkamer regelen wij, met één aanspreekpunt."]),
 ("drop", "Hogedrukreiniging", "hogedrukreiniging", [
   "Oprit, terras of dak weer schoon en veilig, inclusief nieuw voegzand tegen onkruid."]),
 ("sparkle", "Schoonmaak &amp; dieptereiniging", "schoonmaak", [
   "Grondig schoon na een verhuizing of ontruiming: ontvetten, ontkalken en waar nodig ontsmetten."]),
]
par = f'''<section class="sec">
<div class="w hero">
<div>
<span class="tag">Particulier · B2C</span>
<h1>Particuliere dienstverlening in Groningen</h1>
<p class="lead">Verhuizen, leegruimen, uw woning opleveren of uw nieuwe huis opknappen. Wij regelen het van begin tot eind, met duidelijke afspraken en één vast contactpersoon.</p>
<div class="row" style="margin-top:22px">
<a class="btn" href="/contact/">{ic("mail")}Offerte aanvragen</a>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp ons</a>
</div>
</div>
<div class="g1">
<div class="card"><div class="ic">{ic("bolt")}</div><h2 class="h3">Snel &amp; flexibel</h2><p class="muted">We plannen samen met u en houden ons aan de afspraken. <b>Afspraak is afspraak.</b></p></div>
<div class="card"><div class="ic">{ic("chat")}</div><h2 class="h3">Persoonlijk contact</h2><p class="muted">Eén vast contactpersoon, heldere communicatie en duidelijke afspraken van begin tot eind.</p></div>
</div>
</div>
</section>

<section class="sec band">
<div class="w">
<div class="head"><span class="tag">Onze diensten</span><h2>Waar wij u mee helpen</h2></div>
<div class="g2x">{"".join(svc(i, t, p, a) for i, t, a, p in par_svcs)}</div>
</div>
</section>

{REVIEWS_SEC}

{CTA}'''
page("/particulier/", "Verhuizen, leegruimen & woning opleveren in Groningen | JSTN",
     "Particuliere dienstverlening in Groningen: verhuizingen (ook voor senioren), woning leegruimen, opleveren aan verhuurder of corporatie, schilderwerk en hogedrukreiniging. Eén vast aanspreekpunt.",
     "/particulier/", par, extra_ld=[crumbs([("Home", "/"), ("Particulier", "/particulier/")])])

# ======================= OVER ONS =======================
MISSIE = '''<section class="pb">
<div class="w">
<div class="dark" style="padding:40px">
<h2 class="acc" style="margin-top:0">Onze missie</h2>
<p style="color:#E2E8EC;max-width:820px">Wij geven jonge mensen de kans om zich te ontwikkelen, verantwoordelijkheid te nemen en te groeien. Ambitie, kwaliteit en plezier komen bij ons samen, in een hecht team dat elkaar helpt en iedere dag beter wil worden.</p>
<p style="font-weight:800;font-size:18px;margin:18px 0 0">Onze ambitie is duidelijk: <span class="acc">samen groeien, samen beter worden en samen iets neerzetten waar we trots op kunnen zijn.</span></p>
</div>
</div>
</section>'''
over = f'''<section class="sec">
<div class="w hero">
<div>
<span class="tag">Over ons</span>
<h1>Jong, ambitieus en gedreven</h1>
<p class="lead">Wij zijn een jong, ambitieus team met grote plannen. Niet stilstaan, maar iedere dag beter worden en blijven groeien.</p>
<p class="muted">We werken hard, nemen verantwoordelijkheid en blijven leren. Zo bouwen we aan een bedrijf waar klanten en medewerkers trots op zijn, zonder te vergeten waar we vandaan komen.</p>
</div>
<img class="photo" src="{wimg(IMG_KANTOOR, 900, 900, 'kantoor-jstn-multidiensten')}" srcset="{wimg(IMG_KANTOOR, 600, 600, 'kantoor-jstn-multidiensten')} 600w, {wimg(IMG_KANTOOR, 900, 900, 'kantoor-jstn-multidiensten')} 900w" sizes="(max-width: 760px) 100vw, 540px" width="900" height="900" alt="Kantoor van JSTN Multidiensten aan het Zernikepark in Groningen" loading="lazy">
</div>
</section>

<section class="pb">
<div class="w g4">
{card("users", "Goede sfeer", "Een team dat elkaar helpt en samen plezier heeft in het werk.", "h2")}
{card("heart", "Persoonlijke aandacht", "Voor iedere klant en iedere collega.", "h2")}
{card("check", "Kwaliteit", "Netjes, vakkundig en met oog voor het eindresultaat.", "h2")}
{card("home", "Samenwerking", "Korte lijnen en duidelijke afspraken.", "h2")}
</div>
</section>

{MISSIE}

{CTA}'''
page("/over-ons/", "Over ons | JSTN Multidiensten Groningen",
     "Maak kennis met JSTN Multidiensten: een jong, ambitieus team uit Groningen dat schoonmaakt, ontruimt, verhuist en schildert — met persoonlijke aandacht en kwaliteit als basis.",
     "/over-ons/", over, extra_ld=[crumbs([("Home", "/"), ("Over ons", "/over-ons/")])])

# ======================= WERKEN BIJ =======================
werk = f'''<section class="sec">
<div class="w hero" style="align-items:start">
<div>
<span class="tag">Vacatures</span>
<h1>Join the team!</h1>
<p class="lead">Wij zijn altijd op zoek naar enthousiaste mensen die ons team willen versterken!</p>
<p class="muted">Ons team bestaat uit jonge, gezellige en gemotiveerde collega’s die samen zorgen voor een fijne werksfeer. We vinden het belangrijk dat je met plezier naar je werk gaat, jezelf kunt zijn en samen met je collega’s een mooie ervaring neerzet voor onze klanten. Lijkt het jou leuk om ons team te komen versterken?</p>
</div>
<div class="card">
<h2 class="h3">Stuur ons een berichtje</h2>
<p class="muted">Stuur ons een mailtje of bel ons gerust. We maken graag kennis met je en wie weet ben jij binnenkort onze nieuwe collega!</p>
<div class="opts">
<a class="opt" href="{WA}?text=Hoi%2C%20ik%20heb%20interesse%20om%20bij%20JSTN%20Multidiensten%20te%20werken!" target="_blank" rel="noopener"><span class="ic wa">{ic("wa")}</span><span><b>WhatsApp</b><small>{TEL_TXT}</small></span></a>
<a class="opt" href="tel:{TEL}"><span class="ic">{ic("tel")}</span><span><b>Bellen</b><small>{TEL_TXT}</small></span></a>
<a class="opt" href="mailto:{MAIL}?subject=Werken%20bij%20JSTN%20Multidiensten"><span class="ic">{ic("mail")}</span><span><b>E-mail</b><small>{MAIL}</small></span></a>
</div>
</div>
</div>
</section>

{MISSIE}'''
page("/werken-bij/", "Werken bij JSTN Multidiensten | Vacatures Groningen",
     "Werken bij JSTN Multidiensten in Groningen? Wij zoeken enthousiaste collega’s voor schoonmaak, ontruiming, verhuizingen en schilderwerk. Stuur ons een berichtje!",
     "/werken-bij/", werk, extra_ld=[crumbs([("Home", "/"), ("Bij ons werken", "/werken-bij/")])])

# ======================= CONTACT =======================
DIENSTEN_OPT = "".join(f"<option>{d}</option>" for d in [
    "Schoonmaak / dieptereiniging", "Vloerreiniging", "Glasbewassing", "Ontruiming / leegruimen", "Verhuizen",
    "Schilder- en behangwerk", "Zorg-appartement opleveren", "Woning opleveren", "Hogedrukreiniging", "Anders / meerdere diensten"])
contact = f'''<section class="sec">
<div class="w">
<div class="head"><span class="tag">Contact</span><h1>Neem contact met ons op</h1><p class="lead">Vraag een offerte aan of stel uw vraag. Het snelst bereikt u ons via WhatsApp — we reageren binnen 12 uur.</p></div>
<div class="cgrid">
<div class="card">
<div class="tabs" role="tablist">
<button type="button" class="tab on" data-tab="wa" role="tab" aria-selected="true">WhatsApp</button>
<button type="button" class="tab" data-tab="mail" role="tab" aria-selected="false">E-mail</button>
</div>

<div class="pane on" id="pane-wa">
<h2 class="h3">Stuur ons een WhatsApp</h2>
<p class="muted">Vul het in en klik op de knop — uw bericht staat dan direct klaar in WhatsApp.</p>
<form id="waForm" novalidate>
<div class="r2">
<div><label for="naam">Naam *</label><input id="naam" required autocomplete="name" placeholder="Uw naam"></div>
<div><label for="type">Ik ben</label><select id="type"><option>Particulier</option><option>Bedrijf / organisatie</option></select></div>
</div>
<div class="r2">
<div><label for="dienst">Dienst</label><select id="dienst">{DIENSTEN_OPT}</select></div>
<div><label for="plaats">Plaats</label><input id="plaats" autocomplete="address-level2" placeholder="Bijv. Groningen"></div>
</div>
<label for="bericht">Uw vraag of omschrijving *</label>
<textarea id="bericht" required placeholder="Bijv. 3-kamerappartement eindschoonmaak, opleveren op 15 november."></textarea>
<button type="submit" class="btn btn-wa full">{ic("wa")}Verstuur via WhatsApp</button>
<p class="small">Werkt op telefoon en computer (WhatsApp Web).</p>
</form>
</div>

<div class="pane" id="pane-mail">
<h2 class="h3">Stuur ons een e-mail</h2>
<p class="muted">Vraag een offerte aan — u ontvangt binnen 12 uur een reactie per mail.</p>
<form id="mailForm" novalidate>
<div class="r2">
<div><label for="m-naam">Naam *</label><input id="m-naam" name="Naam" required autocomplete="name" placeholder="Uw naam"></div>
<div><label for="m-type">Ik ben</label><select id="m-type" name="Type klant"><option>Particulier</option><option>Bedrijf / organisatie</option></select></div>
</div>
<div class="r2">
<div><label for="m-email">E-mailadres *</label><input id="m-email" name="email" type="email" required autocomplete="email" placeholder="naam@voorbeeld.nl"></div>
<div><label for="m-tel">Telefoon</label><input id="m-tel" name="Telefoon" type="tel" autocomplete="tel" placeholder="06 ..."></div>
</div>
<div class="r2">
<div><label for="m-dienst">Dienst</label><select id="m-dienst" name="Dienst">{DIENSTEN_OPT}</select></div>
<div><label for="m-plaats">Plaats</label><input id="m-plaats" name="Plaats" autocomplete="address-level2" placeholder="Bijv. Groningen"></div>
</div>
<label for="m-bericht">Uw vraag of omschrijving *</label>
<textarea id="m-bericht" name="Bericht" required placeholder="Omschrijf de klus, gewenste datum, etc."></textarea>
<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<button type="submit" class="btn full" id="mailKnop">Verstuur aanvraag</button>
<div class="msg" id="mailMelding" role="status"></div>
<p class="small">Door te versturen gaat u akkoord met ons <a href="/privacy/">privacybeleid</a>.</p>
</form>
</div>
</div>

<div class="card">
<h2 class="h3">Liever direct contact?</h2>
<p class="muted">Kies wat voor u het makkelijkst is.</p>
<div class="opts">
<a class="opt" href="{WA}?text=Hallo%20JSTN%20Multidiensten%2C%20ik%20heb%20een%20vraag%3A%20" target="_blank" rel="noopener"><span class="ic wa">{ic("wa")}</span><span><b>WhatsApp</b><small>{TEL_TXT}</small></span></a>
<a class="opt" href="tel:{TEL}"><span class="ic">{ic("tel")}</span><span><b>Bellen</b><small class="u">{TEL_TXT}</small></span></a>
<a class="opt" href="mailto:{MAIL}"><span class="ic">{ic("mail")}</span><span><b>E-mail</b><small>{MAIL}</small></span></a>
</div>
<div class="info"><p><b>JSTN Multidiensten</b></p><p>Zernikepark 4<br>9747 AN Groningen</p></div>
<div class="dark promise"><span class="acc" style="font-weight:800">Reactie binnen 12 uur.</span> Flexibel inplanbaar, ook in (school)vakanties.</div>
</div>
</div>
</div>
</section>
<script src="/contact.js" defer></script>'''
page("/contact/", "Contact & offerte aanvragen | JSTN Multidiensten Groningen",
     "Neem contact op met JSTN Multidiensten in Groningen via WhatsApp, telefoon (+31 6 36179549) of e-mail. Vraag vrijblijvend een offerte aan — reactie binnen 12 uur.",
     "/contact/", contact, extra_ld=[crumbs([("Home", "/"), ("Contact", "/contact/")])])

# ======================= PRIVACY =======================
PRIV = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "privacy.html"), encoding="utf-8").read()
page("/privacy/", "Privacyverklaring | JSTN Multidiensten",
     "Lees hoe JSTN Multidiensten omgaat met uw persoonsgegevens: welke gegevens we verwerken, waarom, hoe lang en welke rechten u heeft.",
     "", f'<section class="sec"><div class="w prose">{PRIV}</div></section>')

# ======================= BLOG =======================
import posts
blog_cards = ""
for p in sorted(posts.POSTS, key=lambda x: x["date"], reverse=True):
    blog_cards += f'''<a class="card post-card" href="/post/{p["slug"]}/"><div class="ic">{ic(p["icon"])}</div><p class="meta">{p["date_nl"]} · {p["cat"]}</p><h2 class="h3">{p["title"]}</h2><p class="muted">{p["desc"]}</p><span class="link">Lees verder{ic("arrow")}</span></a>'''
    art_ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
              "datePublished": p["date"], "dateModified": p.get("modified", p["date"]),
              "author": {"@type": "Person", "name": "Justin", "jobTitle": "Eigenaar"},
              "publisher": {"@id": BASE + "/#bedrijf"}, "mainEntityOfPage": BASE + f"/post/{p['slug']}/",
              "image": BASE + "/og-image.jpg", "inLanguage": "nl-NL"}
    lds = [art_ld, crumbs([("Home", "/"), ("Blog", "/blog/"), (p["title"], f"/post/{p['slug']}/")])]
    if p.get("faq"):
        lds.append({"@context": "https://schema.org", "@type": "FAQPage",
                    "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]})
    faq_html = ""
    if p.get("faq"):
        faq_html = '<h2>Veelgestelde vragen</h2>' + "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in p["faq"])
    src_html = ""
    if p.get("sources"):
        src_html = '<h2>Bronnen</h2><ul>' + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in p["sources"]) + '</ul>'
    others = [o for o in posts.POSTS if o["slug"] != p["slug"]]
    more = "".join(f'<a class="card post-card" href="/post/{o["slug"]}/"><p class="meta">{o["date_nl"]}</p><h3>{o["title"]}</h3><span class="link">Lees verder{ic("arrow")}</span></a>' for o in others)
    body = f'''<section class="sec">
<div class="w narrow">
<nav class="bc" aria-label="Kruimelpad"><a href="/">Home</a> › <a href="/blog/">Blog</a> › <span>{p["title"]}</span></nav>
<article class="card prose">
<p class="meta">{p["date_nl"]} · {p["cat"]} · door Justin, eigenaar</p>
<h1>{p["title"]}</h1>
{p["html"]}
{faq_html}
<div class="note"><b>Hoe dit artikel tot stand kwam</b><br>{p["note"]}</div>
{src_html}
</article>
<div class="dark cta" style="margin-top:24px">
<div><h2 style="color:#fff;margin:0 0 6px">Hulp nodig bij uw klus?</h2><p style="color:#E2E8EC;margin:0"><span class="acc" style="font-weight:800">Reactie binnen 12 uur.</span> Vraag vrijblijvend een offerte aan.</p></div>
<div class="row"><a class="btn btn-light" href="/contact/">Offerte aanvragen</a><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp</a></div>
</div>
{('<h2 style="margin-top:40px">Lees ook</h2><div class="g2">' + more + '</div>') if more else ''}
</div>
</section>'''
    page(f"/post/{p['slug']}/", p["seo_title"], p["desc"], "/blog/", body, extra_ld=lds, og_type="article")

blog = f'''<section class="sec">
<div class="w">
<div class="head"><span class="tag">Blog</span><h1>Tips &amp; advies</h1><p class="lead">Praktische artikelen over schoonmaak, ontruimen, verhuizen en opleveren in Groningen en omgeving.</p></div>
<div class="g2">{blog_cards}</div>
</div>
</section>
{CTA}'''
page("/blog/", "Blog: tips over schoonmaak, ontruimen & verhuizen | JSTN Multidiensten",
     "Tips en advies van JSTN Multidiensten over zakelijke schoonmaak, woningontruiming, verhuizen en opleveren in Groningen.",
     "/blog/", blog, extra_ld=[crumbs([("Home", "/"), ("Blog", "/blog/")])])



# ======================= PORTFOLIO =======================
import shutil
_src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "portfolio_img")
_dst = os.path.join(OUT, "portfolio", "img"); os.makedirs(_dst, exist_ok=True)
for _f in os.listdir(_src): shutil.copy(os.path.join(_src, _f), _dst)
PF = [
 {"titel": "Badkamer ontkalkt bij een eindschoonmaak", "dienst": "schoonmaak-groningen", "label": "Schoonmaak",
  "tekst": "Douchewand en douchedeur zaten vol kalk en aanslag. Na het ontkalken is het glas weer helder en de douchebak schoon — klaar voor de volgende bewoner.",
  "paren": [("douchewand-voor", "douchewand-na", "Douchewand"), ("douchedeur-voor", "douchedeur-na", "Douchedeur")]},
 {"titel": "Ventilatieventielen gereinigd", "dienst": "schoonmaak-groningen", "label": "Dieptereiniging",
  "tekst": "Ventielen die dichtzaten met stof en vuil. Schoongemaakt zodat de ventilatie weer goed werkt — een onderdeel dat bij een gewone schoonmaak vaak wordt overgeslagen.",
  "paren": [("ventilatie-voor", "ventilatie-na", "Ventiel badkamer"), ("ventilatie-2-voor", "ventilatie-2-na", "Ventiel plafond")]},
 {"titel": "Gaskookplaat ontvet", "dienst": "woning-opleveren-groningen", "label": "Opleveringsschoonmaak",
  "tekst": "Ingebrand vet en vuil op en rond de branders. Na de reiniging glanst het rvs weer — precies wat een verhuurder bij de oplevering wil zien.",
  "paren": [("kookplaat-voor", "kookplaat-na", "Kookplaat")]},
 {"titel": "Vloerreiniging met de schrobmachine", "dienst": "vloerreiniging-groningen", "label": "Vloerreiniging",
  "tekst": "Grote vloeren in een bedrijfspand en keuken grondig gereinigd met een professionele schrobmachine. Vuil dat met dweilen blijft zitten, komt hiermee wel los.",
  "fotos": [("vloerreiniging-schrobmachine", "Schrobmachine op een pvc-vloer"), ("vloerreiniging-bedrijfspand", "Betonvloer in een bedrijfspand"), ("vloerreiniging-keuken", "Keukenvloer")]},
 {"titel": "Bouwoplevering: glasbewassing en opleverschoonmaak", "dienst": "schoonmaak-groningen", "label": "Bouwoplevering",
  "tekst": "Bij de oplevering van een verbouwd kantoorpand hebben wij alle glazen wanden en ramen streeploos schoongemaakt. Daarna is het complete pand schoongemaakt, zodat het netjes en direct bruikbaar kon worden opgeleverd.",
  "fotos": [("glasbewassing-kantoor", "Glasbewassing bij de bouwoplevering van een kantoorpand")]},
 {"titel": "Tegels schoon met hogedruk", "dienst": "hogedrukreiniging-groningen", "label": "Hogedrukreiniging",
  "tekst": "Aanslag en vuil van de tegels gespoten. Het verschil tussen de gereinigde en de vuile tegels is direct zichtbaar.",
  "fotos": [("hogedrukreiniging-tegels", "Hogedrukreiniging van tegels")]},
]
def pf_img(n, alt, cls=""):
    return f'<img{(" class=" + cls) if cls else ""} src="/portfolio/img/{n}.jpg" width="900" height="1200" alt="{alt}" loading="lazy">'
def pf_card(pr):
    if pr.get("paren"):
        media = "".join(f'<div class="ba"><figure>{pf_img(v, w + " voor de schoonmaak")}<figcaption>Voor</figcaption></figure><figure>{pf_img(n, w + " na de schoonmaak")}<figcaption class="na">Na</figcaption></figure></div>' for v, n, w in pr["paren"])
    else:
        media = '<div class="pfg">' + "".join(f'<figure>{pf_img(n, a)}</figure>' for n, a in pr["fotos"]) + '</div>'
    d = next(x for x in D.DIENSTEN if x["slug"] == pr["dienst"])
    return f'<article class="card pf"><span class="tag">{pr["label"]}</span><h2 class="h3">{pr["titel"]}</h2><p class="muted">{pr["tekst"]}</p>{media}<a class="link" href="/{d["slug"]}/">Meer over {d["kort"].lower()}{ic("arrow")}</a></article>'
pf = f"""<section class="sec">
<div class="w">
<div class="head"><span class="tag">Portfolio</span><h1>Ons werk in Groningen en omgeving</h1><p class="lead">Een greep uit onze klussen: schoonmaak, bouwopleveringen, vloerreiniging, glasbewassing en hogedrukreiniging. Echte foto's van ons eigen werk — voor en na.</p><p class="muted">Dit portfolio wordt regelmatig aangevuld met nieuwe klussen. Kom dus gerust nog eens terug.</p></div>
<div class="pfl">{"".join(pf_card(x) for x in PF)}</div>
</div>
</section>

{REVIEWS_SEC}

{CTA}"""
page("/portfolio/", "Portfolio: voor en na foto's van ons werk | JSTN Multidiensten",
     "Bekijk voor- en na-foto's van klussen van JSTN Multidiensten in Groningen: eindschoonmaak, bouwoplevering, ontkalken, vloerreiniging met schrobmachine, glasbewassing en hogedrukreiniging.",
     "/portfolio/", pf, extra_ld=[crumbs([("Home", "/"), ("Portfolio", "/portfolio/")])])
PF_BY = {}
for _x in PF: PF_BY.setdefault(_x["dienst"], []).append(_x)

# ======================= DIENSTPAGINA'S =======================
BYSLUG = {d["slug"]: d for d in D.DIENSTEN}
PLAATS_TXT = ", ".join(D.PLAATSEN[:-1]) + " en " + D.PLAATSEN[-1]
for d in D.DIENSTEN:
    path = f"/{d['slug']}/"
    pts = "".join(f"<li>{ic('check')}{x}</li>" for x in d["pts"])
    blok = "".join(card(i, t, x) for i, t, x in d["blokken"])
    faq = "".join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in d["faq"])
    verw = "".join(f'<a class="card svc-link" href="/{v}/"><div class="ic">{ic(BYSLUG[v]["icon"])}</div><h3>{BYSLUG[v]["kort"]}</h3><p class="muted">{D.KAART[v]}</p></a>' for v in d["verwant"])
    blog = ""
    if d.get("blog"):
        bp = next((p for p in posts.POSTS if p["slug"] == d["blog"]), None)
        if bp:
            blog = f'<p class="muted" style="margin-top:18px">Lees ook: <a class="link" style="display:inline-flex" href="/post/{bp["slug"]}/">{bp["title"]}{ic("arrow")}</a></p>'
    pfsec = ""
    if d["slug"] in PF_BY:
        pfsec = f'''<section class="sec band"><div class="w"><div class="head"><span class="tag">Uit ons werk</span><h2>Voor en na</h2></div><div class="pfl">{"".join(pf_card(x) for x in PF_BY[d["slug"]])}</div><p style="margin-top:18px"><a class="link" href="/portfolio/">Bekijk het hele portfolio{ic("arrow")}</a></p></div></section>

'''
    body = f"""<section class="sec">
<div class="w hero">
<div>
<nav class="bc" aria-label="Kruimelpad"><a href="/">Home</a> › <span>{d["kort"]}</span></nav>
<span class="tag">Groningen en omgeving</span>
<h1>{d["h1"]}</h1>
<p class="lead">{d["lead"]}</p>
<div class="row" style="margin-top:22px">
<a class="btn" href="/contact/">{ic("mail")}Offerte aanvragen</a>
<a class="btn btn-wa" href="{WA}?text={quote('Hallo JSTN Multidiensten, ik heb een vraag over ' + d['kort'].lower() + ': ')}" target="_blank" rel="noopener">{ic("wa")}WhatsApp ons</a>
</div>
</div>
<div class="card">
<h2 class="h3">Waarom JSTN Multidiensten</h2>
<ul class="pts" style="margin-top:12px">{pts}<li>{ic("check")}Reactie binnen 12 uur</li><li>{ic("check")}5,0 ★ uit 15 Google-reviews</li></ul>
</div>
</div>
</section>

<section class="sec band">
<div class="w">
<div class="head"><span class="tag">Wat wij doen</span><h2>{d["kort"]} door JSTN Multidiensten</h2></div>
<div class="{'g2x' if len(d['blokken']) % 2 == 0 else 'g3'}">{blok}</div>
</div>
</section>

<section class="sec">
<div class="w g2" style="align-items:start">
<div>
<span class="tag">Veelgestelde vragen</span>
<h2>Vragen over {d["kort"].lower()}</h2>
{faq}
</div>
<div class="card">
<div class="ic">{ic("pin")}</div>
<h2 class="h3">Werkgebied</h2>
<p class="muted">Wij werken in de stad Groningen en tot ongeveer 50 km daaromheen, onder andere in {PLAATS_TXT}.</p>
<p class="muted">Vanuit ons kantoor aan het Zernikepark 4 in Groningen zijn we snel ter plaatse.</p>
{blog}
</div>
</div>
</section>

{pfsec}{REVIEWS_SEC}

<section class="pb">
<div class="w">
<div class="head"><span class="tag">Combineer en bespaar tijd</span><h2>Andere diensten</h2></div>
<div class="g3">{verw}</div>
</div>
</section>

{CTA}"""
    lds = [crumbs([("Home", "/"), (d["kort"], path)]),
           {"@context": "https://schema.org", "@type": "Service", "name": d["h1"], "serviceType": d["kort"],
            "description": d["desc"], "url": BASE + path, "provider": {"@id": BASE + "/#bedrijf"},
            "areaServed": [{"@type": "City", "name": n} for n in D.PLAATSEN]},
           {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]]}]
    page(path, d["title"], d["desc"], "", body, extra_ld=lds)

# ======================= 404 =======================
nf = f'''<section class="sec"><div class="w narrow" style="text-align:center">
<span class="tag">404</span><h1>Deze pagina bestaat niet (meer)</h1>
<p class="lead" style="margin:0 auto 22px">Misschien is de pagina verplaatst. Kijk op de homepage of neem direct contact met ons op.</p>
<div class="row" style="justify-content:center"><a class="btn" href="/">Naar de homepage</a><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{ic("wa")}WhatsApp</a></div>
</div></section>'''
page("/404.html", "Pagina niet gevonden | JSTN Multidiensten", "Deze pagina bestaat niet (meer).", "", nf)
# 404 mag niet in de index
fn404 = os.path.join(OUT, "404.html")
s = open(fn404, encoding="utf-8").read().replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
s = s.replace(f'<link rel="canonical" href="{BASE}/404.html">\n', "")
open(fn404, "w", encoding="utf-8").write(s)

# ======================= sitemap / robots / redirects =======================
pages_sm = [("/", "1.0"), ("/zakelijk/", "0.9"), ("/particulier/", "0.9"), ("/contact/", "0.8"), ("/over-ons/", "0.6"),
            ("/werken-bij/", "0.5"), ("/blog/", "0.7"), ("/portfolio/", "0.8"), ("/privacy/", "0.2")] + [(f"/{d['slug']}/", "0.9") for d in D.DIENSTEN] + [(f"/post/{p['slug']}/", "0.6", p.get("modified", p["date"])) for p in posts.POSTS]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, pr, *lm in pages_sm:
    sm += f"  <url><loc>{BASE}{u}</loc><lastmod>{lm[0] if lm else '2026-10-04'}</lastmod><priority>{pr}</priority></url>\n"
sm += "</urlset>\n"
open(os.path.join(OUT, "sitemap.xml"), "w").write(sm)
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

redirects = """# Oude Wix-adressen -> nieuwe pagina's (301 = permanent, behoudt Google-waarde)
/about-us              /zakelijk/      301
/about-us-1            /particulier/   301
/blank-1               /werken-bij/    301
/blank-1-1             /over-ons/      301
/privacy-policy        /privacy/       301
/portfolio-collections/*  /portfolio/  301
/blog/categories/*     /blog/          301
/blog/page/*           /blog/          301
# Oude Wix-sitemaps
/pages-sitemap.xml                 /sitemap.xml  301
/blog-posts-sitemap.xml            /sitemap.xml  301
/blog-categories-sitemap.xml       /sitemap.xml  301
/portfolio-projects-sitemap.xml    /sitemap.xml  301
/portfolio-collections-sitemap.xml /sitemap.xml  301
"""
open(os.path.join(OUT, "_redirects"), "w").write(redirects)

headers = """/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
/*.png
  Cache-Control: public, max-age=31536000
/*.jpg
  Cache-Control: public, max-age=31536000
"""
open(os.path.join(OUT, "_headers"), "w").write(headers)
print("klaar")
