import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(channel="msedge", headless=False, slow_mo=900)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bing.com/")
    # Use the correct selector for Bing’s search box
    search_box = page.wait_for_selector("textarea[name='q']", timeout=10000)
    search_box.fill("Tamil nadu images")
    search_box.press("Enter")
    # page.goto("https://www.bing.com/search?q=tamil+nadu+images&form=QBLH&sp=-1&ghc=1&lq=0&pq=tamil+nadu+image&sc=10-16&qs=n&sk=&cvid=132BD19831794BCDA3DB1B1812481F7B")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="Top 10 must visit places in").click()
    page1 = page1_info.value
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Next image result").click()
    page1.locator("iframe[name=\"tamil nadu images - Bing images - details\"]").content_frame.get_by_role("button", name="Close image").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
