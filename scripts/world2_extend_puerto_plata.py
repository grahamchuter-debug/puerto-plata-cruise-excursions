#!/usr/bin/env python3
"""World 2.0 content extensions for Puerto Plata Cruise Excursion.

Self-contained because build-puerto-plata-site.py writes at import time.
Focus: Damajagua vs beach, strengthen Amber Cove vs Taino Bay honesty,
legal/trust pages, schedule sitemap merge. No fabricated pier schedule split.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://puertoplatacruiseexcursion.com"
SITE = "Puerto Plata Cruise Excursion"
DATE = "2026-09-04"
HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(37, 99, 235, 0.72) 0%, "
    "rgba(245, 158, 11, 0.58) 50%, rgba(30, 58, 138, 0.52) 100%)"
)
HEAD_COMMON = """  <script src="https://cdn.tailwindcss.com"></script>
  <script src="js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/site.css" />"""


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print(f"  wrote {rel}")


def soft_claims_in_text(html: str) -> str:
    replacements = [
        (
            r"Allow 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"Keep 60[--]90 min buffer on independent tours",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"Keep 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"Build 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"60[--]90 min before all aboard",
            "a sensible return window before all aboard",
        ),
        (
            r"60[--]90 minutes? before all aboard",
            "a sensible return window before all aboard",
        ),
        (
            r"Always keep 60[--]90 min buffer",
            "Build your own buffer; confirm operator return plan",
        ),
        (
            r"Ship-sponsored excursions guarantee the vessel waits if the tour runs late\.",
            "Ship-sold tours often include a wait-if-late policy from the cruise line.",
        ),
        (
            r"Ship-sold tours often include a wait-if-late policy from the cruise line.",
            "Ship-sold tours often include a wait-if-late policy from the cruise line.",
        ),
        (
            r"Ship-sold tours often include a wait-if-late policy from the cruise line.",
            "Ship-sold tours often include a wait-if-late policy from the cruise line.",
        ),
        (r"Return To Ship On Time", "Plan a return window"),
    ]
    out = html
    for pat, repl in replacements:
        out = re.sub(pat, repl, out, flags=re.IGNORECASE)
    return out.replace("\u2014", " - ").replace("\u2013", "-")


def soft_all_content() -> None:
    for folder in (ROOT / "content", ROOT / "partials"):
        if not folder.exists():
            continue
        for path in folder.rglob("*.html"):
            original = path.read_text(encoding="utf-8")
            updated = soft_claims_in_text(original)
            if updated != original:
                path.write_text(updated, encoding="utf-8")
                print(f"  softened {path.relative_to(ROOT)}")
    build = ROOT / "scripts" / "build-puerto-plata-site.py"
    if build.exists():
        original = build.read_text(encoding="utf-8")
        updated = soft_claims_in_text(original)
        if updated != original:
            build.write_text(updated, encoding="utf-8")
            print("  softened scripts/build-puerto-plata-site.py")


def snapshot(items: dict[str, str]) -> str:
    rows = "".join(
        f'<div class="cruise-snapshot__item"><dt>{k}</dt><dd>{v}</dd></div>'
        for k, v in items.items()
    )
    return (
        '<aside class="cruise-snapshot mb-10 px-4 sm:px-0" aria-label="Cruise passenger snapshot">'
        '<h3 class="font-display font-bold text-lg text-gray-900 mb-4">Cruise Passenger Snapshot</h3>'
        f'<dl class="cruise-snapshot__grid">{rows}</dl></aside>'
    )


def shell(
    *,
    filename: str,
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
    html = f"""<!DOCTYPE html>
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
  <meta property="og:image" content="{DOMAIN}/images/{preload}" />
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
</html>"""
    write(filename, html)


def hero(
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
    bc = ""
    if breadcrumb:
        bc = (
            '<nav class="site-hero__breadcrumb flex items-center gap-2 mb-4 text-xs text-white/60" aria-label="Breadcrumb">'
            '<a href="index.html" class="hover:text-white transition-colors">Home</a>'
            '<svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>'
            f'<span class="text-white/80">{breadcrumb}</span></nav>'
        )
    tag_block = (
        f'<div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">{tags}</div>'
        if tags
        else ""
    )
    act_block = (
        f'<div class="site-hero__actions flex flex-col sm:flex-row gap-3">{actions}</div>'
        if actions
        else '<div class="site-hero__actions"></div>'
    )
    return f"""<section class="site-hero">
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
</section>"""


def internal_links() -> str:
    return """<nav class="mt-10 pt-8 border-t border-dr-100" aria-label="Related Puerto Plata guides">
  <p class="text-sm font-semibold text-gray-900 mb-3">Plan your Puerto Plata port day</p>
  <div class="flex flex-wrap gap-3 text-sm">
    <a href="puerto-plata-cruise-port-guide.html" class="text-ocean-600 hover:text-ocean-800 font-medium">Port Guide</a>
    <span class="text-gray-300">·</span>
    <a href="best-puerto-plata-shore-excursions.html" class="text-ocean-600 hover:text-ocean-800 font-medium">Best Excursions</a>
    <span class="text-gray-300">·</span>
    <a href="amber-cove-vs-taino-bay.html" class="text-ocean-600 hover:text-ocean-800 font-medium">Amber Cove vs Taino Bay</a>
    <span class="text-gray-300">·</span>
    <a href="puerto-plata-waterfalls-vs-beach.html" class="text-ocean-600 hover:text-ocean-800 font-medium">Waterfalls vs Beach</a>
    <span class="text-gray-300">·</span>
    <a href="ship-schedule/" class="text-ocean-600 hover:text-ocean-800 font-medium">Ship Schedule</a>
  </div>
