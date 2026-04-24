#!/usr/bin/env python3
"""
Static-site page generator for Reflection Detailing.
Builds service pages, city pages, content pages, and technical SEO files
from shared templates + a data dict. All output goes into the repo root
so GitHub Pages serves each as /<slug>/.
"""
import os
import json
import textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "https://mrhermanns.github.io/reflection-detailing"
BRAND = "Reflection Detailing"
PHONE_DISPLAY = "(619) 341-0016"
PHONE_TEL = "+16193410016"
SETMORE_URL = "https://reflectiondetailingllc.setmore.com"
CITY = "Chula Vista"

# ---------------- Shared fragments ----------------

def common_head(title, description, canonical_path, og_title=None, keywords=""):
    canonical = f"{BASE_URL}/{canonical_path}".rstrip("/") + "/"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
<meta name="theme-color" content="#0f172a" />
<title>{title}</title>
<meta name="description" content="{description}" />
<meta name="keywords" content="{keywords}" />
<link rel="canonical" href="{canonical}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{og_title or title}" />
<meta property="og:description" content="{description}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:image" content="{BASE_URL}/photos/4runner-exterior-after.jpg?v=3" />
<meta name="twitter:card" content="summary_large_image" />
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='19' fill='%23f59e0b'/%3E%3Cpath d='M13 29 V11 h8.5 a5 5 0 0 1 0 10 H17 l6 8 h-4 l-6-8 Z' fill='%230f172a'/%3E%3Ccircle cx='29' cy='13' r='2.2' fill='%23fff' opacity='.85'/%3E%3C/svg%3E" />
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{ theme: {{ extend: {{
    colors: {{ ink: '#0f172a', accent: '#f59e0b' }},
    fontFamily: {{ sans: ['system-ui','-apple-system','Segoe UI','Roboto','Helvetica','Arial','sans-serif'] }}
  }} }} }}
</script>
<style>
  html {{ scroll-behavior: smooth; }}
</style>
"""

def local_business_schema():
    return """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AutoDetailing",
  "name": "Reflection Detailing",
  "description": "Mobile auto detailing service in Chula Vista, CA. IGL Coatings Certified and HTL Detailing Certified. Ceramic coating, paint correction, headlight restoration, and full interior and exterior detailing.",
  "image": "https://mrhermanns.github.io/reflection-detailing/photos/4runner-exterior-after.jpg?v=3",
  "url": "https://mrhermanns.github.io/reflection-detailing/",
  "telephone": "+1-619-341-0016",
  "priceRange": "$$",
  "address": { "@type": "PostalAddress", "addressLocality": "Chula Vista", "addressRegion": "CA", "postalCode": "91913", "addressCountry": "US" },
  "geo": { "@type": "GeoCoordinates", "latitude": 32.6252, "longitude": -116.993 },
  "areaServed": ["Chula Vista, CA","Bonita, CA","Eastlake, CA","Otay Ranch, CA","National City, CA","Imperial Beach, CA","Coronado, CA","San Diego, CA","Spring Valley, CA","La Mesa, CA"],
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "09:00", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "07:00", "closes": "18:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "07:00", "closes": "14:00" }
  ],
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "4" },
  "paymentAccepted": "Cash, Credit Card, Debit Card, Apple Pay, Google Pay, Zelle, Venmo",
  "hasCredential": [
    { "@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "IGL Coatings Certified Installer", "recognizedBy": { "@type": "Organization", "name": "IGL Coatings" } },
    { "@type": "EducationalOccupationalCredential", "credentialCategory": "certification", "name": "Paint Correction Certification", "recognizedBy": { "@type": "Organization", "name": "HTL Detailing" } }
  ]
}
</script>"""

def breadcrumb_schema(items):
    # items: list of (name, url_path)
    itemlist = ",\n    ".join(
        f'{{ "@type": "ListItem", "position": {i+1}, "name": "{name}", "item": "{BASE_URL}/{path}".rstrip("/") }}'
        for i, (name, path) in enumerate(items)
    )
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {itemlist}
  ]
}}
</script>"""

def breadcrumb_html(items, depth=1):
    # items: list of (name, url_path) — last is current
    rel = "../" * depth
    parts = []
    for i, (name, path) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span class="text-slate-500">{name}</span>')
        elif path == "":
            parts.append(f'<a href="{rel}" class="hover:text-accent">{name}</a>')
        else:
            parts.append(f'<a href="{rel}{path}/" class="hover:text-accent">{name}</a>')
    return '<nav aria-label="Breadcrumb" class="text-sm text-slate-600 mb-6">' + ' <span class="text-slate-400">/</span> '.join(parts) + '</nav>'

def header_html(depth=1):
    rel = "../" * depth
    return f"""<header class="sticky top-0 z-40 bg-ink/95 backdrop-blur text-white">
  <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
    <a href="{rel}" class="flex items-center gap-2 font-black tracking-tight text-lg">
      <svg viewBox="0 0 40 40" class="w-9 h-9" aria-hidden="true">
        <circle cx="20" cy="20" r="19" fill="#f59e0b"/>
        <path d="M13 29 V11 h8.5 a5 5 0 0 1 0 10 H17 l6 8 h-4 l-6-8 Z" fill="#0f172a"/>
        <circle cx="29" cy="13" r="2.2" fill="#fff" opacity=".85"/>
      </svg>
      <span>Reflection Detailing</span>
    </a>
    <nav class="hidden md:flex items-center gap-5 text-sm">
      <a href="{rel}#services" class="hover:text-accent">Services</a>
      <a href="{rel}#process" class="hover:text-accent">How It Works</a>
      <a href="{rel}#about" class="hover:text-accent">About</a>
      <a href="{rel}#area" class="hover:text-accent">Service Area</a>
      <a href="{rel}#faq" class="hover:text-accent">FAQ</a>
      <a href="{rel}#reviews" class="hover:text-accent">Reviews</a>
    </nav>
    <a href="{SETMORE_URL}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-4 py-2 rounded-lg hover:opacity-90 text-sm">Book</a>
  </div>
</header>"""

def cta_strip():
    return f"""<section class="bg-ink text-white py-12">
  <div class="max-w-3xl mx-auto px-4 text-center">
    <h2 class="text-2xl md:text-3xl font-black mb-3">Ready to book?</h2>
    <p class="text-slate-300 mb-6">Mobile service across Chula Vista and South San Diego. Self-contained. Satisfaction guaranteed.</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="{SETMORE_URL}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-6 py-3 rounded-lg hover:opacity-90">Book Online</a>
      <a href="sms:{PHONE_TEL}" class="bg-white/10 border border-white/30 text-white font-bold px-6 py-3 rounded-lg hover:bg-white/20">Text {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>"""

def footer_html(depth=1):
    rel = "../" * depth
    return f"""<footer class="bg-slate-900 text-slate-400 text-sm">
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
      <p>Mobile auto detailing in Chula Vista & South San Diego.</p>
      <p class="mt-2 text-xs">IGL Coatings Certified · HTL Detailing Certified</p>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Services</p>
      <ul class="space-y-1">
        <li><a href="{rel}mobile-detailing/" class="hover:text-accent">Mobile Detailing</a></li>
        <li><a href="{rel}ceramic-coating/" class="hover:text-accent">Ceramic Coating</a></li>
        <li><a href="{rel}paint-correction/" class="hover:text-accent">Paint Correction</a></li>
        <li><a href="{rel}interior-detail/" class="hover:text-accent">Interior Detail</a></li>
        <li><a href="{rel}headlight-restoration/" class="hover:text-accent">Headlight Restoration</a></li>
      </ul>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Service Areas</p>
      <ul class="space-y-1">
        <li><a href="{rel}chula-vista/" class="hover:text-accent">Chula Vista</a></li>
        <li><a href="{rel}eastlake/" class="hover:text-accent">Eastlake</a></li>
        <li><a href="{rel}bonita/" class="hover:text-accent">Bonita</a></li>
        <li><a href="{rel}otay-ranch/" class="hover:text-accent">Otay Ranch</a></li>
        <li><a href="{rel}coronado/" class="hover:text-accent">Coronado</a></li>
        <li><a href="{rel}national-city/" class="hover:text-accent">National City</a></li>
        <li><a href="{rel}imperial-beach/" class="hover:text-accent">Imperial Beach</a></li>
        <li><a href="{rel}san-diego/" class="hover:text-accent">San Diego</a></li>
      </ul>
    </div>
    <div>
      <p class="font-bold text-white mb-2">Contact</p>
      <p><a href="tel:{PHONE_TEL}" class="hover:text-accent">{PHONE_DISPLAY}</a></p>
      <p>Chula Vista, CA 91913</p>
      <p class="mt-3 font-bold text-white mb-1">Resources</p>
      <ul class="space-y-1">
        <li><a href="{rel}pricing/" class="hover:text-accent">Pricing</a></li>
        <li><a href="{rel}learn/" class="hover:text-accent">Detailing Guides</a></li>
      </ul>
    </div>
  </div>
  <div class="border-t border-slate-800 py-4 text-center">
    © <script>document.write(new Date().getFullYear())</script> Reflection Detailing LLC. All rights reserved.
  </div>
</footer>"""

# ---------------- Page data ----------------

