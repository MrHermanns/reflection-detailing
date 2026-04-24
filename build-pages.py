#!/usr/bin/env python3
"""
Page generator for reflection-detailing site.
Outputs subpages under /ceramic-coating/, /eastlake/, etc. with shared scaffolding.
"""
import os, json, textwrap, pathlib

ROOT = pathlib.Path(__file__).parent

# ---------- shared bits ----------
BRAND = {
  "name": "Reflection Detailing",
  "phone_display": "(619) 341-0016",
  "phone_tel": "+16193410016",
  "phone_sms": "+16193410016",
  "email": None,
  "address_locality": "Chula Vista",
  "address_region": "CA",
  "postal_code": "91913",
  "lat": 32.6252,
  "lon": -116.993,
  "website": "https://mrhermanns.github.io/reflection-detailing",
  "setmore": "https://reflectiondetailingllc.setmore.com",
  "owner": "Angel",
}

SERVICE_AREAS = ["Chula Vista, CA", "Bonita, CA", "Eastlake, CA", "Otay Ranch, CA",
                 "National City, CA", "Imperial Beach, CA", "Coronado, CA", "San Diego, CA",
                 "Spring Valley, CA", "La Mesa, CA"]

# ---------- HTML head block (shared) ----------
def head(title, description, canonical_path, og_image=None, extra_schema=None):
    canonical = BRAND["website"].rstrip("/") + canonical_path
    og_image = og_image or f'{BRAND["website"]}/photos/4runner-exterior-after.jpg?v=3'
    extra = extra_schema or ""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
<meta name="theme-color" content="#0f172a" />

<title>{title}</title>
<meta name="description" content="{description}" />
<link rel="canonical" href="{canonical}" />

<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{og_image}" />
<meta name="twitter:card" content="summary_large_image" />

<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='19' fill='%23f59e0b'/%3E%3Cpath d='M13 29 V11 h8.5 a5 5 0 0 1 0 10 H17 l6 8 h-4 l-6-8 Z' fill='%230f172a'/%3E%3Ccircle cx='29' cy='13' r='2.2' fill='%23fff' opacity='.85'/%3E%3C/svg%3E" />

<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{ theme: {{ extend: {{
  colors: {{ ink: '#0f172a', accent: '#f59e0b' }},
  fontFamily: {{ sans: ['system-ui','-apple-system','Segoe UI','Roboto','Helvetica','Arial','sans-serif'] }}
}} }} }}
</script>

{_local_business_schema()}
{extra}

<style>
html {{ scroll-behavior: smooth; }}
.hero-bg {{
  background:
    linear-gradient(rgba(15,23,42,.82), rgba(2,6,23,.86)),
    url('{_path_back(canonical_path)}photos/4runner-exterior-after.jpg?v=3') center/cover no-repeat;
}}
.prose-body p {{ margin: 0 0 1em; }}
.prose-body h2 {{ margin-top: 1.5em; }}
.prose-body ul {{ margin: 0 0 1em 1.25em; list-style: disc; }}
.prose-body ul li::marker {{ color: #f59e0b; }}
</style>
</head>
<body class="bg-white text-ink antialiased font-sans">
'''

def _path_back(canonical_path):
    # Returns relative path prefix to reach site root photos/ etc.
    depth = canonical_path.strip("/").count("/") + (1 if canonical_path.strip("/") else 0)
    return "../" * depth if depth > 0 else ""

def _local_business_schema():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AutoDetailing",
  "name": "Reflection Detailing",
  "description": "Mobile auto detailing service in Chula Vista, CA. Interior and exterior detailing, ceramic coating, paint correction, and headlight restoration — at your location.",
  "image": "https://mrhermanns.github.io/reflection-detailing/photos/4runner-exterior-after.jpg?v=3",
  "url": "https://mrhermanns.github.io/reflection-detailing/",
  "telephone": "+1-619-341-0016",
  "priceRange": "$$",
  "address": { "@type": "PostalAddress", "addressLocality": "Chula Vista", "addressRegion": "CA", "postalCode": "91913", "addressCountry": "US" },
  "geo": { "@type": "GeoCoordinates", "latitude": 32.6252, "longitude": -116.993 },
  "areaServed": ["Chula Vista, CA", "Bonita, CA", "Eastlake, CA", "Otay Ranch, CA", "National City, CA", "Imperial Beach, CA", "Coronado, CA", "San Diego, CA"],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "09:00", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "07:00", "closes": "18:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "07:00", "closes": "14:00" }
  ],
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "4" },
  "paymentAccepted": "Cash, Credit Card, Debit Card, Apple Pay, Google Pay, Zelle, Venmo"
}
</script>'''

def breadcrumb_schema(trail):
    """trail: list of (name, url_path)"""
    items = []
    for i, (name, path) in enumerate(trail, 1):
        full = BRAND["website"].rstrip("/") + path
        items.append({"@type": "ListItem", "position": i, "name": name, "item": full})
    return f'''<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}, indent=2)}
</script>'''

# ---------- shared header / footer ----------
def header(current_path):
    # Use site-root-absolute paths so links work from any depth
    root = BRAND["website"]  # root URL (same-origin won't be an issue on GH Pages subpath)
    # On GitHub Pages the site lives at /reflection-detailing/ so use relative depth
    back = _path_back(current_path)
    return f'''
<header class="sticky top-0 z-40 bg-ink/95 backdrop-blur text-white">
  <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
    <a href="{back}" class="flex items-center gap-2 font-black tracking-tight text-lg">
      <svg viewBox="0 0 40 40" class="w-9 h-9" aria-hidden="true">
        <circle cx="20" cy="20" r="19" fill="#f59e0b"/>
        <path d="M13 29 V11 h8.5 a5 5 0 0 1 0 10 H17 l6 8 h-4 l-6-8 Z" fill="#0f172a"/>
        <circle cx="29" cy="13" r="2.2" fill="#fff" opacity=".85"/>
      </svg>
      <span>Reflection Detailing</span>
    </a>
    <nav class="hidden md:flex items-center gap-5 text-sm">
      <a href="{back}#services" class="hover:text-accent">Services</a>
      <a href="{back}#process" class="hover:text-accent">How It Works</a>
      <a href="{back}pricing/" class="hover:text-accent">Pricing</a>
      <a href="{back}#area" class="hover:text-accent">Service Area</a>
      <a href="{back}#faq" class="hover:text-accent">FAQ</a>
    </nav>
    <a href="{BRAND['setmore']}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-4 py-2 rounded-lg hover:opacity-90 text-sm">Book</a>
  </div>
</header>
'''

def breadcrumb_bar(trail):
    """trail: list of (name, path). Last is current."""
    parts = []
    for i, (name, path) in enumerate(trail):
        is_last = i == len(trail) - 1
        if is_last:
            parts.append(f'<span class="text-ink font-semibold">{name}</span>')
        else:
            full = BRAND["website"].rstrip("/") + path
            parts.append(f'<a href="{full}" class="hover:text-accent">{name}</a>')
    return f'<nav class="text-sm text-slate-500 max-w-6xl mx-auto px-4 py-4" aria-label="Breadcrumb">{" / ".join(parts)}</nav>'

def cta_block(title="Ready to book?", subtitle="Mobile detailing anywhere in Chula Vista and South San Diego."):
    return f'''
<section class="bg-ink text-white py-16">
  <div class="max-w-3xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm">Ready to Roll</p>
    <h2 class="text-3xl md:text-4xl font-black mt-2 mb-3">{title}</h2>
    <p class="text-slate-300 mb-8">{subtitle}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center mb-6">
      <a href="{BRAND['setmore']}" target="_blank" rel="noopener" class="inline-block bg-accent text-ink font-bold px-7 py-4 rounded-lg hover:opacity-90 text-lg">Book Online →</a>
      <a href="sms:{BRAND['phone_sms']}" class="inline-block bg-white/10 border border-white/30 text-white font-bold px-7 py-4 rounded-lg hover:bg-white/20 text-lg">Text {BRAND['phone_display']}</a>
    </div>
    <p class="text-slate-400 text-sm">Owner-operated by {BRAND['owner']}. Satisfaction guaranteed.</p>
  </div>
</section>
'''

def footer(current_path):
    back = _path_back(current_path)
    return f'''
<footer class="bg-slate-900 text-slate-400 text-sm">
  <div class="max-w-6xl mx-auto px-4 py-12 grid md:grid-cols-4 gap-8">
    <div>
      <div class="flex items-center gap-2 mb-3">
        <svg viewBox="0 0 40 40" class="w-8 h-8" aria-hidden="true">
          <circle cx="20" cy="20" r="19" fill="#f59e0b"/>
          <path d="M13 29 V11 h8.5 a5 5 0 0 1 0 10 H17 l6 8 h-4 l-6-8 Z" fill="#0f172a"/>
          <circle cx="29" cy="13" r="2.2" fill="#fff" opacity=".85"/>
        </svg>
        <span class="font-black text-white text-base">Reflection Detailing</span>
      </div>
      <p>Mobile auto detailing in Chula Vista and South San Diego.</p>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Services</p>
      <ul class="space-y-1">
        <li><a href="{back}ceramic-coating/" class="hover:text-accent">Ceramic Coating</a></li>
        <li><a href="{back}paint-correction/" class="hover:text-accent">Paint Correction</a></li>
        <li><a href="{back}mobile-detailing/" class="hover:text-accent">Mobile Detailing</a></li>
        <li><a href="{back}interior-detail/" class="hover:text-accent">Interior Detail</a></li>
        <li><a href="{back}headlight-restoration/" class="hover:text-accent">Headlight Restoration</a></li>
      </ul>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Service Areas</p>
      <ul class="space-y-1">
        <li><a href="{back}chula-vista/" class="hover:text-accent">Chula Vista</a></li>
        <li><a href="{back}eastlake/" class="hover:text-accent">Eastlake</a></li>
        <li><a href="{back}bonita/" class="hover:text-accent">Bonita</a></li>
        <li><a href="{back}otay-ranch/" class="hover:text-accent">Otay Ranch</a></li>
        <li><a href="{back}#area" class="hover:text-accent">All areas</a></li>
      </ul>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Contact</p>
      <p><a href="tel:{BRAND['phone_tel']}" class="hover:text-accent">{BRAND['phone_display']}</a></p>
      <p>Chula Vista, CA 91913</p>
      <p class="mt-2">Mon 9-5 · Tue-Sat 7-6 · Sun 7-2</p>
      <p class="mt-4"><a href="{back}learn/" class="hover:text-accent">Learn &amp; Guides</a></p>
      <p><a href="{back}pricing/" class="hover:text-accent">Pricing</a></p>
    </div>
  </div>
  <div class="border-t border-slate-800 py-4 text-center">
    © <script>document.write(new Date().getFullYear())</script> Reflection Detailing LLC. All rights reserved.
  </div>
</footer>
</body>
</html>
'''

# ---------- individual page generators ----------
def write(path, html):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(html)
    print("wrote", path)

# ================================================================
# SERVICE PAGES
# ================================================================
def service_page(slug, data):
    """data: dict with h1, title, meta_description, hero_kicker, hero_sub, price_from, sections"""
    path = f"/{slug}/"
    trail = [("Home", "/"), (data["breadcrumb"], path)]
    crumb_schema = breadcrumb_schema(trail)
    service_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{data['service_type']}",
  "provider": {{ "@type": "AutoDetailing", "name": "Reflection Detailing",
    "telephone": "+1-619-341-0016",
    "address": {{ "@type": "PostalAddress", "addressLocality": "Chula Vista", "addressRegion": "CA", "postalCode": "91913", "addressCountry": "US" }}
  }},
  "areaServed": "Chula Vista, CA and South San Diego",
  "description": "{data['service_schema_desc']}",
  "offers": {{ "@type": "Offer", "price": "{data['price_number']}", "priceCurrency": "USD", "priceSpecification": {{ "@type": "PriceSpecification", "minPrice": "{data['price_number']}", "priceCurrency": "USD" }} }}
}}
</script>'''

    faq_schema = ""
    if data.get("faqs"):
        faqs = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in data["faqs"]]
        faq_schema = f'''<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs}, indent=2)}
