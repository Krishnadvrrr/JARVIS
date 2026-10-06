import os
import sys
import requests
from dotenv import load_dotenv
import tools
import requirement_analyzer

# Load environment variables
load_dotenv()

groq_key = os.getenv('GROQ_API_KEY')
if not groq_key:
    print("[ERROR] GROQ_API_KEY not found in .env file.")
    sys.exit(1)

JARVIS_SYSTEM_INSTRUCTION = """
You are Jarvis, the highly sophisticated, witty, and loyal AI assistant inspired by Tony Stark's AI.

Guidelines:
1. Special Greeting: When the user greets you (e.g., "hi", "hello", "hey"), always respond with:
   "Hi sir, welcome back. Jarvis here, and I am your personalized AI agent, looking forward to working with you, sir. How may I assist you today?"
2. Pronunciation & Name: Always refer to yourself as "Jarvis".
3. Form of Address: Always address the user respectfully as "Sir" (unless requested otherwise).
4. Persona & Tone: Calm, dignified, intelligent, slightly witty yet polite and deeply loyal. Articulate with a refined British demeanor.
5. Keep terminal responses clear, crisp, and stylish.
"""

GROQ_MODEL = 'qwen/qwen3.8-27b'

history = [
    {"role": "system", "content": JARVIS_SYSTEM_INSTRUCTION}
]

def print_banner():
    print("=" * 65)
    print("         J . A . R . V . I . S .   T E R M I N A L   C O R E")
    print("      Stark Industries Neural Grid (Groq High-Speed LPU)")
    print("=" * 65)
    print("Type your message below. Type 'exit' or 'quit' to shut down.\n")

def call_groq_cli(user_message: str) -> str:
    msg_lower = user_message.lower().strip()
    
    if msg_lower in ['hi', 'hello', 'hey', 'hi jarvis', 'hello jarvis']:
        return "Hi sir, welcome back. Jarvis here, and I am your personalized AI agent, looking forward to working with you, sir. How may I assist you today?"
        
    # Natural-Language Requirement Understanding Workflow
    req_res = requirement_analyzer.process_user_message(user_message, session_id="cli_user")
    if req_res.get('handled'):
        return req_res.get('response', '')

    if any(k in msg_lower for k in ['email', 'mail', 'draft an email', 'send an email', 'write an email']) and not msg_lower.startswith('open '):
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
        return res.get('message', f"Drafted academic email to {recipient} and opened Outlook, Krishna Sir.")

    if any(k in msg_lower for k in ['cpu', 'ram', 'system status', 'diagnostic', 'battery']):
        res = tools.get_system_status()
        return f"System diagnostics complete, Sir. {res.get('summary', '')}"

    if msg_lower.startswith('open ') or msg_lower.startswith('launch '):
        app_name = msg_lower.replace('open ', '').replace('launch ', '').strip()
        if 'youtube' not in app_name and 'google' not in app_name:
            res = tools.open_application(app_name)
            return res.get('message', f"Opening {app_name}, Sir.")

    if 'youtube' in msg_lower and ('play' in msg_lower or 'search' in msg_lower):
        query = msg_lower.replace('play', '').replace('on youtube', '').replace('youtube', '').strip()
        res = tools.play_youtube(query or 'Iron Man theme')
        return res.get('message', f"Playing {query} on YouTube, Sir.")

    if msg_lower.startswith('search ') or 'search google' in msg_lower:
        query = msg_lower.replace('search google for', '').replace('search for', '').replace('search', '').strip()
        res = tools.search_web(query)
        return res.get('message', f"Searching Google for {query}, Sir.")

    if 'volume' in msg_lower or 'mute' in msg_lower:
        res = tools.control_volume(msg_lower)
        return res.get('message', "Audio adjusted, Sir.")

    if 'screenshot' in msg_lower:
        res = tools.take_screenshot()
        return res.get('message', "Screenshot captured, Sir.")

    if 'lock' in msg_lower and ('pc' in msg_lower or 'workstation' in msg_lower or 'computer' in msg_lower or 'down' in msg_lower):
        res = tools.lock_workstation()
        return res.get('message', "Workstation locked securely, Sir.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }

    history.append({"role": "user", "content": user_message})
    
    payload = {
        "model": GROQ_MODEL,
        "messages": history[-10:],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    if resp.status_code == 200:
        reply = resp.json()['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": reply})
        return reply
    else:
        return f"[Connection fault]: Status {resp.status_code}"

def main():
    print_banner()
    print("JARVIS: Good day, sir. All terminal subsystems are active. How may I assist you?\n")
    
    while True:
        try:
            user_input = input("YOU: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nJARVIS: Powering down neural registers. Have a splendid day, sir.")
                break
            
            print("\nJARVIS is analyzing directive...", end="\r")
            response = call_groq_cli(user_input)
            
            print(" " * 40, end="\r")
            print(f"JARVIS: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nJARVIS: Directive cancelled. Farewell, sir.")
            break
        except Exception as e:
            print(f"\n[JARVIS Error]: {e}\n")

if __name__ == '__main__':
    main()