SERVICE_PAGES = [
    {
        "slug": "ceramic-coating",
        "name": "Ceramic Coating",
        "price_from": "$449",
        "h1": "Mobile Ceramic Coating in Chula Vista, CA",
        "tagline": "IGL Coatings Certified · 2-year, 5-year, and 9-year options",
        "keywords": "ceramic coating chula vista, mobile ceramic coating san diego, IGL coatings installer, graphene ceramic coating",
        "description": "IGL Coatings Certified mobile ceramic coating in Chula Vista, CA. 2-year to 9-year protection. We come to your driveway. From $449. Call (619) 341-0016.",
        "intro": "A ceramic coating is the strongest paint protection available short of a full PPF. We're IGL Coatings Certified installers — that means the coating is applied to manufacturer spec, backed by the warranty, and performs exactly as advertised. Mobile service, self-contained, anywhere in South Bay.",
        "benefits": [
            ("Years of protection", "IGL ceramic coatings last 2 to 9 years depending on tier. Wax lasts 1-3 months. Do the math."),
            ("Hydrophobic shine", "Water beads up and rolls off. Dirt, mud, and road grime have nothing to grip."),
            ("UV + chemical resistance", "Protects against bird droppings, tree sap, bug splatter, and the relentless San Diego sun."),
            ("Easier washing forever", "Coated paint washes clean in half the time. No more scrubbing bonded contaminants."),
            ("Certified application", "IGL products applied by an IGL-trained installer. Uncertified shops buy generic coatings and wing it. We don't."),
            ("Full paint prep included", "Every coating job includes wash, decontamination, clay bar, and 1-step or 2-step paint correction as needed. The coating is only as good as the paint underneath.")
        ],
        "process": [
            ("Book + Prep Consult", "Text or book online. We confirm vehicle size, condition, and the right coating tier for your needs."),
            ("Arrival + Full Wash", "We arrive with the full rig. Hand wash, iron decon, tar removal, clay bar."),
            ("Paint Correction", "Machine polish to remove swirl marks and defects. Required for proper coating bond."),
            ("Panel Wipe + Coating", "Every panel wiped with IPA. IGL ceramic applied by panel, leveled, inspected."),
            ("Cure + Final Inspection", "Coating flashes for 20-30 minutes per panel. We walk the finished vehicle with you before leaving."),
        ],
        "pricing_rows": [
            ("2-year Graphene Ceramic", "$449+", "Best value entry tier. Hydrophobic, gloss boost, UV protection. Sedan/coupe base."),
            ("5-year Premium Graphene", "$849+", "Paint correction + premium IGL coating. Our most popular package."),
            ("9-year Flagship IGL", "$1,499+", "Longest-lasting option. Full 2-step correction + top-tier IGL coating with warranty documentation."),
            ("Glass Coating Add-On", "+$129", "Hydrophobic coating on all windows. Rain sheets off — no wipers needed at speed."),
            ("Wheel Face Coating", "+$149", "Ceramic on wheel faces. Brake dust wipes off with a damp cloth. Huge time-saver."),
            ("Leather / Trim Coating", "+$99 / +$79", "Protects interior surfaces from UV fading and stains."),
        ],
        "faq": [
            ("Is a ceramic coating really worth it?",
             "If you're keeping the car more than 2 years, yes. A 5-year IGL coating at $849 equals about $170/year for paint that looks showroom-fresh, washes faster, and resists environmental damage. A $100 annual wax gets you worse protection for more money."),
            ("Can I wash my car after a ceramic coating?",
             "Yes — and it's easier than before. Wait 7 days after application before the first wash. After that, any standard hand-wash method works. Avoid automatic car washes with rotating brushes."),
            ("Do I still need to wax after ceramic coating?",
             "No. A ceramic coating replaces wax entirely for the duration of its lifespan. Adding wax on top is a waste of product."),
            ("Why pay for an IGL Coatings Certified installer?",
             "IGL-certified installers are trained directly by IGL on their specific product line, application technique, and surface prep. Uncertified shops often substitute cheaper coatings — you pay for IGL pricing but get unknown chemistry. With a certified installer, what you pay for is what goes on your car, period."),
            ("How long does ceramic coating take?",
             "A full coating job with paint correction takes 6-8 hours on-site. We start early and work through the day."),
        ],
        "also_see": [("paint-correction", "Paint Correction"), ("mobile-detailing", "Mobile Detailing"), ("headlight-restoration", "Headlight Restoration")],
        "photos": [
            ("photos/4runner-exterior-after.jpg?v=3", "Toyota 4Runner with deep metallic blue gloss after ceramic coating in Chula Vista", "Coated finish on a 4Runner"),
            ("photos/wheel-after.jpg?v=3", "Clean polished wheel after ceramic coating protection", "Ceramic-protected wheel"),
        ],
    },
    {
        "slug": "paint-correction",
        "name": "Paint Correction",
        "price_from": "$499",
        "h1": "Paint Correction in Chula Vista & South San Diego",
        "tagline": "HTL Detailing Certified · 1-step and 2-step machine polishing",
        "keywords": "paint correction chula vista, paint correction san diego, swirl mark removal, machine polish",
        "description": "HTL Detailing Certified paint correction in Chula Vista. Remove swirl marks, scratches, oxidation. Mobile service. From $499. Book online or call (619) 341-0016.",
        "intro": "Paint correction physically removes a micro-thin layer of clear coat to eliminate swirl marks, light scratches, water spots, and oxidation. The result is depth, clarity, and gloss that no wax or spray sealant can fake. We're HTL Detailing Certified — formal training on compound selection, pad matching, and paint-thickness-safe polishing.",
        "benefits": [
            ("Visible swirl + scratch removal", "1-step corrects 60-70% of defects. 2-step handles 80-95% including deeper scratches."),
            ("Paint depth restored", "Corrected paint looks wet — the difference is immediately visible in direct sunlight."),
            ("Prepped for coating", "Paint correction is REQUIRED before ceramic coating. Coating locks in defects if you skip this step."),
            ("Paint-safe process", "Certified technique and paint thickness gauges ensure we never remove more clear coat than is safe."),
            ("Long-lasting results", "Corrected paint stays corrected for years. Only proper wash technique is needed to maintain it."),
        ],
        "process": [
            ("Paint Inspection + Test Spot", "We assess defects, measure paint thickness, and run a test spot to confirm the right compound + pad combo."),
            ("Full Decontamination", "Iron remover, tar remover, clay bar. Nothing on the paint but the paint itself."),
            ("1-Step or 2-Step Polishing", "Machine polish by panel. Each panel inspected under 3000K light before moving on."),
            ("Panel Wipe + Gloss Check", "IPA wipe removes polishing oils to verify true correction level, not filler masking."),
            ("Protection Applied", "Spray sealant included. Ceramic coating available as upgrade."),
        ],
        "pricing_rows": [
            ("1-Step Correction", "$499+", "Removes light-to-moderate swirls, marring, oxidation. Sedan/coupe base. Adds 2-3 hours to any detail."),
            ("2-Step Correction", "$749+", "Compound + polish for heavier defects. 80-95% defect removal."),
            ("3-Step Correction", "$999+", "Heavy compound + polish + final finish. Show-car-level work."),
            ("Wet Sand (severe defects)", "Quote", "For deep scratches that polishing alone won't fix. Priced per panel after inspection."),
        ],
        "faq": [
            ("How do I know if I need paint correction?",
             "Look at your paint in direct sunlight. If you see spider-web swirls, cloudy hazing, or halos around light scratches, your paint needs correction. Most daily drivers collect noticeable swirls within 1-2 years."),
            ("Is paint correction safe?",
             "Yes, when done by a certified professional with paint-thickness gauges. We measure your specific paint thickness before polishing to ensure we never remove more clear coat than is safe. Uncertified shops often over-polish and burn through clear coat."),
            ("How long does paint correction last?",
             "The correction itself is permanent — those swirls are gone forever. New swirls can develop from improper washing, so we recommend proper wash technique and an optional ceramic coating to lock in the results."),
            ("Do I need paint correction before a ceramic coating?",
             "Yes. Ceramic coating is transparent — it seals in whatever is underneath. If you skip correction, any existing swirls and defects get permanently locked under the coating. Every one of our ceramic jobs includes at minimum a 1-step correction for this reason."),
            ("What is the difference between polish and compound?",
             "Compound is more abrasive — it cuts deeper to remove heavier defects. Polish is finer — it refines and adds gloss. A 2-step uses both in sequence."),
        ],
        "also_see": [("ceramic-coating", "Ceramic Coating"), ("mobile-detailing", "Mobile Detailing"), ("headlight-restoration", "Headlight Restoration")],
        "photos": [
            ("photos/accord-paint-headlight-before.jpg?v=3", "Honda Accord before paint correction — oxidized paint and cloudy headlight", "BEFORE paint correction"),
            ("photos/accord-paint-headlight-after.jpg?v=3", "Same Honda Accord after paint correction — restored gloss and clear headlights", "AFTER paint correction"),
        ],
    },
    {
        "slug": "mobile-detailing",
        "name": "Mobile Detailing",
        "price_from": "$89",
        "h1": "Mobile Auto Detailing — Chula Vista & South San Diego",
        "tagline": "We come to you. Self-contained. No hose, no outlet, no mess.",
        "keywords": "mobile detailing chula vista, mobile car detailing san diego, mobile auto detailing near me, south bay mobile detailing",
        "description": "Mobile auto detailing in Chula Vista and the South Bay. Self-contained with water and power. Mini Detail from $89, Full Detail $279. (619) 341-0016.",
        "intro": "Mobile detailing means we bring the shop to your driveway, office, or jobsite. Our rig carries a 40-gallon water tank, a 3,500-watt generator, and every tool and chemistry we need to detail a car to shop-level standards. You park, we show up, you get a detailed car without ever leaving home.",
        "benefits": [
            ("Zero driving for you", "Stay home, stay at work, stay on the golf course. We come to you."),
            ("Self-contained rig", "We bring our own water and power. All you provide is the parking space."),
            ("Same pricing as a shop", "Our mobile pricing matches shop pricing — no travel fee anywhere in South Bay."),
            ("Same-day availability", "Text for fastest response. Most days we can fit you in within 24-48 hours."),
            ("Satisfaction guarantee", "Every appointment ends with a walk-around inspection. Not happy? We fix it on the spot."),
        ],
        "process": [
            ("Book Online or Text", "Pick a service + time. No deposit required."),
            ("Arrive on Time", "We pull up with the rig, water, and tools."),
            ("Detail in Place", "Full detail performed at your location. Typical times 60 min to full day."),
            ("Walk-Around + Pay", "We inspect the finished vehicle with you before accepting payment."),
        ],
        "pricing_rows": [
            ("Mini Detail", "$89", "Hand wash, vacuum, windows, tire dressing. ~60 min."),
            ("Full Interior", "$179", "Deep vacuum, shampoo, leather, UV protect. 2-3 hrs."),
            ("Full Exterior", "$169", "Hand wash, clay bar, wheels, sealant. 2-3 hrs."),
            ("The Works — In + Out", "$279", "Full interior AND exterior. Our most popular. 4-5 hrs."),
            ("Monthly Maintenance", "$149/mo", "2 mini details per month. Best value for daily drivers."),
        ],
        "faq": [
            ("What do you need from me at my location?",
             "A parking space with ~10 ft clearance around the vehicle, and that's it. We bring water, power, and everything else."),
            ("How far will you travel?",
             "We cover Chula Vista, Bonita, Eastlake, Otay Ranch, National City, Imperial Beach, Coronado, Spring Valley, La Mesa, Lemon Grove, and most of South San Diego at no travel fee."),
            ("Do you service apartment parking lots?",
             "Yes, with permission from property management. We've worked in Eastlake, Otay Ranch, and Chula Vista apartment complexes many times."),
            ("Can you detail my car while I'm at work?",
             "Absolutely. We drop by your office parking lot, text you when done, and you come out to a detailed car."),
        ],
        "also_see": [("ceramic-coating", "Ceramic Coating"), ("paint-correction", "Paint Correction"), ("interior-detail", "Interior Detail")],
        "photos": [
            ("photos/angel-mustang-foam-wash.jpg?v=3", "Angel, owner of Reflection Detailing, foam-washing a Mustang in Chula Vista", "Angel on-site with a customer's Mustang"),
            ("photos/4runner-exterior-after.jpg?v=3", "Finished 4Runner exterior detail in Chula Vista", "Finished result — brought to your driveway"),
        ],
    },
    {
        "slug": "headlight-restoration",
        "name": "Headlight Restoration",
        "price_from": "$99 / pair",
        "h1": "Mobile Headlight Restoration in Chula Vista",
        "tagline": "Cloudy headlights? Clear + UV-sealed in 45 minutes.",
        "keywords": "headlight restoration chula vista, cloudy headlight repair san diego, headlight restoration near me",
        "description": "Mobile headlight restoration in Chula Vista. Sanded, polished, UV-sealed in 45 min. $99/pair. Improves nighttime visibility and resale value.",
        "intro": "Oxidized, yellowed, or cloudy headlights don't just look bad — they reduce nighttime visibility by up to 80%. Our mobile restoration service sands away the damage, polishes the plastic clear, and seals with a UV-blocking coating so the results last.",
        "benefits": [
            ("Clearer vision at night", "Restored headlights throw significantly more light on dark roads. Safer driving, period."),
            ("Massive curb appeal", "Headlights are the first thing people notice on a car. Clear lenses shave years off how old it looks."),
            ("Cheaper than replacement", "OEM headlight assemblies run $300-$1,500+. A restoration is $99/pair and lasts 1-3 years with sealer."),
            ("Mobile, 45 minutes", "We come to you. You can work or relax while we do it."),
            ("UV sealer included", "Most shops skip the UV seal — the lenses re-yellow in months. We include it on every job."),
        ],
        "process": [
            ("Tape + Mask", "We protect surrounding paint with automotive tape."),
            ("Wet Sand (3 grits)", "Progressive wet sanding removes the oxidized layer."),
            ("Polish to Clarity", "Machine polish restores optical clarity."),
            ("UV Seal Coating", "Final UV-blocking sealer applied — the part most shops skip."),
        ],
        "pricing_rows": [
            ("Headlight Restoration (pair)", "$99", "Both headlights, sanded + polished + sealed. ~45 min."),
            ("Single Headlight", "$59", "One headlight if only one is cloudy."),
            ("Add to Full Detail", "+$79", "Discounted when bundled with a Full Detail or The Works."),
        ],
        "faq": [
            ("How long does the restoration last?",
             "With the UV sealer, clear for 1-3 years depending on sun exposure and parking situation. Garaged vehicles go longer."),
            ("Can oxidized headlights really reduce visibility that much?",
             "Yes. AAA studies show heavy oxidation can cut headlight output by over 80%. That's a major safety issue, especially on the I-805 at night."),
            ("Does restoration work on severely damaged lenses?",
             "If the damage is internal (water intrusion, cracks) we can't fix it — replacement is needed. But if it's the outer plastic layer that's cloudy or yellow, restoration works."),
            ("Will this pass smog / inspection?",
             "Clear headlights won't affect smog. They will help pass any visibility-related inspection."),
        ],
        "also_see": [("mobile-detailing", "Mobile Detailing"), ("paint-correction", "Paint Correction"), ("ceramic-coating", "Ceramic Coating")],
        "photos": [
            ("photos/accord-paint-headlight-before.jpg?v=3", "Honda Accord with oxidized, cloudy headlights before restoration", "BEFORE — cloudy headlights"),
            ("photos/accord-paint-headlight-after.jpg?v=3", "Same Honda Accord after headlight restoration — clear and UV-sealed", "AFTER — clear and UV-sealed"),
        ],
    },
    {
        "slug": "interior-detail",
        "name": "Interior Detail",
        "price_from": "$179",
        "h1": "Full Interior Car Detail — Mobile, in Chula Vista",
        "tagline": "Deep clean, shampoo, condition, protect. Pet hair, stains, odors — gone.",
        "keywords": "interior car detailing chula vista, car interior cleaning san diego, upholstery shampoo, pet hair removal car",
        "description": "Full interior car detailing at your location in Chula Vista. Deep vacuum, upholstery shampoo, leather condition, UV protect. From $179.",
        "intro": "A Full Interior Detail is the reset button for your car's interior. We vacuum every crevice, extract upholstery, shampoo carpets, condition leather, deodorize, UV-protect trim, and polish glass. Whether it's kid-juice, pet hair, or years of accumulated road dust, we handle it.",
        "benefits": [
            ("Hot-water extraction", "Our extractors pull dirt and stains out of fabric at depth — not just surface wipe-down."),
            ("Leather-safe chemistry", "pH-balanced cleaners and conditioners keep leather supple and UV-protected."),
            ("Pet hair removal", "Specialized rubber extractors for embedded hair. $40 add-on when needed."),
            ("Odor neutralization", "Enzymatic treatments break down odor molecules, not just mask them."),
            ("Stain treatment", "Coffee, juice, ink, makeup — most stains come out with the right chemistry."),
        ],
        "process": [
            ("Full Vacuum", "Every crevice, under seats, air vents, trunk. We go everywhere."),
            ("Shampoo + Extract", "Carpet and upholstery deep-cleaned with hot water extraction."),
            ("Leather / Vinyl / Plastic", "Each surface cleaned with appropriate chemistry, then conditioned and UV-protected."),
            ("Glass + Finish", "Interior glass streak-free. Dash dressed. Final inspection."),
        ],
        "pricing_rows": [
            ("Full Interior Detail", "$179", "Sedan/coupe base. 2-3 hours."),
            ("Pet Hair Removal", "+$40", "Specialized extraction for embedded pet hair."),
            ("Odor Treatment", "+$49", "Enzymatic deep treatment for persistent odors."),
            ("Child Seat Removal + Clean", "+$29", "We'll uninstall, clean under, and reinstall child seats."),
        ],
        "faq": [
            ("Will shampooing make my carpets wet for days?",
             "No. Our hot-water extractors remove most of the moisture on pass. Interior is usually dry enough to sit in within 1-2 hours. Fully dry within 4-6."),
            ("Can you get rid of pet smell?",
             "Usually yes. Our enzymatic treatments break down the proteins that cause odor. Severe cases (urine, skunk) may need a 2-visit process."),
            ("How much pet hair is too much?",
             "We've seen it all. As long as there's fabric underneath, we can extract the hair."),
            ("Do you clean child seats?",
             "We clean around them. If you want them removed for deeper access, it's a $29 add-on — we uninstall, clean, and reinstall properly."),
        ],
        "also_see": [("mobile-detailing", "Mobile Detailing"), ("paint-correction", "Paint Correction"), ("ceramic-coating", "Ceramic Coating")],
        "photos": [
            ("photos/interior-seats-before.jpg?v=3", "Honda Accord back seats before interior detail — debris and stains", "BEFORE — interior seats"),
            ("photos/interior-seats-after.jpg?v=3", "Same Honda Accord back seats after full interior detail — spotless", "AFTER — interior seats"),
        ],
    },
]