</script>'''

    html = head(data["title"], data["meta_description"], path, extra_schema=crumb_schema + service_schema + faq_schema)
    html += header(path)
    html += breadcrumb_bar(trail)

    # Hero
    html += f'''
<section class="hero-bg text-white">
  <div class="max-w-5xl mx-auto px-4 py-20 md:py-28 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">{data['hero_kicker']}</p>
    <h1 class="text-4xl md:text-5xl font-black leading-tight mb-4">{data['h1']}</h1>
    <p class="text-lg md:text-xl max-w-2xl mx-auto mb-7 text-slate-200">{data['hero_sub']}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="{BRAND['setmore']}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-6 py-3 rounded-lg hover:opacity-90">Book {data['breadcrumb']}</a>
      <a href="tel:{BRAND['phone_tel']}" class="bg-white/10 border border-white/30 font-bold px-6 py-3 rounded-lg hover:bg-white/20">Call {BRAND['phone_display']}</a>
    </div>
    <p class="text-sm text-slate-300 mt-6">Starting at <span class="font-bold text-accent">{data['price_from']}</span> &nbsp;·&nbsp; ★★★★★ 5.0 on Google</p>
  </div>
</section>
'''

    # Body sections
    html += '<section class="max-w-4xl mx-auto px-4 py-16 prose-body text-slate-700 text-base md:text-lg leading-relaxed">'
    for section in data["sections"]:
        html += f'<h2 class="text-2xl md:text-3xl font-black text-ink">{section["h2"]}</h2>'
        if section.get("intro"):
            html += f'<p>{section["intro"]}</p>'
        if section.get("list"):
            html += '<ul>'
            for item in section["list"]:
                html += f'<li>{item}</li>'
            html += '</ul>'
        if section.get("body_after"):
            for p in section["body_after"]:
                html += f'<p>{p}</p>'
    html += '</section>'

    # FAQ block if present
    if data.get("faqs"):
        html += '<section class="bg-slate-50 py-16"><div class="max-w-3xl mx-auto px-4">'
        html += '<h2 class="text-2xl md:text-3xl font-black text-ink mb-6">Frequently asked</h2>'
        html += '<div class="space-y-3">'
        for q, a in data["faqs"]:
            html += f'''<details class="group bg-white rounded-xl p-4 md:p-5 border border-slate-200">
  <summary class="cursor-pointer font-bold text-base md:text-lg flex justify-between items-start gap-3">{q} <span class="text-accent group-open:rotate-45 transition text-xl leading-none shrink-0">+</span></summary>
  <p class="text-slate-700 mt-3 text-sm md:text-base leading-relaxed">{a}</p>
</details>'''
        html += '</div></div></section>'

    # Related links
    related = data.get("related_services", [])
    if related:
        html += '<section class="max-w-5xl mx-auto px-4 py-12"><h2 class="text-2xl font-black text-ink mb-5">Related services</h2><div class="grid md:grid-cols-3 gap-4">'
        for name, slug_r, blurb in related:
            html += f'<a href="../{slug_r}/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold text-lg">{name}</p><p class="text-slate-600 text-sm mt-2">{blurb}</p><p class="text-accent font-bold text-sm mt-3">Learn more →</p></a>'
        html += '</div></section>'

    html += cta_block()
    html += footer(path)
    write(f"{slug}/index.html", html)

# ================================================================
# CITY PAGES
# ================================================================
def city_page(slug, data):
    path = f"/{slug}/"
    trail = [("Home", "/"), ("Service Areas", "/#area"), (data["city_name"], path)]
    crumb_schema = breadcrumb_schema(trail)

    place_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Place",
  "name": "{data['city_name']}, CA",
  "geo": {{ "@type": "GeoCoordinates", "latitude": {data['lat']}, "longitude": {data['lon']} }},
  "containedInPlace": {{ "@type": "City", "name": "{data['city_name']}" }}
}}
</script>'''

    html = head(data["title"], data["meta_description"], path, extra_schema=crumb_schema + place_schema)
    html += header(path)
    html += breadcrumb_bar(trail)

    html += f'''
<section class="hero-bg text-white">
  <div class="max-w-5xl mx-auto px-4 py-20 md:py-28 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Mobile Auto Detailing</p>
    <h1 class="text-4xl md:text-5xl font-black leading-tight mb-4">{data['h1']}</h1>
    <p class="text-lg md:text-xl max-w-2xl mx-auto mb-7 text-slate-200">{data['hero_sub']}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="{BRAND['setmore']}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-6 py-3 rounded-lg hover:opacity-90">Book a Detail</a>
      <a href="tel:{BRAND['phone_tel']}" class="bg-white/10 border border-white/30 font-bold px-6 py-3 rounded-lg hover:bg-white/20">Call {BRAND['phone_display']}</a>
    </div>
    <p class="text-sm text-slate-300 mt-6">Free mobile service throughout {data['city_name']}.</p>
  </div>
</section>
'''

    html += '<section class="max-w-4xl mx-auto px-4 py-16 prose-body text-slate-700 text-base md:text-lg leading-relaxed">'
    for section in data["sections"]:
        html += f'<h2 class="text-2xl md:text-3xl font-black text-ink">{section["h2"]}</h2>'
        if section.get("intro"):
            html += f'<p>{section["intro"]}</p>'
        if section.get("list"):
            html += '<ul>'
            for item in section["list"]:
                html += f'<li>{item}</li>'
            html += '</ul>'
        if section.get("body_after"):
            for p in section["body_after"]:
                html += f'<p>{p}</p>'
    html += '</section>'

    # Neighborhoods / zips
    if data.get("zips"):
        html += '<section class="bg-slate-50 py-10"><div class="max-w-4xl mx-auto px-4">'
        html += f'<h2 class="text-2xl font-black text-ink mb-4">{data["city_name"]} ZIP codes we cover</h2>'
        html += '<p class="text-slate-700">' + " · ".join(data["zips"]) + '</p>'
        html += '</div></section>'

    # Services grid
    html += '<section class="max-w-5xl mx-auto px-4 py-12"><h2 class="text-2xl font-black text-ink mb-5">Services available in '+data['city_name']+'</h2><div class="grid md:grid-cols-3 gap-4">'
    for name, slug_r, price in CITY_SERVICE_TILES:
        html += f'<a href="../{slug_r}/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold text-lg">{name}</p><p class="text-accent font-black text-xl my-2">{price}</p><p class="text-accent font-bold text-sm mt-2">Learn more →</p></a>'
    html += '</div></section>'

    html += cta_block(
        title=f"Book a detail in {data['city_name']}",
        subtitle=f"Mobile service anywhere in {data['city_name']} — we bring our own water and power."
    )
    html += footer(path)
    write(f"{slug}/index.html", html)


