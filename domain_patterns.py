"""
J.A.R.V.I.S. Domain Design Patterns & Component Architecture
Defines domain-specific design vocabularies, typography strategies, color harmonies,
UX patterns, anti-patterns, and tailored HTML/CSS/JS generation components.
"""

from typing import Dict, Any, List

DOMAIN_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "photography": {
        "display_name": "Photography & Visual Arts Studio",
        "brand_personalities": ["cinematic", "editorial", "timeless", "intimate", "premium", "poetic"],
        "typography": {
            "display": "Playfair Display",
            "body": "Plus Jakarta Sans",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap",
            "style_note": "High-contrast editorial serif paired with restrained modern sans-serif"
        },
        "color_palettes": [
            {
                "name": "Moody Editorial Noir",
                "bg": "#0D0E11",
                "surface": "#16181D",
                "surface_border": "rgba(255, 255, 255, 0.08)",
                "text_primary": "#F7F6F2",
                "text_secondary": "#A0A4B0",
                "accent": "#C9A96E",  # Warm champagne gold
                "accent_secondary": "#8A94A6",
                "tag": "dark-luxury"
            },
            {
                "name": "Alabaster Fine-Art",
                "bg": "#FBF9F5",
                "surface": "#FFFFFF",
                "surface_border": "rgba(30, 30, 30, 0.08)",
                "text_primary": "#1A1A1A",
                "text_secondary": "#6E6E6E",
                "accent": "#8A7968",  # Earthy muted taupe
                "accent_secondary": "#4A5859",
                "tag": "light-editorial"
            },
            {
                "name": "Golden Hour Warmth",
                "bg": "#141210",
                "surface": "#1F1B17",
                "surface_border": "rgba(224, 185, 131, 0.12)",
                "text_primary": "#FBF8F3",
                "text_secondary": "#B5A799",
                "accent": "#D4A359",  # Rich warm amber
                "accent_secondary": "#9E7B54",
                "tag": "warm-cinematic"
            }
        ],
        "ux_patterns": {
            "primary_action": "Inquire for Dates & Booking",
            "navigation_style": "Minimalist transparent floating nav with delicate monogram",
            "components": [
                "CinematicHero",
                "EditorialMasonryGallery",
                "BeforeAfterInteractiveSlider",
                "ArtistPhilosophyStory",
                "CuratedInvestmentPackages",
                "ClientLoveTestimonials",
                "ConsultationBookingModal"
            ]
        },
        "three_d_policy": {
            "default_enabled": False,
            "recommended_usage": ["Depth-of-field gallery tilt", "Subtle cursor focal plane depth"],
            "rationale": "High-resolution photography demands instantaneous visual fidelity; heavy 3D geometry distracts from client photographic work unless subtle spatial depth is requested."
        },
        "forbidden_terms": [
            "quantum", "neural", "tactical core", "quantum mesh", "terminal simulator",
            "latency: 9ms", "bashing", "stark industries", "mission parameters", "payload",
            "transactions per second", "microsecond execution", "ai engine status"
        ]
    },

    "restaurant_cafe": {
        "display_name": "Artisan Cafe, Bakery & Culinary Bistro",
        "brand_personalities": ["artisanal", "appetizing", "inviting", "warm", "epicurean", "neighborhood-cozy"],
        "typography": {
            "display": "Fraunces",
            "body": "Plus Jakarta Sans",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap",
            "style_note": "Warm, tactile character serif with gentle curves and legible modern sans"
        },
        "color_palettes": [
            {
                "name": "Roasted Caramel Bistro",
                "bg": "#120E0C",
                "surface": "#1D1714",
                "surface_border": "rgba(230, 160, 90, 0.12)",
                "text_primary": "#FAF6F0",
                "text_secondary": "#BFAFA5",
                "accent": "#E07A38",  # Warm toasted pumpkin / terracotta
                "accent_secondary": "#D4A373",
                "tag": "warm-bistro"
            },
            {
                "name": "Botanical Garden Cafe",
                "bg": "#0D1612",
                "surface": "#15221C",
                "surface_border": "rgba(100, 180, 130, 0.12)",
                "text_primary": "#F6FAF7",
                "text_secondary": "#A2B5AA",
                "accent": "#5EAF81",  # Matcha green
                "accent_secondary": "#D9A05B",
                "tag": "botanical-fresh"
            },
            {
                "name": "Cream & Espresso Daylight",
                "bg": "#FAF7F2",
                "surface": "#FFFFFF",
                "surface_border": "rgba(80, 50, 30, 0.08)",
                "text_primary": "#2C1E17",
                "text_secondary": "#755F54",
                "accent": "#C45E28",  # Warm roasted coffee red-orange
                "accent_secondary": "#8B5E3C",
                "tag": "light-bakery"
            }
        ],
        "ux_patterns": {
            "primary_action": "Order for Pickup / Reserve a Table",
            "navigation_style": "Clean category pill navigation with sticky cart preview counter",
            "components": [
                "AtmosphericCafeHero",
                "InteractiveMenuExplorer",
                "CategoryTabFilterNav",
                "LiveCartDrawerManager",
                "SpecialtySignatureDishCallout",
                "HoursLocationInteractiveCard",
                "TableReservationModal"
            ]
        },
        "three_d_policy": {
            "default_enabled": False,
            "recommended_usage": [],
            "rationale": "Culinary patrons prioritize immediate appetite stimulation, dish pricing, and frictionless menu ordering. 3D meshes introduce unnecessary friction to hunger-driven ordering flows."
        },
        "forbidden_terms": [
            "quantum", "neural", "tactical core", "quantum mesh", "terminal simulator",
            "latency: 9ms", "bashing", "stark industries", "mission parameters", "payload",
            "tier 01", "tier 02", "tier 03", "enterprise protocol"
        ]
    },

    "fitness_gym": {
        "display_name": "Athletic Training, Gym & Performance Club",
        "brand_personalities": ["energetic", "relentless", "dynamic", "motivating", "high-performance", "disciplined"],
        "typography": {
            "display": "Oswald",
            "body": "Montserrat",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap",
            "style_note": "Aggressive condensed athletic display with high-energy geometric sans"
        },
        "color_palettes": [
            {
                "name": "Volt Energy & Matte Carbon",
                "bg": "#0A0B0D",
                "surface": "#13151A",
                "surface_border": "rgba(218, 255, 0, 0.15)",
                "text_primary": "#FFFFFF",
                "text_secondary": "#959CA6",
                "accent": "#D4FF00",  # High-vis Volt Yellow / Lime
                "accent_secondary": "#FF3B30",
                "tag": "high-voltage"
            },
            {
                "name": "Forge Crimson & Titanium",
                "bg": "#0D0D10",
                "surface": "#17171C",
                "surface_border": "rgba(255, 59, 48, 0.18)",
                "text_primary": "#FFFFFF",
                "text_secondary": "#A3A3B0",
                "accent": "#FF3B30",  # Intense Forge Red
                "accent_secondary": "#FF9500",
                "tag": "heavy-iron"
            },
            {
                "name": "Apex Athletic Cyan",
                "bg": "#070B14",
                "surface": "#0E1524",
                "surface_border": "rgba(0, 168, 255, 0.18)",
                "text_primary": "#FFFFFF",
                "text_secondary": "#8D9CB3",
                "accent": "#00A8FF",  # Hydro Sport Blue
                "accent_secondary": "#00E5FF",
                "tag": "clean-athletic"
            }
        ],
        "ux_patterns": {
            "primary_action": "Claim Free 1-Day Trial Pass",
            "navigation_style": "Bold uppercase athletic bar with high-contrast Action CTA button",
            "components": [
                "HighImpactKineticHero",
                "TrainingProgramExplorer",
                "InteractiveClassTimetable",
                "EliteCoachRosterCards",
                "AthleteTransformationShowcase",
                "TransparentMembershipPricing",
                "FreePassClaimModal"
            ]
        },
        "three_d_policy": {
            "default_enabled": False,
            "recommended_usage": ["3D muscle group selector (if anatomy interactive is requested)"],
            "rationale": "High-conversion gym interfaces require bold typography, visceral human fitness photography, and easy class scheduling rather than abstract floating 3D geometry."
        },
        "forbidden_terms": [
            "quantum", "neural", "tactical core", "quantum mesh", "terminal simulator",
            "latency: 9ms", "bashing", "stark industries", "mission parameters", "payload",
            "single-point of failure"
        ]
    },

    "architecture": {
        "display_name": "Architectural Studio & Spatial Design Practice",
        "brand_personalities": ["monumental", "spatial", "meticulous", "visionary", "structural", "refined"],
        "typography": {
            "display": "Syne",
            "body": "Archivo",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Syne:wght@500;700;800&family=Archivo:wght@300;400;500;600&display=swap",
            "style_note": "Geometric structural display font with architectural precision sans"
        },
        "color_palettes": [
            {
                "name": "Brutalist Concrete & Monolith",
                "bg": "#121315",
                "surface": "#1A1B1F",
                "surface_border": "rgba(255, 255, 255, 0.08)",
                "text_primary": "#F2F3F5",
                "text_secondary": "#989BA3",
                "accent": "#D4A373",  # Cast brass / timber accent
                "accent_secondary": "#7A8288",
                "tag": "monumental"
            },
            {
                "name": "Nordic Limestone Minimal",
                "bg": "#F5F3EE",
                "surface": "#FFFFFF",
                "surface_border": "rgba(20, 20, 20, 0.06)",
                "text_primary": "#191A1C",
                "text_secondary": "#63666A",
                "accent": "#A37A58",  # Natural oak
                "accent_secondary": "#3E454C",
                "tag": "nordic-light"
            }
        ],
        "ux_patterns": {
            "primary_action": "Request Commission / View Monograph",
            "navigation_style": "Spacious grid-aligned architectural navigation with project index",
            "components": [
                "SpatialMonographHero",
                "InteractiveProjectTypologyGrid",
                "Interactive3DBuildingMassingViewer",
                "ProjectTimelinePhases",
                "MaterialityCraftsmanshipShowcase",
                "StudioPhilosophySection",
                "CommissionConsultationForm"
            ]
        },
        "three_d_policy": {
            "default_enabled": True,
            "recommended_usage": ["Interactive 3D building structural massing / pavilion wireframe orbit viewer"],
            "rationale": "Architecture is intrinsically three-dimensional. An interactive 3D spatial model viewer directly showcases spatial volume, structural cantilever, and geometric harmony in real time."
        },
        "forbidden_terms": [
            "quantum", "neural", "tactical core", "quantum mesh", "terminal simulator",
            "latency: 9ms", "bashing", "stark industries", "mission parameters", "payload",
            "cyberpunk neon"
        ]
    },

    "saas_tech": {
        "display_name": "Software Platform, AI Cloud & Developer Tools",
        "brand_personalities": ["innovative", "analytical", "scalable", "futuristic", "precision", "intelligent"],
        "typography": {
            "display": "Space Grotesk",
            "body": "Plus Jakarta Sans",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
            "style_note": "Futuristic geometric tech headline with ultra-clean software sans and code mono"
        },
        "color_palettes": [
            {
                "name": "Deep Tech Indigo & Violet",
                "bg": "#060913",
                "surface": "#0E1424",
                "surface_border": "rgba(124, 58, 237, 0.2)",
                "text_primary": "#F1F5F9",
                "text_secondary": "#94A3B8",
                "accent": "#7C3AED",  # Electric Violet
                "accent_secondary": "#06B6D4",  # Cyan Aura
                "tag": "deep-tech"
            },
            {
                "name": "Bento Minimal White & Emerald",
                "bg": "#FAFBFC",
                "surface": "#FFFFFF",
                "surface_border": "rgba(226, 232, 240, 0.8)",
                "text_primary": "#0F172A",
                "text_secondary": "#475569",
                "accent": "#10B981",  # Precision Emerald
                "accent_secondary": "#2563EB",
                "tag": "clean-saas"
            }
        ],
        "ux_patterns": {
            "primary_action": "Start Free 14-Day Trial",
            "navigation_style": "Sticky software navbar with status badge, doc links, and App sign-in",
            "components": [
                "InteractiveDemoHero",
                "LiveInteractive3DDataMesh",
                "RealtimeMetricsStatsGrid",
                "FeatureMatrixTabs",
                "InteractiveDashboardPreview",
                "EcosystemIntegrationBadges",
                "MonthlyAnnualPricingMatrix"
            ]
        },
        "three_d_policy": {
            "default_enabled": True,
            "recommended_usage": ["Interactive 3D neural node cluster / data sphere with mouse reaction"],
            "rationale": "SaaS and AI systems benefit significantly from 3D interactive visualizations as an intuitive metaphor for complex distributed systems and autonomous algorithms."
        },
        "forbidden_terms": []  # Tech domains are allowed technical terminology
    },

    "luxury_brand": {
        "display_name": "Luxury Maison, Haute Horlogerie & Fashion",
        "brand_personalities": ["exclusive", "understated", "timeless", "sophisticated", "rare", "impeccable"],
        "typography": {
            "display": "Cormorant Garamond",
            "body": "Montserrat",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Montserrat:wght@300;400;500&display=swap",
            "style_note": "Ultra-refined high-fashion Roman serif with airy spaced sans"
        },
        "color_palettes": [
            {
                "name": "Maison Noir & Champagne Silk",
                "bg": "#0B0B0C",
                "surface": "#141416",
                "surface_border": "rgba(212, 175, 55, 0.15)",
                "text_primary": "#FAF8F5",
                "text_secondary": "#9C9B98",
                "accent": "#CBB279",  # Antique champagne gold
                "accent_secondary": "#7D7B75",
                "tag": "haute-luxe"
            }
        ],
        "ux_patterns": {
            "primary_action": "Schedule Private Salon Appointment",
            "navigation_style": "Centered heritage emblem with expansive airy spacing",
            "components": [
                "MonochromeEditorialHero",
                "CuratedLookbookSlider",
                "HeritageStorytellingChapter",
                "LimitedEditionShowcase",
                "VIPPrivateSalonBooking"
            ]
        },
        "three_d_policy": {
            "default_enabled": False,
            "recommended_usage": ["Subtle 3D object rotation for high-jewelry / watch timepieces if explicitly asked"],
            "rationale": "True luxury is conveyed through generous whitespace, high-craft typography, and tactile restraint. Loud 3D animations risk appearing gimmicky."
        },
        "forbidden_terms": [
            "quantum", "neural", "tactical core", "quantum mesh", "terminal simulator",
            "latency: 9ms", "bashing", "stark industries", "mission parameters", "payload",
            "save 25%", "discount", "cheap", "bulk"
        ]
    }
}


def detect_domain_from_text(prompt_or_purpose: str) -> str:
    """
    Classifies a user prompt or project purpose into a target design domain.
    """
    clean = prompt_or_purpose.lower()

    if any(k in clean for k in ["photo", "photographer", "photography", "portrait", "wedding photo", "camera", "lens", "shoot"]):
        return "photography"
    if any(k in clean for k in ["cafe", "coffee", "restaurant", "bakery", "food", "dining", "menu", "bistro", "eatery", "pizza", "burger", "luna cafe"]):
        return "restaurant_cafe"
    if any(k in clean for k in ["gym", "fitness", "workout", "crossfit", "trainer", "bodybuilding", "athletic", "training club", "yoga"]):
        return "fitness_gym"
    if any(k in clean for k in ["architect", "architecture", "interior design", "building", "spatial", "facade", "monograph", "blueprint"]):
        return "architecture"
    if any(k in clean for k in ["luxury", "jewelry", "fashion", "couture", "watch", "maison", "perfume"]):
        return "luxury_brand"
    if any(k in clean for k in ["saas", "software", "ai", "cloud", "api", "platform", "cyber", "neural", "developer", "fintech", "startup", "app"]):
        return "saas_tech"

    # Default to modern web application
    return "saas_tech"
