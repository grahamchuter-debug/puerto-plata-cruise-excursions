#!/usr/bin/env python3
"""Bake Puerto Plata pages: server-visible HTML, extensionless apex canonicals, Pages 404.

Run after build-puerto-plata-site.py, world2_extend_puerto_plata.py, generate_schedule_pages.py.
Phase 33B — Pages hosting only; do not create a Worker. Do not touch other destinations.
"""
from __future__ import annotations

import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://puertoplatacruiseexcursion.com"
SITE = "Puerto Plata Cruise Excursion"
EMAIL = "hello@puertoplatacruiseexcursion.com"
TODAY = date.today().isoformat()
FONTS = (
    "https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700"
    "&family=Source+Sans+3:wght@400;500;600;700&display=swap"
)
HERO_CSS = (
    "linear-gradient(135deg, rgba(12, 74, 110, 0.94) 0%, "
    "rgba(14, 116, 144, 0.78) 48%, rgba(180, 83, 9, 0.58) 100%)"
)

# Verified-safe local assets only (no alpine/Nassau/macaque/desert contamination).
SAFE_IMAGES = {
    "puerto-plata-beach.png",  # AMBER: generic tropical beach
    "beach-loungers.png",
    "catamaran-snorkel.png",
    "snorkel-caribbean.png",
    "waterfall-pools.png",
}

RED_IMAGES = {
    "hero-puerto-plata.png",
    "damajagua-waterfalls.png",
    "amber-cove-taino-bay.png",
    "puerto-plata-city.png",
    "puerto-plata-port.png",
    "monkeyland.png",
    # Additional wrong-destination stock discovered in 33B
    "best-puerto-plata-excursions.png",
    "puerto-plata-intro.png",
    "colonial-street.png",
    "one-day-puerto-plata.png",
    "monkeys-interaction.png",
}

FORBIDDEN_SCHEMA = {
    "TouristTrip",
    "TouristInformationCenter",
    "LocalBusiness",
    "TravelAgency",
    "Product",
    "Offer",
}