# ================================================================
# CONTENT (PRICING, LEARN HUB, ARTICLES)
# ================================================================
def pricing_page():
    path = "/pricing/"
    trail = [("Home", "/"), ("Pricing", path)]
    crumb_schema = breadcrumb_schema(trail)
    html = head(
        "Mobile Detailing Prices in Chula Vista & San Diego — Reflection Detailing",
        "Transparent mobile auto detailing prices in Chula Vista and San Diego. Mini Detail $89, Full Detail $279, Ceramic Coating from $449, Paint Correction from $499. No travel fees in South Bay.",
        path, extra_schema=crumb_schema
    )
    html += header(path)
    html += breadcrumb_bar(trail)

    html += '''
<section class="hero-bg text-white">
  <div class="max-w-5xl mx-auto px-4 py-20 md:py-24 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Pricing</p>
    <h1 class="text-4xl md:text-5xl font-black leading-tight mb-4">Transparent Detailing Prices</h1>
    <p class="text-lg md:text-xl max-w-2xl mx-auto text-slate-200">Base prices for sedans and coupes. SUVs +$40, full-size trucks +$60-$80. No travel fee in South Bay.</p>
  </div>
</section>
'''

    html += '''
<section class="max-w-5xl mx-auto px-4 py-12 overflow-x-auto">
<table class="w-full text-left border-collapse bg-white rounded-xl overflow-hidden shadow-sm">
  <thead class="bg-ink text-white">
    <tr><th class="p-4">Service</th><th class="p-4">Sedan / Coupe</th><th class="p-4">SUV</th><th class="p-4">Full-size Truck / Van</th><th class="p-4">Time</th></tr>
  </thead>
  <tbody class="text-sm">
    <tr class="border-b"><td class="p-4 font-bold">Mini Detail</td><td class="p-4">$89</td><td class="p-4">$129</td><td class="p-4">$149-$169</td><td class="p-4">~60 min</td></tr>
    <tr class="border-b bg-slate-50"><td class="p-4 font-bold">Full Interior</td><td class="p-4">$179</td><td class="p-4">$219</td><td class="p-4">$239-$259</td><td class="p-4">2-3 hr</td></tr>
    <tr class="border-b"><td class="p-4 font-bold">Full Exterior</td><td class="p-4">$169</td><td class="p-4">$209</td><td class="p-4">$229-$249</td><td class="p-4">2-3 hr</td></tr>
    <tr class="border-b bg-slate-50"><td class="p-4 font-bold">The Works (In + Out)</td><td class="p-4">$279</td><td class="p-4">$319</td><td class="p-4">$339-$359</td><td class="p-4">4-5 hr</td></tr>
    <tr class="border-b"><td class="p-4 font-bold">Paint Correction (1-step)</td><td class="p-4">$499+</td><td class="p-4">$549+</td><td class="p-4">$599+</td><td class="p-4">+2-4 hr</td></tr>
    <tr class="border-b bg-slate-50"><td class="p-4 font-bold">Paint Correction (2-step)</td><td class="p-4">$749+</td><td class="p-4">$799+</td><td class="p-4">$849+</td><td class="p-4">+4-6 hr</td></tr>
    <tr class="border-b"><td class="p-4 font-bold">Ceramic Coating (2-year)</td><td class="p-4">$449+</td><td class="p-4">$499+</td><td class="p-4">$549+</td><td class="p-4">Full day</td></tr>
    <tr class="border-b bg-slate-50"><td class="p-4 font-bold">Ceramic Coating (5-year)</td><td class="p-4">$849+</td><td class="p-4">$949+</td><td class="p-4">$1,049+</td><td class="p-4">Full day</td></tr>
    <tr class="border-b"><td class="p-4 font-bold">Headlight Restoration</td><td class="p-4">$99 / pair</td><td class="p-4">$99 / pair</td><td class="p-4">$99 / pair</td><td class="p-4">~45 min</td></tr>
    <tr class="border-b bg-slate-50"><td class="p-4 font-bold">Pet Hair Removal (add-on)</td><td class="p-4">+$40</td><td class="p-4">+$50</td><td class="p-4">+$60</td><td class="p-4">+30 min</td></tr>
  </tbody>
</table>
</section>

<section class="bg-slate-50 py-16">
  <div class="max-w-4xl mx-auto px-4">
    <h2 class="text-2xl md:text-3xl font-black text-ink mb-5">Monthly Maintenance Plans</h2>
    <div class="grid md:grid-cols-3 gap-4">
      <div class="bg-white rounded-xl p-6 border border-slate-200">
        <p class="font-bold text-lg">Essentials</p>
        <p class="text-accent font-black text-2xl my-2">$149/mo</p>
        <p class="text-slate-600 text-sm">2 Mini Details per month. Saves ~$30/mo vs. one-off pricing.</p>
      </div>
      <div class="bg-white rounded-xl p-6 border-2 border-accent relative">
        <span class="absolute -top-3 right-4 bg-accent text-ink text-xs font-black uppercase px-2 py-1 rounded">Best Value</span>
        <p class="font-bold text-lg">Monthly Reset</p>
        <p class="text-accent font-black text-2xl my-2">$239/mo</p>
        <p class="text-slate-600 text-sm">1 Full Detail per month. Saves ~$40/mo.</p>
      </div>
      <div class="bg-white rounded-xl p-6 border border-slate-200">
        <p class="font-bold text-lg">Premium</p>
        <p class="text-accent font-black text-2xl my-2">$219/mo</p>
        <p class="text-slate-600 text-sm">1 Mini + 1 Full Interior per month. Keeps the inside factory-fresh.</p>
      </div>
    </div>
  </div>
</section>

<section class="max-w-4xl mx-auto px-4 py-16 prose-body text-slate-700 text-base md:text-lg leading-relaxed">
  <h2 class="text-2xl md:text-3xl font-black text-ink">How our pricing compares</h2>
  <p>Reflection Detailing is priced in the middle of the San Diego mobile detailing market. Competitors like Fresh Layer and Pristine Mobile charge $249-$389 for a full detail; shop-based detailers charge $229-$389 plus your time and gas driving there. Our $279 Full Detail is mid-market and includes free on-site mobile service anywhere in South Bay.</p>

  <h2 class="text-2xl md:text-3xl font-black text-ink">What affects final price?</h2>
  <ul>
    <li><strong>Vehicle size:</strong> SUVs add $40, full-size trucks and vans add $60-$80, 3-row SUVs add $80-$100.</li>
    <li><strong>Paint condition:</strong> Heavy oxidation, deep scratches, or neglected paint may require a 2-step correction.</li>
    <li><strong>Interior condition:</strong> Severe pet hair, stains, or smoke damage may require a two-visit treatment.</li>
    <li><strong>Fleet accounts:</strong> 5+ vehicles per month qualify for volume pricing — text us for a quote.</li>
  </ul>

  <h2 class="text-2xl md:text-3xl font-black text-ink">No travel fees in South Bay</h2>
  <p>We do not charge extra for mobile service in Chula Vista, Bonita, Eastlake, Otay Ranch, National City, Imperial Beach, Coronado, or South San Diego. Travel beyond that area may include a small travel fee, quoted at booking.</p>
</section>
'''

    html += cta_block("Ready to book?", "Pick a service above and book a time — real-time availability.")
    html += footer(path)
    write("pricing/index.html", html)


def learn_hub():
    path = "/learn/"
    trail = [("Home", "/"), ("Learn", path)]
    crumb_schema = breadcrumb_schema(trail)
    html = head(
        "Auto Detailing Guides — Reflection Detailing",
        "Practical guides on ceramic coating, paint correction, wax vs sealant, and keeping your car clean in the San Diego climate. Written by Angel at Reflection Detailing.",
        path, extra_schema=crumb_schema
    )
    html += header(path)
    html += breadcrumb_bar(trail)

    html += '''
<section class="hero-bg text-white">
  <div class="max-w-5xl mx-auto px-4 py-20 md:py-24 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Learn</p>
    <h1 class="text-4xl md:text-5xl font-black leading-tight mb-4">Detailing Guides</h1>
    <p class="text-lg md:text-xl max-w-2xl mx-auto text-slate-200">Practical knowledge from Angel, owner of Reflection Detailing in Chula Vista.</p>
  </div>
</section>
'''

    articles = [
        ("wax-vs-ceramic-coating", "Wax vs Ceramic Coating: Which Does Your Car Actually Need?", "A head-to-head breakdown: durability, cost, gloss, and when ceramic makes sense.", "7 min read"),
        ("paint-correction-cost-san-diego", "How Much Does Paint Correction Cost in San Diego?", "A 2026 pricing guide with real numbers, plus what's worth paying for.", "6 min read"),
        ("signs-your-car-needs-detailing", "5 Signs Your Car Needs a Detail", "How to tell when it's time for a full detail — before you start harming the paint.", "4 min read"),
    ]
    html += '<section class="max-w-5xl mx-auto px-4 py-16"><div class="grid md:grid-cols-3 gap-6">'
    for slug, title, blurb, read in articles:
        html += f'''<a href="{slug}/" class="block border border-slate-200 rounded-xl p-6 hover:border-accent">
  <p class="text-sm text-accent font-bold">{read}</p>
  <h2 class="font-bold text-xl mt-2 mb-2">{title}</h2>
  <p class="text-slate-600 text-sm">{blurb}</p>
  <p class="text-accent font-bold text-sm mt-3">Read →</p>
</a>'''
    html += '</div></section>'
    html += cta_block()
    html += footer(path)
    write("learn/index.html", html)