</nav>"""


def concierge_panel() -> str:
    return """<section class="py-14 bg-white" id="concierge" aria-labelledby="concierge-heading">
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="concierge-panel">
      <h2 id="concierge-heading" class="font-display font-bold text-2xl sm:text-3xl mb-3">Need help shaping your Puerto Plata day?</h2>
      <p class="text-white/90 text-sm sm:text-base leading-relaxed mb-4">
        Tell us your ship, call date, which facility you use if known (Amber Cove or Taino Bay), and whether you lean Damajagua, beach time or city sightseeing.
        We are an independent planning resource - not the cruise line and not a ticket marketplace.
      </p>
      <p class="text-white/80 text-sm leading-relaxed mb-5">
        email <a href="mailto:hello@puertoplatacruiseexcursion.com">hello@puertoplatacruiseexcursion.com</a>.
        We do not promise instant replies or 24/7 staffing.
      </p>
      <div class="flex flex-col sm:flex-row gap-3">
        <a href="mailto:hello@puertoplatacruiseexcursion.com" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Email the Puerto Plata concierge</a>
        <a href="best-puerto-plata-shore-excursions.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Compare excursion types</a>
      </div>
    </div>
  </div>
</section>"""


def write_nav() -> None:
    write(
        "partials/nav.html",
        """<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-dr-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="index.html" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Puerto Plata<br/><span class="text-[10px] font-body font-normal text-amber-600 tracking-widest uppercase">Cruise Excursion</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="best-puerto-plata-shore-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" data-nav="damajagua" class="text-gray-600 hover:text-ocean-600 transition-colors">Damajagua</a>
        <a href="amber-cove-vs-taino-bay.html" data-nav="ports" class="text-gray-600 hover:text-ocean-600 transition-colors">Amber Cove vs Taino Bay</a>
        <a href="ship-schedule/" data-nav="schedule" class="text-gray-600 hover:text-ocean-600 transition-colors">Ship Schedule</a>
        <a href="puerto-plata-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
      </div>
      <a href="contact.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">Contact concierge</a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>
