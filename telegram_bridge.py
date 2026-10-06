"""
J.A.R.V.I.S. Mobile Telegram Bridge
Enables complete remote control over J.A.R.V.I.S. from your mobile phone via Telegram:
- Text commands & autonomous actions (Zepto orders, academic emails, study guides)
- Voice notes transcription via Groq Whisper API (whisper-large-v3)
- Live desktop screen capture delivered to phone
- Direct PDF / study guide document delivery
- Strict single-user security pairing (whitelisted chat_id)
"""

import os
import sys
import time
import json
import logging
import requests
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("JarvisTelegram")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
CONFIG_FILE = os.path.join(PROJECT_ROOT, "static", "telegram_config.json")
FLASK_API_URL = "http://127.0.0.1:5000/api/chat"

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_config(cfg: dict):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving config: {e}")

class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.file_url = f"https://api.telegram.org/file/bot{token}"
        self.offset = 0
        self.config = load_config()

    def get_me(self) -> dict:
        try:
            r = requests.get(f"{self.base_url}/getMe", timeout=10)
            return r.json()
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def send_message(self, chat_id: int, text: str, parse_mode: str = "Markdown") -> dict:
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": False
            }
            if parse_mode:
                payload["parse_mode"] = parse_mode
            r = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=15)
            res = r.json()
            # Fallback if markdown parsing fails
            if not res.get("ok") and "can't parse entities" in res.get("description", ""):
                payload.pop("parse_mode", None)
                r = requests.post(f"{self.base_url}/sendMessage", json=payload, timeout=15)
                res = r.json()
            return res
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return {"ok": False, "error": str(e)}

    def send_photo(self, chat_id: int, photo_path: str, caption: str = "") -> dict:
        try:
            with open(photo_path, "rb") as f:
                files = {"photo": f}
                data = {"chat_id": chat_id, "caption": caption}
                r = requests.post(f"{self.base_url}/sendPhoto", data=data, files=files, timeout=25)
                return r.json()
        except Exception as e:
            logger.error(f"Error sending photo: {e}")
            return {"ok": False, "error": str(e)}

    def send_document(self, chat_id: int, doc_path: str, caption: str = "") -> dict:
        try:
            with open(doc_path, "rb") as f:
                files = {"document": f}
                data = {"chat_id": chat_id, "caption": caption}
                r = requests.post(f"{self.base_url}/sendDocument", data=data, files=files, timeout=30)
                return r.json()
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            return {"ok": False, "error": str(e)}

    def transcribe_voice(self, file_id: str) -> str:
        """Downloads voice note from Telegram and transcribes using Groq Whisper API."""
        if not GROQ_API_KEY:
            return ""
        try:
            # 1. Get file path from Telegram
            r = requests.get(f"{self.base_url}/getFile?file_id={file_id}", timeout=10)
            file_info = r.json()
            if not file_info.get("ok"):
                return ""
            file_path = file_info["result"]["file_path"]

            # 2. Download audio bytes
            download_url = f"{self.file_url}/{file_path}"
            audio_resp = requests.get(download_url, timeout=20)
            if audio_resp.status_code != 200:
                return ""

            # 3. Transcribe via Groq Whisper API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            files = {"file": ("voice.oga", audio_resp.content, "audio/ogg")}
            data = {"model": "whisper-large-v3"}

            groq_resp = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers=headers,
                files=files,
                data=data,
                timeout=25
            )
            groq_json = groq_resp.json()
            return groq_json.get("text", "").strip()
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            return ""

    def query_jarvis(self, user_msg: str) -> dict:
        """Sends user message to local J.A.R.V.I.S. core."""
        try:
            r = requests.post(
                FLASK_API_URL,
                json={"message": user_msg, "session_id": "telegram_mobile"},
                timeout=45
            )
            return r.json()
        except Exception as e:
            return {
                "success": False,
                "response": f"J.A.R.V.I.S. Core connection failed: {e}. Ensure Flask backend is running on port 5000."
            }

    def handle_message(self, msg: dict):
        chat = msg.get("chat", {})
        chat_id = chat.get("id")
        user = msg.get("from", {})
        username = user.get("username", "") or user.get("first_name", "Commander")
        text = msg.get("text", "")
        voice = msg.get("voice") or msg.get("audio")

        # Security check & pairing
        allowed_id = self.config.get("allowed_chat_id")
        if not allowed_id:
            # Pair with first user who initiates /start
            self.config["allowed_chat_id"] = chat_id
            self.config["user_name"] = username
            save_config(self.config)
            logger.info(f"Paired J.A.R.V.I.S. securely with Telegram User ID: {chat_id} ({username})")
            welcome = (
                f"🛡️ **J.A.R.V.I.S. Security Protocol Active**\n\n"
                f"Identity Confirmed: **{username}** (ID: `{chat_id}`)\n"
                f"Workstation: Primary Tactical Workstation Core\n\n"
                f"Mobile uplink established. All protocols unlocked.\n\n"
                f"You can now control your desktop from anywhere:\n"
                f"• Speak with **Voice Notes** (Groq Whisper)\n"
                f"• Type commands like *'order apple on zepto'*\n"
                f"• Request *'send screenshot'* to view your screen\n"
                f"• Type *'draft email to professor'* for academics\n"
                f"• Generate PDFs, lock workstation, or control audio."
            )
            self.send_message(chat_id, welcome)
            return

        if chat_id != allowed_id:
            logger.warning(f"Unauthorized access attempt from ID {chat_id}")
            self.send_message(chat_id, "⛔ Access Denied. J.A.R.V.I.S. is locked to Commander Krishna.")
            return

        # Voice Note handling
        if voice:
            self.send_message(chat_id, "🎙️ *Transcribing voice command via Groq Whisper...*")
            transcribed = self.transcribe_voice(voice.get("file_id"))
            if not transcribed:
                self.send_message(chat_id, "❌ Could not transcribe audio. Please try speaking again or send text.")
                return
            self.send_message(chat_id, f"🗣️ *Voice Command Received:*\n_\"{transcribed}\"_")
            text = transcribed

        if not text:
            return

        clean_text = text.lower().strip()

        # Direct Desktop Screenshot command
        screenshot_triggers = ["screenshot", "screen shot", "send screenshot", "take screenshot", "capture screen", "screen capture", "what's on my screen", "what is on my screen", "screen"]
        if any(k in clean_text for k in screenshot_triggers):
            self.send_message(chat_id, "📸 *Capturing live desktop screen...*")
            try:
                import tools
                res = tools.take_screenshot()
                if res.get("status") == "success":
                    full_path = res.get("filepath")
                    if not full_path or not os.path.exists(full_path):
                        rel_url = res.get("image_url", "")
                        full_path = os.path.join(PROJECT_ROOT, rel_url.lstrip("/"))
                    if os.path.exists(full_path):
                        self.send_photo(chat_id, full_path, caption="🖥️ Live Workstation Screen Capture")
                        return
                    else:
                        self.send_message(chat_id, f"❌ Screenshot file not found at: {full_path}")
                        return
                else:
                    self.send_message(chat_id, f"❌ Screenshot capture error: {res.get('message')}")
                    return
            except Exception as e:
                self.send_message(chat_id, f"❌ Failed to capture screenshot: {e}")
                return

        # Status / Ping command
        if clean_text in ["/start", "status", "ping", "system status"]:
            self.send_message(
                chat_id,
                f"⚡ **J.A.R.V.I.S. Online & Armed**\n\n"
                f"• **Neural Engine:** Groq (Llama-3.3-70B) + Whisper-v3\n"
                f"• **Core Node:** Primary Local Workstation\n"
                f"• **Zepto Agent:** Active (/it Foreground Elevation)\n"
                f"• **Workstation:** Ready for remote orders & study tasks."
            )
            return

        # Dispatch to J.A.R.V.I.S. core
        self.send_message(chat_id, "⚡ *Processing instruction...*")
        jarvis_resp = self.query_jarvis(text)

        reply = jarvis_resp.get("response", "Instruction acknowledged, Sir.")
        self.send_message(chat_id, reply)

        # If a file was generated or attached (e.g. PDF study guide), send the document directly!
        attached_file = jarvis_resp.get("attached_file")
        if attached_file and isinstance(attached_file, dict):
            file_url = attached_file.get("url", "")
            if file_url:
                local_file = os.path.join(PROJECT_ROOT, file_url.lstrip("/"))
                if os.path.exists(local_file):
                    self.send_document(
                        chat_id,
                        local_file,
                        caption=f"📄 {attached_file.get('name', 'Generated Document')}"
                    )

    def run_polling(self):
        """Long polling loop for Telegram updates."""
        logger.info("Initializing Telegram mobile bridge polling loop...")
        while True:
            try:
                url = f"{self.base_url}/getUpdates?offset={self.offset}&timeout=20"
                r = requests.get(url, timeout=25)
                data = r.json()
                if data.get("ok"):
                    for update in data.get("result", []):
                        self.offset = update["update_id"] + 1
                        if "message" in update:
                            self.handle_message(update["message"])
                time.sleep(0.5)
            except Exception as e:
                logger.error(f"Polling error: {e}")
                time.sleep(3)

def main():
    token = TELEGRAM_BOT_TOKEN
    if not token:
        # Check command line args
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            token = sys.argv[1]

    if not token:
        print("=" * 60)
        print("  J.A.R.V.I.S. TELEGRAM MOBILE BRIDGE SETUP REQUIRED  ")
        print("=" * 60)
        print("Please provide your Telegram Bot Token in your .env file:")
        print("  TELEGRAM_BOT_TOKEN=your_token_here")
        print("\nOr run with:")
        print("  python telegram_bridge.py <YOUR_BOT_TOKEN>")
        sys.exit(1)

    bot = TelegramBot(token)
    me = bot.get_me()
    if not me.get("ok"):
        print(f"Error connecting to Telegram API: {me.get('error') or me.get('description')}")
        sys.exit(1)

    bot_info = me.get("result", {})
    print(f"Connected successfully to @{bot_info.get('username')} ({bot_info.get('first_name')})!")
    print("Ready to receive mobile commands. Send /start from your phone to pair.")
    bot.run_polling()

if __name__ == "__main__":
    main()