PAGES: dict[str, dict] = {
    "index.html": {
        "slug": "",
        "page": "home",
        "hero": "partials/hero-home.html",
        "trust": "partials/trust-strip.html",
        "content": "content/home.html",
        "og_image": None,
        "schema": "home",
    },
    "best-puerto-plata-shore-excursions.html": {
        "slug": "best-puerto-plata-shore-excursions",
        "page": "excursions",
        "hero": "partials/hero-best-excursions.html",
        "content": "content/best-puerto-plata-shore-excursions.html",
        "og_image": None,
        "schema": "faq",
    },
    "damajagua-waterfalls-shore-excursion-puerto-plata.html": {
        "slug": "damajagua-waterfalls-shore-excursion-puerto-plata",
        "page": "damajagua",
        "hero": "partials/hero-damajagua.html",
        "content": "content/damajagua-waterfalls-shore-excursion-puerto-plata.html",
        "og_image": None,
        "schema": "article",
    },
    "amber-cove-vs-taino-bay.html": {
        "slug": "amber-cove-vs-taino-bay",
        "page": "ports",
        "hero": "partials/hero-amber-vs-taino.html",
        "content": "content/amber-cove-vs-taino-bay.html",
        "og_image": None,
        "schema": "webpage",
    },
    "puerto-plata-cruise-port-guide.html": {
        "slug": "puerto-plata-cruise-port-guide",
        "page": "port",
        "hero": "partials/hero-port-guide.html",
        "content": "content/puerto-plata-cruise-port-guide.html",
        "og_image": None,
        "schema": "webpage",
    },
    "puerto-plata-city-tour.html": {
        "slug": "puerto-plata-city-tour",
        "page": "citytour",
        "hero": "partials/hero-city-tour.html",
        "content": "content/puerto-plata-city-tour.html",
        "og_image": None,
        "schema": "article",
    },
    "puerto-plata-beach-break.html": {
        "slug": "puerto-plata-beach-break",
        "page": "beach",
        "hero": "partials/hero-beach-break.html",
        "content": "content/puerto-plata-beach-break.html",
        "og_image": "images/puerto-plata-beach.png",
        "schema": "article",
        "hero_image": "images/puerto-plata-beach.png",
        "hero_aria": "Generic tropical beach scene used as relaxed cruise-day beach-break context",
    },
    "monkeyland-shore-excursion-puerto-plata.html": {
        "slug": "monkeyland-shore-excursion-puerto-plata",
        "page": "monkeyland",
        "hero": "partials/hero-monkeyland.html",
        "content": "content/monkeyland-shore-excursion-puerto-plata.html",
        "og_image": None,
        "schema": "article",
    },
    "catamaran-snorkel-puerto-plata.html": {
        "slug": "catamaran-snorkel-puerto-plata",
        "page": "catamaran",
        "hero": "partials/hero-catamaran.html",
        "content": "content/catamaran-snorkel-puerto-plata.html",
        "og_image": "images/catamaran-snorkel.png",
        "schema": "article",
        "hero_image": "images/catamaran-snorkel.png",
        "hero_aria": "Underwater Caribbean reef scene for catamaran and snorkel planning context",
    },
    "one-day-in-puerto-plata-from-a-cruise-ship.html": {
        "slug": "one-day-in-puerto-plata-from-a-cruise-ship",
        "page": "oneday",
        "hero": "partials/hero-one-day.html",
        "content": "content/one-day-in-puerto-plata-from-a-cruise-ship.html",
        "og_image": None,
        "schema": "webpage",
    },
    "is-puerto-plata-worth-visiting.html": {
        "slug": "is-puerto-plata-worth-visiting",
        "page": "worth",
        "hero": "partials/hero-worth-visiting.html",
        "content": "content/is-puerto-plata-worth-visiting.html",
        "og_image": None,
        "schema": "faq",
    },
    "puerto-plata-waterfalls-vs-beach.html": {
        "slug": "puerto-plata-waterfalls-vs-beach",
        "page": "compare",
        "hero": "partials/hero-waterfalls-vs-beach.html",
        "content": "content/puerto-plata-waterfalls-vs-beach.html",
        "og_image": None,
        "schema": "webpage",
    },
    "about.html": {
        "slug": "about",
        "page": "about",
        "hero": "partials/hero-about.html",
        "content": "content/about.html",
        "og_image": None,
        "main_class": "pt-16",
        "schema": "webpage",
    },
    "contact.html": {
        "slug": "contact",
        "page": "contact",
        "hero": "partials/hero-contact.html",
        "content": "content/contact.html",
        "og_image": None,
        "main_class": "pt-16",
        "schema": "webpage",
    },
    "methodology.html": {
        "slug": "methodology",
        "page": "methodology",
        "hero": "partials/hero-methodology.html",
        "content": "content/methodology.html",
        "og_image": None,
        "main_class": "pt-16",
        "schema": "webpage",
    },
    "privacy.html": {
        "slug": "privacy",
        "page": "privacy",
        "hero": "partials/hero-privacy.html",
        "content": "content/privacy.html",
        "og_image": None,
        "main_class": "pt-16",
        "schema": "webpage",
    },
    "terms.html": {
        "slug": "terms",
        "page": "terms",
        "hero": "partials/hero-terms.html",
        "content": "content/terms.html",
        "og_image": None,
        "main_class": "pt-16",
        "schema": "webpage",
    },
    "404.html": {
        "slug": "404",
        "page": "404",
        "content": "content/404.html",
        "og_image": None,
        "main_class": "pt-16",
        "noindex": True,
        "canonical_override": f"{DOMAIN}/404",
        "schema": None,
    },
}

PRIORITY = {
    "": 1.0,
    "best-puerto-plata-shore-excursions": 0.9,
    "damajagua-waterfalls-shore-excursion-puerto-plata": 0.9,
    "monkeyland-shore-excursion-puerto-plata": 0.8,
    "puerto-plata-city-tour": 0.8,
    "puerto-plata-beach-break": 0.8,
    "catamaran-snorkel-puerto-plata": 0.8,
    "amber-cove-vs-taino-bay": 0.8,
    "puerto-plata-cruise-port-guide": 0.8,
    "one-day-in-puerto-plata-from-a-cruise-ship": 0.8,
    "is-puerto-plata-worth-visiting": 0.7,
    "puerto-plata-waterfalls-vs-beach": 0.7,
}