""",
    )


def write_footer() -> None:
    write(
        "partials/footer.html",
        f"""<footer class="bg-gray-900 text-gray-400 py-14">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
      <div class="sm:col-span-2 lg:col-span-1">
        <a href="index.html" class="font-display font-semibold text-white text-lg">{SITE}</a>
        <p class="mt-3 text-sm leading-relaxed">Independent planning guide for cruise visitors to Puerto Plata. Amber Cove and Taino Bay are different arrival points - confirm yours. Not affiliated with any cruise line.</p>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="best-puerto-plata-shore-excursions.html" class="hover:text-white transition-colors">All Excursions</a></li>
          <li><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="hover:text-white transition-colors">Damajagua</a></li>
          <li><a href="puerto-plata-beach-break.html" class="hover:text-white transition-colors">Beach Break</a></li>
          <li><a href="puerto-plata-waterfalls-vs-beach.html" class="hover:text-white transition-colors">Waterfalls vs Beach</a></li>
          <li><a href="amber-cove-vs-taino-bay.html" class="hover:text-white transition-colors">Amber Cove vs Taino Bay</a></li>
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Resources</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="puerto-plata-cruise-port-guide.html" class="hover:text-white transition-colors">Port Guide</a></li>
          <li><a href="ship-schedule/" class="hover:text-white transition-colors">Ship Schedule</a></li>
          <li><a href="one-day-in-puerto-plata-from-a-cruise-ship.html" class="hover:text-white transition-colors">One Day Itinerary</a></li>
          <li><a href="methodology.html" class="hover:text-white transition-colors">Methodology</a></li>
        </ul>
      </div>
      <div>
        <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Legal</h3>
        <ul class="space-y-2 text-sm">
          <li><a href="about.html" class="hover:text-white transition-colors">About</a></li>
          <li><a href="contact.html" class="hover:text-white transition-colors">Contact</a></li>
          <li><a href="privacy.html" class="hover:text-white transition-colors">Privacy</a></li>
          <li><a href="terms.html" class="hover:text-white transition-colors">Terms</a></li>
        </ul>
      </div>
    </div>
    <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
      <p>&copy; 2026 {SITE}. Confirm times with your cruise line and operators. No fabricated prices or ratings on this site.</p>
    </div>
  </div>
</footer>
""",
    )


def content_home() -> str:
    snap = snapshot(
        {
            "Typical Time In Port": "8-10 hours (typical)",
            "Best For": "Damajagua, beach, city, Amber Cove / Taino Bay logistics",
            "Activity Level": "Varies - waterfalls higher; beach lower",
            "Family Friendly": "Strong with age-appropriate picks",
            "Return To Ship Friendly": "Build your own buffer; confirm operator return plan",
            "Popular Excursion Types": "Damajagua, beach break, city tour, catamaran",
        }
    )
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
  <p class="section-label mx-auto">Dominican Republic cruise call</p>
  <h2 class="text-2xl sm:text-3xl font-display font-bold text-gray-900 mb-3">Puerto Plata is waterfalls, beach and two arrival points</h2>
  <p class="text-gray-600 text-sm sm:text-base leading-relaxed"><strong>Amber Cove</strong> and <strong>Taino Bay</strong> are related but not the same physical arrival. Confirm which facility your sailing uses before booking pickups. Then choose Damajagua energy, a beach break or city sightseeing.</p>
</div></section>
<section class="pb-10 bg-white"><div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="decision-grid">
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Waterfalls day</h3><p>Damajagua for cascades and active pacing - confirm fitness rules and return timing.</p><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="text-ocean-600 font-semibold text-sm">Damajagua →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Beach day</h3><p>Organised beach breaks when swimming and shade matter more than waterfall climbs.</p><a href="puerto-plata-beach-break.html" class="text-ocean-600 font-semibold text-sm">Beach break →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">City / culture</h3><p>Historic centre stops when you want streets over sand.</p><a href="puerto-plata-city-tour.html" class="text-ocean-600 font-semibold text-sm">City tour →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Waterfalls vs beach</h3><p>Honest trade-offs for a typical Puerto Plata call.</p><a href="puerto-plata-waterfalls-vs-beach.html" class="text-ocean-600 font-semibold text-sm">Compare →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Which facility?</h3><p>Amber Cove and Taino Bay differ in layout and pickup flow - do not guess.</p><a href="amber-cove-vs-taino-bay.html" class="text-ocean-600 font-semibold text-sm">Compare ports →</a></div>
    <div class="decision-card"><h3 class="font-display font-bold text-gray-900">Find your ship</h3><p>Search Puerto Plata call dates. The schedule hub does not invent a pier split.</p><a href="ship-schedule/" class="text-ocean-600 font-semibold text-sm">Ship schedule →</a></div>
  </div>
</div></section>
<section class="pb-4 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-dr-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <p class="section-label">Arrival honesty</p>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Amber Cove is not Taino Bay</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Same destination region, different terminals. Excursion quality can be excellent from either facility when pickup logistics match your ship. Our schedule pages list Puerto Plata calls without manufacturing which pier each sailing uses - confirm with your cruise line.</p>
    <a href="amber-cove-vs-taino-bay.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Amber Cove vs Taino Bay</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
    <img src="images/amber-cove-taino-bay.png" alt="Cruise port facilities in the Puerto Plata area for Amber Cove and Taino Bay orientation" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Still deciding?</h2>
  <p class="text-white/85 text-sm mb-6">Compare waterfalls versus beach, or email the Puerto Plata concierge with your ship and facility.</p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="puerto-plata-waterfalls-vs-beach.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Waterfalls vs beach</a>
    <a href="contact.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Contact concierge</a>
  </div>
</div></section>
{concierge_panel()}"""