def article_page(slug, data):
    path = f"/learn/{slug}/"
    trail = [("Home", "/"), ("Learn", "/learn/"), (data["short_title"], path)]
    crumb_schema = breadcrumb_schema(trail)
    article_schema = f'''<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": data["h1"],
  "description": data["meta_description"],
  "author": {{"@type": "Person", "name": "Angel"}} if False else {"@type": "Person", "name": "Angel"},
  "publisher": {"@type": "Organization", "name": "Reflection Detailing", "logo": {"@type": "ImageObject", "url": BRAND["website"] + "/photos/4runner-exterior-after.jpg?v=3"}},
  "datePublished": "2026-04-23",
  "mainEntityOfPage": BRAND["website"].rstrip("/") + path
}, indent=2)}
</script>'''
    html = head(data["title"], data["meta_description"], path, extra_schema=crumb_schema + article_schema)
    html += header(path)
    html += breadcrumb_bar(trail)

    html += f'''
<article class="max-w-3xl mx-auto px-4 py-12 prose-body text-slate-700 text-base md:text-lg leading-relaxed">
  <p class="uppercase tracking-widest text-accent font-bold text-sm">Guide</p>
  <h1 class="text-3xl md:text-5xl font-black text-ink mt-2 mb-4 leading-tight">{data['h1']}</h1>
  <p class="text-slate-500 text-sm mb-8">By Angel, owner of Reflection Detailing · Chula Vista, CA · {data['read_time']}</p>
'''
    for block in data["blocks"]:
        kind = block[0]
        if kind == "p":
            html += f'<p>{block[1]}</p>'
        elif kind == "h2":
            html += f'<h2 class="text-2xl md:text-3xl font-black text-ink">{block[1]}</h2>'
        elif kind == "h3":
            html += f'<h3 class="text-xl font-bold text-ink">{block[1]}</h3>'
        elif kind == "ul":
            html += '<ul>'
            for it in block[1]:
                html += f'<li>{it}</li>'
            html += '</ul>'
        elif kind == "quote":
            html += f'<blockquote class="border-l-4 border-accent pl-5 italic text-slate-600 my-6">{block[1]}</blockquote>'
        elif kind == "cta":
            html += f'<p class="bg-slate-100 rounded-xl p-5 my-6"><strong>{block[1]}</strong> <a href="{BRAND["setmore"]}" target="_blank" rel="noopener" class="text-accent font-bold">Book online →</a></p>'
    html += '</article>'
    html += cta_block()
    html += footer(path)
    write(f"learn/{slug}/index.html", html)


# ================================================================
# DATA: services, cities, articles
# ================================================================

CITY_SERVICE_TILES = [
    ("Mini Detail", "mobile-detailing", "$89"),
    ("Full Detail", "mobile-detailing", "$279"),
    ("Ceramic Coating", "ceramic-coating", "$449+"),
    ("Paint Correction", "paint-correction", "$499+"),
    ("Headlight Restoration", "headlight-restoration", "$99"),
    ("Full Interior", "interior-detail", "$179"),
]

