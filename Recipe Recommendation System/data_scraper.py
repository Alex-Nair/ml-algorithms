from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless = False)
    page = browser.new_page()
    page.goto("https://www.bbc.co.uk/food/recipes/a-z/a/1#featured-content")
    print(page.title())
    browser.close()