def content_waterfalls_vs_beach() -> str:
    snap = snapshot(
        {
            "Best For": "Choosing Damajagua intensity vs beach calm",
            "Activity Level": "Waterfalls moderate-high; beach low",
            "Return Advice": "Build your own buffer; confirm operator return plan",
            "Facility Note": "Works from Amber Cove or Taino Bay when pickup matches",
            "Family": "Age and fitness rules on waterfall climbs",
            "Popular Pair": "Damajagua morning OR beach afternoon - rarely both rushed",
        }
    )
    return f"""<section class="pt-8 pb-6 bg-white"><div class="max-w-3xl mx-auto px-4">
  <p class="text-gray-600 leading-relaxed mb-4">On a typical Puerto Plata call, many guests choose between a <strong>Damajagua waterfalls day</strong> and a <strong>beach break</strong>. Both can work from Amber Cove or Taino Bay when pickup logistics match your facility.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-dr-50"><div class="max-w-5xl mx-auto px-4">
  <div class="grid md:grid-cols-2 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-dr-100">
      <div class="card-media rounded-2xl overflow-hidden aspect-[16/10] mb-4">
        <img src="images/damajagua-waterfalls.png" alt="Damajagua waterfall pools on a Puerto Plata shore excursion" width="600" height="375" loading="lazy" decoding="async" />
      </div>
      <h3 class="font-display font-bold text-lg mb-3">Waterfalls - Damajagua</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Cascades, jumps and active pacing on organised tours</li>
        <li>Confirm age, height and fitness rules with the operator</li>
        <li>Better when you want adventure over lounger time</li>
        <li>Do not invent exact crowd or water-level promises</li>
      </ul>
      <p class="mt-4"><a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" class="text-ocean-600 font-semibold">Damajagua →</a></p>
    </div>
    <div class="bg-white rounded-3xl p-6 border border-dr-100">
      <div class="card-media rounded-2xl overflow-hidden aspect-[16/10] mb-4">
        <img src="images/puerto-plata-beach.png" alt="Beach break shore excursion near Puerto Plata" width="600" height="375" loading="lazy" decoding="async" />
      </div>
      <h3 class="font-display font-bold text-lg mb-3">Beach day</h3>
      <ul class="space-y-2 text-gray-600">
        <li>Swimming, shade and resort-style pacing</li>
        <li>Better for mixed ages and lower intensity</li>
        <li>Confirm chair and transfer inclusions</li>
        <li>Leave a sensible return window before all aboard</li>
      </ul>
      <p class="mt-4"><a href="puerto-plata-beach-break.html" class="text-ocean-600 font-semibold">Beach break →</a></p>
    </div>
  </div>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def content_amber() -> str:
    snap = snapshot(
        {
            "Destination": "Puerto Plata area",
            "Cruise Ports": "Amber Cove and Taino Bay - different facilities",
            "Best Use": "Confirm pickup before booking",
            "Schedule Note": "Hub lists Puerto Plata calls without inventing pier splits",
            "City Access": "Available from both with different transfer times",
            "Return Advice": "Prioritise buffer and supplier clarity",
        }
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Amber Cove vs Taino Bay</h2>
  <p class="text-gray-600 text-sm">Both serve Puerto Plata cruise calls. They are <strong>not the same physical arrival</strong>. Confirm which facility your sailing uses before you book a meeting point.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-white"><div class="max-w-4xl mx-auto px-4">
  <div class="overflow-x-auto rounded-3xl border border-dr-100 shadow-sm">
    <table class="w-full text-sm text-left min-w-[640px]">
      <thead class="bg-ocean-800 text-white"><tr>
        <th class="py-4 px-4 font-semibold">Factor</th>
        <th class="py-4 px-4 font-semibold">Amber Cove</th>
        <th class="py-4 px-4 font-semibold">Taino Bay</th>
      </tr></thead>
      <tbody class="bg-white">
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Location</td><td class="py-4 px-4 text-gray-600">Maimón area, west of Puerto Plata city</td><td class="py-4 px-4 text-gray-600">Closer to downtown Puerto Plata</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Terminal character</td><td class="py-4 px-4 text-gray-600">Purpose-built cruise village with controlled guest zone</td><td class="py-4 px-4 text-gray-600">Modern terminal nearer city streets - different walking distances</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Excursion pickup</td><td class="py-4 px-4 text-gray-600">Usually coordinated inside or at designated gates</td><td class="py-4 px-4 text-gray-600">Meeting points vary - confirm exact assembly area</td></tr>
        <tr class="border-b border-dr-100"><td class="py-4 px-4 font-semibold text-gray-900">Ship schedule on this site</td><td class="py-4 px-4 text-gray-600" colspan="2">Listed as Puerto Plata calls. We do not invent which facility each sailing uses - check cruise documents.</td></tr>
        <tr><td class="py-4 px-4 font-semibold text-gray-900">Which port does my ship use?</td><td class="py-4 px-4 text-gray-600" colspan="2">Check cruise documents, ship app or daily newsletter. Booking the wrong pickup is the most common Puerto Plata shore-excursion mistake.</td></tr>
      </tbody>
    </table>
  </div>
  <p class="mt-8 text-sm text-gray-600">Damajagua, beach breaks, city tours and catamarans can work from either facility when the supplier supports your pickup. Quality depends more on operator clarity than which pier you use.</p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>
{concierge_panel()}"""