SERVICES = [
    # slug -> data
    ("ceramic-coating", {
        "title": "Ceramic Coating in Chula Vista — 2-yr & 5-yr Options from $449 | Reflection Detailing",
        "meta_description": "Professional mobile ceramic coating in Chula Vista and San Diego. 2-year graphene spray from $449, 5-year from $849. Includes paint prep, decontamination, and installation at your location.",
        "breadcrumb": "Ceramic Coating",
        "service_type": "Mobile Ceramic Coating",
        "service_schema_desc": "Professional ceramic coating installation for vehicles, including paint prep and decontamination. 2-year and 5-year options available.",
        "price_number": "449",
        "price_from": "$449",
        "h1": "Ceramic Coating — Installed at Your Driveway",
        "hero_kicker": "Pro-grade paint protection",
        "hero_sub": "2-year and 5-year graphene ceramic coatings, professionally applied. Includes full paint prep, clay decontamination, and installation. Chula Vista, Bonita, Eastlake and the greater South Bay.",
        "sections": [
            {"h2": "What is ceramic coating?",
             "intro": "Ceramic coating is a liquid polymer that bonds chemically with your vehicle's factory clear coat, forming a semi-permanent layer of protection. Unlike wax (which lasts 1-3 months) or spray sealants (3-6 months), a professionally installed ceramic coating lasts 2-5+ years. It's hydrophobic — water, mud, bird droppings, and tree sap slide off instead of sticking. UV rays don't break down the paint. Swirl marks are dramatically harder to create."},
            {"h2": "What's included in our ceramic coating service",
             "list": [
               "Full exterior hand wash with decontamination soap",
               "Iron-fallout treatment to lift embedded metal particles",
               "Clay bar decontamination (removes bonded contaminants)",
               "Isopropyl alcohol wipe-down to remove polish oils",
               "Ceramic coating application (2-year or 5-year)",
               "Curing time (at least 60 minutes on-site before leaving)",
               "Post-install walk-around and care instructions"
             ]},
            {"h2": "2-year vs 5-year — which should you choose?",
             "intro": "We offer two tiers:",
             "list": [
               "<strong>2-year graphene spray ($449+):</strong> Great value. Hydrophobic beading, UV protection, and easier washing for 2+ years. Best if you change cars every 2-3 years or want to try ceramic for the first time.",
               "<strong>5-year graphene ($849+):</strong> Premium formulation with higher hardness rating and longer protection. Includes a 1-step polish prep to remove light defects before coating. Best long-term value — typically pays for itself in saved wax/sealant costs by year 2."
             ]},
            {"h2": "How long does installation take?",
             "body_after": [
               "Plan for 6-8 hours on-site. The coating itself takes about an hour to apply panel-by-panel, but proper paint prep (wash, clay, decon, IPA wipe, and optional polish) is where most of the time goes. A rushed ceramic install is a bad ceramic install — the coating is only as durable as the prep underneath it."
             ]},
            {"h2": "Aftercare (read this!)",
             "list": [
               "No washing for 7 days after installation — let the coating fully cure.",
               "Avoid rain for the first 24 hours if possible.",
               "When washing, use a pH-neutral ceramic-safe soap (we recommend CarPro Reset or Gyeon Bathe+).",
               "Two-bucket method. No brush washes, no high-pressure at close range.",
               "We include a free 30-day inspection to verify cure and answer questions."
             ]}
        ],
        "faqs": [
            ("How long does ceramic coating actually last?", "A 2-year graphene ceramic realistically lasts 2-3 years with proper care. A 5-year ceramic lasts 5+ years. Durability depends on wash habits, storage, and climate — coastal San Diego UV is tough on paint, so we recommend rinse-only monthly maintenance between full washes."),
            ("Can I apply ceramic coating myself?", "Consumer spray ceramics exist but don't compare to professional installations. The difference is the prep — a proper paint correction and decontamination takes 6+ hours of skilled labor. DIY coatings applied over contaminated or swirled paint seal in the defects permanently."),
            ("Does ceramic coating prevent rock chips and scratches?", "No. Ceramic is 9H hard but only ~2-3 microns thick. It resists swirl marks from washing and minor brush-byes, but it won't stop a rock or a door ding. For rock-chip protection, you want paint protection film (PPF) — which we do not currently offer but can refer."),
            ("What's the difference between graphene and traditional SiO2 ceramic?", "Graphene-enhanced ceramics run slightly cooler on the paint surface (reducing water-spot baking), provide stronger hydrophobicity, and generally last 1-2 years longer than SiO2-only formulations. Our 5-year option is a graphene hybrid."),
        ],
        "related_services": [
            ("Paint Correction", "paint-correction", "Remove swirl marks and oxidation before coating. Often paired."),
            ("Full Detail", "mobile-detailing", "The prep for ceramic is part of our Works package."),
            ("Headlight Restoration", "headlight-restoration", "Clear those cloudy headlights while we're there."),
        ]
    }),

    ("paint-correction", {
        "title": "Paint Correction in Chula Vista — 1-Step & 2-Step from $499 | Reflection Detailing",
        "meta_description": "Mobile paint correction in Chula Vista and San Diego. Machine polish to remove swirl marks, scratches, and oxidation. 1-step from $499, 2-step from $749. Prep for ceramic coating included.",
        "breadcrumb": "Paint Correction",
        "service_type": "Mobile Paint Correction",
        "service_schema_desc": "Machine polishing to remove swirl marks, scratches, water spots, and oxidation. 1-step and 2-step options.",
        "price_number": "499",
        "price_from": "$499",
        "h1": "Paint Correction — Restore the Shine",
        "hero_kicker": "Swirl marks, scratches, and oxidation — gone",
        "hero_sub": "Professional machine polishing that removes up to 95% of defects. Ideal before ceramic coating or anytime your paint has lost its depth. Mobile service throughout South San Diego.",
        "sections": [
            {"h2": "What is paint correction?",
             "intro": "Paint correction is a machine-polishing process that physically removes a micro-thin layer of clear coat — along with the defects embedded in it. Swirl marks (those spider-web scratches that appear under streetlights), light scratches, water spots, bird-dropping etching, and oxidation all disappear. What's left is flat, glossy paint that looks better than the day it left the dealership."},
            {"h2": "1-step vs 2-step correction",
             "list": [
               "<strong>1-step ($499+):</strong> Single polishing pass with a medium compound + polish combo. Removes ~70-80% of swirl marks and light defects. Best for cars 1-4 years old with light wear.",
               "<strong>2-step ($749+):</strong> Heavy compound pass first to remove deeper defects, then a finishing polish to eliminate compound haze. Removes ~90-95% of defects. Best for older paint, neglected finishes, or cars about to be ceramic-coated."
             ]},
            {"h2": "How we correct paint on-site",
             "list": [
               "Full decontamination wash (iron fallout, clay bar, tar remover)",
               "Paint inspection under 1500-lumen swirl-finder lights",
               "Depth measurement to verify clear coat thickness before aggressive polishing",
               "Machine polish panel-by-panel with Rupes or Flex dual-action polishers",
               "IPA wipe-down to reveal true finish",
               "Optional: spray sealant or ceramic coating to lock in results"
             ]},
            {"h2": "Do you need paint correction?",
             "intro": "You likely need paint correction if:",
             "list": [
               "You see swirls or spider-web scratches under sunlight or a streetlight",
               "Paint looks hazy or milky compared to the day you bought it",
               "Water beads unevenly or sits in spots",
               "You're planning to apply a ceramic coating (prep is required)"
             ]},
        ],
        "faqs": [
            ("Will paint correction remove deep scratches?", "It removes scratches that fit within the clear coat — usually anything you can't catch with a fingernail. Deep scratches that go into the base coat require touch-up paint or a respray, which we don't do. We can usually 'round the edges' of deeper scratches to make them dramatically less visible."),
            ("Is paint correction safe for my clear coat?", "Yes, when done properly. We measure clear-coat thickness before any aggressive polishing. We never remove more than a few microns in a single session, leaving plenty of clear coat for future corrections. Rushed or DIY attempts with the wrong pad/compound combo are what damage paint — we use Rupes and Flex DA polishers for safe, controlled correction."),
            ("How long does paint correction last?", "The correction itself is permanent — the defects are physically removed. But new swirls will appear over time from washing and brush-byes. To protect the results, we strongly recommend a spray sealant (3-6 months) or ceramic coating (2-5 years) immediately after correction."),
            ("Can you correct a color-changing or matte finish?", "We do not correct matte, satin, or wrap finishes. Those require specialty products that can damage regular gloss paint. For matte-specific care, please text us — we can refer you to a specialist."),
        ],
        "related_services": [
            ("Ceramic Coating", "ceramic-coating", "Lock in the correction for 2-5+ years."),
            ("The Works", "mobile-detailing", "Complete in + out detail with light polish included."),
            ("Headlight Restoration", "headlight-restoration", "Correct cloudy headlights while we're there."),
        ]
    }),

    ("mobile-detailing", {
        "title": "Mobile Auto Detailing in Chula Vista & San Diego — Reflection Detailing",
        "meta_description": "Full mobile detailing from $89 Mini to $279 Works. We come to you with our own water and power. Serving Chula Vista, Eastlake, Bonita, Otay Ranch, and South San Diego.",
        "breadcrumb": "Mobile Detailing",
        "service_type": "Mobile Auto Detailing",
        "service_schema_desc": "On-site interior and exterior auto detailing. Services include Mini Detail, Full Interior, Full Exterior, and The Works (complete in + out package).",
        "price_number": "89",
        "price_from": "$89",
        "h1": "Mobile Auto Detailing — We Come to You",
        "hero_kicker": "Driveway, office, or jobsite",
        "hero_sub": "Fully self-contained: 40-gallon water tank, 3,500-watt generator, pro-grade products. Serving Chula Vista, Bonita, Eastlake, Otay Ranch, and South San Diego. From $89.",
        "sections": [
            {"h2": "Why mobile detailing beats the shop",
             "list": [
               "<strong>Zero driving.</strong> We come to you — no waiting room, no sitting in a lobby for four hours.",
               "<strong>Self-contained rig.</strong> You don't need to provide water, power, or equipment. We bring everything.",
               "<strong>Real attention.</strong> Owner-operated. Angel is the only person who touches your car.",
               "<strong>Flexible hours.</strong> Evenings and weekends available — we work when you're home."
             ]},
            {"h2": "Our service menu",
             "list": [
               "<strong>Mini Detail ($89):</strong> Hand wash, interior vacuum, windows, tire dressing. ~60 minutes. Perfect between full details.",
               "<strong>Full Interior ($179):</strong> Deep vacuum, carpet and upholstery shampoo, leather condition, UV protect, odor neutralize. 2-3 hours.",
               "<strong>Full Exterior ($169):</strong> Hand wash, clay bar, wheel and tire deep clean, spray sealant, trim dressing. 2-3 hours.",
               "<strong>The Works ($279):</strong> Complete interior + exterior. The reset button. 4-5 hours.",
               "<strong>Add paint correction, ceramic coating, or headlight restoration</strong> to any package."
             ]},
            {"h2": "Where we serve",
             "intro": "Mobile service is free throughout South San Diego:",
             "list": [
                "Chula Vista (all ZIP codes 91910-91915)",
                "Bonita & Rancho Del Rey",
                "Eastlake",
                "Otay Ranch",
                "National City",
                "Imperial Beach",
                "Coronado",
                "San Diego (most neighborhoods)",
                "Spring Valley, La Mesa, Lemon Grove",
             ]},
            {"h2": "What to expect on the day",
             "list": [
               "We confirm your appointment the night before via text.",
               "Angel arrives at the scheduled time with our rig (truck + tank + generator).",
               "You point out any concerns — stains, scratches, etc.",
               "Detailing happens in your driveway/lot. You can go inside or watch.",
               "Walk-around inspection at the end — we don't leave until you're happy.",
               "Payment by card, Zelle, Apple Pay, or cash."
             ]},
        ],
        "faqs": [
            ("Can you detail my car at my apartment or condo complex?", "Yes, as long as there's a flat parking space with ~10 ft clearance. We've detailed in apartment garages, visitor parking, and curbside throughout Chula Vista. If your HOA has rules, let us know ahead of time."),
            ("Do you work in the rain?", "We prefer dry conditions. San Diego rarely gets heavy rain, but if weather looks rough, we'll reschedule at no charge. Ceramic coating and paint correction require dry conditions — we do not do these in rain."),
            ("Can I be there or not — does it matter?", "Either works. Many customers leave us the keys and go inside or head to work. Others watch and ask questions. We treat your car the same either way."),
        ],
        "related_services": [
            ("Ceramic Coating", "ceramic-coating", "Long-term paint protection (2-5+ years)."),
            ("Paint Correction", "paint-correction", "Remove swirl marks and oxidation."),
            ("Interior Detail", "interior-detail", "Deep clean just the inside."),
        ]
    }),

    ("headlight-restoration", {
        "title": "Headlight Restoration in Chula Vista — $99 Mobile Service | Reflection Detailing",
        "meta_description": "Cloudy or yellowed headlights? Mobile headlight restoration in Chula Vista and San Diego. $99 per pair, 45 minutes, we come to you. Sand, polish, and UV seal for clear beams.",
        "breadcrumb": "Headlight Restoration",
        "service_type": "Headlight Restoration",
        "service_schema_desc": "Mobile headlight restoration: sanding, polishing, and UV sealing cloudy or yellowed headlight lenses.",
        "price_number": "99",
        "price_from": "$99 / pair",
        "h1": "Headlight Restoration — 45 Minutes, $99",
        "hero_kicker": "Safer driving, cleaner look",
        "hero_sub": "Mobile headlight restoration in Chula Vista and South San Diego. We sand, polish, and UV-seal cloudy headlights in about 45 minutes per pair. Huge safety improvement — cloudy headlights can reduce night-time visibility by up to 80%.",
        "sections": [
            {"h2": "Why headlights cloud over",
             "intro": "Modern headlight lenses are made of polycarbonate plastic. The factory applies a UV-protective clear coat on the outside — but after 3-5 years in the San Diego sun, that coating breaks down. The plastic itself starts to oxidize, turning yellow or milky. The result: scattered light at night, reduced range, and an old-looking car even if the rest of the paint is mint."},
            {"h2": "Our restoration process",
             "list": [
               "Mask off surrounding paint and trim",
               "Wet-sand the oxidized surface with progressively finer grits (600 → 1000 → 2000 → 3000)",
               "Machine polish with a fine-cut compound to restore optical clarity",
               "Apply a UV-protective sealant that extends the life of the restoration by 1-2 years",
               "Visual inspection — any remaining haze gets an additional pass"
             ]},
            {"h2": "How long does it last?",
             "body_after": [
               "With the UV sealant we apply, expect 12-24 months before mild haze returns. Touch-up service (a light polish pass, no sanding) runs about $45 and takes 15 minutes. Without the UV sealant, restorations typically last 4-6 months — which is why we always include it."
             ]},
            {"h2": "When it's NOT worth restoring",
             "intro": "Occasionally we encounter headlights beyond restoration:",
             "list": [
               "Cracked lenses (replacement required)",
               "Internal fogging — moisture INSIDE the headlight housing from a failed seal (requires replacement)",
               "Deep chemical damage or burns (replacement usually cheaper)"
             ]},
        ],
        "faqs": [
            ("Is this the same as the DIY kits at AutoZone?", "No. DIY kits apply a thin wipe-on polish that lasts weeks. We wet-sand the oxidation out and apply an actual UV-protective sealant that lasts 1-2 years. The difference in longevity is roughly 10x."),
            ("Can you do it while I'm at work?", "Yes. As long as your car is accessible and the space is legal to work in, we don't need you there. Most customers leave the keys and come back to finished headlights."),
            ("Can I book just headlights, or do I need a full detail?", "Headlight restoration is a standalone service. $99 flat rate for the pair. We often tack it onto a detail but you're welcome to book it alone."),
        ],
        "related_services": [
            ("Mobile Detailing", "mobile-detailing", "Pair with a full detail for maximum value."),
            ("Ceramic Coating", "ceramic-coating", "Long-term protection for your paint."),
            ("Paint Correction", "paint-correction", "Cloudy paint? Same idea as cloudy headlights — we fix both."),
        ]
    }),

    ("interior-detail", {
        "title": "Interior Car Detailing in Chula Vista — Full Interior from $179 | Reflection Detailing",
        "meta_description": "Full interior car detailing in Chula Vista and San Diego. Deep vacuum, upholstery shampoo, leather condition, odor neutralize. $179 for sedans, mobile service.",
        "breadcrumb": "Interior Detail",
        "service_type": "Interior Auto Detailing",
        "service_schema_desc": "Full interior car detailing including deep vacuum, carpet and upholstery shampoo, leather conditioning, and odor treatment.",
        "price_number": "179",
        "price_from": "$179",
        "h1": "Full Interior Detail — Factory-Fresh Inside",
        "hero_kicker": "Deep clean, condition, protect",
        "hero_sub": "Complete interior detailing: deep vacuum, carpet and upholstery shampoo, leather condition, UV protectant, and odor neutralizing. 2-3 hours at your location.",
        "sections": [
            {"h2": "What's included",
             "list": [
               "Remove floor mats, detail separately",
               "Full interior vacuum (seats, carpet, trunk, headliner)",
               "Compressed-air blowout of vents, seams, and crevices",
               "Carpet and upholstery shampoo with hot-water extraction",
               "Leather seats: cleaner + conditioner + UV protectant",
               "Dashboard, door panels, console: cleaned and dressed with UV protectant (matte, not shiny)",
               "Glass: streak-free inside and out",
               "Odor treatment: enzymatic neutralizer or ozone on request",
               "Floor mats re-installed, vehicle inspected"
             ]},
            {"h2": "When to book a full interior",
             "intro": "Most customers book a full interior every 3-6 months. Sooner if:",
             "list": [
               "You have kids or pets",
               "You eat in the car regularly",
               "The interior smells or looks tired",
               "You're preparing to sell (adds ~$500 to resale value)"
             ]},
            {"h2": "Pet hair removal (add-on)",
             "body_after": [
               "Embedded pet hair requires specialty rubber extractors — a regular vacuum can't get it out of fabric weaves. $40 add-on to any interior package. Severe cases (multi-dog households, long coats) may need extra time quoted at booking."
             ]},
        ],
        "faqs": [
            ("Can you remove vomit, food spills, or really bad stains?", "Yes. Most organic stains come out with our hot-water extractor and enzymatic treatments. Severe biological contamination (vomit, pet accidents) may need a two-visit process: extraction + neutralizer the first visit, re-extract and condition the second. We'll assess and quote at booking."),
            ("Will shampooing damage my leather or fabric seats?", "No. We use pH-neutral products rated for each surface type. Leather gets a dedicated cleaner and conditioner. Fabric gets an upholstery shampoo with controlled hot-water extraction — not a soak."),
            ("How long does the interior smell like cleaning products?", "Our products are low-fragrance. Most customers report the car smells 'clean' for a day, then neutral. We avoid overly perfumed products on purpose — a 'fresh' smelling car often means something is being masked."),
        ],
        "related_services": [
            ("Full Detail", "mobile-detailing", "Pair interior with exterior — The Works."),
            ("Paint Correction", "paint-correction", "Interior fresh + paint restored = the complete reset."),
            ("Ceramic Coating", "ceramic-coating", "Protect the outside after cleaning the inside."),
        ]
    }),
]

