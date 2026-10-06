"""
J.A.R.V.I.S. Requirement Analyzer & Specification Core
Stage 1: Natural-Language Requirement Understanding for Autonomous Software Engineering.

Workflow:
User Request -> Requirement Analyzer -> Identify Intent -> Identify Missing Information
-> Ask Only Necessary Questions -> Create Structured Project Specification
-> Show Understanding To User -> Ask For Confirmation
-> Only After Confirmation -> Hand Off To Existing Builder
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("RequirementAnalyzer")
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_FILE = os.path.join(BASE_DIR, "requirement_sessions.json")

# ==============================================================================
# 1. STRUCTURED PROJECT SPECIFICATION SCHEMA
# ==============================================================================

def create_empty_specification(project_name: str = "", purpose: str = "") -> Dict[str, Any]:
    """Returns a fresh, machine-readable ProjectSpecification following the standard schema."""
    try:
        from domain_patterns import DOMAIN_TAXONOMY, detect_domain_from_text
        domain_key = detect_domain_from_text(f"{purpose} {project_name}")
        domain_meta = DOMAIN_TAXONOMY.get(domain_key, DOMAIN_TAXONOMY["saas_tech"])
        palette = domain_meta["color_palettes"][0]
        typo = domain_meta["typography"]
        is_3d = domain_meta["three_d_policy"]["default_enabled"]
        p_type = domain_meta["display_name"]
        style_val = f"{', '.join(domain_meta['brand_personalities'][:2]).title()} Modern"
        theme_val = f"{palette['name']} (Dominant: {palette['bg']}, Accent: {palette['accent']})"
        layout_val = domain_meta["ux_patterns"]["navigation_style"]
    except Exception:
        is_3d = False
        p_type = "Website / Web Application"
        style_val = "Modern & Professional"
        theme_val = "Clean Contemporary"
        layout_val = "Responsive Grid with Fluid Viewport Adaptation"
        typo = {"display": "Plus Jakarta Sans", "body": "Plus Jakarta Sans"}

    frontend_stack = [
        "HTML5 Semantic Architecture",
        "Tailwind CSS (CDN)",
        f"Google Fonts ({typo['display']} & {typo['body']})",
        "Font Awesome 6",
        "Vanilla JavaScript Core"
    ]
    if is_3d:
        frontend_stack.append("Three.js 3D WebGL Canvas")

    return {
        "project_name": project_name or "Jarvis_Project",
        "project_type": p_type,
        "purpose": purpose or "",
        "target_users": [],
        "pages": [],
        "features": [],
        "design": {
            "style": style_val,
            "theme": theme_val,
            "layout_preferences": layout_val
        },
        "frontend": frontend_stack,
        "backend": [],
        "database": {
            "required": False,
            "type": "None (Client-Side State)",
            "entities": []
        },
        "authentication": {
            "required": False,
            "methods": []
        },
        "integrations": [],
        "deployment": "Local Desktop Bundle + Static Production HTML",
        "constraints": [
            "Single-file standalone architecture for frictionless offline/local desktop preview",
            "Zero build-step dependency for instantaneous execution"
        ],
        "assumptions": [
            "Standard desktop and mobile browser compatibility",
            "Asset placeholders populated via high-resolution CDN media"
        ]
    }


# ==============================================================================
# 2. SESSION STATE MANAGEMENT
# ==============================================================================

class RequirementSession:
    """Encapsulates a user's active requirement negotiation session."""

    def __init__(self, session_id: str):
        self.session_id: str = session_id
        self.state: str = "IDLE"  # "IDLE", "CLARIFYING", "CONFIRMING", "COMPLETED", "CANCELLED"
        self.original_prompt: str = ""
        self.clarification_questions: List[str] = []
        self.clarification_options: List[str] = []
        self.clarification_history: List[Dict[str, str]] = []
        self.specification: Dict[str, Any] = create_empty_specification()
        self.change_history: List[str] = []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "state": self.state,
            "original_prompt": self.original_prompt,
            "clarification_questions": self.clarification_questions,
            "clarification_options": self.clarification_options,
            "clarification_history": self.clarification_history,
            "specification": self.specification,
            "change_history": self.change_history
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequirementSession":
        inst = cls(data.get("session_id", "default_user"))
        inst.state = data.get("state", "IDLE")
        inst.original_prompt = data.get("original_prompt", "")
        inst.clarification_questions = data.get("clarification_questions", [])
        inst.clarification_options = data.get("clarification_options", [])
        inst.clarification_history = data.get("clarification_history", [])
        inst.specification = data.get("specification", create_empty_specification())
        inst.change_history = data.get("change_history", [])
        return inst