def legal_about() -> str:
    return f"""<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">About {SITE}</h2>
  <p class="text-gray-600 leading-relaxed mb-4">Puerto Plata cruise days often come down to Damajagua versus beach time, with an important logistics wrinkle: Amber Cove and Taino Bay are different arrival facilities. This site exists to keep that distinction honest.</p>
  <p class="text-gray-600 leading-relaxed mb-4">We are not a cruise line, ticket marketplace or port authority. Ship schedules sync from the Caribbean Shore Excursions authority import for Puerto Plata only - without inventing a pier split.</p>
  <p class="text-gray-600 leading-relaxed mb-8">Network context: <a href="https://caribbeanshoreexcursion.com/" class="text-ocean-600 font-medium">Caribbean Shore Excursions</a>.</p>
  {internal_links()}
</div></section>
{concierge_panel()}"""


def legal_contact() -> str:
    return f"""<section class="pt-10 pb-8 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Contact</h2>
  <p class="text-gray-600 leading-relaxed mb-4">Include your ship, call date, Amber Cove or Taino Bay if known, and whether you prefer Damajagua, beach or city sightseeing.</p>
  <p class="text-gray-600 leading-relaxed mb-6"><a class="text-ocean-600 font-semibold" href="mailto:hello@puertoplatacruiseexcursion.com">hello@puertoplatacruiseexcursion.com</a>. Planning concierge, not a booking desk.</p>
  {internal_links()}
</div></section>
{concierge_panel()}"""


