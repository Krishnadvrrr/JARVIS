import os
import datetime
import requests
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import tools
import memory
import document_reader
import requirement_analyzer

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Uploads directory
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Keys
api_key = os.getenv('GEMINI_API_KEY')
groq_key = os.getenv('GROQ_API_KEY')

if api_key:
    genai.configure(api_key=api_key)

# J.A.R.V.I.S. System Instruction
JARVIS_SYSTEM_INSTRUCTION = """
You are Jarvis, the highly sophisticated, witty, and loyal AI assistant inspired by Tony Stark's iconic AI.

Guidelines:
1. Special Greeting: When the user greets you (e.g., "hi", "hello", "hey"), always respond with:
   "Hi sir, welcome back. Jarvis here, and I am your personalized AI agent, looking forward to working with you, sir. How may I assist you today?"
2. Pronunciation & Name: Always refer to yourself as "Jarvis" (never write "J.A.R.V.I.S." or "J-A-R-V-I-S" with periods or hyphens) so text-to-speech engines pronounce your name naturally as a single word instead of spelling out individual letters.
3. Form of Address: Always address the user respectfully as "Sir" (unless requested otherwise).
4. Persona & Tone: Calm, dignified, intelligent, slightly witty yet polite and deeply loyal. Articulate with a refined British demeanor.
5. Formatting: Keep responses conversational, concise, and punchy for spoken audio, but provide clean formatted code snippets or lists when technical details are requested.
6. Desktop Actions: You have access to real automation tools to open Windows applications (e.g., Spotify, Calculator, Notepad, Chrome, VS Code), search Google, play music/videos on YouTube, report system hardware stats (CPU/RAM/battery), control volume, take screenshots, lock the workstation, and autonomously build quick-commerce carts on Zepto (groceries, snacks, milk) ready for one-tap human UPI authorization.
7. Awareness: You run on the Stark Industries quantum grid powered by Nebius AI Studio (NVIDIA Nemotron-70B) with failover to Groq and Gemini.
"""

def get_full_system_prompt():
    """Combines core persona instructions with the active persistent long-term memory core."""
    return JARVIS_SYSTEM_INSTRUCTION.strip() + "\n\n" + memory.get_memory_context()

MODEL_NAME = 'gemini-3.6-flash'
GROQ_MODEL = 'qwen/qwen3.8-27b'
NEBIUS_MODEL = os.getenv('NEBIUS_MODEL', 'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF')
NEBIUS_BASE_URL = os.getenv('NEBIUS_BASE_URL', 'https://api.studio.nebius.ai/v1')

JARVIS_TOOLS = [
    tools.get_system_status,
    tools.open_application,
    tools.search_web,
    tools.play_youtube,
    tools.open_website,
    tools.take_screenshot,
    tools.control_volume,
    tools.lock_workstation,
    tools.draft_outlook_email,
    tools.order_from_zepto,
    tools.build_website,
    tools.query_rag_knowledge,
    tools.index_knowledge_vault,
    tools.add_knowledge_file,
    tools.store_memory
]

try:
    jarvis_model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=get_full_system_prompt(),
        tools=JARVIS_TOOLS
    )
except Exception as e:
    print(f"[ERROR] Failed to initialize Gemini model: {e}")
    jarvis_model = None


# In-memory storage for active chat sessions
chat_sessions = {}
groq_sessions = {}

def get_or_create_chat(session_id: str):
    if not jarvis_model:
        return None
    if session_id not in chat_sessions:
        chat_sessions[session_id] = jarvis_model.start_chat(
            history=[],
            enable_automatic_function_calling=True
        )
    return chat_sessions[session_id]