CITIES = [
    ("chula-vista", {
        "city_name": "Chula Vista",
        "lat": 32.6401, "lon": -117.0842,
        "title": "Mobile Auto Detailing in Chula Vista, CA — Reflection Detailing",
        "meta_description": "Mobile auto detailing throughout Chula Vista, CA. Free mobile service in all ZIP codes 91910-91915. Full Detail $279, Ceramic Coating from $449. Owner-operated by Angel.",
        "h1": "Mobile Auto Detailing in Chula Vista",
        "hero_sub": "We're based in Chula Vista — you're on our home turf. Full mobile coverage across Eastlake, Otay Ranch, Bonita, Rolling Hills, and the Third Avenue area. Most bookings serviced within 48 hours.",
        "zips": ["91910", "91911", "91913", "91914", "91915"],
        "sections": [
            {"h2": "Why Chula Vista customers choose Reflection",
             "list": [
               "Fast scheduling — we're usually out in 24-48 hours",
               "No travel fee anywhere in Chula Vista",
               "Family-owned and operated — your car isn't handed to a rotating crew",
               "Rated 5.0 on Google",
               "Evenings and weekends available"
             ]},
            {"h2": "Neighborhoods we regularly detail in",
             "list": [
               "<strong>Eastlake</strong> — heavy ceramic coating and paint correction demand on Teslas, BMWs, and European daily drivers",
               "<strong>Otay Ranch</strong> — rapid-growth neighborhood, popular for Full Details and monthly maintenance plans",
               "<strong>Rolling Hills Ranch</strong> — luxury vehicles, often ceramic and PPF-prep work",
               "<strong>Third Avenue / downtown Chula Vista</strong> — office and residential bookings",
               "<strong>Rancho Del Rey</strong> — family vehicles, Mini Details and interior deep cleans",
               "<strong>Bonita border</strong> — full coverage to Bonita Road"
             ]},
            {"h2": "Local-specific conditions",
             "body_after": [
               "Chula Vista sits just inland from the San Diego Bay. Paint here takes a double hit: intense UV year-round plus salt aerosol that drifts up from the coast. We adjust our exterior work accordingly — extra decontamination passes on cars driven daily to the coast, and UV-focused ceramic coatings for garaged-outside vehicles.",
               "Summer highs reach 85°F here. We don't polish or coat in direct sun after 11am — we schedule morning slots for paint work and afternoon slots for interiors."
             ]},
        ],
    }),
    ("eastlake", {
        "city_name": "Eastlake",
        "lat": 32.6565, "lon": -116.9673,
        "title": "Mobile Auto Detailing in Eastlake, Chula Vista — Reflection Detailing",
        "meta_description": "Premium mobile auto detailing in Eastlake, Chula Vista. Ceramic coating, paint correction, and full details at your door. Popular among Eastlake Tesla, BMW, and Mercedes owners.",
        "h1": "Mobile Auto Detailing in Eastlake",
        "hero_sub": "Eastlake is one of our busiest zones. Ceramic coatings on Teslas, paint correction on European dailies, and weekly maintenance for families. Full mobile service to every gated community.",
        "zips": ["91914", "91915"],
        "sections": [
            {"h2": "Eastlake's most-booked services",
             "list": [
               "<strong>Ceramic coating</strong> — by far the most popular. Our 5-year package lives here.",
               "<strong>Paint correction</strong> — especially for Tesla Model 3 and Model Y owners seeing swirl marks from daily washing",
               "<strong>The Works (Full Detail)</strong> — the go-to for 3-row SUVs with active family schedules",
               "<strong>Headlight restoration</strong> — on 5+ year old daily drivers",
             ]},
            {"h2": "HOA and gated-community details",
             "body_after": [
                "We've worked in every major Eastlake community — Windingwalk, Woods, Greens, Shores, Trails, Vistas, and Village Center. Just give us the gate code or call box number when booking, or coordinate with your HOA ahead of time.",
                "Our rig is self-contained — we don't need access to outdoor water or outlets. That matters in communities where exterior water use is restricted during drought advisories."
              ]},
            {"h2": "Sample Eastlake job pricing",
             "list": [
                "Tesla Model Y Full Detail + 2-year ceramic: $728",
                "BMW 3-Series paint correction (1-step) + 5-year ceramic: $1,348",
                "Toyota Sienna Works + pet hair removal: $359",
                "Mercedes GLE Interior Detail: $219",
             ]},
        ],
    }),
    ("bonita", {
        "city_name": "Bonita",
        "lat": 32.6579, "lon": -117.0289,
        "title": "Mobile Auto Detailing in Bonita, CA — Reflection Detailing",
        "meta_description": "Premium mobile auto detailing in Bonita, California. Ceramic coating, paint correction, and full interior/exterior detailing at your home. Family-owned, rated 5.0 on Google.",
        "h1": "Mobile Auto Detailing in Bonita",
        "hero_sub": "Bonita is our neighboring community — quick response times and full coverage. Popular for luxury and exotic vehicles. Gated-community friendly.",
        "zips": ["91902"],
        "sections": [
            {"h2": "Popular Bonita services",
             "list": [
                "Ceramic coating for luxury European cars",
                "Paint correction on collector or weekend vehicles",
                "Monthly maintenance plans for daily drivers",
                "RV and boat detailing (custom quote)",
             ]},
            {"h2": "Rancho Del Rey, Sweetwater, and Bonita Grove",
             "body_after": [
                "We've worked across all of Bonita's residential areas. Sweetwater Road and Bonita Road customers get same-week booking during peak months (spring and fall). The Rancho Del Rey area has the highest concentration of ceramic-coated vehicles on our roster."
             ]},
        ],
    }),
    ("otay-ranch", {
        "city_name": "Otay Ranch",
        "lat": 32.6226, "lon": -116.9568,
        "title": "Mobile Auto Detailing in Otay Ranch — Reflection Detailing",
        "meta_description": "Mobile auto detailing in Otay Ranch, Chula Vista. Full detailing, ceramic coating, and paint correction at your driveway. Fast scheduling, no travel fee.",
        "h1": "Mobile Auto Detailing in Otay Ranch",
        "hero_sub": "Otay Ranch is one of Chula Vista's fastest-growing neighborhoods and a big part of our weekly schedule. Full mobile coverage across all neighborhoods.",
        "zips": ["91913", "91914", "91915"],
        "sections": [
            {"h2": "Why Otay Ranch customers book Reflection",
             "list": [
               "Young families — we handle sticky stuff, crumbs, and juice spills without judgment",
               "New-construction driveways — we protect your pavers and concrete with drip mats",
               "Multi-car households — ask about family pricing (2+ cars same appointment)",
               "Weekend warriors — book Saturday evenings for Sunday-ready cars"
             ]},
            {"h2": "Otay Ranch zone coverage",
             "body_after": [
                "We regularly detail in Village 2, Village 6, Village 11, Montecito, Heritage, and the Olympic Parkway corridor. Same-day requests are often possible here — just text us."
             ]},
        ],
    }),
]