def legal_privacy() -> str:
    return """<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Privacy</h2>
  <p class="text-gray-600 leading-relaxed mb-4">This is a static planning website. We do not operate a booking engine, payment system or passenger account database in this phase.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Messages to hello@puertoplatacruiseexcursion.com are used only to respond about Puerto Plata port-day planning.</p>
  <p class="text-gray-600 leading-relaxed">We do not add analytics trackers in this build. If practices change, this page will be updated first.</p>
</div></section>"""


def legal_terms() -> str:
    return """<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Terms of use</h2>
  <p class="text-gray-600 leading-relaxed mb-4">Content is for general planning. It is not a contract of carriage, not travel insurance, and not a guarantee of excursion availability, weather or on-time return.</p>
  <p class="text-gray-600 leading-relaxed mb-4">Confirm arrangements with your cruise line and operators. Amber Cove and Taino Bay logistics can change - verify your facility.</p>
  <p class="text-gray-600 leading-relaxed">You are responsible for leaving enough time to reboard and for following local activity rules.</p>
</div></section>"""


def legal_methodology() -> str:
    return f"""<section class="pt-10 pb-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">How we assess Puerto Plata excursions</h2>
  <p class="text-gray-600 leading-relaxed mb-4">We weigh call length, facility logistics, transfer time and return buffer - not marketplace noise.</p>
  <div class="space-y-4 text-sm text-gray-600 mb-8">
    <div class="bg-dr-50 rounded-2xl p-5 border border-dr-100"><h3 class="font-display font-bold text-gray-900 mb-2">Facility honesty</h3><p>Amber Cove and Taino Bay are different arrivals. We do not invent pier assignments in the schedule hub.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-5 border border-ocean-100"><h3 class="font-display font-bold text-gray-900 mb-2">Decision clarity</h3><p>Waterfalls versus beach, city versus sand - passengers need trade-offs, not invented crowd or price claims.</p></div>
    <div class="bg-dr-50 rounded-2xl p-5 border border-dr-100"><h3 class="font-display font-bold text-gray-900 mb-2">Schedule integrity</h3><p>Call lists come from the Caribbean authority import for Puerto Plata, then QA-checked before pages are built.</p></div>
  </div>
  {internal_links()}
</div></section>
{concierge_panel()}"""


def merge_sitemap(extra: list[tuple[str, str, str]]) -> None:
    sitemap_path = ROOT / "sitemap.xml"
    by_path: dict[str, tuple[str, str]] = {}
    if sitemap_path.exists():
        text = sitemap_path.read_text(encoding="utf-8")
        locs = re.findall(r"<loc>(.*?)</loc>", text)
        freqs = re.findall(r"<changefreq>(.*?)</changefreq>", text)
        pris = re.findall(r"<priority>(.*?)</priority>", text)
        for i, loc in enumerate(locs):
            path = loc.replace(DOMAIN + "/", "").replace(DOMAIN, "")
            if path == "/":
                path = ""
            by_path[path] = (
                pris[i] if i < len(pris) else "0.5",
                freqs[i] if i < len(freqs) else "monthly",
            )
    for path, pri, freq in extra:
        by_path[path] = (pri, freq)
    frag = ROOT / "data" / "generated" / "schedule-sitemap.json"
    if frag.exists():
        try:
            for path, pri, freq in json.loads(frag.read_text(encoding="utf-8")):
                by_path[path] = (pri, freq)
        except json.JSONDecodeError:
            pass
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, (pri, freq) in sorted(by_path.items(), key=lambda x: (x[0] != "", x[0])):
        url = f"{DOMAIN}/{path}" if path else f"{DOMAIN}/"
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


def write_package_json() -> None:
    # Phase 33B: preserve Pages deploy path; do not overwrite package.json.
    return