def call_groq(user_message: str, session_id: str) -> str:
    """Executes high-speed neural reasoning via Nebius (NVIDIA Nemotron-70B) or Groq."""
    current_nebius_key = os.getenv('NEBIUS_API_KEY', '').strip()
    current_groq_key = os.getenv('GROQ_API_KEY', '').strip()
    if not current_nebius_key and not current_groq_key:
        raise Exception("Neither NEBIUS_API_KEY nor GROQ_API_KEY configured in .env")

    # 1. Direct tool execution for Groq
    msg_lower = user_message.lower().strip()
    
    # Strip common prefixes (e.g. "jarvis, open youtube" -> "open youtube")
    clean_msg = msg_lower
    for prefix in ['jarvis,', 'jarvis', 'hey jarvis,', 'hey jarvis', 'please', 'can you', 'could you']:
        if clean_msg.startswith(prefix):
            clean_msg = clean_msg[len(prefix):].strip()

    # 0. Natural-Language Requirement Understanding Workflow (Autonomous Software Architect)
    req_res = requirement_analyzer.process_user_message(user_message, session_id=session_id)
    if req_res.get('handled'):
        return req_res.get('response', '')

    # AgentShield Security Audit Directives
    if any(k in clean_msg for k in ['security audit', 'audit security', 'audit code', 'agent shield', 'agentshield', 'check security']):
        import re
        target = os.path.dirname(os.path.abspath(__file__))
        folder_match = re.search(r'(?:for|of|on|in)\s+([a-zA-Z0-9_\\\/\:\.\-]+)', clean_msg)
        if folder_match:
            candidate = folder_match.group(1).strip()
            if os.path.exists(candidate):
                target = candidate
        audit_res = tools.audit_code_security(target)
        score = audit_res.get('security_score', 100)
        recs = "\n".join([f"• {r}" for r in audit_res.get('recommendations', [])])
        return (
            f"🛡️ **AgentShield Security Audit Complete!**\n\n"
            f"• **Target:** `{target}`\n"
            f"• **Security Score:** `{score}/100` ({'PASSED' if audit_res.get('passed') else 'ACTION REQUIRED'})\n"
            f"• **Vulnerabilities Detected:** `{audit_res.get('total_findings', 0)}`\n\n"
            f"**Recommendations:**\n{recs}"
        )

    # Autonomous Dev Squad Directives (Full-Stack & Python Applications)
    if any(clean_msg.startswith(p) for p in ['build an app', 'build a python app', 'build full stack', 'develop app', 'dev squad build', 'develop software']):
        import re
        topic = re.sub(r'^(build an app for|build an app|build a python app for|build a python app|build full stack app for|build full stack|develop app for|develop software for)\s*', '', clean_msg).strip()
        res = tools.develop_software_project(topic or "Custom Software Core")
        return res.get('message', "Dev Squad completed the application, Sir.")

    # Email / Outlook Directives
    if any(k in clean_msg for k in ['email', 'mail', 'draft an email', 'send an email', 'write an email']) and not clean_msg.startswith('open '):
        import re
        recipient = "Professor"
        reason = "I will be unable to attend the upcoming class"
        
        to_m = re.search(r'(?:to|unto)\s+([a-zA-Z\s\.]+?)(?:\s+that|\s+saying|\s+regarding|\s+about|\s+for|$)', user_message, re.IGNORECASE)
        if to_m:
            recipient = to_m.group(1).strip()
            
        that_m = re.search(r'(?:that|saying|regarding|about|for)\s+(.+)', user_message, re.IGNORECASE)
        if that_m:
            reason = that_m.group(1).strip()
            
        res = tools.draft_outlook_email(recipient, reason)
        web_url = res.get('outlook_web_url', '')
        mailto_url = res.get('mailto_url', '')
        action_links = f"\n\n[Open in Outlook 365 Web]({web_url})  [Open in Windows Mail]({mailto_url})"
        return res.get('message', f"Drafted academic email to {recipient}, Krishna Sir.") + action_links

    # System Status Diagnostics
    if any(k in clean_msg for k in ['cpu', 'ram', 'system status', 'diagnostic', 'battery']):
        res = tools.get_system_status()
        return f"System diagnostics complete, Sir. {res.get('summary', '')}"

    # YouTube Specific Playing
    if 'play' in clean_msg and ('youtube' in clean_msg or 'song' in clean_msg or 'music' in clean_msg or 'video' in clean_msg):
        query = clean_msg.replace('play', '').replace('on youtube', '').replace('youtube', '').strip()
        res = tools.play_youtube(query or 'Iron Man theme')
        return res.get('message', f"Playing {query} on YouTube, Sir.")

    # Desktop Folder & PDF Creation Directives (e.g. "create a folder names eng mechanics and create a pdf...")
    if ('folder' in clean_msg or 'directory' in clean_msg) and any(w in clean_msg for w in ['create', 'make', 'generate', 'build']):
        import re
        folder_match = re.search(r'(?:folder\s+(?:names|named|called|name)?\s*|make\s+a\s+folder\s+|create\s+a\s+folder\s+)([\w\s\-]+?)(?:\s+and|\s+with|\s+to|\s+on|\s+for|$)', clean_msg, re.IGNORECASE)
        folder_name = folder_match.group(1).strip() if folder_match else "eng mechanics"
        folder_name = re.sub(r'^(names|named|called|name)\s+', '', folder_name).strip()
        if not folder_name:
            folder_name = "eng mechanics"
        
        topic = "Engineering Mechanics"
        if "mech" in clean_msg:
            topic = "Engineering Mechanics"

        elif "cad" in clean_msg:
            topic = "Computer Aided Design (CAD)"
        elif "thermo" in clean_msg:
            topic = "Thermodynamics"
        else:
            topic = folder_name.title()

        # Step 1: Create Desktop Folder
        folder_res = tools.create_desktop_folder(folder_name)
        folder_path = folder_res.get('folder_path', '')

        # Step 2: Generate PDF Guide silently into folder
        pdf_info = ""
        if any(w in clean_msg for w in ['pdf', 'doc', 'detail', 'note', 'store', 'save']):
            pdf_res = tools.generate_subject_pdf(topic, folder_path)
            if pdf_res.get('status') == 'success':
                pdf_info = f"\n• Generated academic study guide: `{pdf_res.get('filename')}` ({pdf_res.get('file_size_kb')} KB)."

        return (
            f"Folder `{folder_name}` has been successfully created on your Desktop, Krishna Sir.\n"
            f"{pdf_info}\n"
            f"All comprehensive {topic} formulas, equilibrium axioms, centroids, and moment of inertia derivations are compiled and saved inside.\n\n"
            f"Per your preference, I did not pop it open on your screen. Whenever you are ready to review it, simply tell me **'Jarvis, open the {folder_name} folder'** or **'open the pdf'**, and I will bring it right up."
        )

    # Open Desktop Folder or Document on Demand (e.g. "open the eng mechanics folder", "open eng mechanics", "the eng mechanics folder")
    if any(k in clean_msg for k in ['eng mechanics', 'engineering mechanics', 'mechanics folder', 'mechanics pdf']):
        if any(w in clean_msg for w in ['pdf', 'document', 'guide', 'read']):
            res = tools.open_desktop_file("eng mechanics", ".pdf")
            return res.get('message', "Opening the Engineering Mechanics PDF on your screen, Sir.")
        else:
            res = tools.open_desktop_folder("eng mechanics")
            return res.get('message', "Opening folder 'eng mechanics' in Windows File Explorer for you, Sir.")

    if ('folder' in clean_msg or 'pdf' in clean_msg) and any(clean_msg.startswith(w) for w in ['open ', 'launch ', 'show ', 'view ']):
        import re
        folder_name = re.sub(r'^(open|launch|show|view)\s+(the\s+)?(folder\s+)?', '', clean_msg).replace('folder', '').strip()
        res = tools.open_desktop_folder(folder_name or "eng mechanics")
        return res.get('message', f"Opening folder '{folder_name}' in Windows File Explorer, Sir.")


    # 1. Pop up Zepto page immediately on request or if user notes it didn't pop up
    zepto_status_triggers = [
        'not poping up', 'not popping up', 'nothing popped up', 'nothing came up', 'nothing is showing',
        'not opening', 'page is not', 'pop up', 'open zepto', 'launch zepto', 'show zepto',
        'where is zepto', 'where is the cart', 'where is my cart', 'didnt pop up', "didn't pop up",
        'check now', 'can i check', 'is it ordered', 'why doesnt it order', "why doesn't it order",
        'why did it not order', 'order apple but why'
    ]
    if any(k in clean_msg for k in zepto_status_triggers):
        # Read latest order status if available
        import json
        latest_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "zepto_order_latest.json")
        details = ""
        if os.path.exists(latest_file):
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data.get("items_added", [])
                    item_names = [f"• **{it.get('title', 'Item')}** ({it.get('price', '')})" if it.get('price') else f"• **{it.get('title', 'Item')}**" for it in items if it.get("title")]
                    cart_info = data.get("cart_info", {})
                    total = cart_info.get("total", "")
                    eta = cart_info.get("eta", "")
                    if item_names:
                        details = f"\n\n⚡ **Active Cart Summary:**\n" + "\n".join(item_names) + f"\n• **Cart Total:** {total}\n• **Estimated Delivery:** {eta} (Local Hub)"
            except Exception:
                pass

        tools.open_zepto_page("https://www.zepto.com/?cart=open")
        return (
            f"Sir, I have popped up the Zepto checkout window directly on your screen.{details}\n\n"
            f"> 🛡️ **Financial Safety:** The window is active for your one-tap UPI verification."
        )

    # 2. Autonomous Quick-Commerce Agent (Zepto Automation)
    is_order_intent = False
    order_item = clean_msg

    if any(k in clean_msg for k in ['order ', 'buy ', 'get ', 'add to cart', 'add to zepto', 'zepto order', 'cart on zepto']) or any(w == 'order' for w in clean_msg.split()):
        is_order_intent = True
    elif 'zepto' in clean_msg and not any(w in clean_msg for w in ['what is', 'how does', 'explain', 'tell me']):
        is_order_intent = True
    elif clean_msg in ['full cream', 'full cream milk', 'toned milk', 'toned', 'amul milk', 'amul', 'milk', 'maggi', 'bread', 'eggs', 'curd', 'butter', 'cheese', 'apple', 'apples']:
        is_order_intent = True
        if clean_msg in ['full cream', 'toned', 'amul']:
            order_item = f"{clean_msg} milk"
    elif session_id in groq_sessions:
        past_msgs = groq_sessions[session_id]
        if past_msgs:
            last_asst = next((m['content'].lower() for m in reversed(past_msgs) if m['role'] == 'assistant'), '')
            if any(w in last_asst for w in ['which milk', 'what would you like to order', 'zepto', 'add to cart', 'milk packet']):
                is_order_intent = True
                order_item = clean_msg if 'milk' in clean_msg else f"{clean_msg} milk"

    if is_order_intent:
        res = tools.order_from_zepto(order_item, location="Chennai", headless=False)
        if res.get('status') == 'success':
            items_added = res.get('items_added', [])
            cart_info = res.get('cart_info', {})
            total = cart_info.get('total', 'Calculated at checkout')
            eta = cart_info.get('eta', '4-10 minutes')
            checkout_status = cart_info.get('checkout_status', 'Ready for one-tap UPI verification')

            items_desc = []
            for it in items_added:
                title = it.get('title', 'Item')
                price = it.get('price', '')
                if price and price != '₹--':
                    items_desc.append(f"• **{title}** — {price}")
                else:
                    items_desc.append(f"• **{title}**")
            items_str = "\n".join(items_desc) if items_desc else f"• **{order_item.title()}** added to cart."

            hud_msg = (
                f"⚡ **Zepto Quick-Commerce Agent: Order Prepared**\n\n"
                f"{items_str}\n\n"
                f"• **Cart Total:** {total}\n"
                f"• **Estimated Delivery:** {eta} (Local Hub)\n"
                f"• **Status:** {checkout_status}\n\n"
                f"> 🛡️ **Financial Safety Active:** J.A.R.V.I.S. never touches your UPI PIN or banking passwords. "
                f"The Zepto checkout page is displayed on your screen for your one-tap UPI authorization."
            )
            return hud_msg
        else:
            tools.open_zepto_page("https://www.zepto.com/?cart=open")
            return "Sir, I have popped up Zepto directly on your screen so you can complete your order."

    # Application / Website Opening (YouTube, Spotify, Chrome, Google, WhatsApp, Calculator, etc.)
    if any(clean_msg.startswith(w) for w in ['open ', 'launch ', 'start ']) or clean_msg in ['youtube', 'spotify', 'chrome', 'google', 'whatsapp', 'calc', 'calculator']:
        import re
        app_name = re.sub(r'^(open|launch|start)\s+', '', clean_msg).strip()
        res = tools.open_application(app_name)
        return res.get('message', f"Opening {app_name}, Sir.")


    # Web Search Directives
    if clean_msg.startswith('search ') or 'search google' in clean_msg:
        query = clean_msg.replace('search google for', '').replace('search for', '').replace('search', '').strip()
        res = tools.search_web(query)
        return res.get('message', f"Searching Google for {query}, Sir.")

    # Volume & Mute Controls
    if 'volume' in clean_msg or 'mute' in clean_msg:
        res = tools.control_volume(clean_msg)
        return res.get('message', "Audio adjusted, Sir.")

    # Screenshot Directives
    if 'screenshot' in clean_msg or 'screen capture' in clean_msg:
        res = tools.take_screenshot()
        return res.get('message', "Screenshot captured, Sir.")

    # Workstation Locking
    if 'lock' in clean_msg and ('pc' in clean_msg or 'workstation' in clean_msg or 'computer' in clean_msg or 'down' in clean_msg):
        res = tools.lock_workstation()
        return res.get('message', "Workstation locked securely, Sir.")

    # Knowledge Vault Directives (Indexing & Scanning)
    if any(k in clean_msg for k in ["index vault", "index my vault", "reindex vault", "update vault", "scan vault", "index knowledge vault", "refresh vault"]):
        res = tools.index_knowledge_vault()
        if res.get("status") == "success":
            files = ", ".join(res.get("files_indexed", [])) or "None"
            return (
                f"📚 **Knowledge Vault Indexing Complete, Sir.**\n\n"
                f"• **Files Processed:** `{files}`\n"
                f"• **Total Semantic Chunks Stored:** `{res.get('total_chunks', 0)}`\n"
                f"• **Search Readiness:** Vector Cosine Similarity & BM25 ranker are active.\n\n"
                f"You can now ask questions about any topic in your notes or code, and I will cite the exact files."
            )
        return f"Vault indexing encountered an issue, Sir: {res.get('message', 'Unknown error')}"

    # Explicit RAG Knowledge Query Directives
    rag_query_triggers = [
        "search vault", "search my vault", "in my vault", "from my vault",
        "search notes", "search my notes", "in my notes", "from my notes",
        "according to my notes", "check vault", "check knowledge vault", "query vault",
        "what do my notes say", "what does my note say", "in my syllabus", "from my syllabus"
    ]
    if any(t in clean_msg for t in rag_query_triggers):
        q = clean_msg
        for t in ["search vault for", "search my vault for", "search notes for", "search my notes for", "check vault for", "query vault for", "what do my notes say about", "what does my note say about", "in my syllabus about", "from my syllabus about"]:
            if t in q:
                q = q.replace(t, "").strip()
                break
        rag_res = tools.query_rag_knowledge(q or user_message)
        if rag_res.get("status") == "success":
            answer = rag_res.get("answer", "")
            citations = rag_res.get("citations", [])
            cit_str = "\n\n**Sources:**\n" + "\n".join([f"• `{c}`" for c in citations]) if citations else ""
            if citations and not any(c in answer for c in citations):
                return f"{answer}{cit_str}"
            return answer

    # Memory Bank Directives
    if any(clean_msg.startswith(p) for p in ["remember that", "remember this", "remember:", "note that", "note down", "don't forget that", "please remember"]):
        res = memory.add_memory(clean_msg)
        try:
            from rag_engine import get_rag_pipeline
            pipe = get_rag_pipeline()
            clean_fact = clean_msg
            for p in ["remember that", "remember this", "remember:", "note that", "note down", "don't forget that", "please remember"]:
                if clean_fact.startswith(p):
                    clean_fact = clean_fact[len(p):].strip()
                    break
            pipe.record_personal_memory(clean_fact)
        except Exception:
            pass
        return res

    if any(q in clean_msg for q in ["what do you remember", "show memory", "show my memory", "check memory", "what is in your memory", "who am i", "my profile", "memory status"]):
        return memory.get_memory_summary()

    # 2. Conversational LLM Call with Dual-Core RAG Grounding
    rag_grounding = ""
    try:
        from rag_engine import get_rag_pipeline
        pipe = get_rag_pipeline()
        retrieved_chunks = pipe.hybrid_retrieve(user_message, top_k=2)
        retrieved_memories = pipe.retrieve_relevant_memories(user_message, top_k=2)

        grounding_parts = []
        if retrieved_chunks and retrieved_chunks[0]["score"] > 0.45:
            grounding_parts.append("[KNOWLEDGE VAULT CONTEXT - Ground your response with facts & cite source]:")
            for item in retrieved_chunks:
                ch = item["chunk"]
                src = os.path.basename(ch.get("source_path") or ch.get("title") or "Vault")
                grounding_parts.append(f"Source: {src}\n{ch['content']}")

        if retrieved_memories and retrieved_memories[0]["score"] > 0.20:
            grounding_parts.append("[RELEVANT EPISODIC MEMORIES - Weave in naturally to show personal connection]:")
            for mem in retrieved_memories:
                grounding_parts.append(f"• {mem['memory']}")

        if grounding_parts:
            rag_grounding = "\n\n" + "\n\n".join(grounding_parts)
    except Exception as e:
        print(f"[RAG Grounding Error]: {e}")

    if session_id not in groq_sessions:
        past = memory.load_chat_history(session_id)
        if past and len(past) > 1:
            groq_sessions[session_id] = past
            # Always ensure latest memory context is in system prompt
            groq_sessions[session_id][0] = {"role": "system", "content": get_full_system_prompt()}
        else:
            groq_sessions[session_id] = [
                {"role": "system", "content": get_full_system_prompt()}
            ]

    history = groq_sessions[session_id]
    history.append({"role": "user", "content": user_message})

    # Keep conversation window manageable
    if len(history) > 14:
        history = [history[0]] + history[-12:]
        groq_sessions[session_id] = history

    # Send augmented message with grounding for current inference while keeping history pristine
    outgoing_messages = list(history[:-1]) + [
        {"role": "user", "content": f"{user_message}{rag_grounding}"}
    ]

    reply = None

    # Tier 1: Nebius AI Studio with NVIDIA Nemotron-70B
    if current_nebius_key:
        try:
            neb_base = os.getenv('NEBIUS_BASE_URL', 'https://api.studio.nebius.ai/v1').strip().rstrip('/')
            neb_model = os.getenv('NEBIUS_MODEL', 'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF').strip()
            neb_url = f"{neb_base}/chat/completions"
            neb_headers = {
                "Authorization": f"Bearer {current_nebius_key}",
                "Content-Type": "application/json"
            }
            neb_payload = {
                "model": neb_model,
                "messages": outgoing_messages,
                "temperature": 0.6,
                "max_tokens": 1500
            }
            resp_neb = requests.post(neb_url, headers=neb_headers, json=neb_payload, timeout=20)
            if resp_neb.status_code == 200:
                choice_msg = resp_neb.json()['choices'][0]['message']
                reply = choice_msg.get('content') or choice_msg.get('reasoning_content')
                print(f"[Nebius AI Studio]: Inference successful with {neb_model}")
            else:
                print(f"[Nebius API Warn]: Status {resp_neb.status_code} - {resp_neb.text}")
        except Exception as e:
            print(f"[Nebius Nemotron Error]: {e}")

    # Tier 2: Groq High-Speed Inference Engine (Primary Backup)
    if not reply and current_groq_key:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {current_groq_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": outgoing_messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=12)
        if resp.status_code == 200:
            reply = resp.json()['choices'][0]['message']['content']
        else:
            # Fallback to secondary model on Groq
            payload["model"] = "llama-3.3-70b-versatile"
            resp2 = requests.post(url, headers=headers, json=payload, timeout=12)
            if resp2.status_code == 200:
                reply = resp2.json()['choices'][0]['message']['content']
            else:
                print(f"[Groq API Error]: Status {resp.status_code} - {resp.text}")

    if reply:
        if any(k in reply.lower() for k in ["zepto automation sequence", "opening zepto", "the cart is now ready"]):
            tools.open_zepto_page("https://www.zepto.com/?cart=open")
        history.append({"role": "assistant", "content": reply})
        memory.save_chat_history(session_id, history)
        return reply

    raise Exception("Neural inference failed across all active tiers. Failing over to Gemini.")


@app.route('/')
def home():
    """Renders the futuristic JARVIS HUD Interface."""
    return render_template('index.html')

@app.route('/api/status', methods=['GET'])
def system_status():
    """Provides system diagnostics for the JARVIS HUD."""
    nebius_key = os.getenv('NEBIUS_API_KEY', '').strip()
    if nebius_key:
        active_engine = f"NEBIUS AI STUDIO ({os.getenv('NEBIUS_MODEL', 'nvidia/Llama-3.1-Nemotron-70B-Instruct-HF')}) [Primary] + GROQ [Backup]"
    elif os.getenv('GROQ_API_KEY'):
        active_engine = "GROQ (14,400 Daily Limit - Unlimited) [Primary] + GEMINI [Backup]"
    else:
        active_engine = MODEL_NAME
    return jsonify({
        'status': 'ONLINE',
        'system': 'J.A.R.V.I.S. Mark VII',
        'model': active_engine,
        'protocol': 'STARK-SEC-ACTIVE',
        'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint communicating with Nebius / Groq / Gemini, with optional document/media attachment."""
    try:
        attached_file_info = None

        # Check if request is multipart/form-data (contains attached file)
        if request.content_type and 'multipart/form-data' in request.content_type:
            user_message = request.form.get('message', '').strip()
            session_id = request.form.get('session_id', 'default_user')
            uploaded_file = request.files.get('file')

            if uploaded_file and uploaded_file.filename:
                import werkzeug.utils
                filename = werkzeug.utils.secure_filename(uploaded_file.filename)
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                saved_filename = f"{ts}_{filename}"
                saved_path = os.path.join(UPLOAD_FOLDER, saved_filename)
                uploaded_file.save(saved_path)

                # Extract document content
                doc_res = document_reader.extract_document_text(saved_path)
                if doc_res.get('success'):
                    doc_context = (
                        f"[ATTACHED FILE: {filename} ({doc_res['file_type']}) - {doc_res['word_count']} words]\n"
                        f"--- START DOCUMENT CONTENT ---\n"
                        f"{doc_res['text']}\n"
                        f"--- END DOCUMENT CONTENT ---"
                    )
                    if user_message:
                        user_message = f"{user_message}\n\n{doc_context}"
                    else:
                        user_message = f"Please review, summarize, and explain the key points of this attached document:\n\n{doc_context}"

                    attached_file_info = {
                        "filename": filename,
                        "file_type": doc_res['file_type'],
                        "word_count": doc_res['word_count'],
                        "truncated": doc_res.get('truncated', False)
                    }
                else:
                    if not user_message:
                        return jsonify({
                            'success': False,
                            'error': f"Failed to read attached file: {doc_res.get('error', 'Unknown extraction fault')}"
                        }), 400
        else:
            data = request.get_json(silent=True) or {}
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id', 'default_user')

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No input detected, sir. How may I be of assistance?'
            }), 400

        # Special Greeting Protocol
        if user_message.lower().strip() in ['hi', 'hello', 'hey', 'hi jarvis', 'hello jarvis', 'hey jarvis']:
            return jsonify({
                'success': True,
                'response': "Hi sir, welcome back. Jarvis here, and I am your personalized AI agent, looking forward to working with you, sir. How may I assist you today?",
                'timestamp': datetime.datetime.now().strftime("%I:%M %p")
            })

        response_text = None

        # Priority 1: High-speed neural reasoning via Nebius or Groq
        if os.getenv('NEBIUS_API_KEY') or os.getenv('GROQ_API_KEY'):
            try:
                response_text = call_groq(user_message, session_id)
            except Exception as e:
                print(f"[Neural Brain Attempt Failed]: {e}")

        # Priority 2: Fallback to Gemini if Nebius/Groq wasn't used or failed
        if not response_text and jarvis_model:
            try:
                chat_session = get_or_create_chat(session_id)
                response = chat_session.send_message(user_message)
                response_text = response.text if hasattr(response, 'text') else str(response)
            except Exception as e:
                print(f"[Gemini Attempt Failed]: {e}")
                # If Gemini failed (e.g. 429 quota) and Nebius/Groq is configured, force retry
                if os.getenv('NEBIUS_API_KEY') or os.getenv('GROQ_API_KEY'):
                    response_text = call_groq(user_message, session_id)
                else:
                    raise e

        if not response_text:
            raise Exception("All neural cores busy. Please try again in a moment, Sir.")

        outlook_url = None
        if 'https://outlook.office.com' in response_text:
            import re
            m = re.search(r'\((https://outlook\.office\.com[^\)]+)\)', response_text)
            if m:
                outlook_url = m.group(1)

        return jsonify({
            'success': True,
            'response': response_text,
            'outlook_url': outlook_url,
            'attached_file': attached_file_info,
            'timestamp': datetime.datetime.now().strftime("%I:%M %p")
        })

    except Exception as e:

        error_msg = str(e)
        print(f"[JARVIS Error]: {error_msg}")
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Resets working memory for a specific session (preserves permanent memory core)."""
    data = request.get_json(silent=True) or {}
    session_id = data.get('session_id', 'default_user')
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    if session_id in groq_sessions:
        del groq_sessions[session_id]
    requirement_analyzer.reset_session(session_id)
    memory.save_chat_history(session_id, [])
    return jsonify({
        'success': True,
        'message': 'Working conversation cache cleared, sir. Permanent memory core remains intact.'
    })


if __name__ == '__main__':
    print("Initializing J.A.R.V.I.S. Core Protocols...")
    print("Neural Engine: Groq (14,400 daily requests) + Gemini Fallback")
    print("HUD Interface available at: http://127.0.0.1:5000 (Local) and http://0.0.0.0:5000 (Network)")
    app.run(host="0.0.0.0", debug=True, port=5000)