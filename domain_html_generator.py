"""
J.A.R.V.I.S. Domain-Specific HTML Architecture Synthesizer
Generates bespoke, production-ready, domain-native HTML5/Tailwind/JS web applications.
Guarantees distinct typography, palettes, UX patterns, content copy, and selective 3D usage.
"""

from typing import Dict, Any


def generate_photography_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    pal = design_profile["palette"]
    typo = design_profile["typography"]
    three_d = design_profile["three_d_strategy"]
    display_title = site_name.replace("_", " ").title()

    three_js_scripts = """<!-- Three.js 3D WebGL Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>""" if three_d["enabled"] else ""

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} · Fine Art & Editorial Photography</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typo['google_fonts_url']}" rel="stylesheet">
    {three_js_scripts}
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        serif: ['"{typo['display']}"', 'serif'],
                        sans: ['"{typo['body']}"', 'sans-serif']
                    }},
                    colors: {{
                        studioBg: '{pal['bg']}',
                        studioSurface: '{pal['surface']}',
                        studioAccent: '{pal['accent']}',
                        studioText: '{pal['text_primary']}',
                        studioMuted: '{pal['text_secondary']}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: {pal['bg']}; color: {pal['text_primary']}; }}
        .editorial-border {{ border-color: {pal['surface_border']}; }}
        .gallery-img {{ transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), filter 0.4s ease; }}
        .gallery-card:hover .gallery-img {{ transform: scale(1.04); }}
        .lightbox-modal {{ backdrop-filter: blur(24px); }}
    </style>
</head>
<body class="font-sans antialiased selection:bg-[{pal['accent']}] selection:text-black">

    <!-- Minimal Header Navigation -->
    <header class="fixed top-0 inset-x-0 z-40 bg-[{pal['bg']}]/80 backdrop-blur-md border-b editorial-border">
        <div class="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
            <a href="#" class="font-serif text-2xl tracking-wide text-white hover:text-[{pal['accent']}] transition-colors">
                {display_title}
            </a>
            <nav class="hidden md:flex items-center gap-8 text-xs uppercase tracking-widest text-[{pal['text_secondary']}]">
                <a href="#portfolio" class="hover:text-white transition-colors">Portfolio</a>
                <a href="#story" class="hover:text-white transition-colors">Philosophy</a>
                <a href="#services" class="hover:text-white transition-colors">Commissions</a>
                <a href="#contact" class="hover:text-white transition-colors">Inquire</a>
            </nav>
            <a href="#contact" class="px-5 py-2.5 rounded-full border border-[{pal['accent']}] text-[{pal['accent']}] hover:bg-[{pal['accent']}] hover:text-black transition-all text-xs uppercase tracking-wider font-semibold">
                Book Consultation
            </a>
        </div>
    </header>

    <!-- Cinematic Hero Section -->
    <section class="relative min-h-[90vh] flex items-center justify-center pt-24 pb-16 px-6 overflow-hidden">
        <div class="max-w-5xl mx-auto text-center relative z-10">
            <span class="inline-block text-[{pal['accent']}] text-xs uppercase tracking-[0.3em] font-semibold mb-6">
                Fine Art & Editorial Monograph
            </span>
            <h1 class="font-serif text-5xl sm:text-7xl lg:text-8xl text-white font-normal tracking-tight leading-[1.08] mb-8">
                Capturing unscripted light & timeless intimacy.
            </h1>
            <p class="text-[{pal['text_secondary']}] text-base sm:text-lg max-w-2xl mx-auto font-light leading-relaxed mb-10">
                Documenting bespoke weddings, editorial portraits, and authentic human narratives with medium-format depth and poetic natural light.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="#portfolio" class="w-full sm:w-auto px-8 py-4 rounded-full bg-[{pal['accent']}] text-black font-semibold text-xs uppercase tracking-widest hover:bg-white transition-all shadow-lg shadow-[{pal['accent']}]/20">
                    Explore Curated Works
                </a>
                <a href="#story" class="w-full sm:w-auto px-8 py-4 rounded-full border editorial-border text-[{pal['text_primary']}] text-xs uppercase tracking-widest hover:bg-[{pal['surface']}] transition-all">
                    The Creative Approach
                </a>
            </div>
        </div>
    </section>

    <!-- Curated Editorial Portfolio Grid -->
    <section id="portfolio" class="max-w-7xl mx-auto px-6 py-24 border-t editorial-border">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
            <div>
                <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Curated Gallery</span>
                <h2 class="font-serif text-3xl sm:text-5xl text-white mt-2">Selected Works & Stories</h2>
            </div>
            <!-- Category Filter Tabs -->
            <div class="flex flex-wrap gap-2 text-xs uppercase tracking-wider">
                <button onclick="filterGallery('all')" class="gallery-filter-btn px-4 py-2 rounded-full bg-[{pal['accent']}] text-black font-semibold">All Works</button>
                <button onclick="filterGallery('weddings')" class="gallery-filter-btn px-4 py-2 rounded-full border editorial-border text-[{pal['text_secondary']}] hover:text-white">Weddings</button>
                <button onclick="filterGallery('editorial')" class="gallery-filter-btn px-4 py-2 rounded-full border editorial-border text-[{pal['text_secondary']}] hover:text-white">Editorial</button>
                <button onclick="filterGallery('portraits')" class="gallery-filter-btn px-4 py-2 rounded-full border editorial-border text-[{pal['text_secondary']}] hover:text-white">Portraits</button>
            </div>
        </div>

        <!-- Asymmetric Editorial Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="gallery-grid">
            <div class="gallery-card group cursor-pointer relative overflow-hidden rounded-2xl bg-[{pal['surface']}]" data-cat="weddings" onclick="openLightbox('The Amalfi Vows', 'Weddings', 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=1200&q=80')">
                <div class="aspect-[4/5] overflow-hidden">
                    <img src="https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80" alt="Amalfi Vows" class="gallery-img w-full h-full object-cover">
                </div>
                <div class="p-6">
                    <span class="text-[{pal['accent']}] text-[11px] uppercase tracking-widest">Ravello, Italy · Weddings</span>
                    <h3 class="font-serif text-xl text-white mt-1 group-hover:text-[{pal['accent']}] transition-colors">The Amalfi Vows</h3>
                </div>
            </div>

            <div class="gallery-card group cursor-pointer relative overflow-hidden rounded-2xl bg-[{pal['surface']}]" data-cat="editorial" onclick="openLightbox('Silhouettes in Paris', 'Editorial', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=1200&q=80')">
                <div class="aspect-[4/5] overflow-hidden">
                    <img src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=800&q=80" alt="Editorial Fashion" class="gallery-img w-full h-full object-cover">
                </div>
                <div class="p-6">
                    <span class="text-[{pal['accent']}] text-[11px] uppercase tracking-widest">Paris Fashion Week · Editorial</span>
                    <h3 class="font-serif text-xl text-white mt-1 group-hover:text-[{pal['accent']}] transition-colors">Silhouettes in Paris</h3>
                </div>
            </div>

            <div class="gallery-card group cursor-pointer relative overflow-hidden rounded-2xl bg-[{pal['surface']}]" data-cat="portraits" onclick="openLightbox('Quiet Solitude', 'Portraits', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=1200&q=80')">
                <div class="aspect-[4/5] overflow-hidden">
                    <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80" alt="Character Portrait" class="gallery-img w-full h-full object-cover">
                </div>
                <div class="p-6">
                    <span class="text-[{pal['accent']}] text-[11px] uppercase tracking-widest">Studio Monograph · Portraits</span>
                    <h3 class="font-serif text-xl text-white mt-1 group-hover:text-[{pal['accent']}] transition-colors">Quiet Solitude</h3>
                </div>
            </div>
        </div>
    </section>

    <!-- Lightbox Modal -->
    <div id="lightbox" class="lightbox-modal fixed inset-0 z-50 bg-black/90 hidden flex items-center justify-center p-6" onclick="closeLightbox()">
        <div class="max-w-4xl max-h-[90vh] flex flex-col items-center" onclick="event.stopPropagation()">
            <img id="lightbox-img" src="" alt="Enlarged Photo" class="max-h-[75vh] w-auto rounded-lg shadow-2xl object-contain mb-4">
            <div class="text-center">
                <h4 id="lightbox-title" class="font-serif text-2xl text-white"></h4>
                <p id="lightbox-cat" class="text-xs uppercase tracking-widest text-[{pal['accent']}] mt-1"></p>
            </div>
            <button onclick="closeLightbox()" class="absolute top-6 right-6 text-white text-3xl hover:text-[{pal['accent']}] transition-colors">&times;</button>
        </div>
    </div>

    <!-- Artist Philosophy & Story Section -->
    <section id="story" class="py-24 border-t editorial-border bg-[{pal['surface']}]/40">
        <div class="max-w-6xl mx-auto px-6 grid md:grid-cols-2 gap-16 items-center">
            <div class="aspect-[3/4] rounded-2xl overflow-hidden shadow-2xl">
                <img src="https://images.unsplash.com/photo-1554048612-b6a482bc67e5?auto=format&fit=crop&w=800&q=80" alt="Photographer in Studio" class="w-full h-full object-cover">
            </div>
            <div>
                <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Artist Statement</span>
                <h2 class="font-serif text-4xl sm:text-5xl text-white mt-3 mb-6">
                    "We do not stage your love. We observe its quiet gravity."
                </h2>
                <div class="space-y-4 text-[{pal['text_secondary']}] font-light leading-relaxed text-sm sm:text-base">
                    <p>
                        With over a decade documenting private commissions and heritage ceremonies across Europe and Asia, our studio approaches every project as an heirloom art monograph.
                    </p>
                    <p>
                        Rather than rigid posing and harsh artificial strobes, we work with available natural light, medium-format cameras, and documentary discretion. The result is imagery that feels as genuine fifty years from now as it did the second it occurred.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Curated Investment Packages -->
    <section id="services" class="max-w-7xl mx-auto px-6 py-24 border-t editorial-border">
        <div class="text-center max-w-2xl mx-auto mb-16">
            <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Commission Packages</span>
            <h2 class="font-serif text-3xl sm:text-5xl text-white mt-2">Investments & Coverage</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            <div class="p-8 rounded-3xl bg-[{pal['surface']}] border editorial-border flex flex-col justify-between">
                <div>
                    <h3 class="font-serif text-2xl text-white mb-2">Editorial Portraiture</h3>
                    <p class="text-xs text-[{pal['text_secondary']}] mb-6">Studio and on-location conceptual sessions.</p>
                    <div class="font-serif text-3xl text-[{pal['accent']}] mb-6">From $1,200</div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 2 Hours on Location or Studio</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 30 Hand-Retouched Master Prints</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Private Online Proofing Gallery</li>
                    </ul>
                </div>
                <a href="#contact" class="block text-center py-3 rounded-full border border-[{pal['accent']}] text-[{pal['accent']}] text-xs uppercase tracking-wider font-semibold hover:bg-[{pal['accent']}] hover:text-black transition-all">Book Session</a>
            </div>

            <div class="p-8 rounded-3xl bg-[{pal['surface']}] border border-[{pal['accent']}]/60 shadow-xl shadow-[{pal['accent']}]/10 flex flex-col justify-between relative">
                <div class="absolute -top-3.5 right-8 px-3 py-1 rounded-full bg-[{pal['accent']}] text-black text-[10px] font-bold uppercase tracking-widest">Most Requested</div>
                <div>
                    <h3 class="font-serif text-2xl text-white mb-2">Heritage Wedding</h3>
                    <p class="text-xs text-[{pal['text_secondary']}] mb-6">Comprehensive full-day documentary storytelling.</p>
                    <div class="font-serif text-3xl text-[{pal['accent']}] mb-6">From $4,800</div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Full Day Coverage (Up to 10 Hours)</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Lead Artist + Associate Documentarian</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Custom Hand-Bound Linen Album</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Archival Raw & High-Res Digital Delivery</li>
                    </ul>
                </div>
                <a href="#contact" class="block text-center py-3 rounded-full bg-[{pal['accent']}] text-black text-xs uppercase tracking-wider font-semibold hover:bg-white transition-all">Reserve Wedding Date</a>
            </div>

            <div class="p-8 rounded-3xl bg-[{pal['surface']}] border editorial-border flex flex-col justify-between">
                <div>
                    <h3 class="font-serif text-2xl text-white mb-2">Destination Monograph</h3>
                    <p class="text-xs text-[{pal['text_secondary']}] mb-6">Multi-day worldwide celebration coverage.</p>
                    <div class="font-serif text-3xl text-[{pal['accent']}] mb-6">Custom Inquiries</div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Multi-Day Welcome Dinner & Reception</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Worldwide Travel Included</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Drone Aerial Photography & Super 8 Film</li>
                    </ul>
                </div>
                <a href="#contact" class="block text-center py-3 rounded-full border border-[{pal['accent']}] text-[{pal['accent']}] text-xs uppercase tracking-wider font-semibold hover:bg-[{pal['accent']}] hover:text-black transition-all">Inquire for Travel</a>
            </div>
        </div>
    </section>

    <!-- Consultation & Booking Inquiry Form -->
    <section id="contact" class="max-w-3xl mx-auto px-6 py-24 border-t editorial-border">
        <div class="text-center mb-12">
            <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Commence The Journey</span>
            <h2 class="font-serif text-4xl sm:text-5xl text-white mt-2 mb-4">Inquire For Dates</h2>
            <p class="text-[{pal['text_secondary']}] text-sm font-light">We accept a strictly limited number of commissions each season to ensure undivided focus on every narrative.</p>
        </div>
        <form onsubmit="handleInquirySubmit(event)" class="space-y-6 bg-[{pal['surface']}] p-8 sm:p-12 rounded-3xl border editorial-border">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                    <label class="block text-xs uppercase tracking-widest text-[{pal['text_secondary']}] mb-2">Full Name</label>
                    <input type="text" required placeholder="Elena Rostova" class="w-full px-4 py-3 rounded-xl bg-black/40 border editorial-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
                </div>
                <div>
                    <label class="block text-xs uppercase tracking-widest text-[{pal['text_secondary']}] mb-2">Email Address</label>
                    <input type="email" required placeholder="elena@example.com" class="w-full px-4 py-3 rounded-xl bg-black/40 border editorial-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
                </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                    <label class="block text-xs uppercase tracking-widest text-[{pal['text_secondary']}] mb-2">Event Date or Window</label>
                    <input type="date" class="w-full px-4 py-3 rounded-xl bg-black/40 border editorial-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
                </div>
                <div>
                    <label class="block text-xs uppercase tracking-widest text-[{pal['text_secondary']}] mb-2">Event Location / Venue</label>
                    <input type="text" placeholder="Villa Cimbrone, Ravello" class="w-full px-4 py-3 rounded-xl bg-black/40 border editorial-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
                </div>
            </div>
            <div>
                <label class="block text-xs uppercase tracking-widest text-[{pal['text_secondary']}] mb-2">Your Story & Vision</label>
                <textarea rows="4" required placeholder="Tell us about your celebration, aesthetics, and vision..." class="w-full px-4 py-3 rounded-xl bg-black/40 border editorial-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]"></textarea>
            </div>
            <button type="submit" class="w-full py-4 rounded-full bg-[{pal['accent']}] text-black font-semibold text-xs uppercase tracking-widest hover:bg-white transition-all shadow-lg shadow-[{pal['accent']}]/20">
                Transmit Consultation Request
            </button>
        </form>
    </section>

    <!-- Footer -->
    <footer class="py-12 border-t editorial-border text-center text-xs text-[{pal['text_secondary']}]">
        <p class="font-serif text-lg text-white mb-2">{display_title} · Fine Art Photography Studio</p>
        <p>&copy; 2026 {display_title}. All rights reserved.</p>
    </footer>

    <script>
        function filterGallery(category) {{
            const cards = document.querySelectorAll('.gallery-card');
            cards.forEach(card => {{
                if (category === 'all' || card.getAttribute('data-cat') === category) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            document.querySelectorAll('.gallery-filter-btn').forEach(btn => {{
                btn.classList.remove('bg-[{pal['accent']}]', 'text-black');
                btn.classList.add('border', 'editorial-border', 'text-[{pal['text_secondary']}]');
            }});
            event.target.classList.add('bg-[{pal['accent']}]', 'text-black');
            event.target.classList.remove('border', 'editorial-border', 'text-[{pal['text_secondary']}]');
        }}

        function openLightbox(title, cat, src) {{
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox-title').textContent = title;
            document.getElementById('lightbox-cat').textContent = cat;
            document.getElementById('lightbox').classList.remove('hidden');
        }}

        function closeLightbox() {{
            document.getElementById('lightbox').classList.add('hidden');
        }}

        function handleInquirySubmit(e) {{
            e.preventDefault();
            alert('✨ Thank you. Your inquiry has been received. Our studio will review availability and be in touch within 24 hours.');
            e.target.reset();
        }}
    </script>
</body>
</html>"""


def generate_cafe_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    pal = design_profile["palette"]
    typo = design_profile["typography"]
    display_title = site_name.replace("_", " ").title()

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} · Artisan Coffee & Organic Bakery</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typo['google_fonts_url']}" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        serif: ['"{typo['display']}"', 'serif'],
                        sans: ['"{typo['body']}"', 'sans-serif']
                    }},
                    colors: {{
                        cafeBg: '{pal['bg']}',
                        cafeSurface: '{pal['surface']}',
                        cafeAccent: '{pal['accent']}',
                        cafeSecondary: '{pal['accent_secondary']}',
                        cafeText: '{pal['text_primary']}',
                        cafeMuted: '{pal['text_secondary']}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: {pal['bg']}; color: {pal['text_primary']}; }}
        .cafe-border {{ border-color: {pal['surface_border']}; }}
        .cart-drawer {{ transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1); }}
    </style>
</head>
<body class="font-sans antialiased selection:bg-[{pal['accent']}] selection:text-white">

    <!-- Header Navigation with Sticky Cart Button -->
    <header class="fixed top-0 inset-x-0 z-40 bg-[{pal['bg']}]/90 backdrop-blur-md border-b cafe-border">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="#" class="font-serif text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                <i class="fa-solid fa-mug-hot text-[{pal['accent']}] text-xl"></i>
                {display_title}
            </a>
            <nav class="hidden md:flex items-center gap-8 text-sm font-medium text-[{pal['text_secondary']}]">
                <a href="#menu" class="hover:text-white transition-colors">Menu</a>
                <a href="#about" class="hover:text-white transition-colors">Our Roastery</a>
                <a href="#location" class="hover:text-white transition-colors">Hours & Location</a>
            </nav>
            <button onclick="toggleCartDrawer()" class="relative flex items-center gap-2.5 px-4 py-2 rounded-full bg-[{pal['accent']}] text-white font-medium text-sm hover:opacity-90 transition-all shadow-lg shadow-[{pal['accent']}]/20">
                <i class="fa-solid fa-bag-shopping"></i>
                <span>Order Bag</span>
                <span id="cart-badge" class="w-5 h-5 rounded-full bg-white text-black font-bold text-xs flex items-center justify-center">0</span>
            </button>
        </div>
    </header>

    <!-- Warm Atmospheric Hero -->
    <section class="min-h-[85vh] flex items-center justify-center pt-24 pb-16 px-6 relative">
        <div class="max-w-4xl mx-auto text-center">
            <span class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[{pal['surface']}] border cafe-border text-[{pal['accent']}] text-xs uppercase tracking-widest font-semibold mb-6">
                <i class="fa-solid fa-seedling"></i> Single-Origin Micro-Roasts & Sourdough Pastries
            </span>
            <h1 class="font-serif text-5xl sm:text-7xl text-white font-bold tracking-tight leading-[1.1] mb-6">
                Handcrafted sips, roasted with soul.
            </h1>
            <p class="text-[{pal['text_secondary']}] text-base sm:text-lg max-w-xl mx-auto font-light leading-relaxed mb-8">
                Ethically sourced direct from cooperative farms in Oaxaca and Ethiopia. Baked fresh before sunrise every morning.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="#menu" class="w-full sm:w-auto px-8 py-3.5 rounded-full bg-[{pal['accent']}] text-white font-semibold text-sm hover:bg-[{pal['accent_secondary']}] transition-all shadow-xl shadow-[{pal['accent']}]/25">
                    Explore Today's Menu
                </a>
                <a href="#location" class="w-full sm:w-auto px-8 py-3.5 rounded-full bg-[{pal['surface']}] border cafe-border text-white text-sm font-medium hover:border-[{pal['accent']}] transition-all">
                    Find Our Cafe
                </a>
            </div>
        </div>
    </section>

    <!-- Interactive Menu Explorer -->
    <section id="menu" class="max-w-7xl mx-auto px-6 py-20 border-t cafe-border">
        <div class="text-center mb-12">
            <span class="text-[{pal['accent']}] text-xs uppercase tracking-widest font-bold">Artisanal Offerings</span>
            <h2 class="font-serif text-3xl sm:text-5xl text-white mt-1">Today's Brews & Bakes</h2>
        </div>

        <!-- Menu Category Filter Tabs -->
        <div class="flex items-center justify-center flex-wrap gap-2 mb-12">
            <button onclick="filterMenu('coffee')" class="menu-tab-btn px-5 py-2 rounded-full bg-[{pal['accent']}] text-white font-medium text-xs">Espresso & Brews</button>
            <button onclick="filterMenu('bakery')" class="menu-tab-btn px-5 py-2 rounded-full bg-[{pal['surface']}] border cafe-border text-[{pal['text_secondary']}] text-xs hover:text-white">Pastries & Bakes</button>
            <button onclick="filterMenu('brunch')" class="menu-tab-btn px-5 py-2 rounded-full bg-[{pal['surface']}] border cafe-border text-[{pal['text_secondary']}] text-xs hover:text-white">Farmhouse Toast & Brunch</button>
        </div>

        <!-- Dishes Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="menu-items">
            <!-- Item 1 -->
            <div class="menu-card p-6 rounded-3xl bg-[{pal['surface']}] border cafe-border flex flex-col justify-between" data-category="coffee">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-serif text-xl font-bold text-white">Spanish Honey Latte</h3>
                        <span class="font-bold text-[{pal['accent']}] text-lg">$5.75</span>
                    </div>
                    <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-4">Double shot espresso, organic local wildflower honey, warm cinnamon, and steamed oat milk.</p>
                    <span class="inline-block px-2.5 py-1 rounded-full bg-black/40 text-[10px] text-[{pal['accent']}] font-semibold">Oat Milk · Best Seller</span>
                </div>
                <button onclick="addToCart('Spanish Honey Latte', 5.75)" class="mt-6 w-full py-2.5 rounded-full bg-[{pal['accent']}] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
                    Add to Bag
                </button>
            </div>

            <!-- Item 2 -->
            <div class="menu-card p-6 rounded-3xl bg-[{pal['surface']}] border cafe-border flex flex-col justify-between" data-category="coffee">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-serif text-xl font-bold text-white">Nitro Cold Brew</h3>
                        <span class="font-bold text-[{pal['accent']}] text-lg">$5.25</span>
                    </div>
                    <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-4">Steeped 20 hours in cold filtered spring water. Infused with pure nitrogen for a Guinness-like silky crema.</p>
                    <span class="inline-block px-2.5 py-1 rounded-full bg-black/40 text-[10px] text-[{pal['accent']}] font-semibold">Single-Origin Yirgacheffe</span>
                </div>
                <button onclick="addToCart('Nitro Cold Brew', 5.25)" class="mt-6 w-full py-2.5 rounded-full bg-[{pal['accent']}] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
                    Add to Bag
                </button>
            </div>

            <!-- Item 3 -->
            <div class="menu-card p-6 rounded-3xl bg-[{pal['surface']}] border cafe-border flex flex-col justify-between" data-category="bakery">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-serif text-xl font-bold text-white">Cardamom Pistachio Cruffin</h3>
                        <span class="font-bold text-[{pal['accent']}] text-lg">$4.80</span>
                    </div>
                    <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-4">Flaky laminated croissant-muffin hybrid with roasted Sicilian pistachio cream and crushed cardamom sugar.</p>
                    <span class="inline-block px-2.5 py-1 rounded-full bg-black/40 text-[10px] text-[{pal['accent']}] font-semibold">Baked Fresh 6 AM</span>
                </div>
                <button onclick="addToCart('Cardamom Pistachio Cruffin', 4.80)" class="mt-6 w-full py-2.5 rounded-full bg-[{pal['accent']}] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
                    Add to Bag
                </button>
            </div>

            <!-- Item 4 -->
            <div class="menu-card p-6 rounded-3xl bg-[{pal['surface']}] border cafe-border flex flex-col justify-between" data-category="brunch">
                <div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-serif text-xl font-bold text-white">Whipped Ricotta Sourdough</h3>
                        <span class="font-bold text-[{pal['accent']}] text-lg">$11.50</span>
                    </div>
                    <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-4">House sourdough toast, whipped lemon ricotta, roasted mission figs, hot chili honey, and flaky sea salt.</p>
                    <span class="inline-block px-2.5 py-1 rounded-full bg-black/40 text-[10px] text-[{pal['accent']}] font-semibold">Vegetarian</span>
                </div>
                <button onclick="addToCart('Whipped Ricotta Sourdough', 11.50)" class="mt-6 w-full py-2.5 rounded-full bg-[{pal['accent']}] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
                    Add to Bag
                </button>
            </div>
        </div>
    </section>

    <!-- Slide-Out Order Bag Drawer -->
    <div id="cart-drawer" class="cart-drawer fixed inset-y-0 right-0 w-full max-w-md bg-[{pal['surface']}] border-l cafe-border z-50 transform translate-x-full shadow-2xl flex flex-col justify-between p-6">
        <div>
            <div class="flex items-center justify-between pb-4 border-b cafe-border mb-4">
                <h3 class="font-serif text-xl font-bold text-white flex items-center gap-2">
                    <i class="fa-solid fa-basket-shopping text-[{pal['accent']}]"></i> Your Pickup Order
                </h3>
                <button onclick="toggleCartDrawer()" class="text-[{pal['text_secondary']}] hover:text-white text-2xl">&times;</button>
            </div>
            <div id="cart-items-container" class="space-y-3 max-h-[60vh] overflow-y-auto pr-1">
                <p class="text-sm text-[{pal['text_secondary']}] text-center py-12">Your order bag is currently empty.</p>
            </div>
        </div>
        <div class="pt-4 border-t cafe-border">
            <div class="flex justify-between items-center text-base font-bold text-white mb-4">
                <span>Subtotal:</span>
                <span id="cart-total" class="text-[{pal['accent']}]">$0.00</span>
            </div>
            <button onclick="handleCheckout()" class="w-full py-3.5 rounded-full bg-[{pal['accent']}] text-white font-bold text-sm hover:opacity-90 transition-all shadow-lg shadow-[{pal['accent']}]/20">
                Proceed to Pickup Checkout
            </button>
        </div>
    </div>

    <!-- Location & Opening Hours -->
    <section id="location" class="max-w-7xl mx-auto px-6 py-20 border-t cafe-border">
        <div class="grid md:grid-cols-2 gap-12 bg-[{pal['surface']}] rounded-3xl p-8 sm:p-12 border cafe-border">
            <div>
                <span class="text-[{pal['accent']}] text-xs uppercase tracking-widest font-bold">Visit Us</span>
                <h3 class="font-serif text-3xl text-white mt-1 mb-4">Warm Seats & Fresh Coffee</h3>
                <p class="text-sm text-[{pal['text_secondary']}] leading-relaxed mb-6">
                    Step inside to warm sourdough aromas, vintage vinyl jazz records, and sunlight streaming through our bay windows.
                </p>
                <div class="space-y-3 text-sm text-[{pal['text_secondary']}]">
                    <p><i class="fa-solid fa-location-dot text-[{pal['accent']}] mr-3"></i> 412 Artisan Walk, Corner of Elm & 4th</p>
                    <p><i class="fa-solid fa-phone text-[{pal['accent']}] mr-3"></i> (555) 328-9400</p>
                    <p><i class="fa-solid fa-envelope text-[{pal['accent']}] mr-3"></i> hello@{site_name.lower()}.com</p>
                </div>
            </div>
            <div class="bg-black/30 p-6 rounded-2xl border cafe-border flex flex-col justify-center">
                <h4 class="font-serif text-xl font-bold text-white mb-4">Weekly Operating Hours</h4>
                <div class="space-y-2 text-sm text-[{pal['text_secondary']}]">
                    <div class="flex justify-between py-1 border-b cafe-border"><span>Monday – Friday</span><span class="text-white font-medium">6:30 AM – 6:00 PM</span></div>
                    <div class="flex justify-between py-1 border-b cafe-border"><span>Saturday</span><span class="text-white font-medium">7:00 AM – 7:00 PM</span></div>
                    <div class="flex justify-between py-1"><span>Sunday</span><span class="text-white font-medium">7:30 AM – 5:00 PM</span></div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 border-t cafe-border text-center text-xs text-[{pal['text_secondary']}]">
        <p>&copy; 2026 {display_title}. Handcrafted with love.</p>
    </footer>

    <script>
        let cart = [];

        function filterMenu(cat) {{
            const cards = document.querySelectorAll('.menu-card');
            cards.forEach(card => {{
                if (card.getAttribute('data-category') === cat) {{
                    card.style.display = 'flex';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            document.querySelectorAll('.menu-tab-btn').forEach(btn => {{
                btn.classList.remove('bg-[{pal['accent']}]', 'text-white');
                btn.classList.add('bg-[{pal['surface']}]', 'border', 'cafe-border', 'text-[{pal['text_secondary']}]');
            }});
            event.target.classList.add('bg-[{pal['accent']}]', 'text-white');
            event.target.classList.remove('bg-[{pal['surface']}]', 'border', 'cafe-border', 'text-[{pal['text_secondary']}]');
        }}

        function addToCart(title, price) {{
            cart.push({{ title, price }});
            updateCartUI();
            toggleCartDrawer(true);
        }}

        function updateCartUI() {{
            document.getElementById('cart-badge').textContent = cart.length;
            const container = document.getElementById('cart-items-container');
            if (cart.length === 0) {{
                container.innerHTML = '<p class="text-sm text-[{pal['text_secondary']}] text-center py-12">Your order bag is currently empty.</p>';
                document.getElementById('cart-total').textContent = '$0.00';
                return;
            }}
            let total = 0;
            container.innerHTML = '';
            cart.forEach((item, idx) => {{
                total += item.price;
                const div = document.createElement('div');
                div.className = 'flex justify-between items-center p-3 rounded-xl bg-black/30 border cafe-border text-sm';
                div.innerHTML = `<span>${{item.title}}</span><div class="flex items-center gap-3"><span class="font-bold text-[{pal['accent']}]">$${{item.price.toFixed(2)}}</span><button onclick="removeFromCart(${{idx}})" class="text-red-400 hover:text-red-300">&times;</button></div>`;
                container.appendChild(div);
            }});
            document.getElementById('cart-total').textContent = '$' + total.toFixed(2);
        }}

        function removeFromCart(idx) {{
            cart.splice(idx, 1);
            updateCartUI();
        }}

        function toggleCartDrawer(forceOpen) {{
            const drawer = document.getElementById('cart-drawer');
            if (forceOpen === true) {{
                drawer.classList.remove('translate-x-full');
            }} else {{
                drawer.classList.toggle('translate-x-full');
            }}
        }}

        function handleCheckout() {{
            if (cart.length === 0) return alert('Your order bag is empty!');
            alert('🎉 Order placed for in-store pickup! Estimated ready time: 10-15 minutes.');
            cart = [];
            updateCartUI();
            toggleCartDrawer(false);
        }}
    </script>
</body>
</html>"""


def generate_gym_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    pal = design_profile["palette"]
    typo = design_profile["typography"]
    display_title = site_name.replace("_", " ").upper()

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} · High-Performance Training Club</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typo['google_fonts_url']}" rel="stylesheet">
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        display: ['"{typo['display']}"', 'sans-serif'],
                        sans: ['"{typo['body']}"', 'sans-serif']
                    }},
                    colors: {{
                        gymBg: '{pal['bg']}',
                        gymSurface: '{pal['surface']}',
                        gymAccent: '{pal['accent']}',
                        gymSecondary: '{pal['accent_secondary']}',
                        gymText: '{pal['text_primary']}',
                        gymMuted: '{pal['text_secondary']}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: {pal['bg']}; color: {pal['text_primary']}; }}
        .gym-border {{ border-color: {pal['surface_border']}; }}
        .clip-athletic {{ clip-path: polygon(0 0, 100% 0, 95% 100%, 0% 100%); }}
    </style>
</head>
<body class="font-sans antialiased selection:bg-[{pal['accent']}] selection:text-black">

    <!-- Bold Athletic Navigation -->
    <header class="fixed top-0 inset-x-0 z-40 bg-[{pal['bg']}]/95 backdrop-blur-md border-b gym-border">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="#" class="font-display text-3xl font-extrabold tracking-wider text-white flex items-center gap-2">
                <i class="fa-solid fa-bolt text-[{pal['accent']}]"></i>
                {display_title}
            </a>
            <nav class="hidden md:flex items-center gap-8 text-xs uppercase tracking-widest font-bold text-[{pal['text_secondary']}]">
                <a href="#programs" class="hover:text-white transition-colors">Programs</a>
                <a href="#schedule" class="hover:text-white transition-colors">Schedule</a>
                <a href="#coaches" class="hover:text-white transition-colors">Coaches</a>
                <a href="#membership" class="hover:text-white transition-colors">Membership</a>
            </nav>
            <a href="#trial" class="px-6 py-2.5 rounded-md bg-[{pal['accent']}] text-black font-display text-sm tracking-wider uppercase font-bold hover:bg-white transition-all">
                Free Trial Pass
            </a>
        </div>
    </header>

    <!-- Kinetic Hero Section -->
    <section class="min-h-[85vh] flex items-center justify-center pt-24 pb-16 px-6 relative overflow-hidden">
        <div class="max-w-5xl mx-auto text-center">
            <span class="inline-block px-4 py-1.5 rounded-full bg-[{pal['surface']}] border gym-border text-[{pal['accent']}] font-display text-xs tracking-widest uppercase font-bold mb-6">
                ELITE STRENGTH & METABOLIC CONDITIONING
            </span>
            <h1 class="font-display text-6xl sm:text-8xl lg:text-9xl text-white font-extrabold tracking-tight uppercase leading-[0.95] mb-8">
                FORGE YOUR <span class="text-[{pal['accent']}]">STRONGEST</span> SELF.
            </h1>
            <p class="text-[{pal['text_secondary']}] text-base sm:text-lg max-w-2xl mx-auto font-normal leading-relaxed mb-10">
                World-class coaching, Eleiko Olympic weightlifting platforms, and scientifically programmed hypertrophy. Leave your excuses at the locker.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="#trial" class="w-full sm:w-auto px-10 py-4 rounded-md bg-[{pal['accent']}] text-black font-display text-base tracking-wider uppercase font-extrabold hover:bg-white transition-all shadow-xl shadow-[{pal['accent']}]/20">
                    Claim Free 1-Day Pass
                </a>
                <a href="#schedule" class="w-full sm:w-auto px-10 py-4 rounded-md border gym-border text-white font-display text-base tracking-wider uppercase font-bold hover:bg-[{pal['surface']}] transition-all">
                    View Class Timetable
                </a>
            </div>
        </div>
    </section>

    <!-- High-Impact Training Programs -->
    <section id="programs" class="max-w-7xl mx-auto px-6 py-24 border-t gym-border">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-6">
            <div>
                <span class="text-[{pal['accent']}] font-display text-sm uppercase tracking-widest font-bold">Programs</span>
                <h2 class="font-display text-4xl sm:text-6xl text-white uppercase mt-1">Disciplines Built For Power</h2>
            </div>
            <p class="text-xs text-[{pal['text_secondary']}] max-w-sm">Periodized programming designed by elite strength coaches to break plateaus.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div class="p-8 rounded-2xl bg-[{pal['surface']}] border gym-border hover:border-[{pal['accent']}] transition-all group">
                <i class="fa-solid fa-dumbbell text-3xl text-[{pal['accent']}] mb-6"></i>
                <h3 class="font-display text-2xl font-bold text-white uppercase mb-3">Olympic Barbell Club</h3>
                <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-6">Snatch, Clean & Jerk, and heavy squat cycles under USA Weightlifting certified head coaches.</p>
                <span class="text-[{pal['accent']}] font-display text-xs uppercase tracking-wider font-bold group-hover:translate-x-1 inline-block transition-transform">Explore Program &rarr;</span>
            </div>
            <div class="p-8 rounded-2xl bg-[{pal['surface']}] border gym-border hover:border-[{pal['accent']}] transition-all group">
                <i class="fa-solid fa-heart-pulse text-3xl text-[{pal['accent']}] mb-6"></i>
                <h3 class="font-display text-2xl font-bold text-white uppercase mb-3">Hyrox & Engine Lab</h3>
                <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-6">High-output aerobic power, Concept2 ski/row intervals, and functional hybrid race prep.</p>
                <span class="text-[{pal['accent']}] font-display text-xs uppercase tracking-wider font-bold group-hover:translate-x-1 inline-block transition-transform">Explore Program &rarr;</span>
            </div>
            <div class="p-8 rounded-2xl bg-[{pal['surface']}] border gym-border hover:border-[{pal['accent']}] transition-all group">
                <i class="fa-solid fa-fire text-3xl text-[{pal['accent']}] mb-6"></i>
                <h3 class="font-display text-2xl font-bold text-white uppercase mb-3">Mobility & Hypertrophy</h3>
                <p class="text-xs text-[{pal['text_secondary']}] leading-relaxed mb-6">Muscle building with joint longevity, bulletproofing connective tissue, and dynamic recovery.</p>
                <span class="text-[{pal['accent']}] font-display text-xs uppercase tracking-wider font-bold group-hover:translate-x-1 inline-block transition-transform">Explore Program &rarr;</span>
            </div>
        </div>
    </section>

    <!-- Interactive Class Timetable -->
    <section id="schedule" class="max-w-7xl mx-auto px-6 py-24 border-t gym-border">
        <div class="text-center max-w-2xl mx-auto mb-16">
            <span class="text-[{pal['accent']}] font-display text-sm uppercase tracking-widest font-bold">Daily Timetable</span>
            <h2 class="font-display text-4xl sm:text-6xl text-white uppercase mt-1">Class Schedule</h2>
        </div>
        <div class="space-y-4 max-w-4xl mx-auto">
            <div class="p-6 rounded-2xl bg-[{pal['surface']}] border gym-border flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="font-display text-sm text-[{pal['accent']}] font-bold">06:00 AM – 07:15 AM</span>
                    <h4 class="font-display text-xl text-white uppercase">Dawn Barbell & Strength</h4>
                    <p class="text-xs text-[{pal['text_secondary']}]">Coach Marcus · Olympic Platform Floor</p>
                </div>
                <a href="#trial" class="px-5 py-2 rounded bg-white text-black font-display text-xs uppercase font-bold hover:bg-[{pal['accent']}] transition-colors text-center">Book Spot</a>
            </div>
            <div class="p-6 rounded-2xl bg-[{pal['surface']}] border gym-border flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="font-display text-sm text-[{pal['accent']}] font-bold">12:00 PM – 12:45 PM</span>
                    <h4 class="font-display text-xl text-white uppercase">Lunch Engine Conditioning</h4>
                    <p class="text-xs text-[{pal['text_secondary']}]">Coach Sarah · Functional Turf</p>
                </div>
                <a href="#trial" class="px-5 py-2 rounded bg-white text-black font-display text-xs uppercase font-bold hover:bg-[{pal['accent']}] transition-colors text-center">Book Spot</a>
            </div>
            <div class="p-6 rounded-2xl bg-[{pal['surface']}] border gym-border flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <span class="font-display text-sm text-[{pal['accent']}] font-bold">06:30 PM – 07:45 PM</span>
                    <h4 class="font-display text-xl text-white uppercase">Evening Hypertrophy Blitz</h4>
                    <p class="text-xs text-[{pal['text_secondary']}]">Coach Jax · Main Weight Room</p>
                </div>
                <a href="#trial" class="px-5 py-2 rounded bg-white text-black font-display text-xs uppercase font-bold hover:bg-[{pal['accent']}] transition-colors text-center">Book Spot</a>
            </div>
        </div>
    </section>

    <!-- Membership Tiers -->
    <section id="membership" class="max-w-7xl mx-auto px-6 py-24 border-t gym-border">
        <div class="text-center max-w-2xl mx-auto mb-16">
            <span class="text-[{pal['accent']}] font-display text-sm uppercase tracking-widest font-bold">No Contracts · No Hidden Fees</span>
            <h2 class="font-display text-4xl sm:text-6xl text-white uppercase mt-1">Membership Access</h2>
        </div>
        <div class="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div class="p-8 rounded-3xl bg-[{pal['surface']}] border gym-border flex flex-col justify-between">
                <div>
                    <span class="font-display text-xs uppercase tracking-widest text-[{pal['text_secondary']}]">Basic Athlete</span>
                    <h3 class="font-display text-3xl font-bold text-white uppercase mb-4">Open Gym Access</h3>
                    <div class="font-display text-5xl font-extrabold text-white mb-6">$79 <span class="text-sm font-sans text-[{pal['text_secondary']}]">/ month</span></div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 24/7 Keycard Workstation Access</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Full Eleiko Free Weight & Turf Access</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Locker & Cold Plunge Access</li>
                    </ul>
                </div>
                <a href="#trial" class="block text-center py-3.5 rounded-md border gym-border text-white font-display text-sm uppercase font-bold hover:bg-[{pal['accent']}] hover:text-black transition-all">Join Club</a>
            </div>

            <div class="p-8 rounded-3xl bg-[{pal['surface']}] border border-[{pal['accent']}] flex flex-col justify-between relative shadow-2xl shadow-[{pal['accent']}]/10">
                <div class="absolute -top-3.5 right-6 px-3 py-1 rounded bg-[{pal['accent']}] text-black font-display text-xs font-bold uppercase">All-Inclusive</div>
                <div>
                    <span class="font-display text-xs uppercase tracking-widest text-[{pal['accent']}]">Unlimited Athlete</span>
                    <h3 class="font-display text-3xl font-bold text-white uppercase mb-4">Unlimited Coaching & Classes</h3>
                    <div class="font-display text-5xl font-extrabold text-[{pal['accent']}] mb-6">$149 <span class="text-sm font-sans text-[{pal['text_secondary']}]">/ month</span></div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Unlimited Daily Coaching Classes</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Monthly 1-on-1 Nutrition Strategy</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Infrared Sauna & Compression Boots</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Comp Entry to In-House Meets</li>
                    </ul>
                </div>
                <a href="#trial" class="block text-center py-3.5 rounded-md bg-[{pal['accent']}] text-black font-display text-sm uppercase font-bold hover:bg-white transition-all">Claim Unlimited Pass</a>
            </div>
        </div>
    </section>

    <!-- Free Trial Pass Form -->
    <section id="trial" class="max-w-2xl mx-auto px-6 py-24 border-t gym-border text-center">
        <h2 class="font-display text-4xl sm:text-5xl text-white uppercase mb-4">Claim Your Free 1-Day Trial Pass</h2>
        <p class="text-sm text-[{pal['text_secondary']}] mb-8">Test our equipment, sweat in our classes, and experience why athletes stay with us.</p>
        <form onsubmit="handleTrialSubmit(event)" class="space-y-4 bg-[{pal['surface']}] p-8 rounded-3xl border gym-border">
            <input type="text" required placeholder="Full Name" class="w-full px-4 py-3 rounded-md bg-black/50 border gym-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
            <input type="email" required placeholder="Email Address" class="w-full px-4 py-3 rounded-md bg-black/50 border gym-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
            <input type="tel" required placeholder="Phone Number" class="w-full px-4 py-3 rounded-md bg-black/50 border gym-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
            <button type="submit" class="w-full py-4 rounded-md bg-[{pal['accent']}] text-black font-display text-base uppercase font-extrabold hover:bg-white transition-all">
                Send My Trial Pass Now
            </button>
        </form>
    </section>

    <!-- Footer -->
    <footer class="py-8 border-t gym-border text-center text-xs text-[{pal['text_secondary']}]">
        <p>&copy; 2026 {display_title}. Built for greatness.</p>
    </footer>

    <script>
        function handleTrialSubmit(e) {{
            e.preventDefault();
            alert('🔥 Pass confirmed! Check your email and SMS for your 1-Day VIP QR code pass.');
            e.target.reset();
        }}
    </script>
</body>
</html>"""


def generate_architecture_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    pal = design_profile["palette"]
    typo = design_profile["typography"]
    display_title = site_name.replace("_", " ").title()

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} · Spatial Architecture & Monograph</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typo['google_fonts_url']}" rel="stylesheet">
    <!-- Three.js for Strategic 3D Massing Exploration -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        display: ['"{typo['display']}"', 'sans-serif'],
                        sans: ['"{typo['body']}"', 'sans-serif']
                    }},
                    colors: {{
                        archBg: '{pal['bg']}',
                        archSurface: '{pal['surface']}',
                        archAccent: '{pal['accent']}',
                        archSecondary: '{pal['accent_secondary']}',
                        archText: '{pal['text_primary']}',
                        archMuted: '{pal['text_secondary']}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: {pal['bg']}; color: {pal['text_primary']}; }}
        .arch-border {{ border-color: {pal['surface_border']}; }}
    </style>
</head>
<body class="font-sans antialiased selection:bg-[{pal['accent']}] selection:text-black">

    <!-- Header Navigation -->
    <header class="fixed top-0 inset-x-0 z-40 bg-[{pal['bg']}]/90 backdrop-blur-md border-b arch-border">
        <div class="max-w-7xl mx-auto px-6 py-5 flex items-center justify-between">
            <a href="#" class="font-display text-xl font-bold tracking-widest text-white uppercase">
                {display_title} <span class="text-[{pal['accent']}] font-light text-xs ml-1">/ STUDIO</span>
            </a>
            <nav class="hidden md:flex items-center gap-8 text-xs uppercase tracking-widest text-[{pal['text_secondary']}]">
                <a href="#projects" class="hover:text-white transition-colors">Projects</a>
                <a href="#spatial-3d" class="hover:text-white transition-colors">Spatial 3D Model</a>
                <a href="#philosophy" class="hover:text-white transition-colors">Philosophy</a>
                <a href="#contact" class="hover:text-white transition-colors">Inquire</a>
            </nav>
            <a href="#contact" class="px-5 py-2.5 rounded-none border border-[{pal['accent']}] text-[{pal['accent']}] text-xs uppercase tracking-widest font-semibold hover:bg-[{pal['accent']}] hover:text-black transition-all">
                Commission Studio
            </a>
        </div>
    </header>

    <!-- Monograph Hero Section -->
    <section class="min-h-[85vh] flex items-center justify-center pt-28 pb-16 px-6 relative">
        <div class="max-w-5xl mx-auto text-center">
            <span class="inline-block text-[{pal['accent']}] text-xs uppercase tracking-[0.3em] font-semibold mb-6">
                ARCHITECTURAL MONOGRAPH & URBAN RESEARCH
            </span>
            <h1 class="font-display text-5xl sm:text-7xl lg:text-8xl text-white font-bold tracking-tight leading-[1.05] mb-8">
                Form, shadow & structural permanence.
            </h1>
            <p class="text-[{pal['text_secondary']}] text-base sm:text-lg max-w-2xl mx-auto font-light leading-relaxed mb-10">
                Pioneering contemporary civic pavilions, coastal residential monoliths, and low-carbon timber massing structures.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="#projects" class="px-8 py-3.5 bg-white text-black font-semibold text-xs uppercase tracking-widest hover:bg-[{pal['accent']}] transition-all">
                    View Project Archive
                </a>
                <a href="#spatial-3d" class="px-8 py-3.5 border arch-border text-white text-xs uppercase tracking-widest hover:border-[{pal['accent']}] transition-all">
                    Interact with 3D Massing
                </a>
            </div>
        </div>
    </section>

    <!-- Strategic 3D Model Viewer Section (Useful for Architecture!) -->
    <section id="spatial-3d" class="max-w-7xl mx-auto px-6 py-20 border-t arch-border">
        <div class="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
            <div>
                <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Interactive Massing</span>
                <h2 class="font-display text-3xl sm:text-4xl text-white mt-1">Spatial Pavilion Study #04</h2>
            </div>
            <p class="text-xs text-[{pal['text_secondary']}] max-w-md">Rotate to inspect volumetric cantilever and structural geometry in real-time WebGL space.</p>
        </div>
        <div class="relative w-full h-[450px] sm:h-[550px] rounded-3xl overflow-hidden border arch-border bg-black/60 shadow-2xl">
            <canvas id="arch-3d-canvas" class="w-full h-full"></canvas>
            <div class="absolute bottom-6 left-6 font-mono text-[11px] text-[{pal['accent']}] bg-black/80 px-4 py-2 rounded border arch-border">
                <i class="fa-solid fa-cube mr-2"></i> Click & drag to orbit spatial structure
            </div>
        </div>
    </section>

    <!-- Project Archive Grid -->
    <section id="projects" class="max-w-7xl mx-auto px-6 py-24 border-t arch-border">
        <div class="text-center max-w-2xl mx-auto mb-16">
            <span class="text-[{pal['accent']}] text-xs uppercase tracking-[0.25em] font-semibold">Selected Typologies</span>
            <h2 class="font-display text-4xl sm:text-5xl text-white mt-1">Completed Monograph</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div class="group cursor-pointer">
                <div class="aspect-[16/10] overflow-hidden rounded-2xl bg-[{pal['surface']}] mb-6">
                    <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80" alt="Villa Cantilever" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                </div>
                <div class="flex justify-between items-baseline">
                    <h3 class="font-display text-2xl text-white">Villa Cantilever</h3>
                    <span class="text-xs text-[{pal['accent']}] uppercase tracking-widest">Kyoto, Japan · 2025</span>
                </div>
                <p class="text-xs text-[{pal['text_secondary']}] mt-2">Board-formed architectural concrete and charred cedar cantilevered over granite bluff.</p>
            </div>

            <div class="group cursor-pointer">
                <div class="aspect-[16/10] overflow-hidden rounded-2xl bg-[{pal['surface']}] mb-6">
                    <img src="https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=1200&q=80" alt="Nordic Civic Library" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700">
                </div>
                <div class="flex justify-between items-baseline">
                    <h3 class="font-display text-2xl text-white">The Timber Vault</h3>
                    <span class="text-xs text-[{pal['accent']}] uppercase tracking-widest">Oslo, Norway · 2024</span>
                </div>
                <p class="text-xs text-[{pal['text_secondary']}] mt-2">Mass timber glulam structural lattice sheltering communal municipal library.</p>
            </div>
        </div>
    </section>

    <!-- Studio Inquiry Form -->
    <section id="contact" class="max-w-3xl mx-auto px-6 py-24 border-t arch-border text-center">
        <h2 class="font-display text-3xl sm:text-4xl text-white uppercase mb-4">Commission Consultation</h2>
        <p class="text-xs text-[{pal['text_secondary']}] mb-10 max-w-md mx-auto">Discuss prospective commercial, civic, or private residential commissions with our partners.</p>
        <form onsubmit="handleArchSubmit(event)" class="space-y-4 text-left bg-[{pal['surface']}] p-8 sm:p-12 rounded-2xl border arch-border">
            <input type="text" required placeholder="Principal / Organization Name" class="w-full px-4 py-3 rounded-none bg-black/40 border arch-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
            <input type="email" required placeholder="Direct Contact Email" class="w-full px-4 py-3 rounded-none bg-black/40 border arch-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]">
            <textarea rows="4" required placeholder="Project Scope, Location, and Timeline..." class="w-full px-4 py-3 rounded-none bg-black/40 border arch-border text-white text-sm focus:outline-none focus:border-[{pal['accent']}]"></textarea>
            <button type="submit" class="w-full py-4 rounded-none bg-[{pal['accent']}] text-black font-semibold text-xs uppercase tracking-widest hover:bg-white transition-all">
                Submit Spatial Brief
            </button>
        </form>
    </section>

    <!-- Footer -->
    <footer class="py-8 border-t arch-border text-center text-xs text-[{pal['text_secondary']}]">
        <p>&copy; 2026 {display_title}. Architectural Practice.</p>
    </footer>

    <!-- Three.js Architectural Massing Script -->
    <script>
        const canvas = document.getElementById('arch-3d-canvas');
        if (canvas) {{
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(45, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
            camera.position.set(4, 3, 5);

            const renderer = new THREE.WebGLRenderer({{ canvas, alpha: true, antialias: true }});
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            // Lighting
            const ambient = new THREE.AmbientLight(0xffffff, 0.8);
            scene.add(ambient);
            const dir = new THREE.DirectionalLight(0xfff5e6, 2);
            dir.position.set(5, 10, 7);
            scene.add(dir);

            // Architectural Structural Group (Massing study)
            const group = new THREE.Group();

            // Ground base slab
            const baseGeo = new THREE.BoxGeometry(4, 0.1, 3);
            const baseMat = new THREE.MeshStandardMaterial({{ color: 0x333338, roughness: 0.9 }});
            const baseMesh = new THREE.Mesh(baseGeo, baseMat);
            baseMesh.position.y = -0.5;
            group.add(baseMesh);

            // Cantilevered block
            const blockGeo = new THREE.BoxGeometry(2.5, 1.2, 1.8);
            const blockMat = new THREE.MeshStandardMaterial({{ color: 0xd4a373, metalness: 0.2, roughness: 0.4 }});
            const blockMesh = new THREE.Mesh(blockGeo, blockMat);
            blockMesh.position.set(0.4, 0.4, 0);
            group.add(blockMesh);

            // Glass curtain wall insert
            const glassGeo = new THREE.BoxGeometry(1.6, 0.8, 1.9);
            const glassMat = new THREE.MeshStandardMaterial({{ color: 0x90caf9, transparent: true, opacity: 0.6, roughness: 0.1 }});
            const glassMesh = new THREE.Mesh(glassGeo, glassMat);
            glassMesh.position.set(-0.6, 0.1, 0);
            group.add(glassMesh);

            scene.add(group);

            let isDragging = false, prevX = 0, prevY = 0;
            canvas.addEventListener('mousedown', e => {{ isDragging = true; prevX = e.clientX; prevY = e.clientY; }});
            window.addEventListener('mouseup', () => isDragging = false);
            window.addEventListener('mousemove', e => {{
                if (!isDragging) return;
                const deltaX = e.clientX - prevX;
                const deltaY = e.clientY - prevY;
                group.rotation.y += deltaX * 0.01;
                group.rotation.x += deltaY * 0.01;
                prevX = e.clientX;
                prevY = e.clientY;
            }});

            function animate() {{
                requestAnimationFrame(animate);
                if (!isDragging) group.rotation.y += 0.003;
                camera.lookAt(0, 0, 0);
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                camera.aspect = canvas.clientWidth / canvas.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(canvas.clientWidth, canvas.clientHeight);
            }});
        }}

        function handleArchSubmit(e) {{
            e.preventDefault();
            alert('🏛️ Consultation brief transmitted. Studio partners will reach out within 48 hours.');
            e.target.reset();
        }}
    </script>
</body>
</html>"""


def generate_saas_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    pal = design_profile["palette"]
    typo = design_profile["typography"]
    display_title = site_name.replace("_", " ").title()

    return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} · Intelligent Autonomous Cloud Platform</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="{typo['google_fonts_url']}" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{
                        display: ['"{typo['display']}"', 'sans-serif'],
                        sans: ['"{typo['body']}"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }},
                    colors: {{
                        techBg: '{pal['bg']}',
                        techSurface: '{pal['surface']}',
                        techAccent: '{pal['accent']}',
                        techSecondary: '{pal['accent_secondary']}',
                        techText: '{pal['text_primary']}',
                        techMuted: '{pal['text_secondary']}'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: {pal['bg']}; color: {pal['text_primary']}; }}
        .tech-border {{ border-color: {pal['surface_border']}; }}
        .glass-saas {{ background: rgba(14, 20, 36, 0.7); backdrop-filter: blur(20px); border: 1px solid {pal['surface_border']}; }}
    </style>
</head>
<body class="font-sans antialiased selection:bg-[{pal['accent']}] selection:text-white">

    <!-- Header Navigation with App Sign-In -->
    <header class="fixed top-0 inset-x-0 z-40 bg-[{pal['bg']}]/80 backdrop-blur-md border-b tech-border">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="#" class="font-display text-xl font-bold tracking-tight text-white flex items-center gap-2.5">
                <span class="w-3 h-3 rounded-full bg-[{pal['accent']}] shadow-lg shadow-[{pal['accent']}]"></span>
                {display_title}
            </a>
            <nav class="hidden md:flex items-center gap-8 text-xs font-medium text-[{pal['text_secondary']}]">
                <a href="#demo" class="hover:text-white transition-colors">Live Demo</a>
                <a href="#features" class="hover:text-white transition-colors">Architecture</a>
                <a href="#pricing" class="hover:text-white transition-colors">Pricing</a>
            </nav>
            <div class="flex items-center gap-3">
                <a href="#pricing" class="px-5 py-2 rounded-xl bg-gradient-to-r from-[{pal['accent']}] to-[{pal['accent_secondary']}] text-white text-xs font-semibold hover:opacity-90 transition-opacity">
                    Start Free Trial
                </a>
            </div>
        </div>
    </header>

    <!-- Interactive Hero with 3D Canvas -->
    <section class="min-h-[90vh] flex items-center justify-center pt-28 pb-16 px-6 relative overflow-hidden">
        <div class="max-w-5xl mx-auto text-center relative z-10">
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[{pal['surface']}] border tech-border text-[{pal['accent_secondary']}] text-xs font-mono mb-8">
                <span class="w-2 h-2 rounded-full bg-[{pal['accent_secondary']}] animate-ping"></span>
                v3.4 Production Release · 99.99% Uptime SLA
            </div>
            <h1 class="font-display text-5xl sm:text-7xl lg:text-8xl text-white font-extrabold tracking-tight leading-[1.05] mb-8">
                Autonomous Cloud Orchestration at Scale.
            </h1>
            <p class="text-[{pal['text_secondary']}] text-base sm:text-lg max-w-2xl mx-auto font-normal leading-relaxed mb-10">
                Deploy, monitor, and scale distributed multi-cloud workloads with intelligent real-time resource optimization.
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
                <a href="#pricing" class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[{pal['accent']}] text-white font-semibold text-xs uppercase tracking-wider hover:bg-white hover:text-black transition-all shadow-xl shadow-[{pal['accent']}]/25">
                    Start Free 14-Day Trial
                </a>
                <a href="#demo" class="w-full sm:w-auto px-8 py-3.5 rounded-xl glass-saas text-white text-xs uppercase tracking-wider font-semibold hover:border-[{pal['accent']}] transition-all">
                    Explore Live Demo
                </a>
            </div>
        </div>
        <!-- 3D Interactive Mesh Container -->
        <div class="absolute inset-0 pointer-events-none opacity-40">
            <canvas id="saas-hero-canvas" class="w-full h-full"></canvas>
        </div>
    </section>

    <!-- Interactive Live Demo Sandbox -->
    <section id="demo" class="max-w-6xl mx-auto px-6 py-20 border-t tech-border">
        <div class="text-center mb-12">
            <span class="text-[{pal['accent_secondary']}] text-xs font-mono uppercase tracking-widest">Interactive Sandbox</span>
            <h2 class="font-display text-3xl sm:text-5xl text-white mt-1">Live Workload Simulator</h2>
        </div>
        <div class="glass-saas p-8 rounded-3xl">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 text-center">
                <div class="p-6 rounded-2xl bg-black/40 border tech-border">
                    <span class="text-xs font-mono text-[{pal['text_secondary']}]">Throughput</span>
                    <div id="sim-throughput" class="text-3xl font-mono font-bold text-[{pal['accent_secondary']}] mt-1">142,800 req/s</div>
                </div>
                <div class="p-6 rounded-2xl bg-black/40 border tech-border">
                    <span class="text-xs font-mono text-[{pal['text_secondary']}]">Global Latency</span>
                    <div id="sim-latency" class="text-3xl font-mono font-bold text-emerald-400 mt-1">11.4 ms</div>
                </div>
                <div class="p-6 rounded-2xl bg-black/40 border tech-border">
                    <span class="text-xs font-mono text-[{pal['text_secondary']}]">Cost Efficiency</span>
                    <div class="text-3xl font-mono font-bold text-[{pal['accent']}] mt-1">-42.6%</div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-xl bg-black/50 border tech-border">
                <span class="text-xs font-mono text-[{pal['text_secondary']}]">Simulate Traffic Surge:</span>
                <div class="flex gap-2">
                    <button onclick="setSim('normal')" class="px-3 py-1.5 rounded-lg bg-[{pal['surface']}] text-xs font-mono text-white hover:border-[{pal['accent']}]">Normal (10k)</button>
                    <button onclick="setSim('spike')" class="px-3 py-1.5 rounded-lg bg-[{pal['accent']}] text-xs font-mono text-white font-bold">Black Friday (500k)</button>
                </div>
            </div>
        </div>
    </section>

    <!-- Pricing Matrix -->
    <section id="pricing" class="max-w-6xl mx-auto px-6 py-20 border-t tech-border">
        <div class="text-center mb-16">
            <span class="text-[{pal['accent_secondary']}] text-xs font-mono uppercase tracking-widest">Predictable Scaling</span>
            <h2 class="font-display text-3xl sm:text-5xl text-white mt-1">Pricing Tiers</h2>
        </div>
        <div class="grid md:grid-cols-3 gap-8">
            <div class="glass-saas p-8 rounded-3xl flex flex-col justify-between">
                <div>
                    <h3 class="text-xl font-bold text-white mb-2">Developer</h3>
                    <div class="text-4xl font-mono font-bold text-white my-4">$0 <span class="text-xs text-[{pal['text_secondary']}]">/ mo</span></div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 100,000 monthly events</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Community Discord support</li>
                    </ul>
                </div>
                <button onclick="alert('Trial started!')" class="w-full py-3 rounded-xl border tech-border text-white text-xs font-semibold hover:border-[{pal['accent']}]">Get Started</button>
            </div>

            <div class="glass-saas p-8 rounded-3xl border-[{pal['accent']}] shadow-xl shadow-[{pal['accent']}]/20 flex flex-col justify-between relative">
                <div class="absolute -top-3.5 right-6 px-3 py-1 rounded-full bg-[{pal['accent']}] text-white text-[10px] font-bold uppercase">Pro Scale</div>
                <div>
                    <h3 class="text-xl font-bold text-white mb-2">Team Pro</h3>
                    <div class="text-4xl font-mono font-bold text-[{pal['accent']}] my-4">$129 <span class="text-xs text-[{pal['text_secondary']}]">/ mo</span></div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 10M monthly events</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Automatic multi-region failover</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> 99.99% Guaranteed SLA</li>
                    </ul>
                </div>
                <button onclick="alert('Team trial activated!')" class="w-full py-3 rounded-xl bg-[{pal['accent']}] text-white text-xs font-semibold hover:opacity-90">Start 14-Day Pro Trial</button>
            </div>

            <div class="glass-saas p-8 rounded-3xl flex flex-col justify-between">
                <div>
                    <h3 class="text-xl font-bold text-white mb-2">Enterprise</h3>
                    <div class="text-4xl font-mono font-bold text-white my-4">Custom</div>
                    <ul class="text-xs text-[{pal['text_secondary']}] space-y-3 mb-8">
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Unlimited throughput</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Dedicated Slack channel & TAM</li>
                        <li><i class="fa-solid fa-check text-[{pal['accent']}] mr-2"></i> Custom VPC peering & HIPAA</li>
                    </ul>
                </div>
                <button onclick="alert('Enterprise team contacted!')" class="w-full py-3 rounded-xl border tech-border text-white text-xs font-semibold hover:border-[{pal['accent']}]">Contact Solutions</button>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="py-8 border-t tech-border text-center text-xs text-[{pal['text_secondary']}] font-mono">
        <p>&copy; 2026 {display_title}. Autonomous Cloud Systems.</p>
    </footer>

    <!-- Three.js Tech Mesh Script -->
    <script>
        const canvas = document.getElementById('saas-hero-canvas');
        if (canvas) {{
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(50, canvas.clientWidth / canvas.clientHeight, 0.1, 100);
            camera.position.z = 5;

            const renderer = new THREE.WebGLRenderer({{ canvas, alpha: true, antialias: true }});
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);

            const geo = new THREE.IcosahedronGeometry(2, 2);
            const mat = new THREE.MeshBasicMaterial({{ color: 0x7c3aed, wireframe: true }});
            const mesh = new THREE.Mesh(geo, mat);
            scene.add(mesh);

            function anim() {{
                requestAnimationFrame(anim);
                mesh.rotation.x += 0.003;
                mesh.rotation.y += 0.005;
                renderer.render(scene, camera);
            }}
            anim();
        }}

        function setSim(mode) {{
            if (mode === 'spike') {{
                document.getElementById('sim-throughput').textContent = '548,200 req/s';
                document.getElementById('sim-latency').textContent = '14.2 ms';
            }} else {{
                document.getElementById('sim-throughput').textContent = '142,800 req/s';
                document.getElementById('sim-latency').textContent = '11.4 ms';
            }}
        }}
    </script>
</body>
</html>"""


def generate_domain_native_html(site_name: str, design_profile: Dict[str, Any]) -> str:
    """
    Main dispatcher routing to the bespoke domain architecture synthesizer.
    """
    domain = design_profile.get("domain", "saas_tech")
    if domain == "photography":
        return generate_photography_html(site_name, design_profile)
    elif domain == "restaurant_cafe":
        return generate_cafe_html(site_name, design_profile)
    elif domain == "fitness_gym":
        return generate_gym_html(site_name, design_profile)
    elif domain == "architecture":
        return generate_architecture_html(site_name, design_profile)
    elif domain == "saas_tech":
        return generate_saas_html(site_name, design_profile)
    else:
        # Default tailored
        return generate_saas_html(site_name, design_profile)
