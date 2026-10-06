"""
Automated Verification Suite for Nebius AI Studio & NVIDIA Nemotron-70B Integration
Verifies:
1. HUD status branding reflects Nebius primary + Groq backup when NEBIUS_API_KEY is configured.
2. Dynamic failover mechanism: When NEBIUS_API_KEY is empty or offline, seamlessly routes through Groq.
3. OpenAI-compatible request structure and header conformance for Nebius AI Studio endpoints.
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from app import app, call_groq


class TestNebiusIntegration(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_hud_status_with_groq_only(self):
        """When NEBIUS_API_KEY is unset, HUD displays Groq as active primary engine."""
        with patch.dict(os.environ, {"NEBIUS_API_KEY": "", "GROQ_API_KEY": "dummy_groq_key"}):
            resp = self.client.get('/api/status')
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertIn("GROQ", data["model"])
            self.assertEqual(data["status"], "ONLINE")

    def test_hud_status_with_nebius_active(self):
        """When NEBIUS_API_KEY is present, HUD prominently showcases Nebius AI Studio & Nemotron-70B."""
        with patch.dict(os.environ, {
            "NEBIUS_API_KEY": "nbe-test-key-mock",
            "NEBIUS_MODEL": "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
            "GROQ_API_KEY": "dummy_groq_key"
        }):
            resp = self.client.get('/api/status')
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertIn("NEBIUS AI STUDIO", data["model"])
            self.assertIn("Nemotron-70B", data["model"])
            self.assertIn("GROQ", data["model"])

    @patch("requests.post")
    def test_nebius_primary_inference(self, mock_post):
        """Verifies that requests route to Nebius Studio endpoint when NEBIUS_API_KEY is active."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Greetings Krishna Sir, NVIDIA Nemotron-70B online and operational."}}]
        }
        mock_post.return_value = mock_response

        with patch.dict(os.environ, {
            "NEBIUS_API_KEY": "nbe-mock-key-123",
            "NEBIUS_BASE_URL": "https://api.studio.nebius.ai/v1",
            "NEBIUS_MODEL": "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF",
            "GROQ_API_KEY": "dummy_groq_key"
        }):
            reply = call_groq("How are your systems running today?", session_id="test_nebius_session")
            self.assertIn("Nemotron-70B online", reply)

            # Check that requests.post was called targeting Nebius
            called_args, called_kwargs = mock_post.call_args
            self.assertEqual(called_args[0], "https://api.studio.nebius.ai/v1/chat/completions")
            self.assertEqual(called_kwargs["headers"]["Authorization"], "Bearer nbe-mock-key-123")
            self.assertEqual(called_kwargs["json"]["model"], "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")

    @patch("requests.post")
    def test_nebius_failover_to_groq(self, mock_post):
        """Verifies that if Nebius experiences an error (e.g. 500 or timeout), JARVIS automatically fails over to Groq."""
        # First call (Nebius) returns error, second call (Groq) returns success
        neb_fail_resp = MagicMock()
        neb_fail_resp.status_code = 503
        neb_fail_resp.text = "Service temporarily unavailable"

        groq_success_resp = MagicMock()
        groq_success_resp.status_code = 200
        groq_success_resp.json.return_value = {
            "choices": [{"message": {"content": "Failover to Groq successful, Sir."}}]
        }

        mock_post.side_effect = [neb_fail_resp, groq_success_resp]

        with patch.dict(os.environ, {
            "NEBIUS_API_KEY": "nbe-mock-key-123",
            "NEBIUS_BASE_URL": "https://api.studio.nebius.ai/v1",
            "GROQ_API_KEY": "dummy_groq_key"
        }):
            reply = call_groq("Testing failover resilience", session_id="test_failover_session")
            self.assertIn("Failover to Groq successful", reply)
            self.assertEqual(mock_post.call_count, 2)


if __name__ == "__main__":
    unittest.main()