CITY_PAGES = [
    {
        "slug": "chula-vista",
        "name": "Chula Vista",
        "zips": "91910, 91911, 91913, 91914, 91915",
        "neighborhoods": ["Eastlake", "Otay Ranch", "Rolling Hills Ranch", "Bonita", "Third Avenue"],
        "lat": 32.6401,
        "lng": -117.0842,
        "h1": "Mobile Auto Detailing in Chula Vista, CA",
        "description": "Mobile auto detailing across all Chula Vista zip codes. IGL Coatings Certified. Ceramic coating, paint correction, full details. From $89. (619) 341-0016.",
        "keywords": "mobile detailing chula vista, car detailing chula vista 91913, ceramic coating chula vista, auto detailing near me",
        "intro": "Chula Vista is home base. Reflection Detailing operates out of Chula Vista 91913 and covers every zip code in the city with no travel fee. Whether you're in Eastlake with a new Tesla, in Otay Ranch with a family SUV, or in Third Avenue with a project car, we'll come to your driveway or office with a fully self-contained rig and detail the vehicle on-site.",
        "local_seo": [
            "Fastest response times in the city — most Chula Vista bookings confirmed same-day.",
            "Familiar with all major Chula Vista gated communities and apartment complexes.",
            "Parking is rarely an issue in Chula Vista; most driveways accommodate our rig.",
            "Serves all Chula Vista zip codes: 91910, 91911, 91913, 91914, 91915.",
        ],
        "popular_services": ["The Works — Interior + Exterior", "Ceramic Coating", "Paint Correction"],
    },
    {
        "slug": "eastlake",
        "name": "Eastlake",
        "zips": "91914, 91915 (within Chula Vista)",
        "neighborhoods": ["Eastlake Greens", "Eastlake Vistas", "Eastlake Trails", "Eastlake Hills", "Rolling Hills Ranch"],
        "lat": 32.6509,
        "lng": -116.9692,
        "h1": "Mobile Detailing in Eastlake, Chula Vista",
        "description": "Mobile auto detailing in Eastlake — Eastlake Greens, Vistas, Trails, and Hills. IGL-certified ceramic coating. Full details from $89. (619) 341-0016.",
        "keywords": "eastlake car detailing, eastlake chula vista detailer, mobile detailing eastlake, ceramic coating eastlake",
        "intro": "Eastlake is one of our busiest service areas. The community's mix of luxury vehicles, family SUVs, and enthusiast cars means we see everything from Tesla Model Ys to lifted 4Runners to show-condition exotics. Every Eastlake detail gets the same self-contained mobile setup — we pull up to your driveway or complex, set up in the designated space, and you get a showroom-clean car without leaving home.",
        "local_seo": [
            "Coverage across Eastlake Greens, Eastlake Vistas, Eastlake Trails, Eastlake Hills, Rolling Hills Ranch, and surrounding developments.",
            "Experienced with HOA rules and gate access coordination across Eastlake communities.",
            "Frequent ceramic coating bookings from Eastlake — IGL-Certified installation means warranty-backed results.",
        ],
        "popular_services": ["Ceramic Coating", "Paint Correction", "The Works — Interior + Exterior"],
    },
    {
        "slug": "bonita",
        "name": "Bonita",
        "zips": "91902, 91908",
        "neighborhoods": ["Sweetwater", "Rancho Del Rey", "Bonita Long Canyon", "Bonita Village"],
        "lat": 32.6577,
        "lng": -117.0320,
        "h1": "Mobile Car Detailing in Bonita, CA",
        "description": "Mobile auto detailing in Bonita, CA. Ceramic coating, paint correction, full details at your door. IGL Coatings Certified. From $89. (619) 341-0016.",
        "keywords": "bonita car detailing, bonita mobile detailer, ceramic coating bonita, paint correction bonita",
        "intro": "Bonita is home to some of the most beautiful vehicles in South Bay — and some of the most demanding owners. We handle luxury vehicles, collector cars, and everyday drivers with the same level of care. Our mobile rig means your Porsche, your G-Wagon, or your classic Camaro never leaves your garage — we bring the detail to the car.",
        "local_seo": [
            "Luxury and performance vehicle specialists — comfortable handling exotics, collector cars, and daily drivers.",
            "IGL Coatings Certified installation for premium ceramic coating demands.",
            "Familiar with Bonita gated communities and private estates.",
            "Bonita zip codes covered: 91902, 91908, plus neighboring Rancho Del Rey.",
        ],
        "popular_services": ["Ceramic Coating (5-year + 9-year tiers)", "2-Step Paint Correction", "The Works — Interior + Exterior"],
    },
    {
        "slug": "otay-ranch",
        "name": "Otay Ranch",
        "zips": "91913, 91914, 91915",
        "neighborhoods": ["Otay Ranch Town Center area", "Millenia", "Eastern Chula Vista", "Windingwalk"],
        "lat": 32.6280,
        "lng": -116.9706,
        "h1": "Mobile Auto Detailing in Otay Ranch, Chula Vista",
        "description": "Mobile auto detailing in Otay Ranch. Self-contained rig, no travel fee. IGL Coatings Certified. Ceramic coating, paint correction, full details. (619) 341-0016.",
        "keywords": "otay ranch car detailing, mobile detailing otay ranch, ceramic coating otay ranch, millenia chula vista detailer",
        "intro": "Otay Ranch is one of the fastest-growing communities in South Bay, and we've detailed cars everywhere from the Otay Ranch Town Center residences to Millenia to Windingwalk. Mobile service fits Otay Ranch life — busy families, dual-income households, tight schedules. We show up when you're home or at work, detail the vehicle, and you pay when satisfied.",
        "local_seo": [
            "Covers all Otay Ranch subdivisions: Millenia, Windingwalk, Heritage, Village areas.",
            "Zip codes served at no travel fee: 91913, 91914, 91915.",
            "Experienced with Otay Ranch HOA guidelines for on-property service work.",
            "Most popular in Otay Ranch: Full Detail + Monthly Maintenance plans for family vehicles.",
        ],
        "popular_services": ["The Works — Interior + Exterior", "Monthly Maintenance Plan", "Interior Detail (pet hair + stains)"],
    },
    {
        "slug": "coronado",
        "name": "Coronado",
        "zips": "92118",
        "neighborhoods": ["Coronado Village", "Coronado Cays", "Coronado Shores", "Coronado Cove"],
        "lat": 32.6859,
        "lng": -117.1831,
        "h1": "Mobile Auto Detailing in Coronado, CA",
        "description": "Mobile auto detailing in Coronado. Luxury and exotic experience. IGL Coatings Certified. Coastal salt-air decontamination. From $89. (619) 341-0016.",
        "keywords": "coronado mobile detailing, coronado car detailer, ceramic coating coronado, luxury detailer coronado",
        "intro": "Coronado vehicles take serious abuse from the ocean air. Salt spray, sand, and sun are hard on paint and wheels — and Coronado owners tend to drive vehicles worth protecting. We bring a fully self-contained mobile rig across the bridge so your Coronado Shores condo, Coronado Cays home, or Village residence stays the service location. Every Coronado exterior detail includes extra iron decontamination to pull embedded salt deposits out of the clear coat.",
        "local_seo": [
            "Extra iron + salt decontamination standard on every Coronado exterior service.",
            "Ceramic coating strongly recommended for Coronado vehicles — UV + salt exposure is brutal otherwise.",
            "Service across Coronado Village, Coronado Cays, Coronado Shores, and the Coronado Cove area.",
            "Comfortable with Coronado Cays gated-community access and condo parking garages.",
        ],
        "popular_services": ["Ceramic Coating (5-year + 9-year)", "Exterior Detail with extra decon", "Paint Correction"],
    },
    {
        "slug": "national-city",
        "name": "National City",
        "zips": "91950",
        "neighborhoods": ["Kimball Park area", "Plaza Bonita area", "Paradise Valley", "Granger"],
        "lat": 32.6781,
        "lng": -117.0992,
        "h1": "Mobile Auto Detailing in National City, CA",
        "description": "Affordable mobile auto detailing in National City. No travel fee. Full Detail from $279, Mini from $89. Fleet accounts welcome. (619) 341-0016.",
        "keywords": "national city mobile detailing, national city car detailer, fleet detailing national city, 91950 auto detailing",
        "intro": "National City is a regular stop on our route — busy residential streets, dense apartment complexes, and several small-fleet accounts (contractors, delivery services, auto dealers). We handle one-off details and recurring monthly maintenance in National City with the same quality. Self-contained mobile rig means we service vehicles where they sit — no need to move anything to a shop.",
        "local_seo": [
            "Familiar with National City apartment complexes, condos, and street parking scenarios.",
            "Fleet-friendly — we offer volume pricing for 3+ vehicles per visit.",
            "Zip 91950 served at no travel fee.",
            "Popular in National City: Mini Detail for daily drivers; Full Detail before resale.",
        ],
        "popular_services": ["Mini Detail", "Full Detail (pre-sale clean-up)", "Monthly Maintenance Plan", "Fleet detailing (3+ vehicles)"],
    },
    {
        "slug": "imperial-beach",
        "name": "Imperial Beach",
        "zips": "91932",
        "neighborhoods": ["Seacoast Drive area", "Palm Avenue corridor", "Downtown IB"],
        "lat": 32.5839,
        "lng": -117.1133,
        "h1": "Mobile Auto Detailing in Imperial Beach, CA",
        "description": "Mobile auto detailing in Imperial Beach. Coastal-grade decontamination and salt protection. IGL Coatings Certified. From $89. (619) 341-0016.",
        "keywords": "imperial beach mobile detailing, IB car detailer, ceramic coating imperial beach, coastal car detailer",
        "intro": "Imperial Beach vehicles live on the front lines of salt, sand, and sun. Paint oxidizes faster here than almost anywhere in the county. Our mobile service brings full coastal-grade decontamination right to your driveway in IB — iron removal, tar decon, clay bar, and optional IGL ceramic coating to block the damage from ever starting. We serve Seacoast Drive, Palm Avenue, and the Downtown IB area.",
        "local_seo": [
            "Every Imperial Beach exterior service includes extended iron + salt decontamination.",
            "Ceramic coating is the single best investment for IB vehicles — 5-year IGL coating blocks 90%+ of UV/salt damage.",
            "Zip 91932 served at no travel fee.",
            "Popular: Full Exterior with coastal decon + Ceramic Coating for long-term protection.",
        ],
        "popular_services": ["Full Exterior with coastal decon", "Ceramic Coating (IGL 5-year)", "Paint Correction"],
    },
    {
        "slug": "san-diego",
        "name": "San Diego",
        "zips": "Multiple (92101, 92103, 92104, 92105, 92108, 92116, 92129, etc.)",
        "neighborhoods": ["Mission Valley", "North Park", "Downtown San Diego", "Hillcrest", "Kearny Mesa", "Clairemont", "Pacific Beach"],
        "lat": 32.7157,
        "lng": -117.1611,
        "h1": "Mobile Auto Detailing in San Diego, CA",
        "description": "Mobile auto detailing across San Diego — Mission Valley, North Park, Downtown, Hillcrest, and more. IGL Coatings Certified. Self-contained. From $89.",
        "keywords": "san diego mobile detailing, mobile car detailing san diego, mission valley detailer, north park detailing, downtown san diego detailer",
        "intro": "We extend our mobile service from Chula Vista up into San Diego proper — Mission Valley offices, North Park homes, Downtown condos, Hillcrest residences, and beyond. The 805 and 5 corridors are regular drives for us. Every San Diego appointment gets the same fully self-contained rig, the same IGL + HTL certifications, and the same satisfaction guarantee. Metered street parking, condo garages, and office lots are all workable — we coordinate with you at booking.",
        "local_seo": [
            "Regular coverage: Mission Valley, North Park, Downtown SD, Hillcrest, Kearny Mesa, Clairemont, Pacific Beach.",
            "Experienced with condo/garage parking and metered street setups — we plan around space.",
            "Office-lot bookings welcome — you work, we detail, you come out to a finished car.",
            "Same South Bay pricing applies in San Diego at no travel fee.",
        ],
        "popular_services": ["The Works — Interior + Exterior", "Ceramic Coating", "Paint Correction"],
    },
]


