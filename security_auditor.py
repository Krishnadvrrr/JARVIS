"""
J.A.R.V.I.S. Security Auditor & Red-Team Sub-Agent (AgentShield)
Inspired by the ECC AgentShield security protocol.
Audits generated source code for security vulnerabilities, hardcoded secrets, SQL injection,
and plain-text authentication before saving or presenting to the user.
"""

import re
import ast
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger("SecurityAuditor")
logger.setLevel(logging.INFO)


class SecurityAuditor:
    """Automated security gatekeeper and vulnerability scanner."""

    # Sensitive key patterns
    SECRET_PATTERNS = [
        (r'(?i)(api[_-]?key|secret|token|password|auth_token)\s*=\s*["\']([a-zA-Z0-9_\-\.]{8,})["\']', "Hardcoded secret or API key"),
        (r'(?i)(gsk_[a-zA-Z0-9]{20,})', "Exposed Groq API key"),
        (r'(?i)(sk-[a-zA-Z0-9]{20,})', "Exposed OpenAI/Cloud API key"),
        (r'(?i)(ghp_[a-zA-Z0-9]{20,})', "Exposed GitHub Personal Access Token"),
        (r'(?i)password\s*=\s*["\'](admin|123456|password|root)["\']', "Insecure default/hardcoded password")
    ]

    # SQL Injection patterns
    SQLI_PATTERNS = [
        (r'(?i)cursor\.execute\s*\(\s*f["\'].*SELECT.*\{', "SQL Injection risk via f-string interpolation"),
        (r'(?i)cursor\.execute\s*\(\s*f["\'].*INSERT.*\{', "SQL Injection risk via f-string interpolation"),
        (r'(?i)cursor\.execute\s*\(\s*f["\'].*UPDATE.*\{', "SQL Injection risk via f-string interpolation"),
        (r'(?i)cursor\.execute\s*\(\s*f["\'].*DELETE.*\{', "SQL Injection risk via f-string interpolation"),
        (r'(?i)cursor\.execute\s*\(\s*["\'].*SELECT.*%s["\']\s*%', "SQL Injection risk via % formatting"),
        (r'(?i)cursor\.execute\s*\(\s*["\'].*\+.*["\']', "SQL Injection risk via string concatenation")
    ]

    # Command Injection & Shell patterns
    COMMAND_PATTERNS = [
        (r'subprocess\.(run|Popen|call)\s*\(.*shell\s*=\s*True', "Insecure subprocess call with shell=True"),
        (r'os\.system\s*\(', "Potentially insecure os.system call (prefer subprocess.run with argument list)")
    ]

    # Plaintext password storage
    PLAINTEXT_PASS_PATTERNS = [
        (r'(?i)def (create_user|register|signup)\b(?s).*?password\b(?!.*?hash)', "User registration without apparent password hashing"),
        (r'(?i)SELECT.*FROM.*users.*WHERE.*password\s*=\s*\?', "Direct plaintext password query (passwords should be hashed and compared via verify_password)")
    ]

    # Frontend XSS patterns
    XSS_PATTERNS = [
        (r'\.innerHTML\s*=\s*(?!["\']<)(?!\s*["\'])', "Potential DOM XSS via raw innerHTML assignment"),
        (r'document\.write\s*\(', "Insecure document.write call")
    ]

    @classmethod
    def audit_file(cls, filename: str, content: str) -> Dict[str, Any]:
        """Performs comprehensive security checks on a single file."""
        findings: List[Dict[str, Any]] = []
        is_python = filename.endswith(".py")
        is_web = filename.endswith((".html", ".js"))

        lines = content.splitlines()

        # 1. Hardcoded Secrets Check
        for pat, desc in cls.SECRET_PATTERNS:
            for idx, line in enumerate(lines, start=1):
                # Ignore placeholders like "your_key_here", "os.getenv", or empty
                if "os.getenv" in line or "your_" in line.lower() or "dummy" in line.lower() or "example" in line.lower():
                    continue
                if re.search(pat, line):
                    findings.append({
                        "file": filename,
                        "line": idx,
                        "severity": "CRITICAL",
                        "type": "hardcoded_secret",
                        "message": desc,
                        "snippet": line.strip()
                    })

        # 2. SQL Injection Check (Python files)
        if is_python:
            for pat, desc in cls.SQLI_PATTERNS:
                for idx, line in enumerate(lines, start=1):
                    if re.search(pat, line):
                        findings.append({
                            "file": filename,
                            "line": idx,
                            "severity": "HIGH",
                            "type": "sql_injection",
                            "message": desc,
                            "snippet": line.strip(),
                            "fix": "Use parameterized queries with ? placeholders: cursor.execute('SELECT ... WHERE col = ?', (val,))"
                        })

            # 3. Command Injection
            for pat, desc in cls.COMMAND_PATTERNS:
                for idx, line in enumerate(lines, start=1):
                    if re.search(pat, line):
                        findings.append({
                            "file": filename,
                            "line": idx,
                            "severity": "MEDIUM",
                            "type": "command_injection",
                            "message": desc,
                            "snippet": line.strip(),
                            "fix": "Avoid shell=True; pass command and arguments as a list: subprocess.run(['cmd', 'arg'])"
                        })

            # 4. AST-based check for eval() and exec()
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                        if node.func.id in ("eval", "exec"):
                            findings.append({
                                "file": filename,
                                "line": getattr(node, "lineno", 1),
                                "severity": "HIGH",
                                "type": "unsafe_execution",
                                "message": f"Dangerous dynamic execution via {node.func.id}()",
                                "snippet": lines[getattr(node, "lineno", 1) - 1].strip() if getattr(node, "lineno", 1) <= len(lines) else "",
                                "fix": "Refactor away from eval/exec; use structured parsing or dictionary dispatch."
                            })
            except Exception:
                pass

        # 5. Frontend XSS Check
        if is_web:
            for pat, desc in cls.XSS_PATTERNS:
                for idx, line in enumerate(lines, start=1):
                    if re.search(pat, line):
                        findings.append({
                            "file": filename,
                            "line": idx,
                            "severity": "LOW",
                            "type": "xss_risk",
                            "message": desc,
                            "snippet": line.strip(),
                            "fix": "Use textContent or sanitize inputs before DOM insertion."
                        })

        return {
            "filename": filename,
            "findings": findings
        }

    @classmethod
    def audit_project(cls, project_files: Dict[str, str]) -> Dict[str, Any]:
        """
        Audits an entire multi-file project dictionary {filename: code_content}.
        Returns an overall security score (0-100), findings list, and pass/fail status.
        """
        all_findings: List[Dict[str, Any]] = []
        files_audited = len(project_files)

        for fname, content in project_files.items():
            res = cls.audit_file(fname, content)
            all_findings.extend(res["findings"])

        # Calculate Security Score
        # Critical = -30, High = -15, Medium = -8, Low = -3
        penalty = 0
        for f in all_findings:
            sev = f["severity"]
            if sev == "CRITICAL":
                penalty += 30
            elif sev == "HIGH":
                penalty += 15
            elif sev == "MEDIUM":
                penalty += 8
            else:
                penalty += 3

        score = max(0, 100 - penalty)
        has_critical = any(f["severity"] == "CRITICAL" for f in all_findings)
        has_high = any(f["severity"] == "HIGH" for f in all_findings)

        passed = score >= 80 and not has_critical and not has_high

        recommendations = []
        if has_critical:
            recommendations.append("Isolate all credentials into environment variables (.env).")
        if any(f["type"] == "sql_injection" for f in all_findings):
            recommendations.append("Convert all raw string SQL queries into parameterized statements with ? placeholders.")
        if any(f["type"] == "command_injection" for f in all_findings):
            recommendations.append("Set shell=False on subprocess invocations and pass argument lists.")
        if not recommendations:
            recommendations.append("Code adheres to OWASP secure engineering standards.")

        return {
            "passed": passed,
            "security_score": score,
            "total_findings": len(all_findings),
            "findings": all_findings,
            "recommendations": recommendations,
            "files_audited": files_audited
        }

    @classmethod
    def auto_patch_sql_injection(cls, python_code: str) -> Tuple[str, int]:
        """Automatically refactors simple f-string SQL queries into parameterized queries."""
        patches = 0
        # Pattern: cursor.execute(f"SELECT ... WHERE col = '{val}'")
        pattern = r'cursor\.execute\s*\(\s*f["\'](SELECT.*?WHERE\s+)(\w+)\s*=\s*[\'"]?\{(\w+)\}[\'"]?(.*?)["\']\s*\)'

        def repl(m):
            nonlocal patches
            patches += 1
            query_prefix = m.group(1)
            col_name = m.group(2)
            var_name = m.group(3)
            query_suffix = m.group(4)
            return f'cursor.execute("{query_prefix}{col_name} = ?{query_suffix}", ({var_name},))'

        patched_code = re.sub(pattern, repl, python_code, flags=re.IGNORECASE)
        return patched_code, patches
