"""
J.A.R.V.I.S. Long-Term Memory Core
Manages persistent user profile, life context, academic records, dynamic facts,
and multi-turn session persistence across restarts.
"""

import os
import json
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, 'memory.json')
SESSIONS_FILE = os.path.join(BASE_DIR, 'sessions_history.json')

DEFAULT_MEMORY = {
    "user_profile": {
        "name": "Krishna",
        "honorific": "Sir",
        "role": "1st-year Mechanical Engineering student",
        "roll_number": "26110285",
        "health_status": "Recovered from a 10-day bout of dengue in late September 2026. Needs pacing, hydration, and gradual catch-up."
    },
    "academic_context": {
        "department": "Mechanical Engineering",
        "faculty": {},
        "current_initiatives": [
            "Building J.A.R.V.I.S. as an autonomous multi-modal AI action agent and desktop companion",
            "Preparing presentation to demonstrate J.A.R.V.I.S. capabilities to university professors",
            "Catching up on classes and assignments missed during 10 days of dengue recovery"
        ]
    },
    "learned_memories": [
        "User is an ambitious 1st-year Mechanical Engineering student building autonomous AI agents.",
        "User communicates through Microsoft Outlook 365.",
        "User prefers concise, practical technical explanations without overwhelming jargon.",
        "User is planning smart automation integrating smart displays, mobile devices, and desktop workstations."
    ],
    "preferences": {
        "persona": "Dignified British butler with Stark-level tactical intelligence",
        "communication_style": "Concise, supportive, loyal, and proactive",
        "voice_tone": "Refined British English"
    }
}

def load_memory() -> dict:
    """Loads memory from memory.json, creating it if it doesn't exist."""
    if not os.path.exists(MEMORY_FILE):
        save_memory(DEFAULT_MEMORY)
        return DEFAULT_MEMORY
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Memory Warning] Failed to parse memory.json: {e}. Falling back to defaults.")
        return DEFAULT_MEMORY

def save_memory(data: dict) -> bool:
    """Safely commits memory data to disk."""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[Memory Error] Failed to save memory: {e}")
        return False

def add_memory(fact: str, category: str = "learned_memories") -> str:
    """Dynamically adds a new learned fact or preference to persistent memory."""
    mem = load_memory()
    clean_fact = fact.strip()
    
    # Remove common prefixes if passed
    for prefix in ["remember that", "remember", "note that", "note down", "don't forget that", "please remember"]:
        if clean_fact.lower().startswith(prefix):
            clean_fact = clean_fact[len(prefix):].strip(" :,.")
            break

    if not clean_fact:
        return "No discernible memory fact provided, Sir."

    timestamp = datetime.datetime.now().strftime("%d %b %Y")
    formatted_entry = f"{clean_fact} (Recorded {timestamp})"

    if category not in mem or not isinstance(mem[category], list):
        mem[category] = []

    # Prevent duplicate entries
    for existing in mem[category]:
        if clean_fact.lower() in existing.lower():
            return f"I already have this recorded in my memory core, Sir: \"{existing}\""

    mem[category].append(formatted_entry)
    save_memory(mem)
    return f"Committed to permanent memory core, Sir: \"{clean_fact}\""

def get_memory_context() -> str:
    """Formats the active memory into a high-priority context block for AI system prompts."""
    mem = load_memory()
    profile = mem.get("user_profile", {})
    academic = mem.get("academic_context", {})
    learned = mem.get("learned_memories", [])
    
    context_lines = [
        "=== PERMANENT LONG-TERM MEMORY CORE (ACTIVE) ===",
        f"User Identity: {profile.get('name', 'Krishna')} ({profile.get('honorific', 'Sir')}) | {profile.get('role', 'Mechanical Engineering Student')} (Roll: {profile.get('roll_number', '26110285')}).",
        f"Health Context: {profile.get('health_status', 'Good')}. When offering life advice or planning, ALWAYS consider his well-being and pace.",
        "Key Faculty & Courses: " + (", ".join([f"{k} ({v})" for k, v in academic.get("faculty", {}).items()]) if academic.get("faculty") else "None specified"),
        "Current Objectives: " + "; ".join(academic.get("current_initiatives", []))
    ]

    if learned:
        context_lines.append("Learned Personal Facts & Preferences:")
        for fact in learned[-10:]:  # Keep most relevant
            context_lines.append(f"  • {fact}")

    context_lines.append("Instructions: Ground all life suggestions, schedule advice, and academic decisions in this past context. Speak with loyal, thoughtful personal awareness.")
    context_lines.append("================================================")
    
    return "\n".join(context_lines)

def get_memory_summary() -> str:
    """Returns a readable summary of what JARVIS currently remembers."""
    mem = load_memory()
    profile = mem.get("user_profile", {})
    academic = mem.get("academic_context", {})
    learned = mem.get("learned_memories", [])
    
    lines = [
        "Here is what is currently stored in my permanent memory core, Sir:\n",
        f"• **Identity**: {profile.get('name', 'Krishna')} Sir",
        f"• **Role**: {profile.get('role', '1st-year Mechanical Engineering student')}",
        f"• **Roll Number**: `{profile.get('roll_number', '26110285')}`",
        f"• **Health Status**: {profile.get('health_status', 'Nominal')}",
        f"• **Key Faculty**: " + (", ".join([f"{k} ({v})" for k, v in academic.get("faculty", {}).items()]) if academic.get("faculty") else "None specified"),
        "\n**Active Directives & Projects**:"
    ]
    
    for init in academic.get("current_initiatives", []):
        lines.append(f"  - {init}")
        
    lines.append(f"\n**Recorded Memories ({len(learned)} items)**:")
    for fact in learned:
        lines.append(f"  • {fact}")
        
    lines.append("\n*All data is permanently stored on your local disk (`memory.json`).*")
    return "\n".join(lines)

def load_chat_history(session_id: str = "default_user") -> list:
    """Loads past session conversation history from disk."""
    if not os.path.exists(SESSIONS_FILE):
        return []
    try:
        with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get(session_id, [])
    except Exception:
        return []

def save_chat_history(session_id: str, history: list):
    """Saves session conversation history to disk."""
    try:
        all_sessions = {}
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
                all_sessions = json.load(f)
        # Store last 16 turns to keep file compact
        all_sessions[session_id] = history[-16:] if len(history) > 16 else history
        with open(SESSIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_sessions, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Memory Warning] Could not persist session history: {e}")
