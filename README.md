# 🛡️ J.A.R.V.I.S. Mark VII — Autonomous Multi-Modal AI Agent & Desktop Operating Companion

> *"Sometimes you gotta run before you can walk."* — Tony Stark

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![NVIDIA Nemotron](https://img.shields.io/badge/NVIDIA-Nemotron--70B-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![Groq Fast Inference](https://img.shields.io/badge/Groq-LPU%20Inference-F55036?style=for-the-badge)](https://groq.com)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**J.A.R.V.I.S. (Just A Rather Very Intelligent System) Mark VII** is a fully functional, production-grade autonomous desktop AI operating companion and multi-agent system. Combining a charismatic, British-butler persona with serious agentic software engineering, J.A.R.V.I.S. bridges high-speed multi-model LLM reasoning, real Windows operating system automation, mobile voice teleoperation, verifiable RAG knowledge grounding, and self-auditing code synthesis.

---

## 🏛️ System Architecture Overview

```
                                  USER INTERFACES
                     ┌──────────────────────────────────────┐
                     │    Futuristic Stark HUD (Web GUI)   │
                     │    Telegram Mobile Teleoperation Bot │
                     └──────────────────┬───────────────────┘
                                        │
                                        ▼
                            ORCHESTRATION PIPELINE
                     ┌──────────────────────────────────────┐
                     │  Intent Routing & Direct Tool Gate   │
                     │  Natural-Language Requirement Engine │
                     └──────────────────┬───────────────────┘
                                        │
              ┌─────────────────────────┴─────────────────────────┐
              ▼                                                   ▼
     [KNOWLEDGE VAULT RAG V2]                           [MULTI-TIER NEURAL BRAIN]
  • AST-Aware Python Code Chunking                   • Tier 1: Nebius / NVIDIA Nemotron-70B
  • Reciprocal Rank Fusion (Dense + BM25)            • Tier 2: Groq LPU (Sub-300ms Failover)
  • Dynamic Confidence Abstention Gate               • Tier 3: Google Gemini Multimodal
  • Cryptographic Citation Provenance
              │                                                   │
              └─────────────────────────┬─────────────────────────┘
                                        │
                                        ▼
                            AUTONOMOUS ACTION ENGINES
 ┌───────────────────────┬─────────────────────────┬─────────────────────────┐
 │   DESKTOP CONTROL     │   ZEPTO QUICK-COMMERCE  │  AUTONOMOUS DEV SQUAD   │
 │ • Windows App Launch  │ • Headless Carting      │ • Architect & Planner   │
 │ • Audio & Screenshot  │ • Price & ETA Extract   │ • Multi-File Builder    │
 │ • Hardware Telemetry  │ • Human UPI Safeguard   │ • AgentShield Security  │
 │ • Workstation Lock    │                         │ • Dynamic Unittest QA   │
 └───────────────────────┴─────────────────────────┴─────────────────────────┘
```

---

## ⚡ Core Capabilities & Innovations

### 1. 🧠 Multi-Tier Neural Brain with Auto-Failover
J.A.R.V.I.S. implements a resilient 3-tier LLM inference hierarchy ensuring zero downtime:
* **Tier 1 (Sponsor / Deep Reasoning):** **Nebius AI Studio / NVIDIA Nemotron-70B** (`nvidia/Llama-3.1-Nemotron-70B-Instruct-HF` or NVIDIA NIM) for deep software architecture, requirement analysis, and tool planning.
* **Tier 2 (Ultra-Fast Engine):** **Groq Cloud LPU** (`qwen/qwen3.8-27b` and `llama-3.3-70b-versatile`) processing conversational turns at sub-300ms with a 14,400 daily request capacity.
* **Tier 3 (Multimodal Fallback):** **Google Gemini Flash** for visual analysis and document understanding.

### 2. 📚 Verifiable RAG V2 Knowledge Vault
Built from scratch to eliminate hallucinations and enforce strict attribution:
* **Structural Chunking:** AST-aware Python chunking (captures class/function hierarchy and module imports) + multi-level Markdown/PDF section breadcrumbs.
* **Hybrid Fusion:** Reciprocal Rank Fusion (RRF) combining dense vector embeddings with BM25 keyword matching.
* **Confidence Abstention Gate:** If retrieved evidence score falls below the threshold (e.g., 0.50), J.A.R.V.I.S. explicitly abstains from guessing and reports what evidence is missing.
* **Citation Provenance Validator:** Validates bracketed citations against actual retrieved source chunks and automatically strips ungrounded or hallucinated citations.
* **Anti-Prompt Injection Guardrails:** Neutralizes malicious instructions embedded within indexed documents.

### 3. 👥 Autonomous Dev Squad (4-Tier Agentic Team)
An end-to-end multi-agent software engineering team that builds, audits, and tests multi-file Python applications from a single prompt:
1. **Software Architect Agent:** Formulates technical design plans, component breakdowns, and database schemas.
2. **Lead Builder Agent:** Generates production-grade multi-file codebases (`database.py`, `app.py`, `test_suite.py`, `requirements.txt`).
3. **AgentShield Security Auditor:** Scans code AST for vulnerabilities (SQL injection, plaintext credentials, missing password salts, dangerous `eval`/`exec`) and scores security (0–100/100).
4. **Tester Agent:** Autonomously executes dynamic unit tests via `unittest`, reporting pass/fail metrics.

### 4. 🎨 Natural-Language Requirement Analyzer & Domain Intelligence
* **Clarification Engine:** Detects vague requests, formulates focused multiple-choice questions, and halts execution until requirements are resolved.
* **Domain-Native Web Synthesis:** Synthesizes production websites across 5 distinct industry domains (Cloud AI SaaS, Artisan Cafe, High-Intensity Gym, Architecture Firm, Wedding Studio) with tailored palettes, typography, and interactive **Three.js 3D WebGL** canvas animations.

### 5. 🛒 Autonomous Quick-Commerce Agent (Zepto Automation)
* Autonomous browser automation built on Playwright/Selenium that searches items, checks prices, and adds items to the cart.
* **Human-in-the-Loop Financial Safety Gate:** Automatically pops open the checkout window on screen for one-tap human UPI authorization rather than attempting unauthorized financial transactions.

### 6. 📱 Mobile Telegram Bridge with Whisper Voice Notes
* Complete remote teleoperation via Telegram (`@Ascensionjarvis_bot`).
* **Groq Whisper Audio Transcription:** Translates spoken voice notes into text within 200ms.
* **Live Desktop Screen Streaming:** Captures the current desktop workstation and sends high-resolution snapshots directly to your phone.
* **Strict Single-User Security Pairing:** Whitelists only the authenticated owner's `chat_id`.

---

## 📂 Project Repository Structure

```
JARVIS/
├── app.py                             # Core Flask backend & Stark HUD server
├── cli.py                             # Terminal-based interactive interface
├── desktop_app.py                     # Native desktop window launcher (pywebview)
├── dev_squad.py                       # Autonomous Dev Squad multi-agent engine
├── rag_engine.py                      # RAG V2 Grounded Knowledge Vault & retrieval
├── requirement_analyzer.py            # Natural-Language requirement elicitation engine
├── security_auditor.py                # AgentShield static security AST analyzer
├── tester_agent.py                    # Automated test execution agent
├── domain_html_generator.py           # Domain-native HTML & Three.js 3D generator
├── design_intelligence.py             # Design profile & Stitch brief synthesizer
├── design_validator.py                # HTML5 and design quality validator
├── tools.py                           # Operating system & Windows automation tools
├── zepto_agent.py                     # Quick-commerce autonomous agent
├── telegram_bridge.py                 # Mobile Telegram bot bridge & Whisper transcriber
├── memory.py                          # Permanent semantic & episodic memory core
├── memory.json                        # Long-term user profile & preferences
├── document_reader.py                 # Multi-format document extractor (PDF, DOCX, TXT)
├── generate_deck.py                   # Automated presentation deck compiler
├── JARVIS_OpenAI_Campus_Showcase.pptx # 11-Slide widescreen showcase presentation
├── requirements.txt                   # Production Python dependencies
├── .env.example                       # Environment variables configuration template
├── static/                            # Stark HUD CSS, JS, audio, and visual assets
│   ├── style.css
│   ├── main.js
│   └── jarvis_logo.png
├── templates/                         # Futuristic HUD interface template
│   └── index.html
├── knowledge_vault/                   # Indexed documents and study guides
│   ├── jarvis_architecture_guide.md
│   └── college_mechanics_syllabus.md
├── skills/                            # Agentic coding skills library (Markdown)
│   ├── python_clean_code.md
│   ├── security_standards.md
│   ├── sqlite_database.md
│   └── fastapi_rest_api.md
└── test_*.py                          # 42 Automated unit and regression tests
    ├── test_rag_v2.py                 # RAG V2 10-phase verification
    ├── test_nebius_integration.py     # Nebius / NVIDIA failover tests
    ├── test_requirement_analyzer.py   # Multi-turn clarification tests
    ├── test_dev_squad.py              # Autonomous Dev Squad pipeline tests
    └── test_design_intelligence.py    # Domain website & 3D tests
```

---

## 🚀 Quickstart & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Krishnadvrrr/JARVIS.git
cd JARVIS
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure Environment Credentials
Copy `.env.example` to `.env` and insert your keys:
```bash
cp .env.example .env
```

```env
# Primary LLM API Keys
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key

# Mobile Bridge
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Nebius AI Studio & NVIDIA Nemotron (Optional Sponsor Tier)
NEBIUS_API_KEY=your_nebius_or_nvidia_api_key
NEBIUS_BASE_URL=https://api.studio.nebius.ai/v1
NEBIUS_MODEL=nvidia/Llama-3.1-Nemotron-70B-Instruct-HF
```

### 5. Launch J.A.R.V.I.S.
```bash
# Launch the Stark HUD Web Server (http://127.0.0.1:5000)
python app.py

# Launch Mobile Telegram Bridge (in a separate terminal)
python telegram_bridge.py
```

---

## 🧪 Comprehensive Automated Test Suite

J.A.R.V.I.S. includes **42 automated unit and regression tests** verifying all core subsystems:

```bash
python -m unittest discover -s . -p "test_*.py"
```

```
----------------------------------------------------------------------
Ran 42 tests in 29.2s

OK (100% Passed)
  [PASSED] RAG V2 (10/10 Phases: RRF, AST Chunking, Abstention Gate, Provenance)
  [PASSED] Nebius AI Studio & NVIDIA Nemotron Multi-Tier Failover
  [PASSED] Autonomous Dev Squad (Planner, Builder, AgentShield 100/100, Tester)
  [PASSED] Natural-Language Requirement Analyzer (Multi-Turn Disambiguation)
  [PASSED] Domain Intelligence Engine (5 Bespoke Industry Profiles & WebGL 3D)
```

---

## 📽️ OpenAI Campus Showcase Presentation

Included in this repository is the official widescreen presentation deck crafted specifically for university and OpenAI campus presentations:
* **File:** [`JARVIS_OpenAI_Campus_Showcase.pptx`](./JARVIS_OpenAI_Campus_Showcase.pptx)
* **Slides (11):** Covers Architecture, Multi-Agent Collaboration, AgentShield Security, Grounded RAG V2, and Live Teleoperation.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  <b>Built with ❤️ by Krishna & Pair Programmed with Antigravity</b><br>
  <i>"I am Iron Man."</i>
</p>
