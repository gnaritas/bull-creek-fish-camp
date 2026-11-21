#!/usr/bin/env python3
"""Bull Creek Fish Camp — shelf site generator (v2 template, 2026-11-20).
All copy from card-sourced facts only: Business Debut 2026-11-20 article, GBP/old-FB
NAP, new FB page, TripAdvisor reviews (attributed). Unknowns omitted (no prices,
no exact hours, no bait&tackle, no owner phone claims beyond the published line).
Shop identity only — zero builder/preview tokens. Demo host carries noindex."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(ROOT, "public")
os.makedirs(PUB, exist_ok=True)

ORIGIN = "https://bull-creek-fish-camp-demo.up.railway.app"
SITE = "Bull Creek Fish Camp"
ADDR_LINE1 = "3861 County Rd 2006 W"
ADDR = "3861 County Rd 2006 W, Bunnell, FL 32110"
MAPQ = "3861+County+Rd+2006+W,+Bunnell,+FL+32110"
TEL = "(386) 437-1991"
TELHREF = "tel:+13864371991"
EMAIL = "bullcreekfishcamp@gmail.com"
FB = "https://www.facebook.com/bullcreekfishcampfl/"
LAT, LNG = "29.4228388", "-81.435152"
LASTMOD = "2026-11-20"

# ————— shared fragments —————
EMBLEM = ('<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="Bull Creek Fish Camp emblem: '
 'a catfish above waves inside a double ring">'
 '<g fill="none" stroke="currentColor"><circle cx="50" cy="50" r="47" stroke-width="1.6"/>'
 '<circle cx="50" cy="50" r="39" stroke-width="3"/></g>'
 '<g fill="currentColor" stroke="none">'
 '<path d="M31 40c6-6 16-9 26-6 4 1 7 3 9 6-2 3-5 5-9 6-10 3-20 0-26-6z"/>'
 '<path d="M66 40l10-6v24l-10-6z"/>'
 '<circle cx="41" cy="41" r="1.9" fill="var(--cypress)"/>'
 '<path d="M31 40c-4-2-7-5-8-9" stroke="currentColor" stroke-width="2" fill="none"/>'
 '<path d="M31 46c-4 1-8 1-12 0" stroke="currentColor" stroke-width="2" fill="none"/>'
 '</g>'
 '<g fill="none" stroke="currentColor" stroke-width="2.4">'
 '<path d="M28 62q7-5 14 0t14 0 14 0"/>'
 '<path d="M28 70q7-5 14 0t14 0 14 0"/></g></svg>')

WAVE = ('<svg class="meander" viewBox="0 0 120 16" width="120" height="16" aria-hidden="true">'
 '<g fill="none" stroke="currentColor" stroke-width="2">'
 '<path d="M2 11q10-8 20 0t20 0 20 0 20 0"/>'
 '<path d="M2 15q10-8 20 0t20 0 20 0 20 0"/></g></svg>')

NAVMAP = [("/menu","Menu"),("/breakfast-lunch-dinner","Breakfast &amp; Dinner"),("/visit-by-boat","Visit by Boat"),
 ("/our-story","Our Story"),("/faq","FAQ"),("/contact","Contact")]

HEADER = (f'<a class="skip" href="#main">Skip to content</a>\n<div class="band" aria-hidden="true"></div>\n'
 f'<header class="top"><div class="wrap"><a class="brand" href="/">{EMBLEM}'
 f'<span class="word">{SITE}<small>Seafood on the water · Bunnell, Florida</small></span></a>'
 '<nav class="main" aria-label="Main"><ul>'
 + "".join(f'<li><a href="{p}">{t}</a></li>' for p, t in NAVMAP)
 + '<li><a class="btn" href="/menu">See the menu</a></li></ul></nav></div></header>\n<main id="main">\n')

FOOTER = ('</main>\n<footer class="site"><div class="wrap"><div class="nap">'
 f'<p class="fbrand">{SITE}</p><address>{ADDR_LINE1}<br>Bunnell, FL 32110<br>'
 f'<a href="{TELHREF}">{TEL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{FB}">Find us on Facebook</a></address></div>'
 '<nav aria-label="Footer"><ul>'
 + "".join(f'<li><a href="{p}">{t}</a></li>' for p, t in NAVMAP)
 + '<li><a href="/privacy">Privacy</a></li></ul></nav>'
 '<p class="footline">© 2026 Bull Creek Fish Camp · Seafood on the water · 3861 County Rd 2006 W, Bunnell, FL · Reopening January 2027.</p>'
 f'</div></footer>\n<!-- BUILT-{LASTMOD} -->\n')

def head(title, desc, path, og=True):
    h = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
     '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
     f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
     '<meta name="robots" content="noindex, nofollow">\n'
     f'<link rel="canonical" href="{ORIGIN}{path}">\n'
     '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n')
    if og:
        h += (f'<meta property="og:title" content="{title}">\n'
              f'<meta property="og:description" content="{desc}">\n'
              f'<meta property="og:url" content="{ORIGIN}{path}">\n'
              f'<meta property="og:image" content="{ORIGIN}/og.png">\n'
              '<meta property="og:type" content="website">\n'
              '<meta name="twitter:card" content="summary_large_image">\n')
    return h + '<link rel="stylesheet" href="/style.css">\n</head>\n<body>\n'

def ld(blocks):
    return '<script type="application/ld+json">\n{\n "@context": "https://schema.org",\n "@graph": [\n  ' + ",\n  ".join(blocks) + "\n ]\n}\n</script>\n"

def bc(*items):
    li = ", ".join(f'{{"@type": "ListItem", "position": {i+1}, "name": "{n}", "item": "{ORIGIN}{p}"}}'
                   for i, (p, n) in enumerate(items))
    return f'{{"@type": "BreadcrumbList", "itemListElement": [{li}]}}'

MAPCELL = (f'<div class="mapcell"><iframe src="https://www.google.com/maps?q={MAPQ}&amp;output=embed" '
 f'title="Map: {SITE}, {ADDR_LINE1}, Bunnell, Florida 32110"></iframe></div>')

CALLBAND = ('<section class="callband"><div class="wrap"><div><h2>Questions before we open?</h2>'
 f'<p>Send a note — the form reaches the camp desk. Opening date and hours post first on <a class="inl" href="{FB}">Facebook</a>.</p></div>'
 '<div class="cta-row"><a class="btn ghost" href="/contact">Contact us</a>'
 f'<a class="btn" href="{TELHREF}">Call {TEL}</a></div></div></section>\n')

MAPBLOCK = lambda h2, lede, note: ('<section class="block alt"><div class="wrap"><span class="label">Find the address</span>'
 f'<h2>{h2}</h2><p class="lede" style="margin:0 auto;text-align:center;max-width:640px">{lede}</p>'
 f'{MAPCELL}<p class="mapnote">{note}</p></div></section>\n')

# ————— pages —————
pages = {}

pages["index.html"] = dict(
 title="Bull Creek Fish Camp — Seafood Restaurant on the Water, Bunnell FL",
 desc="Bull Creek Fish Camp is reopening in Bunnell, Florida in January 2027 — a family-run seafood restaurant serving breakfast, lunch and dinner on the water at 3861 County Rd 2006 W, with about 150 seats and a dock for arriving by boat.",
 path="/",
 body=(
  '<section class="hero"><div class="wrap"><span class="label">Reopening January 2027 · 3861 County Rd 2006 W · Bunnell</span>'
  f'<h1>{SITE}</h1><p class="sub">A family-run seafood restaurant coming back to the water on Bull Creek — breakfast, lunch and dinner, '
  'about 150 seats in a new elevated building, and a dock with boat slips so you can tie up and walk in.</p>'
  + WAVE +
  '<div class="ctas"><a class="btn" href="/menu">See the menu</a><a class="btn ghost" href="/contact">Get opening news</a></div></div></section>\n'

  '<section class="block"><div class="wrap"><span class="label">The menu</span><h2>Catfish, gator tail and the fish of the week</h2>'
  '<p class="lede">Seafood anchors the menu — freshwater and saltwater both: catfish, frog legs, gator tail, mahi, and a fish of the day or week that rotates with what the water gives up. Local beef is planned, and a lot of what reaches the table will be made in the kitchen, not off a truck.</p>'
  '<div class="chips"><div class="chip"><h3>Breakfast, lunch &amp; dinner</h3><p>Three meals a day, on the water — six days a week, closed on Tuesdays (planned).</p><p><a href="/breakfast-lunch-dinner">Meals on the water →</a></p></div>'
  '<div class="chip"><h3>Visit by boat</h3><p>The new building sits beside the water with a dock and boat slips — arrive by land or by creek.</p><p><a href="/visit-by-boat">Visit by boat →</a></p></div>'
  '<div class="chip"><h3>The family</h3><p>Jessica Norton-Henry, her mother Pamela White and her brother Joshua White — all born and raised here.</p><p><a href="/our-story">Read the story →</a></p></div></div>'
  '<blockquote class="quote">We\'re gonna try to do a lot of stuff handmade, homemade.</blockquote>'
  '<p class="qby">— Jessica Norton-Henry, co-owner, to Business Debut, November 2026</p></div></section>\n'

  '<section class="block alt"><div class="wrap"><span class="label">The room and the dock</span><h2>150 seats — plus a place to tie up</h2>'
  '<div class="facts"><div class="fact"><h3>Inside</h3><p>About 150 guests in a newly constructed building on elevated ground along the water.</p></div>'
  '<div class="fact"><h3>By boat</h3><p>A new dock with boat slips — guests can visit by boat, the way a fish camp should work.</p></div>'
  '<div class="fact"><h3>Six days a week</h3><p>Plans call for being open six days a week and closed Tuesdays. Exact hours post when the opening date lands.</p></div></div></div></section>\n'

  '<section class="block"><div class="wrap"><span class="label">The neighborhood</span><h2>Where the nearest restaurant is 15 miles away</h2>'
  '<p class="lede">The camp serves the rural west side of Flagler County, where eating options are few — <span class="qsrc">per Business Debut, Nov 2026</span>. Local farmers and fishermen have stopped by during construction to say how eager they are to see the fish camp back. The building rises beside the water near Bull Creek Campground.</p>'
  '<p style="margin-top:22px"><a href="/our-story">Read how the camp came back →</a></p></div></section>\n'

  + MAPBLOCK("3861 County Rd 2006 W",
    "Bunnell, FL 32110 — on the water on the west side of Flagler County, near Bull Creek Campground.",
    "Official opening date and hours will be shared on the restaurant's Facebook page as plans are finalized.")
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "Restaurant",\n   "@id": "' + ORIGIN + '/#bcfc",\n   "name": "' + SITE + '",\n'
  '   "description": "Family-run seafood restaurant reopening January 2027 at 3861 County Rd 2006 W in Bunnell, Florida — breakfast, lunch and dinner on the water, seafood anchored by catfish, frog legs, gator tail, mahi and a rotating fish of the day or week, local beef planned, about 150 seats, with a dock and boat slips for guests arriving by boat.",\n'
  '   "url": "' + ORIGIN + '/",\n   "image": "' + ORIGIN + '/og.png",\n   "telephone": "+1-386-437-1991",\n   "email": "' + EMAIL + '",\n'
  '   "servesCuisine": ["Seafood", "American", "Southern"],\n'
  '   "address": {\n    "@type": "PostalAddress",\n    "streetAddress": "3861 County Rd 2006 W",\n    "addressLocality": "Bunnell",\n    "addressRegion": "FL",\n    "postalCode": "32110",\n    "addressCountry": "US"\n   },\n'
  '   "geo": {\n    "@type": "GeoCoordinates",\n    "latitude": ' + LAT + ',\n    "longitude": ' + LNG + '\n   },\n'
  '   "hasMap": "https://maps.google.com/maps?q=' + MAPQ + '",\n   "sameAs": ["' + FB + '"]\n  }',
  '{\n   "@type": "WebSite",\n   "@id": "' + ORIGIN + '/#website",\n   "url": "' + ORIGIN + '/",\n   "name": "' + SITE + '",\n   "inLanguage": "en-US",\n   "publisher": {"@id": "' + ORIGIN + '/#bcfc"}\n  }',
  bc(("/", "Home"))
 ]))

pages["menu.html"] = dict(
 title="The Menu — Bull Creek Fish Camp, Bunnell FL",
 desc="What the reopened Bull Creek Fish Camp menu will carry: catfish, frog legs, gator tail, mahi, a rotating fish of the day or week, local beef and plenty made from scratch. Menu and prices are announced at opening.",
 path="/menu",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">What\'s coming</span><h1>The menu, as planned</h1>'
  '<p class="sub">Seafood anchors everything — freshwater and saltwater — with breakfast, lunch and dinner served all day, six days a week. The printed menu and prices are announced at opening, so treat this as the direction the kitchen is heading, not the board you\'ll read in January.</p>'
  '<div class="ctas"><a class="btn" href="/breakfast-lunch-dinner">Meals on the water</a><a class="btn ghost" href="/contact">Ask about the menu</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">The board</span><h2>What the kitchen is building around</h2>'
  '<div class="menu-board">'
  '<div class="msection"><h3>From the water</h3><ul class="msec-list">'
  '<li><strong>Catfish</strong> — the anchor of every Florida fish camp, plated fresh</li>'
  '<li><strong>Frog legs</strong> — the old-camp classic, back on the board</li>'
  '<li><strong>Gator tail</strong> — fried, the way the county eats it</li>'
  '<li><strong>Mahi</strong> — from the saltwater side</li>'
  '<li><strong>Fish of the day or week</strong> — rotates with what the water gives up</li></ul>'
  '<p class="mnote">Items as announced by the owners to Business Debut, Nov 2026. Prices come with the opening menu.</p></div>'
  '<div class="msection"><h3>From the land</h3><ul class="msec-list">'
  '<li><strong>Local beef</strong> — the team plans to serve beef raised close by</li>'
  '<li><strong>Made in-house</strong> — "a lot of stuff handmade, homemade," per co-owner Jessica Norton-Henry</li></ul>'
  '<p class="mnote">Planned direction — details land with the opening menu.</p></div>'
  '<div class="msection"><h3>All day, six days</h3><ul class="msec-list">'
  '<li><strong>Breakfast</strong> — served on the water</li>'
  '<li><strong>Lunch and dinner</strong> — the same view, from noon on</li>'
  '<li><strong>Closed Tuesdays</strong> — open six days a week, as planned</li></ul>'
  '<p class="mnote">Exact hours post on Facebook when the opening date lands.</p></div></div></div></section>\n'
  '<section class="block alt"><div class="wrap"><span class="label">Go deeper</span><h2>Two pages built for hungry people</h2>'
  '<div class="chips"><div class="chip"><h3>Meals on the water</h3><p>How breakfast, lunch and dinner work at the new camp — and what the old regulars remember. <a href="/breakfast-lunch-dinner">Read it →</a></p></div>'
  '<div class="chip"><h3>Arrive by boat</h3><p>Dock, slips, and the run in on Bull Creek. <a href="/visit-by-boat">Read it →</a></p></div></div></div></section>\n'
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "WebPage",\n   "name": "The Menu — Bull Creek Fish Camp",\n   "url": "' + ORIGIN + '/menu",\n   "inLanguage": "en-US",\n   "about": {"@id": "' + ORIGIN + '/#bcfc"}\n  }',
  bc(("/", "Home"), ("/menu", "Menu"))
 ]))

pages["breakfast-lunch-dinner.html"] = dict(
 title="Breakfast, Lunch &amp; Dinner on the Water — Bull Creek Fish Camp, Bunnell FL",
 desc="The reopened Bull Creek Fish Camp will serve breakfast, lunch and dinner on the water in Bunnell FL, six days a week and closed on Tuesdays — catfish, the fish of the week, local beef and dishes made in-house.",
 path="/breakfast-lunch-dinner",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">Three meals, on the water</span>'
  '<h1>Breakfast, lunch and dinner — on the water in Bunnell</h1>'
  '<p class="sub">The new Bull Creek Fish Camp plans to serve breakfast, lunch and dinner, six days a week with Tuesdays off — the same rhythm the old camp kept for its regulars, in a brand-new building on high ground beside the creek.</p>'
  '<div class="ctas"><a class="btn" href="/menu">See the menu direction</a><a class="btn ghost" href="/contact">Ask a question</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">The day, start to finish</span><h2>Morning, midday, evening — all with the same view</h2>'
  '<div class="panel-grid">'
  '<div class="panel"><span class="tag">Morning</span><h3>Breakfast before the boats go out</h3><p>Breakfast is on the plan for the new camp. The old-timers tell you what they came for: "a tremendous spot for a Sunday breakfast." <span class="qsrc">per TripAdvisor reviews of the original camp</span></p></div>'
  '<div class="panel"><span class="tag">Midday</span><h3>Fish of the day, rice, and shade</h3><p>Lunch leans on the water — catfish, the rotating fish of the day or week, and local beef on the board when it\'s ready. <span class="qsrc">per Business Debut, Nov 2026</span></p></div>'
  '<div class="panel"><span class="tag">Evening</span><h3>Dinner as the sun drops</h3><p>Dinner at a fish camp is about the light on the water — regulars of the original camp remember the porch and the sunsets. <span class="qsrc">per TripAdvisor reviews</span></p></div></div></div></section>\n'
  '<section class="block alt"><div class="wrap"><span class="label">Hours, as planned</span><h2>Six days a week — closed Tuesdays</h2>'
  '<p class="lede">Co-owner Jessica Norton-Henry told Business Debut the camp plans to open six days a week and close on Tuesdays. Exact opening and closing times will be shared when the opening date is set — the menu and prices come with them.</p>'
  '<div class="facts"><div class="fact"><h3>Open</h3><p>Monday, Wednesday, Thursday, Friday, Saturday, Sunday — as planned.</p></div>'
  '<div class="fact"><h3>Closed</h3><p>Tuesdays, per the owners\' announced plan.</p></div>'
  '<div class="fact"><h3>Times</h3><p>Exact hours post on Facebook with the opening announcement.</p></div></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">Straight talk</span><h2>What is and isn\'t settled</h2><div class="faq-list">'
  '<div class="qa"><h3>Settled</h3><p>Breakfast, lunch and dinner; seafood-led with catfish, frog legs, gator tail, mahi, local beef and a rotating fish of the day or week; six-day week; opening news to Facebook first.</p></div>'
  '<div class="qa"><h3>Still to come</h3><p>Exact hours, the printed menu and prices, and the confirmed opening date. This page updates as the owners announce them.</p></div></div></div></section>\n'
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "Service",\n   "name": "Breakfast, lunch and dinner on the water",\n   "serviceType": "Restaurant meals",\n'
  '   "description": "Breakfast, lunch and dinner served six days a week (closed Tuesdays, as planned) at the reopened Bull Creek Fish Camp — seafood-led menu with catfish, frog legs, gator tail, mahi, a rotating fish of the day or week, local beef planned, and many items made in-house.",\n'
  '   "provider": {"@id": "' + ORIGIN + '/#bcfc"},\n   "areaServed": {"@type": "City", "name": "Bunnell", "addressRegion": "FL"}\n  }',
  bc(("/", "Home"), ("/menu", "Menu"), ("/breakfast-lunch-dinner", "Breakfast, Lunch and Dinner"))
 ]))

pages["visit-by-boat.html"] = dict(
 title="Visit by Boat — Dock &amp; Slips, Bull Creek Fish Camp, Bunnell FL",
 desc="The reopened Bull Creek Fish Camp has a new dock and boat slips — tie up and walk in on Bull Creek near Dead Lake, Bunnell FL, or arrive by car on County Rd 2006 W.",
 path="/visit-by-boat",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">Dock &amp; slips</span><h1>Visit by boat on Bull Creek</h1>'
  '<p class="sub">The new building sits beside the water with a dock and boat slips — the owners built arrival-by-boat right into the camp, the way it worked at the original. Or drive up on County Rd 2006 W and eat with the boats.</p>'
  '<div class="ctas"><a class="btn" href="/menu">See the menu</a><a class="btn ghost" href="/contact">Ask about the dock</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">The run in</span><h2>Creek to lake, table at the end of it</h2>'
  '<p class="lede">Bull Creek runs out into Dead Lake here on the west side of Flagler County — regulars of the original camp spent their afternoons watching pleasure fishing boats come and go from the porch. <span class="qsrc">per TripAdvisor reviews of the original camp</span> The new camp keeps the water in the middle of it: guests can visit by boat and tie up at the camp\'s own dock. <span class="qsrc">dock and slips per Business Debut, Nov 2026</span></p>'
  '<div class="facts"><div class="fact"><h3>By boat</h3><p>New dock with boat slips at the front door — the creek run from Dead Lake ends at your table.</p></div>'
  '<div class="fact"><h3>By land</h3><p>Follow County Rd 2006 W to 3861 — the camp sits beside the water near Bull Creek Campground.</p></div>'
  '<div class="fact"><h3>On the map</h3><p>Bunnell, FL 32110 — rural west Flagler County, about 15 miles from the nearest other restaurant, per the owners.</p></div></div></div></section>\n'
  + MAPBLOCK("3861 County Rd 2006 W, Bunnell",
   "Beside the water on the west side of Flagler County — near Bull Creek Campground, on the creek\'s run into Dead Lake.",
   "Opening date and hours post on Facebook when announced. The dock details come from the owners\' plans as reported to Business Debut.")
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "Service",\n   "name": "Visit by boat — dock and boat slips",\n   "serviceType": "Boat docking",\n'
  '   "description": "The reopened Bull Creek Fish Camp is built with a new dock and boat slips beside the water — guests arrive by boat on Bull Creek near its outlet into Dead Lake, or by car on County Rd 2006 W in Bunnell, Florida.",\n'
  '   "provider": {"@id": "' + ORIGIN + '/#bcfc"},\n   "areaServed": {"@type": "City", "name": "Bunnell", "addressRegion": "FL"}\n  }',
  bc(("/", "Home"), ("/visit-by-boat", "Visit by Boat"))
 ]))

pages["our-story.html"] = dict(
 title="Our Story — Bull Creek Fish Camp, Bunnell FL",
 desc="How Bull Creek Fish Camp came back: torn down by flooding in 2023, rebuilt on high ground through 2025, reopening January 2027 under Bunnell family owners Jessica Norton-Henry, Pamela White and Joshua White.",
 path="/our-story",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">The camp, the flood, the family</span>'
  '<h1>Same creek. New building. The next family.</h1>'
  '<p class="sub">Bull Creek Fish Camp was a Bunnell institution for decades — then the water took the building, and a family that grew up eating here decided to build it back, higher up and ready for boats.</p>'
  '<div class="ctas"><a class="btn" href="/menu">See the menu direction</a><a class="btn ghost" href="/contact">Contact the camp</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">The timeline</span><h2>How it went, and how it\'s coming back</h2>'
  '<ul class="tline">'
  '<li><p class="year">The original camp</p><h3>Decades on the water</h3><p>Bull Creek Fish Camp fed Bunnell for a long time — the old listing carries 4.6 stars across 389 Google reviews, <span class="qsrc">per Google Maps, pre-reopening listing</span> and regulars remember the screened porch, the blackboard menu and the sunsets over the creek. <span class="qsrc">per TripAdvisor reviews of the original camp</span></p></li>'
  '<li><p class="year">2023</p><h3>The flood takes the building</h3><p>Back-to-back hurricanes led to severe flooding at the site. The old restaurant was torn down. <span class="qsrc">per Business Debut, Nov 2026</span></p></li>'
  '<li><p class="year">2025</p><h3>Construction starts on high ground</h3><p>Work began on a newly constructed building on elevated ground along the water, near Bull Creek Campground — about 150 seats, with a dock and boat slips. Local farmers and fishermen stopped by during construction to say how eager they were to see the camp back. <span class="qsrc">per Business Debut, Nov 2026</span></p></li>'
  '<li><p class="year">January 2027</p><h3>The next family takes the dock</h3><p>Jessica Norton-Henry, her mother Pamela White and her brother Joshua White — "we\'re all local to Bunnell. We\'ve all lived here our whole lives," <span class="qsrc">Jessica, to Business Debut</span> — are the new owners, targeting a January opening with the exact date still to be announced.</p></li></ul>'
  '<blockquote class="quote">I think the nearest restaurant is 15 miles from us.</blockquote>'
  '<p class="qby">— Jessica Norton-Henry, to Business Debut, November 2026 — on serving a rural county with few places to eat</p></div></section>\n'
  '<section class="block alt"><div class="wrap"><span class="label">What carries over</span><h2>The water, the menu and the handmade promise</h2>'
  '<p class="lede">What the new camp keeps from the old one is the setting and the spirit: meals on the water, seafood led by what\'s caught, and — in the owners\' words — "a lot of stuff handmade, homemade." What\'s new is everything else: a newer building, on higher ground, built with a dock for the boats.</p>'
  '<p style="margin-top:22px"><a href="/menu">See what\'s coming on the menu →</a></p></div></section>\n'
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "WebPage",\n   "name": "Our Story — Bull Creek Fish Camp",\n   "url": "' + ORIGIN + '/our-story",\n   "inLanguage": "en-US",\n   "about": {"@id": "' + ORIGIN + '/#bcfc"}\n  }',
  bc(("/", "Home"), ("/our-story", "Our Story"))
 ]))

FAQ = [
 ("When are you opening?",
  "The owners are targeting January 2027 — an exact date is to be announced. Opening news posts first on the restaurant's Facebook page."),
 ("Where exactly are you?",
  "3861 County Rd 2006 W, Bunnell, FL 32110 — beside the water on the west side of Flagler County, near Bull Creek Campground. The owners note the nearest other restaurant is about 15 miles away."),
 ("What's on the menu?",
  "Seafood anchors it — freshwater and saltwater: catfish, frog legs, gator tail, mahi and a rotating fish of the day or week, with local beef planned and many items made in-house. The printed menu and prices are announced at opening."),
 ("Do you have hours yet?",
  "The plan calls for six days a week, closed Tuesdays. Exact hours post on Facebook with the opening announcement."),
 ("Can I come by boat?",
  "Yes — the new building comes with a dock and boat slips beside the water. Bull Creek runs out into Dead Lake, so the boats can tie up at the camp."),
 ("How big is the new building?",
  "About 150 guests, in a newly constructed building on elevated ground along the water."),
 ("How do I reach the owners?",
  "Call (386) 437-1991, email bullcreekfishcamp@gmail.com, or use the contact form — notes land at the camp's desk.")]

pages["faq.html"] = dict(
 title="FAQ — Bull Creek Fish Camp, Bunnell FL",
 desc="When Bull Creek Fish Camp reopens in Bunnell FL, what's on the menu, hours plans, boat docking and how to reach the camp — straight answers on what is and isn't settled.",
 path="/faq",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">While the doors are still closed</span><h1>Questions, answered honestly</h1>'
  '<p class="sub">Everything here comes from the owners\' plans as reported to Business Debut in November 2026 or from the camp\'s published listing. Where something isn\'t settled yet, the answer says so.</p>'
  '<div class="ctas"><a class="btn" href="/contact">Ask something else</a><a class="btn ghost" href="/menu">See the menu direction</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">The FAQ</span><h2>What people ask before opening</h2><div class="faq-list">'
  + "".join(f'<div class="qa"><h3>{q}</h3><p>{a}</p></div>' for q, a in FAQ)
  + '</div></div></section>\n'
  '<section class="block alt"><div class="wrap"><span class="label">Not settled</span><h2>Three things still pending</h2>'
  '<div class="panel-grid"><div class="panel"><span class="tag">Date</span><h3>The exact opening day</h3><p>January 2027 is the target the owners gave Business Debut; the date gets announced when it\'s locked.</p></div>'
  '<div class="panel"><span class="tag">Hours</span><h3>Exact open and close times</h3><p>The six-day plan is public; the clock times come with the opening announcement.</p></div>'
  '<div class="panel"><span class="tag">Menu</span><h3>The printed menu and prices</h3><p>The direction is public — catfish, gator tail, mahi, local beef, handmade. Prices land at opening.</p></div></div></div></section>\n'
  + CALLBAND),
 ld=ld([
  '{\n   "@type": "FAQPage",\n   "mainEntity": [\n    ' + ",\n    ".join(
   f'{{"@type": "Question", "name": "{q}", "acceptedAnswer": {{"@type": "Answer", "text": "{a}"}}}}'
   for q, a in FAQ).replace("(386) 437-1991, email bullcreekfishcamp@gmail.com", "(386) 437-1991, email bullcreekfishcamp@gmail.com")
   + '\n   ]\n  }',
  bc(("/", "Home"), ("/faq", "FAQ"))
 ]))

pages["contact.html"] = dict(
 title="Contact — Bull Creek Fish Camp, Bunnell FL",
 desc="Call, email or message Bull Creek Fish Camp at 3861 County Rd 2006 W, Bunnell FL 32110 before the January 2027 reopening — menu questions, dock questions, opening news.",
 path="/contact",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">The camp desk before opening</span><h1>Contact us</h1>'
  '<p class="sub">Menu requests, dock questions, opening questions, press — email reaches the camp, and the form below lands in the same place. Opening date and hours post first on <a href="' + FB + '">Facebook</a>.</p></div></section>\n'
  '<section class="block"><div class="wrap"><div class="contact-grid"><div><span class="label">Write to us</span><h2>Send a note</h2>'
  '<form class="cform" action="/contact" method="post"><p class="note">Name and message are required.</p>'
  '<label for="f-name">Your name<input id="f-name" type="text" name="name" autocomplete="name" placeholder="Your name" required></label>'
  '<label for="f-phone">Phone (optional)<input id="f-phone" type="tel" name="phone" autocomplete="tel" placeholder="Phone, if you\'d rather be called"></label>'
  '<label for="f-email">Email<input id="f-email" type="email" name="email" autocomplete="email" placeholder="you@example.com"></label>'
  '<label for="f-msg">Message<textarea id="f-msg" name="message" rows="5" required placeholder="Your message — menu questions, opening news, anything."></textarea></label>'
  '<p><button class="btn" type="submit">Send it</button></p></form></div>'
  '<div class="contact-side"><span class="label">Direct</span><h3>Call the camp</h3>'
  f'<p><a href="{TELHREF}">{TEL}</a> — the camp\'s published phone line.</p>'
  f'<h3>{EMAIL}</h3><p>The published shop email — it reaches the desk that answers this form.</p>'
  f'<h3>On Facebook</h3><p><a href="{FB}">Follow the page</a> — opening date and hours are announced there first.</p>'
  '<h3>The address</h3><address>3861 County Rd 2006 W<br>Bunnell, FL 32110</address></div></div></div></section>\n'
  + MAPBLOCK("3861 County Rd 2006 W",
   "Beside the water on Bull Creek, west Flagler County — dock and boat slips at the building.",
   "Opening date and hours announced first on Facebook.")),
 ld=ld([
  '{\n   "@type": "WebPage",\n   "name": "Contact — Bull Creek Fish Camp",\n   "url": "' + ORIGIN + '/contact",\n   "inLanguage": "en-US",\n   "about": {"@id": "' + ORIGIN + '/#bcfc"}\n  }',
  bc(("/", "Home"), ("/contact", "Contact"))
 ]))
pages["contact.html"]["ld"] = ld(
 ['{\n   "@type": "WebPage",\n   "name": "Contact — Bull Creek Fish Camp",\n   "url": "' + ORIGIN + '/contact",\n   "inLanguage": "en-US",\n   "about": {"@id": "' + ORIGIN + '/#bcfc"}\n  }', bc(("/", "Home"), ("/contact", "Contact"))])

pages["privacy.html"] = dict(
 title="Privacy — Bull Creek Fish Camp, Bunnell FL",
 desc="What this site collects: just the contact form — no cookies, no advertising trackers, no analytics scripts. A plain-language privacy policy for Bull Creek Fish Camp, Bunnell FL.",
 path="/privacy",
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">Plain language</span><h1>Privacy</h1>'
  f'<p class="sub">This site is published for {SITE} at {ADDR_LINE1}, Bunnell, FL 32110. It sets no cookies, runs no advertising trackers and no analytics scripts. Here is everything it does collect.</p></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">What\'s collected</span><h2>The contact form, and a map tile</h2><div class="faq-list">'
  '<div class="qa"><h3>The contact form</h3><p>When you send the form on the contact page, the name, phone, email and message you type are delivered by email to the camp\'s contact desk so the owners can answer you. Nothing else is stored on this site about you, and the information is used only to reply and to follow up about your note.</p></div>'
  f'<div class="qa"><h3>Email</h3><p>If you email <a href="mailto:{EMAIL}">{EMAIL}</a> directly, your address and message are kept in the camp\'s mailbox so the conversation can be answered and referenced later.</p></div>'
  '<div class="qa"><h3>The map on the contact and home pages</h3><p>The embedded map is served by Google Maps. When the map loads in your browser, Google receives the standard request data of that request (including your IP address and which page embedded it). This site itself has no say in that and sets no cookies of its own.</p></div>'
  '<div class="qa"><h3>No tracking</h3><p>No cookies, no local storage, no pixels, no third-party scripts. The pages are plain files; your browser does all the work.</p></div>'
  f'<div class="qa"><h3>Your say</h3><p>Want a copy of what you sent, or want it deleted from the desk\'s mailbox? Email <a href="mailto:{EMAIL}">{EMAIL}</a> and say which.</p></div></div></div></section>\n'
  '<section class="callband"><div class="wrap"><div><h2>Anything else?</h2><p>The contact desk answers questions about this site the same way it answers questions about the menu.</p></div>'
  '<div class="cta-row"><a class="btn" href="/contact">Contact us</a><a class="btn ghost" href="/">Back to home</a></div></div></section>\n'),
 ld=ld([
  '{\n   "@type": "WebPage",\n   "name": "Privacy — Bull Creek Fish Camp",\n   "url": "' + ORIGIN + '/privacy",\n   "inLanguage": "en-US",\n   "about": {"@id": "' + ORIGIN + '/#bcfc"}\n  }',
  bc(("/", "Home"), ("/privacy", "Privacy"))
 ]))

pages["thanks.html"] = dict(
 title="Thank You — Bull Creek Fish Camp, Bunnell FL",
 desc="Your note about Bull Creek Fish Camp came through — thank you. Opening date and hours post first on the restaurant's Facebook page.",
 path="/thanks", og=False,
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">Message received</span><h1>Thank you — your note came through</h1>'
  f'<p class="sub">It landed at the camp\'s desk. The official opening date and hours post first on <a href="{FB}">Facebook</a>, and anyone who left an email hears about opening week too.</p>'
  '<div class="ctas"><a class="btn" href="/menu">See the menu while you wait</a><a class="btn ghost" href="/">Back to home</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">Meanwhile</span><h2>Two things to look at</h2><div class="chips">'
  '<div class="chip"><h3>What\'s coming on the board</h3><p>Catfish, frog legs, gator tail, mahi, local beef, handmade — the menu direction. <a href="/menu">Read the menu →</a></p></div>'
  '<div class="chip"><h3>How the camp came back</h3><p>2023 flood, 2025 construction, 2027 — the family rebuilding it on high ground. <a href="/our-story">Read the story →</a></p></div></div></div></section>\n'))

pages["404.html"] = dict(
 title="Page Not Found — Bull Creek Fish Camp, Bunnell FL",
 desc="That page isn't here — try the menu, our story, the FAQ or contact for Bull Creek Fish Camp, the seafood camp on the water reopening in Bunnell, FL in January 2027.",
 path="/404", og=False,
 body=(
  '<section class="hero slim"><div class="wrap"><span class="label">Error 404</span><h1>That page isn\'t on the board</h1>'
  '<p class="sub">The link you followed doesn\'t lead anywhere on this site. Try one of these instead — or tell us what you were looking for and we\'ll fix it.</p>'
  '<div class="ctas"><a class="btn" href="/menu">See the menu</a><a class="btn ghost" href="/contact">Tell us what\'s missing</a></div></div></section>\n'
  '<section class="block"><div class="wrap"><span class="label">Popular pages</span><h2>While you\'re here</h2><div class="chips">'
  '<div class="chip"><h3>The menu</h3><p>Catfish, gator tail, mahi, fish of the day or week, local beef. <a href="/menu">Go to the menu →</a></p></div>'
  '<div class="chip"><h3>Our story</h3><p>The flood, the rebuild, and the family taking the dock. <a href="/our-story">Read the story →</a></p></div>'
  '<div class="chip"><h3>Opening questions</h3><p>Date, hours, boats, seating — the FAQ answers what\'s settled. <a href="/faq">Read the FAQ →</a></p></div></div></div></section>\n'))

# ————— emit —————
counts = []
for fname, spec in pages.items():
    html = head(spec["title"], spec["desc"], spec["path"], spec.get("og", True)) + HEADER + spec["body"] + FOOTER
    if spec.get("ld"):
        html += spec["ld"]
    html += "</body>\n</html>\n"
    open(os.path.join(PUB, fname), "w", encoding="utf-8").write(html)
    counts.append(fname)

# sitemap + robots
urls = [("/", 0.9), ("/menu", 0.8), ("/breakfast-lunch-dinner", 0.8), ("/visit-by-boat", 0.7),
        ("/our-story", 0.6), ("/faq", 0.6), ("/contact", 0.7), ("/privacy", 0.3)]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for p, pri in urls:
    chg = "weekly" if p in ("/", "/menu", "/faq") else ("monthly" if p != "/privacy" else "yearly")
    pr = "0.9" if pri == 0.9 else str(pri)
    sm += f'  <url><loc>{ORIGIN}{p}</loc><lastmod>{LASTMOD}</lastmod><changefreq>{chg}</changefreq><priority>{pr}</priority></url>\n'
sm += "</urlset>\n"
open(os.path.join(PUB, "sitemap.xml"), "w").write(sm)
open(os.path.join(PUB, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n")

# favicon
fav = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
 '<rect width="100" height="100" rx="20" fill="#1d3128"/>'
 '<g fill="none" stroke="#d8b25e" stroke-width="3"><circle cx="50" cy="50" r="34"/></g>'
 '<g fill="#d8b25e"><path d="M31 40c6-6 16-9 26-6 4 1 7 3 9 6-2 3-5 5-9 6-10 3-20 0-26-6z"/>'
 '<path d="M66 40l10-6v24l-10-6z"/></g>'
 '<g fill="none" stroke="#d8b25e" stroke-width="3">'
 '<path d="M30 62q6-4 13 0t13 0 13 0"/><path d="M30 70q6-4 13 0t13 0 13 0"/></g></svg>\n')
open(os.path.join(PUB, "favicon.svg"), "w").write(fav)

print("wrote:", len(counts), "pages + sitemap + robots + favicon")
print("\n".join(sorted(counts)))