# ---------------- Renderers ----------------

def render_service_page(data):
    slug = data["slug"]
    canonical = f"{slug}"
    items = [("Home", ""), ("Services", slug), (data["name"], slug)]
    breadcrumbs_data = [("Home", ""), (data["name"], slug)]
    keywords = data.get("keywords", "")
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in data["faq"]
        ]
    }
    service_schema = {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": data["name"],
        "name": data["h1"],
        "description": data["description"],
        "provider": {"@type": "AutoDetailing", "name": "Reflection Detailing"},
        "areaServed": "Chula Vista, CA",
        "offers": {
            "@type": "AggregateOffer",
            "lowPrice": data["price_from"].replace("$", "").split("/")[0].strip(),
            "priceCurrency": "USD"
        }
    }

    benefits_html = "\n".join(
        f'<div class="border border-slate-200 rounded-xl p-5"><h3 class="font-bold mb-2">{t}</h3><p class="text-slate-600 text-sm">{d}</p></div>'
        for t, d in data["benefits"]
    )
    photos_html = ""
    if data.get("photos"):
        tiles = "\n".join(
            f'<figure class="relative"><img src="../{src}" alt="{alt}" class="rounded-xl w-full h-72 md:h-96 object-cover" loading="lazy" /><figcaption class="absolute bottom-3 left-3 bg-ink/90 text-white text-xs font-bold px-3 py-1 rounded">{caption}</figcaption></figure>'
            for src, alt, caption in data["photos"]
        )
        photos_html = f"""
  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">Recent {data['name'].lower()} work</h2>
    <div class="grid md:grid-cols-2 gap-5">{tiles}</div>
  </section>
"""
    process_html = "\n".join(
        f'<li class="border border-slate-200 rounded-xl p-5"><div class="w-10 h-10 bg-accent text-ink rounded-full grid place-items-center font-black mb-3">{i+1}</div><h3 class="font-bold mb-2">{t}</h3><p class="text-slate-600 text-sm">{d}</p></li>'
        for i, (t, d) in enumerate(data["process"])
    )
    pricing_rows_html = "\n".join(
        f'<tr class="border-b border-slate-100 {"bg-slate-50" if i%2 else ""}"><td class="p-4 font-bold">{a}</td><td class="p-4 text-accent font-black whitespace-nowrap">{b}</td><td class="p-4 text-slate-700 text-sm">{c}</td></tr>'
        for i, (a, b, c) in enumerate(data["pricing_rows"])
    )
    faq_html = "\n".join(
        f'<details class="bg-white rounded-xl p-4 md:p-5 border border-slate-200 group"><summary class="cursor-pointer font-bold text-base md:text-lg flex justify-between items-start gap-3">{q} <span class="text-accent group-open:rotate-45 transition text-xl leading-none shrink-0">+</span></summary><p class="text-slate-700 mt-3 text-sm md:text-base leading-relaxed">{a}</p></details>'
        for q, a in data["faq"]
    )
    also_see_html = "\n".join(
        f'<a href="../{s}/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold text-ink">{n}</p><p class="text-sm text-slate-500 mt-1">Learn more →</p></a>'
        for s, n in data["also_see"]
    )

    html = f"""{common_head(
        title=f"{data['h1']} | Reflection Detailing",
        description=data["description"],
        canonical_path=canonical,
        keywords=keywords
    )}
{local_business_schema()}
<script type="application/ld+json">
{json.dumps(service_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>
{breadcrumb_schema(breadcrumbs_data)}
</head>
<body class="bg-white text-ink antialiased font-sans">
{header_html(depth=1)}

<section class="bg-gradient-to-b from-ink to-slate-900 text-white py-16 md:py-24">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">{data['tagline']}</p>
    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-5">{data['h1']}</h1>
    <p class="text-lg text-slate-300 max-w-2xl mx-auto mb-8">{data['intro']}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="{SETMORE_URL}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-6 py-3 rounded-lg hover:opacity-90">Book Now — from {data['price_from']}</a>
      <a href="tel:{PHONE_TEL}" class="bg-white/10 border border-white/30 text-white font-bold px-6 py-3 rounded-lg hover:bg-white/20">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>

<main class="max-w-6xl mx-auto px-4 py-12">
  {breadcrumb_html(breadcrumbs_data, depth=1)}

  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">Why choose Reflection Detailing for {data['name'].lower()}?</h2>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">{benefits_html}</div>
  </section>

  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">Our {data['name']} Process</h2>
    <ol class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">{process_html}</ol>
  </section>
  {photos_html}

  <section class="mb-16" id="pricing">
    <h2 class="text-2xl md:text-3xl font-black mb-6">{data['name']} Pricing</h2>
    <div class="overflow-x-auto">
      <table class="w-full text-left border border-slate-200 rounded-xl overflow-hidden">
        <thead class="bg-ink text-white"><tr><th class="p-4">Package</th><th class="p-4">Price</th><th class="p-4">Includes</th></tr></thead>
        <tbody>{pricing_rows_html}</tbody>
      </table>
    </div>
    <p class="text-sm text-slate-500 mt-3">Base pricing shown for sedans and coupes. SUVs +$40, full-size trucks +$60-$80.</p>
  </section>

  <section class="mb-16" id="faq">
    <h2 class="text-2xl md:text-3xl font-black mb-6">{data['name']} FAQ</h2>
    <div class="space-y-3">{faq_html}</div>
  </section>

  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">Related services</h2>
    <div class="grid md:grid-cols-3 gap-4">{also_see_html}</div>
  </section>
</main>

{cta_strip()}
{footer_html(depth=1)}

</body>
</html>
"""
    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)
    print(f"✓ {slug}/index.html")