ARTICLES = [
    ("wax-vs-ceramic-coating", {
        "short_title": "Wax vs Ceramic Coating",
        "title": "Wax vs Ceramic Coating: Which Does Your Car Actually Need? — Reflection Detailing",
        "meta_description": "A practical comparison of wax vs ceramic coating for cars. Durability, cost, gloss, and when ceramic makes sense. Written by Angel at Reflection Detailing in Chula Vista.",
        "h1": "Wax vs Ceramic Coating: Which Does Your Car Actually Need?",
        "read_time": "7 min read",
        "blocks": [
            ("p", "Customers ask me this at least twice a week: 'Should I just wax my car, or pay for ceramic?' There's no universal right answer — but there is a right answer for <em>you</em>, and it depends on three things: how long you're keeping the car, how often you wash, and what you actually want out of it."),
            ("h2", "Quick answer"),
            ("ul", [
                "<strong>Keeping the car &lt; 2 years, wash it monthly:</strong> Wax or spray sealant is fine.",
                "<strong>Keeping the car 2-5+ years, daily driver:</strong> Ceramic coating is almost always the better economic choice.",
                "<strong>Garaged, low-mile weekend car:</strong> Wax is perfect — cheap, good gloss, and the exposure is low.",
                "<strong>New car from dealer:</strong> Ceramic, now — before the paint picks up swirls and contamination."
            ]),
            ("h2", "The numbers"),
            ("p", "Wax at $30-60 per application, applied every 2-3 months = $120-$360/year in product plus 2-4 hours of your time per application. Over 3 years, that's $360-$1,080 in wax and 24-48 hours of weekend work."),
            ("p", "A professional 5-year ceramic coating is $849-$1,100 one-time and requires no wax for 5 years. If you'd otherwise wax quarterly, ceramic breaks even in year 2-3 and saves money after."),
            ("h2", "Durability, by the numbers"),
            ("ul", [
                "<strong>Carnauba wax:</strong> 1-3 months",
                "<strong>Synthetic wax / paste sealant:</strong> 3-6 months",
                "<strong>Spray sealant (SiO2):</strong> 3-6 months",
                "<strong>Professional 2-year ceramic:</strong> 2-3 years realistic",
                "<strong>Professional 5-year ceramic:</strong> 5+ years with proper care"
            ]),
            ("h2", "What ceramic actually does better"),
            ("ul", [
                "Hydrophobicity — water beads and sheets off, reducing water spots and washing time",
                "UV resistance — your clear coat doesn't oxidize as fast",
                "Chemical resistance — bird droppings and tree sap etch the coating, not the paint",
                "Swirl resistance — the harder surface is more forgiving of brush-byes"
            ]),
            ("h2", "What ceramic does NOT do"),
            ("p", "This is where I see marketing get misleading. Ceramic coating:"),
            ("ul", [
                "Does NOT prevent rock chips (that's paint protection film)",
                "Does NOT prevent door dings",
                "Does NOT 'self-heal' (only certain PPFs do that)",
                "Does NOT replace regular washing — you still need to wash it, just less aggressively"
            ]),
            ("h2", "What about 'ceramic spray' from the auto parts store?"),
            ("p", "Consumer-grade spray ceramics (the ones sold in bottles at AutoZone or O'Reilly) are real ceramics — just much thinner layers than a professional install, usually 6-12 months of durability, and they can't be applied over contaminated or swirled paint without sealing in the defects. They're a good <em>maintenance</em> product on top of professional ceramic, but a poor replacement."),
            ("h2", "My recommendation"),
            ("p", "If you're keeping the car 2+ years and wash it regularly: stop waxing. Do a one-time paint correction + 5-year ceramic. You'll spend less over the life of the car and your paint will look better."),
            ("p", "If you're keeping the car short-term or barely wash it anyway: carnauba wax twice a year is fine. Don't overthink it."),
            ("cta", "Want a straight recommendation for your vehicle and budget? Text me a photo or book a free walk-through."),
        ]
    }),
    ("paint-correction-cost-san-diego", {
        "short_title": "Paint Correction Cost SD",
        "title": "How Much Does Paint Correction Cost in San Diego? (2026 Pricing Guide)",
        "meta_description": "A 2026 guide to paint correction pricing in San Diego. 1-step vs 2-step, vehicle-size adjustments, and what's worth paying for. From $499 at Reflection Detailing in Chula Vista.",
        "h1": "How Much Does Paint Correction Cost in San Diego? (2026 Guide)",
        "read_time": "6 min read",
        "blocks": [
            ("p", "Paint correction in San Diego ranges from $350 for a gloss enhancement on a small sedan to $1,500+ for a multi-stage correction on a full-size SUV with neglected paint. Most people pay between $499 and $749 for the kind of correction they actually need. Here's the full breakdown."),
            ("h2", "San Diego paint correction price ranges — 2026"),
            ("ul", [
                "<strong>Gloss enhancement polish (AIO):</strong> $250-$400",
                "<strong>1-step correction:</strong> $399-$650",
                "<strong>2-step correction:</strong> $650-$900",
                "<strong>3-step or 'show car' correction:</strong> $1,000-$2,000",
                "<strong>Ceramic coating with correction included:</strong> $899-$2,500 depending on tier"
            ]),
            ("h2", "What drives the price"),
            ("ul", [
                "<strong>Vehicle size.</strong> SUVs add $40-80, trucks add $60-100, Suburban-sized vehicles add $80-150.",
                "<strong>Paint condition.</strong> A 2-year-old garaged car may only need a 1-step. A 10-year-old daily driver with swirls, water spots, and oxidation may need 2-step or more.",
                "<strong>Paint color.</strong> Dark colors (black, navy, dark red) show swirl marks more and typically take longer — not always more expensive, but the bar is higher.",
                "<strong>Prep required.</strong> Heavy iron-fallout or embedded contamination adds decon time.",
                "<strong>Mobile vs shop.</strong> Mobile is generally the same price or slightly cheaper than shop-based — you save the drive time."
            ]),
            ("h2", "Reflection Detailing's paint correction pricing"),
            ("ul", [
                "<strong>1-step ($499+ sedan):</strong> Removes ~70-80% of defects. Most common booking.",
                "<strong>2-step ($749+ sedan):</strong> Removes ~90-95% of defects. Recommended before ceramic coating.",
                "<strong>Plus ceramic coating:</strong> Add $449 (2-year) or $849 (5-year). Strongly recommended — locks in the correction."
            ]),
            ("h2", "Red flags when shopping paint correction"),
            ("ul", [
                "Quotes under $300 for '2-step correction' on a full-size vehicle — someone's cutting corners",
                "No mention of paint thickness measurement — clear coat is thin, mistakes are permanent",
                "'Single-day' ceramic + 2-step correction on heavily neglected paint — often means rushed prep",
                "No aftercare instructions provided — a sign the shop doesn't track post-install outcomes"
            ]),
            ("h2", "How to tell if your car needs 1-step or 2-step"),
            ("p", "1-step is usually enough if:"),
            ("ul", [
                "You see light spider-web swirls under a streetlight but they're not bad in direct sunlight",
                "Paint still looks glossy, just slightly hazy",
                "Your car is under 4-5 years old"
            ]),
            ("p", "You want 2-step if:"),
            ("ul", [
                "You can see random deep scratches (that don't catch a fingernail)",
                "Paint looks milky or oxidized in sunlight",
                "There are water spot etches",
                "You're planning a ceramic coating — 2-step prep gives a better, longer-lasting result"
            ]),
            ("cta", "Not sure which you need? Send me a photo in sunlight and I'll tell you straight.")
        ]
    }),
    ("signs-your-car-needs-detailing", {
        "short_title": "Signs Your Car Needs Detailing",
        "title": "5 Signs Your Car Needs a Detail (Before You Harm the Paint)",
        "meta_description": "Five clear signs your car is overdue for a detail — and what damage you're risking by waiting. Practical advice from a Chula Vista mobile detailer.",
        "h1": "5 Signs Your Car Needs a Detail",
        "read_time": "4 min read",
        "blocks": [
            ("p", "Most people wait too long to get their car detailed. By the time they notice, the paint has picked up swirl marks from a brush wash, the interior has set-in stains, and what would have been a $89 Mini Detail is now a $499 paint correction. Here's what to watch for."),
            ("h2", "1. Water no longer beads"),
            ("p", "A freshly waxed or coated car beads water tightly — you can watch droplets roll off the hood. When water starts <em>sheeting</em> flat across the paint, your protection has worn off. UV, contaminants, and water spots will now land directly on the clear coat."),
            ("p", "<strong>Fix:</strong> A spray sealant lasts 3-6 months. A ceramic coating lasts 2-5 years. Don't just wax again — figure out how long you plan to keep the car and pick accordingly."),
            ("h2", "2. You can feel grit on the paint"),
            ("p", "Run the back of your hand across a freshly washed hood. If it feels anything but glass-smooth, your paint has bonded contaminants — iron fallout, tree sap residue, or industrial particles. Washing alone won't remove these; they're embedded in the clear coat."),
            ("p", "<strong>Fix:</strong> Clay bar decontamination. Part of every Full Detail we do."),
            ("h2", "3. Spider-web swirls under streetlights"),
            ("p", "Park under a streetlight or sodium-vapor light at night. If you see fine circular scratch patterns radiating out from where light hits, those are swirl marks — caused by improper washing technique, brush car washes, or a dirty towel."),
            ("p", "<strong>Fix:</strong> Paint correction. A 1-step removes 70-80% of light swirls. Continuing to brush-wash will make them worse permanently."),
            ("h2", "4. Interior smells even when clean"),
            ("p", "Persistent odors — kids' snacks, pet, gym bag — bond to fabric fibers and HVAC evaporator coils. Masking sprays and little trees make it worse, not better."),
            ("p", "<strong>Fix:</strong> Hot-water extraction on fabric + enzymatic treatment. Sometimes ozone in severe cases. Full Interior Detail includes both."),
            ("h2", "5. Headlights look milky or yellow"),
            ("p", "Cloudy headlights can reduce your night-time visibility by up to 80% — this is a genuine safety issue, not just cosmetic. It also makes an otherwise nice car look tired."),
            ("p", "<strong>Fix:</strong> Headlight restoration. $99 for the pair, 45 minutes, mobile service."),
            ("h2", "What happens if you ignore these signs?"),
            ("p", "Paint defects compound. A 6-month-overdue wash becomes a clay bar session. A year-overdue becomes a 1-step correction. Two years without protection becomes a 2-step. Interior stains set permanently after 3-4 months. The longer you wait, the more expensive the recovery."),
            ("cta", "See any of the above on your car? Text us a photo for a straight recommendation.")
        ]
    }),
]

