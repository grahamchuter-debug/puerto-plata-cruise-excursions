#!/usr/bin/env python3
"""Generate Puerto Plata Cruise Excursion static site pages."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "puertoplatacruiseexcursion.com"
SITE = "Puerto Plata Cruise Excursion"
BASE_URL = f"https://{DOMAIN}"

HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(37, 99, 235, 0.72) 0%, "
    "rgba(245, 158, 11, 0.58) 50%, rgba(30, 58, 138, 0.52) 100%)"
)

TOUR_CHECKLIST = [
    "Cruise-friendly timing",
    "Pickup guidance for Amber Cove and Taino Bay",
    "Clear return-to-ship advice",
    "Local destination knowledge",
    "Good options for families, couples and groups",
]

HEAD_COMMON = """  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />"""

RETURN_BADGE = (
    '<span class="return-to-ship-badge" role="status">'
    '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M3 17h18M5 17l2-8h10l2 8M9 9l1-4h4l1 4"/></svg>'
    "Return To Ship On Time</span>"
)


def snapshot(items: dict[str, str]) -> str:
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in items.items()
    )
    return f'''<aside class="cruise-snapshot mb-10 px-4 sm:px-0" aria-label="Cruise passenger snapshot">
  <h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>
  <dl class="cruise-snapshot__grid">{rows}</dl>
</aside>'''


def related_links(links: list[tuple[str, str]]) -> str:
    parts = []
    for i, (href, label) in enumerate(links):
        if i:
            parts.append('<span class="text-gray-300">·</span>')
        parts.append(
            f'<a href="{href}" class="text-ocean-600 hover:text-ocean-800 font-medium">{label}</a>'
        )
    return f'''<nav class="mt-10 pt-8 border-t border-dr-100" aria-label="Related Puerto Plata guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Puerto Plata port day</p>
  <div class="flex flex-wrap gap-3 text-sm">{"".join(parts)}</div>
</nav>'''


def cta_section() -> str:
    return '''<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Puerto Plata Port Day</h2>
  <p class="text-white/85 text-sm mb-6">Compare excursion styles, understand Amber Cove and Taino Bay logistics, and choose the best fit for your cruise schedule.</p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center flex-wrap">
    <a href="best-puerto-plata-shore-excursions.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">View Puerto Plata Excursions</a>
    <a href="puerto-plata-cruise-port-guide.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Plan Your Port Day</a>
    <a href="amber-cove-vs-taino-bay.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Amber Cove vs Taino Bay</a>
  </div>
</div></section>'''


def hero(
    path: str,
    *,
    breadcrumb: str | None = None,
    eyebrow: str,
    title_html: str,
    lead: str,
    image: str,
    aria: str,
    actions: str = "",
    tags: str = "",
) -> str:
    _ = path
    bc = ""
    if breadcrumb:
        bc = f'''<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">
        <a href="index.html" class="hover:text-white transition-colors">Home</a>
        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-white/80">{breadcrumb}</span>
      </nav>'''
    tag_block = (
        f'<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">{tags}</div>'
        if tags
        else ""
    )
    act_block = (
        f'<div class="site-hero__actions flex flex-col sm:flex-row gap-3">{actions}</div>'
        if actions
        else '<div class="site-hero__actions flex flex-col sm:flex-row gap-3"></div>'
    )
    return f'''<section class="site-hero">
  <div class="absolute inset-0 hero-bg-custom" style="background-image: {HERO_GRADIENT}, url('images/{image}');" role="img" aria-label="{aria}"></div>
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl">{bc}
      <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
        <span class="w-2 h-2 rounded-full bg-dr-300 animate-pulse"></span>
        <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">{eyebrow}</span>
      </div>
      <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">{title_html}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/90 font-light leading-relaxed mb-5 max-w-2xl">{lead}</p>
      {act_block}
      {tag_block}
    </div>
  </div>
  <div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>
</section>'''


def shell(
    filename: str,
    *,
    title: str,
    description: str,
    keywords: str,
    canonical: str,
    preload: str,
    page: str,
    hero_file: str,
    content_file: str,
    ld_json: dict | list,
) -> None:
    ld = json.dumps(ld_json, indent=2)
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical}" />
  <link rel="preload" as="image" href="images/{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:image" content="{BASE_URL}/images/{preload}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">
{ld}
  </script>
{HEAD_COMMON}
</head>
<body class="bg-white text-gray-800 antialiased" data-page="{page}" data-base="" data-hero="{hero_file}" data-content="{content_file}" data-trust-strip="partials/trust-strip.html">
  <div id="site-nav"></div>
  <div id="page-hero"></div>
  <div id="page-trust-strip"></div>
  <main id="page-content"></main>
  <div id="site-footer"></div>
  <script src="js/site.js"></script>
</body>
</html>'''
    (ROOT / filename).write_text(html)


def tour_content(
    name: str,
    badge: str,
    badge_class: str,
    intro: str,
    image: str,
    alt: str,
    highlights: list[tuple[str, str, str, str]],
    snap: dict[str, str],
    links: list[tuple[str, str]],
) -> str:
    if "|" in badge and "|" in badge_class:
        badge_labels = [b.strip() for b in badge.split("|")]
        badge_classes = [c.strip() for c in badge_class.split("|")]
        badge_markup = " ".join(
            f'<span class="{bc}" role="status">{bl}</span>'
            for bl, bc in zip(badge_labels, badge_classes)
        )
    else:
        badge_markup = f'<span class="{badge_class}" role="status">{badge}</span>'
    checks = "".join(
        f'<li class="flex gap-2 text-sm text-gray-600"><span class="text-ocean-500">✓</span>{c}</li>'
        for c in TOUR_CHECKLIST
    )
    cards = ""
    for h_img, h_alt, h_title, h_desc in highlights:
        cards += f'''<div class="bg-white rounded-3xl overflow-hidden shadow-md border border-dr-100 flex flex-col">
      <div class="card-media h-40"><img src="images/{h_img}" alt="{h_alt}" width="400" height="240" loading="lazy" decoding="async" /></div>
      <div class="p-5"><h3 class="font-display font-semibold text-gray-900 mb-2">{h_title}</h3><p class="text-sm text-gray-600 leading-relaxed">{h_desc}</p></div>
    </div>'''
    return f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <div class="mb-3 flex flex-wrap gap-2">{badge_markup} {RETURN_BADGE}</div>
    <h2 class="text-2xl font-display font-bold text-gray-900 mb-4">Why cruise passengers choose this excursion</h2>
    <p class="text-gray-600 leading-relaxed mb-6">{intro}</p>
    <ul class="space-y-3 mb-6">{checks}</ul>
    <p class="text-xs text-gray-500">Cruise schedules, pickup details and return windows can vary by ship and supplier. Confirm exact inclusions before booking.</p>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="images/{image}" alt="{alt}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-14 bg-dr-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10"><h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mb-3">{name} Highlights</h2>
  <p class="text-gray-600 text-sm max-w-2xl mx-auto">Key experiences cruise visitors can expect on this Puerto Plata excursion.</p></div>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">{cards}</div>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot(snap)}</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(links)}</div></section>
{cta_section()}'''


def faq_section(title: str, items: list[tuple[str, str]]) -> str:
    blocks = ""
    for q, a in items:
        blocks += f'''<details class="faq-item rounded-2xl border border-dr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary>
      <p class="mt-4 text-sm text-gray-500">{a}</p></details>'''
    return f'''<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-8">{title}</h2>
  <div class="space-y-4">{blocks}</div>
</div></section>'''


def faq_schema(items: list[tuple[str, str]]) -> list[dict]:
    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in items
    ]


# --- Directories ---
(ROOT / "partials").mkdir(exist_ok=True)
(ROOT / "content").mkdir(exist_ok=True)


# --- Partials ---
(ROOT / "partials/nav.html").write_text('''<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-dr-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="index.html" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M3 13h18v2H3zm2-5h14v2H5zm3 10h8v2H8z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Puerto Plata<br/><span class="text-[10px] font-body font-normal text-dr-600 tracking-widest uppercase">Cruise Excursion</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="best-puerto-plata-shore-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" data-nav="damajagua" class="text-gray-600 hover:text-ocean-600 transition-colors">Damajagua</a>
        <a href="monkeyland-shore-excursion-puerto-plata.html" data-nav="monkeyland" class="text-gray-600 hover:text-ocean-600 transition-colors">Monkeyland</a>
        <a href="puerto-plata-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
        <a href="amber-cove-vs-taino-bay.html" data-nav="ports" class="text-gray-600 hover:text-ocean-600 transition-colors">Amber Cove vs Taino Bay</a>
      </div>
      <a href="best-puerto-plata-shore-excursions.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        View Puerto Plata Excursions
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-dr-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>''')

(ROOT / "partials/footer.html").write_text('''<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="index.html" class="font-display font-semibold text-white text-lg">Puerto Plata Cruise Excursion</a>
        <p class="mt-3 text-sm leading-relaxed">Independent destination guide for cruise visitors planning a Puerto Plata shore day.</p>
        <p class="mt-2 text-sm"><a href="https://puertoplatacruiseexcursion.com" class="hover:text-white transition-colors">puertoplatacruiseexcursion.com</a></p>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="hover:text-white transition-colors">Damajagua</a></li>
          <li><a href="monkeyland-shore-excursion-puerto-plata.html" class="hover:text-white transition-colors">Monkeyland</a></li>
          <li><a href="puerto-plata-city-tour.html" class="hover:text-white transition-colors">City Tour</a></li>
          <li><a href="puerto-plata-beach-break.html" class="hover:text-white transition-colors">Beach Break</a></li>
          <li><a href="catamaran-snorkel-puerto-plata.html" class="hover:text-white transition-colors">Catamaran &amp; Snorkel</a></li>
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Guides</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="best-puerto-plata-shore-excursions.html" class="hover:text-white transition-colors">Best Excursions</a></li>
          <li><a href="puerto-plata-cruise-port-guide.html" class="hover:text-white transition-colors">Port Guide</a></li>
          <li><a href="one-day-in-puerto-plata-from-a-cruise-ship.html" class="hover:text-white transition-colors">One Day</a></li>
          <li><a href="is-puerto-plata-worth-visiting.html" class="hover:text-white transition-colors">Worth Visiting?</a></li>
          <li><a href="amber-cove-vs-taino-bay.html" class="hover:text-white transition-colors">Amber Cove vs Taino Bay</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 Puerto Plata Cruise Excursion · puertoplatacruiseexcursion.com. Confirm availability, pickup point and return windows before booking.</p>
    </div>
  </div>
</footer>''')

(ROOT / "partials/trust-strip.html").write_text('''<section class="trust-strip" aria-label="Puerto Plata cruise excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Amber Cove + Taino Bay Logistics</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Waterfalls &amp; Adventure Tours</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> City, Beach &amp; Catamaran Options</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Cruise-Friendly Return Planning</li>
    </ul>
  </div>
</section>''')

print("Partials written")

LINKS_DEFAULT = [
    ("best-puerto-plata-shore-excursions.html", "Best Excursions"),
    ("puerto-plata-cruise-port-guide.html", "Port Guide"),
    ("amber-cove-vs-taino-bay.html", "Amber Cove vs Taino Bay"),
    ("one-day-in-puerto-plata-from-a-cruise-ship.html", "One Day Itinerary"),
    ("damajagua-waterfalls-shore-excursion-puerto-plata.html", "Damajagua"),
    ("monkeyland-shore-excursion-puerto-plata.html", "Monkeyland"),
    ("puerto-plata-city-tour.html", "City Tour"),
    ("puerto-plata-beach-break.html", "Beach Break"),
    ("catamaran-snorkel-puerto-plata.html", "Catamaran & Snorkel"),
    ("is-puerto-plata-worth-visiting.html", "Worth Visiting?"),
]

HOME_FAQ = [
    ("Where do cruise ships dock in Puerto Plata?", "Puerto Plata cruise guests usually dock at either Amber Cove or Taino Bay. Both are in the Puerto Plata area but have different layouts and transfer logistics."),
    ("What is the best shore excursion in Puerto Plata?", "Damajagua waterfalls is the headline adventure choice, while Monkeyland, city tours, beach breaks, and catamaran trips are popular depending on activity level."),
    ("Is Puerto Plata good for families on a cruise stop?", "Yes. Monkeyland, city tours and beach breaks are common family picks, while Damajagua suits active families with older children."),
    ("How much time should I leave before all aboard?", "Aim to return 60 to 90 minutes before all aboard on independent tours, especially if your pickup and drop-off point differs between Amber Cove and Taino Bay."),
    ("Can I visit Puerto Plata city from both ports?", "Yes. Puerto Plata city is reachable from both Amber Cove and Taino Bay, but transfer times differ by traffic and pickup location."),
]


# --- Heroes ---
(ROOT / "partials/hero-home.html").write_text(
    hero(
        "partials/hero-home.html",
        eyebrow="Puerto Plata · Dominican Republic",
        image="hero-puerto-plata.png",
        aria="Puerto Plata coastline, tropical hills and cruise excursion highlights in the Dominican Republic",
        title_html='Puerto Plata Cruise<br/><span class="text-dr-200">Excursions</span><br/>for Amber Cove &amp; Taino Bay',
        lead="Your Puerto Plata destination guide for cruise-day planning, with excursions timed for both Amber Cove and Taino Bay arrivals.",
        actions='''<a href="best-puerto-plata-shore-excursions.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">View Puerto Plata Excursions</a>
          <a href="puerto-plata-cruise-port-guide.html" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Plan Your Port Day</a>''',
        tags='''<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Amber Cove</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Taino Bay</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Damajagua</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Monkeyland</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Cruise Timing Tips</span>''',
    )
)

HERO_PAGES = [
    (
        "hero-best-excursions.html",
        "Best Excursions",
        "Puerto Plata Guide",
        "best-puerto-plata-excursions.png",
        "Top Puerto Plata shore excursion options for cruise visitors docking at Amber Cove and Taino Bay",
        'Best Puerto Plata<br/><span class="text-dr-200">Shore Excursions</span>',
        "Compare adventure, wildlife, city, beach and sailing options for a smooth Puerto Plata cruise day.",
    ),
    (
        "hero-port-guide.html",
        "Port Guide",
        "Cruise Logistics",
        "puerto-plata-port.png",
        "Puerto Plata cruise port planning showing pickup and transfer details from Amber Cove and Taino Bay",
        'Puerto Plata Cruise<br/><span class="text-dr-200">Port Guide</span>',
        "Understand Amber Cove vs Taino Bay pickups, travel times, and return-to-ship planning.",
    ),
    (
        "hero-amber-vs-taino.html",
        "Amber Cove vs Taino Bay",
        "Port Comparison",
        "amber-cove-taino-bay.png",
        "Amber Cove and Taino Bay port comparison for cruise passengers planning Puerto Plata excursions",
        'Amber Cove vs Taino Bay<br/><span class="text-dr-200">Puerto Plata Guide</span>',
        "Clear comparison of both Puerto Plata cruise ports so you can choose the right excursion logistics.",
    ),
    (
        "hero-one-day.html",
        "One Day Itinerary",
        "Cruise Port Day",
        "one-day-puerto-plata.png",
        "One day in Puerto Plata itinerary ideas from cruise ships docking at Amber Cove or Taino Bay",
        'One Day in Puerto Plata<br/><span class="text-dr-200">from a Cruise Ship</span>',
        "Sample Puerto Plata itineraries for active and relaxed cruise travelers.",
    ),
    (
        "hero-damajagua.html",
        "Damajagua",
        "Waterfalls Adventure",
        "damajagua-waterfalls.png",
        "Damajagua waterfalls excursion from Puerto Plata cruise ports with natural pools and canyon adventure",
        'Damajagua Waterfalls<br/><span class="text-dr-200">Shore Excursion</span>',
        "A signature Puerto Plata adventure with waterfall jumps, slides, and tropical natural pools.",
    ),
    (
        "hero-monkeyland.html",
        "Monkeyland",
        "Family Wildlife",
        "monkeyland.png",
        "Monkeyland shore excursion in Puerto Plata with friendly squirrel monkeys and family-friendly experiences",
        'Monkeyland Shore<br/><span class="text-dr-200">Excursion</span>',
        "Interactive wildlife encounters ideal for families, couples and mixed-age groups.",
    ),
    (
        "hero-city-tour.html",
        "City Tour",
        "Historic Puerto Plata",
        "puerto-plata-city.png",
        "Puerto Plata city tour highlights including Umbrella Street Pink Street Fort San Felipe and cable car views",
        'Puerto Plata<br/><span class="text-dr-200">City Tour</span>',
        "Explore the historic center, colorful streets, and iconic landmarks with cruise-friendly pacing.",
    ),
    (
        "hero-beach-break.html",
        "Beach Break",
        "Relaxed Port Day",
        "puerto-plata-beach.png",
        "Puerto Plata beach break excursion for cruise visitors seeking a relaxed low-walking tropical day",
        'Puerto Plata Beach Break<br/><span class="text-dr-200">Shore Excursion</span>',
        "A low-stress beach day with easy pacing for couples, families and groups.",
    ),
    (
        "hero-catamaran.html",
        "Catamaran & Snorkel",
        "Sailing Day",
        "catamaran-snorkel.png",
        "Catamaran and snorkel excursion in Puerto Plata for cruise travelers seeking sailing music and reef time",
        'Catamaran &amp; Snorkel<br/><span class="text-dr-200">Puerto Plata</span>',
        "A social sailing option with snorkeling, music and coastal views.",
    ),
    (
        "hero-worth-visiting.html",
        "Worth Visiting?",
        "Cruise Decision Guide",
        "puerto-plata-intro.png",
        "Puerto Plata cruise destination overview to help decide whether the port is worth visiting",
        'Is Puerto Plata<br/><span class="text-dr-200">Worth Visiting?</span>',
        "Answers to the top Puerto Plata questions cruise passengers ask before arrival.",
    ),
]

for hf, crumb, eyebrow, img, aria, title, lead in HERO_PAGES:
    (ROOT / f"partials/{hf}").write_text(
        hero(
            f"partials/{hf}",
            breadcrumb=crumb,
            eyebrow=eyebrow,
            image=img,
            aria=aria,
            title_html=title,
            lead=lead,
        )
    )

print("Heroes written")


# --- Home content ---
(ROOT / "content/home.html").write_text(
    '''<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10">
    <div class="section-label mx-auto">Puerto Plata Highlights</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">Best Puerto Plata Cruise Excursions</h2>
    <p class="text-gray-600 text-sm max-w-2xl mx-auto">From waterfalls and monkey encounters to city tours, beach breaks and catamaran sailing, these are the most-booked Puerto Plata options for cruise passengers.</p>
  </div>
  <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-dr-100 flex flex-col">
      <div class="card-media h-44"><img src="images/damajagua-waterfalls.png" alt="Damajagua waterfalls adventure in Puerto Plata with tropical pools and canyon route" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Damajagua</h3><p class="text-sm text-gray-500 flex-1">Most popular Puerto Plata adventure with natural pools and waterfall action.</p>
      <a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Waterfalls Guide</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-dr-100 flex flex-col">
      <div class="card-media h-44"><img src="images/monkeyland.png" alt="Monkeyland Puerto Plata excursion with squirrel monkey interaction for families" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Monkeyland</h3><p class="text-sm text-gray-500 flex-1">Family-friendly wildlife interaction with playful squirrel monkeys.</p>
      <a href="monkeyland-shore-excursion-puerto-plata.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Monkeyland Guide</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-dr-100 flex flex-col">
      <div class="card-media h-44"><img src="images/puerto-plata-city.png" alt="Puerto Plata city tour landmarks including Umbrella Street Pink Street and Fort San Felipe" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">City Tour</h3><p class="text-sm text-gray-500 flex-1">Historic center and top landmarks for first-time Puerto Plata visitors.</p>
      <a href="puerto-plata-city-tour.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">City Tour Guide</a></div>
    </div>
    <div class="card-hover bg-white rounded-3xl overflow-hidden shadow-md border border-dr-100 flex flex-col">
      <div class="card-media h-44"><img src="images/catamaran-snorkel.png" alt="Catamaran and snorkel cruise excursion in Puerto Plata with music and group atmosphere" width="600" height="352" loading="lazy" decoding="async" /></div>
      <div class="p-6 flex flex-col flex-1"><h3 class="text-lg font-display font-semibold text-gray-900 mb-2">Catamaran</h3><p class="text-sm text-gray-500 flex-1">Sailing, snorkeling and social energy for couples and groups.</p>
      <a href="catamaran-snorkel-puerto-plata.html" class="mt-5 btn-ocean inline-flex items-center justify-center text-white text-xs font-semibold px-5 py-2.5 rounded-full">Sailing Guide</a></div>
    </div>
  </div>
  <p class="text-center mt-8"><a href="best-puerto-plata-shore-excursions.html" class="text-ocean-600 font-semibold text-sm">See full excursion comparison →</a></p>
</div></section>
<section class="pt-4 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Puerto Plata Destination Guide</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Puerto Plata Is a Destination,<br/><span class="text-ocean-600">Not Just One Cruise Pier</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Cruise ships visiting Puerto Plata may dock at <strong>Amber Cove</strong> or <strong>Taino Bay</strong>. Both serve the same destination, but pickup points and transfer logistics differ. Puerto Plata offers flexible shore days, from high-energy waterfall routes to relaxed beach and city experiences.</p>
    <a href="amber-cove-vs-taino-bay.html" class="btn-ocean inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Compare the Two Ports</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
    <img src="images/puerto-plata-intro.png" alt="Puerto Plata cruise destination overview with tropical coastline city and excursion options" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>'''
    + f'''
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Typical Time In Port": "7-10 hours (varies by itinerary)",
    "Cruise Port Access": "Amber Cove or Taino Bay",
    "Best For": "Adventure, culture, beach and mixed groups",
    "Activity Level": "Easy to active options available",
    "Family Friendly": "Strong across Monkeyland, beach and city tours",
    "Return To Ship Planning": "Keep 60-90 min buffer on independent tours",
})}</div></section>'''
    + '''
<section class="py-16 bg-dr-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-10">Top Things To Do in Puerto Plata</h2>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Damajagua Waterfalls</h3><p class="text-gray-600">Natural pools, slides and jumps for active travelers who want a true adventure.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Monkeyland</h3><p class="text-gray-600">Friendly squirrel monkeys and interactive wildlife moments ideal for families.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Puerto Plata City Tour</h3><p class="text-gray-600">Umbrella Street, Pink Street, Fort San Felipe and cable car views over the coast.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Beach Break</h3><p class="text-gray-600">Relaxed beach day with low walking demand for couples, families and easy-paced groups.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Catamaran &amp; Snorkel</h3><p class="text-gray-600">Sailing, music and snorkeling for social groups and active couples.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100"><h3 class="font-display font-bold text-lg mb-2">Port Planning</h3><p class="text-gray-600">Understand Amber Cove vs Taino Bay transfer times and pickup details before booking.</p></div>
  </div>
</div></section>'''
    + faq_section("Puerto Plata Cruise Excursions FAQ", HOME_FAQ)
    + cta_section()
)

print("Home content written")


# --- Tour pages ---
(ROOT / "content/damajagua-waterfalls-shore-excursion-puerto-plata.html").write_text(
    tour_content(
        "Damajagua Waterfalls",
        "Most Popular",
        "popular-badge",
        "The Damajagua waterfalls excursion is Puerto Plata's most popular adventure. Known as 27 Charcos, this route combines tropical canyon scenery, swimming in natural pools, and optional jumps or slides based on conditions and confidence level. It is best for active travelers comfortable with moderate physical effort.",
        "damajagua-waterfalls.png",
        "Damajagua waterfalls shore excursion in Puerto Plata with tropical pools canyon adventure and guided route",
        [
            (
                "damajagua-waterfalls.png",
                "Damajagua natural pools and waterfalls in Puerto Plata for cruise-day adventure excursions",
                "Waterfalls + Natural Pools",
                "Guided route through cascading falls and freshwater pools with safety instructions throughout.",
            ),
            (
                "damajagua-waterfalls.png",
                "Damajagua canyon adventure levels in Puerto Plata with optional jumps and slides",
                "Adventure Level Choices",
                "Guides usually provide alternatives for selected jumps and slides depending on comfort and conditions.",
            ),
            (
                "puerto-plata-port.png",
                "Puerto Plata port pickup planning for Damajagua excursions from Amber Cove and Taino Bay",
                "Port Pickup Planning",
                "Suppliers vary by pickup point and transfer flow from Amber Cove or Taino Bay.",
            ),
        ],
        {
            "Best For": "Most Popular Adventure",
            "Duration": "4.5-6 hours typical",
            "Walking Required": "Moderate to high on wet terrain",
            "Adventure Level": "High",
            "Return To Ship Confidence": "High with cruise-aware operators",
            "Family Friendly": "Good for active families with suitable ages",
            "Port Compatibility": "Amber Cove / Taino Bay / check supplier",
        },
        LINKS_DEFAULT,
    )
)

(ROOT / "content/monkeyland-shore-excursion-puerto-plata.html").write_text(
    tour_content(
        "Monkeyland",
        "Best for Families",
        "best-for-badge",
        "Monkeyland is one of the easiest Puerto Plata picks for families, couples and mixed-age groups. Visitors interact with squirrel monkeys in a managed setting, guided by staff who explain behavior and habitat. Walking demand is usually manageable and the format works well for cruise travelers wanting memorable wildlife without extreme activity.",
        "monkeyland.png",
        "Monkeyland Puerto Plata cruise excursion with squirrel monkey interaction in family-friendly environment",
        [
            (
                "monkeyland.png",
                "Squirrel monkey interaction at Monkeyland Puerto Plata excursion for cruise passengers",
                "Squirrel Monkey Encounters",
                "A close-up, guided wildlife experience designed for photo-friendly moments and education.",
            ),
            (
                "monkeyland.png",
                "Monkeyland family excursion in Puerto Plata for couples families and groups from cruise ships",
                "Great for Families",
                "Flexible pacing makes it a strong fit for families, couples, and multigenerational groups.",
            ),
            (
                "amber-cove-taino-bay.png",
                "Amber Cove and Taino Bay pickup differences for Monkeyland shore excursion in Puerto Plata",
                "Pickup Clarity",
                "Always confirm whether your booking includes Amber Cove, Taino Bay, or both pickup options.",
            ),
        ],
        {
            "Best For": "Families and wildlife lovers",
            "Duration": "4-5 hours typical",
            "Walking Required": "Low to moderate",
            "Adventure Level": "Low",
            "Return To Ship Confidence": "Very high on standard schedules",
            "Family Friendly": "Excellent",
            "Port Compatibility": "Amber Cove / Taino Bay / check supplier",
        },
        LINKS_DEFAULT,
    )
)

(ROOT / "content/puerto-plata-city-tour.html").write_text(
    tour_content(
        "Puerto Plata City Tour",
        "Best for First-Time Visitors",
        "first-time-badge",
        "A Puerto Plata city tour is the best orientation for first-time visitors who want culture and landmarks over high adventure. Typical routes include the historic center, Umbrella Street, Pink Street, Fort San Felipe, and cable car access toward Mount Isabel de Torres when operating conditions allow.",
        "puerto-plata-city.png",
        "Puerto Plata city tour shore excursion including Umbrella Street Pink Street Fort San Felipe and cable car viewpoints",
        [
            (
                "puerto-plata-city.png",
                "Puerto Plata historic center city tour highlights for cruise visitors from Amber Cove and Taino Bay",
                "Historic Center Highlights",
                "Walk colorful streets, plazas and photo spots that define central Puerto Plata.",
            ),
            (
                "puerto-plata-city.png",
                "Fort San Felipe and Puerto Plata cultural landmarks on city tour excursion",
                "Landmark Stops",
                "Most itineraries include Fort San Felipe plus iconic Umbrella Street and Pink Street zones.",
            ),
            (
                "puerto-plata-city.png",
                "Mount Isabel de Torres cable car views during Puerto Plata cruise city excursion",
                "Cable Car Option",
                "When conditions and operations align, the cable car offers panoramic views over Puerto Plata.",
            ),
        ],
        {
            "Best For": "First-time Puerto Plata visitors",
            "Duration": "4-5.5 hours typical",
            "Walking Required": "Low to moderate",
            "Adventure Level": "Low",
            "Return To Ship Confidence": "High with guided timing",
            "Family Friendly": "Very good",
            "Port Compatibility": "Amber Cove / Taino Bay / check supplier",
        },
        LINKS_DEFAULT,
    )
)

(ROOT / "content/puerto-plata-beach-break.html").write_text(
    tour_content(
        "Puerto Plata Beach Break",
        "Best Beach Day|Easy Day Option",
        "beach-badge|easy-day-badge",
        "A Puerto Plata beach break is ideal when you want a relaxed cruise day with low walking and simple logistics. It suits families, couples and groups who prefer shade, swimming, and flexible free time rather than structured activity-heavy itineraries.",
        "puerto-plata-beach.png",
        "Puerto Plata beach break shore excursion with relaxed low-walking day for cruise passengers",
        [
            (
                "puerto-plata-beach.png",
                "Puerto Plata beach break excursion for cruise visitors seeking a calm easy day",
                "Relaxed Pace",
                "Minimal planning pressure and flexible time make this one of the easiest day choices.",
            ),
            (
                "puerto-plata-beach.png",
                "Family and couple friendly beach break in Puerto Plata with easy access from cruise ports",
                "Families + Couples",
                "Works well for mixed preferences where some want sun and others want a gentle shoreline walk.",
            ),
            (
                "puerto-plata-port.png",
                "Beach break transfer planning from Amber Cove and Taino Bay in Puerto Plata",
                "Easy Return Planning",
                "Shorter activity windows often make return-to-ship timing straightforward.",
            ),
        ],
        {
            "Best For": "Relaxed day seekers",
            "Duration": "4-6 hours typical",
            "Walking Required": "Low",
            "Adventure Level": "Low",
            "Return To Ship Confidence": "Very high with time buffer",
            "Family Friendly": "Excellent",
            "Port Compatibility": "Amber Cove / Taino Bay / check supplier",
        },
        LINKS_DEFAULT,
    )
)

(ROOT / "content/catamaran-snorkel-puerto-plata.html").write_text(
    tour_content(
        "Catamaran & Snorkel",
        "Best for Couples & Groups",
        "group-badge",
        "A catamaran and snorkel day blends sailing, coastal views, music and time in the water. This excursion is a strong fit for couples and social groups who want energy and scenery without the impact level of a waterfall route. Sea conditions can affect exact snorkeling stops and duration.",
        "catamaran-snorkel.png",
        "Catamaran and snorkel Puerto Plata shore excursion with sailing music and group-friendly atmosphere",
        [
            (
                "catamaran-snorkel.png",
                "Catamaran sailing off Puerto Plata for cruise excursion groups and couples",
                "Sailing Experience",
                "Enjoy open-water views and a social onboard atmosphere with music and guide support.",
            ),
            (
                "catamaran-snorkel.png",
                "Snorkeling stop on Puerto Plata catamaran excursion with variable sea conditions",
                "Snorkeling Stops",
                "Snorkeling quality varies by visibility and weather, so confirm expectations before departure.",
            ),
            (
                "amber-cove-taino-bay.png",
                "Catamaran excursion pickup coordination from Amber Cove and Taino Bay in Puerto Plata",
                "Port Transfer Coordination",
                "Check transfer times from Amber Cove or Taino Bay to your departure marina.",
            ),
        ],
        {
            "Best For": "Couples and groups",
            "Duration": "4.5-6 hours typical",
            "Walking Required": "Low to moderate",
            "Adventure Level": "Moderate",
            "Return To Ship Confidence": "High with operator buffer",
            "Family Friendly": "Good for confident swimmers",
            "Port Compatibility": "Amber Cove / Taino Bay / check supplier",
        },
        LINKS_DEFAULT,
    )
)

print("Tour content written")

BEST_FAQ = [
    ("What is the most popular Puerto Plata excursion?", "Damajagua waterfalls is usually the most-booked adventure option, while Monkeyland and city tours are strong alternatives for lower activity levels."),
    ("Which Puerto Plata excursion is best for families?", "Monkeyland and beach breaks are top family choices, with city tours also working well. Damajagua is best for active families comfortable with moderate effort."),
    ("Can both Amber Cove and Taino Bay guests book the same tours?", "Many tours serve both ports, but pickup points and departure times can differ. Always confirm your exact cruise terminal with the supplier."),
]

(ROOT / "content/best-puerto-plata-shore-excursions.html").write_text(
    f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Best Puerto Plata Shore Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Compare the best Puerto Plata cruise-day options across adventure level, logistics, and traveler type.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Cruise Port Access": "Amber Cove and Taino Bay",
    "Best For": "Comparing all excursion types",
    "Activity Range": "Low to high",
    "Family Friendly": "Strong with tour matching",
    "Return To Ship Advice": "Keep 60-90 min buffer",
    "Popular Excursion Types": "Waterfalls, wildlife, city, beach, catamaran",
})}</div></section>
<section class="py-16 bg-dr-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 text-center mb-4">Which Puerto Plata Excursion Is Right for Me?</h2>
  <p class="text-center text-gray-600 text-sm max-w-2xl mx-auto mb-10">Choose based on activity level, port logistics and your travel group.</p>
  <div class="overflow-x-auto rounded-3xl border border-dr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[760px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold rounded-tl-3xl">Excursion</th>
        <th class="py-4 px-3 font-semibold">Duration</th>
        <th class="py-4 px-3 font-semibold">Best For</th>
        <th class="py-4 px-3 font-semibold">Activity Level</th>
        <th class="py-4 px-4 font-semibold rounded-tr-3xl">Details</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-dr-100 hover:bg-dr-50/80"><td class="py-4 pr-4 font-semibold"><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="text-ocean-600">Damajagua</a> <span class="popular-badge text-[10px] py-0.5 px-2">Most Popular</span></td><td class="py-4 px-3 text-gray-600">4.5-6 hrs</td><td class="py-4 px-3 text-gray-600">Adventure seekers</td><td class="py-4 px-3 text-gray-600">High</td><td class="py-4 pl-3"><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="text-dr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-dr-100 hover:bg-dr-50/80"><td class="py-4 pr-4 font-semibold"><a href="monkeyland-shore-excursion-puerto-plata.html" class="text-ocean-600">Monkeyland</a> <span class="best-for-badge text-[10px] py-0.5 px-2">Best for Families</span></td><td class="py-4 px-3 text-gray-600">4-5 hrs</td><td class="py-4 px-3 text-gray-600">Families &amp; wildlife lovers</td><td class="py-4 px-3 text-gray-600">Low</td><td class="py-4 pl-3"><a href="monkeyland-shore-excursion-puerto-plata.html" class="text-dr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-dr-100 hover:bg-dr-50/80"><td class="py-4 pr-4 font-semibold"><a href="puerto-plata-city-tour.html" class="text-ocean-600">City Tour</a> <span class="first-time-badge text-[10px] py-0.5 px-2">Best for First-Time Visitors</span></td><td class="py-4 px-3 text-gray-600">4-5.5 hrs</td><td class="py-4 px-3 text-gray-600">Landmarks &amp; culture</td><td class="py-4 px-3 text-gray-600">Low to moderate</td><td class="py-4 pl-3"><a href="puerto-plata-city-tour.html" class="text-dr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-dr-100 hover:bg-dr-50/80"><td class="py-4 pr-4 font-semibold"><a href="puerto-plata-beach-break.html" class="text-ocean-600">Beach Break</a> <span class="beach-badge text-[10px] py-0.5 px-2">Best Beach Day</span></td><td class="py-4 px-3 text-gray-600">4-6 hrs</td><td class="py-4 px-3 text-gray-600">Relaxed couples &amp; families</td><td class="py-4 px-3 text-gray-600">Low</td><td class="py-4 pl-3"><a href="puerto-plata-beach-break.html" class="text-dr-600 font-medium text-xs">Guide →</a></td></tr>
        <tr class="border-b border-dr-100 hover:bg-dr-50/80"><td class="py-4 pr-4 font-semibold"><a href="catamaran-snorkel-puerto-plata.html" class="text-ocean-600">Catamaran &amp; Snorkel</a> <span class="group-badge text-[10px] py-0.5 px-2">Groups &amp; Couples</span></td><td class="py-4 px-3 text-gray-600">4.5-6 hrs</td><td class="py-4 px-3 text-gray-600">Social sailing day</td><td class="py-4 px-3 text-gray-600">Moderate</td><td class="py-4 pl-3"><a href="catamaran-snorkel-puerto-plata.html" class="text-dr-600 font-medium text-xs">Guide →</a></td></tr>
      </tbody>
    </table>
  </div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{faq_section("Best Puerto Plata Excursions FAQ", BEST_FAQ)}
{cta_section()}'''
)

(ROOT / "content/puerto-plata-cruise-port-guide.html").write_text(
    f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Puerto Plata Cruise Port Guide</h2>
  <p class="text-gray-600 text-sm">Everything cruise travelers need to know about docking at Amber Cove or Taino Bay and planning excursions with confidence.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Main Cruise Ports": "Amber Cove and Taino Bay",
    "City Access": "Both reach Puerto Plata city",
    "Typical Excursion Length": "4-6 hours",
    "Transport": "Pre-booked tours and taxis",
    "Return Advice": "Build 60-90 min buffer",
    "Best Use of Port Day": "Pick one core excursion style",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 space-y-8 text-sm text-gray-600 leading-relaxed">
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Where do cruise ships dock?</h3>
  <p>Puerto Plata is served by two main cruise terminals: <strong>Amber Cove</strong> (Maimón, west of the city) and <strong>Taino Bay</strong> (closer to downtown Puerto Plata). Your cruise documents, ship app or daily newsletter will name your docking location — check this before booking any independent shore excursion.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Amber Cove vs Taino Bay — what changes for you?</h3>
  <p><strong>Amber Cove</strong> is a purpose-built cruise port with shops, pools and a controlled guest zone — excursion pickups are usually coordinated inside or just outside the terminal. <strong>Taino Bay</strong> sits nearer the historic city and has a different terminal layout and meeting-point flow. Same destination, different pickup logistics. See our <a href="amber-cove-vs-taino-bay.html" class="text-ocean-600 font-medium">Amber Cove vs Taino Bay comparison</a> for details.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">How far are the ports from Puerto Plata city?</h3>
  <p><strong>Taino Bay</strong> is roughly 1–2 km from central Puerto Plata — a short taxi or tour transfer. <strong>Amber Cove</strong> is about 11 km (7 miles) west in Maimón, typically 15–25 minutes by road depending on traffic. Damajagua, Monkeyland and beach routes are reachable from both ports, but transfer times differ — confirm with your operator.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Transport tips</h3>
  <ul class="list-disc pl-5 space-y-2"><li>Pre-booked shore excursions are the most reliable option for cruise timeframes.</li><li>Official taxis are available at both terminals; agree the fare before departing.</li><li>USD is widely accepted; Dominican pesos (DOP) are the official currency.</li><li>Do not assume a tour that says "Puerto Plata pickup" covers your specific port without confirming.</li></ul></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Excursion timing</h3>
  <ul class="list-disc pl-5 space-y-2"><li>Most Puerto Plata port calls run 7–10 hours — enough for one full excursion plus buffer.</li><li>Damajagua and city tours typically need 4–6 hours including transfers.</li><li>Beach breaks and Monkeyland often fit shorter windows with comfortable return margins.</li><li>Account for terminal walk-out time when meeting your guide after disembarkation.</li></ul></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">Return-to-ship advice</h3>
  <p>Ship-sponsored excursions guarantee the vessel waits if the tour runs late. Reputable independent operators build in buffer — look for tours that target return at least <strong>60–90 minutes before all aboard</strong>. Keep your cruise line's port contact number and reconfirm end times the morning you dock.</p></div>
  <div><h3 class="text-xl font-display font-bold text-gray-900 mb-3">First-time visitor tips</h3>
  <p>Puerto Plata rewards travelers who plan one strong excursion rather than trying to cram too much. Match activity level to your group — Damajagua for adventure, Monkeyland for families, city tour for culture, beach break for easy pacing. Always verify your docking port and excursion pickup point before final payment.</p></div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}'''
)

(ROOT / "content/amber-cove-vs-taino-bay.html").write_text(
    f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Amber Cove vs Taino Bay</h2>
  <p class="text-gray-600 text-sm">Both are Puerto Plata cruise ports. This comparison helps you avoid pickup confusion and choose tours with clean logistics.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Destination": "Puerto Plata",
    "Cruise Ports": "Amber Cove and Taino Bay",
    "Best Use": "Confirm pickup before booking",
    "City Access": "Available from both ports",
    "Transfer Variance": "Depends on traffic and route",
    "Return Advice": "Prioritize buffer and supplier clarity",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-4xl mx-auto px-4">
  <div class="overflow-x-auto rounded-3xl border border-dr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[640px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold">Factor</th>
        <th class="py-4 px-4 font-semibold">Amber Cove</th>
        <th class="py-4 px-4 font-semibold">Taino Bay</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Location</td><td class="py-4 px-4 text-gray-600">Maimón, ~11 km west of Puerto Plata city</td><td class="py-4 px-4 text-gray-600">Downtown Puerto Plata area, ~1–2 km from historic centre</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Terminal facilities</td><td class="py-4 px-4 text-gray-600">Purpose-built cruise village — shops, pools, zip line, controlled guest zone</td><td class="py-4 px-4 text-gray-600">Modern terminal closer to city — different layout and walking distances</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Excursion pickup</td><td class="py-4 px-4 text-gray-600">Usually inside or at designated gates within the Amber Cove complex</td><td class="py-4 px-4 text-gray-600">Meeting points vary — confirm exact gate or assembly area with your operator</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Transfer to city sights</td><td class="py-4 px-4 text-gray-600">~15–25 min to Puerto Plata historic centre by road</td><td class="py-4 px-4 text-gray-600">~5–10 min to Umbrella Street, Fort San Felipe and central landmarks</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Excursions that work from both</td><td class="py-4 px-4 text-gray-600" colspan="2"><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="text-ocean-600">Damajagua</a>, <a href="monkeyland-shore-excursion-puerto-plata.html" class="text-ocean-600">Monkeyland</a>, <a href="puerto-plata-city-tour.html" class="text-ocean-600">city tour</a>, <a href="puerto-plata-beach-break.html" class="text-ocean-600">beach break</a> and <a href="catamaran-snorkel-puerto-plata.html" class="text-ocean-600">catamaran</a> — but pickup logistics differ; always confirm your port with the supplier</td></tr>
        <tr><td class="py-4 px-4 font-semibold text-gray-900">Which port does my ship use?</td><td class="py-4 px-4 text-gray-600" colspan="2">Check your cruise documents, ship app or daily newsletter — do not guess. Booking the wrong pickup point is the most common shore-excursion mistake in Puerto Plata.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="mt-8 text-sm text-gray-600 leading-relaxed">For most travelers, excursion quality matters more than which port you dock at. The key is booking a supplier that explicitly supports your port and provides a conservative return schedule.</p>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}'''
)

(ROOT / "content/one-day-in-puerto-plata-from-a-cruise-ship.html").write_text(
    f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">One Day in Puerto Plata from a Cruise Ship</h2>
  <p class="text-gray-600 text-sm">Sample Puerto Plata day plans for cruise guests arriving at Amber Cove or Taino Bay.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Cruise Port Start": "Amber Cove or Taino Bay",
    "Best For": "Efficient day planning",
    "Plan Style": "Adventure, mixed, or easy day",
    "Typical Tour Length": "4-6 hours",
    "Return Window": "60-90 min before all aboard",
    "Backup Tip": "Keep one simple fallback option",
})}</div></section>
<section class="py-12 bg-dr-50"><div class="max-w-3xl mx-auto px-4 space-y-10">
  <div class="bg-white rounded-3xl p-6 border border-dr-100 shadow-sm">
    <span class="popular-badge mb-3 inline-block">Adventure Day</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Morning to Afternoon: Damajagua Route</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Early transfer from Amber Cove or Taino Bay to the Damajagua area.</li>
      <li>Guided waterfall adventure with natural pool swims and route options.</li>
      <li>Lunch and return transfer with buffer before all aboard.</li>
    </ol>
    <a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Damajagua guide →</a>
  </div>
  <div class="bg-white rounded-3xl p-6 border border-dr-100 shadow-sm">
    <span class="first-time-badge mb-3 inline-block">Culture + Landmarks</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">City Tour Focus</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Historic center highlights including Umbrella Street and Pink Street.</li>
      <li>Fort San Felipe stop and optional cable car segment if operating.</li>
      <li>Relaxed return timing suitable for first-time visitors.</li>
    </ol>
    <a href="puerto-plata-city-tour.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">City tour guide →</a>
  </div>
  <div class="bg-white rounded-3xl p-6 border border-dr-100 shadow-sm">
    <span class="easy-day-badge mb-3 inline-block">Easy Day Option</span>
    <h3 class="text-xl font-display font-bold text-gray-900 mb-3">Beach Break + Flexible Return</h3>
    <ol class="text-sm text-gray-600 space-y-2 list-decimal pl-5">
      <li>Simple beach transfer with low walking and unhurried pacing.</li>
      <li>Free time for swimming, lounging and light lunch.</li>
      <li>Early return strategy for stress-free all-aboard timing.</li>
    </ol>
    <a href="puerto-plata-beach-break.html" class="inline-block mt-4 text-ocean-600 font-semibold text-sm">Beach break guide →</a>
  </div>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{cta_section()}'''
)

WORTH_FAQ = [
    ("Is Puerto Plata worth visiting on a cruise?", "Yes. Puerto Plata gives you a wide excursion mix in one destination, from adventure and wildlife interaction to culture, beach and sailing."),
    ("Is Puerto Plata safe for cruise passengers?", "Most cruise visitors use organized excursions and standard tourist routes. As with any port day, follow guide instructions and use reputable operators."),
    ("What is Puerto Plata known for?", "Puerto Plata is known for Damajagua waterfalls, Monkeyland, colorful city landmarks, beaches, and cruise access via Amber Cove and Taino Bay."),
    ("Is Amber Cove the same as Puerto Plata?", "Amber Cove is a cruise port serving the Puerto Plata destination. It is one docking point in the Puerto Plata area."),
    ("Is Taino Bay the same as Puerto Plata?", "Taino Bay is also a cruise port serving Puerto Plata. Like Amber Cove, it is a gateway into the same destination."),
]

(ROOT / "content/is-puerto-plata-worth-visiting.html").write_text(
    f'''<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4 text-center">Is Puerto Plata Worth Visiting?</h2>
  <p class="text-gray-600 text-sm text-center leading-relaxed">Straight answers for cruise travelers deciding how to use a Puerto Plata port day.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snapshot({
    "Short Answer": "Yes for most cruise travelers",
    "Known For": "Waterfalls, wildlife interaction, city landmarks, beach, sailing",
    "Cruise Access": "Amber Cove and Taino Bay",
    "Best For": "Families, couples and groups",
    "Activity Choice": "Low to high",
    "Planning Priority": "Match excursion to your pace and port",
})}</div></section>
<section class="py-12 bg-white"><div class="max-w-3xl mx-auto px-4 space-y-6 text-sm text-gray-600 leading-relaxed">
  <p><strong>Puerto Plata is worth visiting for most cruise passengers.</strong> Few destinations offer this many shore-day styles in one place. You can choose high-adventure waterfalls, family wildlife interaction, colorful city sightseeing, beach downtime, or social sailing.</p>
  <p><strong>It works for mixed travel groups.</strong> Families often choose Monkeyland or beach breaks, couples split between catamaran and city options, and active travelers typically prioritize Damajagua.</p>
  <p><strong>The key is understanding your docking port.</strong> Since ships may arrive at Amber Cove or Taino Bay, clear pickup instructions matter as much as the excursion itself.</p>
  <p><strong>Bottom line:</strong> Puerto Plata is a strong cruise stop when you plan around your activity level and return-to-ship timing.</p>
</div></section>
<section class="pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">{related_links(LINKS_DEFAULT)}</div></section>
{faq_section("Is Puerto Plata Worth Visiting? FAQ", WORTH_FAQ)}
{cta_section()}'''
)

print("Guide content written")


PAGES = [
    (
        "index.html",
        "home",
        "partials/hero-home.html",
        "content/home.html",
        "hero-puerto-plata.png",
        "Puerto Plata Cruise Excursion | Excursions from Amber Cove and Taino Bay",
        "Puerto Plata cruise destination guide covering the best excursions, port logistics, and planning advice for Amber Cove and Taino Bay visitors.",
        "Puerto Plata cruise excursion, Puerto Plata shore excursions, Amber Cove excursions, Taino Bay excursions",
        BASE_URL + "/",
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "WebSite",
                    "name": SITE,
                    "url": BASE_URL + "/",
                    "description": "Puerto Plata cruise excursion destination guide",
                },
                {
                    "@type": "LocalBusiness",
                    "name": SITE,
                    "url": BASE_URL + "/",
                    "description": "Cruise destination planning guide for Puerto Plata excursions",
                    "address": {
                        "@type": "PostalAddress",
                        "addressLocality": "Puerto Plata",
                        "addressRegion": "Puerto Plata",
                        "addressCountry": "DO",
                    },
                    "areaServed": {"@type": "City", "name": "Puerto Plata"},
                },
                {
                    "@type": "TouristInformationCenter",
                    "name": SITE,
                    "url": BASE_URL + "/",
                    "description": "Puerto Plata cruise excursion planning information",
                },
                {"@type": "FAQPage", "mainEntity": faq_schema(HOME_FAQ)},
            ],
        },
    ),
    (
        "best-puerto-plata-shore-excursions.html",
        "excursions",
        "partials/hero-best-excursions.html",
        "content/best-puerto-plata-shore-excursions.html",
        "best-puerto-plata-excursions.png",
        "Best Puerto Plata Shore Excursions | Compare Cruise Day Options",
        "Compare the best Puerto Plata shore excursions by adventure level, traveler type, and Amber Cove vs Taino Bay logistics.",
        "best Puerto Plata shore excursions, Puerto Plata cruise excursions comparison",
        BASE_URL + "/best-puerto-plata-shore-excursions.html",
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "TouristInformationCenter",
                    "name": "Best Puerto Plata Shore Excursions",
                    "url": BASE_URL + "/best-puerto-plata-shore-excursions.html",
                    "description": "Puerto Plata excursion comparison guide",
                },
                {"@type": "FAQPage", "mainEntity": faq_schema(BEST_FAQ)},
            ],
        },
    ),
    (
        "puerto-plata-cruise-port-guide.html",
        "port",
        "partials/hero-port-guide.html",
        "content/puerto-plata-cruise-port-guide.html",
        "puerto-plata-port.png",
        "Puerto Plata Cruise Port Guide | Amber Cove and Taino Bay",
        "Puerto Plata cruise port guide with Amber Cove and Taino Bay differences, city transfer tips, and return-to-ship planning advice.",
        "Puerto Plata cruise port guide, Amber Cove vs Taino Bay, Puerto Plata port logistics",
        BASE_URL + "/puerto-plata-cruise-port-guide.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristInformationCenter",
            "name": "Puerto Plata Cruise Port Guide",
            "url": BASE_URL + "/puerto-plata-cruise-port-guide.html",
        },
    ),
    (
        "amber-cove-vs-taino-bay.html",
        "ports",
        "partials/hero-amber-vs-taino.html",
        "content/amber-cove-vs-taino-bay.html",
        "amber-cove-taino-bay.png",
        "Amber Cove vs Taino Bay | Puerto Plata Cruise Port Comparison",
        "Compare Amber Cove and Taino Bay for pickup, transfers and excursion planning in Puerto Plata.",
        "Amber Cove vs Taino Bay, Puerto Plata cruise ports",
        BASE_URL + "/amber-cove-vs-taino-bay.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristInformationCenter",
            "name": "Amber Cove vs Taino Bay",
            "url": BASE_URL + "/amber-cove-vs-taino-bay.html",
        },
    ),
    (
        "one-day-in-puerto-plata-from-a-cruise-ship.html",
        "oneday",
        "partials/hero-one-day.html",
        "content/one-day-in-puerto-plata-from-a-cruise-ship.html",
        "one-day-puerto-plata.png",
        "One Day in Puerto Plata from a Cruise Ship | Itinerary Ideas",
        "Sample one-day Puerto Plata cruise itineraries with adventure, culture and easy-day options from Amber Cove and Taino Bay.",
        "one day in Puerto Plata cruise ship, Puerto Plata cruise itinerary",
        BASE_URL + "/one-day-in-puerto-plata-from-a-cruise-ship.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristInformationCenter",
            "name": "One Day in Puerto Plata",
            "url": BASE_URL + "/one-day-in-puerto-plata-from-a-cruise-ship.html",
        },
    ),
    (
        "damajagua-waterfalls-shore-excursion-puerto-plata.html",
        "damajagua",
        "partials/hero-damajagua.html",
        "content/damajagua-waterfalls-shore-excursion-puerto-plata.html",
        "damajagua-waterfalls.png",
        "Damajagua Waterfalls Shore Excursion Puerto Plata | 27 Charcos",
        "Damajagua waterfalls shore excursion from Puerto Plata with natural pools, adventure level guidance, and cruise-friendly return timing.",
        "Damajagua waterfalls Puerto Plata cruise excursion, 27 Charcos shore excursion",
        BASE_URL + "/damajagua-waterfalls-shore-excursion-puerto-plata.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": "Damajagua Waterfalls Shore Excursion Puerto Plata",
            "description": "Waterfalls and natural pools adventure from Puerto Plata cruise ports.",
            "touristType": "Cruise passengers",
            "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        },
    ),
    (
        "monkeyland-shore-excursion-puerto-plata.html",
        "monkeyland",
        "partials/hero-monkeyland.html",
        "content/monkeyland-shore-excursion-puerto-plata.html",
        "monkeyland.png",
        "Monkeyland Shore Excursion Puerto Plata | Best for Families",
        "Monkeyland shore excursion from Puerto Plata with squirrel monkey interaction, family-focused pacing, and pickup planning from both ports.",
        "Monkeyland Puerto Plata shore excursion, family excursion Puerto Plata cruise",
        BASE_URL + "/monkeyland-shore-excursion-puerto-plata.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": "Monkeyland Shore Excursion Puerto Plata",
            "description": "Family-friendly squirrel monkey interaction tour from Puerto Plata.",
            "touristType": "Cruise passengers",
            "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        },
    ),
    (
        "puerto-plata-city-tour.html",
        "citytour",
        "partials/hero-city-tour.html",
        "content/puerto-plata-city-tour.html",
        "puerto-plata-city.png",
        "Puerto Plata City Tour | Umbrella Street, Fort and Cable Car",
        "Puerto Plata city tour for cruise visitors including Umbrella Street, Pink Street, Fort San Felipe, and cable car viewpoints.",
        "Puerto Plata city tour cruise excursion, Umbrella Street Pink Street Fort San Felipe",
        BASE_URL + "/puerto-plata-city-tour.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": "Puerto Plata City Tour",
            "description": "Historic and landmark-focused Puerto Plata city excursion from cruise ports.",
            "touristType": "Cruise passengers",
            "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        },
    ),
    (
        "puerto-plata-beach-break.html",
        "beach",
        "partials/hero-beach-break.html",
        "content/puerto-plata-beach-break.html",
        "puerto-plata-beach.png",
        "Puerto Plata Beach Break | Easy Day Option for Cruise Visitors",
        "Puerto Plata beach break excursion with low walking, relaxed pacing, and easy return-to-ship planning from Amber Cove and Taino Bay.",
        "Puerto Plata beach break cruise excursion, easy day Puerto Plata",
        BASE_URL + "/puerto-plata-beach-break.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": "Puerto Plata Beach Break",
            "description": "Relaxed beach-focused shore excursion from Puerto Plata cruise ports.",
            "touristType": "Cruise passengers",
            "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        },
    ),
    (
        "catamaran-snorkel-puerto-plata.html",
        "catamaran",
        "partials/hero-catamaran.html",
        "content/catamaran-snorkel-puerto-plata.html",
        "catamaran-snorkel.png",
        "Catamaran & Snorkel Puerto Plata | Sailing Shore Excursion",
        "Catamaran and snorkel shore excursion in Puerto Plata with sailing, music, reef stops, and cruise-port transfer planning.",
        "catamaran snorkel Puerto Plata cruise excursion, Puerto Plata sailing tour",
        BASE_URL + "/catamaran-snorkel-puerto-plata.html",
        {
            "@context": "https://schema.org",
            "@type": "TouristTrip",
            "name": "Catamaran & Snorkel Puerto Plata",
            "description": "Sailing and snorkeling shore excursion from Puerto Plata cruise ports.",
            "touristType": "Cruise passengers",
            "provider": {"@type": "Organization", "name": SITE, "url": BASE_URL},
        },
    ),
    (
        "is-puerto-plata-worth-visiting.html",
        "worth",
        "partials/hero-worth-visiting.html",
        "content/is-puerto-plata-worth-visiting.html",
        "puerto-plata-intro.png",
        "Is Puerto Plata Worth Visiting? | Cruise Passenger FAQ Guide",
        "Is Puerto Plata worth visiting on a cruise? Read practical answers about safety, highlights, and Amber Cove vs Taino Bay context.",
        "is Puerto Plata worth visiting, Puerto Plata cruise FAQ",
        BASE_URL + "/is-puerto-plata-worth-visiting.html",
        {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "TouristInformationCenter",
                    "name": "Is Puerto Plata Worth Visiting",
                    "url": BASE_URL + "/is-puerto-plata-worth-visiting.html",
                },
                {"@type": "FAQPage", "mainEntity": faq_schema(WORTH_FAQ)},
            ],
        },
    ),
]

for fname, page, hero_f, content_f, preload, title, desc, kw, canon, ld in PAGES:
    shell(
        fname,
        title=title,
        description=desc,
        keywords=kw,
        canonical=canon,
        preload=preload,
        page=page,
        hero_file=hero_f,
        content_file=content_f,
        ld_json=ld,
    )

print("HTML shells written")

urls = [
    (BASE_URL + "/", "1.0", "weekly"),
    (BASE_URL + "/best-puerto-plata-shore-excursions.html", "0.9", "monthly"),
    (BASE_URL + "/puerto-plata-cruise-port-guide.html", "0.8", "monthly"),
    (BASE_URL + "/amber-cove-vs-taino-bay.html", "0.8", "monthly"),
    (BASE_URL + "/one-day-in-puerto-plata-from-a-cruise-ship.html", "0.8", "monthly"),
    (BASE_URL + "/damajagua-waterfalls-shore-excursion-puerto-plata.html", "0.9", "monthly"),
    (BASE_URL + "/monkeyland-shore-excursion-puerto-plata.html", "0.9", "monthly"),
    (BASE_URL + "/puerto-plata-city-tour.html", "0.9", "monthly"),
    (BASE_URL + "/puerto-plata-beach-break.html", "0.9", "monthly"),
    (BASE_URL + "/catamaran-snorkel-puerto-plata.html", "0.9", "monthly"),
    (BASE_URL + "/is-puerto-plata-worth-visiting.html", "0.8", "monthly"),
]

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for loc, pri, freq in urls:
    sitemap += (
        f"  <url><loc>{loc}</loc><lastmod>2026-06-10</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{pri}</priority></url>\n"
    )
sitemap += "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sitemap)

(ROOT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n"
)

(ROOT / "wrangler.jsonc").write_text(
    '''{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "puerto-plata-cruise-excursions",
  "compatibility_date": "2026-06-10",
  "observability": { "enabled": true },
  "assets": { "directory": "." },
  "routes": [{ "pattern": "puertoplatacruiseexcursion.com", "custom_domain": true }]
}
'''
)

print("Sitemap, robots, wrangler written — DONE")