def render_city_page(data):
    slug = data["slug"]
    breadcrumbs_data = [("Home", ""), (f"Service Area — {data['name']}", slug)]

    place_schema = {
        "@context": "https://schema.org",
        "@type": "Place",
        "name": f"Reflection Detailing Service Area — {data['name']}",
        "description": data["description"],
        "geo": {"@type": "GeoCoordinates", "latitude": data["lat"], "longitude": data["lng"]},
        "containedInPlace": {"@type": "AdministrativeArea", "name": "San Diego County, CA"}
    }

    # FAQ specific to city
    city_faq = [
        (f"Do you detail cars in {data['name']}?",
         f"Yes, we're a mobile detailing service covering {data['name']} with no travel fee. Serving zip codes {data['zips']} and surrounding neighborhoods: {', '.join(data['neighborhoods'])}."),
        (f"How soon can you detail my car in {data['name']}?",
         f"Most {data['name']} appointments are confirmed within 24-48 hours. Same-day availability is often possible. Text (619) 341-0016 for fastest response."),
        (f"Do you service gated communities in {data['name']}?",
         f"Yes. We regularly work in gated communities across {data['name']} — just coordinate guest access at time of booking."),
    ]
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in city_faq
        ]
    }

    popular_html = "\n".join(f'<li class="border border-slate-200 rounded-xl p-4 text-center font-bold">{s}</li>' for s in data["popular_services"])
    neighborhood_html = ", ".join(data["neighborhoods"])
    local_seo_html = "\n".join(f'<li class="mb-2">✓ {pt}</li>' for pt in data["local_seo"])
    city_faq_html = "\n".join(
        f'<details class="bg-white rounded-xl p-4 md:p-5 border border-slate-200 group"><summary class="cursor-pointer font-bold text-base md:text-lg flex justify-between items-start gap-3">{q} <span class="text-accent group-open:rotate-45 transition text-xl leading-none shrink-0">+</span></summary><p class="text-slate-700 mt-3 text-sm md:text-base leading-relaxed">{a}</p></details>'
        for q, a in city_faq
    )

    html = f"""{common_head(
        title=f"{data['h1']} | Reflection Detailing",
        description=data["description"],
        canonical_path=slug,
        keywords=data["keywords"]
    )}
{local_business_schema()}
<script type="application/ld+json">
{json.dumps(place_schema, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps(faq_schema, indent=2)}
</script>
{breadcrumb_schema(breadcrumbs_data)}
</head>
<body class="bg-white text-ink antialiased font-sans">
{header_html(depth=1)}

<section class="bg-gradient-to-b from-ink to-slate-900 text-white py-16 md:py-24">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Service Area — No Travel Fee</p>
    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-5">{data['h1']}</h1>
    <p class="text-lg text-slate-300 max-w-2xl mx-auto mb-8">{data['intro']}</p>
    <div class="flex flex-col sm:flex-row gap-3 justify-center">
      <a href="{SETMORE_URL}" target="_blank" rel="noopener" class="bg-accent text-ink font-bold px-6 py-3 rounded-lg hover:opacity-90">Book a Detail</a>
      <a href="tel:{PHONE_TEL}" class="bg-white/10 border border-white/30 text-white font-bold px-6 py-3 rounded-lg hover:bg-white/20">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</section>

<main class="max-w-6xl mx-auto px-4 py-12">
  {breadcrumb_html(breadcrumbs_data, depth=1)}

  <section class="mb-16 grid md:grid-cols-2 gap-10">
    <div>
      <h2 class="text-2xl md:text-3xl font-black mb-5">Serving {data['name']} completely</h2>
      <ul class="text-slate-700 text-sm md:text-base">{local_seo_html}</ul>
      <p class="mt-5 text-slate-600 text-sm"><strong>Zip codes served:</strong> {data['zips']}</p>
      <p class="mt-2 text-slate-600 text-sm"><strong>Neighborhoods:</strong> {neighborhood_html}</p>
    </div>
    <div>
      <h3 class="font-black text-xl mb-4">Popular in {data['name']}</h3>
      <ul class="space-y-3">{popular_html}</ul>
    </div>
  </section>

  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">Services available in {data['name']}</h2>
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
      <a href="../mobile-detailing/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">Mobile Detailing</p><p class="text-sm text-slate-600 mt-1">From $89</p></a>
      <a href="../ceramic-coating/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">Ceramic Coating</p><p class="text-sm text-slate-600 mt-1">IGL Certified · from $449</p></a>
      <a href="../paint-correction/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">Paint Correction</p><p class="text-sm text-slate-600 mt-1">HTL Certified · from $499</p></a>
      <a href="../interior-detail/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">Interior Detail</p><p class="text-sm text-slate-600 mt-1">From $179</p></a>
      <a href="../headlight-restoration/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">Headlight Restoration</p><p class="text-sm text-slate-600 mt-1">$99 / pair</p></a>
      <a href="../pricing/" class="block border border-slate-200 rounded-xl p-5 hover:border-accent"><p class="font-bold">See All Pricing</p><p class="text-sm text-slate-600 mt-1">Transparent rates →</p></a>
    </div>
  </section>

  <section class="mb-16">
    <h2 class="text-2xl md:text-3xl font-black mb-6">FAQ for {data['name']} customers</h2>
    <div class="space-y-3">{city_faq_html}</div>
  </section>
</main>

{cta_strip()}
{footer_html(depth=1)}

</body>
</html>
"""
    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)
    print(f"✓ {slug}/index.html")