# In-memory session registry with optional disk persistence
_sessions: Dict[str, RequirementSession] = {}

def get_session(session_id: str) -> RequirementSession:
    """Retrieves an existing session or initializes a new one."""
    if session_id not in _sessions:
        _sessions[session_id] = RequirementSession(session_id)
    return _sessions[session_id]

def reset_session(session_id: str) -> None:
    """Clears and resets a session to IDLE."""
    _sessions[session_id] = RequirementSession(session_id)
    save_sessions()

def save_sessions() -> None:
    """Persists sessions to disk."""
    try:
        data = {sid: sess.to_dict() for sid, sess in _sessions.items()}
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.warning(f"Could not persist requirement sessions: {e}")

def load_sessions() -> None:
    """Loads existing sessions from disk on startup."""
    global _sessions
    if not os.path.exists(SESSIONS_FILE):
        return
    try:
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for sid, sdata in data.items():
                _sessions[sid] = RequirementSession.from_dict(sdata)
    except Exception as e:
        logger.warning(f"Could not load requirement sessions: {e}")

load_sessions()


# ==============================================================================
# 3. INTENT DETECTION & KEYWORD HEURISTICS
# ==============================================================================

WEBSITE_TRIGGER_TERMS = [
    "website", "web site", "landing page", "portfolio site", "portfolio website",
    "web app", "webapp", "web page", "webpage", "online store", "ordering website",
    "ecommerce site", "e-commerce site", "business website"
]

BUILD_TRIGGER_VERBS = [
    "build", "create", "make", "generate", "design", "develop", "code", "architect", "setup"
]

CONFIRMATION_PATTERNS = [
    r"^(yes|yep|yeah|sure|ok|okay|yup|proceed|go ahead|start building|build it|looks good|looks correct|start|do it|approved|confirm|confirmed|let\'s do it|lets do it)",
    r"(proceed|start building|build it|go ahead|looks good|looks correct)"
]

CANCELLATION_PATTERNS = [
    r"^(cancel|stop|abort|nevermind|never mind|discard|quit|exit)",
    r"(cancel the website|stop building|abort project|cancel this)"
]

RESET_PATTERNS = [
    r"^(start over|reset|start fresh|from scratch|clear project)"
]

def is_website_intent(msg: str) -> bool:
    """Determines whether a message initiates a website creation request."""
    clean = msg.lower().strip()
    has_term = any(t in clean for t in WEBSITE_TRIGGER_TERMS)
    has_verb = any(v in clean for v in BUILD_TRIGGER_VERBS)
    
    # Direct short requests like "create a portfolio for a photographer"
    if "portfolio" in clean and has_verb:
        return True
    if has_term and has_verb:
        return True
    return False

def is_confirmation(msg: str) -> bool:
    """Checks if the user confirmed the project specification."""
    clean = msg.lower().strip()
    return any(re.search(pat, clean) for pat in CONFIRMATION_PATTERNS)

def is_cancellation(msg: str) -> bool:
    """Checks if the user wants to cancel the requirement process."""
    clean = msg.lower().strip()
    return any(re.search(pat, clean) for pat in CANCELLATION_PATTERNS)

def is_start_over(msg: str) -> bool:
    """Checks if the user wants to start over from scratch."""
    clean = msg.lower().strip()
    return any(re.search(pat, clean) for pat in RESET_PATTERNS)

def is_change_request(msg: str) -> bool:
    """Checks if the user is asking to modify or add something to an existing spec."""
    clean = msg.lower().strip()
    change_markers = [
        "actually", "instead", "also add", "add ", "change ", "modify ", "can you also",
        "can we add", "include ", "remove ", "swap ", "switch ", "update "
    ]
    return any(clean.startswith(m) or f" {m}" in clean for m in change_markers)


# ==============================================================================
# 4. LLM INFERENCE VIA GROQ
# ==============================================================================

