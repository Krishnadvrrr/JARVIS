"""
J.A.R.V.I.S. Tester Agent & Self-Healing Verification Engine
Inspired by the ECC TDD test runner and self-healing loop.
Validates code syntax, runs unit tests in background subprocesses, and autonomously
repairs bugs and tracebacks before presenting the project to the user.
"""

import os
import ast
import sys
import json
import time
import subprocess
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("TesterAgent")
logger.setLevel(logging.INFO)


class TesterAgent:
    """Automated test execution, syntax validation, and self-healing engine."""

    @staticmethod
    def validate_python_syntax(code: str, filename: str = "code.py") -> Tuple[bool, Optional[str]]:
        """Parses Python code using AST to detect syntax errors before execution."""
        try:
            ast.parse(code, filename=filename)
            return True, None
        except SyntaxError as e:
            err = f"SyntaxError in {filename} at line {e.lineno}: {e.msg}\n  {e.text or ''}"
            return False, err
        except Exception as e:
            return False, str(e)

    @staticmethod
    def run_tests_in_directory(project_dir: str, test_pattern: str = "test_*.py", timeout_sec: int = 20) -> Dict[str, Any]:
        """
        Executes Python unit tests inside the project folder using the standard unittest test runner.
        Returns execution results, pass/fail status, and raw output.
        """
        if not os.path.exists(project_dir):
            return {
                "passed": False,
                "returncode": 1,
                "stdout": "",
                "stderr": f"Directory not found: {project_dir}",
                "execution_time_sec": 0
            }

        start_time = time.time()
        try:
            # Run unittest discovery in the project directory
            res = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", project_dir, "-p", test_pattern],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=timeout_sec
            )
            elapsed = round(time.time() - start_time, 2)
            passed = res.returncode == 0

            return {
                "passed": passed,
                "returncode": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "execution_time_sec": elapsed
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Test execution timed out after {timeout_sec} seconds (possible infinite loop).",
                "execution_time_sec": timeout_sec
            }
        except Exception as e:
            return {
                "passed": False,
                "returncode": 1,
                "stdout": "",
                "stderr": f"Test execution error: {str(e)}",
                "execution_time_sec": round(time.time() - start_time, 2)
            }

    @staticmethod
    def call_repair_llm(broken_code: str, error_traceback: str, filename: str = "main.py") -> str:
        """Invokes Groq LLM to autonomously diagnose and fix broken code."""
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            return broken_code

        try:
            import requests
            import re

            system_prompt = (
                "You are an elite Autonomous Software Debugger and Repair Agent.\n"
                "Your task is to fix broken source code that caused a test failure or syntax error.\n"
                "Rules:\n"
                "1. Analyze the exact traceback/error message.\n"
                "2. Fix the bug while preserving the intended architecture, class names, and functions.\n"
                "3. Return ONLY the complete, corrected source code.\n"
                "4. Do NOT wrap in markdown explanation, no preamble, no backticks."
            )

            user_prompt = (
                f"File: {filename}\n\n"
                f"ERROR TRACEBACK:\n{error_traceback}\n\n"
                f"BROKEN CODE:\n{broken_code}\n\n"
                f"Provide the fixed, working code now:"
            )

            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3.8-27b",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 4096
                },
                timeout=25
            )

            if resp.status_code == 200:
                text = resp.json()["choices"][0]["message"]["content"].strip()
                # Clean possible markdown wrapping
                cleaned = re.sub(r"^```python\s*", "", text, flags=re.IGNORECASE)
                cleaned = re.sub(r"^```\s*", "", cleaned)
                cleaned = re.sub(r"```$", "", cleaned).strip()
                if cleaned and len(cleaned) > 20:
                    return cleaned
        except Exception as e:
            logger.warning(f"Repair LLM call failed: {e}")

        return broken_code

    @classmethod
    def self_healing_test_loop(
        cls,
        project_dir: str,
        files_dict: Dict[str, str],
        max_attempts: int = 3
    ) -> Dict[str, Any]:
        """
        Orchestrates the self-healing cycle:
        1. Validate syntax of all files
        2. Run test suite
        3. If failure, send traceback to repair agent
        4. Re-apply fix and retry until passing or max attempts reached
        """
        current_files = dict(files_dict)
        attempts_log: List[Dict[str, Any]] = []

        for attempt in range(1, max_attempts + 1):
            logger.info(f"Self-healing verification attempt {attempt}/{max_attempts}...")

            # 1. Syntax check on all Python files
            syntax_errors = []
            broken_file = None
            syntax_traceback = ""

            for fname, code in current_files.items():
                if fname.endswith(".py"):
                    ok, err = cls.validate_python_syntax(code, filename=fname)
                    if not ok:
                        syntax_errors.append(err)
                        broken_file = fname
                        syntax_traceback = err
                        break

            # If syntax error found, repair immediately
            if syntax_errors:
                logger.warning(f"Attempt {attempt}: Syntax error detected in {broken_file}. Triggering repair agent.")
                attempts_log.append({
                    "attempt": attempt,
                    "stage": "syntax_check",
                    "passed": False,
                    "error": syntax_traceback,
                    "target_file": broken_file
                })

                if attempt < max_attempts:
                    healed_code = cls.call_repair_llm(current_files[broken_file], syntax_traceback, broken_file)
                    current_files[broken_file] = healed_code
                    # Write updated code to disk
                    fpath = os.path.join(project_dir, broken_file)
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(healed_code)
                    continue
                else:
                    break

            # 2. Syntax passed; write files to project dir if not already there
            for fname, code in current_files.items():
                fpath = os.path.join(project_dir, fname)
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(code)

            # 3. Run unit tests
            test_res = cls.run_tests_in_directory(project_dir)
            if test_res["passed"]:
                logger.info(f"Attempt {attempt}: All unit tests PASSED cleanly!")
                attempts_log.append({
                    "attempt": attempt,
                    "stage": "test_execution",
                    "passed": True,
                    "output": test_res["stderr"] or test_res["stdout"]
                })
                return {
                    "passed": True,
                    "total_attempts": attempt,
                    "self_healed": attempt > 1,
                    "attempts_log": attempts_log,
                    "final_files": current_files,
                    "test_output": test_res["stderr"] or test_res["stdout"]
                }
            else:
                # Tests failed; capture traceback
                tb = test_res["stderr"] or test_res["stdout"]
                logger.warning(f"Attempt {attempt}: Unit tests failed with traceback:\n{tb}")
                attempts_log.append({
                    "attempt": attempt,
                    "stage": "test_execution",
                    "passed": False,
                    "error": tb
                })

                if attempt < max_attempts:
                    # Identify likely culprit file (look for filenames in traceback)
                    target_fname = None
                    for fname in current_files.keys():
                        if fname.endswith(".py") and not fname.startswith("test_") and fname in tb:
                            target_fname = fname
                            break
                    if not target_fname:
                        # Default to primary python file
                        py_files = [f for f in current_files.keys() if f.endswith(".py") and not f.startswith("test_")]
                        target_fname = py_files[0] if py_files else list(current_files.keys())[0]

                    logger.info(f"Reparing {target_fname} with repair agent...")
                    healed_code = cls.call_repair_llm(current_files[target_fname], tb, target_fname)
                    current_files[target_fname] = healed_code
                    # Write to disk
                    with open(os.path.join(project_dir, target_fname), "w", encoding="utf-8") as f:
                        f.write(healed_code)
                else:
                    break

        return {
            "passed": False,
            "total_attempts": max_attempts,
            "self_healed": False,
            "attempts_log": attempts_log,
            "final_files": current_files,
            "test_output": attempts_log[-1].get("error", "Failed after max attempts") if attempts_log else "Failed"
        }
