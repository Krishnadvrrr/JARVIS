import os
import re
import time
import logging
from typing import List, Dict, Any, Optional
from playwright.sync_api import sync_playwright, Page, BrowserContext

logger = logging.getLogger("ZeptoAgent")
logger.setLevel(logging.INFO)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROFILE_DIR = os.path.join(PROJECT_ROOT, "static", "browser_profiles", "zepto")
os.makedirs(PROFILE_DIR, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"

CATEGORY_MAP = {
    "milk": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "bread": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "egg": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "butter": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "cheese": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "curd": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "paneer": "https://www.zepto.com/cn/dairy-bread-eggs/dairy-bread-eggs/cid/4b938e02-7bde-4479-bc0a-2b54cb6bd5f5/scid/22964a2b-0439-4236-9950-0d71b532b243",
    "maggi": "https://www.zepto.com/cn/packaged-food/packaged-food/cid/5736ad99-f589-4d58-a24b-a12222320a37/scid/dbb39a86-256b-4664-81ed-6668418a5436",
    "noodle": "https://www.zepto.com/cn/packaged-food/packaged-food/cid/5736ad99-f589-4d58-a24b-a12222320a37/scid/dbb39a86-256b-4664-81ed-6668418a5436",
    "chips": "https://www.zepto.com/cn/packaged-food/packaged-food/cid/5736ad99-f589-4d58-a24b-a12222320a37/scid/dbb39a86-256b-4664-81ed-6668418a5436",
    "biscuit": "https://www.zepto.com/cn/breakfast-sauces/breakfast-sauces/cid/f804bccc-c565-4879-b6ab-1b964bb1ed41/scid/c07e4c22-d076-45b0-9c73-92c117956810",
    "cookie": "https://www.zepto.com/cn/breakfast-sauces/breakfast-sauces/cid/f804bccc-c565-4879-b6ab-1b964bb1ed41/scid/c07e4c22-d076-45b0-9c73-92c117956810",
    "tea": "https://www.zepto.com/cn/tea-coffee-more/tea-coffee-more/cid/d7e98d87-6850-4cf9-a37c-e4fa34ae302c/scid/e6763c2d-0bf3-4332-82e4-0c8df1c94cad",
    "coffee": "https://www.zepto.com/cn/tea-coffee-more/tea-coffee-more/cid/d7e98d87-6850-4cf9-a37c-e4fa34ae302c/scid/e6763c2d-0bf3-4332-82e4-0c8df1c94cad",
    "fruits": "https://www.zepto.com/cn/fruits-vegetables/fruits-vegetables/cid/64374cfe-d06f-4a01-898e-c07c46462c36/scid/e78a8422-5f20-4e4b-9a9f-22a0e53962e3",
    "vegetables": "https://www.zepto.com/cn/fruits-vegetables/fruits-vegetables/cid/64374cfe-d06f-4a01-898e-c07c46462c36/scid/e78a8422-5f20-4e4b-9a9f-22a0e53962e3",
    "apple": "https://www.zepto.com/cn/fruits-vegetables/fruits-vegetables/cid/64374cfe-d06f-4a01-898e-c07c46462c36/scid/e78a8422-5f20-4e4b-9a9f-22a0e53962e3",
    "banana": "https://www.zepto.com/cn/fruits-vegetables/fruits-vegetables/cid/64374cfe-d06f-4a01-898e-c07c46462c36/scid/e78a8422-5f20-4e4b-9a9f-22a0e53962e3",
}

_GLOBAL_PLAYWRIGHT = None
_GLOBAL_CONTEXT = None
_GLOBAL_PAGE = None

def focus_zepto_window():
    """Brings the Zepto browser window to the foreground on Windows Default desktop."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        try:
            h_desk = user32.OpenDesktopW('Default', 0, False, 0x01FF)
            if h_desk:
                user32.SetThreadDesktop(h_desk)
        except Exception:
            pass

        try:
            user32.AllowSetForegroundWindow(-1)
        except Exception:
            pass

        def enum_windows_proc(hwnd, lParam):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value.lower()
                if 'zepto' in title or ('edge' in title and any(k in title for k in ['cart', 'fruit', 'dairy', 'quick', 'grocery'])):
                    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                    user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
                    user32.SetForegroundWindow(hwnd)
                    user32.BringWindowToTop(hwnd)
                    return False
            return True

        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        user32.EnumWindows(EnumWindowsProc(enum_windows_proc), 0)
    except Exception as e:
        logger.warning(f"Could not focus window: {e}")

STATE_FILE = os.path.join(PROJECT_ROOT, "static", "zepto_state.json")

def create_browser_and_page(p, headless: bool = False):
    """Launches lightweight Edge/Chromium browser with saved state, avoiding directory lock collisions."""
    browser = None
    for ch in ["msedge", "chrome", None]:
        try:
            browser = p.chromium.launch(
                channel=ch,
                headless=headless,
                args=["--start-maximized"] if not headless else []
            )
            break
        except Exception as e:
            logger.warning(f"Could not launch browser with channel '{ch}': {e}")

    if not browser:
        raise RuntimeError("Failed to launch Edge, Chrome, or Chromium.")

    context_kwargs = {
        "user_agent": USER_AGENT,
        "locale": "en-IN",
        "timezone_id": "Asia/Kolkata",
    }
    if not headless:
        context_kwargs["no_viewport"] = True
    else:
        context_kwargs["viewport"] = {"width": 1280, "height": 840}

    if os.path.exists(STATE_FILE):
        try:
            context_kwargs["storage_state"] = STATE_FILE
        except Exception:
            pass

    context = browser.new_context(**context_kwargs)
    page = context.new_page()
    return browser, context, page

def set_delivery_location_if_needed(page: Page, target_location: str = "Chennai") -> bool:
    """Configures delivery location if not already selected."""
    try:
        page.goto("https://www.zepto.com", wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(2500)
        
        loc_btn = page.locator('text=/Select Location/i').first
        if loc_btn.count() > 0:
            logger.info("Setting delivery location on Zepto...")
            loc_btn.click()
            page.wait_for_timeout(1500)
            
            addr_inp = page.locator('input[placeholder*="Search a new address" i]').first
            if addr_inp.count() > 0:
                addr_inp.fill(target_location)
                page.wait_for_timeout(2500)
                
                # Check for suggestion containing target_location
                sug = page.locator(f'text=/{target_location}/i').all()
                clicked = False
                for s in sug:
                    txt = s.inner_text().strip()
                    if 'tamil nadu' in txt.lower() or 'chennai' in txt.lower():
                        s.click()
                        clicked = True
                        page.wait_for_timeout(2500)
                        break
                
                if not clicked and len(sug) > 0:
                    sug[0].click()
                    page.wait_for_timeout(2500)
                    
                # If a confirm button appears, click it
                for b in page.locator('button').all():
                    if 'confirm' in b.inner_text().lower():
                        b.click()
                        page.wait_for_timeout(2000)
                        break
                        
                return True
        return True
    except Exception as e:
        logger.error(f"Error checking/setting location: {e}")
        return False

def extract_title_and_price(card_lines: List[str], fallback: str) -> tuple:
    price = "₹--"
    title = fallback.title()

    prices = [l for l in card_lines if '\u20b9' in l or '₹' in l]
    if prices:
        price = prices[0]

    # First priority: line containing keyword from query (e.g. 'apple', 'milk')
    query_words = [w for w in fallback.lower().split() if len(w) >= 3]
    for l in card_lines:
        clean = l.strip()
        if not clean or clean.lower() in ['add', 'off'] or '\u20b9' in clean or '₹' in clean:
            continue
        if any(unit in clean.lower() for unit in [' g', ' kg', ' pcs', ' mins', ' ml', ' pack']):
            continue
        if any(w in clean.lower() for w in query_words):
            return clean, price

    # Second priority: first descriptive text line
    for l in card_lines:
        clean = l.strip()
        if not clean or clean.lower() in ['add', 'off'] or '\u20b9' in clean or '₹' in clean:
            continue
        if any(unit in clean.lower() for unit in [' g', ' kg', ' pcs', ' mins', ' ml', ' pack']):
            continue
        title = clean
        break

    return title, price

def add_item_to_cart(page: Page, item_query: str) -> Dict[str, Any]:
    """
    Finds product for item_query and clicks ADD.
    Tries direct search first; if login wall is hit, uses smart category fallback.
    """
    clean_q = item_query.strip().lower()

    # 1. Try search bar
    try:
        search_url = f"https://www.zepto.com/search?query={item_query.replace(' ', '+')}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(3000)

        # Check if login block is triggered
        body_sample = page.inner_text("body")[:800].lower()
        needs_category_fallback = "please login to continue searching" in body_sample

        if not needs_category_fallback:
            add_btns = page.locator('button:has-text("ADD")').all()
            if add_btns:
                first_btn = add_btns[0]
                try:
                    p_card = first_btn.locator('xpath=ancestor::div[3]')
                    lines = [l.strip() for l in p_card.inner_text().split('\n') if l.strip()]
                    title, price = extract_title_and_price(lines, clean_q)
                except Exception:
                    title = clean_q.title()
                    price = "₹--"

                first_btn.click()
                page.wait_for_timeout(2000)
                return {"status": "success", "title": title, "price": price, "query": item_query}
    except Exception as e:
        logger.warning(f"Direct search attempt failed for '{item_query}': {e}")

    # 2. Smart Category Fallback (works without login)
    matched_cat_url = None
    for keyword, cat_url in CATEGORY_MAP.items():
        if keyword in clean_q:
            matched_cat_url = cat_url
            break

    if not matched_cat_url:
        matched_cat_url = CATEGORY_MAP["milk"]

    try:
        logger.info(f"Navigating to category fallback for '{item_query}': {matched_cat_url}")
        page.goto(matched_cat_url, wait_until="domcontentloaded", timeout=25000)
        page.wait_for_timeout(3500)

        add_btns = page.locator('button:has-text("ADD")').all()
        if not add_btns:
            return {"status": "error", "message": f"Could not find available stock for '{item_query}'."}

        selected_btn = add_btns[0]
        selected_title = clean_q.title()
        selected_price = "₹--"

        words = clean_q.split()
        for b in add_btns:
            try:
                p_card = b.locator('xpath=ancestor::div[3]')
                text = p_card.inner_text().lower()
                if any(w in text for w in words):
                    selected_btn = b
                    lines = [l.strip() for l in p_card.inner_text().split('\n') if l.strip()]
                    selected_title, selected_price = extract_title_and_price(lines, clean_q)
                    break
            except Exception:
                pass

        if selected_price == "₹--":
            try:
                p_card = selected_btn.locator('xpath=ancestor::div[3]')
                lines = [l.strip() for l in p_card.inner_text().split('\n') if l.strip()]
                selected_title, selected_price = extract_title_and_price(lines, clean_q)
            except Exception:
                pass

        selected_btn.click()
        page.wait_for_timeout(2000)
        return {
            "status": "success",
            "title": selected_title,
            "price": selected_price,
            "query": item_query
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def parse_cart_details(page: Page) -> Dict[str, Any]:
    """Opens cart drawer and parses line items, total price, and delivery ETA."""
    try:
        # Check if cart drawer is already open
        is_drawer_open = page.locator('[data-vaul-drawer], [role="dialog"]').count() > 0
        if not is_drawer_open:
            cart_btn = page.locator('text=/Cart/i').first
            if cart_btn.count() > 0:
                try:
                    cart_btn.click(timeout=3000)
                    page.wait_for_timeout(2000)
                except Exception:
                    pass
            
        body_text = page.inner_text("body")
        
        # Delivery ETA
        eta_match = re.search(r'(\d+\s+minutes|\d+\s+mins|Delivering in\s+[^\n]+)', body_text, re.IGNORECASE)
        eta = eta_match.group(0) if eta_match else "4-10 minutes"
        
        # Item Count
        count_match = re.search(r'(\d+)\s+items?', body_text, re.IGNORECASE)
        count_str = count_match.group(0) if count_match else "Items in cart"
        
        # Item Total (Bill Summary)
        total_match = re.search(r'Item Total\s*\n\s*[₹?]?\s*(\d+)', body_text)
        if not total_match:
            total_match = re.search(r'To Pay\s*\n\s*[₹?]?\s*(\d+)', body_text)
            
        total_str = f"₹{total_match.group(1)}" if total_match else "Calculated at checkout"
        
        # Check login status
        is_logged_in = "login to proceed" not in body_text.lower() and "please login" not in body_text.lower()
        
        return {
            "status": "success",
            "eta": eta,
            "item_count": count_str,
            "total": total_str,
            "is_logged_in": is_logged_in,
            "checkout_status": "Ready for one-tap UPI verification" if is_logged_in else "Awaiting 1-time mobile verification"
        }
    except Exception as e:
        return {
            "status": "partial",
            "eta": "4-10 minutes",
            "total": "Calculated at checkout",
            "is_logged_in": False,
            "error": str(e)
        }

def pop_up_zepto(url: str = "https://www.zepto.com/?cart=open"):
    """Instantly opens or focuses the Zepto window on the user's screen."""
    import webbrowser
    webbrowser.open(url)

def order_from_zepto_flow(items: List[str], location: str = "Chennai", headless: bool = False) -> Dict[str, Any]:
    """
    Full autonomous quick-commerce flow:
    1. Launches browser with persistent storage state (stays open on screen).
    2. Verifies delivery location.
    3. Adds requested items to cart.
    4. Extracts itemized receipt, ETA, and total.
    5. Keeps browser active on checkout page for user's one-tap UPI verification.
    """
    import threading
    p = sync_playwright().start()
    try:
        browser, context, page = create_browser_and_page(p, headless=headless)

        # 1. Location
        set_delivery_location_if_needed(page, target_location="Chennai")

        # 2. Add each item
        added_results = []
        for it in items:
            res = add_item_to_cart(page, it)
            if res.get("status") == "success":
                added_results.append(res)

        # 3. Open Cart & Parse Details
        try:
            page.goto("https://www.zepto.com/?cart=open", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)
        except Exception:
            pass

        cart_info = parse_cart_details(page)

        # Save storage state
        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        # Ensure page is brought to front
        if not headless:
            try:
                page.bring_to_front()
                focus_zepto_window()
            except Exception:
                pass

        summary = {
            "status": "success" if added_results else "failed",
            "location": location,
            "items_added": added_results,
            "cart_info": cart_info,
            "note": "Browser is kept open on your screen for one-tap UPI verification."
        }

        # Keep browser open in background daemon thread
        if not headless:
            def keep_open():
                try:
                    while not page.is_closed():
                        time.sleep(1)
                except Exception:
                    pass
                finally:
                    try:
                        context.close()
                        browser.close()
                        p.stop()
                    except Exception:
                        pass
            threading.Thread(target=keep_open, daemon=True).start()
        else:
            try:
                context.close()
                browser.close()
                p.stop()
            except Exception:
                pass

        return summary
    except Exception as e:
        logger.error(f"Zepto order error: {e}")
        try:
            p.stop()
        except Exception:
            pass
        return {"status": "error", "message": str(e)}

def run_agent_cli():
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Zepto Quick-Commerce Agent CLI")
    parser.add_argument("--items", nargs="+", default=None, help="List of items to order")
    parser.add_argument("--location", default="Chennai", help="Target delivery location")
    parser.add_argument("--headless", action="store_true", help="Run browser headlessly")
    parser.add_argument("--open-cart", type=str, default=None, help="Directly open cart URL")
    args = parser.parse_args()

    p = sync_playwright().start()
    try:
        browser, context, page = create_browser_and_page(p, headless=args.headless)

        if not args.headless:
            try:
                page.bring_to_front()
                focus_zepto_window()
            except Exception:
                pass

        if args.open_cart:
            page.goto(args.open_cart, wait_until="domcontentloaded")
            if not args.headless:
                try:
                    page.bring_to_front()
                    focus_zepto_window()
                except Exception:
                    pass
                while not page.is_closed():
                    try:
                        page.wait_for_timeout(1000)
                    except Exception:
                        break
            return

        items = args.items or ["apple"]
        location = args.location
        headless = args.headless

        # 1. Location
        set_delivery_location_if_needed(page, target_location="Chennai")

        # 2. Add each item
        added_results = []
        for it in items:
            res = add_item_to_cart(page, it)
            if res.get("status") == "success":
                added_results.append(res)

        # 3. Open Cart & Parse Details
        try:
            page.goto("https://www.zepto.com/?cart=open", wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000)
        except Exception:
            pass

        cart_info = parse_cart_details(page)

        # Save storage state
        try:
            context.storage_state(path=STATE_FILE)
        except Exception:
            pass

        # Bring window to front with cart open
        if not headless:
            try:
                page.bring_to_front()
                focus_zepto_window()
            except Exception:
                pass

        summary = {
            "status": "success" if added_results else "failed",
            "location": location,
            "items_added": added_results,
            "cart_info": cart_info,
            "note": "Browser is kept open on your screen for one-tap UPI verification."
        }

        # Write to static/zepto_order_latest.json
        latest_file = os.path.join(PROJECT_ROOT, "static", "zepto_order_latest.json")
        try:
            with open(latest_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
        except Exception:
            pass

        # Output JSON result marker for parent process
        print(f"__ZEPTO_RESULT__:{json.dumps(summary)}", flush=True)

        # Keep browser open on main thread for human authorization
        if not headless:
            logger.info("Zepto checkout is ready on screen. Waiting for user interaction...")
            while not page.is_closed():
                try:
                    page.wait_for_timeout(1000)
                except Exception:
                    break
    except Exception as e:
        logger.error(f"CLI Error: {e}")
        err_res = {"status": "error", "message": str(e)}
        print(f"__ZEPTO_RESULT__:{json.dumps(err_res)}", flush=True)
    finally:
        try:
            context.close()
            browser.close()
            p.stop()
        except Exception:
            pass

if __name__ == "__main__":
    run_agent_cli()
