"""
J.A.R.V.I.S. Desktop Application Entry Point
Launches Flask in a background thread and presents the Stitch Tactical HUD
inside a dedicated native Windows application window (Edge WebView2).
"""

import os
import sys
import threading
import time
import socket
import webview

# Import the existing Flask app instance
from app import app

HOST = '127.0.0.1'
PORT = 5000

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((HOST, port)) == 0

def run_flask():
    """Runs the Flask backend server quietly without the auto-reloader."""
    import logging
    # Lower Flask/Werkzeug default request log noise
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def on_closed():
    """Ensures clean shutdown of all background threads upon window exit."""
    print("[JARVIS Desktop]: Window closed. Shutting down neural protocols.")
    os._exit(0)

def main():
    print("=" * 60)
    print("      J.A.R.V.I.S. DESKTOP APPLICATION - TACTICAL CORE        ")
    print("=" * 60)

    # 1. Start Flask if not already running on port 5000
    if not is_port_in_use(PORT):
        print("[JARVIS Desktop]: Booting neural server on localhost:5000...")
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()

        # Wait for server to bind
        for _ in range(50):
            if is_port_in_use(PORT):
                print("[JARVIS Desktop]: Core connected successfully.")
                break
            time.sleep(0.1)
    else:
        print("[JARVIS Desktop]: Neural server already online on port 5000.")

    # Start Telegram Mobile Bridge if token configured
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if telegram_token:
        def run_telegram():
            try:
                from telegram_bridge import TelegramBot
                bot = TelegramBot(telegram_token)
                bot.run_polling()
            except Exception as e:
                print(f"[JARVIS Telegram Error]: {e}")
        threading.Thread(target=run_telegram, daemon=True).start()
        print("[JARVIS Desktop]: Mobile Telegram Bridge uplink online (@Ascensionjarvis_bot).")
    print("[JARVIS Desktop]: Initializing Holographic HUD Window...")
    window = webview.create_window(
        title='J.A.R.V.I.S. Tactical HUD - Primary Workstation',
        url=f'http://{HOST}:{PORT}',
        width=1366,
        height=850,
        min_size=(1024, 680),
        background_color='#060913',
        text_select=True,
        zoomable=True
    )

    # Attach clean exit handler
    window.events.closed += on_closed

    # Start Edge WebView2 event loop with custom Holographic Iron Man icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'jarvis_logo.ico')
    webview.start(gui='edgechromium', private_mode=False, icon=icon_path if os.path.exists(icon_path) else None)


if __name__ == '__main__':
    main()