EDITORIAL_SLUGS = [
    m["slug"] for m in PAGES.values() if m["slug"] and m["slug"] != "404"
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {rel}")


def canon_url(slug: str) -> str:
    if slug == "404":
        return f"{DOMAIN}/404"
    if not slug:
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{slug}"


def extensionlessify_html(html: str) -> str:
    def repl(m: re.Match) -> str:
        attr, quote, url = m.group(1), m.group(2), m.group(3)
        if url.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            return m.group(0)
        if url.startswith(("images/", "/images/", "css/", "/css/", "js/", "/js/")):
            if not url.startswith("/") and not url.startswith("http"):
                return f"{attr}={quote}/{url}{quote}"
            return m.group(0)
        parts = urlsplit(url)
        path = parts.path
        if path.endswith(".html"):
            if path.endswith("index.html"):
                path = path[: -len("index.html")] or "/"
            else:
                path = path[: -len(".html")]
            if path in ("", "index") or path.endswith("/index"):
                path = "/"
        if path == "index" or path == "":
            path = "/"
        if not path.startswith("/"):
            path = "/" + path
        if len(path) > 1 and path.endswith("/"):
            # Keep ship-schedule directory trailing slash convention
            if not path.startswith("/ship-schedule"):
                path = path.rstrip("/") or "/"
        rebuilt = path
        if parts.query:
            rebuilt += "?" + parts.query
        if parts.fragment:
            rebuilt += "#" + parts.fragment
        return f"{attr}={quote}{rebuilt}{quote}"

    html = re.sub(r'(href|action)=([\'"])([^\'"]+)\2', repl, html)
    html = re.sub(
        r"""(\b(?:src|href)=)(['"])(?!/|https?:|mailto:|tel:|#|data:)(images/|css/|js/)([^'"]+)\2""",
        lambda m: f"{m.group(1)}{m.group(2)}/{m.group(3)}{m.group(4)}{m.group(2)}",
        html,
    )
    html = re.sub(
        r"""url\((['"]?)(?!/|https?:)(images/[^)'"]+)\1\)""",
        lambda m: f"url({m.group(1)}/{m.group(2)}{m.group(1)})",
        html,
    )
    return html


def strip_forbidden_schema(obj):
    if isinstance(obj, dict):
        t = obj.get("@type")
        types = t if isinstance(t, list) else ([t] if t else [])
        if any(x in FORBIDDEN_SCHEMA for x in types):
            return None
        # Drop provider Organization blocks
        if "provider" in obj:
            del obj["provider"]
        cleaned = {}
        for k, v in obj.items():
            nv = strip_forbidden_schema(v)
            if nv is not None:
                cleaned[k] = nv
        return cleaned
    if isinstance(obj, list):
        out = []
        for item in obj:
            ni = strip_forbidden_schema(item)
            if ni is not None:
                out.append(ni)
        return out
    return obj


def faq_schema_from_content(content_html: str) -> dict | None:
    entities = []
    for m in re.finditer(
        r"<details[^>]*>\s*<summary[^>]*>(.*?)</summary>\s*<p[^>]*>(.*?)</p>",
        content_html,
        re.S | re.I,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1))
        a = re.sub(r"<[^>]+>", "", m.group(2))
        q = re.sub(r"\s+", " ", q).strip()
        a = re.sub(r"\s+", " ", a).strip()
        if q and a:
            entities.append(
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
            )
    if not entities:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}


