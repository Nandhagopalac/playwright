from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    # Launch Microsoft Edge with a little slowdown so we can watch
    browser = playwright.chromium.launch(channel="msedge", headless=False, slow_mo=900)
    context = browser.new_context()
    page = context.new_page()

    # Open Bing
    page.goto("https://www.bing.com/")

    # Use the correct selector for Bing’s search box
    search_box = page.wait_for_selector("textarea[name='q']", timeout=10000)
    search_box.fill("Tamil nadu")
    search_box.press("Enter")

    # Wait for search results
    page.wait_for_selector("text=Tamil nadu", timeout=10000)

    print("✅ Bing search completed successfully!")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
