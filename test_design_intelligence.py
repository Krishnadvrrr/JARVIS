"""
Comprehensive Test Suite for J.A.R.V.I.S. Domain-Aware Design Intelligence System
Tests A through E:
- Test A: Wedding Photography Studio (Elena Vance Photography)
- Test B: Artisan Cafe (Luna Cafe Online Ordering)
- Test C: High-Intensity Gym (Apex Fitness)
- Test D: Architectural Practice (Studio Forma)
- Test E: Cloud AI & Data SaaS Platform (HyperScale AI)
"""

import os
import sys
import json
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from domain_patterns import DOMAIN_TAXONOMY, detect_domain_from_text
from design_intelligence import DesignIntelligenceEngine, StitchDesignBriefGenerator, ThreeDDecisionSystem
from design_validator import DesignValidator
from domain_html_generator import (
    generate_domain_native_html,
    generate_photography_html,
    generate_cafe_html,
    generate_gym_html,
    generate_architecture_html,
    generate_saas_html
)
import tools

class TestDomainAwareDesignIntelligence(unittest.TestCase):

    def setUp(self):
        self.test_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_outputs")
        os.makedirs(self.test_output_dir, exist_ok=True)

    def test_domain_detection(self):
        """Verifies accurate categorization across distinct domains."""
        self.assertEqual(detect_domain_from_text("Build a website for my wedding photography business"), "photography")
        self.assertEqual(detect_domain_from_text("Create an online ordering website for Luna Cafe"), "restaurant_cafe")
        self.assertEqual(detect_domain_from_text("Build a website for Apex Fitness, a crossfit and boxing gym"), "fitness_gym")
        self.assertEqual(detect_domain_from_text("Create a website for Studio Forma, an architecture practice"), "architecture")
        self.assertEqual(detect_domain_from_text("Build a landing page for HyperScale AI, a distributed inference engine"), "saas_tech")
        print("\n[PASSED] Domain detection correctly identified all 5 domains.")

    def test_three_d_decision_system(self):
        """
        Verifies strategic 3D evaluation:
        - Photography, Cafe, Gym must disable 3D by default with clear domain justification.
        - Architecture and SaaS must enable 3D with spatial/technical justification.
        """
        # Photography
        dec_photo = ThreeDDecisionSystem.evaluate("photography", "wedding photography portfolio")
        self.assertFalse(dec_photo["enabled"])
        self.assertIn("distract", dec_photo["reason"].lower())

        # Cafe
        dec_cafe = ThreeDDecisionSystem.evaluate("restaurant_cafe", "cafe online ordering")
        self.assertFalse(dec_cafe["enabled"])
        self.assertTrue("food" in dec_cafe["reason"].lower() or "speed" in dec_cafe["reason"].lower() or "unnecessary" in dec_cafe["reason"].lower())

        # Gym
        dec_gym = ThreeDDecisionSystem.evaluate("fitness_gym", "gym membership")
        self.assertFalse(dec_gym["enabled"])
        self.assertTrue("kinetic" in dec_gym["reason"].lower() or "timetable" in dec_gym["reason"].lower() or "unnecessary" in dec_gym["reason"].lower())

        # Architecture
        dec_arch = ThreeDDecisionSystem.evaluate("architecture", "modern architecture practice")
        self.assertTrue(dec_arch["enabled"])
        self.assertIn("spatial", dec_arch["reason"].lower())

        # SaaS
        dec_saas = ThreeDDecisionSystem.evaluate("saas_tech", "cloud AI inference platform")
        self.assertTrue(dec_saas["enabled"])
        self.assertTrue("platform" in dec_saas["reason"].lower() or "technical" in dec_saas["reason"].lower() or "visual" in dec_saas["reason"].lower())

        print("\n[PASSED] 3D Decision System correctly enforced domain-specific 3D policies.")

    def test_domain_differentiation(self):
        """Verifies that generated design profiles and briefs have distinct palettes and typography."""
        profile_photo = DesignIntelligenceEngine.create_design_profile("Wedding photography studio portfolio")
        profile_cafe = DesignIntelligenceEngine.create_design_profile("Luna cafe coffee pastries online ordering")
        profile_gym = DesignIntelligenceEngine.create_design_profile("Apex Fitness high intensity crossfit boxing gym")
        profile_arch = DesignIntelligenceEngine.create_design_profile("Studio Forma architectural practice")
        profile_saas = DesignIntelligenceEngine.create_design_profile("HyperScale AI cloud infrastructure platform")

        # Color palette backgrounds & accents must not all be identical
        bg_set = {p["palette"]["bg"] for p in [profile_photo, profile_cafe, profile_gym, profile_arch, profile_saas]}
        accent_set = {p["palette"]["accent"] for p in [profile_photo, profile_cafe, profile_gym, profile_arch, profile_saas]}
        self.assertGreaterEqual(len(bg_set), 3, "Background palettes must vary across domains")
        self.assertGreaterEqual(len(accent_set), 4, "Accent colors must be distinct across domains")

        # Typography must differ
        fonts_display = {p["typography"]["display"] for p in [profile_photo, profile_cafe, profile_gym, profile_arch, profile_saas]}
        self.assertGreaterEqual(len(fonts_display), 4, "Display fonts must be domain-tailored")

        # Brand personalities must differ
        self.assertIn("editorial", [p.lower() for p in profile_photo["brand_personality"]])
        self.assertTrue(any(w in [p.lower() for p in profile_cafe["brand_personality"]] for w in ["welcoming", "warm", "artisanal"]))
        self.assertTrue(any(w in [p.lower() for p in profile_gym["brand_personality"]] for w in ["energetic", "motivating", "dynamic", "athletic"]))
        self.assertTrue(any(w in [p.lower() for p in profile_arch["brand_personality"]] for w in ["monumental", "structural", "spatial", "minimalist"]))
        self.assertTrue(any(w in [p.lower() for p in profile_saas["brand_personality"]] for w in ["innovative", "scalable", "intelligent", "futuristic"]))

        print("\n[PASSED] Palettes, typography, and brand personalities are completely differentiated.")

    def test_scenario_a_wedding_photography(self):
        """
        TEST A: Wedding Photography Studio
        - Playfair / Cormorant serif typography
        - Champagne / charcoal palette
        - Responsive photo gallery + lightbox modal + inquiry CTA
        - Zero Three.js or sci-fi terms
        """
        profile = DesignIntelligenceEngine.create_design_profile("Build a website for my wedding photography business")
        brief = StitchDesignBriefGenerator.generate_brief(profile, "Elena_Vance_Photography")
        html = generate_photography_html("Elena_Vance_Photography", profile)

        # Validation
        val = DesignValidator.validate(html, profile)
        self.assertTrue(val["passed"], f"Photography validation failed: {val['issues']}")
        self.assertGreaterEqual(val["overall_score"], 85)

        # Content assertions
        html_lower = html.lower()
        self.assertIn("gallery", html_lower)
        self.assertIn("portfolio", html_lower)
        self.assertIn("lightbox", html_lower)
        self.assertIn("inquiry", html_lower)
        self.assertNotIn("three.min.js", html_lower, "Photography site must NOT include Three.js")
        self.assertNotIn("quantum", html_lower)
        self.assertNotIn("terminal", html_lower)
        self.assertNotIn("neural core", html_lower)
        self.assertTrue("playfair display" in html_lower or "cormorant" in html_lower, "Photography site must use editorial serif font")
        print("\n[PASSED] TEST A: Wedding Photography website generated with bespoke editorial aesthetics.")

    def test_scenario_b_artisan_cafe(self):
        """
        TEST B: Luna Cafe Online Ordering
        - Warm roasted caramel & terracotta palette
        - Menu-first UX with category selector, interactive cart, checkout
        - Zero Three.js or sci-fi terms
        """
        profile = DesignIntelligenceEngine.create_design_profile("Create an online ordering website for Luna Cafe")
        brief = StitchDesignBriefGenerator.generate_brief(profile, "Luna_Cafe")
        html = generate_cafe_html("Luna_Cafe", profile)

        # Validation
        val = DesignValidator.validate(html, profile)
        self.assertTrue(val["passed"], f"Cafe validation failed: {val['issues']}")
        self.assertGreaterEqual(val["overall_score"], 85)

        # Content assertions
        html_lower = html.lower()
        self.assertIn("menu", html_lower)
        self.assertIn("cart", html_lower)
        self.assertIn("order", html_lower)
        self.assertIn("espresso", html_lower)
        self.assertNotIn("three.min.js", html_lower, "Cafe site must NOT include Three.js")
        self.assertNotIn("quantum", html_lower)
        self.assertNotIn("terminal", html_lower)
        self.assertNotIn("tactical", html_lower)
        self.assertIn("fraunces", html_lower)
        print("\n[PASSED] TEST B: Artisan Cafe website generated with menu-first UX and cart functionality.")

    def test_scenario_c_fitness_gym(self):
        """
        TEST C: Apex Fitness Gym
        - Matte carbon & volt yellow / electric orange palette
        - Bold athletic typography (Oswald & Montserrat)
        - Class schedule, coaching staff, membership passes
        - Zero Three.js or sci-fi terms
        """
        profile = DesignIntelligenceEngine.create_design_profile("Build a website for Apex Fitness, a crossfit and boxing gym")
        brief = StitchDesignBriefGenerator.generate_brief(profile, "Apex_Fitness")
        html = generate_gym_html("Apex_Fitness", profile)

        # Validation
        val = DesignValidator.validate(html, profile)
        self.assertTrue(val["passed"], f"Gym validation failed: {val['issues']}")
        self.assertGreaterEqual(val["overall_score"], 85)

        # Content assertions
        html_lower = html.lower()
        self.assertIn("schedule", html_lower)
        self.assertIn("membership", html_lower)
        self.assertIn("training", html_lower)
        self.assertIn("coach", html_lower)
        self.assertNotIn("three.min.js", html_lower, "Gym site must NOT include Three.js")
        self.assertNotIn("quantum", html_lower)
        self.assertNotIn("tactical core", html_lower)
        self.assertIn("oswald", html_lower)
        print("\n[PASSED] TEST C: High-Intensity Gym website generated with athletic kinetic aesthetic.")

    def test_scenario_d_architecture_studio(self):
        """
        TEST D: Studio Forma Architecture
        - Architectural brutalist / structural palette (monochrome & brass)
        - Syne & Archivo typography
        - Monograph case studies
        - Strategic 3D WebGL pavilion massing model enabled with orbit controls
        """
        profile = DesignIntelligenceEngine.create_design_profile("Create a website for Studio Forma, an architecture practice")
        brief = StitchDesignBriefGenerator.generate_brief(profile, "Studio_Forma")
        html = generate_architecture_html("Studio_Forma", profile)

        # Validation
        val = DesignValidator.validate(html, profile)
        self.assertTrue(val["passed"], f"Architecture validation failed: {val['issues']}")
        self.assertGreaterEqual(val["overall_score"], 85)

        # Content assertions
        html_lower = html.lower()
        self.assertIn("spatial", html_lower)
        self.assertIn("monograph", html_lower)
        self.assertIn("projects", html_lower)
        self.assertIn("three.min.js", html_lower, "Architecture site MUST include 3D WebGL massing model")
        self.assertTrue("orbit" in html_lower or "drag" in html_lower, "Must have 3D orbit or drag interaction")
        self.assertIn("syne", html_lower)
        self.assertNotIn("quantum mesh", html_lower)
        self.assertNotIn("cyberpunk", html_lower)
        print("\n[PASSED] TEST D: Architecture Firm website generated with 3D structural massing pavilion.")

    def test_scenario_e_saas_platform(self):
        """
        TEST E: HyperScale AI Platform
        - Deep indigo & electric violet palette
        - Space Grotesk & JetBrains Mono typography
        - Interactive 3D neural mesh visualizer + throughput/latency simulation sandbox + pricing
        """
        profile = DesignIntelligenceEngine.create_design_profile("Build a landing page for HyperScale AI, a distributed inference engine")
        brief = StitchDesignBriefGenerator.generate_brief(profile, "HyperScale_AI")
        html = generate_saas_html("HyperScale_AI", profile)

        # Validation
        val = DesignValidator.validate(html, profile)
        self.assertTrue(val["passed"], f"SaaS validation failed: {val['issues']}")
        self.assertGreaterEqual(val["overall_score"], 85)

        # Content assertions
        html_lower = html.lower()
        self.assertTrue("throughput" in html_lower or "workload" in html_lower or "cloud" in html_lower)
        self.assertIn("throughput", html_lower)
        self.assertIn("three.min.js", html_lower, "SaaS site MUST include 3D WebGL cluster")
        self.assertIn("space grotesk", html_lower)
        self.assertIn("jetbrains mono", html_lower)
        print("\n[PASSED] TEST E: Cloud AI SaaS website generated with interactive neural 3D and metrics sandbox.")

    def test_builder_integration_all_artifacts(self):
        """
        Tests tools.build_website() end-to-end integration:
        Ensures index.html, stitch_brief.md, and design_profile.json are saved and returned.
        """
        test_prompt = "Online bakery and cafe shop"
        res = tools.build_website(prompt_or_topic=test_prompt, site_name="Test_Cafe_Studio")

        self.assertEqual(res["status"], "success")
        self.assertEqual(res["domain"], "restaurant_cafe")
        self.assertFalse(res["three_d_enabled"], "Bakery/cafe must NOT enable 3D by default")
        self.assertTrue(os.path.exists(res["index_path"]))
        self.assertTrue(os.path.exists(res["stitch_brief_path"]))
        self.assertTrue(os.path.exists(res["design_profile_path"]))

        # Verify brief content
        with open(res["stitch_brief_path"], "r", encoding="utf-8") as f:
            brief_text = f.read()
        self.assertIn("GOOGLE STITCH DESIGN BRIEF", brief_text)
        self.assertIn("RESTAURANT_CAFE", brief_text)

        # Verify profile JSON content
        with open(res["design_profile_path"], "r", encoding="utf-8") as f:
            profile_data = json.load(f)
        self.assertEqual(profile_data["domain"], "restaurant_cafe")
        print("\n[PASSED] End-to-end builder generated all domain artifacts with complete integrity.")


if __name__ == "__main__":
    unittest.main()