def build_schema(meta: dict, title: str, description: str, content_html: str) -> str | None:
    kind = meta.get("schema")
    if not kind:
        return None
    canon = canon_url(meta["slug"])
    if kind == "home":
        graph = [
            {
                "@type": "WebSite",
                "name": SITE,
                "url": f"{DOMAIN}/",
                "description": description,
            },
            {
                "@type": "WebPage",
                "name": title,
                "url": canon,
                "description": description,
                "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
            },
        ]
        faq = faq_schema_from_content(content_html)
        if faq:
            graph.append({"@type": "FAQPage", "mainEntity": faq["mainEntity"]})
        return json.dumps(
            {"@context": "https://schema.org", "@graph": graph},
            ensure_ascii=False,
            indent=2,
        )
    if kind == "faq":
        faq = faq_schema_from_content(content_html)
        if faq:
            faq["url"] = canon
            return json.dumps(faq, ensure_ascii=False, indent=2)
        kind = "webpage"
    if kind == "article":
        data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "url": canon,
            "mainEntityOfPage": canon,
            "author": {"@type": "Organization", "name": SITE},
            "publisher": {"@type": "Organization", "name": SITE, "url": f"{DOMAIN}/"},
        }
        # Organization as publisher is fine (not a tour seller); keep
        return json.dumps(data, ensure_ascii=False, indent=2)
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "description": description,
        "url": canon,
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_head(meta: dict, title: str, description: str, schema_json: str | None) -> str:
    if meta.get("canonical_override"):
        url = meta["canonical_override"]
    else:
        url = canon_url(meta["slug"])
    robots = '  <meta name="robots" content="noindex, follow" />\n' if meta.get("noindex") else ""
    og_block = ""
    preload = ""
    if meta.get("og_image"):
        og = f"{DOMAIN}/{meta['og_image'].lstrip('/')}"
        og_block = f'  <meta property="og:image" content="{og}" />\n'
        preload = f'  <link rel="preload" as="image" href="/{meta["og_image"].lstrip("/")}" fetchpriority="high" />\n'
    schema_block = ""
    if schema_json:
        schema_block = f'  <script type="application/ld+json">\n{schema_json}\n  </script>\n'
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
{robots}  <link rel="canonical" href="{url}" />
{preload}  <meta property="og:type" content="website" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
{og_block}  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
{schema_block}  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
"""


def title_desc_from_shell(filename: str, meta: dict) -> tuple[str, str]:
    shell = ROOT / filename
    if shell.exists():
        text = shell.read_text(encoding="utf-8")
        t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        d = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', text, re.I
        )
        title = re.sub(r"\s+", " ", t.group(1)).strip() if t else meta["slug"] or SITE
        desc = d.group(1) if d else ""
        return title, desc
    return SITE, ""


def hero_css_only(aria: str, *, image: str | None = None) -> str:
    if image and Path(image).name in SAFE_IMAGES:
        bg = f"{HERO_CSS}, url('/{image.lstrip('/')}')"
    else:
        bg = HERO_CSS
    return (
        f'<div class="absolute inset-0 hero-bg-custom" style="background-image: {bg};" '
        f'role="img" aria-label="{aria}"></div>'
    )


def rewrite_hero_background(html: str, meta: dict) -> str:
    aria_m = re.search(r'aria-label="([^"]*)"', html)
    aria = aria_m.group(1) if aria_m else f"{SITE} page header"
    # Soften Amber Cove–primary hero framing
    aria = aria.replace("from Amber Cove and Taino Bay", "for Puerto Plata cruise days")
    aria = aria.replace("docking at Amber Cove or Taino Bay", "on a Puerto Plata cruise call")
    image = meta.get("hero_image")
    if meta.get("hero_aria"):
        aria = meta["hero_aria"]
    new_bg = hero_css_only(aria, image=image)
    return re.sub(
        r'<div class="absolute inset-0 hero-bg-custom"[^>]*></div>',
        new_bg,
        html,
        count=1,
    )


def ensure_utility_heroes() -> None:
    heroes = {
        "partials/hero-about.html": (
            "About",
            "Independent Puerto Plata cruise-day planning",
        ),
        "partials/hero-contact.html": (
            "Contact",
            "Planning concierge — not a booking desk",
        ),
        "partials/hero-methodology.html": (
            "Methodology",
            "How we assess Puerto Plata excursion options",
        ),
        "partials/hero-privacy.html": (
            "Privacy",
            "How this planning site handles information",
        ),
        "partials/hero-terms.html": (
            "Terms of use",
            "Planning content — not a booking contract",
        ),
    }
    for path, (h1, lead) in heroes.items():
        html = f"""<section class="site-hero site-hero--compact">
  {hero_css_only(f"{h1} — {SITE}")}
  <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl pt-8 pb-4">
      <h1 class="site-hero__title text-4xl sm:text-5xl font-display font-bold text-white leading-tight mb-3">{h1}</h1>
      <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed max-w-2xl">{lead}</p>
    </div>
  </div>
  <div class="absolute bottom-0 left-0 right-0"><svg viewBox="0 0 1440 48" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" class="site-hero__wave" aria-hidden="true"><path d="M0 24 C360 48 1080 0 1440 24 L1440 48 L0 48 Z" fill="white"/></svg></div>
</section>
"""
        write(path, html)


def ensure_404_content() -> None:
    write(
        "content/404.html",
        """<section class="pt-10 pb-20 bg-white">
  <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
    <p class="section-label mx-auto mb-3">404</p>
    <h1 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">Page not found</h1>
    <p class="text-gray-600 leading-relaxed mb-8">That URL is not part of the Puerto Plata cruise excursion planning guide. Try the home page, best excursions list, or ship schedule.</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="/" class="btn-ocean inline-flex items-center justify-center text-white font-semibold px-6 py-3 rounded-full text-sm no-underline">Puerto Plata home</a>
      <a href="/best-puerto-plata-shore-excursions" class="btn-outline inline-flex items-center justify-center font-semibold px-6 py-3 rounded-full text-sm no-underline border border-ocean-600 text-ocean-700">Best excursions</a>
      <a href="/ship-schedule/" class="btn-outline inline-flex items-center justify-center font-semibold px-6 py-3 rounded-full text-sm no-underline border border-ocean-600 text-ocean-700">Ship schedule</a>
    </div>
  </div>