def render_pricing_page():
    slug = "pricing"
    breadcrumbs_data = [("Home", ""), ("Pricing", slug)]
    rows = [
        ("Mini Detail", "$89", "Hand wash, vacuum, windows, tire dressing. ~60 min."),
        ("Full Interior Detail", "$179", "Deep vacuum, shampoo, leather, UV protect. 2-3 hrs."),
        ("Full Exterior Detail", "$169", "Hand wash, clay bar, wheels, sealant. 2-3 hrs."),
        ("The Works — In + Out", "$279", "Complete interior + exterior. 4-5 hrs. Most popular."),
        ("Paint Correction — 1-step", "$499+", "Removes light-to-moderate swirls. HTL Certified."),
        ("Paint Correction — 2-step", "$749+", "Compound + polish. 80-95% defect removal."),
        ("Paint Correction — 3-step", "$999+", "Show-car level. Compound + polish + finishing."),
        ("Ceramic Coating — 2-year", "$449+", "IGL Certified. Graphene ceramic. Hydrophobic."),
        ("Ceramic Coating — 5-year", "$849+", "IGL Certified. Premium graphene + correction."),
        ("Ceramic Coating — 9-year", "$1,499+", "IGL flagship coating with warranty documentation."),
        ("Headlight Restoration", "$99 / pair", "Sand + polish + UV seal. 45 min."),
        ("Pet Hair Removal", "+$40", "Specialized extraction. Adds to any interior package."),
        ("Odor Treatment", "+$49", "Enzymatic deep odor neutralization."),
        ("Monthly Maintenance Plan", "$149/mo+", "Recurring. Save ~$30/mo vs one-off pricing."),
        ("Custom / Fleet / RV Quote", "Text", "Text (619) 341-0016 with photos for tailored quote."),
    ]
    rows_html = "\n".join(
        f'<tr class="border-b border-slate-100 {"bg-slate-50" if i%2 else ""}"><td class="p-4 font-bold">{a}</td><td class="p-4 text-accent font-black whitespace-nowrap">{b}</td><td class="p-4 text-slate-700 text-sm">{c}</td></tr>'
        for i, (a, b, c) in enumerate(rows)
    )
    html = f"""{common_head(
        title="Detailing Pricing in Chula Vista | Reflection Detailing",
        description="Transparent mobile detailing pricing in Chula Vista. Mini Detail $89, Full Detail $279, Ceramic Coating from $449, Paint Correction from $499. No travel fee.",
        canonical_path=slug,
        keywords="detailing prices chula vista, mobile detailing cost san diego, how much does detailing cost"
    )}
{local_business_schema()}
{breadcrumb_schema(breadcrumbs_data)}
</head>
<body class="bg-white text-ink antialiased font-sans">
{header_html(depth=1)}

<section class="bg-gradient-to-b from-ink to-slate-900 text-white py-16">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Full Price List</p>
    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-5">Mobile Detailing Pricing — Chula Vista & South Bay</h1>
    <p class="text-lg text-slate-300 max-w-2xl mx-auto">Transparent pricing. No travel fee anywhere in the South Bay. Sedan/coupe base — SUVs +$40, full-size trucks +$60-$80.</p>
  </div>
</section>

<main class="max-w-5xl mx-auto px-4 py-12">
  {breadcrumb_html(breadcrumbs_data, depth=1)}
  <div class="overflow-x-auto">
    <table class="w-full text-left border border-slate-200 rounded-xl overflow-hidden">
      <thead class="bg-ink text-white"><tr><th class="p-4">Service</th><th class="p-4">Starting Price</th><th class="p-4">Includes</th></tr></thead>
      <tbody>{rows_html}</tbody>
    </table>
  </div>
</main>

{cta_strip()}
{footer_html(depth=1)}
</body>
</html>
"""
    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(html)
    print(f"✓ {slug}/index.html")


