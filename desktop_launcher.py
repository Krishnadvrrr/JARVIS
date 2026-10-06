import os
import sys
import json
import time
import ctypes
import subprocess
import logging

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_FILE = os.path.join(PROJECT_ROOT, "static", "launch_target.json")
RESULT_FILE = os.path.join(PROJECT_ROOT, "static", "launch_result.json")

logging.basicConfig(
    filename=os.path.join(PROJECT_ROOT, "static", "launcher.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def focus_window_by_keyword(keywords):
    """Finds and foregrounds windows matching any of the keywords on Default desktop."""
    try:
        user32 = ctypes.windll.user32
        h_desk = user32.OpenDesktopW('Default', 0, False, 0x01FF)
        if h_desk:
            user32.SetThreadDesktop(h_desk)

        try:
            user32.AllowSetForegroundWindow(-1)
        except Exception:
            pass

        matched_hwnd = None

        def enum_cb(hwnd, extra):
            nonlocal matched_hwnd
            if user32.IsWindowVisible(hwnd):
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value.lower()
                    if any(k.lower() in title for k in keywords):
                        matched_hwnd = hwnd
                        return False
            return True

        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        user32.EnumWindows(EnumWindowsProc(enum_cb), 0)

        if matched_hwnd:
            user32.ShowWindow(matched_hwnd, 9)  # SW_RESTORE
            user32.ShowWindow(matched_hwnd, 3)  # SW_MAXIMIZE
            user32.SetForegroundWindow(matched_hwnd)
            user32.BringWindowToTop(matched_hwnd)
            return True
        return False
    except Exception as e:
        logging.error(f"Error focusing window: {e}")
        return False

def main():
    if not os.path.exists(TARGET_FILE):
        logging.warning("No launch_target.json found.")
        return

    try:
        with open(TARGET_FILE, "r", encoding="utf-8") as f:
            target_info = json.load(f)
    except Exception as e:
        logging.error(f"Failed to read target file: {e}")
        return

    target_type = target_info.get("type", "url")
    target = target_info.get("target", "")
    browser_pref = target_info.get("browser", "auto")

    logging.info(f"Executing launch: type={target_type}, target={target}, browser={browser_pref}")

    success = False
    window_found = False

    EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    if target_type == "url":
        args = []
        if browser_pref == "chrome" and os.path.exists(CHROME_PATH):
            args = [CHROME_PATH, "--new-window", target]
        elif os.path.exists(EDGE_PATH):
            args = [EDGE_PATH, "--new-window", target]
        elif os.path.exists(CHROME_PATH):
            args = [CHROME_PATH, "--new-window", target]
        else:
            args = ["explorer.exe", target]

        try:
            p = subprocess.Popen(args)
            logging.info(f"Launched browser PID {p.pid} with args: {args}")
            success = True
        except Exception as e:
            logging.error(f"Popen failed: {e}")

        # Wait briefly for window creation and bring to front
        time.sleep(1.8)
        kw = ["youtube", "edge", "chrome", "google", "personal"]
        if "youtube" in target.lower():
            kw = ["youtube"]
        elif "spotify" in target.lower():
            kw = ["spotify"]
        elif "instagram" in target.lower():
            kw = ["instagram"]
        elif "whatsapp" in target.lower():
            kw = ["whatsapp"]

        window_found = focus_window_by_keyword(kw)
        logging.info(f"Window focus result for {kw}: {window_found}")

    elif target_type == "app":
        cmd = target_info.get("cmd", target)
        try:
            subprocess.Popen(f'start {cmd}', shell=True)
            success = True
        except Exception as e:
            logging.error(f"Failed to launch app: {e}")

        time.sleep(1.0)
        kw = [target.lower()]
        window_found = focus_window_by_keyword(kw)

    result = {
        "status": "success" if success else "failed",
        "target": target,
        "type": target_type,
        "window_focused": window_found,
        "timestamp": time.time()
    }

    try:
        with open(RESULT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        logging.error(f"Failed to write result: {e}")

if __name__ == "__main__":
    main()