</section>
""",
    )


def ensure_nav_mobile() -> None:
    nav_path = ROOT / "partials" / "nav.html"
    nav = nav_path.read_text(encoding="utf-8")
    if 'id="menu-toggle"' not in nav:
        nav = nav.replace(
            '<button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">',
            '<button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" id="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">',
        )
    if 'id="mobile-menu"' not in nav:
        mobile = """
    <div id="mobile-menu" class="hidden lg:hidden pb-4 border-t border-dr-100">
      <div class="flex flex-col gap-3 pt-3 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-ocean-600">Home</a>
        <a href="best-puerto-plata-shore-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-ocean-600">Excursions</a>
        <a href="damajagua-waterfalls-shore-excursion-puerto-plata.html" data-nav="damajagua" class="text-gray-600 hover:text-ocean-600">Damajagua</a>
        <a href="amber-cove-vs-taino-bay.html" data-nav="ports" class="text-gray-600 hover:text-ocean-600">Amber Cove vs Taino Bay</a>
        <a href="ship-schedule/" data-nav="schedule" class="text-gray-600 hover:text-ocean-600">Ship Schedule</a>
        <a href="puerto-plata-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-ocean-600">Port Guide</a>
        <a href="contact.html" data-nav="contact" class="text-gray-600 hover:text-ocean-600">Contact</a>
      </div>
    </div>
