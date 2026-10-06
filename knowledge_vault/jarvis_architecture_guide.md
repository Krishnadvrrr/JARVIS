# J.A.R.V.I.S. Autonomous Engineering System Architecture

## Overview
J.A.R.V.I.S. is an autonomous, multi-agent AI engineering and personal assistant developed for Commander Krishna.
It features a dual-core intelligence engine:
1. Autonomous Dev Squad (Planner, Builder, Tester with Self-Healing, and AgentShield Security Auditor)
2. Domain-Aware Design Intelligence Engine (Tailoring websites specifically across photography, cafes, gyms, architecture, and tech SaaS)

## Key Technical Specifications
- Database Architecture: SQLite with parameterized query interfaces, ACID compliance, and foreign key enforcement.
- Security Protocol: AgentShield audits all generated code against OWASP standards, ensuring salted password hashing, zero hardcoded secrets, and no SQL injection vulnerabilities.
- Verification System: Background automated test runner using Python unittest discovery with self-healing feedback loops.
- Mobile Connectivity: Real-time Telegram Mobile Uplink (@Ascensionjarvis_bot) powered by Groq Whisper voice transcription.