def render_learn_hub():
    slug = "learn"
    articles = [
        ("wax-vs-ceramic-coating", "Wax vs Ceramic Coating: Which Is Right for Your Car?",
         "The definitive guide to paint protection options. Real costs, real timelines, real tradeoffs — no sales pitch.",
         [
             ("The short answer", "If you're keeping the car more than 2 years, ceramic wins on cost-per-year and protection. If you're selling in under 2 years, a good synthetic sealant does the job for a fraction of the cost."),
             ("Wax — 1 to 3 months", "Carnauba-based products. Warm, deep shine. Needs reapplication every 1-3 months depending on climate and washing. Best for enthusiasts who love the weekend ritual."),
             ("Sealant — 3 to 6 months", "Synthetic polymer-based. Longer-lasting than wax, easier to apply. Good middle option for budget-conscious owners."),
             ("Ceramic Coating — 2 to 9 years", "Silica (SiO2) or graphene-based. Forms a semi-permanent bond with clear coat. Requires professional application for warranty coverage. Outperforms wax and sealant on durability, UV resistance, and chemical resistance."),
             ("Real cost math", "Wax: $100/yr in product + 20 hours of your time. 5-year ceramic at $849: about $170/yr, zero wax purchases, 2-3 hours per wash saved. Ceramic wins on any time-value analysis."),
         ]),
        ("how-much-does-detailing-cost-san-diego", "How Much Does a Car Detail Cost in San Diego?",
         "Market pricing breakdown for 2026 — shop vs mobile, services tier by tier, what to watch out for.",
         [
             ("Current San Diego market (2026)", "Mini details: $89-$149. Full details: $229-$389. Paint correction: $399-$750. Ceramic coating: $299 (2-year) to $1,500 (9-year). Mobile detailers typically price the same as shops — travel fees have become rare."),
             ("What affects the price?", "Vehicle size (SUV/truck/RV upcharges), vehicle condition (pet hair, severe stains, heavy oxidation), package tier, whether paint correction is needed before coating, and installer certification level."),
             ("Red flags in pricing", "A $200 ceramic coating is not a real ceramic coating — it's probably a spray sealant mislabeled. A $99 full detail likely skips decontamination, clay bar, or shampoo. If the price seems too low, ask what's included."),
             ("Reflection Detailing's positioning", "We price mid-market. Mini Detail $89 (market: $99-$149). Full Detail $279 (market: $229-$389). We undercut the premium players while matching their certification — IGL Coatings and HTL Detailing certified."),
         ]),
        ("5-signs-your-car-needs-detailing", "5 Signs Your Car Needs Professional Detailing",
         "If you see any of these, it's time. No guilt — just a quick checklist.",
         [
             ("1. Swirl marks visible in sunlight", "Those circular scratches in your paint are from improper washing (usually automatic car washes). They won't buff out with wax — they need paint correction."),
             ("2. Water doesn't bead on the paint", "If water sheets across your paint instead of beading into droplets, your protection has worn off. Time for a refresh — wax, sealant, or ideally a ceramic coating."),
             ("3. The interior smells like something other than 'clean'", "Odor is bacteria. No amount of air freshener will fix it. Hot-water extraction and enzymatic treatment is the only real solution."),
             ("4. Cloudy or yellow headlights", "Oxidation on the outer plastic cuts light output by up to 80%. That's a safety issue. Headlight restoration takes 45 minutes and costs $99 per pair."),
             ("5. The last time you detailed was over a year ago", "Cars collect bonded contaminants over time — brake dust, rail dust, tree sap, bug splatter — that regular washing won't remove. An annual full detail with decontamination keeps paint healthy for the long haul."),
         ]),
        ("ceramic-coating-maintenance-guide", "How to Maintain a Ceramic Coating: 2026 Guide",
         "Your IGL-certified installer's guide to making a ceramic coating last its full rated lifespan.",
         [
             ("The first 7 days are the most important", "A ceramic coating needs 5-7 days to fully cure after application. During that window: no car washes, no rain if you can help it, no parking under trees. After 7 days, the coating is bonded and durable — you can wash normally."),
             ("Use the 2-bucket wash method (or a touchless wash)", "The #1 thing that damages coated paint isn't UV or salt — it's improper washing. Automatic car washes with rotating brushes introduce micro-scratches that dull the coating's slickness. Either hand-wash with two buckets (one soapy, one rinse), a clean microfiber mitt, and a grit guard — or use a touchless automatic wash only."),
             ("Use a pH-neutral shampoo", "Dish soap, household cleaners, and aggressive car wash shampoos can strip a ceramic coating over time. Use a pH-neutral car shampoo labeled 'coating-safe.' Meguiar's Gold Class, Chemical Guys Mr. Pink, and Gyeon Bathe are all fine choices."),
             ("Dry with a clean microfiber or blower", "Water spots are the enemy of coated paint. Don't let coated paint air-dry — either blow-dry with a leaf blower (seriously, this works great) or dry with a clean, fluffy microfiber towel using the 'drag technique.'"),
             ("Apply a spray sealant boost every 3-6 months", "A maintenance spray like IGL Quartz+, Gyeon WetCoat, or CarPro Reload adds sacrificial protection on top of the ceramic coating. This doesn't replace the coating — it extends the effective lifespan by protecting it from environmental damage."),
             ("Schedule an annual maintenance inspection", "Come back to your installer once a year for a coating inspection. We check for high spots, reduced slickness, or damage, and decant a maintenance spray. For IGL-certified coatings with registered warranties, this annual check keeps the warranty valid."),
         ]),
        ("ppf-vs-ceramic-coating", "PPF vs Ceramic Coating: Which Does Your Car Actually Need?",
         "Both protect paint. Both cost money. They do different things. Here's the honest breakdown.",
         [
             ("Short version", "PPF (paint protection film) is a thick self-healing urethane film that physically blocks rock chips. Ceramic coating is a liquid chemistry that blocks UV, chemical, and staining damage. You can run both — PPF on the front impact zones and ceramic on everything else is the gold-standard setup."),
             ("What PPF is good for", "Rock chips, road debris, bug-etch damage, and minor scratches — PPF takes the hit instead of your paint. Modern PPF self-heals minor scratches with heat. Best for daily drivers with long commutes, lifted trucks, anything driven on dirt roads, collector cars you want to sell in 10 years with zero chips."),
             ("What ceramic coating is good for", "UV fading, chemical etching (bird droppings, tree sap, bug splatter), water spots, staining, and everyday swirl resistance. Ceramic keeps paint looking 'wet' and makes washing dramatically easier. Best for preserving a fresh paint job, maintaining resale value, and saving time on maintenance."),
             ("What they won't do", "Ceramic coating is NOT scratch-proof. It resists minor swirls but a shopping cart will still scratch your paint through the coating. PPF is NOT bulletproof either — hard enough impacts can still damage paint underneath. Both are protection, not armor."),
             ("Cost comparison", "PPF full-front (hood, fenders, bumper, mirrors, headlights): $1,500-$2,500. PPF full-car: $4,500-$9,000. Ceramic Coating: $449-$1,499 depending on tier. Ceramic is massively cheaper but covers different risks."),
             ("Our recommendation", "For most South Bay daily drivers: start with a 5-year IGL ceramic coating. Add PPF to the front impact zones (hood, front bumper, fenders) if you park outside often or commute on freeways with road debris. That combination gives 80%+ of full-car PPF protection at roughly 30% of the cost."),
         ]),
        ("how-often-should-you-detail-car-san-diego", "How Often Should You Detail Your Car in San Diego?",
         "Frequency recommendations by service type, driving habits, and where you park.",
         [
             ("Mini Detail — every 4-6 weeks", "A Mini Detail (hand wash, vacuum, windows, tire dressing) is a maintenance touch, not a deep clean. For daily drivers, bi-monthly keeps the car looking sharp without much effort. Go monthly if you park outside or drive frequently."),
             ("Full Interior Detail — every 3-6 months", "Interior grime builds slowly but steadily — seat stains, dashboard dust, carpet tracks. A Full Interior Detail every 3-6 months resets the clock. More frequent if you have kids, pets, or commute long distances."),
             ("Full Exterior Detail — every 3-4 months", "Exterior paint accumulates bonded contaminants (rail dust, iron, tar, bug splatter) that regular washing won't remove. Every 3-4 months is the sweet spot for a full exterior with decontamination."),
             ("Paint Correction — once, then every 2-5 years", "Paint correction is a one-and-done reset. Once done, proper maintenance should extend the results for years. Most owners do a fresh correction every 2-5 years as swirls accumulate."),
             ("Ceramic Coating — every 2-9 years (depending on tier)", "Match the ceramic tier to your ownership timeline. Keeping the car 2-3 years? A 2-year IGL coating at $449 is perfect. 5+ years? Go 5-year IGL at $849. Long-haul? 9-year IGL at $1,499."),
             ("Headlight Restoration — every 1-3 years", "If you live and park in the San Diego sun, plastic headlights oxidize faster than you'd think. Every 1-3 years with a UV sealer keeps them clear. Garaged cars go longer."),
             ("Adjust for how you park", "Garaged daily: everything gets the longer end of the range. Parked outside, frequent freeway driving, or coastal (IB/Coronado): everything gets the shorter end. Salt air and UV age paint 2-3x faster than sheltered storage."),
         ]),
    ]

    # Hub page
    breadcrumbs_hub = [("Home", ""), ("Detailing Guides", slug)]
    hub_links_html = "\n".join(
        f'<a href="{a_slug}/" class="block border border-slate-200 rounded-xl p-6 hover:border-accent"><h3 class="font-bold text-lg mb-2">{title}</h3><p class="text-slate-600 text-sm">{subtitle}</p></a>'
        for a_slug, title, subtitle, _ in articles
    )
    hub_html = f"""{common_head(
        title="Detailing Guides & Resources | Reflection Detailing",
        description="Free guides on ceramic coating, paint correction, detailing pricing, and more. Straight talk from an IGL + HTL certified detailer in Chula Vista.",
        canonical_path=slug,
        keywords="car detailing guides, ceramic coating guide, paint correction guide, detailing blog"
    )}
{local_business_schema()}
{breadcrumb_schema(breadcrumbs_hub)}
</head>
<body class="bg-white text-ink antialiased font-sans">
{header_html(depth=1)}

<section class="bg-gradient-to-b from-ink to-slate-900 text-white py-16">
  <div class="max-w-4xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Learn</p>
    <h1 class="text-3xl md:text-5xl font-black leading-tight mb-5">Detailing Guides & Resources</h1>
    <p class="text-lg text-slate-300 max-w-2xl mx-auto">Straight talk from a certified detailer — no sales pitch, no fluff. Real answers to real questions.</p>
  </div>
</section>

<main class="max-w-5xl mx-auto px-4 py-12">
  {breadcrumb_html(breadcrumbs_hub, depth=1)}
  <div class="grid md:grid-cols-2 gap-5">{hub_links_html}</div>
</main>

{cta_strip()}
{footer_html(depth=1)}
</body>
</html>
"""
    out_dir = os.path.join(ROOT, slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w") as f:
        f.write(hub_html)
    print(f"✓ {slug}/index.html")

    # Each article
    for a_slug, title, subtitle, sections in articles:
        breadcrumbs_art = [("Home", ""), ("Guides", slug), (title, f"{slug}/{a_slug}")]
        sections_html = "\n".join(
            f'<section class="mb-10"><h2 class="text-2xl font-black mb-3">{t}</h2><p class="text-slate-700 leading-relaxed">{body}</p></section>'
            for t, body in sections
        )
        art_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": subtitle,
            "author": {"@type": "Organization", "name": "Reflection Detailing"},
            "publisher": {"@type": "Organization", "name": "Reflection Detailing"},
            "datePublished": "2026-04-24",
            "dateModified": "2026-04-24"
        }
        art_html = f"""{common_head(
            title=f"{title} | Reflection Detailing",
            description=subtitle,
            canonical_path=f"{slug}/{a_slug}",
            keywords=""
        )}
{local_business_schema()}
<script type="application/ld+json">
{json.dumps(art_schema, indent=2)}
</script>
{breadcrumb_schema(breadcrumbs_art)}
</head>
<body class="bg-white text-ink antialiased font-sans">
{header_html(depth=2)}

<section class="bg-gradient-to-b from-ink to-slate-900 text-white py-16">
  <div class="max-w-3xl mx-auto px-4 text-center">
    <p class="uppercase tracking-widest text-accent font-bold text-sm mb-3">Detailing Guide</p>
    <h1 class="text-3xl md:text-4xl font-black leading-tight mb-4">{title}</h1>
    <p class="text-lg text-slate-300">{subtitle}</p>
  </div>
</section>

<main class="max-w-3xl mx-auto px-4 py-12">
  {breadcrumb_html(breadcrumbs_art, depth=2)}
  {sections_html}

  <div class="border-t border-slate-200 pt-8 mt-10 text-center">
    <p class="text-slate-600 mb-4">Questions? Angel personally answers every text.</p>
    <a href="sms:{PHONE_TEL}" class="inline-block bg-ink text-white font-bold px-6 py-3 rounded-lg hover:bg-slate-800">Text {PHONE_DISPLAY}</a>
  </div>
</main>

{cta_strip()}
{footer_html(depth=2)}
</body>
</html>
"""
        out_dir = os.path.join(ROOT, slug, a_slug)
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w") as f:
            f.write(art_html)
        print(f"✓ {slug}/{a_slug}/index.html")