def ensure_decision_css() -> None:
    css_path = ROOT / "css" / "site.css"
    css = css_path.read_text(encoding="utf-8")
    if ".decision-grid" not in css:
        css += """
.section-label { display: inline-flex; align-items: center; gap: 0.5rem; color: #2563eb; font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.75rem; }
.decision-grid { display: grid; gap: 1rem; }
@media (min-width: 640px) { .decision-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .decision-grid { grid-template-columns: repeat(3, 1fr); } }
.decision-card { background: #fff; border: 1px solid #dbeafe; border-radius: 1.25rem; padding: 1.25rem 1.35rem; }
.decision-card h3 { font-size: 1.05rem; margin-bottom: 0.4rem; }
.decision-card p { font-size: 0.875rem; color: #4b5563; line-height: 1.55; margin-bottom: 0.75rem; }
.concierge-panel { background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 55%, #d97706 100%); border-radius: 1.5rem; padding: 2rem; color: #fff; }
"""
        css_path.write_text(css, encoding="utf-8")
        print("  updated css/site.css")


def main() -> None:
    print("World 2.0 extending Puerto Plata Cruise Excursion…")
    ensure_decision_css()
    write_nav()
    write_footer()
    write(
        "partials/hero-home.html",
        hero(
            eyebrow="Dominican Republic · Puerto Plata",
            title_html='Puerto Plata<br/><span class="text-amber-300">Cruise Excursion</span>',
            lead="Confirm Amber Cove or Taino Bay, then choose Damajagua waterfalls, a beach break or city sightseeing around a realistic return window.",
            image="hero-puerto-plata.png",
            aria="Puerto Plata cruise shore excursion planning hero",
            actions=(
                '<a href="puerto-plata-waterfalls-vs-beach.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Waterfalls or beach?</a>'
                '<a href="ship-schedule/" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Find your ship</a>'
            ),
            tags=(
                '<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Damajagua</span>'
                '<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Beach</span>'
                '<span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Amber Cove vs Taino Bay</span>'
            ),
        ),
    )
    write(
        "partials/hero-waterfalls-vs-beach.html",
        hero(
            breadcrumb="Waterfalls vs Beach",
            eyebrow="Puerto Plata decision",
            title_html='Waterfalls vs<br/><span class="text-amber-300">Beach</span>',
            lead="Damajagua intensity versus a calmer beach break - choose how to spend a Puerto Plata cruise call.",
            image="damajagua-waterfalls.png",
            aria="Damajagua waterfalls versus beach decision for Puerto Plata cruise passengers",
        ),
    )
    write(
        "partials/hero-amber-vs-taino.html",
        hero(
            breadcrumb="Amber Cove vs Taino Bay",
            eyebrow="Arrival facilities",
            title_html='Amber Cove vs<br/><span class="text-amber-300">Taino Bay</span>',
            lead="Two Puerto Plata-area cruise facilities - confirm yours before booking pickups. We do not invent which ships use which pier.",
            image="amber-cove-taino-bay.png",
            aria="Amber Cove and Taino Bay cruise port facilities near Puerto Plata",
        ),
    )
    write("content/home.html", content_home())
    write("content/puerto-plata-waterfalls-vs-beach.html", content_waterfalls_vs_beach())
    write("content/amber-cove-vs-taino-bay.html", content_amber())
    write("content/about.html", legal_about())
    write("content/contact.html", legal_contact())
    write("content/privacy.html", legal_privacy())
    write("content/terms.html", legal_terms())
    write("content/methodology.html", legal_methodology())
    soft_all_content()

    for filename, title, desc, kw, canon, page, hero_f, content_f, preload in [
        (
            "puerto-plata-waterfalls-vs-beach.html",
            "Puerto Plata Waterfalls vs Beach | Cruise Decision",
            "Compare Damajagua waterfalls with a Puerto Plata beach break on a cruise call - honest trade-offs for Amber Cove and Taino Bay guests.",
            "Puerto Plata waterfalls vs beach, Damajagua vs beach, cruise decision",
            "puerto-plata-waterfalls-vs-beach.html",
            "excursions",
            "partials/hero-waterfalls-vs-beach.html",
            "content/puerto-plata-waterfalls-vs-beach.html",
            "damajagua-waterfalls.png",
        ),
        (
            "about.html",
            "About Puerto Plata Cruise Excursion",
            "About Puerto Plata Cruise Excursion - independent planning for Amber Cove and Taino Bay cruise calls.",
            "about Puerto Plata Cruise Excursion",
            "about.html",
            "contact",
            "partials/hero-port-guide.html",
            "content/about.html",
            "puerto-plata-port.png",
        ),
        (
            "contact.html",
            "Contact Puerto Plata Cruise Excursion",
            "Contact hello@puertoplatacruiseexcursion.com for Puerto Plata port-day planning help.",
            "contact Puerto Plata Cruise Excursion",
            "contact.html",
            "contact",
            "partials/hero-port-guide.html",
            "content/contact.html",
            "puerto-plata-port.png",
        ),
        (
            "privacy.html",
            "Privacy | Puerto Plata Cruise Excursion",
            "Privacy policy for Puerto Plata Cruise Excursion.",
            "privacy Puerto Plata",
            "privacy.html",
            "contact",
            "partials/hero-port-guide.html",
            "content/privacy.html",
            "puerto-plata-port.png",
        ),
        (
            "terms.html",
            "Terms of Use | Puerto Plata Cruise Excursion",
            "Terms of use for Puerto Plata Cruise Excursion planning content.",
            "terms Puerto Plata",
            "terms.html",
            "contact",
            "partials/hero-port-guide.html",
            "content/terms.html",
            "puerto-plata-port.png",
        ),
        (
            "methodology.html",
            "How We Assess Puerto Plata Excursions",
            "Methodology for assessing Puerto Plata cruise excursions - timing, facility honesty and schedule integrity.",
            "Puerto Plata excursion methodology",
            "methodology.html",
            "contact",
            "partials/hero-port-guide.html",
            "content/methodology.html",
            "puerto-plata-port.png",
        ),
    ]:
        shell(
            filename=filename,
            title=title,
            description=desc,
            keywords=kw,
            canonical=f"{DOMAIN}/{canon}",
            preload=preload,
            page=page,
            hero_file=hero_f,
            content_file=content_f,
            ld_json={
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title,
                "url": f"{DOMAIN}/{canon}",
            },
        )

    shell(
        filename="index.html",
        title=f"{SITE} | Damajagua, Beach &amp; Two Ports",
        description="Independent Puerto Plata cruise excursion planning - Damajagua waterfalls, beach breaks, city tours, and honest Amber Cove versus Taino Bay logistics.",
        keywords="Puerto Plata cruise excursions, Amber Cove, Taino Bay, Damajagua, Dominican Republic shore excursions",
        canonical=f"{DOMAIN}/",
        preload="hero-puerto-plata.png",
        page="home",
        hero_file="partials/hero-home.html",
        content_file="content/home.html",
        ld_json={
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE,
            "url": f"{DOMAIN}/",
        },
    )
    shell(
        filename="amber-cove-vs-taino-bay.html",
        title="Amber Cove vs Taino Bay | Puerto Plata Cruise Ports",
        description="Honest Amber Cove versus Taino Bay comparison for Puerto Plata cruise passengers - different facilities, confirm pickup before booking.",
        keywords="Amber Cove vs Taino Bay, Puerto Plata cruise ports, Amber Cove Taino Bay difference",
        canonical=f"{DOMAIN}/amber-cove-vs-taino-bay.html",
        preload="amber-cove-taino-bay.png",
        page="ports",
        hero_file="partials/hero-amber-vs-taino.html",
        content_file="content/amber-cove-vs-taino-bay.html",
        ld_json={
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Amber Cove vs Taino Bay",
            "url": f"{DOMAIN}/amber-cove-vs-taino-bay.html",
        },
    )

    merge_sitemap(
        [
            ("puerto-plata-waterfalls-vs-beach.html", "0.8", "monthly"),
            ("about.html", "0.5", "yearly"),
            ("contact.html", "0.5", "yearly"),
            ("privacy.html", "0.3", "yearly"),
            ("terms.html", "0.3", "yearly"),
            ("methodology.html", "0.5", "yearly"),
        ]
    )
    write_package_json()
    print("World 2.0 extend done.")


if __name__ == "__main__":
    main()
