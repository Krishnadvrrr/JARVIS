"""
Comprehensive Test Suite for J.A.R.V.I.S. Autonomous Dev Squad
Validates:
1. Skills Manager & On-Demand Context Loading
2. AgentShield Security Auditor (Vulnerability & Secret Detection)
3. Tester Agent (Automated Verification & Self-Healing Loop)
4. End-to-End Dev Squad Multi-Agent Pipeline
"""

import os
import sys
import json
import shutil
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills_manager import SkillsManager
from security_auditor import SecurityAuditor
from tester_agent import TesterAgent
from dev_squad import AutonomousDevSquad


class TestDevSquad(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_outputs", "dev_squad_test")
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            try:
                shutil.rmtree(self.test_dir)
            except Exception:
                pass

    def test_skills_manager(self):
        """Verifies skill discovery, keyword scoring, and prompt injection formatting."""
        skills = SkillsManager.load_skills(force_reload=True)
        self.assertGreaterEqual(len(skills), 4, "Should load at least 4 modular skills")

        # Test query matching for database
        db_skills = SkillsManager.find_relevant_skills("Build a SQLite database with tables")
        self.assertTrue(any("sqlite" in s.title.lower() or "database" in s.title.lower() for s in db_skills))

        # Test query matching for security
        sec_skills = SkillsManager.find_relevant_skills("Check password security and audit vulnerabilities")
        self.assertTrue(any("security" in s.title.lower() for s in sec_skills))

        # Test context generation
        context = SkillsManager.get_skills_prompt_context("FastAPI REST endpoints")
        self.assertIn("ACTIVE J.A.R.V.I.S. MODULAR SKILL PROTOCOLS", context)
        print("\n[PASSED] Skills Manager discovered skills and matched relevant manuals.")

    def test_security_auditor_detection(self):
        """Verifies AgentShield catches hardcoded secrets, SQL injection, and dangerous eval."""
        vulnerable_code = {
            "app.py": """
import os
API_KEY = "gsk_1234567890abcdef1234567890abcdef"

def get_user(user_id):
    import sqlite3
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Blatant SQL Injection
    cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")
    return cursor.fetchone()

def run_calc(expr):
    return eval(expr)
"""
        }

        report = SecurityAuditor.audit_project(vulnerable_code)
        self.assertFalse(report["passed"], "Insecure code must fail the security gate")
        self.assertLess(report["security_score"], 70, "Score must drop due to critical vulnerabilities")

        findings_types = [f["type"] for f in report["findings"]]
        self.assertIn("hardcoded_secret", findings_types)
        self.assertIn("sql_injection", findings_types)
        self.assertIn("unsafe_execution", findings_types)
        print(f"\n[PASSED] AgentShield caught {len(report['findings'])} vulnerabilities (Score: {report['security_score']}/100).")

    def test_security_auditor_clean_code(self):
        """Verifies AgentShield passes clean, hardened code."""
        clean_code = {
            "safe_app.py": """
import os
import sqlite3

def get_user_secure(user_id: int):
    api_key = os.getenv("API_KEY", "")
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    # Parameterized query
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()
"""
        }
        report = SecurityAuditor.audit_project(clean_code)
        self.assertTrue(report["passed"])
        self.assertEqual(report["security_score"], 100)
        print("\n[PASSED] AgentShield passed 100/100 for clean parameterized code.")

    def test_tester_agent_syntax_validation(self):
        """Verifies syntax validation flags malformed Python immediately."""
        bad_code = "def broken_func(\n    print('missing closing parenthesis'"
        ok, err = TesterAgent.validate_python_syntax(bad_code)
        self.assertFalse(ok)
        self.assertIn("SyntaxError", err)

        good_code = "def valid_func():\n    return 42\n"
        ok, err = TesterAgent.validate_python_syntax(good_code)
        self.assertTrue(ok)
        self.assertIsNone(err)
        print("\n[PASSED] Tester Agent successfully validated syntax via AST.")

    def test_dev_squad_end_to_end(self):
        """
        Tests the full 4-Agent Autonomous Dev Squad lifecycle:
        Plan -> Build -> Test -> Security Audit -> Artifact Packaging.
        """
        project_name = "Student_Exam_Portal"
        desc = "Full-stack student examination and grading management system with SQLite"

        res = AutonomousDevSquad.develop_project(
            project_name=project_name,
            description=desc,
            project_type="full_stack"
        )

        self.assertEqual(res["status"], "success")
        self.assertTrue(res["test_status"]["passed"], "Automated unit tests must pass")
        self.assertGreaterEqual(res["security_score"], 80, "AgentShield security score must be >= 80")
        self.assertTrue(os.path.exists(res["desktop_path"]))

        # Verify artifacts
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "database.py")))
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "test_suite.py")))
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "security_audit.json")))
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "test_results.json")))
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "run.bat")))
        self.assertTrue(os.path.exists(os.path.join(res["desktop_path"], "README.md")))

        # Check audit file content
        with open(os.path.join(res["desktop_path"], "security_audit.json"), "r") as f:
            audit_data = json.load(f)
        self.assertIn("security_score", audit_data)
        self.assertIn("findings", audit_data)

        print(f"\n[PASSED] Autonomous Dev Squad built '{project_name}' (Security Score: {res['security_score']}/100, Tests: Passed).")


if __name__ == "__main__":
    unittest.main()