def render_sitemap():
    urls = [
        ("", 1.0),
        ("ceramic-coating/", 0.9),
        ("paint-correction/", 0.9),
        ("mobile-detailing/", 0.9),
        ("headlight-restoration/", 0.8),
        ("interior-detail/", 0.8),
        ("chula-vista/", 0.9),
        ("eastlake/", 0.8),
        ("bonita/", 0.8),
        ("otay-ranch/", 0.8),
        ("coronado/", 0.8),
        ("national-city/", 0.7),
        ("imperial-beach/", 0.7),
        ("san-diego/", 0.8),
        ("pricing/", 0.8),
        ("learn/", 0.7),
        ("learn/wax-vs-ceramic-coating/", 0.6),
        ("learn/how-much-does-detailing-cost-san-diego/", 0.6),
        ("learn/5-signs-your-car-needs-detailing/", 0.6),
        ("learn/ceramic-coating-maintenance-guide/", 0.6),
        ("learn/ppf-vs-ceramic-coating/", 0.6),
        ("learn/how-often-should-you-detail-car-san-diego/", 0.6),
    ]
    entries = "\n".join(
        f'  <url><loc>{BASE_URL}/{p}</loc><lastmod>2026-04-24</lastmod><priority>{pr}</priority></url>'
        for p, pr in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
        f.write(xml)
    print("✓ sitemap.xml")


def render_robots():
    txt = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(ROOT, "robots.txt"), "w") as f:
        f.write(txt)
    print("✓ robots.txt")


def render_llms_txt():
    txt = f"""# Reflection Detailing

> Mobile auto detailing in Chula Vista and South San Diego. Owner-operated by Angel. IGL Coatings Certified and HTL Detailing Certified. Self-contained rig — brings own water and power.

## Business details
- Name: Reflection Detailing LLC
- Phone: (619) 341-0016
- Location: Chula Vista, CA 91913
- Website: {BASE_URL}/
- Booking: {SETMORE_URL}
- Rating: 5.0 stars on Google
- Hours: Mon 9-5, Tue-Sat 7-6, Sun 7-2

## Service area (no travel fee)
Chula Vista, Bonita, Eastlake, Otay Ranch, National City, Imperial Beach, Coronado, San Diego, Spring Valley, La Mesa, Lemon Grove.

## Services & pricing (sedan/coupe base)
- Mini Detail: $89
- Full Interior Detail: $179
- Full Exterior Detail: $169
- The Works (Interior + Exterior): $279
- Paint Correction (1-step): $499+ | 2-step: $749+ | 3-step: $999+
- Ceramic Coating: 2-year $449+ | 5-year $849+ | 9-year $1,499+
- Headlight Restoration: $99 / pair
- Pet Hair Removal: +$40
- Monthly Maintenance: from $149/mo

SUVs add $40. Full-size trucks and vans add $60-$80. 3-row vehicles add $80-$100.

## Certifications
- IGL Coatings Certified Installer (ceramic coating — paint, windows, wheels, trim, leather)
- HTL Detailing Certified (paint correction)

## Key pages
- [Ceramic Coating]({BASE_URL}/ceramic-coating/): IGL-certified ceramic coating installation
- [Paint Correction]({BASE_URL}/paint-correction/): HTL-certified 1-step, 2-step, 3-step machine polishing
- [Mobile Detailing]({BASE_URL}/mobile-detailing/): Self-contained mobile detailing service
- [Headlight Restoration]({BASE_URL}/headlight-restoration/): Cloudy headlight repair
- [Interior Detail]({BASE_URL}/interior-detail/): Full interior cleaning and protection
- [Pricing]({BASE_URL}/pricing/): Complete price list
- [Learn]({BASE_URL}/learn/): Detailing guides
- [Chula Vista]({BASE_URL}/chula-vista/): Primary service area
- [Eastlake]({BASE_URL}/eastlake/): Eastlake coverage
- [Bonita]({BASE_URL}/bonita/): Bonita coverage
- [Otay Ranch]({BASE_URL}/otay-ranch/): Otay Ranch coverage
- [Coronado]({BASE_URL}/coronado/): Coronado coverage — luxury/beach area
- [National City]({BASE_URL}/national-city/): National City + fleet accounts
- [Imperial Beach]({BASE_URL}/imperial-beach/): Imperial Beach — coastal decon
- [San Diego]({BASE_URL}/san-diego/): Mission Valley, North Park, Downtown, Hillcrest

## Detailing guides
- [Wax vs Ceramic Coating]({BASE_URL}/learn/wax-vs-ceramic-coating/)
- [Detailing prices in San Diego]({BASE_URL}/learn/how-much-does-detailing-cost-san-diego/)
- [5 signs your car needs detailing]({BASE_URL}/learn/5-signs-your-car-needs-detailing/)
- [Ceramic coating maintenance guide]({BASE_URL}/learn/ceramic-coating-maintenance-guide/)
- [PPF vs Ceramic Coating]({BASE_URL}/learn/ppf-vs-ceramic-coating/)
- [How often to detail in San Diego]({BASE_URL}/learn/how-often-should-you-detail-car-san-diego/)

## Frequently asked
- How much does mobile detailing cost in Chula Vista? Mini Detail starts at $89, Full Detail $279, Ceramic Coating from $449.
- Do you come to my location? Yes — 100% mobile, self-contained, no travel fee in South Bay.
- Are you certified? Yes — IGL Coatings Certified Installer and HTL Detailing Certified.
- How long does it take? Mini Detail 60 min, Full Detail 4-5 hrs, Ceramic Coating 6-8 hrs.
- What payment methods? Credit/debit, Apple Pay, Google Pay, Zelle, Venmo, Cash App, cash.

Last updated: 2026-04-24
"""
    with open(os.path.join(ROOT, "llms.txt"), "w") as f:
        f.write(txt)
    print("✓ llms.txt")


# ---------------- Main ----------------

def main():
    for s in SERVICE_PAGES:
        render_service_page(s)
    for c in CITY_PAGES:
        render_city_page(c)
    render_pricing_page()
    render_learn_hub()
    render_sitemap()
    render_robots()
    render_llms_txt()
    print("\nAll pages generated.")


if __name__ == "__main__":
    main()
