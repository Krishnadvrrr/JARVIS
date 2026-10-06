# Skill: Cybersecurity & Application Hardening (AgentShield)
keywords: [security, audit, agentshield, auth, password, hash, vulnerability, owasp, xss, sql injection]

## 1. Secrets & Credentials Management
- NEVER hardcode API keys, passwords, database URLs, or session secrets in source code.
- Always load credentials from environment variables using `os.getenv("VAR_NAME")` or a `.env` file.
- Provide a `.env.example` template without sensitive values.

## 2. Authentication & Password Security
- Plaintext passwords are strictly forbidden.
- Always hash passwords using a salted cryptographic hashing function (e.g. `hashlib.pbkdf2_hmac`, `bcrypt`, or `argon2`).
- Timing-attack resistant comparisons using `hmac.compare_digest()`.

## 3. Injection Prevention
- SQL Injection: Use parameterized queries exclusively (`?` or `:name`).
- Command Injection: Never pass unvalidated user input into `os.system()` or `subprocess.run(shell=True)`. Use argument lists with `shell=False`.
- Path Traversal: Sanitize filenames using `os.path.basename()` and ensure paths resolve inside the allowed project sandbox.

## 4. Frontend Web Hardening
- XSS Prevention: Avoid unsanitized `innerHTML` or `document.write`. Prefer `textContent` or sanitized DOM node insertion.
- Enforce Content-Security-Policy (CSP) headers where applicable.
