"""
J.A.R.V.I.S. Design Intelligence Engine
Translates user requirements, business domain, audience psychographics, and brand personality
into a tailored, domain-native Design Profile and Google Stitch Design Brief.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional
from domain_patterns import DOMAIN_TAXONOMY, detect_domain_from_text

logger = logging.getLogger("DesignIntelligence")
logger.setLevel(logging.INFO)


# ==============================================================================
# 1. 3D DECISION SYSTEM
# ==============================================================================

class ThreeDDecisionSystem:
    """
    Evaluates whether 3D WebGL graphics genuinely improve UX or represent decorative bloat.
    5 Internal Tests:
    1. Does 3D improve the user experience?
    2. Does it fit the business ethos?
    3. Does it communicate something genuinely useful (spatial/data)?
    4. Will it degrade mobile performance or fast ordering?
    5. Is it appropriate for the target audience?
    """

    @staticmethod
    def evaluate(domain: str, user_prompt: str, business_type: str = "") -> Dict[str, Any]:
        clean_text = (user_prompt + " " + business_type).lower()
        explicit_3d_requested = any(w in clean_text for w in ["3d", "three.js", "threejs", "webgl", "interactive 3d", "spatial model", "canvas 3d"])
        explicit_no_3d = any(w in clean_text for w in ["no 3d", "disable 3d", "flat", "2d only", "lightweight", "fast load"])

        if explicit_no_3d:
            return {
                "enabled": False,
                "usage": [],
                "reason": "User explicitly requested a clean 2D lightweight experience without 3D WebGL."
            }

        domain_meta = DOMAIN_TAXONOMY.get(domain, DOMAIN_TAXONOMY["saas_tech"])
        three_d_policy = domain_meta["three_d_policy"]

        # If user explicitly asked for 3D on any domain, honor it with domain-tailored usage
        if explicit_3d_requested:
            if domain == "photography":
                return {
                    "enabled": True,
                    "usage": ["Interactive 3D camera lens aperture depth-of-field viewer tracking cursor motion"],
                    "reason": "User explicitly requested 3D capabilities. Applied domain-appropriate depth-of-field optics simulation."
                }
            elif domain == "restaurant_cafe":
                return {
                    "enabled": True,
                    "usage": ["Interactive 3D artisanal coffee cup / steam particle physics simulation"],
                    "reason": "User requested 3D interaction. Applied lightweight culinary ambient particle experience."
                }
            elif domain == "fitness_gym":
                return {
                    "enabled": True,
                    "usage": ["Interactive 3D athletic equipment / anatomical power zone rotator"],
                    "reason": "User explicitly requested 3D visualization. Applied sports performance equipment model."
                }
            elif domain == "architecture":
                return {
                    "enabled": True,
                    "usage": ["Interactive 3D structural massing and architectural pavilion model with orbit camera controls"],
                    "reason": "Architecture requires spatial inspection. 3D WebGL model viewer displays volume and perspective."
                }
            else:
                return {
                    "enabled": True,
                    "usage": ["Interactive 3D neural network cluster / dynamic data geometry reactively tracking user interaction"],
                    "reason": "3D visualization provides tangible visual metaphor for advanced algorithmic intelligence."
                }

        # Otherwise evaluate according to domain-native principles
        if domain == "architecture":
            return {
                "enabled": True,
                "usage": ["Interactive 3D structural pavilion massing model viewer with intuitive mouse orbit controls"],
                "reason": "Architecture is fundamentally spatial. A lightweight 3D massing model provides immediate proof of spatial expertise."
            }
        elif domain == "saas_tech":
            return {
                "enabled": True,
                "usage": ["Interactive 3D data grid node sphere reacting smoothly to spatial mouse tracking"],
                "reason": "Demonstrates technical mastery and interactive fidelity for cloud infrastructure / software platform."
            }
        elif domain == "restaurant_cafe":
            return {
                "enabled": False,
                "usage": [],
                "reason": "3D is unnecessary for this project. Food patrons prioritize appetizing dish imagery, menu prices, and frictionless ordering speed over 3D rendering."
            }
        elif domain == "fitness_gym":
            return {
                "enabled": False,
                "usage": [],
                "reason": "3D is unnecessary for this project. High-conversion fitness clubs convert on bold kinetic typography, athlete photography, and class timetables rather than 3D geometry."
            }
        elif domain == "photography":
            return {
                "enabled": False,
                "usage": [],
                "reason": "3D is unnecessary for this project. High-fidelity photography demands clean editorial whitespace and instant uncompressed photo viewing; 3D canvas distracts from the photographer's imagery."
            }
        else:
            return {
                "enabled": False,
                "usage": [],
                "reason": "3D is unnecessary for this project. Clean visual hierarchy and rapid page load optimize user engagement."
            }


# ==============================================================================
# 2. REFERENCE IMAGE ANALYZER
# ==============================================================================

class ReferenceImageAnalyzer:
    """
    Extracts color palettes and aesthetic guidance if the user attached or referenced an image.
    """

    @staticmethod
    def extract_palette_from_image(image_path: str) -> Optional[List[str]]:
        if not image_path or not os.path.exists(image_path):
            return None
        try:
            from PIL import Image
            img = Image.open(image_path).convert("RGB")
            img = img.resize((50, 50))
            colors = img.getcolors(maxcolors=2500)
            if not colors:
                return None
            sorted_colors = sorted(colors, key=lambda c: c[0], reverse=True)
            hex_palette = []
            for count, (r, g, b) in sorted_colors[:5]:
                hex_palette.append(f"#{r:02x}{g:02x}{b:02x}")
            return hex_palette
        except Exception as e:
            logger.warning(f"Could not extract colors from reference image: {e}")
            return None


# ==============================================================================
# 3. DESIGN INTELLIGENCE ENGINE
# ==============================================================================

class DesignIntelligenceEngine:
    """
    Synthesizes requirements into a complete, domain-native Design Profile.
    """

    @staticmethod
    def create_design_profile(
        user_prompt: str,
        spec: Optional[Dict[str, Any]] = None,
        reference_image_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive domain-aware Design Profile.
        """
        combined_text = user_prompt
        if spec:
            combined_text += " " + spec.get("purpose", "") + " " + spec.get("project_type", "")

        domain = detect_domain_from_text(combined_text)
        domain_meta = DOMAIN_TAXONOMY[domain]

        # 1. 3D Decision
        three_d = ThreeDDecisionSystem.evaluate(domain, user_prompt, spec.get("project_type", "") if spec else "")

        # 2. Palette Variation Selection
        palettes = domain_meta["color_palettes"]
        # Seed variation by project name or user hint
        p_seed = hash(spec.get("project_name", user_prompt) if spec else user_prompt) % len(palettes)
        selected_palette = palettes[p_seed]

        # If user uploaded a reference image, incorporate extracted colors
        ref_colors = ReferenceImageAnalyzer.extract_palette_from_image(reference_image_path)
        if ref_colors and len(ref_colors) >= 3:
            selected_palette = {
                "name": "Custom Reference-Extracted Harmony",
                "bg": ref_colors[0],
                "surface": ref_colors[1],
                "surface_border": "rgba(255, 255, 255, 0.1)",
                "text_primary": "#FFFFFF" if ref_colors[0] < "#555555" else "#111111",
                "text_secondary": "#A0A0A0",
                "accent": ref_colors[2],
                "accent_secondary": ref_colors[3] if len(ref_colors) > 3 else ref_colors[2],
                "tag": "reference-guided"
            }

        # 3. Business Type & Target Audience Formulation
        business_type = spec.get("project_type") if spec and spec.get("project_type") else domain_meta["display_name"]
        target_audience = ", ".join(spec.get("target_users", [])) if spec and spec.get("target_users") else "Clients, customers, and domain stakeholders"

        # 4. Brand Personality Selection
        brand_personality = domain_meta["brand_personalities"][:4]

        # 5. Visual Direction Strategies
        typo = domain_meta["typography"]
        visual_direction = {
            "color_strategy": f"Palette: {selected_palette['name']}. Background {selected_palette['bg']}, Surface {selected_palette['surface']}, Primary Text {selected_palette['text_primary']}, Distinctive Accent {selected_palette['accent']}.",
            "typography_strategy": f"Headline Display: '{typo['display']}', Body Sans: '{typo['body']}'. {typo['style_note']}.",
            "layout_strategy": f"Domain-tailored grid for {domain}. Generous intentional whitespace, dynamic content rhythm, zero generic template repetition.",
            "imagery_strategy": f"High-fidelity domain photography with refined corner radiuses, subtle hover depth, and high contrast against {selected_palette['bg']}.",
            "spacing_strategy": "Responsive fluid padding (py-16 to py-28 for desktop sections, px-6 for comfortable mobile touch gutters)."
        }

        # 6. UX Strategy
        ux_strategy = {
            "primary_action": domain_meta["ux_patterns"]["primary_action"],
            "navigation_style": domain_meta["ux_patterns"]["navigation_style"],
            "content_hierarchy": [
                "1. Value proposition hero with domain-native visual magnet",
                "2. Core offering / catalog / portfolio discovery",
                "3. Trust validation / philosophy / practitioner credibility",
                "4. Transparent pricing / packages / menu tiers",
                "5. High-visibility conversion CTA & touchpoint"
            ]
        }

        # 7. Motion Strategy
        motion_strategy = {
            "level": "immersive" if three_d["enabled"] else "subtle to moderate",
            "animations": [
                "Smooth cubic-bezier card elevation transitions (0.3s ease)",
                "Subtle image zoom on hover without layout shift",
                "Interactive accordion state transitions with chevron rotation"
            ]
        }

        # 8. Content Strategy
        content_strategy = {
            "tone_of_voice": f"Authentic {domain} domain tone: {', '.join(brand_personality)}.",
            "copywriting_rules": [
                f"Write authentic copy strictly native to {business_type}.",
                "NEVER use generic placeholder buzzwords ('Experience next-gen solutions').",
                "Detail realistic domain menu items, packages, or services with authentic nomenclature."
            ],
            "forbidden_terms": domain_meta["forbidden_terms"]
        }

        # 9. Assembled Profile
        design_profile = {
            "domain": domain,
            "business_type": business_type,
            "target_audience": target_audience,
            "brand_personality": brand_personality,
            "visual_direction": visual_direction,
            "typography": typo,
            "palette": selected_palette,
            "ux_strategy": ux_strategy,
            "motion_strategy": motion_strategy,
            "three_d_strategy": three_d,
            "components": domain_meta["ux_patterns"]["components"],
            "pages": spec.get("pages", ["Home", "Offerings", "About", "Contact"]) if spec else ["Home", "Offerings", "About", "Contact"],
            "content_strategy": content_strategy
        }

        return design_profile


