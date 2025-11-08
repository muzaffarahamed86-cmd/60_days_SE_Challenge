from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
import time

def locate_bing_search_bar():
    with sync_playwright() as p:
        # Launch Edge (maximized)
        browser = p.chromium.launch(channel="msedge", headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        print("🌐 Navigating to Bing...")
        page.goto("https://www.bing.com", wait_until="domcontentloaded")

        # Handle cookie consent popup
        try:
            accept_btn = page.locator("button:has-text('Accept')")
            if accept_btn.is_visible():
                print("🍪 Clicking Accept cookies...")
                accept_btn.click()
        except Exception:
            pass

        # Try multiple selectors for search bar
        possible_selectors = [
            "input[name='q']",
            "input#sb_form_q",
            "textarea[name='q']",
        ]

        search_bar = None
        for selector in possible_selectors:
            try:
                print(f"🔍 Trying selector: {selector}")
                search_bar = page.wait_for_selector(selector, timeout=10000, state="visible")
                if search_bar:
                    print(f"✅ Search bar found with selector: {selector}")
                    break
            except PlaywrightTimeoutError:
                continue

        if not search_bar:
            print("❌ Could not find Bing search bar with any known selector!")
            browser.close()
            return

        # Print info about the located element
        print("🔧 Element details:")
        print(f"Tag: {search_bar.evaluate('el => el.tagName')}")
        print(f"Placeholder: {search_bar.get_attribute('placeholder')}")
        print(f"Name: {search_bar.get_attribute('name')}")

        # Step 2️⃣ Type and search
        search_query = "IND vs SA Women's Final scorecard"
        print(f"⌨️ Typing query: {search_query}")
        search_bar.fill(search_query)
        page.keyboard.press("Enter")

        print("🔄 Waiting for search results to load...")
        page.wait_for_selector("li.b_algo h2 a", timeout=15000)
        print("✅ Search results loaded successfully!")

        # Step 3️⃣ Take a screenshot of the search results page
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = os.path.join("screenshots", "bing_search_results.png")

        time.sleep(2)  # small delay for full visual load
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 Screenshot saved: {screenshot_path}")

        # 🆕 Step 4️⃣ Click the first link, wait for page load, scroll, and screenshot
        print("🧭 Opening the first search result link...")
        try:
            first_link = page.query_selector("li.b_algo h2 a")
            if first_link:
                href = first_link.get_attribute("href")
                print(f"🔗 Navigating to: {href}")
                page.goto(href, wait_until="domcontentloaded")
                page.wait_for_load_state("networkidle")
                time.sleep(3)  # Allow elements to render

                # 🆕 Scroll slightly down before screenshot
                print("📜 Scrolling slightly down for a better screenshot...")
                page.mouse.wheel(0, 500)
                time.sleep(2)

                # Take screenshot of the opened page
                scorecard_screenshot = os.path.join("screenshots", "scorecard_page.png")
                page.screenshot(path=scorecard_screenshot, full_page=True)
                print(f"📸 Scorecard page screenshot saved: {scorecard_screenshot}")
            else:
                print("❌ No link found in search results!")
        except Exception as e:
            print(f"⚠️ Error opening or capturing first link: {e}")

        browser.close()


if __name__ == "__main__":
    locate_bing_search_bar()
