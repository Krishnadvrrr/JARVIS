"""
J.A.R.V.I.S. Design Quality Gate & Validation Engine
Evaluates generated frontend code across Domain Fit, UX Fit, Visual Coherence,
Content Authenticity, 3D Strategic Justification, Mobile Responsiveness, and Uniqueness.
"""

import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger("DesignValidator")
logger.setLevel(logging.INFO)

class DesignValidator:
    """
    Quality Gate validating that a generated website strictly respects its domain-native Design Profile.
    """

    @staticmethod
    def validate(html_code: str, design_profile: Dict[str, Any]) -> Dict[str, Any]:
        d = design_profile
        domain = d.get("domain", "saas_tech")
        forbidden_terms = d.get("content_strategy", {}).get("forbidden_terms", [])
        typo = d.get("typography", {})
        three_d = d.get("three_d_strategy", {})

        issues = []
        scores = {}

        html_lower = html_code.lower()

        # 1. FORBIDDEN TERMS CHECK (Critical Anti-Pattern Guard)
        found_forbidden = []
        for term in forbidden_terms:
            if term.lower() in html_lower:
                found_forbidden.append(term)
        if found_forbidden:
            issues.append(f"Forbidden sci-fi buzzwords detected in {domain} website: {found_forbidden}")
            scores["content_fit"] = 40
        else:
            scores["content_fit"] = 98

        # 2. TYPOGRAPHY CHECK
        disp_font = typo.get("display", "").lower()
        if disp_font and disp_font in html_lower:
            scores["typography_fit"] = 100
        else:
            scores["typography_fit"] = 75
            issues.append(f"Recommended display font '{typo.get('display')}' was not found in stylesheet link.")

        # 3. 3D FIT CHECK
        three_d_enabled = three_d.get("enabled", False)
        has_threejs = "three.min.js" in html_lower or "three.js" in html_lower
        if three_d_enabled and has_threejs:
            scores["three_d_fit"] = 100
        elif not three_d_enabled and not has_threejs:
            scores["three_d_fit"] = 100  # Correctly omitted!
        elif not three_d_enabled and has_threejs:
            scores["three_d_fit"] = 60
            issues.append(f"Three.js WebGL script was bundled when 3D was designated unnecessary for {domain}.")
        else:
            scores["three_d_fit"] = 75
            issues.append("3D was planned for this domain but Three.js library was omitted.")

        # 4. MOBILE RESPONSIVENESS CHECK
        has_meta_viewport = "viewport" in html_lower
        has_responsive_classes = any(cls in html_lower for cls in ["sm:", "md:", "lg:", "max-w-", "grid-cols-"])
        if has_meta_viewport and has_responsive_classes:
            scores["responsiveness"] = 100
        else:
            scores["responsiveness"] = 50
            issues.append("Viewport meta tag or Tailwind responsive breakpoints are missing.")

        # 5. DOMAIN COMPONENT FIT
        domain_keywords = {
            "photography": ["portfolio", "gallery", "photo", "book", "consultation", "lightbox"],
            "restaurant_cafe": ["menu", "order", "cart", "coffee", "dish", "bakery", "table", "hours"],
            "fitness_gym": ["program", "class", "trainer", "membership", "pass", "coach", "schedule"],
            "architecture": ["project", "spatial", "studio", "monograph", "residential", "firm", "materials"],
            "saas_tech": ["platform", "features", "demo", "pricing", "integration", "dashboard", "api"]
        }
        req_keywords = domain_keywords.get(domain, ["features", "contact"])
        matched_kw = [k for k in req_keywords if k in html_lower]
        keyword_score = int((len(matched_kw) / max(len(req_keywords), 1)) * 100)
        scores["domain_fit"] = max(keyword_score, 70)

        # 6. OVERALL QUALITY SCORE
        avg_score = sum(scores.values()) / max(len(scores), 1)
        passed = avg_score >= 80 and len(found_forbidden) == 0

        return {
            "passed": passed,
            "overall_score": round(avg_score, 1),
            "scores": scores,
            "issues": issues,
            "forbidden_terms_found": found_forbidden
        }

    @staticmethod
    def clean_and_sanitize_html(html_code: str, design_profile: Dict[str, Any]) -> str:
        """
        Removes any accidental forbidden terms from the HTML output if an LLM hallucinated them.
        """
        forbidden = design_profile.get("content_strategy", {}).get("forbidden_terms", [])
        if not forbidden:
            return html_code

        sanitized = html_code
        for term in forbidden:
            # Replace case-insensitively with neutral text
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            sanitized = pattern.sub("", sanitized)

        return sanitized
