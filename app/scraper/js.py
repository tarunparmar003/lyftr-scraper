from playwright.async_api import async_playwright


async def js_scrape(url):
    interactions = {
        "clicks": [],
        "scrolls": 0,
        "pages": [url]
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle")

        # Scroll depth ≥ 3
        for _ in range(3):
            await page.mouse.wheel(0, 4000)
            await page.wait_for_timeout(1500)
            interactions["scrolls"] += 1

        html = await page.content()
        await browser.close()

    return html, interactions