# ==============================================================================
# 4. GOOGLE STITCH DESIGN BRIEF GENERATOR
# ==============================================================================

class StitchDesignBriefGenerator:
    """
    Generates an exhaustive, production-grade Design Brief formatted specifically for Google Stitch.
    Stitch serves as the UI/UX exploration layer for generating bespoke interface concepts.
    """

    @staticmethod
    def generate_brief(design_profile: Dict[str, Any], project_name: str = "") -> str:
        d = design_profile
        pal = d["palette"]
        typo = d["typography"]
        three_d = d["three_d_strategy"]

        brief = f"""# GOOGLE STITCH DESIGN BRIEF: {project_name or d['business_type'].upper()}

## 1. PROJECT & DOMAIN CONTEXT
- **Domain:** {d['domain'].upper()}
- **Business Type:** {d['business_type']}
- **Target Audience:** {d['target_audience']}
- **Brand Personality:** {', '.join(d['brand_personality'])}

## 2. DESIGN GOAL
Create an authentic, breathtaking, domain-native web interface that feels custom-crafted by world-class designers specifically for a **{d['business_type']}**. It must avoid generic tech templates and reflect the genuine expectations of {d['target_audience']}.

## 3. VISUAL LANGUAGE & DESIGN TOKENS
- **Aesthetic Vibe:** {d['visual_direction']['layout_strategy']}
- **Color Strategy:**
  - Background (Dominant): `{pal['bg']}`
  - Surface / Panels: `{pal['surface']}` (Border: `{pal['surface_border']}`)
  - Primary Text: `{pal['text_primary']}`
  - Secondary Text: `{pal['text_secondary']}`
  - Signature Accent: `{pal['accent']}`
  - Secondary Accent: `{pal['accent_secondary']}`
- **Typography Pairing:**
  - Display / Headings: **{typo['display']}** (Google Fonts)
  - Body / Interface: **{typo['body']}**
  - Font Philosophy: {typo['style_note']}
- **Spacing & Rhythm:** {d['visual_direction']['spacing_strategy']}

## 4. UX & INTERACTION STRATEGY
- **Primary CTA:** {d['ux_strategy']['primary_action']}
- **Navigation Architecture:** {d['ux_strategy']['navigation_style']}
- **Section Order:**
{chr(10).join([f"  {line}" for line in d['ux_strategy']['content_hierarchy']])}

## 5. 3D & MOTION STRATEGY
- **3D Enabled:** {'YES' if three_d['enabled'] else 'NO (Intentionally Omitted)'}
- **3D Usage:** {', '.join(three_d['usage']) if three_d['usage'] else 'None'}
- **Strategic Justification:** {three_d['reason']}
- **Motion Level:** {d['motion_strategy']['level']}

## 6. DOMAIN COMPONENT LIBRARY
The interface must implement these domain design patterns:
{chr(10).join([f"  • {comp}" for comp in d['components']])}

## 7. CONTENT & COPYWRITING INSTRUCTIONS
- Write authentic, realistic, compelling copy for **{d['business_type']}**.
- Use natural terminology that customers of this business actually look for.

## 8. STRICT ANTI-PATTERNS & FORBIDDEN STYLING
- DO NOT apply uniform dark sci-fi / neon cyberpunk styling unless the domain is specifically futuristic tech.
- DO NOT create generic SaaS pricing cards or terminal simulators for non-tech businesses.
{f"- Strictly FORBIDDEN Words: {', '.join(d['content_strategy']['forbidden_terms'])}" if d['content_strategy']['forbidden_terms'] else ""}
"""
        return brief
