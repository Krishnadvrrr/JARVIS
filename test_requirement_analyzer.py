"""
Test Suite for J.A.R.V.I.S. Requirement Analyzer (Stage 1)
Validates Natural-Language Requirement Understanding, Smart Clarification,
Specification Schema Generation, Change Handling, Cancellation, and Builder Handoff.
"""

import os
import sys
import json
import unittest

# Ensure current folder is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requirement_analyzer

class TestRequirementAnalyzer(unittest.TestCase):

    def setUp(self):
        # Use an isolated test session ID
        self.session_id = "unit_test_session"
        requirement_analyzer.reset_session(self.session_id)

    def tearDown(self):
        requirement_analyzer.reset_session(self.session_id)

    def test_scenario_1_vague_request_asks_concise_clarification(self):
        """
        TEST 1:
        Request: "Create a portfolio website for a photographer."
        Expected: JARVIS identifies missing important requirements and asks concise questions.
        """
        prompt = "Create a portfolio website for a photographer."
        res = requirement_analyzer.process_user_message(prompt, session_id=self.session_id)

        self.assertTrue(res["handled"], "Request should be recognized as website intent")
        self.assertEqual(res["status"], "clarifying", "Should transition to CLARIFYING state")
        self.assertIn("clarify", res["response"].lower(), "Response should ask for clarification")
        self.assertTrue("options" in res["response"].lower() or "•" in res["response"], "Response should provide concrete options")

        # Verify session state
        session = requirement_analyzer.get_session(self.session_id)
        self.assertEqual(session.state, "CLARIFYING")
        self.assertGreaterEqual(len(session.clarification_questions), 1)
        self.assertLessEqual(len(session.clarification_questions), 2, "Must not ask 15 questions; keep concise")
        print("\n[PASSED] TEST 1: Vague request triggered smart clarification.")

    def test_scenario_2_detailed_request_skips_unnecessary_questions(self):
        """
        TEST 2:
        Request: "Create a photography portfolio with Home, About, Gallery and Contact pages. Use a dark modern design and include a contact form."
        Expected: JARVIS can generate a project specification without unnecessary questions.
        """
        prompt = "Create a photography portfolio with Home, About, Gallery and Contact pages. Use a dark modern design and include a contact form."
        res = requirement_analyzer.process_user_message(prompt, session_id=self.session_id)

        self.assertTrue(res["handled"], "Request should be recognized as website intent")
        self.assertEqual(res["status"], "confirming", "Should transition directly to CONFIRMING state without asking questions")
        self.assertIn("PROJECT UNDERSTANDING", res["response"], "Must present PROJECT UNDERSTANDING summary")
        self.assertIn("Does this look correct", res["response"], "Must prompt for confirmation")

        # Verify structured specification content
        session = requirement_analyzer.get_session(self.session_id)
        self.assertEqual(session.state, "CONFIRMING")
        spec = session.specification

        self.assertIn("Photography", spec["project_name"])
        self.assertTrue(any("Home" in p for p in spec["pages"]))
        self.assertTrue(any("Gallery" in p for p in spec["pages"]))
        self.assertTrue(any("Contact" in p for p in spec["pages"]))
        self.assertTrue(any("About" in p for p in spec["pages"]))
        self.assertIn("dark", spec["design"]["style"].lower())
        print("\n[PASSED] TEST 2: Detailed request generated complete spec directly without questions.")

    def test_scenario_3_cafe_ordering_asks_only_genuinely_missing_details(self):
        """
        TEST 3:
        Request: "Build an online cafe ordering website where customers can browse the menu, add items to a cart and place orders."
        Expected: JARVIS identifies the major requirements and asks only for genuinely important missing details.
        """
        prompt = "Build an online cafe ordering website where customers can browse the menu, add items to a cart and place orders."
        res = requirement_analyzer.process_user_message(prompt, session_id=self.session_id)

        self.assertTrue(res["handled"])
        self.assertEqual(res["status"], "clarifying")
        
        # Verify it does NOT re-ask if users can browse menu or add to cart
        resp_lower = res["response"].lower()
        self.assertNotIn("can customers browse menu", resp_lower)
        self.assertNotIn("can customers add to cart", resp_lower)
        
        # Verify it asks only genuinely important missing details (fulfillment / payment)
        self.assertTrue(
            "fulfillment" in resp_lower or "pickup" in resp_lower or "delivery" in resp_lower or "checkout" in resp_lower,
            "Must ask genuinely important missing details like fulfillment or delivery"
        )
        print("\n[PASSED] TEST 3: Identified major requirements and asked only genuinely missing details.")

    def test_scenario_4_user_changes_updates_spec_incrementally(self):
        """
        TEST 4:
        Flow: Establish specification -> User says: "Actually add user login."
        Expected: The project specification is updated rather than recreated unnecessarily.
        """
        # Step 1: Establish base spec
        prompt = "Create a photography portfolio with Home, About, Gallery and Contact pages. Use a dark modern design and include a contact form."
        res1 = requirement_analyzer.process_user_message(prompt, session_id=self.session_id)
        self.assertEqual(res1["status"], "confirming")

        original_spec = json.loads(json.dumps(requirement_analyzer.get_session(self.session_id).specification))
        self.assertFalse(original_spec["authentication"]["required"])

        # Step 2: User requests change
        change_prompt = "Actually add user login."
        res2 = requirement_analyzer.process_user_message(change_prompt, session_id=self.session_id)

        self.assertTrue(res2["handled"])
        self.assertEqual(res2["status"], "confirming")
        self.assertIn("updated", res2["response"].lower())
        self.assertIn("login", res2["response"].lower())

        # Verify updated spec in session
        updated_spec = requirement_analyzer.get_session(self.session_id).specification
        self.assertTrue(updated_spec["authentication"]["required"], "Authentication must be enabled")
        self.assertTrue(any("Login" in p or "Account" in p for p in updated_spec["pages"]), "Login page must be added")
        self.assertTrue(any("auth" in f.lower() or "login" in f.lower() for f in updated_spec["features"]), "Login feature must be added")

        # Verify original attributes preserved (not recreated from scratch)
        self.assertEqual(updated_spec["project_name"], original_spec["project_name"])
        self.assertEqual(updated_spec["design"]["style"], original_spec["design"]["style"])
        print("\n[PASSED] TEST 4: Specification updated incrementally with user login.")

    def test_scenario_5_cancellation_safely_stops_operation(self):
        """
        TEST 5:
        Flow: In active requirement workflow -> User says: "Cancel."
        Expected: The current operation stops safely and resets state to IDLE.
        """
        # Step 1: Start a request
        requirement_analyzer.process_user_message("Create a portfolio website for a photographer.", session_id=self.session_id)
        session = requirement_analyzer.get_session(self.session_id)
        self.assertEqual(session.state, "CLARIFYING")

        # Step 2: Cancel
        res = requirement_analyzer.process_user_message("Cancel.", session_id=self.session_id)
        self.assertTrue(res["handled"])
        self.assertEqual(res["status"], "cancelled")
        self.assertIn("cancelled", res["response"].lower())

        # Verify session is reset to IDLE
        session_after = requirement_analyzer.get_session(self.session_id)
        self.assertEqual(session_after.state, "IDLE")
        print("\n[PASSED] TEST 5: Cancellation safely aborted project.")

    def test_scenario_6_full_pipeline_to_confirmation(self):
        """
        TEST 6:
        Multi-turn flow:
        User: "Create an online ordering website for my cafe."
        -> JARVIS asks clarification
        User: "In-store pickup with pay-at-counter or UPI"
        -> JARVIS presents PROJECT UNDERSTANDING and asks confirmation
        User: "Yes, build it!"
        -> JARVIS hands off to builder
        """
        # Turn 1: Initial vague request
        res1 = requirement_analyzer.process_user_message("Build an online cafe ordering website.", session_id=self.session_id)
        self.assertEqual(res1["status"], "clarifying")

        # Turn 2: User provides clarification
        res2 = requirement_analyzer.process_user_message("In-store pickup with pay-at-counter or UPI", session_id=self.session_id)
        self.assertEqual(res2["status"], "confirming")
        self.assertIn("PROJECT UNDERSTANDING", res2["response"])
        self.assertIn("Does this look correct", res2["response"])

        spec = requirement_analyzer.get_session(self.session_id).specification
        self.assertEqual(spec["project_name"], "Artisan_Cafe_Ordering")
        self.assertTrue(any("Pickup" in f for f in spec["features"]))

        # Turn 3: User confirms -> trigger build
        res3 = requirement_analyzer.process_user_message("Yes, build it!", session_id=self.session_id)
        self.assertEqual(res3["status"], "building")
        self.assertIn("built", res3["response"].lower())
        print("\n[PASSED] TEST 6: Complete multi-turn pipeline successfully handed off to builder.")

    def test_scenario_7_unrelated_messages_pass_through(self):
        """
        TEST 7:
        Verify that unrelated non-website directives (Zepto, YouTube, system status, Outlook)
        are NOT intercepted and return handled=False.
        """
        non_website_queries = [
            "What is my battery level and CPU usage?",
            "Order 2 packets of milk on Zepto",
            "Play Iron Man theme song on YouTube",
            "Take a screenshot",
            "Draft an email to Professor"
        ]

        for q in non_website_queries:
            res = requirement_analyzer.process_user_message(q, session_id=self.session_id)
            self.assertFalse(res["handled"], f"Query '{q}' should not be intercepted as a website request")

        print("\n[PASSED] TEST 7: Non-website directives cleanly pass through to existing JARVIS tools.")


if __name__ == "__main__":
    unittest.main()