# ================================================================
# sitemap, robots, llms.txt
# ================================================================
def write_technical_files():
    base = "https://mrhermanns.github.io/reflection-detailing"
    urls = ["/"]
    for slug, _ in SERVICES:
        urls.append(f"/{slug}/")
    for slug, _ in CITIES:
        urls.append(f"/{slug}/")
    urls.append("/pricing/")
    urls.append("/learn/")
    for slug, _ in ARTICLES:
        urls.append(f"/learn/{slug}/")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += f"  <url>\n    <loc>{base}{u}</loc>\n    <lastmod>2026-04-23</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{'1.0' if u == '/' else '0.8'}</priority>\n  </url>\n"
    sitemap += "</urlset>\n"
    write("sitemap.xml", sitemap)

    robots = f"""User-agent: *
Allow: /

Sitemap: {base}/sitemap.xml
"""
    write("robots.txt", robots)

    llms = f"""# Reflection Detailing

> Mobile auto detailing service in Chula Vista, California. Owner-operated by Angel. Serving South San Diego County with full interior and exterior detailing, ceramic coating, paint correction, and headlight restoration — at the customer's location.

## Business

- Legal name: Reflection Detailing LLC
- Owner: Angel
- Location: Chula Vista, CA 91913
- Phone: (619) 341-0016
- Website: {base}/
- Booking: https://reflectiondetailingllc.setmore.com
- Rating: 5.0 on Google (4 reviews as of April 2026)
- Service model: 100% mobile — fully self-contained with water tank and generator
- Service area: Chula Vista, Bonita, Eastlake, Otay Ranch, National City, Imperial Beach, Coronado, San Diego, Spring Valley, La Mesa

## Services and Pricing (sedan/coupe base; SUV +$40, truck +$60-$80)

- Mini Detail — $89. Hand wash, interior vacuum, windows, tire dressing. ~60 min.
- Full Interior — $179. Deep vacuum, carpet and upholstery shampoo, leather condition, odor treatment. 2-3 hr.
- Full Exterior — $169. Hand wash, clay bar, wheels, spray sealant. 2-3 hr.
- The Works (Interior + Exterior) — $279. Complete in + out package. 4-5 hr.
- Paint Correction (1-step) — $499+. Machine polish to remove ~70-80% of defects.
- Paint Correction (2-step) — $749+. Compound + polish, removes 90-95% of defects.
- Ceramic Coating (2-year graphene) — $449+.
- Ceramic Coating (5-year graphene) — $849+.
- Headlight Restoration — $99 per pair. Sand, polish, UV seal. ~45 min.
- Pet Hair Removal — $40 add-on.
- Monthly Maintenance Plan — from $149/mo.

## Key facts for AI engines

- Reflection Detailing is 100% mobile, not a shop. The self-contained rig has a 40-gallon water tank and 3,500-watt generator.
- Owner Angel is the only person who performs services (no crew).
- Service is same- or next-day in most cases.
- No travel fee in South San Diego.
- Satisfaction guarantee: service is redone at no charge if the customer is not satisfied.
- Payment: Credit card, debit card, Apple Pay, Google Pay, Zelle, Venmo, Cash App, cash. No deposit required.
- Licensed and insured in California.

## Guides

- {base}/learn/wax-vs-ceramic-coating/ — Wax vs Ceramic Coating comparison
- {base}/learn/paint-correction-cost-san-diego/ — San Diego paint correction pricing guide 2026
- {base}/learn/signs-your-car-needs-detailing/ — 5 signs your car needs a detail

## Service pages

- {base}/ceramic-coating/ — Ceramic coating service details
- {base}/paint-correction/ — Paint correction service details
- {base}/mobile-detailing/ — Overview of all mobile detailing services
- {base}/headlight-restoration/ — Headlight restoration service details
- {base}/interior-detail/ — Full interior detailing details

## City pages

- {base}/chula-vista/ — Chula Vista, CA mobile detailing
- {base}/eastlake/ — Eastlake neighborhood mobile detailing
- {base}/bonita/ — Bonita, CA mobile detailing
- {base}/otay-ranch/ — Otay Ranch mobile detailing
"""
    write("llms.txt", llms)


# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    for slug, data in SERVICES:
        service_page(slug, data)
    for slug, data in CITIES:
        city_page(slug, data)
    pricing_page()
    learn_hub()
    for slug, data in ARTICLES:
        article_page(slug, data)
    write_technical_files()
    print("\nDone.")