"""
        nav = nav.replace("    </div>\n  </div>\n</nav>", f"    </div>{mobile}  </div>\n</nav>")
    nav_path.write_text(nav, encoding="utf-8")
    print("  patched partials/nav.html")


def remove_bad_images_from_html(html: str) -> str:
    """Drop or neutralize RED/wrong img tags; prefer no image to wrong image."""

    def repl_img(m: re.Match) -> str:
        tag = m.group(0)
        src_m = re.search(r'src=["\']([^"\']+)["\']', tag)
        if not src_m:
            return tag
        name = Path(src_m.group(1)).name
        if name in SAFE_IMAGES:
            return tag
        alt_m = re.search(r'alt=["\']([^"\']*)["\']', tag)
        aria = alt_m.group(1) if alt_m else "Puerto Plata cruise planning"
        return (
            f'<div class="w-full h-full min-h-[10rem] bg-gradient-to-br from-sky-900 via-cyan-800 to-amber-700" '
            f'role="img" aria-label="{aria}"></div>'
        )

    html = re.sub(r"<img\b[^>]*>", repl_img, html, flags=re.I)
    # Remove url() references to RED assets in inline styles
    for bad in RED_IMAGES:
        html = re.sub(
            rf""",\s*url\(['"]?(?:/?images/)?{re.escape(bad)}['"]?\)""",
            "",
            html,
        )
        html = re.sub(
            rf"""url\(['"]?(?:/?images/)?{re.escape(bad)}['"]?\)""",
            HERO_CSS,
            html,
        )
    return html


def hygiene_content(html: str, slug: str) -> str:
    """Light claim / template / AC-boundary hygiene while touching pages."""
    reps = [
        (
            r"Official taxis are available at both terminals; agree the fare before departing\.",
            "Taxis are commonly available at both terminals; agree the fare before departing.",
        ),
        (r"Official taxis", "Terminal taxis"),
        (r"Cruise-friendly timing", "Cruise-day pacing"),
        (r"cruise-friendly return timing", "return-window planning"),
        (r"cruise-friendly", "cruise-day"),
        (
            r"Pickup guidance for Amber Cove and Taino Bay",
            "Confirm pickup for your arrival facility",
        ),
        (
            r"Clear return-to-ship advice",
            "Plan your own return window",
        ),
        (
            r"Local destination knowledge",
            "Destination-level planning notes",
        ),
        (
            r"Good options for families, couples and groups",
            "Works for mixed traveler groups when the day matches fitness",
        ),
        (
            r"Everything cruise travelers need to know about docking at Amber Cove or Taino Bay and planning excursions with confidence\.",
            "Puerto Plata cruise-day orientation: two arrival facilities, city access, and how to choose one core plan.",
        ),
        (
            r"<strong>Amber Cove</strong> is a purpose-built cruise port with shops, pools and a controlled guest zone\s+-\s+excursion pickups are usually coordinated inside or just outside the terminal\.",
            "<strong>Amber Cove</strong> (west of the city, in Maimón) is one of two Puerto Plata-area arrival facilities — treat it as a logistics checkpoint, not the destination identity of this site.",
        ),
        (
            r"<strong>Taino Bay</strong> sits nearer the historic city and has a different terminal layout and meeting-point flow\. Same destination, different pickup logistics\.",
            "<strong>Taino Bay</strong> sits nearer central Puerto Plata with a different meeting-point flow. Same destination region; different pickup logistics.",
        ),
        (
            r"<strong>Amber Cove</strong> is about 11 km \(7 miles\) west in Maimón, typically 15-25 minutes by road depending on traffic\.",
            "<strong>Amber Cove</strong> is about 11 km (7 miles) west in Maimón — plan on roughly 15–25 minutes by road as approximate context only (traffic varies).",
        ),
        (
            r"<strong>Taino Bay</strong> is roughly 1-2 km from central Puerto Plata\s+-\s+a short taxi or tour transfer\.",
            "<strong>Taino Bay</strong> is roughly 1–2 km from central Puerto Plata as approximate planning context — a short taxi or tour transfer when traffic allows.",
        ),
        (
            r"Return To Ship Confidence</dt><dd>High with guided timing",
            "Return Window</dt><dd>Confirm with your operator",
        ),
        (
            r"Return To Ship Confidence</dt><dd>High with cruise-aware operators",
            "Return Window</dt><dd>Confirm with your operator",
        ),
        (
            r"Sample Puerto Plata day plans for cruise guests arriving at Amber Cove or Taino Bay\.",
            "Sample Puerto Plata day plans for cruise guests — confirm which facility your sailing uses.",
        ),
    ]
    for old, new in reps:
        html = re.sub(old, new, html, flags=re.I)

    if slug in (
        "puerto-plata-city-tour",
        "damajagua-waterfalls-shore-excursion-puerto-plata",
        "best-puerto-plata-shore-excursions",
    ):
        html = html.replace(
            "from Amber Cove and Taino Bay",
            "from either Puerto Plata-area arrival facility",
        )
        html = html.replace(
            "for cruise visitors from Amber Cove and Taino Bay",
            "for Puerto Plata cruise visitors",
        )
    return html


def patch_source_heroes() -> None:
    for path in (ROOT / "partials").glob("hero-*.html"):
        if path.name.startswith("hero-about") or path.name in {
            "hero-contact.html",
            "hero-methodology.html",
            "hero-privacy.html",
            "hero-terms.html",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        # Map filename to page meta for hero_image
        meta = {"hero_image": None, "hero_aria": None}
        for m in PAGES.values():
            if m.get("hero") == f"partials/{path.name}":
                meta = m
                break
        text = rewrite_hero_background(text, meta)
        path.write_text(text, encoding="utf-8")
        print(f"  hero CSS hygiene {path.name}")


def patch_content_sources() -> None:
    for path in (ROOT / "content").glob("*.html"):
        if path.name == "404.html":
            continue
        slug = path.stem
        text = path.read_text(encoding="utf-8")
        text = remove_bad_images_from_html(text)
        text = hygiene_content(text, slug)
        path.write_text(text, encoding="utf-8")
        print(f"  content hygiene {path.name}")


def remove_red_image_files() -> None:
    for name in RED_IMAGES:
        p = ROOT / "images" / name
        if p.exists():
            p.unlink()
            print(f"  removed images/{name}")


def assemble_page(filename: str, meta: dict) -> str:
    nav = extensionlessify_html(read("partials/nav.html"))
    footer = extensionlessify_html(read("partials/footer.html"))
    hero = ""
    if meta.get("hero"):
        hero = extensionlessify_html(rewrite_hero_background(read(meta["hero"]), meta))
    trust = extensionlessify_html(read(meta["trust"])) if meta.get("trust") else ""
    content = extensionlessify_html(
        hygiene_content(remove_bad_images_from_html(read(meta["content"])), meta["slug"])
    )
    title, description = title_desc_from_shell(filename, meta)
    if meta["slug"] == "404":
        title = f"Page not found | {SITE}"
        description = f"The requested {SITE} page was not found."
    # Soften homepage title away from Amber Cove–primary branding if present
    if meta["slug"] == "" and "Excursions from Amber Cove" in title:
        title = "Puerto Plata Cruise Excursion | Damajagua, Beach & Two Ports"

    schema_json = build_schema(meta, title, description, content)
    main_class = meta.get("main_class", "")
    main_attr = f' class="{main_class}"' if main_class else ""
    body = f"""<body class="bg-white text-gray-800 antialiased" data-page="{meta["page"]}" data-static="1">
  <div id="site-nav" data-inlined="true">{nav}</div>
  <div id="page-hero" data-inlined="true">{hero}</div>
  <div id="page-trust-strip" data-inlined="true">{trust}</div>
  <main id="page-content"{main_attr}>{content}</main>
  <div id="site-footer" data-inlined="true">{footer}</div>
  <script src="/js/site.js" defer></script>
</body>
</html>
"""
    return build_head(meta, title, description, schema_json) + body


def bake_schedule_pages() -> None:
    nav = extensionlessify_html(read("partials/nav.html"))
    footer = extensionlessify_html(read("partials/footer.html"))
    for path in (ROOT / "ship-schedule").rglob("index.html"):
        text = path.read_text(encoding="utf-8")
        m_body = re.search(r'<main id="page-content">(.*?)</main>', text, re.S)
        if not m_body:
            continue
        body_html = m_body.group(1)
        title_m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        desc_m = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', text, re.I
        )
        canon_m = re.search(r'rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', text, re.I)
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else "Ship schedule"
        description = desc_m.group(1) if desc_m else ""
        canon = canon_m.group(1) if canon_m else f"{DOMAIN}/ship-schedule"
        if ".html" in canon:
            canon = canon.replace(".html", "")
        if not canon.startswith(DOMAIN):
            canon = DOMAIN + (canon if canon.startswith("/") else "/" + canon)
        html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canon}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="/js/tailwind-config.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body class="bg-white text-gray-800 antialiased" data-page="schedule" data-static="1">
  <div id="site-nav" data-inlined="true">{nav}</div>
  <main id="page-content">{body_html}</main>
  <div id="site-footer" data-inlined="true">{footer}</div>
  <script src="/js/site.js" defer></script>
  <script src="/js/schedule-search.js" defer></script>
