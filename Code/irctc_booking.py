# irctc_booking_manual_captcha.py  ·  Python 3.10+  ·  Playwright ≥ 1.40
#
# 1. open IRCTC → close Ask-Disha → dismiss alert → click LOGIN
# 2. autofill username & password, then gives you 5 s to type the captcha and click SIGN IN
# 3. searches NDLS→BOM   11-Sep-2025   train 12954   class 3A
# 4. fills one passenger, pauses at UPI payment for manual completion

import asyncio, logging, time
from datetime import datetime
from playwright.async_api import async_playwright

CFG = {
    "username":  "ayyampudur",
    "password":  "Agalya@253520",
    "journey":   {"from": "NDLS", "to": "BOM", "date": "2025-09-11",
                  "train": "12954", "cls": "3A"},
    "passenger": {"name": "JOHN DOE", "age": 30, "gender": "M"},
    "upi":       "your_upi@okaxis",
    "timeouts":  {"elm": 30_000, "nav": 90_000},
    "headless":  False
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    handlers=[logging.FileHandler("irctc_booking.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)

async def smart_click(page, selector, timeout_ms=4000):
    end = time.time() + timeout_ms/1000
    while time.time() < end:
        try:
            el = await page.query_selector(selector)
            if el and await el.is_visible():
                await el.click()
                return True
        except:
            pass
        await page.wait_for_timeout(200)
    return False

async def main():
    t0 = time.time()
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(headless=CFG["headless"])
    ctx = await browser.new_context(viewport={"width": 1366, "height": 768})
    ctx.set_default_timeout(CFG["timeouts"]["elm"])
    ctx.set_default_navigation_timeout(CFG["timeouts"]["nav"])
    page = await ctx.new_page()
    page.on("dialog", lambda d: asyncio.create_task(d.accept()))
    await page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")

    # 1) open site
    log.info("Opening IRCTC …")
    await page.goto("https://www.irctc.co.in/nget/train-search", wait_until="load")
    await smart_click(page, "#disha-banner-close")
    await smart_click(page, 'button:has-text("OK")')
    await smart_click(page, 'text=LOGIN', timeout_ms=6000)
    log.info("Pop-ups cleared, LOGIN clicked.")

    # 2) login – fill credentials, pause for manual captcha
    await page.fill('input[formcontrolname="userid"]', CFG["username"])
    await page.fill('input[formcontrolname="password"]', CFG["password"])
    log.info("Username & password filled – you have 5 s to solve captcha and click SIGN IN.")
    await page.wait_for_timeout(5_000)               # 5-second pause for user captcha entry
    await page.wait_for_selector("text=Hi", timeout=120_000)
    log.info("Logged in.")

    # 3) search train
    j = CFG["journey"]
    await page.fill('input[placeholder*="From"]', j["from"])
    await page.keyboard.press("ArrowDown"); await page.keyboard.press("Enter")
    await page.fill('input[placeholder*="To"]', j["to"])
    await page.keyboard.press("ArrowDown"); await page.keyboard.press("Enter")
    await page.fill('input[placeholder="Journey Date*"]',
                    datetime.strptime(j["date"], "%Y-%m-%d").strftime("%d-%m-%Y"))
    await page.select_option('select[formcontrolname="journeyClass"]', j["cls"])
    await page.click('button:has-text("FIND TRAINS")')
    await page.wait_for_selector(f".train-list >> text={j['train']}", timeout=45_000)
    log.info("Train list loaded.")

    # 4) book class
    row = await page.wait_for_selector(f'tr:has-text("{j["train"]}")')
    book = await row.query_selector(f'td:has-text("{j["cls"]}") >> button:has-text("Book")')
    if not book:
        log.error("Desired class unavailable."); await browser.close(); await pw.stop(); return
    await book.click()

    # 5) passenger
    p = CFG["passenger"]
    await page.wait_for_selector('input[placeholder*="Passenger Name"]')
    await page.fill('input[placeholder*="Passenger Name"]', p["name"])
    await page.fill('input[placeholder="Age"]', str(p["age"]))
    await page.select_option('select[formcontrolname="passengerGender"]', p["gender"])
    await page.click('button:has-text("Continue")')

    # 6) payment pause
    await page.wait_for_selector("text=BHIM/UPI", timeout=30_000)
    await page.click("text=BHIM/UPI")
    await page.fill('input[placeholder*="UPI"]', CFG["upi"])
    log.info("Payment page – complete payment manually.")
    input("Pay in browser, then press Enter …")

    log.info("Finished – %.1f s total.", time.time() - t0)
    await browser.close(); await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