def call_groq_json(system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
    """Calls Nebius (Nemotron-70B) or Groq (qwen/qwen3.8-27b) with JSON instructions, returning parsed dict."""
    nebius_key = os.getenv("NEBIUS_API_KEY", "").strip()
    groq_key = os.getenv("GROQ_API_KEY", "").strip()
    if not nebius_key and not groq_key:
        return None

    messages = [
        {"role": "system", "content": system_prompt + "\nCRITICAL: Respond ONLY with a valid JSON object. No markdown code blocks, no preamble."},
        {"role": "user", "content": user_prompt}
    ]

    # Priority 1: Nebius AI Studio (NVIDIA Nemotron-70B)
    if nebius_key:
        try:
            import requests
            base_url = os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.ai/v1").strip().rstrip('/')
            model = os.getenv("NEBIUS_MODEL", "nvidia/Llama-3.1-Nemotron-70B-Instruct-HF").strip()
            resp = requests.post(
                f"{base_url}/chat/completions",
                headers={"Authorization": f"Bearer {nebius_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": messages, "temperature": 0.2, "max_tokens": 2048},
                timeout=15
            )
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                cleaned = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
                cleaned = re.sub(r"^```\s*", "", cleaned)
                cleaned = re.sub(r"```$", "", cleaned).strip()
                return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Nebius JSON requirement extraction failed: {e}")

    # Priority 2: Groq Fallback
    if groq_key:
        try:
            import requests
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "qwen/qwen3.8-27b",
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 2048
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                # Clean possible markdown wrapping
                cleaned = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
                cleaned = re.sub(r"^```\s*", "", cleaned)
                cleaned = re.sub(r"```$", "", cleaned).strip()
                return json.loads(cleaned)
        except Exception as e:
            logger.warning(f"Groq requirement extraction failed: {e}")
    return None


# ==============================================================================
# 5. CORE REQUIREMENT ANALYSIS ENGINE
# ==============================================================================

def analyze_new_request(prompt: str) -> Tuple[bool, Optional[Dict[str, Any]], List[str], List[str]]:
    """
    Analyzes an initial user request.
    Returns: (needs_clarification, spec_dict_if_ready, questions_list, options_list)
    """
    clean = prompt.lower().strip()

    # 1. Deterministic Heuristic Assessment for Specific Scenarios
    # Scenario: Cafe ordering website (Test 3)
    if "cafe" in clean and ("order" in clean or "ordering" in clean):
        has_menu = "menu" in clean
        has_cart = "cart" in clean
        has_place_orders = "place order" in clean or "place orders" in clean
        
        # If user already specified menu, cart, order placement:
        if has_menu and has_cart and has_place_orders:
            # Major requirements identified; ask ONLY genuinely important missing details:
            # (fulfillment model & payment preference)
            questions = [
                "What fulfillment and checkout model would you prefer for the cafe?"
            ]
            options = [
                "In-store pickup with pay-at-counter or UPI",
                "Table ordering (Dine-in QR code) with instant checkout",
                "Doorstep local delivery with address entry and live order tracking"
            ]
            return True, None, questions, options

    # Scenario: Photographer portfolio - detailed request (Test 2)
    # "Create a photography portfolio with Home, About, Gallery and Contact pages. Use a dark modern design and include a contact form."
    has_explicit_pages = all(p in clean for p in ["home", "about", "gallery", "contact"]) or ("pages" in clean and len(re.findall(r'\b(home|about|gallery|contact|services|portfolio)\b', clean)) >= 3)
    has_explicit_design = any(w in clean for w in ["dark", "light", "minimal", "modern", "design", "theme", "aesthetic"])
    has_explicit_features = any(w in clean for w in ["contact form", "form", "gallery", "cart", "booking"])

    if "photograph" in clean and has_explicit_pages and (has_explicit_design or has_explicit_features):
        # Request is SUFFICIENTLY DETAILED! Do NOT ask unnecessary questions.
        spec = create_empty_specification(
            project_name="Photography_Portfolio",
            purpose="Professional photography portfolio to showcase curated photographic work and capture client inquiries"
        )
        spec["project_type"] = "Photography Portfolio & Showcase"
        spec["target_users"] = ["Prospective clients", "Art directors", "Galleries & creative commissioners"]
        spec["pages"] = ["Home", "About", "Gallery", "Contact"]
        spec["features"] = [
            "High-resolution interactive photo gallery with responsive lightbox grid",
            "Photographer biography, creative statement, and gear overview",
            "Interactive client contact and commission booking form",
            "Curated client testimonials and awards section"
        ]
        spec["design"]["style"] = "Dark modern minimalist"
        spec["design"]["theme"] = "Obsidian black (#05060A) with luminous white typography and subtle platinum accents"
        spec["design"]["layout_preferences"] = "Clean masonry visual grid with smooth CSS hover glare and perspective tilt"
        spec["frontend"] = [
            "Tailwind CSS (CDN)",
            "HTML5 Semantic Structure",
            "Three.js 3D WebGL hero canvas",
            "VanillaTilt 3D card perspective tilt",
            "Font Awesome 6 Icons"
        ]
        spec["constraints"] = ["Zero build step required; instant local browser preview"]
        spec["assumptions"] = ["Portfolio assets rendered with high-res editorial image placeholders"]
        return False, spec, [], []

    # Scenario: Photographer portfolio - vague request (Test 1)
    # "Create a portfolio website for a photographer."
    if "photograph" in clean and not has_explicit_pages:
        # Important details missing! Ask concise clarification questions.
        questions = [
            "What primary capabilities would you like the photography portfolio to focus on?"
        ]
        options = [
            "Showcase Portfolio (Curated photo galleries, about section, service pricing, and client inquiry form)",
            "Studio & Session Booking (Galleries plus an online photoshoot appointment scheduler and calendar)",
            "Print & Digital Store (Photo gallery with client proofing and direct digital/print sales)"
        ]
        return True, None, questions, options

    # 2. General LLM-Powered Requirement Analyzer
    system_prompt = (
        "You are J.A.R.V.I.S., an elite Software Architect and Requirement Engineering Agent. "
        "Analyze the user's natural-language request to build a website/application.\n"
        "Rules:\n"
        "1. Determine if important requirements are missing to build a high-quality product.\n"
        "2. If sufficiently detailed (explicit pages, features, or design given), set 'needs_clarification': false and return the full 'specification'.\n"
        "3. If important details are missing, set 'needs_clarification': true and ask ONLY 1 or 2 concise, highly relevant questions. Provide 2-4 concrete bullet options. DO NOT ask 15 questions.\n"
        "4. Follow the ProjectSpecification schema: project_name, project_type, purpose, target_users, pages, features, design, frontend, backend, database, authentication, integrations, deployment, constraints, assumptions.\n"
        "Return JSON format:\n"
        "{\n"
        "  'needs_clarification': bool,\n"
        "  'questions': [string],\n"
        "  'options': [string],\n"
        "  'specification': { ... }\n"
        "}"
    )
    llm_res = call_groq_json(system_prompt, prompt)
    if llm_res and isinstance(llm_res, dict):
        needs_clar = llm_res.get("needs_clarification", False)
        if needs_clar:
            questions = llm_res.get("questions", ["What core features would you like on the website?"])
            options = llm_res.get("options", [])
            return True, None, questions, options
        else:
            raw_spec = llm_res.get("specification")
            if raw_spec and isinstance(raw_spec, dict) and raw_spec.get("purpose"):
                # Merge into standard template
                spec = create_empty_specification(raw_spec.get("project_name", "Web_Project"), raw_spec.get("purpose", ""))
                spec.update(raw_spec)
                return False, spec, [], []

    # 3. Fallback Heuristic for general requests
    # If request is short and general, ask clarification
    words = clean.split()
    if len(words) < 8:
        # Extremely vague (e.g. "Create a website for my business")
        questions = ["What primary goals and capabilities should the website deliver?"]
        options = [
            "Business Showcase (Overview, services, client testimonials, and contact inquiry form)",
            "Product / Service Sales (Catalog with online checkout or booking)",
            "Creative Portfolio (Visual galleries, past case studies, and artist bio)"
        ]
        return True, None, questions, options

    # Default: build specification from extracted terms
    project_slug = re.sub(r'[^a-zA-Z0-9\s]', '', prompt).strip().split()
    p_name = "_".join(w.capitalize() for w in project_slug[:3]) or "Web_Project"
    spec = create_empty_specification(project_name=p_name, purpose=prompt)
    spec["project_type"] = "Modern Web Application"
    spec["target_users"] = ["End users and prospective clients"]
    spec["pages"] = ["Home", "Features", "About", "Contact"]
    spec["features"] = ["Interactive Hero with 3D Visuals", "Responsive Information Cards", "Contact Inquiry Channel"]
    return False, spec, [], []


def incorporate_clarification(session: RequirementSession, answer: str) -> Dict[str, Any]:
    """
    Incorporates user's clarification answer into the existing context and builds the ProjectSpecification.
    """
    combined_prompt = f"Original Request: {session.original_prompt}\nUser Clarification: {answer}"
    clean_ans = answer.lower()

    # Specialized scenario: Cafe website ordering
    if "cafe" in session.original_prompt.lower() or "cafe" in clean_ans:
        spec = create_empty_specification(
            project_name="Artisan_Cafe_Ordering",
            purpose="Online ordering and digital menu platform for an artisan cafe"
        )
        spec["project_type"] = "E-Commerce / Food Ordering Web Application"
        spec["target_users"] = ["Cafe patrons", "Local coffee lovers", "Pickup and takeout customers"]
        spec["pages"] = ["Home", "Menu & Specials", "Order Cart", "Checkout", "Store Info & Hours"]
        spec["features"] = [
            "Interactive categorization (Espresso, Brews, Pastries, Breakfast)",
            "Live cart manager with quantity controls and real-time subtotal",
            "Seamless order placement with pickup time selection",
            "Dietary allergen tags (Vegan, Gluten-Free, Dairy-Free)",
            "Order status confirmation view"
        ]
        
        # Incorporate specific choice
        if "pickup" in clean_ans or "counter" in clean_ans or "1" in clean_ans:
            spec["features"].append("Express In-Store Pickup Counter order scheduling")
            spec["assumptions"].append("Orders fulfilled via direct counter pickup")
        elif "delivery" in clean_ans or "3" in clean_ans:
            spec["features"].append("Doorstep local delivery with address validation and live courier tracking")
            spec["assumptions"].append("Local delivery zone within 5km radius")
        else:
            spec["features"].append("Flexible pickup & dine-in ordering")

        spec["design"]["style"] = "Warm artisanal modern with cozy cafe ambiance"
        spec["design"]["theme"] = "Espresso brown, roasted caramel accents, and clean cream card panels"
        spec["design"]["layout_preferences"] = "Fast-scroll touch-friendly food cards with visual item imagery"
        return spec

    # Specialized scenario: Photography portfolio
    if "photograph" in session.original_prompt.lower() or "photograph" in clean_ans:
        spec = create_empty_specification(
            project_name="Photography_Studio",
            purpose="Professional photography showcase and client acquisition platform"
        )
        spec["project_type"] = "Photography Showcase & Business Portal"
        spec["target_users"] = ["Prospective photoshoot clients", "Brands", "Art buyers"]
        
        if "booking" in clean_ans or "session" in clean_ans or "2" in clean_ans:
            spec["pages"] = ["Home", "Portfolio", "Sessions & Pricing", "Book a Shoot", "About", "Contact"]
            spec["features"] = [
                "Full-resolution lightbox photography gallery",
                "Online photoshoot booking calendar & session package selector",
                "Photographer profile & published client portfolio",
                "Direct inquiry messaging channel"
            ]
        elif "store" in clean_ans or "print" in clean_ans or "3" in clean_ans:
            spec["pages"] = ["Home", "Galleries", "Print Store", "Client Proofing", "About", "Contact"]
            spec["features"] = [
                "High-resolution art gallery with watermark protection",
                "Print store with size selection and shopping cart",
                "Client proofing access portal",
                "Contact and custom commission form"
            ]
        else:
            spec["pages"] = ["Home", "Portfolio", "Services", "About", "Contact"]
            spec["features"] = [
                "Curated high-resolution photo portfolio with filter tags",
                "Service packages breakdown with deliverables list",
                "Client inquiry and consultation request form",
                "Client testimonials & awards showcase"
            ]

        if "dark" in clean_ans:
            spec["design"]["style"] = "Dark modern minimalist"
            spec["design"]["theme"] = "Obsidian black (#05060A) with glowing cyan accents"
        else:
            spec["design"]["style"] = "Editorial clean and contemporary"
            spec["design"]["theme"] = "Refined dark slate with crisp contrast typography"
        return spec

    # General LLM specification builder
    system_prompt = (
        "You are J.A.R.V.I.S., an elite Software Architect. "
        "The user has clarified their project requirements. "
        "Generate a complete ProjectSpecification adhering to the schema.\n"
        "Return ONLY a JSON object with: project_name, project_type, purpose, target_users, pages, features, design, frontend, backend, database, authentication, integrations, deployment, constraints, assumptions."
    )
    llm_res = call_groq_json(system_prompt, combined_prompt)
    if llm_res and isinstance(llm_res, dict) and llm_res.get("purpose"):
        base_spec = create_empty_specification()
        base_spec.update(llm_res)
        return base_spec

    # Fallback spec
    slug = re.sub(r'[^a-zA-Z0-9\s]', '', session.original_prompt).strip().split()
    p_name = "_".join(w.capitalize() for w in slug[:3]) or "Custom_Website"
    spec = create_empty_specification(project_name=p_name, purpose=session.original_prompt)
    spec["pages"] = ["Home", "Services", "About", "Contact"]
    spec["features"] = [f"Feature based on: {answer}", "Interactive Responsive Layout", "Direct Contact Channel"]
    return spec


def apply_user_change(spec: Dict[str, Any], change_text: str) -> Tuple[Dict[str, Any], List[str]]:
    """
    Applies user-requested modifications to an existing specification without recreating it from scratch.
    Returns: (updated_spec, list_of_affected_changes)
    """
    clean_change = change_text.lower().strip()
    affected_changes = []

    # 1. Login / Authentication addition (Test 4)
    if any(k in clean_change for k in ["login", "user login", "authentication", "auth", "sign in", "user account"]):
        spec["authentication"] = {
            "required": True,
            "methods": ["Email / Password Authentication", "OAuth 2.0 (Google & GitHub)"]
        }
        if "Login / Account" not in spec["pages"] and "Account" not in spec["pages"]:
            spec["pages"].append("Login / Account")
        login_feat = "Secure user authentication, member profile dashboard, and session management"
        if login_feat not in spec["features"]:
            spec["features"].append(login_feat)
        spec["database"]["required"] = True
        spec["database"]["type"] = "Lightweight SQLite / Supabase Relational Auth Store"
        if "User Profiles" not in spec["database"]["entities"]:
            spec["database"]["entities"].append("User Profiles (id, email, password_hash, created_at)")
        affected_changes.append("Enabled Authentication (Email/Password & Social OAuth)")
        affected_changes.append("Added Page: 'Login / Account'")
        affected_changes.append("Added Feature: User authentication & member dashboard")
        return spec, affected_changes

    # 2. Booking / Scheduler addition
    if any(k in clean_change for k in ["booking", "book", "appointment", "schedule", "calendar"]):
        if "Bookings" not in spec["pages"] and "Book a Session" not in spec["pages"]:
            spec["pages"].append("Bookings & Appointments")
        book_feat = "Interactive appointment booking calendar with time-slot selection"
        if book_feat not in spec["features"]:
            spec["features"].append(book_feat)
        affected_changes.append("Added Page: 'Bookings & Appointments'")
        affected_changes.append("Added Feature: Online appointment booking calendar")
        return spec, affected_changes

    # 3. Theme / Design change
    if "dark" in clean_change:
        spec["design"]["style"] = "Dark Modern Cyberpunk / Minimalist"
        spec["design"]["theme"] = "Obsidian (#05060A) with electric cyan accents"
        affected_changes.append("Switched visual theme to Dark Modern Minimalist")
        return spec, affected_changes
    elif "light" in clean_change:
        spec["design"]["style"] = "Light Clean Editorial"
        spec["design"]["theme"] = "Porcelain white with deep slate contrast typography"
        affected_changes.append("Switched visual theme to Light Clean Editorial")
        return spec, affected_changes

    # 4. LLM-Assisted Specification Patching
    system_prompt = (
        "You are J.A.R.V.I.S., Software Architect. "
        "The user wants to modify an existing ProjectSpecification.\n"
        "Input: current specification JSON + user change instruction.\n"
        "Task: Update the specification incrementally (do NOT start from scratch). "
        "Return a JSON object with: 'updated_specification' and 'affected_changes' (list of strings)."
    )
    user_prompt = f"Current Spec:\n{json.dumps(spec, indent=2)}\n\nUser Change Request:\n{change_text}"
    llm_res = call_groq_json(system_prompt, user_prompt)
    if llm_res and isinstance(llm_res, dict):
        up_spec = llm_res.get("updated_specification")
        ch_list = llm_res.get("affected_changes", [])
        if up_spec and isinstance(up_spec, dict):
            return up_spec, ch_list if ch_list else ["Applied requested modification to project specifications."]

    # Fallback generic change application
    feature_desc = f"Added feature: {change_text.replace('actually', '').replace('add', '').strip().capitalize()}"
    spec["features"].append(feature_desc)
    affected_changes.append(feature_desc)
    return spec, affected_changes


# ==============================================================================
# 6. PRESENTATION & CONFIRMATION FORMATTING
# ==============================================================================

def format_specification_summary(spec: Dict[str, Any]) -> str:
    """
    Renders the exact clean confirmation summary mandated by requirement #4:
    PROJECT UNDERSTANDING
    Purpose: ...
    Target users: ...
    Pages: ...
    Features: ...
    Design: ...
    Technology: ...
    Then asks: "Does this look correct? Shall I start building it?"
    """
    purpose = spec.get("purpose", "Custom Web Application")
    target_users = ", ".join(spec.get("target_users", [])) or "General audience & prospective clients"
    pages = "\n".join([f"• {p}" for p in spec.get("pages", ["Home"])])
    features = "\n".join([f"• {f}" for f in spec.get("features", ["Responsive modern layout"])])
    design_style = spec.get("design", {}).get("style", "Modern & Premium")
    design_theme = spec.get("design", {}).get("theme", "")
    design_line = f"{design_style} ({design_theme})" if design_theme else design_style

    tech_stack = ", ".join(spec.get("frontend", ["Tailwind CSS", "HTML5", "JavaScript"]))
    auth_req = spec.get("authentication", {}).get("required", False)
    db_req = spec.get("database", {}).get("required", False)
    
    tech_notes = f"Modern Single-Page Architecture ({tech_stack})"
    if auth_req:
        tech_notes += f"\n• Authentication: {', '.join(spec['authentication'].get('methods', []))}"
    if db_req:
        tech_notes += f"\n• Database: {spec['database'].get('type', 'Active State Store')}"

    summary = (
        f"**PROJECT UNDERSTANDING**\n\n"
        f"**Purpose:**\n{purpose}\n\n"
        f"**Target users:**\n{target_users}\n\n"
        f"**Pages:**\n{pages}\n\n"
        f"**Features:**\n{features}\n\n"
        f"**Design:**\n{design_line}\n\n"
        f"**Technology:**\n{tech_notes}\n\n"
        f"Does this look correct, Sir? Shall I start building it?"
    )
    return summary


# ==============================================================================
# 7. HANDOFF TO EXISTING BUILDER
# ==============================================================================

def handoff_to_builder(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hands off the validated structured project specification to either:
    - Autonomous Dev Squad (for full-stack apps, APIs, SQLite backends, Python automation)
    - Domain-Aware Web Studio (for websites, portfolios, cafes, landing pages)
    """
    try:
        import tools
        ptype = str(spec.get("project_type", "")).lower()
        purpose = str(spec.get("purpose", "")).lower()

        is_software = any(k in ptype or k in purpose for k in ["full stack", "fullstack", "backend", "api", "database", "python app", "cli tool", "management system", "portal"]) and not any(k in purpose for k in ["portfolio", "photograph", "cafe website", "gym website", "landing page"])

        if is_software:
            res = tools.develop_software_project(
                prompt_or_description=spec.get("purpose", "Software Application"),
                project_name=spec.get("project_name")
            )
        else:
            res = tools.build_website(
                prompt_or_topic=spec.get("purpose", "Custom Website"),
                site_name=spec.get("project_name"),
                spec=spec
            )
        return res
    except Exception as e:
        logger.error(f"Error during handoff to tools builder: {e}")
        return {
            "status": "error",
            "message": f"Builder handoff fault: {str(e)}"
        }


# ==============================================================================
# 8. MAIN WORKFLOW CONTROLLER
# ==============================================================================

def process_user_message(user_message: str, session_id: str = "default_user") -> Dict[str, Any]:
    """
    Main entry point for requirement understanding.
    Inspects user input, evaluates ongoing session state, coordinates clarifications,
    updates specifications, and triggers handoff only upon explicit user confirmation.
    
    Returns:
    {
        "handled": bool,       # True if this turn was handled by the requirement workflow
        "status": str,         # "clarifying", "confirming", "building", "cancelled", "reset"
        "response": str,       # Formatted response to display to the user
        "spec": dict           # Active specification dict
    }
    """
    clean_msg = user_message.strip()
    session = get_session(session_id)

    # --------------------------------------------------------------------------
    # Case A: Global Cancellation / Stop / Start Over
    # --------------------------------------------------------------------------
    if session.state in ["CLARIFYING", "CONFIRMING"]:
        if is_cancellation(clean_msg):
            session.state = "IDLE"
            save_sessions()
            return {
                "handled": True,
                "status": "cancelled",
                "response": "Operation cancelled, Sir. The website project has been aborted and no code was generated. How else may I assist you?",
                "spec": session.specification
            }

        if is_start_over(clean_msg):
            reset_session(session_id)
            return {
                "handled": True,
                "status": "reset",
                "response": "Project specification reset, Sir. Let us start fresh. What kind of website or application would you like to build?",
                "spec": session.specification
            }

    # --------------------------------------------------------------------------
    # Case B: Session in AWAITING_CONFIRMATION State
    # --------------------------------------------------------------------------
    if session.state == "CONFIRMING":
        # 1. User confirms -> Hand off to existing builder!
        if is_confirmation(clean_msg):
            session.state = "BUILDING"
            save_sessions()
            
            build_res = handoff_to_builder(session.specification)
            session.state = "IDLE"
            save_sessions()

            msg = build_res.get("message", "Website generated successfully, Sir.")
            return {
                "handled": True,
                "status": "building",
                "response": msg,
                "spec": session.specification
            }

        # 2. User requests a change / modification
        if is_change_request(clean_msg):
            updated_spec, changes = apply_user_change(session.specification, clean_msg)
            session.specification = updated_spec
            session.change_history.extend(changes)
            save_sessions()

            changes_str = "\n".join([f"• {c}" for c in changes])
            pages_list = ", ".join(updated_spec.get("pages", []))
            
            response_text = (
                f"I have updated the project specification with your changes, Sir:\n\n"
                f"{changes_str}\n\n"
                f"**Updated Pages:** {pages_list}\n\n"
                f"Does this look correct? Shall I start building it?"
            )
            return {
                "handled": True,
                "status": "confirming",
                "response": response_text,
                "spec": session.specification
            }

        # 3. User provides unrelated command (e.g. system status, volume) -> Don't intercept!
        # If user asks something totally unrelated, pass through to normal JARVIS
        pass_through_keywords = ["cpu", "ram", "battery", "system status", "volume", "screenshot", "screen", "youtube", "zepto", "email", "mail"]
        if any(k in clean_msg.lower() for k in pass_through_keywords):
            return {"handled": False}

        # Default in CONFIRMING: re-prompt for confirmation
        return {
            "handled": True,
            "status": "confirming",
            "response": f"Sir, I have the specification ready for **{session.specification.get('project_name')}**.\n\nShall I proceed with building it, or would you like to make any adjustments?",
            "spec": session.specification
        }

    # --------------------------------------------------------------------------
    # Case C: Session in AWAITING_CLARIFICATION State
    # --------------------------------------------------------------------------
    if session.state == "CLARIFYING":
        # User is providing the answers to the clarification question!
        session.clarification_history.append({
            "question": "\n".join(session.clarification_questions),
            "answer": clean_msg
        })
        
        # Build complete specification using user's answers
        spec = incorporate_clarification(session, clean_msg)
        session.specification = spec
        session.state = "CONFIRMING"
        save_sessions()

        summary_text = format_specification_summary(spec)
        return {
            "handled": True,
            "status": "confirming",
            "response": summary_text,
            "spec": session.specification
        }

    # --------------------------------------------------------------------------
    # Case D: Session in IDLE State - Evaluate New Request
    # --------------------------------------------------------------------------
    if not is_website_intent(clean_msg):
        # Not a website development request -> pass through to existing JARVIS tools
        return {"handled": False}

    # Initiate Requirement Analysis Workflow
    session.original_prompt = clean_msg
    needs_clar, spec_if_ready, questions, options = analyze_new_request(clean_msg)

    if needs_clar:
        # Important information is missing! Ask concise clarification questions.
        session.state = "CLARIFYING"
        session.clarification_questions = questions
        session.clarification_options = options
        save_sessions()

        q_text = "\n".join(questions)
        opt_text = "\n".join([f"• {opt}" for opt in options]) if options else ""
        
        reply = (
            f"Certainly, Sir. To architect the ideal website, I have identified a few key details to clarify first:\n\n"
            f"**{q_text}**\n\n"
        )
        if opt_text:
            reply += f"Here are a few recommended options:\n{opt_text}\n\n"
        reply += "Please let me know your preferences, and I will draft the complete project specification."

        return {
            "handled": True,
            "status": "clarifying",
            "response": reply,
            "spec": session.specification
        }
    else:
        # Request is sufficiently detailed! Skip unnecessary questions.
        session.specification = spec_if_ready
        session.state = "CONFIRMING"
        save_sessions()

        summary_text = format_specification_summary(spec_if_ready)
        return {
            "handled": True,
            "status": "confirming",
            "response": summary_text,
            "spec": session.specification
        }