</body>
</html>
"""
        html = extensionlessify_html(html)
        path.write_text(html, encoding="utf-8")
        print(f"  baked {path.relative_to(ROOT)}")


def write_sitemap() -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for _, meta in PAGES.items():
        if meta.get("noindex") or meta["slug"] == "404":
            continue
        slug = meta["slug"]
        pri = PRIORITY.get(slug, 0.6)
        loc = canon_url(slug)
        freq = "weekly" if pri >= 0.9 else "monthly"
        if slug in ("about", "contact", "methodology", "privacy", "terms"):
            freq = "yearly"
            pri = 0.5 if slug in ("about", "contact", "methodology") else 0.3
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{pri:.1f}</priority>",
            "  </url>",
        ]

    frag = ROOT / "data" / "generated" / "schedule-sitemap.json"
    schedule_paths: list[str] = []
    if frag.exists():
        try:
            for path, _pri, _freq in json.loads(frag.read_text(encoding="utf-8")):
                schedule_paths.append(path)
        except json.JSONDecodeError:
            pass
    if not schedule_paths:
        schedule_paths = ["ship-schedule"]
        for p in sorted((ROOT / "ship-schedule").rglob("index.html")):
            rel = p.relative_to(ROOT).as_posix().replace("/index.html", "").replace(
                "index.html", ""
            )
            schedule_paths.append(rel)

    seen = set()
    for path in schedule_paths:
        path = path.strip("/")
        if not path or path in seen:
            continue
        seen.add(path)
        pri = 0.8 if path == "ship-schedule" else 0.6
        lines += [
            "  <url>",
            f"    <loc>{DOMAIN}/{path}</loc>",
            f"    <lastmod>{TODAY}</lastmod>",
            f"    <changefreq>{'weekly' if path == 'ship-schedule' else 'monthly'}</changefreq>",
            f"    <priority>{pri:.1f}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")


def write_robots() -> None:
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")


def write_redirects() -> None:
    # First-match wins on Pages — block internals before editorial .html redirects.
    # Do NOT use /*.html splat: it rewrites /content/*.html → /content/* before 404.
    lines = [
        "# Phase 33B — Cloudflare Pages redirects (301 where possible)",
        "/content /404 404",
        "/content/* /404 404",
        "/partials /404 404",
        "/partials/* /404 404",
        "/scripts /404 404",
        "/scripts/* /404 404",
        "/data /404 404",
        "/data/* /404 404",
        "/functions /404 404",
        "/functions/* /404 404",
        "/destination.config.json /404 404",
        "/package.json /404 404",
        "/package-lock.json /404 404",
        "/wrangler.jsonc /404 404",
        "/index.html / 301",
    ]
    for slug in EDITORIAL_SLUGS:
        lines.append(f"/{slug}.html /{slug} 301")
        lines.append(f"/{slug}/ /{slug} 301")
    write("_redirects", "\n".join(lines) + "\n")


def write_pages_middleware() -> None:
    """Pages Function (not a standalone Worker) for www → apex + internal block."""
    write(
        "functions/_middleware.js",
        """/**
 * Cloudflare Pages middleware (part of existing Pages project — not a Worker).
 * - www → apex 301
 * - Block internals even if a prior full-tree deploy left cached objects
 */
const BLOCKED = [
  /^\\/content(\\/|$)/i,
  /^\\/partials(\\/|$)/i,
  /^\\/scripts(\\/|$)/i,
  /^\\/data(\\/|$)/i,
  /^\\/destination\\.config\\.json$/i,
  /^\\/package(-lock)?\\.json$/i,
  /^\\/wrangler\\.jsonc$/i,
];

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.puertoplatacruiseexcursion.com") {
    url.hostname = "puertoplatacruiseexcursion.com";
    return Response.redirect(url.toString(), 301);
  }

  if (BLOCKED.some((re) => re.test(url.pathname))) {
    let body =
      '<!DOCTYPE html><html lang="en-GB"><head><meta charset="UTF-8"/><meta name="robots" content="noindex,follow"/><title>Page not found | Puerto Plata Cruise Excursion</title></head><body><h1>Page not found</h1><p><a href="/">Puerto Plata home</a></p></body></html>';
    let contentType = "text/html; charset=utf-8";
    try {
      if (context.env && context.env.ASSETS) {
        const asset = await context.env.ASSETS.fetch(
          new Request(new URL("/404.html", url.origin), context.request)
        );
        if (asset.ok) {
          body = await asset.text();
          contentType = asset.headers.get("content-type") || contentType;
        }
      }
    } catch (_) {
      /* use fallback body */
    }
    return new Response(body, {
      status: 404,
      headers: {
        "content-type": contentType,
        "cache-control": "private, no-store",
        "x-robots-tag": "noindex, follow",
      },
    });
  }

  return context.next();
}
""",
    )


def update_attribution() -> None:
    write(
        "images/ATTRIBUTION.md",
        """# Image attribution — Puerto Plata

Local project assets under `images/`. Do not scrape OTA galleries. Do not hotlink at runtime.

## Active assets (Phase 33B)

| File | Notes |
|------|-------|
| `puerto-plata-beach.png` | AMBER — generic tropical beach; not asserted as a named Puerto Plata beach |
| `beach-loungers.png` | Generic tropical beach / lounge context |
| `catamaran-snorkel.png` | Generic Caribbean underwater reef context |
| `snorkel-caribbean.png` | Generic ocean wave / marine atmosphere |
| `waterfall-pools.png` | Neutral tropical countryside tree (not Damajagua-specific) |

## Removed in Phase 33B (wrong destination / RED)

`hero-puerto-plata.png`, `damajagua-waterfalls.png`, `amber-cove-taino-bay.png`,
`puerto-plata-city.png`, `puerto-plata-port.png` (Nassau), `monkeyland.png`,
`best-puerto-plata-excursions.png`, `puerto-plata-intro.png`, `colonial-street.png`,
`one-day-puerto-plata.png`, `monkeys-interaction.png`.

Prefer no image to a wrong image. Heroes without a verified photo use intentional CSS gradients.
""",
    )


def package_pages_dist() -> None:
    """Build a clean Pages upload directory (no content/partials/scripts source)."""
    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()

    # Editorial HTML
    for filename in PAGES:
        src = ROOT / filename
        if src.exists():
            shutil.copy2(src, dist / filename)

    for name in ("sitemap.xml", "robots.txt", "_redirects", "404.html"):
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, dist / name)

    for folder in ("css", "js", "ship-schedule"):
        src = ROOT / folder
        if src.exists():
            shutil.copytree(src, dist / folder, dirs_exist_ok=True)

    # Images: only SAFE
    img_out = dist / "images"
    img_out.mkdir()
    for name in SAFE_IMAGES:
        src = ROOT / "images" / name
        if src.exists():
            shutil.copy2(src, img_out / name)
    attr = ROOT / "images" / "ATTRIBUTION.md"
    if attr.exists():
        shutil.copy2(attr, img_out / "ATTRIBUTION.md")

    # Pages Functions
    fn_src = ROOT / "functions"
    if fn_src.exists():
        shutil.copytree(fn_src, dist / "functions", dirs_exist_ok=True)

    print(f"  packaged dist/ ({sum(1 for _ in dist.rglob('*'))} paths)")


def main() -> None:
    print("Assembling Puerto Plata server-visible Pages build…")
    ensure_nav_mobile()
    ensure_utility_heroes()
    ensure_404_content()
    patch_source_heroes()
    patch_content_sources()
    remove_red_image_files()
    write_pages_middleware()
    write_redirects()

    for filename, meta in PAGES.items():
        out = ROOT / filename
        html = assemble_page(filename, meta)
        out.write_text(html, encoding="utf-8")
        print(f"  wrote {filename}")

    bake_schedule_pages()
    write_sitemap()
    write_robots()
    update_attribution()
    package_pages_dist()
    print("Done.")


if __name__ == "__main__":
    main()
